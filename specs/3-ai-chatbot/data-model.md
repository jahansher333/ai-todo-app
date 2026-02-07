# Data Model: Todo AI-Powered Chatbot

## Entity: User
- **Fields**:
  - id (UUID/string): Unique identifier
  - email (string): User's email address
  - created_at (timestamp): Account creation time
  - updated_at (timestamp): Last update time
- **Relationships**: One-to-many with Conversations and Tasks
- **Validation**: Email format validation, unique constraint on email

## Entity: Conversation
- **Fields**:
  - id (UUID/string): Unique identifier
  - user_id (UUID/string): Foreign key to User
  - title (string, optional): Conversation title/description
  - created_at (timestamp): Creation time
  - updated_at (timestamp): Last update time
- **Relationships**: Belongs to User, one-to-many with Messages
- **Validation**: user_id must reference existing User

## Entity: Message
- **Fields**:
  - id (UUID/string): Unique identifier
  - conversation_id (UUID/string): Foreign key to Conversation
  - user_id (UUID/string): Foreign key to User
  - role (string): "user" or "assistant"
  - content (text): Message content
  - timestamp (timestamp): Message creation time
- **Relationships**: Belongs to Conversation and User
- **Validation**: conversation_id must reference existing Conversation, role must be valid value

## Entity: Task
- **Fields**:
  - id (UUID/string): Unique identifier
  - user_id (UUID/string): Foreign key to User
  - title (string): Task title
  - description (text, optional): Task description
  - status (string): "pending", "in-progress", "completed"
  - created_at (timestamp): Creation time
  - updated_at (timestamp): Last update time
- **Relationships**: Belongs to User
- **Validation**: user_id must reference existing User, status must be valid value

## State Transitions

### Task Status Transitions
- pending → in-progress: When user starts working on task
- in-progress → completed: When user marks task as complete
- completed → pending: When user reopens completed task
- pending → completed: Direct completion from pending state

### Message Role Values
- user: Messages sent by the end user
- assistant: Messages sent by the AI assistant

## Relationships

### User → Conversation (One-to-Many)
- A user can have multiple conversations
- Each conversation belongs to exactly one user
- Deleting a user cascades to conversations

### Conversation → Message (One-to-Many)
- A conversation can have multiple messages
- Each message belongs to exactly one conversation
- Deleting a conversation cascades to messages

### User → Task (One-to-Many)
- A user can have multiple tasks
- Each task belongs to exactly one user
- Deleting a user cascades to tasks

## Indexes
- User.email: For efficient authentication lookups
- Conversation.user_id: For user-specific queries
- Message.conversation_id: For conversation history retrieval
- Message.user_id: For user-specific message queries
- Task.user_id: For user-specific task queries
- Task.status: For status-based filtering