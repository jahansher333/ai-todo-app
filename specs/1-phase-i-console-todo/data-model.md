# Data Model: Phase I Console Todo

## Entities

### TodoTask
- **id**: `int` - Auto-incrementing unique identifier.
- **title**: `str` - Required, task summary.
- **description**: `str` - Optional, extra details.
- **is_completed**: `bool` - Defaults to `False`.

## State Transitions
- **Pending** -> **Completed**: Via `complete [ID]` command.
- **Completed** -> **Pending**: Via `complete [ID]` command (toggle).

## Validation Rules
- `title` must not be empty or whitespace only.
- `id` must exist in the in-memory store for update/delete/complete operations.
