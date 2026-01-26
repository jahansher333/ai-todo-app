# Todo Full-Stack Web Application Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-01-21

## Active Technologies

- Next.js 16+ (App Router)
- FastAPI (Python 3.11+)
- SQLModel (ORM)
- Neon Postgres (Database)
- Better-Auth (Authentication)
- Tailwind CSS (Styling)
- TypeScript/JavaScript (Frontend)
- Python (Backend)
- JWT (Authentication tokens)

## Project Structure

```text
hackathon-todo/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   ├── public/
│   ├── styles/
│   ├── package.json
│   └── next.config.js
├── backend/
│   ├── src/
│   │   ├── models/
│   │   ├── services/
│   │   ├── api/
│   │   └── middleware/
│   ├── requirements.txt
│   └── main.py
├── specs/
├── .specify/
└── README.md
```

## Commands

### Frontend
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production build
- `npm run lint` - Run linter

### Backend
- `uvicorn src.main:app --reload --port 8000` - Start development server
- `pytest` - Run tests
- `mypy src/` - Run type checks

### Database
- `alembic upgrade head` - Apply migrations
- `alembic revision --autogenerate -m "message"` - Create migration

## Code Style

### Frontend (JavaScript/TypeScript)
- Use functional components with hooks
- Follow React best practices
- Use TypeScript for type safety
- Use Tailwind CSS utility classes

### Backend (Python)
- Follow PEP 8 style guidelines
- Use type hints for all functions
- Use Pydantic models for data validation
- Use async/await for asynchronous operations

## Recent Changes

- 1-todo-fullstack-jira: Full-stack Todo app with Jira-like Kanban interface
- Implementation of JWT-based authentication with user isolation
- Database schema with tasks linked to users and supporting features like priorities, tags, due dates, and recurring tasks

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->