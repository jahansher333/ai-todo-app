import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel
from sqlalchemy import text

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Database URL: {DATABASE_URL}")

try:
    # Create database engine
    engine = create_engine(DATABASE_URL, echo=True)

    # Drop existing tables if they exist (be careful!)
    from sqlalchemy import inspect
    inspector = inspect(engine)

    # Get all table names
    table_names = inspector.get_table_names()
    print(f"Existing tables: {table_names}")

    # Drop all tables (this is a destructive operation, but necessary for schema reset)
    with engine.connect() as connection:
        # Disable foreign key checks temporarily
        trans = connection.begin()

        # Drop tables in reverse order to respect foreign key constraints
        for table_name in reversed(table_names):
            print(f"Dropping table: {table_name}")
            # Use CASCADE to handle dependencies
            connection.execute(text(f'DROP TABLE IF EXISTS "{table_name}" CASCADE'))

        trans.commit()

    print("All tables dropped. Now recreating with correct schema...")

    # Create tables with correct schema
    from src.models import SQLModel
    SQLModel.metadata.create_all(engine)
    print("Tables recreated with correct schema!")

    # Verify the schema
    with engine.connect() as connection:
        # Check columns in the user table
        result = connection.execute(text("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'user'
            ORDER BY ordinal_position
        """))

        print("Columns in 'user' table after recreation:")
        for row in result:
            print(f"  {row[0]}: {row[1]}")

        # Check columns in the task table
        result = connection.execute(text("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'task'
            ORDER BY ordinal_position
        """))

        print("\nColumns in 'task' table after recreation:")
        for row in result:
            print(f"  {row[0]}: {row[1]}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()