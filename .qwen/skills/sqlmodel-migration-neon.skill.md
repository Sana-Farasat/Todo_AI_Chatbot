Skill: SQLModel migrations with Alembic for Neon Postgres

Commands:
cd backend
alembic init migrations
alembic revision --autogenerate -m "add tasks table"
alembic upgrade head

In env.py:
target_metadata = SQLModel.metadata
Include models.py

Neon specific:
- Use connection string with ?sslmode=require
- Pool size = 5-10 for serverless