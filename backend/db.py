import os
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlmodel import SQLModel

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

# Remove query parameters that asyncpg doesn't understand
# Neon DB URL format: postgresql://user:pass@host/dbname?sslmode=require
# asyncpg expects: postgresql+asyncpg://user:pass@host/dbname with ssl in connect_args

# Convert to asyncpg format
# if not DATABASE_URL.startswith("postgresql+asyncpg://"):
#     DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

DATABASE_URL.startswith("postgresql+asyncpg://")
    
# Handle SSL mode for providers like Neon
if "?sslmode=" in DATABASE_URL or "?ssl=" in DATABASE_URL:
    base_url, query_string = DATABASE_URL.split("?", 1)
    DATABASE_URL = base_url

# Async engine banate hain – SQLAlchemy se
engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
    connect_args={"ssl": "require"}  # Enable SSL for Neon/production DBs
)

# Async session generator (FastAPI Depends ke liye)
async def get_session():
    async with AsyncSession(engine) as session:
        yield session


# Optional: Startup event pe tables create karne ke liye (testing ke liye)
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)