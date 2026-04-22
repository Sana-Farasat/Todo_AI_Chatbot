# Tasks: AI Todo Chatbot with Gemini

**Input**: Design documents from `/specs/002-gemini-chatbot/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: Included (contract + integration tests for chat flow)

**Organization**: Tasks organized by user story for independent implementation and testing

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story mapping (US1-US5)
- File paths: `backend/`, `frontend/` (web app monorepo)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install dependencies and configure environment

- [X] T001 [P] Install `google-generativeai==0.3.2` in backend (`pip install google-generativeai`)
- [X] T002 [P] Add `GEMINI_API_KEY` to `backend/.env`
- [X] T003 [P] Verify backend dependencies in `requirements.txt`
- [X] T004 [P] Verify frontend dependencies (Framer Motion already installed)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create database migration for `conversations` and `messages` tables in `backend/alembic/versions/`
- [X] T006 Run migration: `alembic upgrade head`
- [X] T007 [P] Add `Conversation` model to `backend/models.py`
- [X] T008 [P] Add `Message` model to `backend/models.py`
- [X] T009 [P] Create `backend/services/mcp_tools.py` with tool interface
- [X] T010 [P] Create `backend/services/gemini_agent.py` with agent skeleton
- [X] T011 [P] Create `backend/routes/chat.py` with endpoint skeleton
- [X] T012 Register chat router in `backend/main.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Chat to Add Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can add tasks via natural language chat

**Independent Test**: Send "Add task to buy groceries" → task created → confirmation received

### Tests for User Story 1 ⚠️

> **Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T013 [P] [US1] Contract test for chat endpoint in `backend/test_chat_contract.py`
- [ ] T014 [P] [US1] Integration test for add_task flow in `backend/test_chat_integration.py`

### Implementation for User Story 1

- [X] T015 [P] [US1] Implement `add_task()` MCP tool in `backend/services/mcp_tools.py`
- [X] T016 [P] [US1] Implement `list_tasks()` MCP tool in `backend/services/mcp_tools.py`
- [X] T017 [US1] Define Gemini tool schema in `backend/services/gemini_agent.py`
- [X] T018 [US1] Implement agent message processing in `backend/services/gemini_agent.py`
- [X] T019 [US1] Implement conversation history fetch in `backend/routes/chat.py`
- [X] T020 [US1] Implement message persistence in `backend/routes/chat.py`
- [X] T021 [US1] Complete POST `/api/{user_id}/chat` endpoint in `backend/routes/chat.py`
- [X] T022 [US1] Create `ChatRequest` and `ChatResponse` Pydantic models
- [X] T023 [US1] Add error handling for Gemini API calls
- [X] T024 [US1] Add logging for chat operations

**Checkpoint**: US1 complete - can add tasks via chat independently

---

## Phase 4: User Story 2 - View Tasks via Chat (Priority: P2)

**Goal**: Users can view tasks with filters via natural language

**Independent Test**: Send "Show my tasks" or "What's pending?" → correct task list returned

### Tests for User Story 2 ⚠️

- [ ] T025 [P] [US2] Integration test for list_tasks with filters in `backend/test_chat_integration.py`

### Implementation for User Story 2

- [X] T026 [P] [US2] Enhance `list_tasks()` tool with status filter in `backend/services/mcp_tools.py`
- [X] T027 [US2] Add few-shot examples for list queries in `backend/services/gemini_agent.py`
- [X] T028 [US2] Implement task formatting for chat responses
- [X] T029 [US2] Add "no tasks found" handling

**Checkpoint**: US1 + US2 complete - can add and view tasks via chat

---

## Phase 5: User Story 3 - Complete/Delete Tasks (Priority: P3)

**Goal**: Users can mark tasks done or remove them via chat

**Independent Test**: Send "Mark task 3 complete" or "Delete task 2" → task updated/deleted

### Tests for User Story 3 ⚠️

- [ ] T030 [P] [US3] Integration test for complete_task in `backend/test_chat_integration.py`
- [ ] T031 [P] [US3] Integration test for delete_task in `backend/test_chat_integration.py`

