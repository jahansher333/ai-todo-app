from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select, update, delete
from typing import List, Optional
from datetime import datetime
import sys
import os
from ..database import engine
from ..middleware.jwt_middleware import get_current_user
import uuid

import sys
import os
# Add the backend directory to the path so we can import models
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from models import Task, User, PriorityEnum, RecurringEnum

router = APIRouter()

@router.get("/tasks", response_model=List[Task])
async def get_tasks(
    user_id: str,
    decoded_token: dict = Depends(get_current_user),
    status_filter: Optional[str] = Query(None, alias="status"),
    priority_filter: Optional[PriorityEnum] = Query(None, alias="priority"),
    search: Optional[str] = Query(None)
):
    # Verify that the user_id in the token matches the path user_id
    token_user_id = decoded_token.get("user_id")
    if token_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Token user_id does not match request user_id"
        )

    # Connect to database
    with Session(engine) as session:
        # Build query
        query = select(Task).where(Task.user_id == user_id)

        # Apply filters
        if status_filter:
            # Assuming status filter refers to completed status
            if status_filter.lower() == "completed":
                query = query.where(Task.completed == True)
            elif status_filter.lower() == "pending":
                query = query.where(Task.completed == False)

        if priority_filter:
            query = query.where(Task.priority == priority_filter)

        if search:
            query = query.where(Task.title.contains(search) | Task.description.contains(search))

        # Execute query
        tasks = session.exec(query).all()
        return tasks


@router.post("/tasks", response_model=Task)
async def create_task(
    user_id: str,
    task_data: Task,
    decoded_token: dict = Depends(get_current_user)
):
    # Verify that the user_id in the token matches the path user_id
    token_user_id = decoded_token.get("user_id")
    if token_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Token user_id does not match request user_id"
        )

    # Create task with the specified user_id
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        priority=task_data.priority,
        tags=task_data.tags if task_data.tags else [],
        due=task_data.due,
        recurring=task_data.recurring if task_data.recurring else RecurringEnum.none,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Save to database
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(
    user_id: str,
    task_id: str,
    task_data: Task,
    decoded_token: dict = Depends(get_current_user)
):
    # Verify that the user_id in the token matches the path user_id
    token_user_id = decoded_token.get("user_id")
    if token_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Token user_id does not match request user_id"
        )

    # Update task
    with Session(engine) as session:
        # First, verify the task belongs to the user
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to user"
            )

        # Update the task fields
        task.title = task_data.title
        task.description = task_data.description
        task.completed = task_data.completed
        task.priority = task_data.priority
        task.tags = task_data.tags if task_data.tags else []
        task.due = task_data.due
        task.recurring = task_data.recurring if task_data.recurring else RecurringEnum.none
        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)
        return task

@router.delete("/tasks/{task_id}")
async def delete_task(
    user_id: str,
    task_id: str,
    decoded_token: dict = Depends(get_current_user)
):
    # Verify that the user_id in the token matches the path user_id
    token_user_id = decoded_token.get("user_id")
    if token_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Token user_id does not match request user_id"
        )

    # Delete task
    with Session(engine) as session:
        # First, verify the task belongs to the user
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to user"
            )

        session.delete(task)
        session.commit()
        return {"message": "Task deleted successfully"}

@router.patch("/tasks/{task_id}/complete")
async def update_task_completion(
    user_id: str,
    task_id: str,
    completed: bool,
    decoded_token: dict = Depends(get_current_user)
):
    # Verify that the user_id in the token matches the path user_id
    token_user_id = decoded_token.get("user_id")
    if token_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Token user_id does not match request user_id"
        )

    # Update task completion status
    with Session(engine) as session:
        # First, verify the task belongs to the user
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to user"
            )

        task.completed = completed
        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)
        return task