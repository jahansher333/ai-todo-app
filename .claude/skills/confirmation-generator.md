# ConfirmationGeneratorSkill

## Purpose
Generate natural, friendly confirmation reply after MCP tool execution

## Inputs
- `action` (string): One of "created"/"updated"/"completed"/"deleted"
- `task_data` (object): Object containing task information (e.g., title, id, details)

## Outputs
- `message` (string): Human-readable confirmation message in a friendly tone

## Behavior
- Use friendly, conversational tone
- Include relevant task title or information
- Add appropriate emoji for positive reinforcement
- Handle different action types with appropriate phrasing
- Gracefully handle errors with empathetic messaging

## Action-Specific Responses

### Created
- Format: "Added your task: [task title]! ✅"
- Alternative: "Great! I've created the task '[task title]' for you! 📝"
- Emoji options: ✅, 📝, ➕

### Updated
- Format: "Updated task to '[new task title]' ✓"
- Alternative: "Changes saved! Task updated to '[task title]' 💾"
- Emoji options: ✓, 💾, 🔄

### Completed
- Format: "Great job! Task '[task title]' marked as complete 🎉"
- Alternative: "Nice work! Marked '[task title]' as done ✨"
- Emoji options: 🎉, ✨, 👍

### Deleted
- Format: "Task removed successfully 🗑️"
- Alternative: "Task '[task title]' has been deleted 🗑️"
- Emoji options: 🗑️, ❌, 🚫

### Error Handling
- Format: "Sorry, couldn't find task [id] 😕"
- Alternative: "Oops! Something went wrong with the task operation 🤔"
- Emoji options: 😕, 🤔, ⚠️

## Examples

### Example 1:
**Action:** "created"
**Task Data:** {title: "Buy groceries"}
**Output:** "Added your task: Buy groceries! ✅"

### Example 2:
**Action:** "completed"
**Task Data:** {title: "Call mom"}
**Output:** "Great job! Task 'Call mom' marked as complete 🎉"

### Example 3:
**Action:** "updated"
**Task Data:** {title: "Buy groceries and eggs"}
**Output:** "Updated task to 'Buy groceries and eggs' ✓"

### Example 4:
**Action:** "deleted"
**Task Data:** {title: "Old task"}
**Output:** "Task 'Old task' has been deleted 🗑️"

### Example 5 (Error):
**Action:** "error"
**Task Data:** {id: 5, error: "not found"}
**Output:** "Sorry, couldn't find task 5 😕"

## Implementation Notes
- Personalize messages using pronouns like "your" when appropriate
- Maintain consistency in emoji usage for each action type
- Ensure task titles are properly escaped to prevent formatting issues
- Include contextual information from task_data when helpful
- Keep messages concise but informative