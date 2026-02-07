# Research: Phase II - Todo Full-Stack Web Application

## Technology Stack Decisions

### Frontend Framework: Next.js 16+ with App Router

**Decision**: Use Next.js 16+ with App Router for the frontend
**Rationale**: Next.js provides excellent developer experience, built-in optimizations, and supports both static generation and server-side rendering. The App Router offers better organization for complex applications. Supports the required monorepo structure.
**Alternatives considered**:
- React with Create React App: Less optimized, lacks built-in routing
- Remix: Good but smaller community than Next.js
- Vue/Nuxt: Different ecosystem, Next.js has better integration with backend APIs

### Backend Framework: FastAPI

**Decision**: Use FastAPI for the backend API
**Rationale**: FastAPI offers automatic API documentation, type hints, async support, and high performance. It integrates well with Pydantic for data validation. Perfect for implementing JWT middleware with token verification and user_id extraction.
**Alternatives considered**:
- Flask: More manual work for documentation and validation
- Django: Overkill for this application, heavier framework
- Express.js: Node.js alternative but staying with Python ecosystem

### Database ORM: SQLModel

**Decision**: Use SQLModel for database modeling
**Rationale**: SQLModel combines SQLAlchemy and Pydantic, offering both ORM capabilities and data validation in one package. Created by the same author as FastAPI for seamless integration. Ideal for Neon PostgreSQL connection.
**Alternatives considered**:
- Pure SQLAlchemy: More verbose, separate validation layer needed
- Tortoise ORM: Async native but less mature
- Peewee: Simpler but less powerful than SQLModel

### Authentication: Better-Auth

**Decision**: Use Better-Auth for authentication
**Rationale**: Better-Auth provides easy JWT token handling, session management, and integrates well with Next.js applications. It handles common authentication patterns securely. Supports shared BETTER_AUTH_SECRET for both frontend and backend.
**Alternatives considered**:
- Custom JWT implementation: More work, potential security issues
- Auth0/Supabase: External dependency, vendor lock-in
- NextAuth.js: More suited for Next.js only, less backend integration

### Database: Neon PostgreSQL

**Decision**: Use Neon PostgreSQL for data storage
**Rationale**: Neon provides serverless PostgreSQL with branching capabilities, automatic scaling, and good performance. It's compatible with standard PostgreSQL. Perfect for implementing the required tasks table with user_id foreign key.
**Alternatives considered**:
- SQLite: Simpler but not suitable for multi-user production
- PostgreSQL on bare metal: More complex setup and maintenance
- MongoDB: NoSQL approach but relational model fits better for this use case

### UI Styling: Tailwind CSS

**Decision**: Use Tailwind CSS for styling
**Rationale**: Tailwind provides utility-first approach that works well with React/Next.js, enabling rapid UI development and consistent design. Supports responsive design requirements.
**Alternatives considered**:
- Styled-components: More flexible but requires more setup
- Material UI: Opinionated design system, less customization
- Vanilla CSS: More verbose, less maintainable

### Internationalization: i18next

**Decision**: Use i18next for multi-language support including Urdu
**Rationale**: i18next is well-established internationalization framework that works seamlessly with Next.js. Supports the constitution requirement for Urdu language support.
**Alternatives considered**:
- Next.js built-in i18n: Limited compared to i18next
- FormatJS: Good alternative but i18next has better Next.js integration

### Accessibility: Voice Command Support

**Decision**: Implement voice command functionality using Web Speech API
**Rationale**: Web Speech API provides native browser support for speech recognition and synthesis. Aligns with constitution requirement for accessibility features.
**Alternatives considered**:
- Third-party libraries: More complex setup
- Custom speech recognition: Higher complexity and maintenance

## Architecture Patterns

### API Design

**Decision**: RESTful API with user-specific endpoints at /api/{user_id}/tasks
**Rationale**: REST is well-understood, widely supported, and fits the CRUD operations of the todo app. The user_id in the path ensures clear ownership separation. All endpoints will enforce user_id ownership with 401 responses for mismatches.
**Alternatives considered**:
- GraphQL: More flexible but adds complexity for simple CRUD
- RPC-style: Less standardized approach

### Frontend State Management

**Decision**: Use React state management with custom hooks for API interactions
**Rationale**: For this application size, React's built-in state management with custom hooks is sufficient and avoids the complexity of Redux or Zustand.
**Alternatives considered**:
- Redux: More complex for this use case
- Zustand: Good alternative but React state is sufficient here

### Task Organization Views

**Decision**: Implement both Kanban and List views
**Rationale**: Kanban provides visual organization familiar to Jira users, while List view offers dense information display for power users. Both views will support drag-and-drop functionality.
**Alternatives considered**:
- Calendar view: Could be added later as an extension
- Gantt chart: Too complex for initial implementation

### Security Implementation

**Decision**: JWT middleware to verify tokens, extract user_id, and return 401 for invalid/missing tokens
**Rationale**: This approach ensures all API endpoints properly validate authentication and enforce user isolation. Critical for security requirements.
**Alternatives considered**:
- Session-based authentication: Less suitable for API
- OAuth-only: More complex than needed for this application