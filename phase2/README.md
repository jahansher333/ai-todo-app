# Phase V: Advanced Cloud Deployment of Todo Chatbot

This phase implements advanced cloud deployment of the Todo Chatbot application with Dapr, Kafka/Redpanda, PostgreSQL, and automated CI/CD to DigitalOcean Kubernetes (DOKS).

## Architecture Overview

The application consists of:
- **Frontend**: Next.js application with ChatKit UI
- **Backend**: FastAPI application with Dapr integration, MCP and Agents SDK
- **Chatbot**: AI-powered chatbot service with Dapr pub/sub
- **Notification Service**: Event-driven notification service
- **Data Storage**: PostgreSQL for state management
- **Event Streaming**: Redpanda (Kafka-compatible) for pub/sub messaging
- **Orchestration**: Dapr sidecars on all services with Kubernetes and Helm charts
- **CI/CD**: Automated deployment pipeline to DOKS

## Prerequisites

- Docker Desktop (with Gordon AI agent enabled)
- Helm 3.x
- kubectl
- doctl (DigitalOcean CLI)
- kubectl-ai (optional, for AI-assisted operations)
- kagent (optional, for AI-assisted operations)
- DigitalOcean account with API token
- GitHub account for CI/CD

## Setup Instructions

### 1. Local Development Setup (Minikube)

For local development and testing:

```bash
# Start Minikube
minikube start

# Install Dapr locally
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
dapr init --kubernetes --wait

# Deploy Dapr components
kubectl apply -f k8s/dapr/

# Deploy Redpanda (Kafka replacement)
kubectl create namespace redpanda || true
helm repo add redpanda https://charts.redpanda.com
helm repo update
helm install redpanda redpanda/redpanda \
  --namespace redpanda \
  --set 'console.enabled=false' \
  --set 'auth.sasl.enabled=false' \
  --wait

# Deploy PostgreSQL
kubectl create namespace postgresql || true
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install postgresql bitnami/postgresql \
  --namespace postgresql \
  --set 'auth.postgresPassword=secretpassword' \
  --set 'primary.persistence.enabled=false' \
  --wait
```

### 2. Containerize Applications

#### Backend (FastAPI + Dapr + MCP + Agents SDK):
```bash
# Build the backend image:
docker build -f backend/Dockerfile.backend -t todo-backend:latest .

# Test the backend container locally:
docker run -p 8000:8000 todo-backend:latest
```

#### Frontend (Next.js + ChatKit):
```bash
# Build the frontend image:
docker build -f frontend/Dockerfile.frontend -t todo-frontend:latest .

# Test the frontend container locally:
docker run -p 3000:3000 todo-frontend:latest
```

#### Chatbot (AI-powered with Dapr pub/sub):
```bash
# Build the chatbot image:
docker build -f chatbot/Dockerfile.chatbot -t todo-chatbot:latest .

# Test the chatbot container locally:
docker run -p 8001:8001 todo-chatbot:latest
```

### 3. Deploy Full Application Stack with Helm

```bash
# Navigate to the Helm chart directory
cd k8s/helm

# Update dependencies
helm dependency update

# Install the full application stack
helm install todo-app . \
  --set todoBackend.image.repository=todo-backend \
  --set todoBackend.image.tag=latest \
  --set todoFrontend.image.repository=todo-frontend \
  --set todoFrontend.image.tag=latest \
  --set todoChatbot.image.repository=todo-chatbot \
  --set todoChatbot.image.tag=latest \
  --wait
```

### 4. Cloud Deployment (DOKS)

For production deployment to DigitalOcean Kubernetes:

```bash
# Set your DigitalOcean access token
export DIGITALOCEAN_ACCESS_TOKEN="your_do_token_here"

# Run the DOKS setup script
cd k8s/cloud
chmod +x doks-setup.sh
./doks-setup.sh
```

This will:
- Create a DOKS cluster
- Install Dapr on the cluster
- Deploy Redpanda (Kafka replacement)
- Deploy PostgreSQL
- Integrate with DigitalOcean Container Registry

### 5. Access the Application

```bash
# Get the frontend service URL
kubectl get service todo-frontend -n default

# Or port-forward for local access
kubectl port-forward service/todo-frontend 3000:80 -n default
kubectl port-forward service/todo-backend 8000:8000 -n default
kubectl port-forward service/todo-chatbot 8001:8001 -n default
```

## AI-Assisted Operations

### Using kubectl-ai for deployment:
```bash
# Deploy full application stack
kubectl-ai "deploy todo application stack with Dapr sidecars"

# Scale backend if load is high
kubectl-ai "scale backend deployment to 3 replicas if CPU usage is high"

# Analyze cluster health
kubectl-ai "show current cluster status and resource usage"

# Monitor Dapr components
kubectl-ai "show status of all Dapr components"

# Check pub/sub connectivity
kubectl-ai "verify Redpanda and pubsub components are connected"
```

### Using kagent for operations:
```bash
# Analyze cluster health
kagent "analyze cluster health and show pod status"

# Monitor Dapr sidecars
kagent "check status of all Dapr sidecars in the cluster"

# Troubleshoot pub/sub issues
kagent "troubleshoot pubsub connectivity between services"
```

## Gordon AI Fallback Commands

If Gordon AI is not available, use standard Docker and Kubernetes commands:

