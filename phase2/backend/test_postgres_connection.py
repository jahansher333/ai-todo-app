import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel
from sqlalchemy.exc import OperationalError
import urllib.parse

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Database URL: {DATABASE_URL}")

if not DATABASE_URL:
    print("Error: DATABASE_URL not found in environment variables")
    exit(1)

try:
    # Create database engine
    engine = create_engine(DATABASE_URL, echo=True)

    # Test the connection
    from sqlalchemy import text
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()"))
        version = result.fetchone()[0]
        print(f"Connected to PostgreSQL version: {version}")

    print("Successfully connected to PostgreSQL database!")

    # Create tables (this will test if we can create the schema)
    from src.models import SQLModel
    SQLModel.metadata.create_all(engine)
    print("Tables created successfully!")

except OperationalError as e:
    print(f"Operational Error connecting to database: {e}")
except Exception as e:
    print(f"Error connecting to database: {e}")