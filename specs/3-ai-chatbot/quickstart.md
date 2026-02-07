# Quickstart Guide: Todo AI-Powered Chatbot

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL-compatible database (Neon recommended)
- OpenAI API key
- MCP server setup

## Environment Setup

1. Clone the repository:
```bash
git clone <repo-url>
cd <repo-name>
```

2. Set up backend environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up frontend environment:
```bash
cd ../frontend
npm install
```

4. Configure environment variables:
```bash
# backend/.env
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://user:password@localhost/dbname
NEON_DATABASE_URL=your_neon_database_url
JWT_SECRET=your_jwt_secret
MCP_SERVER_URL=http://localhost:8000
```

```bash
# frontend/.env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_JWT_SECRET=your_jwt_secret
```

## Database Setup

1. Run database migrations:
```bash
cd backend
python -m src.models  # or however you handle migrations
```

2. Initialize the database with required tables:
- conversations
- messages
- tasks
- users

## Running the Application

### Backend
```bash
cd backend
python main.py
```

The backend will start on `http://localhost:8000`

### MCP Server
```bash
cd backend
python -m src.services.mcp_server
```

The MCP server will start on `http://localhost:8001`

### Frontend
```bash
cd frontend
npm run dev
```

The frontend will start on `http://localhost:3000`

## API Endpoints

- `POST /api/{user_id}/chat` - Process chat messages
- `GET /api/conversations` - Get user's conversations
- `GET /api/conversations/{conversation_id}/messages` - Get messages from conversation

## Testing

Backend tests:
```bash
cd backend
pytest
```

Frontend tests:
```bash
cd frontend
npm test
```

## Building for Production

Backend:
```bash
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Frontend:
```bash
cd frontend
npm run build
```

## Troubleshooting

1. If you encounter database connection errors, verify your DATABASE_URL is correct
2. If JWT authentication fails, check that the secret matches between frontend and backend
3. If MCP tools aren't working, ensure the MCP server is running and accessible
4. For OpenAI API errors, verify your API key is valid and has sufficient quota