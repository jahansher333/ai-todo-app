"""
Agent Runner for Todo AI-Powered Chatbot
Uses OpenAI Agents SDK with MCP tools
"""
from __future__ import annotations

import asyncio
from typing import Dict, Any, List, Optional
from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
import os
from dotenv import load_dotenv
from mcp_server import handle_tool_request

load_dotenv()

# Disable tracing for cleaner output
set_tracing_disabled(True)

# Define the tools using the MCP server functions
@function_tool
async def add_task(user_id: str, title: str, description: str = None) -> Dict[str, Any]:
    """Add a new task to the user's task list."""
    print(f"[debug] Adding task: {title} for user {user_id}")
    tool_request = {
        "name": "add_task",
        "parameters": {
            "user_id": user_id,
            "title": title,
            "description": description
        }
    }
    result = await handle_tool_request(tool_request)
    return result

@function_tool
async def list_tasks(user_id: str, status: str = "all") -> List[Dict[str, Any]]:
    """List tasks for the user, optionally filtered by status."""
    print(f"[debug] Listing tasks for user {user_id}, status: {status}")
    tool_request = {
        "name": "list_tasks",
        "parameters": {
            "user_id": user_id,
            "status": status
        }
    }
    result = await handle_tool_request(tool_request)
    return result

@function_tool
async def complete_task(user_id: str, task_id: str) -> Dict[str, Any]:
    """Mark a task as complete."""
    print(f"[debug] Completing task {task_id} for user {user_id}")
    tool_request = {
        "name": "complete_task",
        "parameters": {
            "user_id": user_id,
            "task_id": task_id
        }
    }
    result = await handle_tool_request(tool_request)
    return result

@function_tool
async def delete_task(user_id: str, task_id: str) -> Dict[str, Any]:
    """Delete a task from the user's list."""
    print(f"[debug] Deleting task {task_id} for user {user_id}")
    tool_request = {
        "name": "delete_task",
        "parameters": {
            "user_id": user_id,
            "task_id": task_id
        }
    }
    result = await handle_tool_request(tool_request)
    return result

@function_tool
async def update_task(user_id: str, task_id: str, title: str = None, description: str = None) -> Dict[str, Any]:
    """Update a task's title or description."""
    print(f"[debug] Updating task {task_id} for user {user_id}")
    params = {
        "user_id": user_id,
        "task_id": task_id
    }
    if title:
        params["title"] = title
    if description:
        params["description"] = description

    tool_request = {
        "name": "update_task",
        "parameters": params
    }
    result = await handle_tool_request(tool_request)
    return result


async def run_agent_with_mcp_tools(user_id: str, conversation_id: str, messages: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Run the AI agent with MCP tools to process user messages
    """
    # Get model and API key from environment
    model = os.getenv("LLM_MODEL", "grok-beta")
    api_key = os.getenv("GROK_API_KEY") or os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROK_API_KEY or GROQ_API_KEY not found in environment variables")

    # Create the agent with MCP tools
    agent = Agent(
        name="TodoAssistant",
        instructions="""
        You are a helpful AI assistant that helps users manage their tasks.
        You can add, list, complete, delete, and update tasks.
        Always be polite and confirm actions with users.
        When a user asks to add a task, use the add_task function.
        When a user asks to see tasks, use the list_tasks function.
        When a user asks to complete a task, use the complete_task function.
        When a user asks to delete a task, use the delete_task function.
        When a user asks to update a task, use the update_task function.
        Always provide clear, friendly responses.
        """,
        model=LitellmModel(model=model, api_key=api_key),
        tools=[add_task, list_tasks, complete_task, delete_task, update_task],
    )

    # Prepare the conversation for the agent
    # Take the last few messages to keep context manageable
    recent_messages = messages[-5:]  # Keep last 5 messages for context

    # Run the agent with the user's message
    result = await Runner.run(
        agent,
        "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent_messages])
    )

    # Format the response
    response_content = result.final_output or "I'm sorry, I couldn't process your request."

    # Extract tool calls if any
    tool_calls = []
    if hasattr(result, 'tool_calls') and result.tool_calls:
        for tool_call in result.tool_calls:
            tool_calls.append({
                "name": tool_call.name,
                "arguments": tool_call.arguments
            })

    return {
        "response": response_content,
        "tool_calls": tool_calls,
        "conversation_id": conversation_id
    }


# For testing purposes
if __name__ == "__main__":
    async def test_agent():
        # Test the agent with a sample message
        test_messages = [
            {"role": "user", "content": "Add a task to buy groceries"},
        ]

        try:
            result = await run_agent_with_mcp_tools(
                user_id="test_user_123",
                conversation_id="test_conv_456",
                messages=test_messages
            )
            print("Agent response:", result)
        except Exception as e:
            print(f"Error running agent: {e}")

    # Uncomment to run test
    # asyncio.run(test_agent())