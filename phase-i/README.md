# Evolution of Todo: Phase I (Full Progression)

## Overview
Phase I has evolved from a basic script into a comprehensive productivity tool. It remains a lightweight, single-user, in-memory console application built with Python 3.13+, now featuring advanced organization and automation logic.

## Enhanced Features

### Basic Features
- **Task Management**: Add, view, update, delete, and complete tasks
- **Interactive Console Loop**: Intuitive command-line interface with real-time feedback
- **Rich ANSI Output**: Color-coded status, priorities, and warnings
- **Table Formatting**: Clean multi-column layout with aligned text

### Intermediate Features
- **Prioritized Tasks**: High, Medium, and Low priorities with visual badges ([H], [M], [L])
- **Tagging System**: Categorize tasks (e.g., #WORK, #HOME) for better organization
- **Keyword Search**: Search across titles, descriptions, and tags
- **Status Filters**: Filter tasks by completion status (pending/done)
- **Priority Filters**: Filter tasks by priority level (high/medium/low)
- **Multi-column Sorting**: Sort by Due Date, Priority, or Title

### Advanced Features
- **Due Dates**: Parse relative (today/tomorrow) and absolute (YYYY-MM-DD) dates
- **Overdue Detection**: Automatic red highlighting for past-due tasks
- **Proactive Reminders**: Visual alerts in status bar showing overdue count
- **Recurring Tasks**: Automatic rescheduling for Daily and Weekly tasks
  - Completing a recurring task creates a new instance for the next period
  - Supports both daily and weekly intervals

## Command Reference

| Command | Arguments | Description |
|---------|-----------|-------------|
| `add` | `<title> [desc] [prio] [tag] [due] [recur]` | Add a fully documented task |
| `list` | None | View all tasks with status and priority |
| `filter` | `<status|pri> <value>` | Filter by: status (pending/done) or priority (high/med/low) |
| `search`| `<query>` | Search titles, descriptions, and tags |
| `sort` | `due\|priority\|title` | Reorder your productivity list |
| `update`| `<id> <field> <value>` | Update task: title, desc, prio, tag, due |
| `complete`| `<id>` | Toggle task completion (triggers recurring) |
| `delete` | `<id>` | Remove a task |
| `clear` | None | Clear the console and reprint banner |
| `quit` | None | Exit application |
| `help` | None | Show command reference |

## Setup & Execution

```bash
# Navigate to phase-i
cd phase-i

# Run using the advanced CLI
python src/main.py
```

## Advanced Usage Examples

### Adding Tasks with All Properties
```text
todo » add "Finish Report" "Q4 Data" HIGH WORK "2026-01-05 14:00" DAILY
Success: Task 'Finish Report' added! ID: 1

todo » list
 STATUS  Total: 1 Done: 0 Overdue: 0

  ID   Pri     Status      Task Title            Due Date              Tag
  -------------------------------------------------------------------------------------
    1  HIGH    [ ] Pending  Finish Report         2026-01-05 14:00      #WORK
```

### Filtering Tasks
```text
todo » filter status pending
Results for: status: pending
# Shows only pending tasks

todo » filter priority high
Results for: priority: high
# Shows only high priority tasks
```

### Updating Tasks
```text
todo » update 1 title "Updated Report Title"
Success: Task 1 updated.

todo » update 1 prio LOW
Success: Task 1 updated.

todo » update 1 tag PERSONAL
Success: Task 1 updated.
```

### Searching Tasks
```text
todo » search "report"
Results for: REPORT
# Shows all tasks matching "report" in title, description, or tags
```

### Sorting
```text
todo » sort due
Success: Tasks sorted by due.
# Orders tasks chronologically by due date

todo » sort priority
Success: Tasks sorted by priority.
# Orders tasks by priority (high first)
```

### Recurring Tasks
```text
todo » add "Daily Standup" "Team sync" HIGH WORK today DAILY
Success: Task 'Daily Standup' added! ID: 1

todo » complete 1
Success: Task 1 is now completed.
Success: Task 'Daily Standup' added! ID: 2
 * Recurring task scheduled for: 2026-01-02
# A new task is automatically created for tomorrow
```

### Overdue Detection
```text
todo » add "Old Task" "Past due" HIGH WORK "2025-12-01"
Success: Task 'Old Task' added! ID: 1

todo » list
 STATUS  Total: 1 Done: 0 Overdue: 1

  ID   Pri     Status      Task Title            Due Date              Tag
  -------------------------------------------------------------------------------------
    1  HIGH    [ ] Pending  Old Task             2025-12-01 00:00 (OVERDUE)  #WORK
# Due date shown in RED with (OVERDUE) indicator
```

## Date Formats Supported

- **Absolute**: `2026-01-05`, `2026-01-05 14:30`
- **Relative**: `today`, `tomorrow`
- **No Date**: Omit the due date field for tasks without deadlines
