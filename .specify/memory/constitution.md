<!--
Sync Impact Report:
- Version change: [INITIAL] → 1.0.0
- List of modified principles: Populated from Hackathon requirements
- Added sections: Core Deliverables, Bonus Points, Phase-specific Constraints
- Removed sections: N/A
- Templates requiring updates:
  - .specify/templates/plan-template.md (✅ updated)
  - .specify/templates/spec-template.md (✅ updated)
  - .specify/templates/tasks-template.md (✅ updated)
- Follow-up TODOs: Initial ratification date unknown, set to current year.
-->

# Evolution of Todo Constitution

## Core Principles

### I. Helpful and Innovative
Deliver a progressive Todo app that evolves from console to distributed AI system, demonstrating AI-native principles. Structure for iterative development, with hands-on examples. Integrate reusable intelligence for smart features like task prioritization.

### II. Honest and Accurate
Base all features on hackathon requirements—no inventing specs or technologies. Cite sources (e.g., Spec-Kit Plus docs, MCP SDK guides). Warn on limitations (e.g., free-tier constraints for Kafka/Neon). Use exact phase deliverables and timelines (e.g., Phase I due Dec 7, 2025).

### III. Harmless and Inclusive
Ensure app accessibility (e.g., multi-language Urdu, voice commands). Promote ethical AI (e.g., unbiased task suggestions). Use free/open-source tiers to minimize barriers.

### IV. Spec-Driven and AI-Native (Spec-Kit Plus Integration)
Begin every phase with Spec-Kit Plus CLI (/sp.specify for user stories, /sp.plan for architecture, /sp.tasks for breakdown, /sp.implement for execution). Generate YAML/JSON specs for features (e.g., Todo CRUD, MCP tools). Leverage Claude Code subagents and skills.

### V. Structured and Comprehensive
Output a monorepo blueprint: hackathon-todo/ with /phase-i/ to /phase-v/, /specs/, frontend/, and backend/. Include Docusaurus docs, FastAPI backend, Next.js frontend, Neon DB, and MCP agents. Ensure assessments for natural language task management.

### VI. Efficient and Scalable
Keep code modular (e.g., stateless MCP tools). Use free tiers (Neon starter, Redpanda Cloud free, DigitalOcean $200 credit). Optimize for deployment via GitHub Actions CI/CD and Helm charts.

### VII. Practical yet Advanced
Infuse AI-native elements like agents for recurring tasks/reminders. Maximize bonus points by integrating subagents/skills for intelligence, cloud-native blueprints via skills, Urdu support, and voice commands.

## Core Deliverables

- **Phase I**: In-memory Python console app (UV, Python 3.13+; basic CRUD: Add/Delete/Update/View/Mark Complete).
- **Phase II**: Full-stack web app (Next.js 16+, FastAPI, SQLModel, Neon DB, Better-Auth with JWT; REST endpoints with user_id filtering).
- **Phase III**: AI chatbot (OpenAI ChatKit UI, Agents SDK, MCP SDK tools; natural language CRUD, stateless with DB history).
- **Phase IV**: Local K8s deploy (Docker, Minikube, Helm charts, kubectl-ai/kagent for ops).
- **Phase V**: Cloud deploy (DigitalOcean DOKS, Dapr for pub/sub/state/jobs, Kafka/Redpanda; CI/CD with GitHub Actions).

## Development Workflow

1. **Clarify and Plan First**: Keep business understanding separate from technical planning. Architecture must be carefully designed before implementation.
2. **Authoritative Source Mandate**: Prioritize MCP tools and CLI commands for information gathering. Never assume solutions from internal knowledge.
3. **Knowledge Capture**: Record every user input verbatim in a Prompt History Record (PHR) after every significant exchange.
4. **Smallest Viable Diff**: Prefer the smallest changes; do not refactor unrelated code.

## Governance

- This constitution supersedes all other practices within the "Evolution of Todo" project.
- Amendments require a version bump (MAJOR.MINOR.PATCH) and a documentation of reasoning.
- All PRs and tasks must be evaluated against these principles. Misalignment requires immediate revision.
- Use CLAUDE.md for project-specific rules and runtime guidance.

**Version**: 1.0.0 | **Ratified**: 2025-12-31 | **Last Amended**: 2025-12-31
