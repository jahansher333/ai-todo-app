# Evolution of Todo: Phase I (Full Progression)

## Overview
Phase I has evolved from a basic script into a comprehensive productivity tool. It remains a lightweight, single-user, in-memory console application built with Python 3.13+, now featuring advanced organization and automation logic.

## Enhanced Features
- **Intermediate**:
    - **Prioritized Tasks**: High, Medium, and Low priorities with visual badges.
    - **Tagging**: Categorize tasks (e.g., #WORK, #HOME) for better organization.
    - **Search & Filter**: Keyword search across all fields and status-based filtering.
    - **Multi-column Sorting**: Sort by Due Date, Priority, or Title.
- **Advanced**:
    - **Due Dates**: Parse relative (today/tomorrow) and absolute (YYYY-MM-DD) dates.
    - **Recurring Tasks**: Automatic rescheduling for Daily and Weekly tasks.
    - **Proactive Reminders**: Visual alerts for overdue tasks upon every action.

## Command Reference
| Command | Arguments | Description |
|---------|-----------|-------------|
| `add` | `<title> [desc] [prio] [tag] [due]` | Add a fully documented task |
| `list` | None | View all tasks with status and priority |
| `search`| `<query>` | Search titles, descriptions, and tags |
| `sort` | `due\|priority\|title` | Reorder your productivity list |
| `complete` | `<id>` | Toggle task completion (triggers recurring) |
| `clear` | None | Clear the console and reprint banner |

## Setup & Execution
```bash
# Navigate to phase-i
cd phase-i

# Run using the advanced CLI
python src/main.py
```

## Advanced Usage Example
```text
todo » add "Finish Report" "Q4 Data" HIGH WORK "2025-01-01"
Success: Task 'Finish Report' added! ID: 1

todo » list
 STATUS  Total: 1 Done: 0 Overdue: 0

  ID   Pri     Status      Task Title            Due Date              Tag
  -------------------------------------------------------------------------------------
    1  HIGH    [ ] Pending  Finish Report         2025-01-01 23:59      #WORK
```
