# API Contract: Chat Endpoint

## Overview

This document defines the API contract for the AI Todo Chatbot chat endpoint. The contract ensures consistent communication between frontend and backend, with clear request/response formats and error handling.

## Base URL

```
Production: https://your-api-domain.com
Local Dev:  http://localhost:8000
```

## Authentication

All endpoints require authentication via Better Auth JWT token.

**Header Format**:
```
Authorization: Bearer <jwt_token>
```

**Token Validation**:
- Token decoded via JWKS endpoint
- `user_id` extracted from token payload
- User isolation enforced on all operations

---

## Endpoint: POST /api/{user_id}/chat

Send a message to the AI chatbot and receive a response with optional tool invocations.

### Method
`POST`

### URL Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string | Yes | User identifier (must match JWT token) |

### Request Headers

| Header | Value | Required | Description |
|--------|-------|----------|-------------|
| `Authorization` | `Bearer <token>` | Yes | JWT token from Better Auth |
| `Content-Type` | `application/json` | Yes | Request format |

### Request Body

```json
{
  "conversation_id": 123,
  "message": "Add a task to buy groceries"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `conversation_id` | integer | No | Existing conversation ID. If omitted, creates new conversation |
| `message` | string | Yes | User's natural language message (max 500 chars) |

### Request Validation

```python
class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str = Field(..., min_length=1, max_length=500)
    
    @validator('message')
    def message_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty or whitespace')
        return v.strip()
