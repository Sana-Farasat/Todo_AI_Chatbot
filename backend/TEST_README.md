# Task CRUD API Tests

## Requirements

For these tests to pass, you need:

1. **Backend Server** running on `http://localhost:8000`
2. **Frontend Server** running on `http://localhost:3000` (for JWT token generation)
3. **Database** configured and accessible

## Starting the Servers

### Backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm run dev
```

## Running Tests

### Simple Tests (with mock tokens)
```bash
cd backend
python test_tasks_simple.py
```

Note: These tests will fail authentication because mock tokens can't be verified without the frontend's JWKS endpoint.

### Full Integration Tests (requires both servers)
```bash
cd backend
python test_tasks_crud.py
```

## Test Coverage

### CRUD Operations Tested:
1. **CREATE** - POST `/api/tasks/{user_id}`
2. **READ** - GET `/api/tasks/{user_id}`
3. **UPDATE** - PUT `/api/tasks/{user_id}/{task_id}`
4. **PATCH** - PATCH `/api/tasks/{user_id}/{task_id}/complete`
5. **DELETE** - DELETE `/api/tasks/{user_id}/{task_id}`

### Authentication Tests:
- Requests without tokens are rejected (401)
- Requests with invalid tokens are rejected (401)
- Users can only access their own tasks (403 for cross-user access)

## Common Issues

### 1. "Token verification failed" Error
**Cause**: Frontend server not running or JWKS endpoint unavailable

**Solution**: 
```bash
cd frontend
npm run dev
```

### 2. "DATABASE_URL not found" Error
**Cause**: Database connection string missing in `.env`

**Solution**: Create `.env` file in backend directory:
```
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database
BETTER_AUTH_JWKS_URL=http://localhost:3000/api/auth/jwks
```

### 3. "404 Not Found" for routes
**Cause**: Incorrect route paths

**Solution**: Use these exact paths:
- `/api/tasks/{user_id}` (NOT `/api/{user_id}/tasks`)
- No trailing slashes

## API Endpoints Reference

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/tasks/{user_id}` | Get all tasks for user | Yes (Bearer Token) |
| POST | `/api/tasks/{user_id}` | Create new task | Yes (Bearer Token) |
| PUT | `/api/tasks/{user_id}/{task_id}` | Update task | Yes (Bearer Token) |
| PATCH | `/api/tasks/{user_id}/{task_id}/complete` | Toggle task completion | Yes (Bearer Token) |
| DELETE | `/api/tasks/{user_id}/{task_id}` | Delete task | Yes (Bearer Token) |

## Request/Response Examples

### Create Task
**Request:**
```http
POST /api/tasks/user-123
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "My Task",
  "description": "Task description"
}
```

**Response (201):**
```json
{
  "id": 1,
  "user_id": "user-123",
  "title": "My Task",
  "description": "Task description",
  "completed": false,
  "created_at": "2026-03-07T10:00:00Z",
  "updated_at": "2026-03-07T10:00:00Z"
}
```

### Get All Tasks
**Request:**
```http
GET /api/tasks/user-123
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "user_id": "user-123",
    "title": "My Task",
    "description": "Task description",
    "completed": false,
    "created_at": "2026-03-07T10:00:00Z",
    "updated_at": "2026-03-07T10:00:00Z"
  }
]
```

### Update Task
**Request:**
```http
PUT /api/tasks/user-123/1
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "Updated Task",
  "description": "Updated description"
}
```

**Response (200):**
```json
{
  "message": "Task updated"
}
```

### Toggle Complete
**Request:**
```http
PATCH /api/tasks/user-123/1/complete
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "completed": true
}
```

**Response (200):**
```json
{
  "message": "Task status updated"
}
```

### Delete Task
**Request:**
```http
DELETE /api/tasks/user-123/1
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "message": "Task deleted"
}
```
