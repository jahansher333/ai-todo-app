from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

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
            import uuid
            self.id = str(uuid.uuid4())

# Create database and tables
def create_db_and_tables():
    from .main import engine
    SQLModel.metadata.create_all(engine)