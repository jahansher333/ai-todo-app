from typing import Dict, Any, Optional
from sqlmodel import Session, select, create_engine
from datetime import datetime
import uuid
import sys
import os
from dotenv import load_dotenv

import sys
import os
# Add the backend directory to the path so we can import models
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from models import Conversation, Message, MessageRole, Task
from ..services.agent_service import get_agent_service

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL)


class ChatService:
    def __init__(self):
        """
        Initialize the chat service
        """
        self.agent_service = get_agent_service()

    async def process_chat_message(self, user_id: str, message: str, conversation_id: Optional[str] = None, model_preferences: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a chat message and return the AI response
        """
        print(f"[debug] Processing chat message for user {user_id}, conversation {conversation_id}")

        # Create a database session
        with Session(engine) as session:
            # Get or create conversation
            if conversation_id:
                try:
                    conv_uuid = uuid.UUID(conversation_id)
                    conversation = session.get(Conversation, conv_uuid)

                    if not conversation:
                        # If conversation doesn't exist, create a new one
                        conversation = Conversation(
                            id=conv_uuid,
                            user_id=user_id,
                            title=message[:50] if len(message) > 50 else message
                        )
                        session.add(conversation)
                        session.commit()
                except ValueError:
                    # Invalid UUID, create new conversation
                    conversation = Conversation(
                        user_id=user_id,
                        title=message[:50] if len(message) > 50 else message
                    )
                    session.add(conversation)
            else:
                # Create new conversation
                conversation = Conversation(
                    user_id=user_id,
                    title=message[:50] if len(message) > 50 else message
                )
                session.add(conversation)

            session.commit()
            session.refresh(conversation)

            # Add user message to the conversation
            user_message = Message(
                conversation_id=conversation.id,
                role=MessageRole.user,
                content=message,
                timestamp=datetime.utcnow(),
                sequence_number=self._get_next_sequence_number(session, conversation.id)
            )
            session.add(user_message)
            session.commit()

            # Process the message with the agent
            agent_result = await self.agent_service.run_with_context(
                message=message,
                user_id=user_id,
                conversation_id=str(conversation.id),
                db_session=session
            )

            # Add assistant response to the conversation
            assistant_message = Message(
                conversation_id=conversation.id,
                role=MessageRole.assistant,
                content=agent_result["response"],
                timestamp=datetime.utcnow(),
                sequence_number=self._get_next_sequence_number(session, conversation.id, offset=1)
            )
            session.add(assistant_message)

            # Update conversation timestamp
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)

            session.commit()

            return {
                "conversation_id": str(conversation.id),
                "response": agent_result["response"],
                "action_taken": agent_result["action_taken"]
            }

    def _get_next_sequence_number(self, session: Session, conversation_id: uuid.UUID, offset: int = 0) -> int:
        """
        Get the next sequence number for a conversation
        """
        result = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.sequence_number.desc())
            .limit(1)
        ).first()

        if result:
            return result.sequence_number + 1 + offset
        else:
            return 1 + offset

    async def get_user_conversations(self, user_id: str) -> Dict[str, Any]:
        """
        Get all conversations for a user
        """
        with Session(engine) as session:
            # Query conversations for the user
            conversations = session.exec(
                select(Conversation)
                .where(Conversation.user_id == user_id)
                .order_by(Conversation.updated_at.desc())
            ).all()

            # Count messages for each conversation
            conversation_list = []
            for conv in conversations:
                message_count = session.exec(
                    select(Message).where(Message.conversation_id == conv.id)
                ).count()

                conversation_list.append({
                    "id": str(conv.id),
                    "title": conv.title,
                    "created_at": conv.created_at.isoformat(),
                    "updated_at": conv.updated_at.isoformat(),
                    "message_count": message_count
                })

            return {
                "conversations": conversation_list,
                "total_count": len(conversation_list),
                "limit": len(conversation_list),
                "offset": 0
            }

    async def get_conversation_messages(self, user_id: str, conversation_id: str) -> Dict[str, Any]:
        """
        Get messages for a specific conversation
        """
        with Session(engine) as session:
            # Verify that the conversation belongs to the user
            try:
                conv_uuid = uuid.UUID(conversation_id)
                conversation = session.get(Conversation, conv_uuid)

                if not conversation or str(conversation.user_id) != user_id:
                    return {"error": "Conversation not found or access denied", "messages": []}
            except ValueError:
                return {"error": "Invalid conversation ID", "messages": []}

            # Get messages for the conversation
            messages = session.exec(
                select(Message)
                .where(Message.conversation_id == conv_uuid)
                .order_by(Message.sequence_number)
            ).all()

            message_list = []
            for msg in messages:
                message_list.append({
                    "id": str(msg.id),
                    "role": msg.role.value,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat(),
                    "sequence_number": msg.sequence_number
                })

            return {
                "messages": message_list
            }


# Global chat service instance
chat_service = ChatService()