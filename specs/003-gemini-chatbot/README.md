# AI Todo Chatbot with Gemini

Manage your tasks using natural language conversations powered by Google's Gemini AI.

## Features

- 💬 **Natural Language Chat** - Add, view, complete, delete, and update tasks using conversation
- 🤖 **AI-Powered** - Powered by Google Gemini 1.5 Flash (free tier)
- 💾 **Persistent Conversations** - Chat history saved across sessions
- 🎨 **Beautiful UI** - Floating action button with smooth animations
- 🔐 **Secure** - JWT authentication with user isolation

## Quick Start

### 1. Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### 2. Configure Backend

```bash
cd backend
```

Edit `.env` and add your Gemini API key:

```env
GEMINI_API_KEY="your-actual-api-key-here"
```

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
cd backend
alembic upgrade head
```

### 5. Start Backend Server

```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

### 6. Configure Frontend

Edit `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 7. Start Frontend

```bash
cd frontend
npm run dev
```

Visit `http://localhost:3000`

## Usage

### Opening the Chat

1. Click the purple chat icon in the bottom-right corner
2. The chat window will slide in smoothly

### Example Commands

**Add Tasks:**
- "Add a task to buy groceries"
- "Create a task: Call mom tomorrow"
- "I need to finish the report by Friday"

**View Tasks:**
- "Show me my tasks"
- "What are my pending tasks?"
- "List completed tasks"

**Complete Tasks:**
- "Mark task 1 as complete"
- "I finished task 3"
- "Task 2 is done"

**Delete Tasks:**
- "Delete task 5"
- "Remove the first task"
- "Get rid of task 2"

**Update Tasks:**
- "Change task 1 to 'Buy milk and eggs'"
- "Update task 3 description to 'Call at 3pm'"

## API Endpoints

### POST /api/{user_id}/chat

Send a message to the AI chatbot.

**Request:**
```json
{
  "conversation_id": 123,
  "message": "Add a task to buy groceries"
}
```

**Response:**
```json
{
  "conversation_id": 123,
  "response": "I've added 'Buy groceries' to your task list!",
  "tool_calls": [
    {
      "tool": "add_task",
      "parameters": {"title": "Buy groceries"},
      "result": {"task_id": 5, "status": "created", "title": "Buy groceries"}
    }
  ],
  "message_id": 456
}
```

### GET /api/{user_id}/chat/history

Get conversation history.

**Query Parameters:**
- `conversation_id` (optional) - Specific conversation ID

### DELETE /api/{user_id}/chat/conversation/{conversation_id}

Delete a conversation and all its messages.

## MCP Tools

The chatbot uses 5 MCP-style tools:

| Tool | Description | Parameters |
|------|-------------|------------|
| `add_task` | Create a new task | title (required), description (optional) |
| `list_tasks` | List tasks | status: "all", "pending", "completed" |
| `complete_task` | Mark task complete | task_id (required) |
| `delete_task` | Delete a task | task_id (required) |
| `update_task` | Update task | task_id (required), title, description |

## Architecture

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

## Tech Stack

**Backend:**
- FastAPI
- SQLModel (ORM)
- Google Generative AI (Gemini SDK)
- PostgreSQL (Neon)
- Alembic (migrations)

**Frontend:**
- Next.js 16
- React 18
- Framer Motion (animations)
- Shadcn/Radix UI (components)
- TypeScript

## Rate Limits

**Gemini Free Tier:**
- 15 requests per minute
- 1,000,000 tokens per minute

The app handles rate limiting gracefully with retry logic.

## Troubleshooting

### "GEMINI_API_KEY not found"

Make sure you've added your API key to `backend/.env`:
```env
GEMINI_API_KEY="your-key-here"
```

### "Conversation not found"

Ensure you're authenticated and using the correct user ID.

### Chat not appearing

1. Check that backend is running on port 8000
2. Verify `NEXT_PUBLIC_API_URL` in `.env.local`
3. Make sure you're signed in

### Tasks not being created

1. Verify database migration ran: `alembic upgrade head`
2. Check database connection in `.env`
3. Ensure JWT authentication is working

## Development

### Running Tests

```bash
cd backend
pytest
```

### Database Reset

```bash
cd backend
alembic downgrade base
alembic upgrade head
```

## License

MIT

## Support

For issues or questions, please open an issue on GitHub.
