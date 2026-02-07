# Data Model: Local Kubernetes Deployment of Todo Chatbot

## Deployment Configuration Entity
- **Name**: Deployment Configuration
- **Fields**:
  - deploymentName: string (name of the Kubernetes deployment)
  - replicas: integer (number of pod replicas to maintain)
  - containerImage: string (Docker image reference)
  - resourceLimits: object (CPU and memory limits)
  - resourceRequests: object (CPU and memory requests)
  - environmentVars: map (environment variables for the container)
  - healthChecks: object (liveness and readiness probe configuration)
- **Relationships**: Belongs to a Namespace entity
- **Validation rules**: Replicas must be >= 1, resource limits must be >= requests
- **State transitions**: Pending → Running → Terminated

## Service Discovery Entity
- **Name**: Service Discovery
- **Fields**:
  - serviceName: string (Kubernetes service name)
  - serviceType: enum (ClusterIP, NodePort, LoadBalancer, ExternalName)
  - portMapping: array (port mappings from external to internal)
  - selector: object (labels to match pods)
  - clusterIp: string (internal cluster IP address)
- **Relationships**: Connects to Deployment Configuration entity
- **Validation rules**: Port numbers must be valid (1-65535), service type must be supported
- **State transitions**: None (configuration-based entity)

## Database Connection Entity
- **Name**: Database Connection
- **Fields**:
  - connectionString: string (full database connection string)
  - host: string (database hostname)
  - port: integer (database port number)
  - databaseName: string (name of the database)
  - username: string (database username)
  - sslEnabled: boolean (whether SSL is required)
  - connectionTimeout: integer (connection timeout in seconds)
- **Relationships**: Referenced by Deployment Configuration entity
- **Validation rules**: Connection string must follow proper format, port must be valid
- **State transitions**: Disconnected → Connecting → Connected → Disconnected

## Kubernetes Namespace Entity
- **Name**: Kubernetes Namespace
- **Fields**:
  - namespaceName: string (unique identifier for the namespace)
  - labels: map (key-value pairs for identification)
  - annotations: map (non-identifying metadata)
  - resourceQuota: object (resource limits for the namespace)
- **Relationships**: Contains multiple Deployment Configuration entities
- **Validation rules**: Namespace name must follow DNS-1123 label standard
- **State transitions**: Active → Terminating

## Helm Values Entity
- **Name**: Helm Values
- **Fields**:
  - imageTag: string (version tag for container images)
  - replicaCount: integer (desired number of pod replicas)
  - serviceType: string (type of Kubernetes service)
  - ingressHost: string (hostname for ingress access)
  - databaseConfig: object (database connection parameters)
  - resources: object (resource limits and requests)
- **Relationships**: Used to configure Helm chart deployment
- **Validation rules**: Values must conform to Helm template expectations
- **State transitions**: None (configuration-based entity)