# API Contract: Task CRUD Operations

## Base Path
`/api/{user_id}/tasks`

## Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

The user_id in the URL path must match the 'sub' claim in the JWT token, otherwise a 403 Forbidden response will be returned.

## Endpoints

### GET /api/{user_id}/tasks
Retrieve a list of tasks for the specified user.

#### Query Parameters
- `status` (optional): Filter by completion status. Values: `all`, `pending`, `completed`. Default: `all`
- `sort` (optional): Sort order. Values: `created`, `title`. Default: `created`

#### Response
- Status: 200 OK
- Body:
```json
[
  {
    "id": 1,
    "user_id": "user-uuid-string",
    "title": "Task title",
    "description": "Optional task description",
    "completed": false,
    "created_at": "2023-01-01T10:00:00Z",
    "updated_at": "2023-01-01T10:00:00Z"
  }
]
```

#### Error Responses
- 403: Unauthorized access (user_id mismatch)
- 500: Internal server error

---

### POST /api/{user_id}/tasks
Create a new task for the specified user.

#### Request Body
```json
{
  "title": "Task title",
  "description": "Optional task description"
}
```

#### Response
- Status: 201 Created
- Body:
```json
{
  "id": 1,
  "user_id": "user-uuid-string",
  "title": "Task title",
  "description": "Optional task description",
  "completed": false,
  "created_at": "2023-01-01T10:00:00Z",
  "updated_at": "2023-01-01T10:00:00Z"
}
```

#### Validation
- Title is required and must be 1-200 characters
- Description, if provided, can be any length

#### Error Responses
- 400: Bad request (validation error)
- 403: Unauthorized access (user_id mismatch)
- 500: Internal server error

---

### GET /api/{user_id}/tasks/{task_id}
Retrieve a specific task by ID.

#### Response
- Status: 200 OK
- Body:
```json
{
  "id": 1,
  "user_id": "user-uuid-string",
  "title": "Task title",
  "description": "Optional task description",
  "completed": false,
  "created_at": "2023-01-01T10:00:00Z",
  "updated_at": "2023-01-01T10:00:00Z"
}
```

#### Error Responses
- 403: Unauthorized access (user_id mismatch)
- 404: Task not found
- 500: Internal server error

---

### PUT /api/{user_id}/tasks/{task_id}
Update an existing task.

#### Request Body
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true
}
```

#### Response
- Status: 200 OK
- Body:
```json
{
  "id": 1,
  "user_id": "user-uuid-string",
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true,
  "created_at": "2023-01-01T10:00:00Z",
  "updated_at": "2023-01-02T15:30:00Z"
}
```

#### Validation
- Title is required and must be 1-200 characters
- Description, if provided, can be any length

#### Error Responses
- 400: Bad request (validation error)
- 403: Unauthorized access (user_id mismatch)
- 404: Task not found
- 500: Internal server error

---

### PATCH /api/{user_id}/tasks/{task_id}/complete
Toggle the completion status of a task.

#### Request Body
```json
{
  "completed": true
}
```

#### Response
- Status: 200 OK
- Body:
```json
{
  "id": 1,
  "user_id": "user-uuid-string",
  "title": "Task title",
  "description": "Optional task description",
  "completed": true,
  "created_at": "2023-01-01T10:00:00Z",
  "updated_at": "2023-01-02T15:30:00Z"
}
```

#### Error Responses
- 400: Bad request (invalid completed value)
- 403: Unauthorized access (user_id mismatch)
- 404: Task not found
- 500: Internal server error

---

### DELETE /api/{user_id}/tasks/{task_id}
Delete a specific task.

#### Response
- Status: 204 No Content

#### Error Responses
- 403: Unauthorized access (user_id mismatch)
- 404: Task not found
- 500: Internal server error

## Common Error Responses

### 403 Forbidden
Returned when the user_id in the URL doesn't match the user_id in the JWT token.

Body:
```json
{
  "detail": "Not authorized to access this resource"
}
```

### 404 Not Found
Returned when the requested task doesn't exist.

Body:
```json
{
  "detail": "Task not found"
}
```

### 400 Bad Request
Returned when request validation fails.

Body:
```json
{
  "detail": "Validation error details"
}
```

### 500 Internal Server Error
Returned when an unexpected error occurs.

Body:
```json
{
  "detail": "Internal server error"
}
```