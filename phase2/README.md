# Phase II: Todo Full-Stack Web Application – Jira-like Todo App

Welcome to Phase II of the Todo application! This phase introduces a full-stack web application with a Jira-like interface, featuring Kanban boards, authentication, and persistent storage.

## Features

- **User Authentication**: Secure login/signup with JWT tokens
- **Task Management**: Create, read, update, and delete tasks
- **Jira-like Interface**: Kanban board with drag-and-drop functionality
- **Task Properties**: Priority levels, tags, due dates, recurring tasks
- **Advanced Filtering**: Search, filter by status/priority/date, sort by various criteria
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: SQLModel with PostgreSQL (Neon)
- **Authentication**: JWT middleware
- **Dependencies**: See `backend/requirements.txt`

### Frontend
- **Framework**: Next.js 16+ with App Router
- **Styling**: Tailwind CSS
- **State Management**: React hooks
- **UI Components**: Custom-built with Tailwind
- **Dependencies**: See `frontend/package.json`

## Setup Instructions

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL (or Neon account)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd phase2/backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the environment file and update the values:
   ```bash
   cp ../.env.example .env
   # Edit .env with your database URL and secret
   ```

5. Run the backend server:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd phase2/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Copy the environment file:
   ```bash
   cp .env.example .env.local
   # Ensure NEXT_PUBLIC_API_BASE_URL points to your backend
   ```

4. Run the frontend development server:
   ```bash
   npm run dev
   ```

## API Endpoints

The backend provides the following REST API endpoints:

- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task for a user
- `PUT /api/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Update task completion status

All endpoints require a valid JWT token in the Authorization header.

## Environment Variables

Both backend and frontend require the following environment variables:

- `DATABASE_URL` - Connection string for PostgreSQL database
- `BETTER_AUTH_SECRET` - Secret key for JWT token signing
- `NEXT_PUBLIC_API_BASE_URL` - Base URL for the backend API

## Project Structure

```
phase2/
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── models/          # SQLModel definitions
│   │   ├── services/        # Business logic
│   │   ├── api/            # API routes
│   │   └── middleware/     # Authentication middleware
│   └── requirements.txt
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/            # App Router pages
│   │   ├── components/     # Reusable UI components
│   │   ├── lib/           # Utilities and API clients
│   │   └── types/         # TypeScript type definitions
│   ├── public/            # Static assets
│   └── package.json
├── .env.example           # Example environment variables
└── README.md              # This file
```

## Running the Application

1. Start the backend server (port 8000)
2. Start the frontend server (port 3000)
3. Visit `http://localhost:3000` in your browser
4. Register a new account or log in to start using the application

## Security Features

- JWT-based authentication with token verification
- User isolation - users can only access their own tasks
- Proper error handling and validation
- Input sanitization and validation

## Troubleshooting

- If you encounter database connection issues, verify your `DATABASE_URL` in the environment variables
- For authentication problems, ensure the `BETTER_AUTH_SECRET` is the same in both backend and frontend
- If API calls fail, check that the `NEXT_PUBLIC_API_BASE_URL` is correctly set in the frontend