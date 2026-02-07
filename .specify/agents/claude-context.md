# Agent Context: Todo AI-Powered Chatbot

## Technologies Added

- FastAPI: Modern Python web framework for backend API
- OpenAI Agents SDK: Framework for creating AI agents with tool usage
- MCP SDK: Model Context Protocol for standardized tool integration
- SQLModel: SQL database modeling with Pydantic compatibility
- Neon Postgres: Serverless PostgreSQL database
- Better-Auth: JWT-based authentication solution
- ChatKit: Pre-built chat UI components
- Next.js: React-based web framework for frontend

## Architecture Patterns

- Stateless server design with all data persisted in database
- JWT-based user authentication and isolation
- Conversation and message persistence for context continuity
- MCP tools for standardized AI tool integration
- Monorepo structure with separate frontend and backend

## Key Components

- Chat endpoint: /api/{user_id}/chat for processing user messages
- MCP tools: 5 standardized tools for todo operations
- Data models: Conversation, Message, and Task with user relationships
- Authentication: JWT middleware for user identification
- Agent service: OpenAI agent with MCP tool integration