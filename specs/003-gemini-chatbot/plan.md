# Implementation Plan: AI Todo Chatbot with Gemini

**Branch**: `002-gemini-chatbot` | **Date**: 2026-02-28 | **Spec**: [spec.md](./spec.md)
**Input**: Create AI-powered todo chatbot using Gemini Free API, custom Next.js chat UI, MCP-style tools for task CRUD, conversation persistence in database, stateless FastAPI backend

## Summary

Build an AI-powered chatbot interface for managing todos through natural language using Google's Gemini Free API. The system features a custom Next.js chat UI with a floating action button, FastAPI backend with MCP-style tools for task operations, and stateless conversation management with database persistence.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5+ (frontend), React 18.3.1
**Primary Dependencies**: 
- Backend: FastAPI, SQLModel, google-generativeai (Gemini SDK), httpx
- Frontend: Next.js 16, Shadcn/Radix UI, Framer Motion (animations)
**Storage**: Neon Serverless PostgreSQL (existing), new tables: Conversation, Message
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web browser (desktop/mobile responsive)
**Project Type**: Web application (frontend + backend monorepo)
**Performance Goals**: 
- Chat response < 3 seconds (p95)
- Support 100 concurrent chat sessions
- Tool invocation accuracy > 90%
**Constraints**: 
- Gemini Free API rate limits (15 RPM, 1M TPM)
- Stateless server architecture
- Existing Better Auth integration required
**Scale/Scope**: 
- Single user sessions (authenticated)
- Conversation history persistence
- 5 MCP tools (add, list, complete, delete, update tasks)

## Constitution Check

✅ **GATE 1**: Spec-driven - All decisions traceable to spec requirements
✅ **GATE 2**: Smallest viable change - Reuse existing auth, DB, task models
✅ **GATE 3**: No over-engineering - Gemini Free API (no OpenAI costs), simple chat UI
✅ **GATE 4**: Testability - Each tool independently testable, stateless design
✅ **GATE 5**: Security - Existing JWT auth, user isolation maintained

## Project Structure

### Documentation (this feature)

```text
specs/002-gemini-chatbot/
├── plan.md              # This file
├── spec.md              # Feature specification
├── checklists/
│   └── requirements.md  # Spec quality checklist
├── contracts/           # API contracts (created in Phase 1)
│   └── chat-api-contract.md
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── models.py            # Add: Conversation, Message models
├── routes/
│   ├── tasks.py         # Existing task CRUD
│   └── chat.py          # NEW: Chat endpoint + MCP tools
├── services/
│   ├── gemini_agent.py  # NEW: Gemini AI agent + tool definitions
│   └── mcp_tools.py     # NEW: MCP-style tool functions
├── db.py                # Existing DB config (reuse)
└── requirements.txt     # Add: google-generativeai

frontend/
├── app/
│   ├── chat/
│   │   └── page.tsx     # NEW: Chat page
│   └── api/
│       └── chat/
│           └── route.ts # Optional: BFF layer (if needed)
├── components/
│   ├── chat/
│   │   ├── ChatBot.tsx        # NEW: Main chat container
│   │   ├── ChatMessage.tsx    # NEW: Message bubble
│   │   ├── ChatInput.tsx      # NEW: Input field
│   │   └── ChatBotIcon.tsx    # NEW: Floating action button
│   └── ui/              # Reuse Shadcn components
└── lib/
    └── api.ts           # Add: chat API calls
```

**Structure Decision**: Web application structure (Option 2). Backend adds chat routes and services. Frontend adds chat page and components with floating action button in bottom-right corner.

## Architecture Overview

```
┌─────────────────┐     ┌─────────────────────────────────┐     ┌──────────────┐
│  Next.js App    │────▶│  FastAPI Server                 │────▶│  Gemini API  │
│  (Chat UI +     │     │  - POST /api/{user_id}/chat     │     │  (Free tier) │
│   FAB Icon)     │◀────│  - Gemini Agent + MCP Tools     │     │              │
└─────────────────┘     │  - Stateless conversation mgmt  │     └──────────────┘
                        └───────────────┬─────────────────┘
                                        ▼
                              ┌──────────────────┐
                              │  Neon PostgreSQL │
                              │  - tasks         │
                              │  - conversations │
                              │  - messages      │
                              └──────────────────┘
```