### Implementation for User Story 3

- [X] T032 [P] [US3] Implement `complete_task()` MCP tool in `backend/services/mcp_tools.py`
- [X] T033 [P] [US3] Implement `delete_task()` MCP tool in `backend/services/mcp_tools.py`
- [X] T034 [US3] Add few-shot examples for complete/delete queries
- [X] T035 [US3] Handle "task not found" errors gracefully
- [X] T036 [US3] Add confirmation messages for destructive actions

**Checkpoint**: US1-3 complete - full task CRUD via chat

---

## Phase 6: User Story 4 - Update Tasks via Chat (Priority: P4)

**Goal**: Users can modify task title/description via chat

**Independent Test**: Send "Change task 1 to 'Call mom tonight'" → task updated

### Tests for User Story 4 ⚠️

- [ ] T037 [P] [US4] Integration test for update_task in `backend/test_chat_integration.py`

### Implementation for User Story 4

- [X] T038 [P] [US4] Implement `update_task()` MCP tool in `backend/services/mcp_tools.py`
- [X] T039 [US4] Add few-shot examples for update queries
- [X] T040 [US4] Handle partial updates (title only, description only)

**Checkpoint**: All 5 MCP tools functional

---

## Phase 7: User Story 5 - Conversation Persistence (Priority: P5)

**Goal**: Conversations persist across server restarts and sessions

**Independent Test**: Send messages → restart server → resume conversation → history intact

### Tests for User Story 5 ⚠️

- [ ] T041 [P] [US5] Test conversation history retrieval in `backend/test_chat_integration.py`
- [ ] T042 [P] [US5] Test conversation resumption after restart

### Implementation for User Story 5

- [X] T043 [P] [US5] Implement conversation creation logic in `backend/routes/chat.py`
- [X] T044 [US5] Implement conversation history limit (last 20 messages)
- [X] T045 [US5] Add conversation updated_at timestamp logic
- [X] T046 [US5] Test database persistence across restarts

**Checkpoint**: All backend user stories complete

---

## Phase 8: Frontend - Chat Components (Priority: P1-P5)

**Goal**: Beautiful chat UI with floating action button

### Tests for Frontend ⚠️

- [ ] T047 [P] [FE] Manual test: Chat icon visible in bottom-right
- [ ] T048 [P] [FE] Manual test: Chat window opens/closes smoothly
- [ ] T049 [FE] Manual test: Messages send and display correctly

### Implementation for Frontend

#### Floating Action Button (FAB)
- [X] T050 [P] [FE] Create `frontend/components/chat/ChatBotIcon.tsx` (FAB component)
- [X] T051 [FE] Style FAB with purple gradient and pulse animation
- [X] T052 [FE] Add click handler to open chat window
- [X] T053 [FE] Add Framer Motion hover/press animations

#### Chat Window
- [X] T054 [P] [FE] Create `frontend/components/chat/ChatBot.tsx` (main container)
- [X] T055 [FE] Style chat window (380px width, 600px height, responsive)
- [X] T056 [FE] Add slide-in animation (Framer Motion)
- [X] T057 [FE] Add header with close button
- [X] T058 [FE] Add message list (scrollable)

#### Message Components
- [X] T059 [P] [FE] Create `frontend/components/chat/ChatMessage.tsx`
- [X] T060 [FE] Style user messages (right, blue gradient)
- [X] T061 [FE] Style assistant messages (left, gray background)
- [X] T062 [FE] Add timestamps
- [X] T063 [FE] Add tool call indicators

#### Input Component
- [X] T064 [P] [FE] Create `frontend/components/chat/ChatInput.tsx`
- [X] T065 [FE] Add textarea with auto-resize
- [X] T066 [FE] Add send button (Enter to send)
- [X] T067 [FE] Add loading state during API call
- [X] T068 [FE] Add character limit (500 chars)

#### API Integration
- [X] T069 [P] [FE] Add `chat()` function to `frontend/lib/api.ts`
- [X] T070 [FE] Create `frontend/app/chat/page.tsx` (chat page route)
- [X] T071 [FE] Integrate chat components in page
- [X] T072 [FE] Handle authentication (JWT token)
- [X] T073 [FE] Handle errors gracefully (toast notifications)

