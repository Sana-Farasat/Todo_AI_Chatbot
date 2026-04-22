---
id: "001"
title: "Frontend Implementation Plan"
stage: "plan"
date_iso: "2026-02-06"
surface: "agent"
model: "Qwen Code"
feature: "frontend-todo-ui"
branch: "001-frontend-todo-ui"
user: "user"
command: "/sp.plan Generate a step-by-step Markdown plan file for implementing Phase 2 Frontend (Next.js) using the generated spec (specs/frontend/todo-ui-spec.md). Enforce @memory/constitution.md and reference skills: @skills/nextjs-app-router-phase2.skill.md, @skills/better-auth-jwt-fastapi.skill.md."
labels:
  - "frontend"
  - "nextjs"
  - "planning"
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml:
  - "plans/frontend-implementation-plan.md"
  - "plans/frontend-implementation-checklist.md"
tests_yaml: []
---

# Frontend Implementation Plan

## Prompt

```
/sp.plan Generate a step-by-step Markdown plan file for implementing Phase 2 Frontend (Next.js) using the generated spec (specs/frontend/todo-ui-spec.md). Enforce @memory/constitution.md and reference skills: @skills/nextjs-app-router-phase2.skill.md, @skills/better-auth-jwt-fastapi.skill.md.

Plan must include:
- Step 1: Install deps (shadcn/ui init if not, framer-motion, better-auth hooks, lucide-react icons, sonner for toasts).
- Step 2: Setup theme (tailwind.config.ts mein dark mode class, amber-500 primary, custom CSS vars for :root & .dark).
- Step 3: Create lib/api.ts (authenticated fetch with JWT from Better Auth).
- Step 4: Implement auth pages (/signup, /login) with Better Auth signUp/signIn calls.
- Step 5: Dashboard page (/dashboard): fetch tasks on mount, display list with TaskCard.
- Step 6: TaskForm component for add/update (modal or inline, Framer Motion animate presence).
- Step 7: Add animations: wrap list in <motion.div layout>, each task in <motion.li initial/animate/exit>, checkbox onChange with transition.
- Step 8: Implement CRUD actions: add (POST), delete (DELETE with confirm), update (PUT), toggle complete (PATCH).
- Step 9: Loading/error states, responsive design, logout button.
- Step 10: Local testing (npm run dev), Vercel deploy prep (vercel.json if needed).
- Common issues: auth token not sending, dark mode not applying, animation flicker (use layoutId if needed).
- Timeline: Aim for 6-8 hours, commit per major step.

Output as plans/frontend-implementation-plan.md in Markdown with numbered steps, each with suggested Qwen Code sub-prompt for generation (e.g. "Implement TaskCard component using @specs/frontend/todo-ui-spec.md").
```

## Response

[Response content would go here, but it's captured in the generated plan file]

## Outcome

Successfully generated a comprehensive implementation plan for the Phase 2 Frontend (Next.js) of the Todo App. The plan includes all required steps with detailed code examples and suggested Qwen Code sub-prompts for each component. A checklist was also created to ensure all requirements are met during implementation.