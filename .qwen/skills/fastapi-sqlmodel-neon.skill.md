Skill: FastAPI + SQLModel + Neon Serverless Postgres (Phase 2)

Database URL: os.getenv("DATABASE_URL")  # postgresql://...
Use SQLModel with async engine (asyncpg)

Models:
class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id")  # Better Auth users table
    title: str = Field(max_length=200)
    description: str | None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

Index on (user_id, completed)

Session: Depends(get_db) → async session
All queries MUST filter by user_id from JWT