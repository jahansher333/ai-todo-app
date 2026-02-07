from mcp.server.fastmcp import FastMCP
from sqlmodel import Session
from datetime import datetime
import uuid
from typing import List, Dict, Any
from backend.models import Task, User
from src.database import engine

# Create the MCP server
mcp = FastMCP("Todo AI-Powered Chatbot MCP Server", json_response=True)


@mcp.tool()
def add_task(user_id: str, title: str, description: str = None, priority: str = "medium") -> Dict[str, Any]:
    """
    Add a new task for a user
    """
    try:
        with Session(engine) as session:
            task = Task(
                user_id=user_id,
                title=title,
                description=description,
                completed=False,
                priority=priority
            )
            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "task_id": task.id,
                "status": "created",
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "priority": task.priority
            }
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }


@mcp.tool()
def list_tasks(user_id: str, status: str = "all", limit: int = 10) -> List[Dict[str, Any]]:
    """
    List tasks for a user with optional status filter
    """
    try:
        with Session(engine) as session:
            from sqlmodel import select

            query = select(Task).where(Task.user_id == user_id)

            if status != "all":
                if status == "completed":
                    query = query.where(Task.completed == True)
                elif status == "pending":
                    query = query.where(Task.completed == False)

            # Apply limit
            query = query.limit(limit)

            tasks = session.exec(query).all()

            return [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "created_at": task.created_at.isoformat() if task.created_at else None
                }
                for task in tasks
            ]
    except Exception as e:
        return [{"error": str(e), "status": "failed"}]


@mcp.tool()
def complete_task(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    Mark a task as complete
    """
    try:
        with Session(engine) as session:
            from sqlmodel import select

            task = session.exec(
                select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
            ).first()

            if not task:
                return {
                    "error": f"Task with ID {task_id} not found for user {user_id}",
                    "status": "not_found"
                }

            task.completed = True
            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "task_id": task.id,
                "status": "completed",
                "title": task.title
            }
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }


@mcp.tool()
def delete_task(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    Delete a task
    """
    try:
        with Session(engine) as session:
            from sqlmodel import select

            task = session.exec(
                select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
            ).first()

            if not task:
                return {
                    "error": f"Task with ID {task_id} not found for user {user_id}",
                    "status": "not_found"
                }

            session.delete(task)
            session.commit()

            return {
                "task_id": task.id,
                "status": "deleted",
                "title": task.title
            }
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }


@mcp.tool()
def update_task(user_id: str, task_id: str, title: str = None, description: str = None, priority: str = None) -> Dict[str, Any]:
    """
    Update a task
    """
    try:
        with Session(engine) as session:
            from sqlmodel import select

            task = session.exec(
                select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
            ).first()

            if not task:
                return {
                    "error": f"Task with ID {task_id} not found for user {user_id}",
                    "status": "not_found"
                }

            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if priority is not None:
                task.priority = priority

            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "task_id": task.id,
                "status": "updated",
                "title": task.title
            }
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }


if __name__ == "__main__":
    # Run the MCP server using streamable-http transport
    mcp.run(transport="streamable-http")