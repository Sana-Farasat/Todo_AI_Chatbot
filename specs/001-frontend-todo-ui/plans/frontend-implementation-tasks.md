# Frontend Implementation Tasks

## Overview
This document breaks down the frontend implementation plan into specific, actionable tasks for the Phase 2 Todo App using Next.js 15+ with App Router.

## Task List

### Task 1: Initialize Next.js Project and Install Dependencies
**Objective**: Set up the Next.js project structure and install all required dependencies.
**Steps**:
- Initialize Next.js 15+ project with App Router in frontend/ directory
- Install dependencies: next, react, react-dom, typescript, @types/react, @types/node, @types/react-dom, tailwindcss, postcss, autoprefixer
- Install additional dependencies: shadcn-ui, better-auth, @better-auth/react, framer-motion, lucide-react, sonner
**Estimated Time**: 30 minutes
**Priority**: High

### Task 2: Configure Tailwind CSS and Dark Mode
**Objective**: Set up Tailwind CSS with dark mode enabled and configure the required color scheme.
**Steps**:
- Configure Tailwind CSS for dark mode with class strategy
- Set amber-500 as primary color
- Add custom CSS variables for :root & .dark in tailwind.config.ts and globals.css
**Estimated Time**: 45 minutes
**Priority**: High

### Task 3: Initialize shadcn/ui
**Objective**: Set up shadcn/ui components for the project.
**Steps**:
- Initialize shadcn/ui in the Next.js project with default configuration
- Install required components: Card, Input, Button, Checkbox, Badge, Dialog, Sheet, Skeleton
**Estimated Time**: 30 minutes
**Priority**: High

### Task 4: Create API Client Library
**Objective**: Create the authenticated API client for interacting with the backend.
**Steps**:
- Create lib/api.ts with authenticated fetch function
- Use Better Auth getToken to add Bearer header
- Handle errors appropriately
- Implement endpoints for /api/{userId}/tasks (CRUD operations)
**Estimated Time**: 1 hour
**Priority**: High

### Task 5: Set Up Better Auth Provider
**Objective**: Configure Better Auth for the Next.js application.
**Steps**:
- Create auth-provider wrapper component
- Configure Better Auth in Next.js App Router with proper session handling
- Update root layout to include the auth provider
**Estimated Time**: 45 minutes
**Priority**: High

### Task 6: Create Authentication Pages
**Objective**: Implement login and signup pages with Better Auth integration.
**Steps**:
- Create login page component at app/(auth)/login/page.tsx
- Implement Better Auth signIn functionality
- Add form validation and error handling
- Create signup page component at app/(auth)/signup/page.tsx
- Implement Better Auth signUp functionality
- Add form validation and error handling
**Estimated Time**: 1.5 hours
**Priority**: High

### Task 7: Create Protected Route Handler
**Objective**: Implement a utility to protect routes that require authentication.
**Steps**:
- Create a protected route handler utility
- Redirect unauthenticated users from app/page.tsx to login
**Estimated Time**: 30 minutes
**Priority**: High

### Task 8: Create Header Component
**Objective**: Build a header component with logout functionality.
**Steps**:
- Create Header component with logout button
- Use Better Auth signOut function
- Display user info and logout option
**Estimated Time**: 45 minutes
**Priority**: Medium

### Task 9: Create TaskCard Component
**Objective**: Implement the TaskCard component with the required UI elements.
**Steps**:
- Create TaskCard component using shadcn/ui Card
- Include title, description, checkbox, and edit/delete buttons
- Implement styling for completed tasks
**Estimated Time**: 1 hour
**Priority**: High

### Task 10: Define Task Type
**Objective**: Create a type definition for tasks.
**Steps**:
- Create types/task.ts file
- Define the Task interface with id, title, description, completed, createdAt, updatedAt fields
**Estimated Time**: 15 minutes
**Priority**: Low

### Task 11: Create TaskForm Component
**Objective**: Implement the TaskForm component for adding and updating tasks.
**Steps**:
- Create TaskForm component with form fields for title and description
- Add submit handler and proper validation
- Include cancel functionality
**Estimated Time**: 1 hour
**Priority**: High

### Task 12: Create Dashboard Page with Animations
**Objective**: Implement the dashboard page with task list and animations using Framer Motion.
**Steps**:
- Create dashboard page at app/dashboard/page.tsx
- Fetch user's tasks on mount
- Display tasks in a list with TaskCard components
- Implement Framer Motion animations for task interactions
- Add loading states and error handling
**Estimated Time**: 2 hours
**Priority**: High

### Task 13: Add Animation Variants
**Objective**: Create animation variants for consistent animations across the app.
**Steps**:
- Create lib/animations.ts with predefined animation variants
- Define variants for task entry, exit, and completion transitions
**Estimated Time**: 45 minutes
**Priority**: Medium

### Task 14: Update Global Styles
**Objective**: Add custom CSS for the dark theme and amber accents.
**Steps**:
- Update app/globals.css with custom CSS variables for dark theme and amber accents
- Include styles for both light and dark modes
**Estimated Time**: 30 minutes
**Priority**: Medium

### Task 15: Add Toast Provider
**Objective**: Set up the Sonner toast provider for notifications.
**Steps**:
- Create app/providers.tsx to include Sonner toast provider
- Update root layout to include the providers
**Estimated Time**: 30 minutes
**Priority**: Medium

### Task 16: Create Directory Structure
**Objective**: Finalize the directory structure as outlined in the spec.
**Steps**:
- Ensure complete directory structure exists for the frontend
- Verify all necessary files and folders are in place as specified in the feature spec
**Estimated Time**: 15 minutes
**Priority**: Low

### Task 17: Add Environment Configuration
**Objective**: Set up environment variables for API configuration.
**Steps**:
- Create .env.example file in frontend directory
- Define environment variable for API configuration
**Estimated Time**: 15 minutes
**Priority**: Low

### Task 18: Prepare for Local Testing
**Objective**: Add scripts for local development and testing.
**Steps**:
- Update package.json with scripts for development, building, and testing
- Include scripts: dev, build, start, lint
**Estimated Time**: 15 minutes
**Priority**: Low

### Task 19: Prepare for Vercel Deployment
**Objective**: Create Vercel configuration if needed.
**Steps**:
- Create vercel.json configuration file for deploying the Next.js application to Vercel
**Estimated Time**: 15 minutes
**Priority**: Low

### Task 20: Create README
**Objective**: Document the frontend setup and usage.
**Steps**:
- Create README.md in frontend directory
- Include setup instructions, available scripts, and project overview
**Estimated Time**: 30 minutes
**Priority**: Low

## Timeline
The estimated total time to complete all these tasks is 6-8 hours, depending on familiarity with the technologies. It's recommended to commit changes after completing each major task to maintain a clean development history.