from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
import uuid

# Define an enumeration for priority levels
class PriorityEnum(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"

# Define an enumeration for recurring patterns
class RecurringEnum(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    none = "none"

# User model
class User(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    email: str = Field(default=None)
    password_hash: str = Field(default=None)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

# Task model
class Task(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)  # Will be auto-generated
    user_id: Optional[str] = Field(default=None)  # Foreign key to User
    title: str = Field(default=None)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    priority: PriorityEnum = Field(default=PriorityEnum.medium)
    tags: Optional[str] = Field(default=None)  # Store tags as JSON string instead of list
    due: Optional[datetime] = Field(default=None)
    recurring: Optional[RecurringEnum] = Field(default=RecurringEnum.none)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def __init__(self, **data):
        super().__init__(**data)
        # Auto-generate ID if not provided
        if self.id is None:
            self.id = str(uuid.uuid4())

class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"

# Conversation model
class Conversation(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    user_id: str = Field(default=None, index=True)  # Foreign Key to User
    title: Optional[str] = Field(default=None, max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    def __init__(self, **data):
        super().__init__(**data)
        # Auto-generate ID if not provided
        if self.id is None:
            self.id = str(uuid.uuid4())

# Message model
class Message(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    conversation_id: str = Field(default=None, index=True, foreign_key="conversation.id")
    role: MessageRole = Field(default=None)
    content: str = Field(default=None)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata_: Optional[str] = Field(default=None)  # Store as JSON string
    sequence_number: int = Field(default=0, index=True)

    def __init__(self, **data):
        super().__init__(**data)
        # Auto-generate ID if not provided
        if self.id is None:
            self.id = str(uuid.uuid4())

# Create database and tables
def create_db_and_tables():
    from database import engine
    SQLModel.metadata.create_all(engine)