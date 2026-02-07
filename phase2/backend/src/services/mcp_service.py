"""
MCP Service for handling tool requests
"""
from typing import Dict, Any
from ...mcp_server.main import handle_tool_request
from ...src.middleware.jwt_middleware import encode_token as create_access_token
import uuid


class MCPTaskService:
    """
    Service to handle MCP tool requests for task management
    """

    def __init__(self):
        self.service_name = "MCPTaskService"

    async def execute_task_tool(self, tool_name: str, params: Dict[str, Any], user_token: str) -> Dict[str, Any]:
        """
        Execute a task management tool via MCP
        """
        # Prepare the tool request
        tool_request = {
            "name": tool_name,
            "parameters": params
        }

        try:
            # Execute the tool via the MCP server
            result = await handle_tool_request(tool_request, user_token)
            return result
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed"
            }

    async def add_task(self, title: str, description: str = None, priority: str = "medium",
                      due_date: str = None, user_token: str = None) -> Dict[str, Any]:
        """
        Add a new task using the MCP tool
        """
        params = {
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date
        }

        return await self.execute_task_tool("add_task", params, user_token)

    async def list_tasks(self, status: str = "all", priority: str = "all",
                        limit: int = 10, search_query: str = None, user_token: str = None) -> Dict[str, Any]:
        """
        List tasks using the MCP tool
        """
        params = {
            "status": status,
            "priority": priority,
            "limit": limit,
            "search_query": search_query
        }

        return await self.execute_task_tool("list_tasks", params, user_token)

    async def complete_task(self, task_id: str, user_token: str = None) -> Dict[str, Any]:
        """
        Complete a task using the MCP tool
        """
        params = {"task_id": task_id}
        return await self.execute_task_tool("complete_task", params, user_token)

    async def delete_task(self, task_id: str, user_token: str = None) -> Dict[str, Any]:
        """
        Delete a task using the MCP tool
        """
        params = {"task_id": task_id}
        return await self.execute_task_tool("delete_task", params, user_token)

    async def update_task(self, task_id: str, title: str = None, description: str = None,
                         priority: str = None, due_date: str = None, status: str = None,
                         user_token: str = None) -> Dict[str, Any]:
        """
        Update a task using the MCP tool
        """
        params = {
            "task_id": task_id,
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "status": status
        }

        # Remove None values from params
        params = {k: v for k, v in params.items() if v is not None}

        return await self.execute_task_tool("update_task", params, user_token)


# Global MCP service instance
mcp_service_instance = None


def get_mcp_service() -> MCPTaskService:
    """
    Get or create the MCP service instance
    """
    global mcp_service_instance

    if mcp_service_instance is None:
        mcp_service_instance = MCPTaskService()

    return mcp_service_instance