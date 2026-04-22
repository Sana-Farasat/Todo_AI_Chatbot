# Project Constitution – Hackathon II Phase 2: Full-Stack Todo Web Application

## Core Purpose & Scope
This project is Phase 2 of "The Evolution of Todo" in Hackathon II: Spec-Driven Development & Cloud-Native AI.
- Transform the Phase I in-memory Python console Todo app into a secure, multi-user full-stack web application.
- Strictly implement **Basic Level** features only in this phase (as per hackathon doc): 
  1. Add Task (title + description)
  2. Delete Task
  3. Update Task
  4. View Task List
  5. Mark as Complete (toggle status)
- No intermediate/advanced features (priorities, search, recurring, due dates) until later phases.
- Multi-user support: Each user has isolated tasks (no shared/global list).
- Use Spec-Driven Development: Refine specs until Qwen Code generates 100% correct code. No manual coding.

## Immutable Technology Stack (Opinionated & Fixed for Phase 2)
- Monorepo structure:
  - /frontend → Next.js 15+ (App Router, Server Components default, React 18+)
  - /backend → FastAPI (Python 3.11+)
  - Database: Neon Serverless Postgres (SQLModel + asyncpg)
- Authentication: Better Auth (JWT-based, stateless) on frontend → Verify JWT in FastAPI middleware.
- API: RESTful, user-isolated endpoints: /api/{user_id}/tasks/...
- Styling: Tailwind CSS + shadcn/ui components (mobile-first, responsive).
- Environment: Use .env files, DATABASE_URL from Neon, BETTER_AUTH_SECRET shared.
- No Docker/K8s in Phase 2 (that's Phase IV+).

## Security & Authorization Rules (Non-Negotiable)
- Every API endpoint MUST validate:
  - Authorization: Bearer <JWT> header present.
  - JWT decoded → "sub" (user_id) MUST match {user_id} in URL path → else 403 Forbidden.
- Backend NEVER trusts frontend user_id without token validation.
- Use PyJWT for verification in backend.
- Tasks ALWAYS filtered by user_id = JWT.sub.
- No global tasks, no admin bypass in this phase.

## Code Quality & Best Practices (Always Enforce)
- Python (backend):
  - Use type hints everywhere (SQLModel, Pydantic v2).
  - Async endpoints & sessions.
  - Alembic for migrations.
  - Clean architecture: routes/, models/, db.py, middleware/.
- Next.js (frontend):
  - App Router only (no pages/).
  - Server Actions for mutations where possible.
  - lib/api.ts for authenticated fetch with JWT.
  - Error handling + loading states.
- General:
  - Follow PEP8 + ESLint/Prettier defaults.
  - Commit per feature/task (small, atomic commits).
  - No console.logs in production code.
  - README.md + setup instructions always updated.

## Spec-Driven Workflow Rules (Qwen Code Specific)
- Always reference:
  - @specs/... for current feature.
  - @skills/... for reusable patterns (e.g. better-auth-jwt-fastapi.skill.md, fastapi-sqlmodel-neon.skill.md).
- Refine spec iteratively until output is correct (no manual fixes).
- Generate code only via Qwen Code prompts.
- Use AGENT.md in root for Qwen-specific instructions.
- Keep context low: Skills load progressively only when @-referenced.

## Non-Negotiable Constraints
- No Claude Code, Claude mentions, or Claude-specific files (CLAUDE.md banned – use AGENT.md).
- No Phase III+ features (no AI chatbot, no OpenAI SDK, no voice).
- Deployment: Local only (npm run dev + uvicorn) – Vercel link for frontend in submission.
- Bonus intent: Design for future reusable skills/blueprints, but implement only Phase 2 now.

## Amendment Process
- Constitution is immutable except for critical bug fixes or hackathon clarifications.
- Any change MUST be documented with date + reason in this file's history.
- Last updated: February 2026 (for current hackathon timeline).

This constitution governs ALL specifications, plans, tasks, and code generations in Phase 2.
Qwen Code MUST comply fully – no exceptions.