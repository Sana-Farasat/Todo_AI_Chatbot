Skill: Phase 2 REST API Conventions (User-isolated)

Base path: /api/{user_id}/tasks

Endpoints:
GET    /api/{user_id}/tasks?status=all|pending|completed&sort=created|title
POST   /api/{user_id}/tasks
GET    /api/{user_id}/tasks/{task_id}
PUT    /api/{user_id}/tasks/{task_id}
PATCH  /api/{user_id}/tasks/{task_id}/complete
DELETE /api/{user_id}/tasks/{task_id}

Always:
- Validate user_id from path == JWT.sub
- Return only user's tasks
- Use Pydantic v2 models for request/response
- HTTPException(403, "Not authorized") if mismatch