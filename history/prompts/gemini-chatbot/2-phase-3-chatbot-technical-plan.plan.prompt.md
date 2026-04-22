---
id: 2
title: "Phase 3 Chatbot Technical Plan"
stage: plan
date_iso: "2026-02-28"
surface: agent
model: qwen-coder
feature: gemini-chatbot
branch: 002-gemini-chatbot
user: user
command: "/sp.plan Create technical architecture plan for AI Todo Chatbot with Gemini API, MCP tools, custom chat UI with floating action button"
labels: ["plan", "ai-chatbot", "gemini", "phase-3", "architecture"]
links:
  spec: specs/002-gemini-chatbot/spec.md
  plan: specs/002-gemini-chatbot/plan.md
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - specs/002-gemini-chatbot/plan.md
  - specs/002-gemini-chatbot/research.md
  - specs/002-gemini-chatbot/data-model.md
  - specs/002-gemini-chatbot/quickstart.md
  - specs/002-gemini-chatbot/contracts/chat-api-contract.md
  - specs/002-gemini-chatbot/checklists/plan-quality.md
tests_yaml: |
  - Plan quality validation (all items passed)
  - Constitution check passed (5 gates)
prompt_text: |
  User requested technical planning phase for Phase 3 AI Todo Chatbot.
  
  Key requirements from spec:
  - Gemini Free API integration (not OpenAI)
  - Custom Next.js chat UI with beautiful floating action button (FAB) in bottom-right
  - MCP-style tools for task CRUD (5 tools: add, list, complete, delete, update)
  - Conversation persistence in Neon PostgreSQL
  - Stateless FastAPI backend architecture
  - Better Auth JWT authentication
  
  Technical decisions:
  - google-generativeai SDK for Gemini
  - Custom agent implementation (no LangChain overhead)
  - Shadcn + Framer Motion for chat UI animations
  - MCP tools pattern without official MCP SDK
  - 20-message conversation history limit

response_text: |
  Created complete technical architecture plan for AI Todo Chatbot.
  
  Key deliverables:
  - Branch: 002-gemini-chatbot
  - Plan file: specs/002-gemini-chatbot/plan.md
  - Research: specs/002-gemini-chatbot/research.md (technology evaluation)
  - Data model: specs/002-gemini-chatbot/data-model.md (schema + migration)
  - API contract: specs/002-gemini-chatbot/contracts/chat-api-contract.md
  - Quickstart: specs/002-gemini-chatbot/quickstart.md (setup guide)
  - Quality checklist: specs/002-gemini-chatbot/checklists/plan-quality.md (all passed)
  
  Architecture highlights:
  - POST /api/{user_id}/chat endpoint (stateless)
  - 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
  - Conversation + Message database models
  - Gemini 1.5 Flash model (fast, free tier)
  - FAB icon with purple gradient and pulse animation
  - Chat window: 380px width, slide-in animation
  
  Performance targets:
  - Response time < 3s (p95)
  - 100 concurrent chat sessions
  - Tool accuracy > 90%
  
  Plan ready for /sp.tasks command.
outcome: |
  Technical plan successfully created and validated. All quality checks passed.
evaluation: |
  Plan quality: 100% pass rate on validation checklist
  - Technology stack verified (Gemini Free API feasible)
  - Architecture sound (stateless, scalable)
  - Database schema complete (indexes, relationships)
  - API contract RESTful and consistent
  - Frontend design detailed (FAB + chat components)
  - Risk mitigation strategies defined
  - No blockers identified
