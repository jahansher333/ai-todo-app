"""
Agent Service for AI-powered chatbot
"""
from __future__ import annotations
import asyncio
from typing import Dict, Any, Optional
from openai import AsyncOpenAI
from mcp_server import add_task, list_tasks, complete_task, delete_task, update_task
import sys
import os
import json
# Add the backend directory to the path so we can import models
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from models import Conversation, Message, MessageRole
from sqlmodel import Session
import uuid
import os
from dotenv import load_dotenv
from ..database import engine

load_dotenv()

from mcp_server import handle_tool_request


class AgentService:
    def __init__(self, model: str = "llama-3.1-8b-instant", api_key: str = None):
        """
        Initialize the agent service with MCP tools using OpenAI SDK
        """
        if not api_key:
            api_key = os.getenv("GROQ_API_KEY") or os.getenv("GROK_API_KEY")  # Support both environment variable names

        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")

        print(f"[debug] Initializing agent with model: {model}")

        # Initialize the OpenAI client
        self.openai_client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"  # Using Groq as the provider
        )

        self.model_name = model
        self.api_key = api_key

        # Define the tools that correspond to our MCP server functions
        # Note: We don't include user_id in the function parameters since it's passed separately
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task for a user. Extract title, description, priority, due date, and tags from natural language.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Task title"},
                            "description": {"type": "string", "description": "Task description"},
                            "priority": {"type": "string", "description": "Task priority (high, medium, low)", "default": "medium"},
                            "due": {"type": ["string", "null"], "description": "Due date in YYYY-MM-DD format"},
                            "tags": {"type": ["string", "null"], "description": "Comma-separated tags"}
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List tasks for a user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "description": "Filter by status: all, completed, pending", "default": "all"},
                            "limit": {"type": "integer", "description": "Maximum number of tasks to return", "default": 10}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as complete",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": ["string", "null"], "description": "Task ID to complete"},
                            "task_title": {"type": ["string", "null"], "description": "Task title to complete"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": ["string", "null"], "description": "Task ID to delete"},
                            "task_title": {"type": ["string", "null"], "description": "Task title to delete"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": ["string", "null"], "description": "Task ID to update"},
                            "task_title": {"type": ["string", "null"], "description": "Task title to update"},
                            "title": {"type": ["string", "null"], "description": "New task title"},
                            "description": {"type": ["string", "null"], "description": "New task description"}
                        }
                    }
                }
            }
        ]

    async def process_message(self, message: str, user_id: str, db_session: Session) -> Dict[str, Any]:
        """
        Process a user message using the agent and MCP tools with OpenAI function calling
        """
        print(f"[debug] Processing message for user {user_id}: {message}")

        try:
            # Prepare the messages for the AI
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant that helps users manage their tasks through natural language. "
                               "You can add, list, complete, delete, and update tasks. "
                               "Always be polite and confirm actions with users. "
                               "When a user wants to add a task, look for titles, dates, priorities, and tags in their message. "
                               "For example, if someone says 'create task milk with date tomorrow and tag grocery', "
                               "extract the task title as 'milk', set a due date for tomorrow, and add 'grocery' as a tag. "
                               "Always try to extract as much detail as possible from natural language."
                },
                {
                    "role": "user",
                    "content": message
                }
            ]

            # Prepare the system message to guide the AI properly
            system_message = {
                "role": "system",
                "content": "You are a helpful AI assistant that helps users manage their tasks through natural language. "
                           "You can add, list, complete, delete, and update tasks. "
                           "Always be polite and confirm actions with users. "
                           "When a user wants to add a task, look for titles, dates, priorities, and tags in their message. "
                           "For example, if someone says 'create task milk with date tomorrow and tag grocery', "
                           "extract the task title as 'milk', set a due date for tomorrow (in YYYY-MM-DD format), and add 'grocery' as a tag. "
                           "Always return valid JSON with proper string values. For dates, use YYYY-MM-DD format. "
                           "Do not return Python expressions or code - only valid JSON values."
            }

            # Prepare the messages for the AI
            ai_messages = [system_message] + [
                {
                    "role": "user",
                    "content": message
                }
            ]

            # Call the AI with tool capability
            response = await self.openai_client.chat.completions.create(
                model=self.model_name,
                messages=ai_messages,
                tools=self.tools,
                tool_choice="auto"  # Let the AI decide when to call tools
            )

            response_message = response.choices[0].message

            # Check if the AI wants to call any tools
            tool_calls = response_message.tool_calls
            if tool_calls:
                # Execute the requested tools
                tool_results = []
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    try:
                        function_args = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        # If JSON parsing fails, return an error
                        result = {"error": f"Invalid JSON arguments: {tool_call.function.arguments}"}
                    else:
                        # Ensure user_id is included in the function arguments
                        function_args["user_id"] = user_id

                        # Call the appropriate MCP tool
                        # Handle cases where AI might provide task title instead of ID for operations
                        if function_name == "add_task":
                            result = await add_task(**function_args)
                        elif function_name == "list_tasks":
                            result = await list_tasks(**function_args)
                        elif function_name == "complete_task":
                            # Check if what's provided as task_id is actually a task title
                            if "task_id" in function_args and function_args["task_id"]:
                                # Check if the provided task_id looks like a UUID or is actually a task title
                                import re
                                task_id_value = function_args["task_id"]
                                # If it contains spaces or common task words, it's probably a title
                                if ' ' in task_id_value or not re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', task_id_value):
                                    # Move the value from task_id to task_title
                                    function_args["task_title"] = task_id_value
                                    del function_args["task_id"]

                            # If no task_id provided but message contains task title, extract it
                            if "task_id" not in function_args and "task_title" not in function_args:
                                # Try to get task title from the original message
                                import re
                                # Look for patterns like "complete task X" or "mark task X as complete"
                                match = re.search(r"(?:complete|finish|done|mark as complete)\s+(?:task\s+)?(.+?)(?:\s|$|[.!?])", message, re.IGNORECASE)
                                if not match:
                                    match = re.search(r"(?:task\s+)?(.+?)(?:\s+(?:as\s+)?(?:complete|finished|done))", message, re.IGNORECASE)

                                if match:
                                    task_title = match.group(1).strip()
                                    if task_title:
                                        function_args["task_title"] = task_title

                            result = await complete_task(**function_args)
                        elif function_name == "delete_task":
                            # Check if what's provided as task_id is actually a task title
                            if "task_id" in function_args and function_args["task_id"]:
                                # Check if the provided task_id looks like a UUID or is actually a task title
                                import re
                                task_id_value = function_args["task_id"]
                                # If it contains spaces or common task words, it's probably a title
                                if ' ' in task_id_value or not re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', task_id_value):
                                    # Move the value from task_id to task_title
                                    function_args["task_title"] = task_id_value
                                    del function_args["task_id"]

                            # If no task_id provided but message contains task title, extract it
                            if "task_id" not in function_args and "task_title" not in function_args:
                                # Try to get task title from the original message
                                import re
                                # Look for patterns like "delete task X" or "remove task X"
                                match = re.search(r"(?:delete|remove|erase)\s+(?:task\s+)?(.+?)(?:\s|$|[.!?])", message, re.IGNORECASE)
                                if not match:
                                    match = re.search(r"(?:task\s+)('?.+?'?)(?:\s+(?:please\s+)?(?:delete|remove|erase))", message, re.IGNORECASE)

                                if match:
                                    task_title = match.group(1).strip().strip("'\"")
                                    if task_title:
                                        function_args["task_title"] = task_title

                            result = await delete_task(**function_args)
                        elif function_name == "update_task":
                            # Check if what's provided as task_id is actually a task title
                            if "task_id" in function_args and function_args["task_id"]:
                                # Check if the provided task_id looks like a UUID or is actually a task title
                                import re
                                task_id_value = function_args["task_id"]
                                # If it contains spaces or common task words, it's probably a title
                                if ' ' in task_id_value or not re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', task_id_value):
                                    # Move the value from task_id to task_title
                                    function_args["task_title"] = task_id_value
                                    del function_args["task_id"]

                            # If no task_id provided but message contains task title, extract it
                            if "task_id" not in function_args and "task_title" not in function_args:
                                # Try to get task title from the original message
                                import re
                                # Look for patterns like "update task X" or "change task X"
                                match = re.search(r"(?:update|modify|change|edit)\s+(?:task\s+)?(.+?)(?:\s+(?:to|with)|\s*$|[.!?])", message, re.IGNORECASE)
                                if not match:
                                    match = re.search(r"(?:task\s+)('?.+?'?)(?:\s+(?:update|modify|change|edit))", message, re.IGNORECASE)

                                if match:
                                    task_title = match.group(1).strip().strip("'\"")
                                    if task_title:
                                        function_args["task_title"] = task_title

                            result = await update_task(**function_args)
                        else:
                            result = {"error": f"Unknown tool: {function_name}"}

                    # Append the result regardless of whether there was an error
                    tool_results.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(result)
                    })

                # Get final response from AI with tool results
                final_messages = ai_messages + [response_message] + tool_results
                final_response = await self.openai_client.chat.completions.create(
                    model=self.model_name,
                    messages=final_messages
                )

                # Determine action taken based on tools called
                action_taken = "_".join([tc.function.name for tc in tool_calls]) if tool_calls else "unknown"

                return {
                    "response": final_response.choices[0].message.content,
                    "action_taken": action_taken,
                    "tool_calls": [tc.function.name for tc in tool_calls] if tool_calls else []
                }
            else:
                # No tools needed, return direct response from AI
                response_content = response_message.content or f"I understand you said: '{message}'. I can help you manage tasks. You can say things like 'create task milk with date tomorrow and tag grocery', 'show my tasks', or 'complete task milk'."

                return {
                    "response": response_content,
                    "action_taken": "direct_response",
                    "tool_calls": []
                }

        except Exception as e:
            print(f"[debug] Error processing message with agent: {str(e)}")
            return {
                "response": f"I encountered an error processing your request: {str(e)}",
                "action_taken": "error",
                "tool_calls": []
            }

        except Exception as e:
            print(f"[debug] Error processing message with agent: {str(e)}")
            return {
                "response": f"I encountered an error processing your request: {str(e)}",
                "action_taken": "error"
            }

    async def run_with_context(self, message: str, user_id: str, conversation_id: Optional[str], db_session: Session) -> Dict[str, Any]:
        """
        Run the agent with conversation context
        """
        print(f"[debug] Running agent with context for conversation {conversation_id}")

        # Process the message
        result = await self.process_message(message, user_id, db_session)

        return result


# Global agent service instance
agent_service = None


def get_agent_service() -> AgentService:
    """
    Get or create the agent service instance
    """
    global agent_service

    if agent_service is None:
        model = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
        api_key = os.getenv("GROQ_API_KEY") or os.getenv("GROK_API_KEY")  # Support both environment variable names

        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")

        agent_service = AgentService(model=model, api_key=api_key)

    return agent_service