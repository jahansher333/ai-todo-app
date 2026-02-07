# Quickstart Guide: Local Kubernetes Deployment of Todo Chatbot

## Prerequisites

- Docker Desktop with Kubernetes enabled OR Minikube installed and running
- Helm 3.x
- kubectl
- Gordon AI (Docker AI Agent)
- kubectl-ai and kagent
- Access to Neon database (external connection)

## Setup Steps

### 1. Start Minikube Cluster

```bash
minikube start
minikube status
```

### 2. Prepare Docker Images

Using Gordon AI to generate Dockerfiles:

```bash
# For frontend (Next.js app)
cd frontend
gordon ai "generate Dockerfile for Next.js application"
docker build -t todo-frontend:latest .

# For backend (FastAPI + MCP + Agents SDK)
cd ../backend
gordon ai "generate Dockerfile for FastAPI application with MCP and Agents SDK"
docker build -t todo-backend:latest .
```

### 3. Generate Helm Chart

Using kubectl-ai to create Helm chart:

```bash
kubectl-ai "generate Helm chart for Todo backend application"
```

Or using kagent:

```bash
kagent generate helm-chart --name todo-chatbot
```

### 4. Configure Database Connection

Create a ConfigMap with your Neon database connection details:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: db-config
data:
  DATABASE_URL: "your-neon-database-url-here"
```

### 5. Deploy Application

```bash
helm install todo-chatbot ./k8s/helm/todo-chatbot/ \
  --set frontend.image.repository=todo-frontend \
  --set frontend.image.tag=latest \
  --set backend.image.repository=todo-backend \
  --set backend.image.tag=latest
```

### 6. Verify Deployment

```bash
kubectl get pods
kubectl get services
kubectl get ingress  # if using ingress
```

Access the application:

```bash
minikube service todo-frontend-service --url
```

## AI-Assisted Operations

### Generate Additional Resources

```bash
kubectl-ai "create Kubernetes deployment for Next.js frontend"
kubectl-ai "generate service for FastAPI backend with NodePort"
kubectl-ai "create ingress to expose both services"
```

### Scale Application

```bash
kubectl-ai "scale frontend deployment to 3 replicas"
kubectl scale deployment todo-backend --replicas=3
```

### Troubleshoot Issues

```bash
kubectl-ai "show logs for backend pods"
kubectl-ai "check resource usage of frontend pods"
```

## Cleanup

```bash
helm uninstall todo-chatbot
minikube stop
```

## Common Commands

- Check deployment status: `kubectl get all`
- View logs: `kubectl logs deployment/todo-frontend`
- Port forward for testing: `kubectl port-forward svc/todo-frontend-service 3000:80`