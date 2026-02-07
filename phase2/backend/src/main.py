from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from datetime import datetime, timedelta
from typing import Optional
import jwt
from jwt import PyJWTError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from .middleware.jwt_middleware import JWTBearer, decode_token
from .routes.tasks import router as tasks_router
from .routes.auth import router as auth_router
from .database import engine, create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    create_db_and_tables()
    yield

# Initialize FastAPI app
app = FastAPI(
    title="Todo Application API",
    description="API for the Todo Full-Stack Web Application with Jira-like features",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks_router, prefix="/api/{user_id}", tags=["tasks"])
app.include_router(auth_router, tags=["auth"])

# Additional test route to ensure reload
@app.get("/test")
def test_route():
    return {"message": "Test route working"}

@app.get("/")
def read_root():
    return {"message": "Todo Application API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}