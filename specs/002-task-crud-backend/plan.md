# Implementation Plan: Task CRUD Backend API

**Branch**: `001-task-crud-backend` | **Date**: 2026-02-04 | **Spec**: [specs/001-task-crud-backend/spec.md]
**Input**: Feature specification from `/specs/001-task-crud-backend/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a secure Task CRUD API using FastAPI, SQLModel, and Neon Postgres with Better Auth JWT validation. The API will allow authenticated users to create, read, update, and delete their personal tasks with proper authorization checks to ensure users can only access their own tasks.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, SQLModel, asyncpg, Pydantic v2, PyJWT, Alembic, uvicorn
**Storage**: Neon Serverless Postgres (SQLModel + asyncpg)
**Testing**: pytest
**Target Platform**: Linux server (local development with uvicorn)
**Project Type**: Web application (backend service)
**Performance Goals**: <200ms p95 response time for CRUD operations
**Constraints**: User-isolated tasks, JWT validation on all endpoints, secure auth flow
**Scale/Scope**: Multi-user support with isolated task lists

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Technology stack compliance: Using FastAPI, SQLModel, Neon Postgres as required
- ✅ Security compliance: JWT validation and user isolation enforced
- ✅ Architecture compliance: Following clean architecture with models/routes/db layers
- ✅ Multi-user compliance: Tasks filtered by user_id from JWT token
- ✅ No unauthorized access: All endpoints validate user_id matches JWT.sub

## Project Structure

### Documentation (this feature)

```text
specs/001-task-crud-backend/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── main.py              # FastAPI app entry point
├── models.py            # SQLModel definitions
├── db.py                # Database connection and session
├── middleware/
│   └── jwt.py           # JWT validation middleware
├── routes/
│   └── tasks.py         # Task CRUD endpoints
├── alembic/
│   ├── env.py           # Alembic configuration
│   ├── versions/        # Migration files
│   └── script.py.mako   # Migration template
├── pyproject.toml       # Dependencies and build config
└── .env                 # Environment variables
```

**Structure Decision**: Web application with dedicated backend service following clean architecture patterns with separation of concerns (models, routes, database layer, middleware).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (none)    | (none)     | (none)                              |

## Phase 0: Outline & Research

1. **Research JWT validation in FastAPI** - Understand how to properly validate Better Auth JWTs in middleware
2. **Research SQLModel async patterns** - Ensure proper async database operations
3. **Research Alembic migration best practices** - Proper setup for Neon Postgres
4. **Research Neon Postgres connection pooling** - Optimal settings for serverless

## Phase 1: Design & Contracts

1. **Data Model Design** - Define Task model with proper relationships and constraints
2. **API Contract Design** - Define REST endpoints following Phase 2 conventions
3. **Authentication Flow** - Design JWT validation and user isolation mechanism

## Phase 2: Implementation Plan

### Step 1: Setup Backend Dependencies
- Add FastAPI, SQLModel, asyncpg, pydantic, pyjwt, alembic using UV
- Configure pyproject.toml with all required dependencies
- Set up proper async patterns for database operations

**Qwen Code Sub-Prompt**: "Setup backend dependencies with UV for FastAPI, SQLModel, asyncpg, pydantic, pyjwt, alembic"

### Step 2: Create Models and Database Layer
- Create Task model following SQLModel conventions with user_id foreign key
- Create database connection with async engine for Neon Postgres
- Implement get_db dependency for session management

**Qwen Code Sub-Prompt**: "Create models.py with Task SQLModel and db.py with async engine for Neon Postgres"

### Step 3: Setup Alembic Migrations
- Initialize Alembic in the backend directory
- Configure env.py to use SQLModel metadata
- Create initial migration for Task table
- Test migration with alembic upgrade head

**Qwen Code Sub-Prompt**: "Initialize Alembic migrations for Neon Postgres with SQLModel"

### Step 4: Implement JWT Middleware
- Create middleware/jwt.py with JWT validation logic
- Verify JWT using BETTER_AUTH_SECRET
- Extract user_id from token and validate against URL path
- Attach validated user_id to request.state

**Qwen Code Sub-Prompt**: "Implement JWT validation middleware for Better Auth tokens in FastAPI"

### Step 5: Create Task CRUD Routes
- Create routes/tasks.py with all required endpoints
- Implement GET /api/{user_id}/tasks with filtering options
- Implement POST /api/{user_id}/tasks for creating tasks
- Implement GET /api/{user_id}/tasks/{task_id} for retrieving specific tasks
- Implement PUT /api/{user_id}/tasks/{task_id} for updating tasks
- Implement PATCH /api/{user_id}/tasks/{task_id}/complete for toggling completion
- Implement DELETE /api/{user_id}/tasks/{task_id} for deleting tasks
- Add proper authentication checks on all endpoints

**Qwen Code Sub-Prompt**: "Create FastAPI routes for Task CRUD operations with JWT validation"

### Step 6: Update Main Application
- Update main.py to include task routes
- Add JWT middleware to FastAPI app
- Configure CORS for frontend integration
- Set up proper exception handlers

**Qwen Code Sub-Prompt**: "Update main.py to include task routes and JWT middleware"

### Step 7: Local Testing
- Run uvicorn locally to test API endpoints
- Test all CRUD operations with sample JWT from frontend
- Verify user isolation (one user can't access another's tasks)
- Test error cases and edge conditions

**Qwen Code Sub-Prompt**: "Test FastAPI backend with JWT authentication and task CRUD operations"

### Step 8: Integration Notes for Frontend
- Document API endpoints for frontend integration
- Specify required headers and payload formats
- Note authentication requirements and error responses
- Prepare API client examples for lib/api.ts

**Qwen Code Sub-Prompt**: "Document API endpoints for frontend integration with auth requirements"

## Error Handling & Common Issues

- JWT secret mismatch: Ensure BETTER_AUTH_SECRET is identical in frontend and backend
- DB connection errors: Verify DATABASE_URL format for Neon Postgres with sslmode=require
- User isolation failures: Double-check that all endpoints validate user_id from JWT against URL
- Migration issues: Ensure SQLModel metadata is properly configured in Alembic

## Timeline

- Estimated duration: 4-6 hours
- Recommended: Commit changes after each step for easier debugging
- Priority: Authentication and user isolation must work perfectly before moving to CRUD operations