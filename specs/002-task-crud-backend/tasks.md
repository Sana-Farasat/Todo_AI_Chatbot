# Task List: Task CRUD Backend API

**Feature**: Task CRUD Backend API  
**Branch**: `001-task-crud-backend`  
**Generated**: 2026-02-06  
**Spec**: [specs/001-task-crud-backend/spec.md](../001-task-crud-backend/spec.md)

## Overview

This document contains the dependency-ordered task list for implementing the secure Task CRUD API using FastAPI, SQLModel, and Neon Postgres with Better Auth JWT validation. Tasks are organized by user story to enable independent implementation and testing.

## Implementation Strategy

- **MVP Scope**: Implement User Story 1 (Secure Task Management) first to deliver core value
- **Incremental Delivery**: Complete each user story phase with independent test criteria
- **Parallel Opportunities**: Identified where tasks operate on different files/components
- **Quality Assurance**: Each task follows checklist format with IDs, story labels, and file paths

## Dependencies

- User Story 2 (Task Completion Tracking) depends on User Story 1 (Secure Task Management)
- User Story 3 (Secure Access Control) is implemented through authentication middleware that applies to all other stories
- Foundational tasks (database setup, authentication) must be completed before user story tasks

## Parallel Execution Examples

- Task model creation can run in parallel with database layer implementation
- JWT middleware can be developed in parallel with route implementation
- API endpoint tests can be written in parallel with endpoint implementation

---

## Phase 1: Setup

### Goal
Initialize the project structure and install required dependencies for the backend service.

- [ ] T001 Create backend directory structure with models, routes, middleware, and db modules
- [ ] T002 [P] Install FastAPI, SQLModel, asyncpg, PyJWT, Alembic, uvicorn using UV package manager
- [ ] T003 Create pyproject.toml with all required dependencies and build configuration
- [ ] T004 Create .env file template with DATABASE_URL and BETTER_AUTH_SECRET placeholders

---

## Phase 2: Foundational

### Goal
Set up the foundational components that all user stories depend on: database layer, authentication middleware, and data models.

- [X] T005 [P] Create Task model in backend/models.py following SQLModel conventions with user_id foreign key
- [X] T006 Create database connection layer in backend/db.py with async engine for Neon Postgres
- [X] T007 [P] Initialize Alembic migrations for Neon Postgres with SQLModel in backend/alembic/
- [X] T008 Implement JWT validation middleware in backend/middleware/jwt.py for Better Auth tokens
- [X] T009 Update main.py to include database dependency and JWT middleware
- [X] T010 Create initial migration for Task table and test migration with alembic upgrade head

---

## Phase 3: User Story 1 - Secure Task Management (Priority: P1)

### Goal
As an authenticated user, I want to securely manage my personal tasks so that I can organize my work and personal life.

### Independent Test Criteria
The system can be fully tested by authenticating a user and performing CRUD operations on their tasks, delivering the core value of task management.

- [X] T011 [P] [US1] Create GET /api/{user_id}/tasks endpoint in backend/routes/tasks.py with filtering options
- [X] T012 [P] [US1] Create POST /api/{user_id}/tasks endpoint for creating tasks with validation
- [X] T013 [US1] Create GET /api/{user_id}/tasks/{task_id} endpoint for retrieving specific tasks
- [X] T014 [US1] Create PUT /api/{user_id}/tasks/{task_id} endpoint for updating tasks with validation
- [X] T015 [US1] Create DELETE /api/{user_id}/tasks/{task_id} endpoint for deleting tasks
- [X] T016 [US1] Add authentication checks to all task endpoints to ensure user isolation
- [X] T017 [US1] Implement proper error handling for unauthorized access attempts

---

## Phase 4: User Story 2 - Task Completion Tracking (Priority: P2)

### Goal
As a user, I want to mark my tasks as completed so that I can track my progress and focus on remaining items.

### Independent Test Criteria
The system can be tested by creating a task, changing its completion status, and verifying the status updates correctly.

- [X] T018 [P] [US2] Create PATCH /api/{user_id}/tasks/{task_id}/complete endpoint for toggling completion status
- [X] T019 [US2] Add validation to ensure completed field is boolean in completion toggle endpoint
- [X] T020 [US2] Update task model to properly handle completion status updates with timestamp
- [X] T021 [US2] Add authentication checks to completion endpoint to ensure user isolation

---

## Phase 5: User Story 3 - Secure Access Control (Priority: P3)

### Goal
As a security-conscious user, I want to ensure that I can only access my own tasks and not others', so that my personal data remains private.

### Independent Test Criteria
The system can be tested by attempting to access tasks belonging to other users, which should result in access denial.

- [X] T022 [P] [US3] Enhance JWT middleware to validate user_id from token against URL path
- [X] T023 [US3] Add comprehensive authorization checks to all task endpoints
- [X] T024 [US3] Implement proper error responses for unauthorized access attempts (403 Forbidden)
- [X] T025 [US3] Test edge cases where user attempts to access tasks for another user

---

## Phase 6: Polish & Cross-Cutting Concerns

### Goal
Complete the implementation with proper documentation, testing, and integration preparation.

- [X] T026 Add comprehensive error handling with appropriate HTTP status codes
- [X] T027 [P] Create API documentation for frontend integration with auth requirements
- [X] T028 [P] Add logging for debugging and monitoring purposes
- [X] T029 Update CORS configuration to allow frontend integration
- [X] T030 Perform end-to-end testing of all implemented functionality
- [X] T031 Document API endpoints in quickstart guide for frontend team
- [X] T032 Optimize database queries for performance (add indexes where needed)
- [X] T033 Add input sanitization and security measures against injection attacks
- [X] T034 Update README with backend setup instructions and API usage