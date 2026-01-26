# Todo Full-Stack Web Application

Multi-user todo application with authentication, built as part of Phase II.

## Project Structure

```
todo/
├── backend/           # FastAPI backend
│   ├── src/
│   │   ├── models/    # SQLModel database models
│   │   ├── schemas/   # Pydantic request/response schemas
│   │   ├── routers/   # API route handlers
│   │   ├── middleware/# JWT authentication middleware
│   │   ├── services/  # Business logic layer
│   │   ├── config.py  # Configuration management
│   │   ├── db.py      # Database connection
│   │   └── main.py    # FastAPI app entry point
│   ├── tests/         # Backend tests
│   └── requirements.txt
│
├── frontend/          # Next.js 16+ frontend
│   ├── src/
│   │   ├── app/       # App Router pages
│   │   ├── components/# React components
│   │   ├── lib/       # Utilities
│   │   ├── types/     # TypeScript types
│   │   └── hooks/     # Custom React hooks
│   └── package.json
│
├── specs/             # Feature specifications
└── phase-i/           # Phase I CLI application
```

## Tech Stack

**Backend**:
- FastAPI - API framework
- SQLModel - ORM + validation
- Neon Postgres - Serverless database
- python-jose - JWT tokens
- bcrypt - Password hashing
- Alembic - Database migrations

**Frontend**:
- Next.js 16+ App Router - React framework
- Better-Auth - Authentication
- Tailwind CSS - Styling
- date-fns - Date formatting

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
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

4. Create `.env` file (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```

5. Update `.env` with your values:
   - `DATABASE_URL`: Get from Neon.tech
   - `BETTER_AUTH_SECRET`: Generate with `openssl rand -hex 32`

6. Initialize database (after Phase 3 when models are created):
   ```bash
   alembic upgrade head
   ```

7. Start backend server:
   ```bash
   uvicorn src.main:app --reload
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
   - `BETTER_AUTH_SECRET`: Same value as backend

5. Start frontend server:
   ```bash
   npm run dev
   ```
   Frontend will run on http://localhost:3000

## Development Status

### Phase II: Full-Stack Web Application - ✅ COMPLETE

All features implemented and ready for use:

- ✅ **User Authentication**: Signup, signin, JWT tokens, session management
- ✅ **Basic Task Management**: Create, read, update, delete, mark complete
- ✅ **Task Prioritization**: High/medium/low with color-coded badges
- ✅ **Tags & Categories**: Multiple tags per task, filterable
- ✅ **Search & Filter**: Keyword search, status/priority/tag filters
- ✅ **Task Sorting**: Sort by date, priority, title, due date
- ✅ **Due Dates**: Date/time picker with overdue warnings
- ✅ **Reminders & Warnings**: Visual indicators for overdue and due-soon tasks
- ✅ **Recurring Tasks**: Daily/weekly auto-generation on completion
- ✅ **User Isolation**: Complete data privacy between users
- ✅ **Responsive Design**: Mobile and desktop optimized

**Total**: All 9 user stories (US1-US9) implemented with full feature set

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Backend tests:
```bash
cd backend
pytest
```

Frontend tests (when implemented):
```bash
cd frontend
npm run test
```

## Contributing

Follow the task breakdown in `specs/001-todo-web-fullstack/tasks.md` for implementation.

## License

MIT
