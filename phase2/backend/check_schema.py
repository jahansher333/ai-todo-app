import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session, select
from sqlalchemy import text
from src.models import User

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Database URL: {DATABASE_URL}")

try:
    # Create database engine
    engine = create_engine(DATABASE_URL, echo=True)

    # Check if the user table exists and what columns it has
    with engine.connect() as connection:
        # Check columns in the user table
        result = connection.execute(text("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'user'
            ORDER BY ordinal_position
        """))

        print("Columns in 'user' table:")
        for row in result:
            print(f"  {row[0]}: {row[1]}")

    print("\nAttempting to create tables...")
    # Create tables (this will try to sync the schema)
    SQLModel.metadata.create_all(engine)
    print("Tables creation attempted!")

    # Try to connect with a session
    with Session(engine) as session:
        print("Session created successfully!")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()