#### Polish
- [X] T074 [P] [FE] Mobile responsiveness (80vh on mobile)
- [X] T075 [FE] Add notification badge on FAB for new messages
- [X] T076 [FE] Add sound effects (optional)
- [X] T077 [FE] Test across browsers

**Checkpoint**: Frontend complete - beautiful chat UI functional

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements affecting multiple user stories

- [ ] T078 [P] Update `README.md` with chatbot setup instructions
- [X] T079 [P] Add API documentation to `specs/002-gemini-chatbot/`
- [ ] T080 Code cleanup and refactoring
- [ ] T081 Performance optimization (DB queries, API calls)
- [ ] T082 [P] Run quickstart.md validation
- [ ] T083 [P] Test rate limiting behavior
- [ ] T084 Security review (auth, data isolation)
- [ ] T085 [P] Final E2E testing

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start immediately
- **Foundational (Phase 2)**: Depends on Setup - **BLOCKS all user stories**
- **Backend User Stories (Phase 3-7)**: All depend on Foundational
  - Can proceed sequentially (P1 → P2 → P3 → P4 → P5)
  - Or parallel if multiple developers
- **Frontend (Phase 8)**: Depends on Backend Phase 3+ (need working API)
- **Polish (Phase 9)**: Depends on all above

### User Story Dependencies

- **US1 (P1)**: After Foundational - No story dependencies
- **US2 (P2)**: After Foundational - Independent of US1
- **US3 (P3)**: After Foundational - Independent of US1-2
- **US4 (P4)**: After Foundational - Independent of US1-3
- **US5 (P5)**: After Foundational - Independent of US1-4

### Within Each User Story

1. Tests first (ensure FAIL)
2. MCP tools implementation
3. Agent integration
4. Endpoint completion
5. Error handling + logging

### Parallel Opportunities

**Setup Phase**:
- T001, T002, T003, T004 (all [P])

**Foundational Phase**:
- T007, T008, T009, T010, T011 (all [P])

**Backend User Stories**:
- All MCP tools within a story marked [P]
- Different user stories can be parallelized

**Frontend Phase**:
- T050, T054, T059, T064, T069 (all [P] - different components)
- Component implementation can parallelize after API contract known

---

## Parallel Example: Backend MCP Tools

```bash
# Launch all MCP tool implementations together:
Task: "Implement add_task() in mcp_tools.py"
Task: "Implement list_tasks() in mcp_tools.py"
Task: "Implement complete_task() in mcp_tools.py"
Task: "Implement delete_task() in mcp_tools.py"
Task: "Implement update_task() in mcp_tools.py"
```

---

## Parallel Example: Frontend Components

```bash
# Launch all component creations together:
Task: "Create ChatBotIcon.tsx"
Task: "Create ChatBot.tsx"
Task: "Create ChatMessage.tsx"
Task: "Create ChatInput.tsx"
Task: "Add chat() to api.ts"
```

---

## Implementation Strategy

### MVP First (Backend US1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: US1 (add tasks via chat)
4. **STOP and VALIDATE**: Test adding task via curl
5. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Backend foundation ready
2. Add US1 → Test independently → Demo (add tasks via chat!)
3. Add US2 → Test → Demo (view tasks via chat!)
4. Add US3-4 → Test → Demo (full CRUD via chat!)
5. Add US5 → Test → Demo (conversation persistence!)
6. Add Frontend → Test → Demo (beautiful UI!)

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational done:
   - Developer A: Backend US1-5 (Phases 3-7)
   - Developer B: Frontend components (Phase 8)
3. Integrate and test together

---

## Notes

- [P] tasks = different files, no dependencies, can parallelize
- [Story] label = US1-US5 for backend, FE for frontend
- Each user story independently testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at checkpoints to validate independently
- Backend API contract must be stable before frontend implementation
- FAB icon design: purple gradient, bottom-right, pulse animation
