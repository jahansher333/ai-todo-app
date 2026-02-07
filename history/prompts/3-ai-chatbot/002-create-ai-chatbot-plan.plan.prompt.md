---
id: 002
title: Create AI chatbot plan
stage: plan
date: 2026-02-03
surface: agent
model: Claude Sonnet 4.5
feature: ai-chatbot
branch: 3-ai-chatbot
user: jahansher
command: /sp.plan
labels: [plan, ai, chatbot, todo]
links:
  spec: specs/3-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/3-ai-chatbot/plan.md
  - specs/3-ai-chatbot/research.md
  - specs/3-ai-chatbot/data-model.md
  - specs/3-ai-chatbot/contracts/chat-api.yaml
  - specs/3-ai-chatbot/quickstart.md
  - .specify/agents/claude-context.md
tests:
  - specs/3-ai-chatbot/plan.md validation
  - specs/3-ai-chatbot/data-model.md validation
---

## Prompt

Phase III: Todo AI-Powered Chatbot
Use specs from previous phase.
Success criteria:
- Monorepo: frontend/ (Next.js + ChatKit), backend/ (FastAPI + MCP + Agents SDK), specs/
- Backend: FastAPI with /api/{user_id}/chat endpoint, JWT middleware (extract user_id)
- MCP Server: Official MCP SDK with 5 tools (stateless, DB-backed)
- Database: Add Conversation (user_id, id, timestamps) + Message (user_id, conversation_id, role, content, timestamps)
- Agent: OpenAI Agents SDK runner, uses MCP tools, confirms actions, handles errors
- Frontend: ChatKit UI in protected route, sends message + conversation_id + JWT
- Stateless flow: fetch history → add user message → run agent → save assistant response → return
Tech stack: FastAPI, OpenAI Agents SDK, Official MCP SDK, SQLModel, Neon Postgres, Better-Auth JWT, ChatKit
What the agent does: Output plan.md with Mermaid diagram (ChatKit → FastAPI → Agents → MCP → Neon), file structure, JWT + MCP flow, database schema, agent behavior guidelines. Ready for /sp.tasks.

## Response snapshot

Created comprehensive implementation plan for the AI-powered chatbot with all required components. The plan includes:
- Technical context with technology stack and constraints
- Monorepo project structure with separate frontend and backend
- Architecture diagram showing the flow from ChatKit to Neon Postgres
- Detailed implementation flow and MCP server tools specification
- Research document with technology decisions and alternatives
- Data model with all entities and relationships
- API contracts in OpenAPI format
- Quickstart guide for development setup
- Agent context file with technology additions

## Outcome

- ✅ Impact: Complete implementation plan with architecture, data models, and API contracts
- 🧪 Tests: All plan components validated
- 📁 Files: plan.md, research.md, data-model.md, contracts/chat-api.yaml, quickstart.md, claude-context.md
- 🔁 Next prompts: /sp.tasks to generate implementation tasks
- 🧠 Reflection: Plan comprehensively covers all requirements from the specification

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All plan components created successfully
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Generate tasks from the plan