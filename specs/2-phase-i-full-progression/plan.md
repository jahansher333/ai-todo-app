# Implementation Plan: Phase I Full Progression

**Branch**: `2-phase-i-full-progression` | **Date**: 2025-12-31 | **Spec**: [specs/2-phase-i-full-progression/spec.md](spec.md)

## Summary
The goal is to evolve the Phase I console application into a full-featured productivity tool. This includes adding support for task priorities, tags, multi-column sorting, keyword search, recurring schedules (Daily/Weekly), and simulated due-date reminders.

## Technical Context
- **Language/Version**: Python 3.13+
- **Primary Dependencies**: `datetime`, `shlex`, `re`, `sys`, `os`.
- **Storage**: Python list of dicts.
- **Constraints**: 100% built-in modules only.

## Architecture
```text
[main.py]
  ├── [Command Loop] <--> [shlex Parser]
  ├── [CRUD Module] (add, delete, update, status toggle)
  ├── [Search/Filter Module] (keyword match, status filter)
  ├── [Sort Module] (priority lambda, date lambda)
  ├── [Advanced Module] (Recurring calculation, Overdue reminder check)
  └── [UI Module] (ASCII layout, ANSI color engine)
```

## Constitution Check

| Principle | Status | Justification |
|-----------|--------|---------------|
| Helpful/Innovative | ✅ | Demonstrates high maturity for a console app. |
| Honest/Accurate | ✅ | Aligned with Phase I "Advanced" deliverables for 600 bonus pts. |
| Spec-Driven | ✅ | All features mapped from 2-phase-i-full-progression/spec.md. |
| Efficient/Scalable | ✅ | Modular command groups prevent `main()` bloat. |

## Feature Breakdown
1. **Intermediate**:
   - Priority field + sorting.
   - Tag system + filtering.
   - Keyword search across title/tag.
2. **Advanced**:
   - `datetime` parsing for due dates.
   - Overdue highlighting (Reminder simulation).
   - Recursive task reset logic.

## UX Guidelines
- **Priority Badges**: [H], [M], [L] with distinct colors.
- **Overdue Alert**: Red bold text for dates in the past.
- **Completion Symbols**: Consistent `[X]` vs `[ ]` across all listing modes.
- **Search Result Info**: "Showing N results for '[query]'" feedback.
