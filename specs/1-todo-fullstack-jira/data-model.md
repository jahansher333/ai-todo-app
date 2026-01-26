# Data Model: Phase II - Todo Full-Stack Web Application

## Entity Definitions

### User
Represents a registered user of the application

**Fields**:
- `id` (UUID/String): Unique identifier for the user
- `email` (String): User's email address (unique, validated)
- `password_hash` (String): Hashed password for authentication
- `first_name` (String, optional): User's first name
- `last_name` (String, optional): User's last name
- `created_at` (DateTime): Timestamp when user account was created
- `updated_at` (DateTime): Timestamp when user account was last updated
- `is_active` (Boolean): Whether the account is active

### Task
Represents a personal task owned by a user

**Fields**:
- `id` (UUID/String): Unique identifier for the task
- `user_id` (UUID/String): Foreign key linking to the owning user
- `title` (String): Task title (required, max 200 characters)
- `description` (Text, optional): Detailed task description
- `completed` (Boolean): Whether the task is completed
- `priority` (String): Task priority level ('high', 'medium', 'low')
- `tags` (Array/List): Array of category tags for the task
- `due` (DateTime, optional): Deadline for task completion
- `recurring` (String, optional): Recurrence pattern ('daily', 'weekly', etc.)
- `created_at` (DateTime): Timestamp when task was created
- `updated_at` (DateTime): Timestamp when task was last updated

### Tag
Represents a category label that can be applied to tasks

**Fields**:
- `id` (UUID/String): Unique identifier for the tag
- `name` (String): Tag name (unique per user)
- `color` (String): Color code for visual representation
- `user_id` (UUID/String): Foreign key linking to the owning user
- `created_at` (DateTime): Timestamp when tag was created

## Relationships

- **User → Task**: One-to-Many (One user owns many tasks)
- **User → Tag**: One-to-Many (One user owns many tags)
- **Task → Tag**: Many-to-Many through tags field (Tasks can have multiple tags)

## Validation Rules

### User Validation
- Email must be a valid email format
- Password must meet minimum strength requirements
- Email must be unique across all users

### Task Validation
- Title is required and must be between 1-200 characters
- Description, if provided, must be under 10,000 characters
- Status must be one of the allowed enum values
- Priority must be one of the allowed enum values
- Due date, if set, must not be in the past (optional business rule)
- User_id must reference an existing, active user

### Tag Validation
- Name is required and must be unique per user
- Name must be between 1-50 characters
- Color, if provided, must be a valid hex color code

## State Transitions

### Task Status Transitions
- `to_do` → `in_progress`: When user starts working on the task
- `in_progress` → `to_do`: When user returns task to pending state
- `in_progress` → `done`: When user completes the task
- `done` → `in_progress`: When user reopens completed task
- `to_do` → `done`: Direct completion (valid transition)

## Indexes

### Recommended Database Indexes
- `users.email` (Unique index for authentication)
- `tasks.user_id` (Index for user-based queries)
- `tasks.status` (Index for status filtering)
- `tasks.priority` (Index for priority sorting)
- `tasks.due_date` (Index for due date queries)
- `tasks.created_at` (Index for chronological sorting)

## Constraints

### Business Logic Constraints
- A task can only be accessed by its owner (enforced by API)
- Completed tasks cannot have a due date in the past (informational)
- Recurring tasks generate new instances based on pattern when completed
- Tags are scoped to user (cannot share tags between users)