```bash
# Backend Dockerfile (manual creation)
cat > backend/Dockerfile.backend << EOF
# Multi-stage build for optimized image
FROM python:3.11-slim AS builder
RUN apt-get update && apt-get install -y gcc g++ && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY backend/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.11-slim
RUN apt-get update && apt-get install -y gcc g++ && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
WORKDIR /app
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*
COPY backend/ /app/
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# Frontend Dockerfile (manual creation)
cat > frontend/Dockerfile.frontend << EOF
# Multi-stage build for optimized image
FROM node:18-alpine AS builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci --only=production
COPY frontend/ .
RUN npm run build

FROM node:18-alpine AS runner
RUN apk add --no-cache dumb-init
WORKDIR /app
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./
USER node
EXPOSE 3000
ENTRYPOINT ["dumb-init"]
CMD ["node", "server.js"]
EOF

# Chatbot Dockerfile (manual creation)
cat > chatbot/Dockerfile.chatbot << EOF
# Multi-stage build for optimized image
FROM python:3.11-slim AS builder
RUN apt-get update && apt-get install -y gcc g++ && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY chatbot/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.11-slim
RUN apt-get update && apt-get install -y gcc g++ && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
WORKDIR /app
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*
COPY chatbot/ /app/
EXPOSE 8001
CMD ["uvicorn", "chatbot_app:app", "--host", "0.0.0.0", "--port", "8001"]
EOF
```

## Testing the Deployment

1. Verify all pods are running:
```bash
kubectl get pods --all-namespaces
```

2. Verify services are accessible:
```bash
kubectl get services --all-namespaces
```

3. Verify Dapr components are ready:
```bash
kubectl get components.dapr.io --all-namespaces
```

4. Verify Redpanda (Kafka) is running:
```bash
kubectl get pods -n redpanda
```

5. Verify PostgreSQL is running:
```bash
kubectl get pods -n postgresql
```

6. Test the chatbot functionality:
- Access the frontend URL
- Verify that you can interact with the Todo Chatbot
- Test creating, updating, and deleting todos
- Verify recurring tasks are created via Dapr cron
- Verify reminders are sent via Dapr pub/sub
- Check that events are flowing through Redpanda

## Troubleshooting

### Common Issues:

1. **Images not found**: Make sure to build the Docker images before deploying with Helm
2. **Dapr sidecar injection failures**: Verify Dapr is properly installed and running
3. **Pub/Sub connectivity issues**: Check Redpanda status and Dapr pubsub component configuration
4. **State store failures**: Verify PostgreSQL is running and Dapr state component is configured correctly
5. **Service not accessible**: Check if LoadBalancer is provisioned for external access

### Useful Commands:
```bash
# Check pod logs
kubectl logs -l app.kubernetes.io/name=todo-backend -n default
kubectl logs -l app.kubernetes.io/name=todo-frontend -n default
kubectl logs -l app.kubernetes.io/name=todo-chatbot -n default

# Check Dapr sidecar logs
kubectl logs -l app.kubernetes.io/name=todo-backend -n default -c daprd
kubectl logs -l app.kubernetes.io/name=todo-frontend -n default -c daprd

# Port forward for testing
kubectl port-forward service/todo-backend 8000:8000 -n default
kubectl port-forward service/todo-frontend 3000:80 -n default
kubectl port-forward service/todo-chatbot 8001:8001 -n default

# Check service status
kubectl get all -n default
kubectl get all -n redpanda
kubectl get all -n postgresql

# Check Dapr status
dapr status -k

# Check pubsub connectivity
kubectl exec -it -n dapr-system deployment/dapr-operator -- dapr components -k
```

## CI/CD Pipeline

The GitHub Actions workflow in `.github/workflows/deploy.yaml` provides:

- Automated build and push to DigitalOcean Container Registry
- Deployment to DOKS when changes are pushed to main branch
- Dapr, Redpanda, and PostgreSQL installation on cluster
- Full application stack deployment with Helm

To configure the CI/CD pipeline:

1. Set the following secrets in your GitHub repository:
   - `DIGITALOCEAN_ACCESS_TOKEN`: Your DigitalOcean API token
   - `DOKS_CLUSTER_NAME`: Name of your DOKS cluster

2. The workflow will automatically trigger on pushes to the main branch

## Blueprint Skills

Several blueprint skills are available to assist with development:

1. **Helm Generator Skill**: Generates Helm charts from specifications
2. **Dapr Component Generator Skill**: Creates Dapr component YAML files

These skills are defined in `phase2/.claude/skills/` and can generate complete configurations from feature specifications.

## Development Status

### Phase V: Advanced Cloud Deployment - ✅ COMPLETE

All features implemented and ready for use:

- ✅ **Dapr Integration**: Sidecars on all services with pub/sub and state management
- ✅ **Event Streaming**: Redpanda (Kafka-compatible) for pub/sub messaging
- ✅ **State Management**: PostgreSQL for reliable state storage
- ✅ **Recurring Tasks**: Dapr cron bindings for automated task creation
- ✅ **Reminders**: Event-driven notification system via pub/sub
- ✅ **Cloud Deployment**: Automated CI/CD to DOKS
- ✅ **Helm Charts**: Complete charts for full application stack
- ✅ **Containerization**: Dockerfiles for all services
- ✅ **AI-Assisted Tools**: Integration with kubectl-ai and kagent
- ✅ **Blueprint Skills**: Generator skills for Dapr components and Helm charts
- ✅ **Documentation**: Complete setup and deployment instructions

**Total**: Full event-driven, scalable cloud deployment with automated CI/CD pipeline