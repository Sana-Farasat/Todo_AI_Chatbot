# Quickstart: AI Todo Chatbot

## Prerequisites

- ✅ Phase 1 & 2 completed (task CRUD + frontend UI)
- ✅ Python 3.11+ installed
- ✅ Node.js 18+ installed
- ✅ Neon PostgreSQL database configured
- ✅ Better Auth working
- ✅ Gemini API key (free)

## Step 1: Get Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key (starts with `AIza...`)

## Step 2: Backend Setup

### Install Dependencies

```bash
cd backend
pip install google-generativeai==0.3.2
```

### Add Environment Variable

Create/update `backend/.env`:

```env
DATABASE_URL="postgresql+asyncpg://..."
BETTER_AUTH_SECRET="..."
GEMINI_API_KEY="AIzaSy..."  # Add this line
```

### Run Database Migration

```bash
cd backend
alembic upgrade head
```

This creates `conversations` and `messages` tables.

## Step 3: Verify Backend

```bash
cd backend
uvicorn main:app --reload
```

Check server starts without errors.

## Step 4: Frontend Setup

No new dependencies needed (using existing Shadcn + Framer Motion).

```bash
cd frontend
npm install  # Ensure all existing deps installed
```

## Step 5: Test Chat Endpoint

```bash
# Get auth token first (sign in via frontend)
# Then test chat endpoint

curl -X POST http://localhost:8000/api/testuser/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, can you help me add a task?"}'
```

Expected response:
```json
{
  "conversation_id": 1,
  "response": "Hello! I'd be happy to help you add a task...",
  "tool_calls": [],
  "message_id": 1
}
```

## Step 6: Development Workflow

### Backend Changes
1. Edit files in `backend/routes/chat.py`, `backend/services/`
2. Server auto-reloads (uvicorn --reload)
3. Test via curl or frontend

### Frontend Changes
1. Edit files in `frontend/app/chat/`, `frontend/components/chat/`
2. Dev server auto-reloads (next dev)
3. Open `http://localhost:3000/chat`

## Step 7: Testing Checklist

### Backend Tests

```bash
# Test conversation creation
POST /api/{user_id}/chat with new conversation

# Test task creation via chat
POST /api/{user_id}/chat with "Add task to buy milk"

# Test task listing via chat
POST /api/{user_id}/chat with "Show my tasks"

# Test conversation persistence
Send multiple messages, restart server, resume conversation
```

### Frontend Tests

- [ ] Chatbot icon appears in bottom-right
- [ ] Click icon opens chat window
- [ ] Can send messages
- [ ] Responses display correctly
- [ ] Tool calls show visual feedback
- [ ] Conversation persists on refresh
- [ ] Close button works
- [ ] Mobile responsive

## Common Issues

### Issue: Gemini API Error

**Error**: `403 Forbidden` or `API_KEY_INVALID`

**Solution**:
1. Verify API key in `.env`
2. Check key starts with `AIza`
3. Ensure no extra spaces in `.env`
4. Restart backend after adding key

### Issue: Database Tables Missing

**Error**: `relation "conversations" does not exist`

**Solution**:
```bash
cd backend
alembic upgrade head
```

### Issue: JWT Authentication Fails

**Error**: `401 Not authenticated`

**Solution**:
1. Sign in via frontend `/sign-in`
2. Copy token from request headers
3. Use in chat API requests

### Issue: Chatbot Icon Not Showing

**Error**: Icon not visible on page

**Solution**:
1. Check component imported in layout/page
2. Verify z-index (should be 9999)
3. Check console for React errors
4. Ensure Tailwind CSS loaded

## File Structure Reference

```
backend/
├── routes/
│   ├── tasks.py         # Existing
│   └── chat.py          # NEW
├── services/
│   ├── gemini_agent.py  # NEW
│   └── mcp_tools.py     # NEW
└── models.py            # Add Conversation, Message

frontend/
├── app/
│   └── chat/
│       └── page.tsx     # NEW
├── components/
│   └── chat/
│       ├── ChatBot.tsx        # NEW
│       ├── ChatBotIcon.tsx    # NEW (FAB)
│       ├── ChatMessage.tsx    # NEW
│       └── ChatInput.tsx      # NEW
└── lib/
    └── api.ts           # Add chat function
```

## Next Steps

After quickstart verification:

1. **Implement Backend** (`/sp.tasks` Phase 1)
   - Create models
   - Build MCP tools
   - Implement chat endpoint

2. **Implement Frontend** (`/sp.tasks` Phase 2)
   - Create chat components
   - Add FAB icon
   - Style with animations

3. **Testing** (`/sp.tasks` Phase 3)
   - Unit tests for tools
   - Integration tests for chat flow
   - E2E tests for user scenarios

## Resources

- [Gemini API Docs](https://ai.google.dev/docs)
- [Spec Document](./spec.md)
- [Plan Document](./plan.md)
- [API Contract](./contracts/chat-api-contract.md)
- [Data Model](./data-model.md)

## Support

Issues or questions:
1. Check common issues above
2. Review error logs (`backend/` console, browser console)
3. Verify all prerequisites met
4. Check environment variables set correctly
