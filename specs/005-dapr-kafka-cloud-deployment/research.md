# Research: Phase V - Dapr + Kafka Event-Driven Architecture

**Feature**: 005-dapr-kafka-cloud-deployment
**Date**: 2026-02-08
**Researcher**: Claude Code Agent

---

## Research Questions

1. How to configure Dapr Pub/Sub with Redpanda/Kafka for task events?
2. How to implement recurring tasks using Dapr Bindings vs Dapr Jobs?
3. How to set up Dapr State Store with Neon PostgreSQL?
4. What is the optimal local development setup (Minikube + Dapr + Redpanda)?
5. How to structure GitHub Actions CI/CD for DOKS deployment?

---

## Findings

### 1. Dapr Pub/Sub with Kafka/Redpanda

**Decision**: Use Dapr's Kafka pub/sub component with Redpanda (API-compatible)

**Configuration**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: task-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "redpanda:9092"
  - name: consumerGroup
    value: "task-consumers"
  - name: authType
    value: "none"  # For local; use TLS for production
```

**Topics**:
- `task-events`: Task lifecycle events (create, update, delete, complete)
- `reminders`: Reminder trigger events for scheduled notifications
- `task-updates`: Real-time update notifications for UI

**Rationale**: Redpanda is Kafka API-compatible but easier to run locally and on managed Kubernetes. Dapr abstracts the producer/consumer code, allowing services to use simple HTTP POST to publish and subscribe via webhook endpoints.

---

### 2. Recurring Tasks: Dapr Bindings vs Jobs

**Decision**: Use Dapr Cron Input Bindings for recurring task generation

**Binding Configuration**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: recurring-task-cron
spec:
  type: bindings.cron
  version: v1
  metadata:
  - name: schedule
    value: "0 */6 * * *"  # Every 6 hours - check for recurring tasks
```

**Alternative Considered**: Dapr Jobs API (v1.14+)
- Jobs API is newer and designed specifically for scheduled tasks
- However, Bindings have broader documentation and community examples
- Bindings work well for "check and generate" pattern for recurring tasks

**Implementation Pattern**:
1. Cron binding triggers `/generate-recurring-tasks` endpoint every 6 hours
2. Service queries PostgreSQL for recurring tasks due for next occurrence
3. New task instances created via Dapr state store API
4. Events published to `task-events` topic

---

### 3. Reminders: Dapr Jobs API

**Decision**: Use Dapr Jobs API for reminder scheduling

**Job Configuration**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: reminder-jobs
spec:
  type: jobs.http
  version: v1
```

**Implementation Pattern**:
1. When user sets a reminder, schedule Dapr Job with trigger time
2. Job invokes `/send-reminder` endpoint with task ID
3. Service fetches task, sends notification via webhook/email
4. Job automatically deleted after execution (one-time) or rescheduled (recurring)

**Rationale**: Jobs API provides precise scheduling with at-least-once execution guarantees, better suited for reminder delivery than cron bindings which are time-interval based.

---

### 4. Dapr State Store with PostgreSQL

**Decision**: Use Neon PostgreSQL via Dapr PostgreSQL State Store component

**Configuration**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: task-state
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    secretKeyRef:
      name: neon-db-secret
      key: connection-string
```

**Benefits**:
- Dapr handles connection pooling and retries
- Transactions supported across multiple state operations
- Built-in TTL for temporary state (useful for session data)
- Neon serverless PostgreSQL scales to zero when not in use

---

### 5. Local Development Setup

**Stack**: Minikube + Dapr + Redpanda (Docker Compose or Helm)

**Setup Steps**:
1. Start Minikube: `minikube start --cpus=4 --memory=8192`
2. Install Dapr on K8s: `dapr init -k`
3. Deploy Redpanda (single node for dev):
   ```bash
   helm repo add redpanda https://charts.redpanda.com/
   helm install redpanda redpanda/redpanda \
     --set statefulset.replicas=1 \
     --set resources.memory.container=1Gi
   ```
