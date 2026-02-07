from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.chat import include_router
from src.routes.auth import router as auth_router
from src.routes.tasks import router as tasks_router
from src.database import create_db_and_tables
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    create_db_and_tables()
    yield

app = FastAPI(
    title="Todo AI-Powered Chatbot API",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, tags=["auth"])  # Auth routes like /auth/register, /auth/login
app.include_router(tasks_router, prefix="/api/{user_id}", tags=["tasks"])  # Task routes
include_router(app)  # Chat routes


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)