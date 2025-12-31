# Tasks: Phase I Full Progression (Full Feature Set)

**Input**: Design documents from `/specs/2-phase-i-full-progression/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 [P1] Initialize project structure (phase-i/src/main.py, README.md, constitution.md) (15m)
- [x] T002 [P1] Define full task data model (dict: id, title, desc, completed, priority, tags, due, recurring) (10m)
- [x] T003 [P1] Configure ANSI color constants and specialized UI symbols (✓/○/H/M/L) (10m)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before user story work

- [x] T004 [P1] Implement rich view_tasks() with multi-column colored table output (30m)
- [x] T005 [P1] Implement core CRUD logic: add_task, update_task, delete_task, toggle_complete (30m)
- [x] T006 [P1] Implement shlex-based command parser with keyword detection (25m)

---

## Phase 3: User Story 1 - Advanced Task Management (Priority: P1) 🎯 MVP

**Goal**: As a user, I want to add/organize tasks with priorities and categories.

- [x] T007 [P] [US1] Implement priority setting logic (High/Medium/Low) in src/main.py (15m)
- [x] T008 [P] [US1] Implement tag/category management in src/main.py (15m)
- [x] T009 [US1] Integrate priority and tags into the table list view (15m)

---

## Phase 4: User Story 2 - Search & Retrieval (Priority: P2)

**Goal**: As a user, I want to filter and search through my tasks.

- [x] T010 [P] [US2] Implement search command (keyword match on title/description/tags) (20m)
- [x] T011 [P] [US2] Implement status and priority filters (e.g., list pending high) (20m)
- [x] T012 [US2] Implement sort_tasks() by Due Date, Priority, or Title (20m)

---

## Phase 5: User Story 3 - Smart Automation (Priority: P3)

**Goal**: As a user, I want recurring tasks and due-date reminders.

- [x] T013 [P] [US3] Implement datetime parsing for Due Dates (YYYY-MM-DD HH:MM) (20m)
- [x] T014 [P] [US3] Implement recurring task logic (Daily/Weekly next occurrence) (25m)
- [x] T015 [US3] Implement reminder check logic (trigger overdue alerts on startup/listing) (20m)

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Final touches and graceful handling

- [x] T016 [P3] Add comprehensive help screen with command syntax and examples (15m)
- [x] T017 [P3] Implement graceful exit handling and error boundary coloring (10m)
- [x] T018 [P3] Finalize Phase I README.md with Full Progression feature mapping (15m)

---

## Validation

Run `/sp.check` to validate coverage of:
1. Basic CRUD (Complete)
2. Intermediate (Priorities, Tags, Search, Filter, Sort)
3. Advanced (Due Dates, Recurring, Reminders)
