---
id: "001"
title: "frontend-todo-ui"
stage: "spec"
date_iso: "2026-02-06"
surface: "agent"
model: "Qwen"
feature: "frontend-todo-ui"
branch: "001-frontend-todo-ui"
user: "user"
command: "/sp.specify"
labels: ["frontend", "ui", "todo-app", "specification"]
spec: null
ticket: null
adr: null
pr: null
files_yaml:
  - "specs/001-frontend-todo-ui/spec.md"
  - "specs/001-frontend-todo-ui/checklists/requirements.md"
tests_yaml: []
prompt_text: |
  Generate a detailed Markdown spec file for Phase 2 Frontend (Next.js 15+ App Router) of Todo App. Follow @memory/constitution.md strictly. Reference these skills: @skills/monorepo-speckit-fullstack.skill.md, @skills/nextjs-app-router-phase2.skill.md, @skills/better-auth-jwt-fastapi.skill.md. UI/Theme Requirements: - Professional dark theme: background black/gray-950, text white/gray-100, accents amber-500 (#f59e0b) for buttons, hover states, completed tasks (amber-400 for lighter highlights). - Use shadcn/ui components: Card for tasks, Input for forms, Button (variant=outline or default with amber bg), Checkbox, Badge if needed. - Responsive, mobile-first layout: centered container, max-w-3xl, grid or flex for task list. - Animations with Framer Motion: - New task: fadeIn + slide down from top (opacity 0→1, y -20→0, duration 0.4s) - Delete task: fadeOut + scale 1→0.8 + y +20 (duration 0.3s) - Mark complete: strikethrough line animation + text color gray-500 (transition 0.5s) - List reorder/layout animation on add/delete (use <motion.ul> with layout prop) - Pages: / (redirect to /login if not auth), /login, /signup, /dashboard (main todo list) - Components: TaskCard (with title, desc, checkbox, edit/delete buttons), TaskForm (add/update modal or inline), Header with logout. - Auth: Use Better Auth hooks (useSession, signOut), redirect unauth users. - API Integration: lib/api.ts with authenticated fetch (getToken from Better Auth, add Bearer header), endpoints /api/{userId}/tasks... - Error handling: toast notifications (shadcn toast), loading skeletons. - Constraints: No manual code – refine spec until Qwen generates correct output. Use Tailwind dark mode class strategy. Output as specs/frontend/todo-ui-spec.md in Markdown with sections: Overview, Theme & Colors, Folder Structure, Pages & Routing, Components, Animations, Auth Flow, API Client, Best Practices.
response_text: |
  Created a comprehensive feature specification for the Phase 2 Frontend of the Todo App with detailed sections covering Overview, Theme & Colors, Folder Structure, Pages & Routing, Components, Animations, Auth Flow, API Client, and Best Practices. The specification includes user scenarios, functional requirements, and success criteria as required by the template.
outcome: "SUCCESS"
evaluation: "Specification successfully created with all required sections and validated against quality criteria"
---

# Feature Specification: Phase 2 Frontend (Next.js 15+ App Router) of Todo App

**Feature Branch**: `001-frontend-todo-ui`
**Created**: 2026-02-06
**Status**: Draft
**Input**: User description: "Generate a detailed Markdown spec file for Phase 2 Frontend (Next.js 15+ App Router) of Todo App. Follow @memory/constitution.md strictly. Reference these skills: @skills/monorepo-speckit-fullstack.skill.md, @skills/nextjs-app-router-phase2.skill.md, @skills/better-auth-jwt-fastapi.skill.md. UI/Theme Requirements: - Professional dark theme: background black/gray-950, text white/gray-100, accents amber-500 (#f59e0b) for buttons, hover states, completed tasks (amber-400 for lighter highlights). - Use shadcn/ui components: Card for tasks, Input for forms, Button (variant=outline or default with amber bg), Checkbox, Badge if needed. - Responsive, mobile-first layout: centered container, max-w-3xl, grid or flex for task list. - Animations with Framer Motion: - New task: fadeIn + slide down from top (opacity 0→1, y -20→0, duration 0.4s) - Delete task: fadeOut + scale 1→0.8 + y +20 (duration 0.3s) - Mark complete: strikethrough line animation + text color gray-500 (transition 0.5s) - List reorder/layout animation on add/delete (use <motion.ul> with layout prop) - Pages: / (redirect to /login if not auth), /login, /signup, /dashboard (main todo list) - Components: TaskCard (with title, desc, checkbox, edit/delete buttons), TaskForm (add/update modal or inline), Header with logout. - Auth: Use Better Auth hooks (useSession, signOut), redirect unauth users. - API Integration: lib/api.ts with authenticated fetch (getToken from Better Auth, add Bearer header), endpoints /api/{userId}/tasks... - Error handling: toast notifications (shadcn toast), loading skeletons. - Constraints: No manual code – refine spec until Qwen generates correct output. Use Tailwind dark mode class strategy. Output as specs/frontend/todo-ui-spec.md in Markdown with sections: Overview, Theme & Colors, Folder Structure, Pages & Routing, Components, Animations, Auth Flow, API Client, Best Practices."

## Overview

The Phase 2 Frontend of the Todo App is a comprehensive user interface built with Next.js 15+ App Router, featuring a professional dark-themed UI with amber accent colors. The application will provide a responsive, mobile-first experience with smooth animations for task interactions. The frontend will integrate with a backend API for data persistence and implement secure authentication using Better Auth.

## Theme & Colors

- **Primary Background**: black/gray-950
- **Text Color**: white/gray-100
- **Accent Color**: amber-500 (#f59e0b) for buttons, hover states, and completed tasks
- **Secondary Accent**: amber-400 for lighter highlights
- **Completed Task Color**: gray-500 with strikethrough effect
- **Responsive Layout**: Centered container with max-width of 3xl, using grid or flexbox for task list

## Folder Structure

```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── signup/
│   │       └── page.tsx
│   ├── dashboard/
│   │   └── page.tsx
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx (redirects to login if not authenticated)
├── components/
│   ├── ui/ (shadcn/ui components)
│   ├── TaskCard.tsx
│   ├── TaskForm.tsx
│   └── Header.tsx
├── lib/
│   ├── api.ts
│   └── utils.ts
├── hooks/
│   └── useAuth.ts
└── public/
```

## Pages & Routing

- **/**: Landing page that redirects to /login if user is not authenticated
- **/login**: Authentication page with form for existing users
- **/signup**: Registration page with form for new users
- **/dashboard**: Main todo list page showing user's tasks with add/edit/delete functionality

## Components

- **TaskCard**: Displays individual tasks with title, description, checkbox, and edit/delete buttons
- **TaskForm**: Modal or inline form for adding/updating tasks
- **Header**: Navigation bar with logout button
- **UI Components**: Using shadcn/ui library for Cards, Inputs, Buttons (with amber background), Checkboxes, and Badges

## Animations

- **New Task**: FadeIn + slide down from top (opacity 0→1, y -20→0, duration 0.4s)
- **Delete Task**: FadeOut + scale 1→0.8 + y +20 (duration 0.3s)
- **Mark Complete**: Strikethrough line animation + text color transition to gray-500 (transition 0.5s)
- **List Reorder/Layout**: Smooth layout animations on add/delete using motion.ul with layout prop

## Auth Flow

- **Authentication**: Using Better Auth with hooks (useSession, signOut)
- **Protected Routes**: Unauthenticated users redirected to login page
- **Session Management**: Secure token handling with automatic refresh

## API Client

- **Location**: lib/api.ts
- **Authenticated Fetch**: Using getToken from Better Auth to add Bearer header
- **Endpoints**: /api/{userId}/tasks for CRUD operations
- **Error Handling**: Proper error responses and user notifications

## Best Practices

- **Responsive Design**: Mobile-first approach with centered container and max-width 3xl
- **Accessibility**: Proper semantic HTML and ARIA attributes
- **Performance**: Loading skeletons for better perceived performance
- **Error Handling**: Toast notifications for user feedback
- **Code Organization**: Component-based architecture with reusable UI elements

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Authentication (Priority: P1)

A user visits the application and needs to log in or sign up to access their todo list. The user can securely authenticate using the login/signup forms and gain access to their personalized dashboard.

**Why this priority**: Authentication is the foundation for all other functionality - users must be authenticated to access their personal tasks.

**Independent Test**: Can be fully tested by navigating to the login page, entering credentials, and verifying access to the dashboard with proper session management.

**Acceptance Scenarios**:

1. **Given** user is not logged in, **When** user navigates to homepage, **Then** user is redirected to login page
2. **Given** user is on login page, **When** user enters valid credentials and submits, **Then** user is redirected to dashboard with active session
3. **Given** user is on signup page, **When** user enters valid registration details and submits, **Then** user account is created and user is logged in

---

### User Story 2 - View and Manage Tasks (Priority: P1)

An authenticated user can view their task list on the dashboard, mark tasks as complete/incomplete, and see visual feedback for task status changes with smooth animations.

**Why this priority**: This is the core functionality of a todo app - users need to see and interact with their tasks.

**Independent Test**: Can be fully tested by logging in, viewing the task list, toggling task completion status, and observing the visual feedback and animations.

**Acceptance Scenarios**:

1. **Given** user is on dashboard with tasks, **When** user clicks checkbox on a task, **Then** task gets strikethrough effect with smooth animation and status updates in the backend
2. **Given** user has completed tasks, **When** viewing the task list, **Then** completed tasks appear with gray-500 text color and strikethrough
3. **Given** user has incomplete tasks, **When** viewing the task list, **Then** incomplete tasks appear with normal text color

---

### User Story 3 - Add and Delete Tasks (Priority: P2)

An authenticated user can add new tasks to their list and delete existing tasks with appropriate animations and confirmation.

**Why this priority**: Adding and removing tasks are essential CRUD operations that enable users to manage their todo list effectively.

**Independent Test**: Can be fully tested by logging in, adding new tasks through the form, and deleting existing tasks while observing the animations and data persistence.

**Acceptance Scenarios**:

1. **Given** user is on dashboard, **When** user adds a new task via TaskForm, **Then** task appears in the list with fadeIn + slide down animation and is persisted in the backend
2. **Given** user has tasks on dashboard, **When** user deletes a task, **Then** task fades out with scale and position animation before being removed from the list and backend
3. **Given** user is adding a task, **When** submission fails due to validation or network error, **Then** appropriate error message is displayed via toast notification

---

### User Story 4 - Responsive Experience (Priority: P2)

Users can access and use the todo application seamlessly across different device sizes, with the UI adapting appropriately to mobile, tablet, and desktop screens.

**Why this priority**: Modern web applications must provide a consistent experience across all devices to serve users effectively.

**Independent Test**: Can be fully tested by accessing the application on different screen sizes and verifying that the layout, components, and interactions work properly.

**Acceptance Scenarios**:

1. **Given** user accesses app on mobile device, **When** viewing the dashboard, **Then** the layout adapts to mobile with appropriate touch targets and spacing
2. **Given** user accesses app on desktop, **When** viewing the dashboard, **Then** the centered container with max-width 3xl is displayed appropriately
3. **Given** user resizes browser window, **When** crossing responsive breakpoints, **Then** the UI adjusts smoothly without layout issues

---

### Edge Cases

- What happens when the user loses internet connection while interacting with tasks?
- How does the system handle multiple simultaneous updates to the same task from different devices?
- What occurs when a user attempts to add a task with empty content?
- How does the application behave when the user's authentication token expires during a session?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST implement a professional dark theme with specified color palette (background black/gray-950, text white/gray-100, accents amber-500)
- **FR-002**: System MUST use shadcn/ui components for consistent UI elements (Card, Input, Button, Checkbox, Badge)
- **FR-003**: Users MUST be able to add new tasks with title and description via TaskForm component
- **FR-004**: Users MUST be able to mark tasks as complete/incomplete with visual feedback and animations
- **FR-005**: Users MUST be able to delete tasks with appropriate confirmation and animations
- **FR-006**: System MUST redirect unauthenticated users from homepage to login page
- **FR-007**: System MUST implement secure authentication using Better Auth with proper session management
- **FR-008**: System MUST provide responsive, mobile-first layout with centered container and max-width 3xl
- **FR-009**: System MUST implement specified animations for task interactions (fadeIn, fadeOut, strikethrough, layout)
- **FR-010**: System MUST handle API errors gracefully with toast notifications
- **FR-011**: System MUST display loading skeletons during data fetching operations
- **FR-012**: System MUST persist task data through API integration with proper authentication headers

### Key Entities

- **User**: Represents an authenticated user with unique ID, session information, and personal task list
- **Task**: Represents a todo item with properties like title, description, completion status, creation date, and association with a user

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully authenticate (login/signup) and access their dashboard within 30 seconds
- **SC-002**: Task operations (add, complete, delete) complete within 2 seconds including animations and API calls
- **SC-003**: Application achieves 95% uptime during peak usage hours
- **SC-004**: 90% of users can successfully add, complete, and delete tasks without assistance
- **SC-005**: Page load times remain under 3 seconds on 3G connections
- **SC-006**: All UI components are responsive and usable on screen sizes from 320px to 1920px width
- **SC-007**: All animations perform smoothly at 60fps on mid-range devices
- **SC-008**: Error rate for API operations remains below 1%