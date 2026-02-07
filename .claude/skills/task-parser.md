# TaskParserSkill

## Purpose
Parse natural language user message to extract structured task data for MCP tools

## Inputs
- `message` (string) – user's chat input, e.g. "Add task buy groceries high work tomorrow 10am"

## Outputs
JSON object with the following structure:
```json
{
  "title": "string (main action phrase - required)",
  "description": "string (optional - any extra text after title)",
  "priority": "string (optional - high/medium/low/urgent/normal)",
  "tags": "array (optional - work/home/personal/shopping as list)",
  "due": "string (optional - date/time in ISO format)",
  "recurring": "string (optional - daily/weekly/monthly)"
}
```

## Behavior
- Title: main action phrase (required)
- Description: any extra text after title
- Priority: detect high/medium/low/urgent/normal
- Tags: detect words like work/home/personal/shopping as list
- Due: parse dates/times (tomorrow, next week, YYYY-MM-DD, 10am, etc.) into ISO string
- Recurring: detect daily/weekly/monthly
- Return null fields if not present

## Examples

### Example 1:
**Input:** "Add weekly team meeting next monday 3pm important"
**Output:**
```json
{
  "title": "team meeting",
  "recurring": "weekly",
  "due": "2026-02-09T15:00:00",
  "priority": "high"
}
```

### Example 2:
**Input:** "Buy groceries high work tomorrow 10am"
**Output:**
```json
{
  "title": "Buy groceries",
  "priority": "high",
  "tags": ["work"],
  "due": "2026-02-02T10:00:00"
}
```

### Example 3:
**Input:** "Call doctor appointment personal urgent"
**Output:**
```json
{
  "title": "Call doctor appointment",
  "priority": "urgent",
  "tags": ["personal"]
}
```

## Implementation Notes
- Use natural language processing to identify key elements
- Implement date/time parsing with consideration for relative dates
- Handle multiple possible interpretations of priority and tags
- Return consistent JSON format regardless of missing fields