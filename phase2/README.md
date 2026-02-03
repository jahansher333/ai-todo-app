# Todo AI-Powered Chatbot

AI-powered chatbot interface for managing todos through natural language using MCP (Model Context Protocol) server architecture.

## Features

- **Natural Language Interface**: Interact with your todo list using everyday language
- **AI-Powered**: Uses OpenAI Agents SDK with MCP tools for intelligent task management
- **Secure Authentication**: JWT-based authentication with user isolation
- **Persistent Conversations**: Conversation history stored in database
- **Stateless Architecture**: Scalable server design with all state stored in database

## Architecture

```
┌─────────────────┐     ┌──────────────────────────────────────────────┐     ┌─────────────────┐
│                 │     │              FastAPI Server                   │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │     │    Neon DB      │
│  ChatKit UI     │────▶│  │         Chat Endpoint                  │  │     │  (PostgreSQL)   │
│  (Frontend)     │     │  │  POST /api/chat                        │  │     │                 │
│                 │     │  └───────────────┬────────────────────────┘  │     │  - tasks        │
│                 │     │                  │                           │     │  - conversations│
│                 │     │                  ▼                           │     │  - messages     │
│                 │     │  ┌────────────────────────────────────────┐  │     │                 │
│                 │◀────│  │      OpenAI Agents SDK                 │  │     │                 │
│                 │     │  │      (Agent + Runner)                  │  │     │                 │
│                 │     │  └───────────────┬────────────────────────┘  │     │                 │
│                 │     │                  │                           │     │                 │
│                 │     │                  ▼                           │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │────▶│                 │
│                 │     │  │         MCP Server                     │  │     │                 │
│                 │     │  │  (MCP Tools for Task Operations)       │  │◀────│                 │
│                 │     │  └────────────────────────────────────────┘  │     │                 │
└─────────────────┘     └──────────────────────────────────────────────┘     └─────────────────┘
```

## Technology Stack

- **Frontend**: OpenAI ChatKit
- **Backend**: Python FastAPI
- **AI Framework**: OpenAI Agents SDK with LiteLLM
- **MCP Server**: Official MCP SDK
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth

## Database Models

### Task
- user_id, id, title, description, completed, created_at, updated_at

### Conversation
- user_id, id, created_at, updated_at

### Message
- user_id, id, conversation_id, role (user/assistant), content, created_at

## API Endpoints

### POST `/api/{user_id}/chat`
Send message & get AI response

**Request:**
```json
{
  "message": "string",
  "conversation_id": "string (optional)"
}
```

**Response:**
```json
{
  "conversation_id": "string",
  "response": "string",
  "tool_calls": "array"
}
```

## MCP Tools

The MCP server exposes the following tools for the AI agent:

### add_task
- Purpose: Create a new task
- Parameters: user_id (required), title (required), description (optional)
- Returns: task_id, status, title

### list_tasks
- Purpose: Retrieve tasks from the list
- Parameters: user_id (required), status (optional: "all", "pending", "completed")
- Returns: Array of task objects

### complete_task
- Purpose: Mark a task as complete
- Parameters: user_id (required), task_id (required)
- Returns: task_id, status, title

### delete_task
- Purpose: Remove a task from the list
- Parameters: user_id (required), task_id (required)
- Returns: task_id, status, title

### update_task
- Purpose: Modify task title or description
- Parameters: user_id (required), task_id (required), title (optional), description (optional)
- Returns: task_id, status, title

## Natural Language Commands

The chatbot understands and responds to:

| User Says | Agent Should |
|-----------|--------------|
| "Add a task to buy groceries" | Call add_task with title "Buy groceries" |
| "Show me all my tasks" | Call list_tasks with status "all" |
| "What's pending?" | Call list_tasks with status "pending" |
| "Mark task 3 as complete" | Call complete_task with task_id 3 |
| "Delete the meeting task" | Call list_tasks first, then delete_task |
| "Change task 1 to 'Call mom tonight'" | Call update_task with new title |
| "I need to remember to pay bills" | Call add_task with title "Pay bills" |
| "What have I completed?" | Call list_tasks with status "completed" |

## Setup Instructions

### Prerequisites

- Node.js 18+
- Python 3.11+
- UV package manager
- Neon account (free tier at https://neon.tech)

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```

5. Update `.env` with your values:
   - `DATABASE_URL`: Get from Neon.tech
   - `BETTER_AUTH_SECRET`: Generate with `openssl rand -hex 32`
   - `GROK_API_KEY`: Your Grok API key
   - `LLM_MODEL`: The model to use (default: grok-beta)

6. Start backend server:
   ```bash
   uvicorn main:app --reload
   ```
   Backend will run on http://localhost:8000

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create `.env.local` file (copy from `.env.local.example`):
   ```bash
   cp .env.local.example .env.local
   ```

4. Update `.env.local`:
   - `NEXT_PUBLIC_API_URL`: http://localhost:8000
   - `NEXT_PUBLIC_OPENAI_DOMAIN_KEY`: Your OpenAI domain key
   - `BETTER_AUTH_SECRET`: Same value as backend

5. Start frontend server:
   ```bash
   npm run dev
   ```
   Frontend will run on http://localhost:3000

## Conversation Flow (Stateless Request Cycle)

1. Receive user message
2. Fetch conversation history from database
3. Build message array for agent (history + new message)
4. Store user message in database
5. Run agent with MCP tools
6. Agent invokes appropriate MCP tool(s)
7. Store assistant response in database
8. Return response to client
9. Server holds NO state (ready for next request)

## Key Architecture Benefits

| Aspect | Benefit |
|--------|---------|
| MCP Tools | Standardized interface for AI to interact with your app |
| Single Endpoint | Simpler API — AI handles routing to tools |
| Stateless Server | Scalable, resilient, horizontally scalable |
| Tool Composition | Agent can chain multiple tools in one turn |

## Key Stateless Architecture Benefits

- **Scalability**: Any server instance can handle any request
- **Resilience**: Server restarts don't lose conversation state
- **Horizontal scaling**: Load balancer can route to any backend
- **Testability**: Each request is independent and reproducible

## Development Status

### Phase III: Todo AI-Powered Chatbot - ✅ COMPLETE

All features implemented and ready for use:

- ✅ **Natural Language Processing**: AI understands and processes natural language commands
- ✅ **MCP Integration**: Official MCP SDK with 5 tools for task management
- ✅ **Stateless Architecture**: All state persisted in Neon database
- ✅ **JWT Authentication**: Secure user isolation with token validation
- ✅ **Chat Interface**: OpenAI ChatKit integration in protected route
- ✅ **Agent Behavior**: Proper confirmation and error handling
- ✅ **Conversation Persistence**: Full conversation history maintained
- ✅ **API Integration**: Complete backend API with proper middleware
- ✅ **Frontend Integration**: Full chat interface with JWT token handling

**Total**: All 5 basic features (add, list, update, delete, complete) working via natural language

## Testing

Try these commands in the chat interface:
- "Add a task to buy groceries"
- "Show me all my tasks"
- "Mark task 3 as complete"
- "Delete the meeting task"
- "Change task 1 to 'Call mom tonight'"