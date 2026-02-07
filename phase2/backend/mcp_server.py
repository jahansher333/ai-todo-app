"""
MCP Server for Todo AI-Powered Chatbot
Implements the Official MCP SDK with 5 tools for task management
"""
import asyncio
from typing import Dict, Any, List
from fastapi import HTTPException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import sys
import os
# Add the backend directory to the path so we can import models
sys.path.insert(0, os.path.dirname(__file__))
from models import Task, Conversation, Message
from sqlmodel import Session, select, func
from src.database import engine
import uuid
from datetime import datetime


class MCPServer:
    """
    MCP Server implementation with 5 tools for task management
    """

    def __init__(self):
        self.tools = {
            "add_task": self.add_task,
            "list_tasks": self.list_tasks,
            "complete_task": self.complete_task,
            "delete_task": self.delete_task,
            "update_task": self.update_task,
        }

    async def add_task(self, user_id: str, title: str, description: str = "", priority: str = "medium", tags: str = "", due: str = "", recurring: str = "none") -> Dict[str, Any]:
        """
        Add a new task
        """
        try:
            with Session(engine) as session:
                task = Task(
                    user_id=user_id,
                    title=title,
                    description=description or "",
                    completed=False,
                    priority=priority,
                    tags=tags or "",
                    due=due or None,
                    recurring=recurring
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

    async def list_tasks(self, user_id: str, status: str = "all", limit: int = 10) -> List[Dict[str, Any]]:
        """
        List tasks with optional status filter
        """
        try:
            with Session(engine) as session:
                query = select(Task).where(Task.user_id == user_id)

                if status != "all":
                    if status == "completed":
                        query = query.where(Task.completed == True)
                    elif status == "pending":
                        query = query.where(Task.completed == False)

                # Apply limit if specified
                if limit is not None:
                    query = query.limit(limit)

                tasks = session.exec(query).all()

                return [
                    {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat() if task.created_at else None
                    }
                    for task in tasks
                ]
        except Exception as e:
            return [{"error": str(e), "status": "failed"}]

    async def complete_task(self, user_id: str, task_id: str = None, task_title: str = None) -> Dict[str, Any]:
        """
        Mark a task as complete - can accept either task_id or task_title
        """
        try:
            with Session(engine) as session:
                task = None

                # If task_id is provided, use it directly
                if task_id:
                    task = session.exec(
                        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
                    ).first()

                # If task_id is not provided but task_title is, search by title
                elif task_title:
                    # Look for exact match first
                    task = session.exec(
                        select(Task).where(Task.title == task_title).where(Task.user_id == user_id)
                    ).first()

                    # If not found, try partial match (case-insensitive) - simple approach for compatibility
                    if not task:
                        try:
                            # Try to find task with case-insensitive partial match
                            tasks = session.exec(
                                select(Task).where(Task.user_id == user_id)
                            ).all()

                            # Manually search for case-insensitive partial match
                            for t in tasks:
                                if task_title.lower() in t.title.lower():
                                    task = t
                                    break
                        except:
                            # If all matching fails, just return the exact match result (which is None)
                            pass

                if not task:
                    task_identifier = task_id if task_id else f"title '{task_title}'"
                    return {
                        "error": f"Task with {task_identifier} not found for user {user_id}",
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

    async def delete_task(self, user_id: str, task_id: str = None, task_title: str = None) -> Dict[str, Any]:
        """
        Delete a task - can accept either task_id or task_title
        """
        try:
            with Session(engine) as session:
                task = None

                # If task_id is provided, use it directly
                if task_id:
                    task = session.exec(
                        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
                    ).first()

                # If task_id is not provided but task_title is, search by title
                elif task_title:
                    # Look for exact match first
                    task = session.exec(
                        select(Task).where(Task.title == task_title).where(Task.user_id == user_id)
                    ).first()

                    # If not found, try partial match (case-insensitive) - simple approach for compatibility
                    if not task:
                        try:
                            # Try to find task with case-insensitive partial match
                            tasks = session.exec(
                                select(Task).where(Task.user_id == user_id)
                            ).all()

                            # Manually search for case-insensitive partial match
                            for t in tasks:
                                if task_title.lower() in t.title.lower():
                                    task = t
                                    break
                        except:
                            # If all matching fails, just return the exact match result (which is None)
                            pass

                if not task:
                    task_identifier = task_id if task_id else f"title '{task_title}'"
                    return {
                        "error": f"Task with {task_identifier} not found for user {user_id}",
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

    async def update_task(self, user_id: str, task_id: str = None, task_title: str = None, title: str = None, description: str = None, priority: str = None, due: str = None, tags: str = None) -> Dict[str, Any]:
        """
        Update a task - can accept either task_id or task_title
        """
        try:
            with Session(engine) as session:
                task = None

                # If task_id is provided, use it directly
                if task_id:
                    task = session.exec(
                        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
                    ).first()

                # If task_id is not provided but task_title is, search by title
                elif task_title:
                    # Look for exact match first
                    task = session.exec(
                        select(Task).where(Task.title == task_title).where(Task.user_id == user_id)
                    ).first()

                    # If not found, try partial match (case-insensitive) - simple approach for compatibility
                    if not task:
                        try:
                            # Try to find task with case-insensitive partial match
                            tasks = session.exec(
                                select(Task).where(Task.user_id == user_id)
                            ).all()

                            # Manually search for case-insensitive partial match
                            for t in tasks:
                                if task_title.lower() in t.title.lower():
                                    task = t
                                    break
                        except:
                            # If all matching fails, just return the exact match result (which is None)
                            pass

                if not task:
                    task_identifier = task_id if task_id else f"title '{task_title}'"
                    return {
                        "error": f"Task with {task_identifier} not found for user {user_id}",
                        "status": "not_found"
                    }

                if title is not None:
                    task.title = title
                if description is not None:
                    task.description = description
                if priority is not None:
                    task.priority = priority
                if due is not None:
                    task.due = due
                if tags is not None:
                    task.tags = tags

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


# Global MCP server instance
mcp_server = MCPServer()

# Export the tool functions directly at the module level
async def add_task(user_id: str, title: str, description: str = None, priority: str = "medium", tags: str = None, due: str = None, recurring: str = "none") -> Dict[str, Any]:
    return await mcp_server.add_task(user_id, title, description, priority, tags, due, recurring)

async def list_tasks(user_id: str, status: str = "all") -> List[Dict[str, Any]]:
    return await mcp_server.list_tasks(user_id, status)

async def complete_task(user_id: str, task_id: str = None, task_title: str = None) -> Dict[str, Any]:
    return await mcp_server.complete_task(user_id, task_id, task_title)

async def delete_task(user_id: str, task_id: str = None, task_title: str = None) -> Dict[str, Any]:
    return await mcp_server.delete_task(user_id, task_id, task_title)

async def update_task(user_id: str, task_id: str = None, task_title: str = None, title: str = None, description: str = None, priority: str = None, due: str = None, tags: str = None) -> Dict[str, Any]:
    return await mcp_server.update_task(user_id, task_id, task_title, title, description, priority, due, tags)

async def list_tasks(user_id: str, status: str = "all") -> List[Dict[str, Any]]:
    return await mcp_server.list_tasks(user_id, status)

async def complete_task(user_id: str, task_id: str = None, task_title: str = None) -> Dict[str, Any]:
    return await mcp_server.complete_task(user_id, task_id, task_title)

async def delete_task(user_id: str, task_id: str = None, task_title: str = None) -> Dict[str, Any]:
    return await mcp_server.delete_task(user_id, task_id, task_title)



async def handle_tool_request(tool_request: Dict[str, Any], user_token: str = None) -> Dict[str, Any]:
    """
    Handle incoming tool requests from the agent
    """
    tool_name = tool_request.get("name")
    parameters = tool_request.get("parameters", {})

    # Extract user_id from token or parameters
    user_id = parameters.get("user_id")
    if not user_id and user_token:
        # In a real implementation, you would decode the JWT to get the user_id
        # For now, we'll assume the user_id is passed in the parameters
        pass

    if not user_id:
        return {"error": "user_id is required", "status": "failed"}

    # Remove user_id from parameters since it's handled separately
    if "user_id" in parameters:
        del parameters["user_id"]

    # Add user_id to parameters for the tool functions
    parameters["user_id"] = user_id

    if tool_name in mcp_server.tools:
        try:
            # Call the appropriate tool function with the parameters
            tool_func = mcp_server.tools[tool_name]
            # Remove the user_id from parameters when passing to the function
            user_id = parameters.pop("user_id")

            # Call the function with user_id as a separate parameter
            if tool_name == "add_task":
                result = await tool_func(user_id, **parameters)
            elif tool_name == "list_tasks":
                result = await tool_func(user_id, **parameters)
            elif tool_name == "complete_task":
                result = await tool_func(user_id, **parameters)
            elif tool_name == "delete_task":
                result = await tool_func(user_id, **parameters)
            elif tool_name == "update_task":
                result = await tool_func(user_id, **parameters)

            return result
        except Exception as e:
            return {
                "error": f"Error executing {tool_name}: {str(e)}",
                "status": "failed"
            }
    else:
        return {
            "error": f"Unknown tool: {tool_name}",
            "status": "failed"
        }


if __name__ == "__main__":
    # Example usage
    async def main():
        # Example of how to use the MCP server
        tool_request = {
            "name": "add_task",
            "parameters": {
                "user_id": "user123",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread"
            }
        }

        result = await handle_tool_request(tool_request)
        print(f"Result: {result}")

    # Run the example
    asyncio.run(main())