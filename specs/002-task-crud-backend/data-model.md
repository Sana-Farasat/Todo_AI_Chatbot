# Data Model: Task CRUD Backend API

## Overview
This document defines the data model for the secure Task CRUD API, including entity definitions, relationships, and validation rules.

## Task Entity

### Properties
- **id**: `int | None` (Primary Key, Auto-generated)
  - Unique identifier for each task
  - Auto-incremented by the database
- **user_id**: `str` (Foreign Key referencing users.id)
  - Links the task to the user who owns it
  - Required for user isolation and authorization
- **title**: `str` (Max length: 200)
  - The title of the task
  - Required field
- **description**: `str | None`
  - Optional detailed description of the task
- **completed**: `bool` (Default: False)
  - Indicates whether the task is completed
  - Used for filtering and status tracking
- **created_at**: `datetime`
  - Timestamp when the task was created
  - Auto-populated using datetime.utcnow
- **updated_at**: `datetime`
  - Timestamp when the task was last updated
  - Auto-populated using datetime.utcnow with onupdate trigger

### SQLModel Definition
```python
from sqlmodel import SQLModel, Field
from datetime import datetime

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id")  # Better Auth users table
    title: str = Field(max_length=200)
    description: str | None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
```

### Indexes
- Composite index on (user_id, completed) for efficient filtering of user tasks by completion status

### Validation Rules
1. Title must be between 1 and 200 characters
2. Description, if provided, has no length limit
3. Completed status defaults to False
4. Created and updated timestamps are automatically managed

### State Transitions
- A task can transition from `completed=False` to `completed=True` (marked as done)
- A task can transition from `completed=True` to `completed=False` (marked as incomplete)

## Relationships
- Task belongs to a User (via user_id foreign key)
- Each user can have multiple tasks
- Tasks are isolated by user_id to ensure privacy

## Data Persistence Requirements
- All task data must be persisted reliably in Neon Postgres
- Creation and update timestamps must be recorded for audit purposes
- Data integrity must be maintained through foreign key constraints