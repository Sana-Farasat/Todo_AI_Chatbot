Skill: Better Auth JWT → FastAPI verification (Cross-service Auth)

Better Auth (Next.js) JWT payload:
{
  "sub": "user_id",
  "email": "...",
  "name": "...",
  "iat": ..., "exp": ...
}

FastAPI side (middleware/jwt.py):
- Secret: BETTER_AUTH_SECRET (same in both services)
- Header: Authorization: Bearer <jwt>
- Use PyJWT to decode & verify
- Extract user_id from "sub"
- Reject if user_id in URL != token.sub → 403
- Attach request.state.user_id

Never store session in backend. Always stateless JWT.

Common mistakes to avoid:
- Different secret keys
- Not checking user_id in path matches token
- Using session instead of JWT