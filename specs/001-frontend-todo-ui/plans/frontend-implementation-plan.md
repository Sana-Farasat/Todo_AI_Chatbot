# Frontend Implementation Plan: Next.js Todo App

## Overview
This document outlines the step-by-step implementation plan for the Phase 2 Frontend of the Todo Web Application using Next.js 15+ with App Router. The plan follows the feature specification and enforces the project constitution, focusing on creating a professional dark-themed UI with amber accents, responsive design, and smooth animations.

## Prerequisites
- Node.js 18+ installed
- Access to the backend API (FastAPI server running)
- Better Auth configured for authentication
- Neon Postgres database with user isolation

## Implementation Steps

### Step 1: Initialize Next.js Project and Install Dependencies
Set up the Next.js project with required dependencies for the UI components, authentication, animations, and styling.

**Suggested Qwen Code Sub-prompt**: "Initialize Next.js 15+ project in /frontend with TypeScript, install dependencies: shadcn/ui, framer-motion, better-auth, lucide-react, sonner, tailwindcss"

#### Dependencies to Install:
- next@latest
- react@latest
- react-dom@latest
- typescript
- @types/react
- @types/node
- @types/react-dom
- tailwindcss
- postcss
- autoprefixer
- shadcn/ui
- framer-motion
- better-auth
- lucide-react
- sonner

#### Shadcn/UI Setup:
- Initialize shadcn/ui with default configuration
- Install required components: Card, Input, Button, Checkbox, Badge, Dialog, Skeleton

### Step 2: Configure Tailwind CSS and Dark Mode
Set up Tailwind CSS with dark mode enabled and custom color configurations for the amber accent.

**Suggested Qwen Code Sub-prompt**: "Configure tailwind.config.ts with dark mode class strategy, amber-500 primary color, and custom CSS variables for :root and .dark classes"

#### Configuration Details:
- Enable dark mode using class strategy
- Define amber-500 as primary color
- Add custom CSS variables for dark/light themes in globals.css
- Set up color palette: black/gray-950 for backgrounds, white/gray-100 for text

### Step 3: Create API Client Library
Implement an authenticated fetch client that integrates with Better Auth for JWT handling.

**Suggested Qwen Code Sub-prompt**: "Create lib/api.ts with authenticated fetch function that retrieves JWT from Better Auth and adds Bearer header to API requests"

#### Implementation Details:
- Create `lib/api.ts` with authenticated fetch wrapper
- Function to get JWT token from Better Auth session
- Add Bearer token to authorization header
- Handle API errors and return appropriate responses
- Include retry mechanism for failed requests

### Step 4: Implement Authentication Pages
Create login and signup pages with Better Auth integration.

**Suggested Qwen Code Sub-prompt**: "Implement /login and /signup pages using Better Auth hooks with form validation and error handling"

#### Implementation Details:
- Create `/app/(auth)/login/page.tsx` and `/app/(auth)/signup/page.tsx`
- Use Better Auth `signIn` and `signUp` functions
- Implement form validation
- Add error handling and user feedback
- Redirect to dashboard after successful authentication

### Step 5: Create Protected Dashboard Page
Build the main dashboard page that fetches and displays user tasks.

**Suggested Qwen Code Sub-prompt**: "Create /dashboard page that fetches user tasks on mount, displays them in a list with TaskCard components, and handles loading/error states"

#### Implementation Details:
- Create `/app/dashboard/page.tsx`
- Fetch tasks using the authenticated API client
- Display loading skeleton while fetching
- Handle error states with appropriate messaging
- Redirect unauthenticated users to login
- Use layout animations for smooth transitions

### Step 6: Develop Task Components
Create reusable components for displaying and managing tasks.

**Suggested Qwen Code Sub-prompt**: "Implement TaskCard component that displays task title, description, completion status, and action buttons with proper styling"

#### Components to Create:
- `components/TaskCard.tsx` - Displays individual tasks with title, description, checkbox, and action buttons
- `components/TaskForm.tsx` - Modal or inline form for adding/updating tasks
- `components/Header.tsx` - Navigation header with logout button

### Step 7: Implement Animations with Framer Motion
Add smooth animations for task interactions as specified in the requirements.

