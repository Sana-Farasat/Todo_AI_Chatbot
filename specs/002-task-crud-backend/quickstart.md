# Quickstart Guide: Task CRUD Backend API

## Overview
This guide provides instructions for setting up and running the Task CRUD Backend API with JWT authentication and Neon Postgres.

## Prerequisites
- Python 3.11+
- UV package manager
- Neon Postgres database instance
- Better Auth configured in frontend

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd todo_web_app/backend
```

### 2. Install Dependencies
```bash
uv venv  # Create virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install fastapi sqlmodel asyncpg pydantic pyjwt alembic uvicorn python-multipart
```

### 3. Environment Configuration
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
BETTER_AUTH_SECRET=your-better-auth-secret
```

### 4. Database Setup
```bash
# Run migrations to create tables
alembic upgrade head
```

### 5. Run the Application
```bash
# Development mode
uvicorn main:app --reload --port 8000

# Or using the app directly
python main.py
```

## API Endpoints

### Authentication Required
All endpoints require a valid JWT in the Authorization header:
```
Authorization: Bearer <jwt-token>
```

### Available Endpoints

#### List Tasks
```
GET /api/{user_id}/tasks
Query params:
  - status: all|pending|completed (default: all)
  - sort: created|title (default: created)
```

#### Create Task
```
POST /api/{user_id}/tasks
Content-Type: application/json
Body: {
  "title": "Task title",
  "description": "Optional description"
}
```

#### Get Specific Task
```
GET /api/{user_id}/tasks/{task_id}
```

#### Update Task
```
PUT /api/{user_id}/tasks/{task_id}
Content-Type: application/json
Body: {
  "title": "Updated title",
  "description": "Updated description",
  "completed": false
}
```

#### Toggle Task Completion
```
PATCH /api/{user_id}/tasks/{task_id}/complete
Content-Type: application/json
Body: {
  "completed": true
}
```

#### Delete Task
```
DELETE /api/{user_id}/tasks/{task_id}
```

## Testing the API

### With curl
```bash
# Get user's tasks (replace USER_ID and JWT_TOKEN)
curl -H "Authorization: Bearer JWT_TOKEN" \
     http://localhost:8000/api/USER_ID/tasks

# Create a new task
curl -X POST \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer JWT_TOKEN" \
     -d '{"title": "New Task", "description": "Task description"}' \
     http://localhost:8000/api/USER_ID/tasks
```

### With Python requests
```python
import requests

headers = {
    "Authorization": f"Bearer {jwt_token}",
    "Content-Type": "application/json"
}

# Get tasks
response = requests.get(
    f"http://localhost:8000/api/{user_id}/tasks",
    headers=headers
)

# Create task
response = requests.post(
    f"http://localhost:8000/api/{user_id}/tasks",
    json={"title": "New Task", "description": "Description"},
    headers=headers
)
```

## Troubleshooting

### Common Issues

1. **JWT Validation Errors**
   - Ensure `BETTER_AUTH_SECRET` matches between frontend and backend
   - Verify JWT is properly formatted in Authorization header

2. **Database Connection Errors**
   - Check that `DATABASE_URL` is properly formatted
   - Ensure Neon Postgres instance is accessible
   - Verify SSL mode is set to 'require'

3. **User Isolation Failures**
   - Confirm that user_id in URL matches the 'sub' claim in JWT
   - Check that all endpoints validate the user identity

### Logs
Check application logs for detailed error information:
```bash
# View logs when running uvicorn
uvicorn main:app --reload --log-level info
```