# Implementation Tasks: Phase II - Todo Full-Stack Web Application – Jira-like Experience

## Phase 1: Project Setup and Monorepo Configuration

- [X] T001 [P1] Setup monorepo: create frontend/ directory with Next.js 16+ App Router
- [X] T002 [P1] Setup monorepo: create backend/ directory with FastAPI structure
- [X] T003 [P1] Setup monorepo: create specs/ directory and .spec-kit/config.yaml
- [X] T004 [P1] Initialize Next.js 16+ app in frontend/ with App Router and Tailwind CSS
- [X] T005 [P1] Initialize FastAPI app in backend/ with basic structure (main.py)

## Phase 2: Backend Foundation

- [X] T006 [P1] Create SQLModel models (User, Task) with user_id FK, priority, tags, due, recurring
- [X] T007 [P1] Set up Neon DB connection with proper configuration
- [X] T008 [P1] Implement JWT middleware (verify token, extract user_id, 401 on error/mismatch)
- [X] T009 [P1] Create base API dependencies for authentication
- [X] T010 [P1] Set up database session management

## Phase 3: Backend API Implementation

- [X] T011 [P2] Create REST endpoints /api/{user_id}/tasks with ownership filter
- [X] T012 [P2] Implement GET /api/{user_id}/tasks supporting all fields (basic/intermediate/advanced)
- [X] T013 [P2] Implement POST /api/{user_id}/tasks supporting all fields (basic/intermediate/advanced)
- [X] T014 [P2] Implement PUT /api/{user_id}/tasks/{task_id} supporting all fields (basic/intermediate/advanced)
- [X] T015 [P2] Implement DELETE /api/{user_id}/tasks/{task_id} with ownership validation
- [X] T016 [P2] Add proper error handling and validation to all endpoints

## Phase 4: Frontend Foundation

- [X] T017 [P2] Set up Better-Auth in frontend (signup/signin + JWT handling)
- [X] T018 [P2] Create API client (lib/api.ts) with Authorization: Bearer token
- [X] T019 [P2] Set up authentication context/provider in frontend
- [X] T020 [P2] Create login and signup pages with form validation
- [X] T021 [P2] Implement protected route handling

## Phase 5: Jira-like UI Implementation

- [X] T022 [P3] Create Kanban board layout with To Do / In Progress / Done columns
- [X] T023 [P3] Implement drag-and-drop functionality for task status change
- [X] T024 [P3] Create task card component with priority badges, tags chips, due date
- [X] T025 [P3] Implement list view toggle for Kanban board
- [X] T026 [P3] Add filters/sorts/search bar functionality
- [X] T027 [P3] Make UI responsive with mobile-friendly layout
- [X] T028 [P3] Implement task creation form with all required fields
- [X] T029 [P3] Implement task editing functionality

## Phase 6: Advanced Features

- [X] T030 [P3] Add recurring task functionality (daily/weekly)
- [X] T031 [P3] Implement calendar date picker for due dates
- [X] T032 [P3] Add overdue task highlighting
- [X] T033 [P3] Enhance search functionality with advanced filtering
- [X] T034 [P3] Implement proper loading and error states

## Phase 7: Testing and Integration

- [X] T035 [P3] Test end-to-end: Signup, login, create task, update task, delete task
- [X] T036 [P3] Test authentication flow with JWT tokens
- [X] T037 [P3] Test user isolation (ensure users can't access other users' tasks)
- [X] T038 [P3] Test Kanban board functionality (drag-and-drop, status changes)
- [X] T039 [P3] Test all advanced features (recurring, due dates, filters)
- [X] T040 [P3] Perform responsive design testing on multiple screen sizes

## Dependencies

### User Story Dependencies:
- All foundational tasks (Phase 1-2) must be completed before API implementation
- Backend API (Phase 3) must be completed before frontend implementation
- Frontend foundation (Phase 4) must be completed before UI implementation
- Authentication must be working before advanced features

### Parallel Execution Opportunities:
- [P] Database model creation can run parallel to API endpoint development
- [P] Frontend authentication setup can run parallel to API development
- [P] UI components can be developed in parallel after foundation is complete

## Implementation Strategy

1. **MVP Scope**: Complete Phase 1, 2, and basic API functionality (T001-T016) to establish the foundation
2. **Incremental Delivery**: Each phase builds upon the previous one, delivering increasing value to users
3. **Test Early**: Critical user flows should be tested as soon as core functionality is implemented
4. **Security First**: Authentication and user isolation should be implemented early and validated throughout development