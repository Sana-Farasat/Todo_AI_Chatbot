Skill: Monorepo + SpecKit Structure for Next.js 16 + FastAPI (Phase 2)

Project root:
hackathon-todo/
├── .spec-kit/config.yaml
├── specs/
│   ├── overview.md
│   ├── features/task-crud.md
│   ├── api/rest-endpoints.md
│   ├── database/schema.md
│   └── ui/
├── skills/                          ← yahan ye skill files
├── frontend/ (Next.js 16 App Router)
│   ├── app/
│   ├── components/
│   ├── lib/api.ts                   ← authenticated API client
│   └── CLAUDE.md → rename to AGENT.md
├── backend/ (FastAPI)
│   ├── main.py
│   ├── models.py
│   ├── routes/tasks.py
│   ├── db.py
│   ├── middleware/jwt.py
│   └── AGENT.md
├── docker-compose.yml
└── README.md

Referencing rule for Qwen Code:
@specs/features/task-crud.md
@skills/monorepo-speckit-fullstack.skill.md
@skills/better-auth-jwt.skill.md