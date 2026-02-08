# ADR-001: Event-Driven Architecture with Dapr and Kafka

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Proposed
- **Date:** 2026-02-08
- **Feature:** 005-dapr-kafka-cloud-deployment
- **Context:** Phase V requires production-grade cloud deployment with event-driven capabilities for task reminders, real-time notifications, and decoupled service communication.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

We will implement an event-driven architecture using **Dapr (Distributed Application Runtime)** as the sidecar abstraction layer and **Apache Kafka** (via Redpanda for simplified operations) as the message broker.

### Component Stack

- **Dapr Sidecar**: Provides unified APIs for Pub/Sub, State Management, Service Invocation, Bindings, and Secrets
- **Kafka/Redpanda**: Message broker for event streaming with topics: `task-events`, `reminders`, `task-updates`
- **Dapr Pub/Sub Component**: Kafka-backed pub/sub for inter-service event publishing and subscription
- **Dapr State Store**: PostgreSQL for persistent task state with transactional guarantees
- **Dapr Bindings**: Cron-based input bindings for scheduled reminder triggering
- **Dapr Secrets**: Kubernetes secrets integration for sensitive configuration

## Consequences

### Positive

- **Platform Agnostic**: Dapr abstracts infrastructure concerns; services can run on any Kubernetes cluster (DOKS, GKE, AKS) without code changes
- **Reduced Complexity**: Developers interact with simple HTTP/gRPC APIs instead of native Kafka or PostgreSQL drivers
- **Observability Built-in**: Dapr provides distributed tracing, metrics, and logging out of the box
- **Resilience**: Automatic retries, circuit breaking, and timeout policies via Dapr sidecars
- **Local/Prod Parity**: Same Dapr components work in local Minikube and production environments
- **Language Agnostic**: Services can be written in any language; Dapr provides consistent APIs via sidecar
- **Event Sourcing Ready**: Kafka's log-based retention enables replay and audit capabilities

### Negative

- **Operational Complexity**: Running Dapr + Kafka adds infrastructure overhead compared to direct database access
- **Learning Curve**: Team must learn Dapr concepts (components, bindings, pub/sub) in addition to Kubernetes
- **Resource Overhead**: Every pod runs a Dapr sidecar container (additional memory/CPU per instance)
- **Debugging Complexity**: Distributed tracing required to troubleshoot across sidecars and services
- **Kafka Management**: Even with Redpanda simplification, topic management and consumer group tuning required
- **Cold Start Latency**: Dapr sidecar initialization adds startup time to pods

## Alternatives Considered

### Alternative A: Direct Service Communication with REST APIs

- **Approach**: Services call each other directly via HTTP/REST with load balancers
- **Why Rejected**: Tight coupling between services; no event history or replay; difficult to add new consumers without modifying producers; retry logic must be implemented in each service

### Alternative B: RabbitMQ with Custom Abstraction Layer

- **Approach**: Use RabbitMQ as message broker with custom Python/Node.js abstraction library
- **Why Rejected**: Reinventing Dapr's value proposition; no built-in observability; team must maintain custom abstraction; fewer managed service options compared to Kafka

### Alternative C: AWS EventBridge + Lambda (Cloud-Locked)

- **Approach**: Use AWS-native event bus and serverless functions
- **Why Rejected**: Vendor lock-in to AWS prevents multi-cloud or on-premise deployment; violates requirement for DigitalOcean/GCP/Azure compatibility

### Alternative D: NATS Streaming (now JetStream)

- **Approach**: Use NATS with JetStream for persistence
- **Why Rejected**: Smaller ecosystem compared to Kafka; fewer managed service providers; less mature tooling for operations and monitoring

## References

- Feature Spec: `specs/005-dapr-kafka-cloud-deployment/spec.md`
- Implementation Plan: `specs/005-dapr-kafka-cloud-deployment/plan.md` (to be created)
- Related ADRs: None yet
- Evaluator Evidence: Feature specification quality checklist passed; decision significance confirmed
