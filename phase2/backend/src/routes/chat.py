"""
Chat API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid
from ..middleware.jwt_middleware import get_current_user
from ..services.chat_service import ChatService
from datetime import datetime

router = APIRouter(prefix="/api", tags=["chat"])

# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    model_preferences: Optional[Dict[str, Any]] = {"temperature": 0.7}


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    action_taken: str
    timestamp: datetime


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(user_id: str, request: ChatRequest, current_user: dict = Depends(get_current_user)):
    """
    Chat endpoint that processes natural language messages and returns AI responses
    """
    try:
        # Verify that the user_id in the path matches the authenticated user
        if current_user.get("user_id") != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID does not match authenticated user"
            )

        # Process the chat request
        chat_service = ChatService()
        result = await chat_service.process_chat_message(
            user_id=user_id,
            message=request.message,
            conversation_id=request.conversation_id,
            model_preferences=request.model_preferences
        )

        return ChatResponse(
            conversation_id=result["conversation_id"],
            response=result["response"],
            action_taken=result["action_taken"],
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )


@router.get("/{user_id}/conversations")
async def get_conversations(user_id: str, current_user: dict = Depends(get_current_user)):
    """
    Get user's conversations
    """
    try:
        # Verify that the user_id in the path matches the authenticated user
        if current_user.get("user_id") != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID does not match authenticated user"
            )

        # Get user's conversations
        chat_service = ChatService()
        conversations = await chat_service.get_user_conversations(user_id)
        return conversations
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving conversations: {str(e)}"
        )


@router.get("/{user_id}/conversations/{conversation_id}/messages")
async def get_messages(user_id: str, conversation_id: str, current_user: dict = Depends(get_current_user)):
    """
    Get messages from a specific conversation
    """
    try:
        # Verify that the user_id in the path matches the authenticated user
        if current_user.get("user_id") != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID does not match authenticated user"
            )

        # Get messages from the conversation
        chat_service = ChatService()
        messages = await chat_service.get_conversation_messages(user_id, conversation_id)
        return messages
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving messages: {str(e)}"
        )


# Health check endpoint
@router.get("/")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "service": "Todo AI-Powered Chatbot API"}


# Include this router in the main app
def include_router(app):
    app.include_router(router)