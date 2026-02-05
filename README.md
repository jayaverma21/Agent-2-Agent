# Agent-2-Agent
Linkdin post- https://www.linkedin.com/posts/saurabh-vartak-8448a7a_microsoftaitour-microsoftagentframework-activity-7405267032239464448-6tCJ?utm_source=share&utm_medium=member_desktop&rcm=ACoAAERHeLcBY_xVb1v3w6iW6KKzfhkepx9IHzA

# Agentic AI Protocols Implementation on Azure (MCP + A2A + AG-UI)

This repository provides a complete implementation of an Agentic AI workflow using MCP tool server, multi-agent execution (A2A), AG-UI trigger layer, deployed on Azure AKS with OpenTelemetry tracing.

---

# ✅ PHASE 0 — VM Setup & Prerequisites

Run on your Linux VM:

```bash
docker --version
az version
python3 --version
git --version

sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
newgrp docker
✅ PHASE 1 — Create Azure Container Registry (ACR)
az acr create \
  --resource-group jaya-rg-agentic-protocol \
  --name acragentt \
  --sku Basic
Login:

az acr login --name acragentt
✅ PHASE 2 — Project Structure
agentic-docker-poc/
├── mcp-server/              # MCP Tool Backend
├── dockerfile-agent/        # Agent-1 Planner
├── build-push-agent/        # Agent-2 Executor
├── ag-ui/                   # User Trigger Layer
├── shared/                  # Shared Dockerfile output
└── telemetry.py             # OpenTelemetry tracing
✅ PHASE 3 — MCP Tool Server (FastAPI)
MCP server exposes tools like health check + server logs.

Step 3.1 Setup
cd mcp-server
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn
Step 3.2 Run MCP Server
uvicorn app:app --host 0.0.0.0 --port 9000
Step 3.3 Verify Tool Discovery
curl http://localhost:9000/mcp/tools
✅ PHASE 4 — Agent-1 (Planner Agent)
Agent-1 generates Dockerfile using Azure OpenAI.

Step 4.1 Setup
cd dockerfile-agent
python3 -m venv venv
source venv/bin/activate

pip install openai azure-identity python-dotenv
Step 4.2 Azure OpenAI Environment Variables
export AZURE_OPENAI_API_KEY="YOUR_KEY"
export AZURE_OPENAI_ENDPOINT="https://YOUR-RESOURCE.openai.azure.com/"
export AZURE_OPENAI_DEPLOYMENT="agent-gpt4o"
Step 4.3 Run Agent-1
python app.py
Output:

Dockerfile saved into:

shared/Dockerfile
✅ PHASE 5 — Agent-2 (Executor Agent)
Agent-2 builds Docker image and pushes to Azure Container Registry.

Step 5.1 Setup
cd build-push-agent
python3 -m venv venv
source venv/bin/activate

pip install python-dotenv
Step 5.2 Set ACR Variables
export ACR_NAME=acragentt
export IMAGE_NAME=agent-runner
export IMAGE_TAG=v1
Step 5.3 Run Executor Agent
python app.py
Expected:

Docker image built

Image pushed to ACR

✅ PHASE 6 — AG-UI Layer (User Trigger)
AG-UI provides Swagger UI for running agent workflows.

Step 6.1 Setup
cd ag-ui
python3 -m venv venv
source venv/bin/activate

pip install fastapi uvicorn requests
Step 6.2 Run AG-UI Server
uvicorn app:app --host 0.0.0.0 --port 7000
Open:

http://<VM-IP>:7000/docs
Step 6.3 Trigger Workflow
POST /run

{
  "task": "Build docker image and push to ACR",
  "image_name": "agent-runner",
  "image_tag": "v2"
}
✅ PHASE 7 — OpenTelemetry Distributed Tracing
Tracing enabled across AG-UI + Agent-2.

Step 7.1 Install Dependencies (All Services)
pip install \
 opentelemetry-api \
 opentelemetry-sdk \
 opentelemetry-instrumentation-fastapi \
 opentelemetry-instrumentation-requests \
 opentelemetry-exporter-otlp
Step 7.2 Run Jaeger (Trace UI)
docker run -d --name jaeger \
  -e COLLECTOR_OTLP_ENABLED=true \
  -p 16686:16686 \
  -p 4318:4318 \
  jaegertracing/all-in-one:latest
Open Jaeger UI:

http://<VM-IP>:16686
Expected Trace Flow:

AG-UI → Executor Agent → Docker Build → Push → Response
✅ PHASE 8 — Containerize Agents
Agent-2 Docker Image
cd build-push-agent

docker build -t acragentt.azurecr.io/agent2-executor:v1 .
docker push acragentt.azurecr.io/agent2-executor:v1
Agent-1 Docker Image
cd dockerfile-agent

docker build -t acragentt.azurecr.io/agent1-planner:v1 .
docker push acragentt.azurecr.io/agent1-planner:v1
✅ PHASE 9 — Deploy on Azure Kubernetes Service (AKS)
Step 9.1 Attach ACR
az aks update \
  --resource-group jaya-rg-agentic-protocol \
  --name agentic-aks \
  --attach-acr acragentt
Step 9.2 Get Cluster Credentials
az aks get-credentials \
  --resource-group jaya-rg-agentic-protocol \
  --name agentic-aks
Step 9.3 Create Namespace
kubectl create namespace agentic
✅ PHASE 10 — AKS YAML Deployments
Jaeger Deployment (jaeger.yaml)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jaeger
  namespace: agentic
spec:
  replicas: 1
  selector:
    matchLabels:
      app: jaeger
  template:
    metadata:
      labels:
        app: jaeger
    spec:
      containers:
      - name: jaeger
        image: jaegertracing/all-in-one:latest
        ports:
        - containerPort: 16686
        - containerPort: 4318
        env:
        - name: COLLECTOR_OTLP_ENABLED
          value: "true"
---
apiVersion: v1
kind: Service
metadata:
  name: jaeger
  namespace: agentic
spec:
  type: LoadBalancer
  selector:
    app: jaeger
  ports:
  - port: 16686
    targetPort: 16686
Apply:

kubectl apply -f jaeger.yaml
Agent-2 Executor (agent2.yaml)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent2-executor
  namespace: agentic
spec:
  replicas: 1
  selector:
    matchLabels:
      app: agent2
  template:
    metadata:
      labels:
        app: agent2
    spec:
      containers:
      - name: agent2
        image: acragentt.azurecr.io/agent2-executor:v1
        ports:
        - containerPort: 8001
---
apiVersion: v1
kind: Service
metadata:
  name: agent2-service
  namespace: agentic
spec:
  selector:
    app: agent2
  ports:
  - port: 8001
    targetPort: 8001
Apply:

kubectl apply -f agent2.yaml
Agent-1 Planner (agent1.yaml)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent1-planner
  namespace: agentic
spec:
  replicas: 1
  selector:
    matchLabels:
      app: agent1
  template:
    metadata:
      labels:
        app: agent1
    spec:
      containers:
      - name: agent1
        image: acragentt.azurecr.io/agent1-planner:v1
        env:
        - name: EXECUTOR_URL
          value: "http://agent2-service:8001/execute"
Apply:

kubectl apply -f agent1.yaml
✅ PHASE 11 — End-to-End Test on AKS
Verify Pods
kubectl get pods -n agentic
kubectl get svc -n agentic
Check Logs
kubectl logs deployment/agent1-planner -n agentic
kubectl logs deployment/agent2-executor -n agentic
Trigger Workflow
curl -X POST http://<AGUI-IP>:7000/run \
  -H "Content-Type: application/json" \
  -d '{
    "task":"Build docker image and push to ACR",
    "image_name":"agent-runner",
    "image_tag":"v1"
  }'
View Trace in Jaeger
Open:

http://<Jaeger-LB-IP>:16686
Trace should show:

AG-UI → Agent-2 → Docker Build → Docker Push
✅ Completed End-to-End
✔ MCP Tool Server
✔ Agent-1 Planner
✔ Agent-2 Executor
✔ AG-UI Trigger Layer
✔ OpenTelemetry Tracing
✔ Jaeger Observability
✔ Containerization
✔ AKS Deployment
✔ End-to-End Test Success
