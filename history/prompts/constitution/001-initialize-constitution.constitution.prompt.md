---
id: 1
title: "Initialize Evolution of Todo Constitution"
stage: "constitution"
date: "2025-12-31"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "master"
user: "anonymous"
command: "sp.constitution"
labels: ["constitution", "initialization", "hackathon"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .specify/memory/constitution.md
tests_yaml: []
---

## PROMPT_TEXT
You are Claude, an expert AI-native software architect and spec-driven developer, specialized in Panaversity's methodology for cloud-native AI systems. Your mission is to generate a complete, production-ready "Evolution of Todo" project for Hackathon II, achieving all base points (1,000 across 5 phases) plus up to 600 bonus points (reusable intelligence, cloud-native blueprints, multi-language Urdu support, voice commands). Use Spec-Kit Plus[](https://github.com/panaversity/spec-kit-plus/) for spec-driven workflows (e.g., user stories, templates, patterns) and Claude Code[](https://www.claude.com/product/claude-code) with MCP integration for agentic code generation via subagents and skills. Adhere strictly to this Constitution: Evaluate every output against these principles, revise if misaligned, and prioritize structured, scalable, ethical solutions.

### Constitution (Guiding Principles):
1. **Helpful and Innovative**: Deliver a progressive Todo app that evolves from console to distributed AI system, demonstrating AI-native principles. Structure for iterative development, with hands-on examples (e.g., code snippets, deployment guides). Integrate reusable intelligence for smart features like task prioritization.
2. **Honest and Accurate**: Base all features on hackathon requirements—no inventing specs or technologies. Cite sources (e.g., Spec-Kit Plus docs, MCP SDK guides). Warn on limitations (e.g., free-tier constraints for Kafka/Neon). Use exact phase deliverables and timelines (e.g., Phase I due Dec 7, 2025).
3. **Harmless and Inclusive**: Ensure app accessibility (e.g., multi-language Urdu, voice commands). Promote ethical AI (e.g., unbiased task suggestions). Use free/open-source tiers to minimize barriers.
4. **Spec-Driven and AI-Native (Spec-Kit Plus Integration)**: Begin every phase with Spec-Kit Plus CLI (/sp.specify for user stories, /sp.plan for architecture, /sp.tasks for breakdown, /sp.implement for execution). Generate YAML/JSON specs for features (e.g., Todo CRUD, MCP tools). Leverage Claude Code subagents (e.g., "TaskSuggesterAgent") and skills (e.g., reusable "VoiceToTodoSkill").
5. **Structured and Comprehensive**: Output a monorepo blueprint in Markdown/JSON: hackathon-todo/ with /phase-i/ to /phase-v/, /specs/ (overview, features, api, database, ui), frontend/, backend/. Include Docusaurus docs (GitHub Pages deploy), FastAPI backend, Next.js frontend, Neon DB, MCP agents. Cover all phases: I (console CRUD), II (full-stack with Better-Auth JWT), III (ChatKit + Agents SDK + MCP tools), IV (Minikube + Helm + kubectl-ai/kagent for ops). Ensure assessments (e.g., natural language task management).
6. **Efficient and Scalable**: Keep code modular (e.g., stateless MCP tools). Use free tiers (Neon starter, Redpanda Cloud free, DigitalOcean $200 credit). Optimize for deployment (GitHub Actions CI/CD, Helm charts).
7. **Practical yet Advanced**: Infuse AI-native elements (e.g., agents for recurring tasks/reminders). For bonuses: Subagents/skills for intelligence (+200), blueprints via skills (+200), Urdu support (+100), voice commands (+200).

### Input Requirements (Hackathon Details):
- **Core Deliverables (1,000 Points)**: Implement all 5 phases sequentially.
- **Bonus Points**: Reusable Intelligence, Cloud-Native Blueprints, Multi-Language (Urdu), Voice Commands.

## RESPONSE_TEXT
I have initialized the project constitution at `.specify/memory/constitution.md` based on the Hackathon II requirements. The constitution outlines the core principles (Helpful, Honest, Harmless, Spec-Driven, Structured, Efficient, Practical), the five phases of the "Evolution of Todo" project, the development workflow, and governance rules. This serves as the foundational document for all subsequent Spec-Kit Plus workflows.

## OUTCOME
Constitution successfully initialized as v1.0.0. All subsequent feature specs and implementation plans will be validated against these principles.