4. Apply Dapr components (pubsub, state store, bindings)
5. Deploy application with `dapr.io/enabled: "true"` annotation

**Alternative**: Redpanda in Docker Compose alongside Minikube
- Simpler for initial development
- Use `host.minikube.internal` to connect from K8s to local Redpanda

---

### 6. CI/CD Pipeline (GitHub Actions → DOKS)

**Pipeline Structure**:
```yaml
# .github/workflows/deploy.yml
name: Deploy to DOKS
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and push images
        run: |
          docker build -t registry.digitalocean.com/todo/backend:${{ github.sha }} .
          docker push registry.digitalocean.com/todo/backend:${{ github.sha }}
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install doctl
        uses: digitalocean/action-doctl@v2
        with:
          token: ${{ secrets.DIGITALOCEAN_ACCESS_TOKEN }}
      - name: Deploy to DOKS
        run: |
          doctl kubernetes cluster kubeconfig save todo-cluster
          helm upgrade --install todo-app ./k8s/cloud/helm \
            --set backend.image.tag=${{ github.sha }}
```

**DOKS Setup**:
1. Create cluster via DO UI or doctl
2. Install Dapr: `dapr init -k --runtime-version 1.14.0`
3. Configure container registry integration
4. Set up secrets for Neon DB connection string

---

### 7. Monitoring with kubectl-ai/kagent

**Decision**: Use kubectl-ai (now kagent) for cluster insights

**Setup**:
```bash
# Install kagent CLI
brew install kagent-dev/kagent/kagent

# Run interactive agent
kagent run
```

**Capabilities**:
- Natural language queries: "Why is my pod crashing?"
- Automated troubleshooting and log analysis
- Integration with Prometheus metrics

**Fallback**: Basic Prometheus + Grafana via kube-prometheus-stack Helm chart if kagent insufficient.

---

## Decisions Summary

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Message Broker | Redpanda (Kafka API) | Simpler ops than Kafka, compatible with Dapr Kafka pubsub |
| Event Bus | Dapr Pub/Sub | Abstracts Kafka complexity, supports multiple backends |
| Recurring Tasks | Dapr Cron Bindings | Proven pattern, good for batch generation |
| Reminders | Dapr Jobs API | Precise scheduling, at-least-once execution |
| State Store | Neon PostgreSQL | Serverless, scales to zero, Dapr native support |
| Local Dev | Minikube + Dapr + Redpanda | Matches production architecture |
| Cloud | DOKS + Dapr + Redpanda Cloud | Managed K8s, free Redpanda tier |
| CI/CD | GitHub Actions → DO | Native integration, free tier sufficient |
| Monitoring | kagent + Prometheus | AI-assisted ops, standard metrics |

---

## Open Questions (Resolved)

**Q**: Should we use Redpanda Cloud or self-hosted Strimzi?
**A**: Use Redpanda Cloud serverless for production (free tier: 5GB storage, 100MB/s throughput) - sufficient for initial launch. Strimzi adds operational complexity.

**Q**: How to handle reminder timezone issues?
**A**: Store all times in UTC, convert to user timezone at display time. Dapr Jobs accept ISO8601 timestamps with timezone.

**Q**: What happens if reminder job fails?
**A**: Dapr Jobs provide at-least-once execution with configurable retry policy. Failed jobs logged to app logs for kagent/Prometheus alerting.

---

## References

- Dapr Pub/Sub Kafka: https://docs.dapr.io/reference/components-reference/supported-pubsub/setup-apache-kafka/
- Dapr Cron Bindings: https://docs.dapr.io/reference/components-reference/supported-bindings/cron/
- Dapr Jobs API: https://docs.dapr.io/reference/api/jobs_api/
- Redpanda Helm Chart: https://docs.redpanda.com/current/deploy/deployment-option/self-hosted/kubernetes/get-started-dev/
- kagent: https://github.com/kagent-dev/kagent
- Neon Serverless Postgres: https://neon.tech/