## Key Technical Decisions

### 1. Gemini API over OpenAI
**Decision**: Use Google Gemini Free API instead of OpenAI (as per user requirement)
**Rationale**: 
- Free tier (no cost for hackathon)
- Similar capabilities for natural language understanding
- Easy SDK integration (`google-generativeai` package)

### 2. MCP-Style Tools Pattern
**Decision**: Implement MCP-style tools without official MCP SDK
**Rationale**:
- Existing task APIs already functional
- Simple function-based tools for AI agent
- Maintains stateless architecture

### 3. Floating Action Button (FAB)
**Decision**: Beautiful chatbot icon in bottom-right corner
**Rationale**:
- Industry standard pattern (Intercom, Drift, etc.)
- Always accessible without navigation
- Smooth animations with Framer Motion

### 4. Stateless Conversation Management
**Decision**: Store all conversation state in database
**Rationale**:
- Server can restart without losing context
- Horizontal scaling possible
- Any server instance handles any request

## Database Schema Changes

### New Models

**Conversation**
```python
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Message**
```python
class Message(SQLModel, table=True):
    __tablename__ = "messages"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## API Contract (New Endpoint)

### POST /api/{user_id}/chat

**Request**:
```json
{
  "conversation_id": 123,  // Optional - creates new if not provided
  "message": "Add a task to buy groceries"
}
```

**Response**:
```json
{
  "conversation_id": 123,
  "response": "I've added 'Buy groceries' to your task list!",
  "tool_calls": [
    {
      "tool": "add_task",
      "parameters": {"title": "Buy groceries"},
      "result": {"task_id": 5, "status": "created"}
    }
  ]
}
```

## MCP Tools Specification

| Tool | Function | Parameters | Returns |
|------|----------|------------|---------|
| `add_task` | Create task | user_id, title, description (opt) | task_id, status |
| `list_tasks` | Get tasks | user_id, status (opt) | Task[] |
| `complete_task` | Mark done | user_id, task_id | status |
| `delete_task` | Remove task | user_id, task_id | status |
| `update_task` | Modify task | user_id, task_id, title/desc (opt) | status |

## Frontend Components

### ChatBotIcon (FAB)
- Fixed position: bottom-right (24px from edges)
- Animated pulse effect when new message
- Click to open chat window
- Beautiful gradient/icon design

### ChatBot (Main Container)
- Slide-in animation from bottom
- Fixed width: 380px (mobile responsive)
- Height: 600px (or 80vh on mobile)
- Header with close button
- Message list (scrollable)
- Input field with send button

### ChatMessage (Bubble)
- User messages: right-aligned, blue gradient
- Assistant messages: left-aligned, gray background
- Timestamps
- Tool call indicators (when actions performed)

### ChatInput (Form)
- Textarea with auto-resize
- Send button (Enter to send)
- Loading state during API call
- Character limit: 500

## Implementation Phases

### Phase 0: Setup & Dependencies
1. Install `google-generativeai` in backend
2. Add Gemini API key to `.env`
3. Create database migration for Conversation, Message

### Phase 1: Backend Implementation
1. Create Conversation, Message models
2. Implement MCP tools (5 functions)
3. Build Gemini agent with tool definitions
4. Create `/api/{user_id}/chat` endpoint
5. Add conversation history management

### Phase 2: Frontend Implementation
1. Create ChatBotIcon (FAB) component
2. Build ChatBot main container
3. Implement ChatMessage bubbles
4. Create ChatInput form
5. Add API integration
6. Style with Shadcn + Framer Motion

### Phase 3: Testing & Polish
1. Test all MCP tools independently
2. Test conversation persistence
3. Test error handling
4. Polish animations and transitions
5. Mobile responsiveness

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Gemini API rate limits | Medium | Implement retry logic, queue messages |
| Token context overflow | Low | Limit conversation history to last 20 messages |
| Tool misinterpretation | Medium | Clear tool descriptions, few-shot examples |
| UI performance | Low | Virtual scrolling for long conversations |

## Success Metrics

- ✅ All 5 MCP tools functional and testable
- ✅ Chat response time < 3s (p95)
- ✅ Conversation persists across server restarts
- ✅ Beautiful FAB icon with smooth animations
- ✅ Mobile-responsive chat UI
- ✅ Error handling for all edge cases
