"""
Fix database schema - Recreate tables with correct auto-increment
"""
import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from models import Task, Conversation, Message

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

# Handle SSL mode
if "?sslmode=" in DATABASE_URL or "?ssl=" in DATABASE_URL:
    base_url, query_string = DATABASE_URL.split("?", 1)
    DATABASE_URL = base_url

async def fix_database():
    """Drop and recreate all tables with correct schema"""
    print("=" * 60)
    print("FIXING DATABASE SCHEMA")
    print("=" * 60)
    
    # Create engine
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,
        future=True,
        connect_args={"ssl": "require"}
    )
    
    async with engine.begin() as conn:
        print("\n1. Dropping existing tables...")
        # Drop all tables
        await conn.run_sync(SQLModel.metadata.drop_all)
        print("   [OK] Tables dropped")
        
        print("\n2. Creating tables with correct schema...")
        # Create all tables
        await conn.run_sync(SQLModel.metadata.create_all)
        print("   [OK] Tables created")
    
    print("\n" + "=" * 60)
    print("DATABASE SCHEMA FIXED")
    print("=" * 60)
    print("\nTables created:")
    print("- tasks")
    print("- conversations")
    print("- messages")
    print("\nYou can now run the CRUD tests again.")


if __name__ == "__main__":
    asyncio.run(fix_database())
