# Research: Phase I Full Progression

## Decisions

### Command Parsing: shlex + position-aware logic
- **Decision**: Continue using `shlex` for basic splitting, but implement a more flexible argument parser that detects keywords (priority, tag, due) vs. title and description.
- **Rationale**: Enables complex commands like `add "Task title" "desc" high work 2025-01-01` by checking list length and matching against known priority/recurring tokens.
- **Alternatives**: Python `argparse` (rejected as it's built for CLI flags, not interactive mini-shell commands).

### Date Handling: datetime.strptime with multiple formats
- **Decision**: Attempt to parse dates using a list of common formats (YYYY-MM-DD, YYYY-MM-DD HH:MM). For "tomorrow", implement a simple keyword mapper.
- **Rationale**: Balancing "no external libraries" with UX flexibility.
- **Alternatives**: `dateutil` (rejected due to library constraint).

### Reminder Simulation: Passive check on loop iteration
- **Decision**: Perform an overdue task check at the start of every command loop and before rendering the task list.
- **Rationale**: Simple way to provide "Reminders" in an in-memory, single-threaded console script without persistent background workers.

### Recurring Logic: Re-insertion on completion
- **Decision**: When a recurring task is marked complete, calculate the next due date based on the interval (Daily/Weekly) and immediately add/reset the task for the next occurrence.
- **Rationale**: Keeps the logic simple and ensures the "upcoming" task is always visible in the list.
