---
id: 7
title: "Fix Task ID Re-indexing"
stage: "refactor"
date: "2025-12-31"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "1-phase-i-console-todo"
branch: "1-phase-i-console-todo"
user: "anonymous"
command: "bash"
labels: ["refactor", "bugfix", "id-management"]
links:
  spec: "specs/1-phase-i-console-todo/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - phase-i/src/main.py
tests_yaml: []
---

## PROMPT_TEXT
i am delete list tasks id not remove and i am enter another id number is + not 1 is 2

## RESPONSE_TEXT
I have updated the `delete_task` logic in `phase-i/src/main.py`. Now, whenever a task is deleted:
1. All remaining tasks are re-indexed to ensure the ID list remains sequential (1, 2, 3...).
2. The `next_id` counter is reset to `len(tasks) + 1` so that the next added task follows the current sequence instead of skipping numbers.

## OUTCOME
Task IDs are now dynamic and sequential after deletion.
