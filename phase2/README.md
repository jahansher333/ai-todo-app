# Phase IV: Local Kubernetes Deployment of Todo Chatbot

This phase implements containerization and deployment of the Todo Chatbot application on a local Kubernetes cluster using Minikube.

## Architecture Overview

The application consists of:
- **Frontend**: Next.js application with ChatKit UI
- **Backend**: FastAPI application with MCP and Agents SDK
- **Database**: External Neon database connection
- **Orchestration**: Kubernetes with Helm charts

## Prerequisites

- Docker Desktop (with Gordon AI agent enabled)
- Minikube
- Helm 3.x
- kubectl
- kubectl-ai (optional, for AI-assisted operations)
- kagent (optional, for AI-assisted operations)

## Setup Instructions

### 1. Start Minikube

```bash
minikube start
```

### 2. Containerize Applications

#### Backend (FastAPI + MCP + Agents SDK):
```bash
# If Gordon AI is available:
gordon ai "generate Dockerfile for FastAPI Todo app with MCP and Agents SDK"
# Or use the provided Dockerfile in k8s/docker/backend/Dockerfile

# Build the backend image:
docker build -f k8s/docker/backend/Dockerfile -t todo-backend:latest .

# Test the backend container locally:
docker run -p 8000:8000 todo-backend:latest
```

#### Frontend (Next.js + ChatKit):
```bash
# If Gordon AI is available:
gordon ai "generate Dockerfile for Next.js ChatKit app"
# Or use the provided Dockerfile in k8s/docker/frontend/Dockerfile

# Build the frontend image:
docker build -f k8s/docker/frontend/Dockerfile -t todo-frontend:latest .

# Test the frontend container locally:
docker run -p 3000:3000 todo-frontend:latest
```

### 3. Configure Database Connection

Set up your Neon database connection and update the configmap with your DATABASE_URL:

```bash
# Edit the configmap with your actual database URL
kubectl create configmap todo-app-config --from-literal=DATABASE_URL="your-neon-database-url" --dry-run=client -o yaml | kubectl apply -f -
```

### 4. Deploy with Helm

#### Backend Deployment:
```bash
# Navigate to the backend Helm chart directory
cd k8s/helm/todo-backend

# Install the backend chart
helm install todo-backend . --set image.repository=todo-backend --set image.tag=latest
```

#### Frontend Deployment:
```bash
# Navigate to the frontend Helm chart directory
cd k8s/helm/todo-frontend

# Install the frontend chart
helm install todo-frontend . --set image.repository=todo-frontend --set image.tag=latest --set backend.apiUrl=http://todo-backend:8000
```

### 5. Alternative: Deploy Both with Helm

```bash
# From the phase2 directory
helm install todo-app k8s/helm/todo-backend --set image.repository=todo-backend --set image.tag=latest
helm install todo-ui k8s/helm/todo-frontend --set image.repository=todo-frontend --set image.tag=latest --set backend.apiUrl=http://todo-app:8000
```

### 6. Access the Application

```bash
# Get the frontend service URL
minikube service frontend --url -n todo-chatbot

# Or use minikube tunnel for external access (in a separate terminal)
minikube tunnel
```

## AI-Assisted Operations

### Using kubectl-ai for deployment:
```bash
# Deploy frontend with 2 replicas
kubectl-ai "deploy frontend with 2 replicas"

# Scale backend if load is high
kubectl-ai "scale backend deployment to 3 replicas if CPU usage is high"

# Analyze cluster health
kubectl-ai "show current cluster status and resource usage"
```

### Using kagent for operations:
```bash
# Analyze cluster health
kagent "analyze cluster health"
```

## Gordon AI Fallback Commands

If Gordon AI is not available, use standard Docker commands:

```bash
# Backend Dockerfile (manual creation)
cat > k8s/docker/backend/Dockerfile << EOF
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
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# Frontend Dockerfile (manual creation)
cat > k8s/docker/frontend/Dockerfile << EOF
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
```

## Testing the Deployment

1. Verify all pods are running:
```bash
kubectl get pods -n todo-chatbot
```

2. Verify services are accessible:
```bash
kubectl get services -n todo-chatbot
```

3. Test the chatbot functionality:
- Access the frontend URL
- Verify that you can interact with the Todo Chatbot
- Test creating, updating, and deleting todos
- Verify data persists in the Neon database

## Troubleshooting

### Common Issues:

1. **Images not found**: Make sure to build the Docker images before deploying with Helm
2. **Database connection failures**: Verify the DATABASE_URL in the ConfigMap
3. **Service not accessible**: Check if Minikube tunnel is running for external access

### Useful Commands:
```bash
# Check pod logs
kubectl logs -l app.kubernetes.io/name=todo-backend -n todo-chatbot
kubectl logs -l app.kubernetes.io/name=todo-frontend -n todo-chatbot

# Port forward for testing
kubectl port-forward svc/backend -n todo-chatbot 8000:8000
kubectl port-forward svc/frontend -n todo-chatbot 3000:3000

# Check service status
kubectl get all -n todo-chatbot
```

## Blueprint Skill Usage

The Helm Generator skill can be used to generate Helm charts from specifications:

```yaml
# Example usage of the HelmGeneratorSkill
skill: "helm-generator"
params:
  specification: "FastAPI backend with 2 replicas"
  chart_name: "todo-backend"
  image_repository: "todo-backend"
  replicas: 2
```

This skill is defined in `phase2/.claude/skills/helm-generator.yaml` and can generate complete Helm charts from feature specifications.

## Development Status

### Phase IV: Local Kubernetes Deployment - ✅ COMPLETE

All features implemented and ready for use:

- ✅ **Containerization**: Dockerfiles for both frontend and backend applications
- ✅ **Helm Charts**: Complete Helm charts for both frontend and backend
- ✅ **Kubernetes Deployment**: Deployable on local Minikube cluster
- ✅ **AI-Assisted Tools**: Integration with Gordon AI, kubectl-ai, and kagent
- ✅ **Database Connection**: ConfigMap for Neon database connection
- ✅ **Blueprint Skill**: HelmGeneratorSkill for generating YAML from specs
- ✅ **Documentation**: Complete setup and deployment instructions

**Total**: Full containerization, orchestration, and deployment pipeline established for local Kubernetes environment