```

### Response: Success (200 OK)

```json
{
  "conversation_id": 123,
  "response": "I've added 'Buy groceries' to your task list!",
  "tool_calls": [
    {
      "tool": "add_task",
      "parameters": {
        "title": "Buy groceries"
      },
      "result": {
        "task_id": 5,
        "status": "created",
        "title": "Buy groceries"
      }
    }
  ],
  "message_id": 456
}
```

| Field | Type | Description |
|-------|------|-------------|
| `conversation_id` | integer | The conversation ID (new or existing) |
| `response` | string | AI assistant's natural language response |
| `tool_calls` | array | List of MCP tools invoked (empty if no tools needed) |
| `tool_calls[].tool` | string | Name of the tool invoked |
| `tool_calls[].parameters` | object | Parameters passed to the tool |
| `tool_calls[].result` | object | Result returned by the tool |
| `message_id` | integer | ID of the stored assistant message |

### Response: Error (4xx/5xx)

**401 Unauthorized - Missing Token**
```json
{
  "detail": "Not authenticated"
}
```

**403 Forbidden - User Mismatch**
```json
{
  "detail": "Not authorized to access this conversation"
}
```

**404 Not Found - Conversation Not Found**
```json
{
  "detail": "Conversation not found"
}
```

**422 Validation Error**
```json
{
  "detail": [
    {
      "loc": ["body", "message"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

**500 Internal Server Error**
```json
{
  "detail": "Gemini API unavailable",
  "error_code": "EXTERNAL_SERVICE_ERROR"
}
```

---

## MCP Tools Specification

The chatbot uses 5 MCP-style tools to interact with the task management system.

### Tool: add_task

**Purpose**: Create a new todo task

**Parameters**:
```json
{
  "user_id": "string (required)",
  "title": "string (required, max 200 chars)",
  "description": "string (optional)"
}
```

**Returns**:
```json
{
  "task_id": 5,
  "status": "created",
  "title": "Buy groceries"
}
```

**Example Invocation**:
```
User: "Add a task to buy groceries"
→ Tool: add_task
→ Parameters: {"title": "Buy groceries"}
→ Result: {"task_id": 5, "status": "created", "title": "Buy groceries"}
```

---

### Tool: list_tasks

**Purpose**: Retrieve tasks with optional filtering

**Parameters**:
```json
{
  "user_id": "string (required)",
  "status": "string (optional: 'all', 'pending', 'completed')"
}
```

**Returns**:
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-02-28T10:00:00Z"
  },
  {
    "id": 2,
    "title": "Call mom",
    "completed": true,
    "created_at": "2026-02-27T15:30:00Z"
  }
]
```

**Example Invocation**:
```
User: "Show me all my tasks"
→ Tool: list_tasks
→ Parameters: {"status": "all"}
→ Result: [{...}, {...}]
```

---

### Tool: complete_task

**Purpose**: Mark a task as complete

**Parameters**:
```json
{
  "user_id": "string (required)",
  "task_id": "integer (required)"
}
```

**Returns**:
```json
{
  "task_id": 3,
  "status": "completed",
  "title": "Call mom"
}
```

**Example Invocation**:
```
User: "Mark task 3 as complete"
→ Tool: complete_task
→ Parameters: {"task_id": 3}
→ Result: {"task_id": 3, "status": "completed", "title": "Call mom"}
```

---

### Tool: delete_task

**Purpose**: Remove a task from the list

**Parameters**:
```json
{
  "user_id": "string (required)",
  "task_id": "integer (required)"
}
```

**Returns**:
```json
{
  "task_id": 2,
  "status": "deleted",
  "title": "Old task"
}
```

**Example Invocation**:
```
User: "Delete the meeting task"
→ Tool: list_tasks (to find task ID)
→ Tool: delete_task
→ Parameters: {"task_id": 2}
→ Result: {"task_id": 2, "status": "deleted", "title": "Old task"}
```

---

### Tool: update_task

**Purpose**: Modify task title or description

**Parameters**:
```json
{
  "user_id": "string (required)",
  "task_id": "integer (required)",
  "title": "string (optional)",
  "description": "string (optional)"
}
```

**Returns**:
```json
{
  "task_id": 1,
  "status": "updated",
  "title": "Buy groceries and fruits"
}
```

**Example Invocation**:
```
User: "Change task 1 to 'Buy groceries and fruits'"
→ Tool: update_task
→ Parameters: {"task_id": 1, "title": "Buy groceries and fruits"}
→ Result: {"task_id": 1, "status": "updated", "title": "Buy groceries and fruits"}
```

---

## Conversation Flow

### Stateless Request Cycle

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Client  │     │  API    │     │   DB    │     │ Gemini  │     │  Tools  │
└────┬────┘     └────┬────┘     └────┬────┘     └────┬────┘     └────┬────┘
     │               │               │               │               │
     │ POST /chat    │               │               │               │
     │──────────────▶│               │               │               │
     │               │               │               │               │
     │               │ Fetch history │               │               │
     │               │──────────────▶│               │               │
     │               │               │               │               │
     │               │◀──────────────│               │               │
     │               │ History       │               │               │
     │               │               │               │               │
     │               │ Store message │               │               │
     │               │──────────────▶│               │               │
     │               │               │               │               │
     │               │ Run agent     │               │               │
     │               │──────────────────────────────▶│               │
     │               │               │               │               │
     │               │               │               │ Invoke tool   │
     │               │──────────────────────────────────────────────▶│
     │               │               │               │               │
     │               │◀──────────────────────────────────────────────│
     │               │ Tool result   │               │               │
     │               │               │               │               │
     │               │◀──────────────│               │               │
     │               │ AI response   │               │               │
     │               │               │               │               │
     │               │ Store response│               │               │
     │               │──────────────▶│               │               │
     │               │               │               │               │
     │               │ Response      │               │               │
     │◀──────────────│               │               │               │
     │               │               │               │               │
```

### Step-by-Step Flow

1. **Client sends message**
   - POST `/api/{user_id}/chat`
   - Body: `{conversation_id?, message}`

2. **Server fetches conversation history**
   - Query: Last 20 messages from DB
   - Filter: `user_id` and `conversation_id`

3. **Server stores user message**
   - Create Message record (role: "user")
   - Update Conversation.updated_at

4. **Server runs Gemini agent**
   - Build message array (system prompt + history + new message)
   - Include tool definitions
   - Call Gemini API

5. **Agent invokes tools**
   - Parse tool calls from Gemini response
   - Execute MCP tool functions
   - Collect results

6. **Server stores assistant response**
   - Create Message record (role: "assistant")
   - Include tool call metadata in content

7. **Server returns response**
   - Send JSON response to client
   - No state held in server

---

## Error Handling

### Error Categories

| Category | HTTP Code | Recovery |
|----------|-----------|----------|
| Authentication | 401 | Re-authenticate |
| Authorization | 403 | Check permissions |
| Not Found | 404 | Create new resource |
| Validation | 422 | Fix request format |
| Rate Limit | 429 | Retry after delay |
| Server Error | 500 | Retry or escalate |
| External Service | 503 | Retry with backoff |

### Tool Error Handling

**Task Not Found**:
```json
{
  "tool": "complete_task",
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "Task with ID 5 not found",
    "suggestion": "Try listing your tasks first to find the correct ID"
  }
}
```

**Database Error**:
```json
{
  "tool": "add_task",
  "error": {
    "code": "DB_ERROR",
    "message": "Failed to create task",
    "suggestion": "Please try again in a moment"
  }
}
```

### Gemini API Error Handling

**Rate Limit**:
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please wait before sending another message.",
    "retry_after": 5
  }
}
```

**Service Unavailable**:
```json
{
  "error": {
    "code": "GEMINI_UNAVAILABLE",
    "message": "AI service temporarily unavailable",
    "suggestion": "Please try again in a few moments"
  }
}
```

---

## Rate Limiting

### Limits

| Tier | Requests/Minute | Tokens/Minute |
|------|-----------------|---------------|
| Gemini Free | 15 | 1,000,000 |
| Per-User Throttle | 10 | N/A |

### Rate Limit Response

**429 Too Many Requests**:
```json
{
  "detail": "Rate limit exceeded",
  "retry_after": 10
}
```

**Headers**:
```
Retry-After: 10
X-RateLimit-Limit: 15
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1677580810
```

---

## Testing

### Test Cases

**Happy Path**:
```bash
curl -X POST http://localhost:8000/api/testuser/chat \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}'
```

**New Conversation**:
```bash
curl -X POST http://localhost:8000/api/testuser/chat \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'
# Response includes new conversation_id
```

**Existing Conversation**:
```bash
curl -X POST http://localhost:8000/api/testuser/chat \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": 123, "message": "What are my pending tasks?"}'
```

**Error Case - Empty Message**:
```bash
curl -X POST http://localhost:8000/api/testuser/chat \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"message": ""}'
# Expected: 422 Validation Error
```

**Error Case - User Mismatch**:
```bash
curl -X POST http://localhost:8000/api/wronguser/chat \
  -H "Authorization: Bearer <token_for_testuser>" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
# Expected: 403 Forbidden
```

---

## Versioning

**Current Version**: v1 (implicit)

**Future Versions**:
- v2: `/api/v2/{user_id}/chat`
- Backward compatibility maintained
- Deprecation notices via headers

---

## Monitoring

### Metrics to Track

- Request count (total, by user, by tool)
- Response time (p50, p95, p99)
- Error rate (by error type)
- Tool invocation frequency
- Conversation count (new, active)
- Message count (user, assistant)

### Logging

**Request Log**:
```json
{
  "timestamp": "2026-02-28T10:00:00Z",
  "user_id": "testuser",
  "conversation_id": 123,
  "message_id": 456,
  "message": "Add a task to buy groceries",
  "tools_invoked": ["add_task"],
  "response_time_ms": 1250
}
```

**Error Log**:
```json
{
  "timestamp": "2026-02-28T10:05:00Z",
  "user_id": "testuser",
  "error_code": "TASK_NOT_FOUND",
  "tool": "complete_task",
  "task_id": 999,
  "stack_trace": "..."
}
```
