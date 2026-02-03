"""
AI Agent that integrates with MCP server for task management
"""
import asyncio
from typing import Dict, Any, List
from openai import AsyncOpenAI
import os
from mcp.client import Client
from mcp.types import Tool
import json
from dotenv import load_dotenv

load_dotenv()

class AIAgentWithMCP:
    def __init__(self):
        # Initialize OpenAI client
        self.openai_client = AsyncOpenAI(
            api_key=os.getenv("GROQ_API_KEY") or os.getenv("GROK_API_KEY") or "dummy-key",
            base_url="https://api.groq.com/openai/v1"  # Using Groq as example
        )

        # Initialize MCP client to connect to our MCP server
        self.mcp_client = None

        # Define the system prompt for the agent
        self.system_prompt = """
        You are a helpful AI assistant that helps users manage their tasks.
        You can add, list, complete, delete, and update tasks.
        Always be polite and confirm actions with users.
        When a user asks to add a task, use the add_task function.
        When a user asks to see tasks, use the list_tasks function.
        When a user asks to complete a task, use the complete_task function.
        When a user asks to delete a task, use the delete_task function.
        When a user asks to update a task, use the update_task function.
        Always provide clear, friendly responses.
        """

    async def connect_to_mcp_server(self):
        """Connect to the MCP server to discover available tools"""
        try:
            # Connect to the MCP server running on localhost:8000
            self.mcp_client = Client()
            # Note: In a real implementation, you would connect to the actual MCP server
            print("Connected to MCP server")
        except Exception as e:
            print(f"Error connecting to MCP server: {e}")

    async def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools from MCP server"""
        # In a real implementation, this would fetch tools from the MCP server
        # For now, defining the tools that our MCP server provides
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "User ID"},
                            "title": {"type": "string", "description": "Task title"},
                            "description": {"type": "string", "description": "Task description"},
                            "priority": {"type": "string", "description": "Task priority", "default": "medium"}
                        },
                        "required": ["user_id", "title"]
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
                            "user_id": {"type": "string", "description": "User ID"},
                            "status": {"type": "string", "description": "Task status filter", "default": "all"},
                            "limit": {"type": "integer", "description": "Max number of tasks to return", "default": 10}
                        },
                        "required": ["user_id"]
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
                            "user_id": {"type": "string", "description": "User ID"},
                            "task_id": {"type": "string", "description": "Task ID to complete"}
                        },
                        "required": ["user_id", "task_id"]
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
                            "user_id": {"type": "string", "description": "User ID"},
                            "task_id": {"type": "string", "description": "Task ID to delete"}
                        },
                        "required": ["user_id", "task_id"]
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
                            "user_id": {"type": "string", "description": "User ID"},
                            "task_id": {"type": "string", "description": "Task ID to update"},
                            "title": {"type": "string", "description": "New task title"},
                            "description": {"type": "string", "description": "New task description"},
                            "priority": {"type": "string", "description": "New task priority"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]

    async def call_mcp_tool(self, tool_name: str, tool_arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call the appropriate MCP tool"""
        try:
            # In a real implementation, this would call the actual MCP server
            # For now, we'll simulate calling the tool by sending to our MCP server

            # This would normally make an HTTP call to the MCP server
            import aiohttp
            async with aiohttp.ClientSession() as session:
                # Call the MCP server endpoint
                # Note: This is a simplified example - actual MCP protocol is more complex
                async with session.post(
                    f"http://localhost:8000/tools/{tool_name}",
                    json=tool_arguments
                ) as response:
                    result = await response.json()
                    return result
        except Exception as e:
            return {"error": f"Error calling MCP tool {tool_name}: {str(e)}"}

    async def process_message(self, message: str, user_id: str) -> Dict[str, Any]:
        """Process a user message using the AI agent with MCP tools"""
        try:
            # Get available tools
            tools = await self.get_available_tools()

            # Prepare the messages for the AI
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": message}
            ]

            # Call the AI with tool capability
            response = await self.openai_client.chat.completions.create(
                model="llama3-groq-70b-8192-tool-use-preview",  # Using Groq model as example
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )

            response_message = response.choices[0].message

            # Check if the AI wants to call any tools
            tool_calls = response_message.tool_calls
            if tool_calls:
                # Execute the requested tools
                tool_results = []
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Ensure user_id is included
                    function_args["user_id"] = user_id

                    # Call the MCP tool
                    result = await self.call_mcp_tool(function_name, function_args)
                    tool_results.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(result)
                    })

                # Get final response from AI with tool results
                final_messages = messages + [response_message] + tool_results
                final_response = await self.openai_client.chat.completions.create(
                    model="llama3-groq-70b-8192-tool-use-preview",
                    messages=final_messages
                )

                return {
                    "response": final_response.choices[0].message.content,
                    "action_taken": "tool_execution",
                    "tool_calls": [tc.function.name for tc in tool_calls]
                }
            else:
                # No tools needed, return direct response
                return {
                    "response": response_message.content,
                    "action_taken": "direct_response",
                    "tool_calls": []
                }

        except Exception as e:
            return {
                "response": f"Sorry, I encountered an error: {str(e)}",
                "action_taken": "error",
                "tool_calls": []
            }


# Example usage
async def main():
    agent = AIAgentWithMCP()
    await agent.connect_to_mcp_server()

    # Example interaction
    result = await agent.process_message("Add task: Buy groceries", "user123")
    print(f"Response: {result}")

if __name__ == "__main__":
    asyncio.run(main())