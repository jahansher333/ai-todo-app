# ErrorHandlerSkill

Convert backend/tool errors into user-friendly chat responses

## Purpose
Convert backend/tool errors into user-friendly chat responses

## Inputs
- `error_type`: string ("not_found"/"invalid_input"/"permission_denied"/"unknown")
- `details`: string

## Output
String - polite, helpful reply

## Behavior
- `not_found` → "I couldn't find that task. Maybe check the ID? 😅"
- `invalid_input` → "Hmm, I didn't understand that command. Try something like 'add task buy milk'?"
- `permission_denied` → "This task belongs to someone else. Make sure you're logged in correctly!"
- `unknown` → "Something went wrong on my end 😔 Please try again."

Always keep tone supportive and suggest retry/help.

## Prompt Template
```
When encountering an error of type "{{error_type}}" with details "{{details}}", respond with a user-friendly message that follows these guidelines:

- If error_type is "not_found": "I couldn't find that task. Maybe check the ID? 😅"
- If error_type is "invalid_input": "Hmm, I didn't understand that command. Try something like 'add task buy milk'?"
- If error_type is "permission_denied": "This task belongs to someone else. Make sure you're logged in correctly!"
- If error_type is "unknown": "Something went wrong on my end 😔 Please try again."

Always maintain a supportive tone and suggest retrying or asking for help when appropriate.
```

## Test Cases

### Test Case 1: not_found
- Input: `{error_type: "not_found", details: "Task ID 123 not found"}`
- Expected Output: "I couldn't find that task. Maybe check the ID? 😅"

### Test Case 2: invalid_input
- Input: `{error_type: "invalid_input", details: "Command 'xyz' not recognized"}`
- Expected Output: "Hmm, I didn't understand that command. Try something like 'add task buy milk'?"

### Test Case 3: permission_denied
- Input: `{error_type: "permission_denied", details: "Access denied for task 456"}`
- Expected Output: "This task belongs to someone else. Make sure you're logged in correctly!"

### Test Case 4: unknown
- Input: `{error_type: "unknown", details: "Unexpected server error occurred"}`
- Expected Output: "Something went wrong on my end 😔 Please try again."