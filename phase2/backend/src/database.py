from sqlmodel import SQLModel, create_engine
import os

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")

# Create database engine
# For PostgreSQL, we need to handle the SSL requirements
connect_args = {}

if DATABASE_URL.startswith("postgresql"):
    # For PostgreSQL connections, especially with Neon, we may need specific SSL settings
    connect_args = {"sslmode": "require"}
else:
    # For SQLite, use different settings
    connect_args = {
        "check_same_thread": False  # Allow multi-threading for SQLite
    }

engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)


# Create database and tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)