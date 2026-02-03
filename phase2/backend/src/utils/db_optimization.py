"""
Database Optimization Utilities
"""
from sqlmodel import create_engine, Session, select, and_, or_
from models import Task, Conversation, Message
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid


class DatabaseOptimizer:
    """
    Utility class for database optimizations
    """

    @staticmethod
    def get_optimized_task_query(
        user_id: uuid.UUID,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        search_query: Optional[str] = None,
        limit: Optional[int] = 10
    ):
        """
        Get an optimized query for fetching tasks with filters
        """
        from models import TaskStatus, TaskPriority

        query = select(Task).where(Task.user_id == user_id)

        # Apply status filter
        if status and status != "all":
            try:
                status_enum = TaskStatus(status)
                query = query.where(Task.status == status_enum)
            except ValueError:
                pass  # Invalid status, ignore filter

        # Apply priority filter
        if priority and priority != "all":
            try:
                priority_enum = TaskPriority(priority)
                query = query.where(Task.priority == priority_enum)
            except ValueError:
                pass  # Invalid priority, ignore filter

        # Apply search filter
        if search_query:
            query = query.where(
                Task.title.contains(search_query) |
                (Task.description.contains(search_query) if Task.description else False)
            )

        # Apply limit
        if limit:
            query = query.limit(limit)

        # Order by creation date descending
        query = query.order_by(Task.created_at.desc())

        return query

    @staticmethod
    def get_optimized_conversation_query(user_id: uuid.UUID, limit: int = 20):
        """
        Get an optimized query for fetching user conversations
        """
        query = select(Conversation).where(Conversation.user_id == user_id)
        query = query.order_by(Conversation.updated_at.desc()).limit(limit)
        return query

    @staticmethod
    def get_optimized_message_query(conversation_id: uuid.UUID, limit: int = 50):
        """
        Get an optimized query for fetching messages in a conversation
        """
        query = select(Message).where(Message.conversation_id == conversation_id)
        query = query.order_by(Message.sequence_number.asc()).limit(limit)
        return query

    @staticmethod
    def get_recent_tasks_for_user(user_id: uuid.UUID, days: int = 30) -> select:
        """
        Get tasks created within the specified number of days
        """
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        query = select(Task).where(
            and_(
                Task.user_id == user_id,
                Task.created_at >= cutoff_date
            )
        )
        return query.order_by(Task.created_at.desc())

    @staticmethod
    def get_completed_tasks_count(user_id: uuid.UUID) -> select:
        """
        Get count of completed tasks for a user
        """
        from models import TaskStatus
        query = select(Task).where(
            and_(
                Task.user_id == user_id,
                Task.status == TaskStatus.completed
            )
        )
        return query

    @staticmethod
    def get_pending_tasks_count(user_id: uuid.UUID) -> select:
        """
        Get count of pending tasks for a user
        """
        from models import TaskStatus
        query = select(Task).where(
            and_(
                Task.user_id == user_id,
                Task.status == TaskStatus.pending
            )
        )
        return query

    @staticmethod
    def bulk_update_task_status(task_ids: List[uuid.UUID], new_status: str) -> str:
        """
        Generate SQL for bulk updating task status
        """
        from models import TaskStatus
        try:
            status_enum = TaskStatus(new_status)
            return f"UPDATE tasks SET status = '{status_enum.value}', updated_at = NOW() WHERE id = ANY(%s)"
        except ValueError:
            raise ValueError(f"Invalid status: {new_status}")

    @staticmethod
    def get_tasks_summary(user_id: uuid.UUID) -> Dict[str, Any]:
        """
        Get a summary of tasks for a user
        """
        # This would typically be implemented with raw SQL for performance
        # For now, we'll return a structure that would be populated by a query
        return {
            "total_tasks": 0,
            "completed_tasks": 0,
            "pending_tasks": 0,
            "high_priority_tasks": 0,
            "overdue_tasks": 0,
            "this_week_tasks": 0
        }


# Index suggestions as comments since SQLModel doesn't directly support index creation
"""
Suggested database indexes for optimal performance:

1. Task table indexes:
   - CREATE INDEX idx_tasks_user_id ON tasks(user_id);
   - CREATE INDEX idx_tasks_status ON tasks(status);
   - CREATE INDEX idx_tasks_priority ON tasks(priority);
   - CREATE INDEX idx_tasks_created_at ON tasks(created_at);
   - CREATE INDEX idx_tasks_due_date ON tasks(due_date);
   - CREATE INDEX idx_tasks_user_status ON tasks(user_id, status);
   - CREATE INDEX idx_tasks_user_priority ON tasks(user_id, priority);

2. Conversation table indexes:
   - CREATE INDEX idx_conversations_user_id ON conversations(user_id);
   - CREATE INDEX idx_conversations_updated_at ON conversations(updated_at);
   - CREATE INDEX idx_conversations_user_active ON conversations(user_id, is_active);

3. Message table indexes:
   - CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
   - CREATE INDEX idx_messages_role ON messages(role);
   - CREATE INDEX idx_messages_timestamp ON messages(timestamp);
   - CREATE INDEX idx_messages_conversation_seq ON messages(conversation_id, sequence_number);
"""


def create_indexes_sql() -> List[str]:
    """
    Return SQL statements to create recommended indexes
    """
    return [
        # Task table indexes
        "CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);",
        "CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);",
        "CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);",
        "CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at);",
        "CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);",
        "CREATE INDEX IF NOT EXISTS idx_tasks_user_status ON tasks(user_id, status);",
        "CREATE INDEX IF NOT EXISTS idx_tasks_user_priority ON tasks(user_id, priority);",

        # Conversation table indexes
        "CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);",
        "CREATE INDEX IF NOT EXISTS idx_conversations_updated_at ON conversations(updated_at);",
        "CREATE INDEX IF NOT EXISTS idx_conversations_user_active ON conversations(user_id, is_active);",

        # Message table indexes
        "CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);",
        "CREATE INDEX IF NOT EXISTS idx_messages_role ON messages(role);",
        "CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);",
        "CREATE INDEX IF NOT EXISTS idx_messages_conversation_seq ON messages(conversation_id, sequence_number);"
    ]


# Global optimizer instance
db_optimizer = DatabaseOptimizer()