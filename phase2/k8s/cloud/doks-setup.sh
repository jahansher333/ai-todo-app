#!/bin/bash

# DOKS Cluster Setup Script
# This script creates a DOKS cluster and configures kubectl to connect to it

set -e  # Exit immediately if a command exits with a non-zero status

# Configuration variables
CLUSTER_NAME="${CLUSTER_NAME:-todo-cluster}"
REGION="${REGION:-nyc3}"
NODE_SIZE="${NODE_SIZE:-s-2vcpu-4gb}"
NODE_COUNT="${NODE_COUNT:-2}"
MIN_NODES="${MIN_NODES:-2}"
MAX_NODES="${MAX_NODES:-5}"

# Check if doctl is installed
if ! command -v doctl &> /dev/null; then
    echo "Error: doctl is not installed. Please install DigitalOcean CLI first."
    echo "Installation instructions: https://docs.digitalocean.com/reference/doctl/how-to/install/"
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "Error: kubectl is not installed. Please install kubectl first."
    echo "Installation instructions: https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi

# Check if DigitalOcean access token is set
if [ -z "$DIGITALOCEAN_ACCESS_TOKEN" ]; then
    echo "Error: DIGITALOCEAN_ACCESS_TOKEN environment variable is not set."
    echo "Please set your DigitalOcean access token:"
    echo "export DIGITALOCEAN_ACCESS_TOKEN='your_token_here'"
    exit 1
fi

echo "Starting DOKS cluster setup..."
echo "Cluster name: $CLUSTER_NAME"
echo "Region: $REGION"
echo "Node size: $NODE_SIZE"
echo "Initial node count: $NODE_COUNT"
echo "Auto-scaling: $MIN_NODES-$MAX_NODES nodes"

# Create DOKS cluster
echo "Creating DOKS cluster: $CLUSTER_NAME..."
doctl kubernetes cluster create $CLUSTER_NAME \
  --region $REGION \
  --version latest \
  --node-pool "name=default;size=$NODE_SIZE;count=$NODE_COUNT;auto-scale=true;min-nodes=$MIN_NODES;max-nodes=$MAX_NODES"

echo "DOKS cluster $CLUSTER_NAME created successfully."

# Configure kubectl to use the new cluster
echo "Configuring kubectl to use the new cluster..."
doctl kubernetes cluster kubeconfig save $CLUSTER_NAME

echo "Kubeconfig saved for cluster: $CLUSTER_NAME"

# Verify cluster connectivity
echo "Verifying cluster connectivity..."
kubectl cluster-info

# Wait for cluster to be ready
echo "Waiting for cluster to be ready..."
kubectl wait --for=condition=Ready nodes --all --timeout=300s

echo "Cluster is ready!"

# Install Dapr on the cluster
echo "Installing Dapr on the cluster..."
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update
helm install dapr dapr/dapr \
  --namespace dapr-system \
  --create-namespace \
  --wait \
  --version 1.14.0

echo "Dapr installed on the cluster."

# Verify Dapr installation
echo "Waiting for Dapr to be ready..."
kubectl wait --for=condition=Ready pods --namespace dapr-system --all --timeout=300s

echo "Dapr is ready!"

# Set up container registry integration
echo "Setting up DigitalOcean Container Registry integration..."
doctl kubernetes cluster registry add $CLUSTER_NAME --registry-name todo-registry

echo "Container registry integration complete."

# Deploy Dapr components
echo "Deploying Dapr components..."
kubectl apply -f ../dapr/
kubectl wait --for=condition=ready component --all --timeout=300s

# Deploy Redpanda (Kafka replacement)
echo "Deploying Redpanda (Kafka replacement)..."
kubectl create namespace redpanda || true
helm repo add redpanda https://charts.redpanda.com
helm repo update
helm install redpanda redpanda/redpanda \
  --namespace redpanda \
  --set 'console.enabled=false' \
  --set 'auth.sasl.enabled=false' \
  --wait

# Deploy PostgreSQL
echo "Deploying PostgreSQL..."
kubectl create namespace postgresql || true
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install postgresql bitnami/postgresql \
  --namespace postgresql \
  --set 'auth.postgresPassword=secretpassword' \
  --set 'primary.persistence.enabled=false' \
  --wait

# Instructions for next steps
echo ""
echo "=================================="
echo "DOKS Setup Complete!"
echo "=================================="
echo ""
echo "Your cluster is ready. Here are the next steps:"
echo ""
echo "1. Deploy the full application stack:"
echo "   cd ../helm"
echo "   helm dependency update"
echo "   helm install todo-app . --wait"
echo ""
echo "2. Check deployment status:"
echo "   kubectl get pods --all-namespaces"
echo "   kubectl get services --all-namespaces"
echo ""
echo "3. Access the application:"
echo "   kubectl port-forward service/todo-frontend 3000:80 -n default"
echo "   kubectl port-forward service/todo-backend 8000:8000 -n default"
echo ""
echo "Your DOKS cluster '$CLUSTER_NAME' is ready for deployment!"
echo "Dapr, Redpanda (Kafka), and PostgreSQL are installed and configured."