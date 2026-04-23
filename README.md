# Wrote README.md
# Spec Kit Plus - AI-Powered Task Management System
A full-stack task management application built with Next.js, FastAPI, PostgreSQL, and AI integration (Gemini).
## Project Overview
This is a complete full-stack task management system where users can manage tasks in three ways:
1. **Manual** - Add tasks manually with custom fields
2. **Chatbot** - Use AI chatbot to add tasks conversationally  
3. **NLP** - Natural language processing to parse task details
### Hackathon Achievement: Rank 3rd Place 🎉
---
## Tech Stack
### Frontend
- **Next.js 16** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS 4** - Styling
- **Framer Motion** - Animations
- **Better Auth** - Authentication
- **Shadcn UI** - UI Components
- **Sonner** - Toast notifications
- **Jotai** - State management
### Backend
- **FastAPI** - Python web framework
- **SQLAlchemy + SQLModel** - ORM
- **PostgreSQL (Neon DB)** - Database
- **PyJWT** - JWT authentication
- **Google Gemini AI** - AI integration
- **Alembic** - Database migrations
### Database
- **Neon DB** - Serverless PostgreSQL
- **AsyncPG** - Async database driver
---
## Features
### Authentication
- Email/Password login and signup
- JWT token-based authentication
- Protected routes with session management
- Better Auth integration
### Task Management
- Create, Read, Update, Delete tasks
- Task fields: title, description, priority, due_date, category, completed
- Filter and organize tasks
- Mark tasks as complete/incomplete
### AI Chatbot
- Gemini-powered AI assistant
- Natural language task creation
- Smart task parsing (extracts dates, priorities automatically)
- Context-aware conversations
- MCP (Model Context Protocol) tools integration
### UI/UX
- Dark theme with amber accents
- Responsive design
- Smooth animations
- Loading states
- Error handling
---
## Project Structure
```
grok_todo - Copy/
├── frontend/                 # Next.js frontend
│   ├── app/                  # App router pages
│   │   ├── page.tsx         # Landing page
│   │   ├── sign-in/         # Login page
│   │   ├── sign-up/         # Signup page
│   │   ├── dashboard/       # Main dashboard
│   │   ├── chat/           # AI Chatbot page
│   │   ├── profile/        # User profile
│   │   └── settings/       # App settings
│   ├── components/          # React components
│   │   └── ui/             # Shadcn UI components
│   ├── lib/                # Utilities
│   │   ├── auth.ts        # Better Auth client
│   │   ├── api.ts         # API utilities
│   │   └── utils.ts       # Helper functions
│   └── package.json       # Frontend dependencies
│
├── backend/                 # FastAPI backend
│   ├── main.py             # FastAPI app entry
│   ├── db.py              # Database configuration
│   ├── models.py          # SQLModel models
│   ├── jwt_auth.py        # JWT authentication
│   ├── routes/
│   │   ├── tasks.py        # Task CRUD endpoints
│   │   └── chat.py        # AI Chatbot endpoints
│   ├── services/
│   │   ├── gemini_agent.py # Gemini AI service
│   │   └── mcp_tools.py   # MCP tools
│   ├── middleware/
│   │   └── jwt_auth.py    # JWT middleware
│   ├── alembic/           # Database migrations
│   ├── .env               # Environment variables
│   └── requirements.txt   # Python dependencies
│
├── specs/                  # Specification documents
│   └── 003-gemini-chatbot/
└���─ README.md             # This file
```
---
## Setup Instructions
### Prerequisites
1. **Node.js 18+** - [Download](https://nodejs.org)
2. **Python 3.11+** - [Download](https://python.org)
3. **Git** - [Download](https://git-scm.com)
4. **Neon DB Account** - [Sign up](https://neon.tech)
---
### Step 1: Clone the Repository
```bash
# Open terminal and clone
git clone https://github.com/YOUR_USERNAME/grok_todo.git
cd grok_todo
```
---
### Step 2: Frontend Setup
Navigate to the frontend directory:
```bash
cd frontend
```
Install dependencies:
```bash
npm install
```
Create environment file:
```bash
# Create .env.local with your settings
cp .env.example .env.local
```
Edit `.env.local` with your values:
```env
BETTER_AUTH_SECRET=your_secret_key_here
BETTER_AUTH_URL=http://localhost:3000
```
Start development server:
```bash
npm run dev
```
Frontend will be running at: **http://localhost:3000**
---
### Step 3: Backend Setup
Open a new terminal and navigate to backend:
```bash
cd backend
```
Create virtual environment:
```bash
# Create venv
python -m venv .venv
# Activate (Windows)
.venv\Scripts\activate.ps1
# Activate (Linux/Mac)
source .venv/bin/activate
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Or with uv:
```bash
uv sync
```
Create environment file:
```bash
cp .env.example .env
```
Edit `.env` with your values:
```env
DATABASE_URL=postgresql+asyncpg://user:pass@host/dbname?sslmode=require
BETTER_AUTH_SECRET=your_secret_key_here
GEMINI_API_KEY=your_gemini_api_key
```
Start the backend server:
```bash
# With uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Backend will be running at: **http://localhost:8000**
---
### Step 4: Database Setup (Neon DB)
1. Go to [Neon Dashboard](https://neon.tech)
2. Create a new project
3. Copy the connection string
4. Update `DATABASE_URL` in backend `.env`
The connection string format:
```
postgresql+asyncpg://username:password@host.neon.tech/dbname?sslmode=require
```
---
### Step 5: Run the Application
**Terminal 1 - Backend:**
```bash
cd backend
.venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
---
## API Endpoints
### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/signin` - Login user
- `GET /api/auth/jwks` - Get JSON Web Key Set
### Tasks
- `GET /api/tasks/{user_id}` - Get all tasks for user
- `POST /api/tasks/{user_id}` - Create new task
- `PUT /api/tasks/{user_id}/{task_id}` - Update task
- `PATCH /api/tasks/{user_id}/{task_id}/complete` - Mark task complete
- `DELETE /api/tasks/{user_id}/{task_id}` - Delete task
### Chat
- `POST /api/chat/message` - Send message to AI chatbot
---
## Environment Variables
### Frontend (.env.local)
```env
BETTER_AUTH_SECRET=your_32_char_secret_key
BETTER_AUTH_URL=http://localhost:3000
```
### Backend (.env)
```env
DATABASE_URL=postgresql+asyncpg://...
BETTER_AUTH_SECRET=your_32_char_secret_key
GEMINI_API_KEY=your_gemini_api_key
```
---
## How to Use
### 1. Landing Page
Open browser to `http://localhost:3000` - Shows landing page with Login/Sign Up buttons
### 2. Sign Up
Click "Sign Up" → Enter email/password → Create account
### 3. Dashboard
After login → View all tasks → Add new tasks → Mark complete
### 4. Chatbot
Click "Chat" → Type "Add task: Finish report by tomorrow" → AI parses and creates task
---
## Building Steps (How I Built This)
### Phase 1: Project Setup
1. Initialized Next.js 16 with TypeScript
2. Set up FastAPI backend
3. Configured Neon PostgreSQL database
### Phase 2: Authentication
1. Integrated Better Auth for frontend
2. Created JWT middleware for backend
3. Set up protected routes
### Phase 3: Task CRUD
1. Created `models.py` with SQLModel for Task
2. Built REST API endpoints in `routes/tasks.py`
3. Connected to frontend with API calls
### Phase 4: UI Development
1. Created landing page with Tailwind + Framer Motion
2. Built login/signup pages
3. Created dashboard with task list
4. Added dark theme with amber accents
### Phase 5: AI Chatbot
1. Set up Gemini API integration
2. Created MCP tools for task operations
3. Built chat endpoint in `routes/chat.py`
4. Created chat UI in frontend
---
## Deployment
### Frontend (Vercel)
```bash
cd frontend
npm run build
vercel --prod
```
### Backend (Railway/Render)
1. Push to GitHub
2. Connect to Railway/Render
3. Set environment variables
4. Deploy
---
## Acknowledgments
- **Next.js** - React framework
- **Neon** - Serverless PostgreSQL
- **Google Gemini** - AI capabilities
- **Better Auth** - Authentication
- **Shadcn** - UI components
---
## Contact
For questions or support, open an issue on GitHub.
---
**Built with ❤️ for Hackathon II**
