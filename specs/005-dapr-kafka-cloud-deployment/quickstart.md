# Quickstart Guide: Phase V - Dapr + Kafka Deployment

**Feature**: 005-dapr-kafka-cloud-deployment
**Prerequisites**: Docker, kubectl, Helm, Dapr CLI

---

## Local Development (Minikube)

### 1. Start Minikube

```bash
# Start with sufficient resources for Dapr + Kafka
minikube start --cpus=4 --memory=8192 --driver=docker

# Enable ingress addon
minikube addons enable ingress
```

### 2. Install Dapr on Kubernetes

```bash
# Initialize Dapr with specific runtime version
dapr init -k --runtime-version 1.14.0

# Verify installation
kubectl get pods -n dapr-system
```

### 3. Deploy Redpanda (Kafka-compatible)

```bash
# Add Redpanda Helm repo
helm repo add redpanda https://charts.redpanda.com/
helm repo update

# Install single-node Redpanda for development
helm install redpanda redpanda/redpanda \
  --namespace redpanda \
  --create-namespace \
  --set statefulset.replicas=1 \
  --set resources.memory.container=1Gi \
  --set resources.memory.redpanda=800Mi

# Wait for Redpanda to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=redpanda -n redpanda --timeout=300s

# Port-forward for local access
kubectl port-forward svc/redpanda 9092:9092 -n redpanda
```

### 4. Configure Dapr Components

Create Dapr component configurations in `k8s/cloud/dapr-components/`:

```bash
# Apply all Dapr components
kubectl apply -f k8s/cloud/dapr-components/
```

**pubsub-kafka.yaml**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: task-pubsub
  namespace: default
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "redpanda.redpanda.svc.cluster.local:9092"
  - name: consumerGroup
    value: "task-consumers"
  - name: authType
    value: "none"
  - name: disableTls
    value: "true"
```

**state-postgres.yaml**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: task-state
  namespace: default
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    secretKeyRef:
      name: neon-db-secret
      key: connection-string
```

**binding-cron.yaml**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: recurring-task-cron
  namespace: default
spec:
  type: bindings.cron
  version: v1
  metadata:
  - name: schedule
    value: "0 */6 * * *"  # Every 6 hours
```

### 5. Build and Deploy Application

```bash
# Build Docker image in Minikube context
eval $(minikube docker-env)
docker build -t todo-backend:local ./backend

# Deploy application with Helm
helm upgrade --install todo-app ./k8s/cloud/helm \
  --namespace default \
  --set backend.image.repository=todo-backend \
  --set backend.image.tag=local \
  --set backend.replicaCount=1

# Verify deployment
kubectl get pods -l app=todo-backend
kubectl logs -l app=todo-backend -c todo-backend
kubectl logs -l app=todo-backend -c daprd  # Dapr sidecar logs
```

### 6. Access the Application

```bash
# Port-forward to access locally
kubectl port-forward svc/todo-backend 8000:8000

# Test the API
curl http://localhost:8000/health
```

---

## Production Deployment (DigitalOcean DOKS)

### 1. Create DOKS Cluster

```bash
# Via doctl CLI
doctl kubernetes cluster create todo-cluster \
  --region nyc3 \
  --version 1.29 \
  --node-pool "name=worker-pool;size=s-2vcpu-4gb;count=2;auto-scale=true;min-nodes=2;max-nodes=5"

# Save kubeconfig
doctl kubernetes cluster kubeconfig save todo-cluster
```

### 2. Install Dapr on DOKS

```bash
dapr init -k --runtime-version 1.14.0

# Verify
kubectl get pods -n dapr-system
```

### 3. Set Up Container Registry

```bash
# Create DO Container Registry
doctl registry create todo-registry

# Connect registry to cluster
doctl kubernetes cluster registry add todo-cluster todo-registry
```

### 4. Configure Secrets

```bash
# Create Neon PostgreSQL secret
kubectl create secret generic neon-db-secret \
  --from-literal=connection-string="postgresql://user:pass@neon-host/db"

# Create Redpanda Cloud credentials (if using managed)
kubectl create secret generic redpanda-secret \
  --from-literal=bootstrap-servers="your-cluster.redpanda.cloud:9092" \
  --from-literal=username="user" \
  --from-literal=password="pass"
```

### 5. Deploy Redpanda or Connect to Redpanda Cloud

**Option A: Redpanda Cloud (Recommended)**
- Create serverless cluster at https://cloud.redpanda.com/
- Update pubsub component with Cloud brokers and SASL auth

**Option B: Self-hosted in DOKS**:
```bash
helm install redpanda redpanda/redpanda \
  --namespace redpanda \
  --create-namespace \
  --set statefulset.replicas=3 \
  --set storage.persistentVolume.size=10Gi
```

### 6. Deploy via GitHub Actions

Ensure repository secrets are set:
- `DIGITALOCEAN_ACCESS_TOKEN`
- `NEON_DB_CONNECTION_STRING`
- `REDPANDA_BOOTSTRAP_SERVERS`
- `REDPANDA_USERNAME`
- `REDPANDA_PASSWORD`

Push to `main` branch triggers deployment:

```bash
git push origin main
```

Monitor in GitHub Actions tab.

---

## Troubleshooting

### Dapr Sidecar Not Starting

```bash
# Check Dapr system pods
kubectl get pods -n dapr-system
kubectl logs -n dapr-system -l app=dapr-operator

# Check component status
kubectl get components
kubectl describe component task-pubsub
```

### Kafka Connection Issues

```bash
# Test Redpanda connectivity
kubectl run -it --rm debug --image=vectorized/redpanda:latest \
  -- rpk cluster info --brokers redpanda.redpanda.svc.cluster.local:9092

# Check topic creation
kubectl exec -it redpanda-0 -n redpanda -- \
  rpk topic list --brokers localhost:9092
```

### Application Logs

```bash
# View application logs
kubectl logs -l app=todo-backend -c todo-backend --tail=100 -f

# View Dapr sidecar logs
kubectl logs -l app=todo-backend -c daprd --tail=100 -f
```

### Reset Local Environment

```bash
# Delete and recreate
minikube delete
minikube start --cpus=4 --memory=8192
dapr init -k

# Re-deploy
helm upgrade --install redpanda redpanda/redpanda --namespace redpanda --create-namespace
kubectl apply -f k8s/cloud/dapr-components/
helm upgrade --install todo-app ./k8s/cloud/helm
```

---

## Monitoring with kagent

### Install kagent

```bash
brew install kagent-dev/kagent/kagent
```

### Run Interactive Agent

```bash
# Run against your cluster
kagent run

# Example queries:
# "Why is my pod crashing?"
# "Show me the logs for the todo-backend pod"
# "What events are happening in the default namespace?"
```

---

## Next Steps

1. **Verify Event Flow**: Create a task and check that events appear in Redpanda topics
2. **Test Recurring Tasks**: Create a recurring task and verify cron binding triggers
3. **Set Up Reminders**: Create a reminder and verify Dapr Jobs trigger correctly
4. **Configure Webhooks**: Set up webhook endpoint and verify event delivery
5. **Add Monitoring**: Deploy Prometheus/Grafana or configure kagent alerts

