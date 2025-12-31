# Feature Specification: Phase I - In-Memory Python Console Todo Application (Full Progression)

**Feature Branch**: `2-phase-i-full-progression`
**Created**: 2025-12-31
**Status**: Draft
**Input**: User description: "Phase I: In-Memory Python Console Todo Application – Full Progression. Target: Single-user, in-memory console Todo app with complete feature set. Focus: Professional, rich console UX with colored output, intuitive commands, clear formatting. Success criteria: Implement ALL Basic features (CRUD), ALL Intermediate features (Priorities, Tags, Search, Sort), and ALL Advanced features (Recurring Tasks, Due Dates, Reminders). Rich console design: ANSI colors, table-like list, command menu. Commands: interactive loop (e.g., 'add Buy groceries high work tomorrow 10am')."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Advanced Task Creation (Priority: P1)

As a busy professional, I want to add tasks with specific priorities, categories, and due dates using a single command string so that I can organize my day efficiently without multiple prompts.

**Why this priority**: Core functionality that enables all downstream features (sorting, filtering, reminders).

**Independent Test**: Add a task with title, priority (High), tag (Work), and a due date. Verify the task details appear correctly in the list.

**Acceptance Scenarios**:

1. **Given** the app is running, **When** I enter `add "Finish report" high work "2025-01-05 14:00"`, **Then** the system confirms the task is added with all 4 attributes.
2. **Given** no due date is provided, **When** I add a task, **Then** the system defaults to "None" or "No Deadline".

---

### User Story 2 - Organization and Retrieval (Priority: P2)

As a user with many tasks, I want to search by keywords and sort my list by priority or due date so that I can focus on the most urgent work first.

**Why this priority**: Essential for managing more than a handful of tasks.

**Independent Test**: Add 5 tasks with varied priorities and dates. Run `sort priority` and verify the "High" priority tasks appear at the top.

**Acceptance Scenarios**:

1. **Given** several tasks exist, **When** I run `search "groceries"`, **Then** only tasks matching that keyword are displayed in the table.
2. **Given** tasks with different dates, **When** I run `sort due`, **Then** the list is ordered chronologically by the due timestamp.

---

### User Story 3 - Smart Management & Automation (Priority: P3)

As a user, I want some tasks to repeat every day and receive reminders when a deadline is approaching so that I don't forget recurring responsibilities.

**Why this priority**: High-value feature for long-term productivity and automation.

**Independent Test**: Add a task with a reminder set for 5 minutes from now. Wait and run any command (or 'check'); verify a "Reminder" alert is displayed.

**Acceptance Scenarios**:

1. **Given** a recurring task set to "daily", **When** I mark it complete, **Then** the system automatically creates a new instance for the next day.
2. **Given** a task list is displayed, **When** a task is overdue, **Then** the due date is highlighted in blinking or bold Red.

---

### Edge Cases

- **Invalid Date Format**: User enters "tomorrow" instead of ISO format. System should attempt a basic natural language parse or show a helpful usage guide.
- **Malformed Command**: Command like `add "Task"` without enough args. System should show specific syntax for that command.
- **Recurring Collision**: Attempting to set a recurring rule on a task that already has one.
- **Empty Search**: Search keyword returning zero results. System should show a "No matches found" warning rather than an empty table.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support CRUD operations (Add, View, Update, Delete, Complete).
- **FR-002**: System MUST allow tasks to have a Priority (High, Medium, Low) and Tags (user-defined strings).
- **FR-003**: System MUST provide a search function (keyword match on titles/tags) and filters (by status/priority).
- **FR-004**: System MUST allow sorting the list by Title, Priority, or Due Date.
- **FR-005**: System MUST support Due Dates with minute precision (YYYY-MM-DD HH:MM).
- **FR-006**: System MUST implement Recurring Tasks (Daily, Weekly) – completion triggers next occurrence.
- **FR-007**: System MUST simulate Reminders by checking current time against thresholds upon every user command invocation.
- **FR-008**: System MUST use rich ANSI colors (Green/Done, Red/Pending, Magenta/High Priority, Yellow/Warning).
- **FR-009**: System MUST handle all data in-memory (RAM) and exit gracefully.

### Key Entities

- **Task**:
  - `ID`: unique int
  - `Title`: string
  - `Description`: string
  - `Status`: boolean
  - `Priority`: enum (High, Medium, Low)
  - `Tags`: list of strings
  - `DueDate`: datetime object
  - `Recurring`: enum (None, Daily, Weekly)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The single-line command parser correctly identifies ≥95% of valid argument combinations.
- **SC-002**: List rendering handles up to 5 categories (ID, Status, Priority, Title, Due Date) without column misalignment.
- **SC-003**: Sorting 100 in-memory tasks takes less than 5ms.
- **SC-004**: Reminders are triggered within 1 second of the first command run after the threshold.
- **SC-005**: 100% of user input errors are caught with descriptive, colored feedback.