**Suggested Qwen Code Sub-prompt**: "Add Framer Motion animations to task list: fadeIn for new tasks, fadeOut for deleted tasks, strikethrough for completed tasks, and layout animations for reordering"

#### Animation Details:
- New task: fadeIn + slide down (opacity 0→1, y -20→0, duration 0.4s)
- Delete task: fadeOut + scale 1→0.8 + y +20 (duration 0.3s)
- Mark complete: strikethrough line animation + text color transition to gray-500 (0.5s)
- List reorder: Use `<motion.ul>` with layout prop for smooth layout animations

### Step 8: Implement CRUD Operations
Connect the UI to the backend API for full task management functionality.

**Suggested Qwen Code Sub-prompt**: "Implement CRUD operations for tasks: add (POST), delete (DELETE with confirmation), update (PUT), toggle complete (PATCH) with proper error handling"

#### Operations to Implement:
- Add task: POST request to `/api/{userId}/tasks`
- Delete task: DELETE request with confirmation dialog
- Update task: PUT request to update task details
- Toggle complete: PATCH request to update completion status
- Error handling with toast notifications

### Step 9: Add Loading States and Error Handling
Implement proper loading indicators and error handling throughout the application.

**Suggested Qwen Code Sub-prompt**: "Add loading skeletons for task list, toast notifications for errors using shadcn/ui, and proper error boundaries"

#### Implementation Details:
- Loading skeletons for task list while fetching
- Toast notifications for API errors using sonner
- Error boundaries for catching unexpected errors
- Form validation and submission feedback
- Network error handling with retry options

### Step 10: Implement Responsive Design
Ensure the application works well on all device sizes with a mobile-first approach.

**Suggested Qwen Code Sub-prompt**: "Make the Todo app responsive with mobile-first design, centered container with max-width 3xl, and properly sized touch targets"

#### Responsive Features:
- Mobile-first layout with appropriate breakpoints
- Centered container with max-width 3xl
- Properly sized touch targets for mobile devices
- Responsive task cards and forms
- Adaptive navigation for different screen sizes

### Step 11: Add Logout Functionality
Implement secure logout with session cleanup.

**Suggested Qwen Code Sub-prompt**: "Add logout functionality to Header component using Better Auth signOut hook with redirect to login page"

#### Implementation Details:
- Use Better Auth `signOut` function
- Clear any local storage or session data
- Redirect to login page after logout
- Update UI to reflect logged-out state

### Step 12: Local Testing and Preparation for Deployment
Test the application locally and prepare for deployment to Vercel.

**Suggested Qwen Code Sub-prompt**: "Prepare for local testing with npm run dev and create vercel.json for Vercel deployment configuration"

#### Testing Steps:
- Run `npm run dev` to start the development server
- Test all functionality: authentication, task CRUD, animations, responsive design
- Verify API integration works correctly
- Check error handling and loading states
- Prepare vercel.json for deployment if needed

## Common Issues and Solutions

### Issue 1: Auth Token Not Sending
- **Problem**: API requests fail due to missing JWT token
- **Solution**: Verify the API client correctly retrieves the token from Better Auth session

### Issue 2: Dark Mode Not Applying
- **Problem**: Dark mode styles not appearing despite configuration
- **Solution**: Ensure Tailwind config uses class strategy and CSS includes dark mode variants

### Issue 3: Animation Flicker
- **Problem**: Task animations cause flickering or unexpected behavior
- **Solution**: Use layoutId if needed and ensure proper key props for animated components

## Timeline and Milestones

- **Days 1-2**: Project setup, dependencies installation, authentication pages
- **Day 3**: API client, dashboard page, and basic task display
- **Day 4**: Task components, animations, and CRUD operations
- **Day 5**: Responsive design, error handling, and testing
- **Day 6**: Final testing, bug fixes, and deployment preparation

## Commit Strategy
- Commit after each major step (e.g., "Step 1: Initialize Next.js project and install dependencies")
- Small, atomic commits for bug fixes and minor improvements
- Clear commit messages following conventional commits format

## Success Criteria
- All user stories from the spec are implemented and tested
- Application meets all functional requirements (FR-001 through FR-012)
- Responsive design works across all targeted screen sizes
- All animations perform smoothly
- Authentication flow works correctly
- API integration handles all CRUD operations properly
- Error handling provides clear feedback to users