# Research: Phase I Console Todo Application

## Decisions

### Architecture: Function-Based Commands
- **Decision**: Use a procedural approach with a main loop and separate functions for CRUD operations.
- **Rationale**: Keeps the implementation simple, testable, and aligned with Phase I requirements (in-memory, console).
- **Alternatives**: Class-based Object Oriented (rejected as potentially over-engineering for a basic console script, though entities will be objects).

### CLI UX: ANSI Colors and Table Formatting
- **Decision**: Use standard ANSI escape sequences for coloring (Green for success/complete, Red for errors/pending, Yellow for warnings). Use formatted strings with fixed widths for the "table" view.
- **Rationale**: Minimal complexity while meeting "Rich console UX" requirements without external dependencies.
- **Alternatives**: `colorama` (optional, but ANSI is standard on modern terminals), `rich` (rejected to maintain "no external libraries" constraint).

### Command Parsing: Split and Switch
- **Decision**: Split user input string and use a `match/case` (Python 3.10+) or `if/elif` block to route to functions.
- **Rationale**: Standard, robust way to handle single-line commands like `add Buy milk`.

### Exit Handling: signal/try-except
- **Decision**: Wrap the main loop in a `try/except KeyboardInterrupt` block.
- **Rationale**: Ensures the application prints a "Goodbye" message and exits status 0 instead of showing a traceback.
