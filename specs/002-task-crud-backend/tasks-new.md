# Tasks: Task CRUD Backend API

**Input**: Design documents from `/specs/001-task-crud-backend/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

<!--
  ============================================================================
  IMPORTANT: The tasks below are based on actual design artifacts from:
  - spec.md: Contains user stories with priorities
  - plan.md: Contains technical implementation details
  - data-model.md: Contains entity definitions
  - contracts/: Contains API endpoint specifications
  ============================================================================-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend directory structure with models, routes, middleware, and db modules
- [ ] T002 [P] Install FastAPI, SQLModel, asyncpg, PyJWT, Alembic, uvicorn using UV package manager
- [ ] T003 Create pyproject.toml with all required dependencies and build configuration
- [ ] T004 Create .env file template with DATABASE_URL and BETTER_AUTH_SECRET placeholders

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [ ] T005 [P] Create Task model in backend/models.py following SQLModel conventions with user_id foreign key
- [ ] T006 Create database connection layer in backend/db.py with async engine for Neon Postgres
- [ ] T007 [P] Initialize Alembic migrations for Neon Postgres with SQLModel in backend/alembic/
- [ ] T008 Implement JWT validation middleware in backend/middleware/jwt.py for Better Auth tokens
- [ ] T009 Update main.py to include database dependency and JWT middleware
- [ ] T010 Create initial migration for Task table and test migration with alembic upgrade head

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Secure Task Management (Priority: P1) 🎯 MVP

**Goal**: As an authenticated user, I want to securely manage my personal tasks so that I can organize my work and personal life.

**Independent Test**: The system can be fully tested by authenticating a user and performing CRUD operations on their tasks, delivering the core value of task management.

### Implementation for User Story 1

- [ ] T011 [P] [US1] Create GET /api/{user_id}/tasks endpoint in backend/routes/tasks.py with filtering options
- [ ] T012 [P] [US1] Create POST /api/{user_id}/tasks endpoint for creating tasks with validation
- [ ] T013 [US1] Create GET /api/{user_id}/tasks/{task_id} endpoint for retrieving specific tasks
- [ ] T014 [US1] Create PUT /api/{user_id}/tasks/{task_id} endpoint for updating tasks with validation
- [ ] T015 [US1] Create DELETE /api/{user_id}/tasks/{task_id} endpoint for deleting tasks
- [ ] T016 [US1] Add authentication checks to all task endpoints to ensure user isolation
- [ ] T017 [US1] Implement proper error handling for unauthorized access attempts

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Completion Tracking (Priority: P2)

**Goal**: As a user, I want to mark my tasks as completed so that I can track my progress and focus on remaining items.

**Independent Test**: The system can be tested by creating a task, changing its completion status, and verifying the status updates correctly.

### Implementation for User Story 2

- [ ] T018 [P] [US2] Create PATCH /api/{user_id}/tasks/{task_id}/complete endpoint for toggling completion status
- [ ] T019 [US2] Add validation to ensure completed field is boolean in completion toggle endpoint
- [ ] T020 [US2] Update task model to properly handle completion status updates with timestamp
- [ ] T021 [US2] Add authentication checks to completion endpoint to ensure user isolation

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Secure Access Control (Priority: P3)

**Goal**: As a security-conscious user, I want to ensure that I can only access my own tasks and not others', so that my personal data remains private.

**Independent Test**: The system can be tested by attempting to access tasks belonging to other users, which should result in access denial.

### Implementation for User Story 3

- [ ] T022 [P] [US3] Enhance JWT middleware to validate user_id from token against URL path
- [ ] T023 [US3] Add comprehensive authorization checks to all task endpoints
- [ ] T024 [US3] Implement proper error responses for unauthorized access attempts (403 Forbidden)
- [ ] T025 [US3] Test edge cases where user attempts to access tasks for another user

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T026 Add comprehensive error handling with appropriate HTTP status codes
- [ ] T027 [P] Create API documentation for frontend integration with auth requirements
- [ ] T028 [P] Add logging for debugging and monitoring purposes
- [ ] T029 Update CORS configuration to allow frontend integration
- [ ] T030 Perform end-to-end testing of all implemented functionality
- [ ] T031 Document API endpoints in quickstart guide for frontend team
- [ ] T032 Optimize database queries for performance (add indexes where needed)
- [ ] T033 Add input sanitization and security measures against injection attacks
- [ ] T034 Update README with backend setup instructions and API usage

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Create Task model in backend/models.py following SQLModel conventions with user_id foreign key"

# Launch all endpoints for User Story 1 together:
Task: "Create GET /api/{user_id}/tasks endpoint in backend/routes/tasks.py with filtering options"
Task: "Create POST /api/{user_id}/tasks endpoint for creating tasks with validation"
Task: "Create GET /api/{user_id}/tasks/{task_id} endpoint for retrieving specific tasks"
Task: "Create PUT /api/{user_id}/tasks/{task_id} endpoint for updating tasks with validation"
Task: "Create DELETE /api/{user_id}/tasks/{task_id} endpoint for deleting tasks"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence