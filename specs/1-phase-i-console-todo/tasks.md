# Tasks: Phase I Console Todo Application

**Input**: Design documents from `/specs/1-phase-i-console-todo/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 [P1] Initialize project structure (phase-i/src/main.py, README.md, constitution.md) (15m)
- [x] T002 [P1] Create task data structure and initial state (list of dicts: id, title, description, completed) (10m)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before user story work

- [x] T003 [P1] Implement view_tasks() with rich colored table output (ANSI formatting) (30m)
- [x] T004 [P3] Add error handling utilities and ANSI color constants (15m)

---

## Phase 3: User Story 1 - Quick Task Management (Priority: P1) 🎯 MVP

**Goal**: As a user, I want to quickly add a task and mark it as complete.

- [x] T005 [P] [US1] Implement add_task() with title/description support and input validation (20m)
- [x] T006 [US1] Implement toggle_complete() logic with visual feedback (15m)

---

## Phase 4: User Story 2 - Task Organization (Priority: P2)

**Goal**: As a user, I want to see a formatted list of all tasks.

- [x] T007 [US2] Build main application loop with simple command parser (25m)
- [x] T008 [US2] Implement help menu and status bar display (15m)

---

## Phase 5: User Story 3 - Maintenance (Priority: P2)

**Goal**: As a user, I want to update or delete existing tasks.

- [x] T009 [US3] Implement update_task() for title and description by ID (20m)
- [x] T010 [US3] Implement delete_task() functionality by ID (15m)

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Final touches and graceful handling

- [x] T011 [P3] Implement graceful exit handling (KeyboardInterrupt/Ctrl+C) (15m)
- [x] T012 [P3] Write README.md with run instructions and command examples (15m)

---

## Dependencies & Execution Order

1. **Setup (Phase 1)** -> **Foundational (Phase 2)** (T001-T004)
2. **User Story 1 (Phase 3)**: Core MVP functionality.
3. **User Story 2 & 3 (Phase 4 & 5)**: Can proceed in parallel after US1 logic is ready.
4. **Polish (Phase N)**: Final wrap-up.

---

## Validation

Run `/sp.check` to validate coverage of all 5 basic features:
1. Add Task
2. Delete Task
3. Update Task
4. View Task List
5. Mark as Complete
