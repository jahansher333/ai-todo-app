# Quickstart Guide: Phase II - Todo Full-Stack Web Application

## Prerequisites

- Node.js 18+ installed
- Python 3.11+ installed
- pip package manager
- Git
- Access to Neon PostgreSQL database

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Backend Setup

#### Navigate to Backend Directory
```bash
cd backend
```

#### Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Environment Configuration
Create `.env` file in the backend directory:
```env
DATABASE_URL="postgresql://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
SECRET_KEY="your-secret-key-here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Run Database Migrations
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

#### Start Backend Server
```bash
uvicorn src.main:app --reload --port 8000
```

### 3. Frontend Setup

#### Navigate to Frontend Directory
```bash
cd frontend  # From project root
```

#### Install Dependencies
```bash
npm install
```

#### Environment Configuration
Create `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-nextauth-secret
```

#### Start Frontend Development Server
```bash
npm run dev
```

## Running the Application

1. Start the backend server (port 8000)
2. Start the frontend server (port 3000)
3. Access the application at http://localhost:3000

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token
- `POST /auth/logout` - Logout user

### Tasks (require authentication)
- `GET /api/{user_id}/tasks` - Get all user tasks
- `POST /api/{user_id}/tasks` - Create a new task
- `PUT /api/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Mark task as complete

## Development Commands

### Backend
```bash
# Run tests
pytest

# Format code
black src/

# Check types
mypy src/
```

### Frontend
```bash
# Run tests
npm test

# Format code
npm run format

# Lint code
npm run lint
```

## Deployment

### Backend (to production)
```bash
# Build for production
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start production server
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend (to production)
```bash
# Build for production
npm run build

# Start production server
npm start
```