# Data Model: Phase I Full Progression

## Entities

### TodoTask
- **id**: `int` (incremental & re-indexed)
- **title**: `str` (required)
- **description**: `str` (optional)
- **completed**: `bool` (default False)
- **priority**: `str` (HIGH, MEDIUM, LOW)
- **tag**: `str` (e.g., WORK, HOME, SHOPPING)
- **due_date**: `datetime` or `None`
- **recurring**: `str` or `None` (DAILY, WEEKLY)

## State Transitions
- **Mark Complete**: If `recurring` is set, completeness toggles and `due_date` is pushed forward. Completion of a recurring task effectively resets it for the next interval.

## Sorting Logic
- **Priority Sort**: High (1) > Medium (2) > Low (3).
- **Date Sort**: Past (overdue) > Today > Future > None.
