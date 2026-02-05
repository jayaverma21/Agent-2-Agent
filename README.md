# Agent-2-Agent 🤖 (MCP + A2A + AG-UI)

📌 Reference LinkedIn Post:  
https://www.linkedin.com/posts/saurabh-vartak-8448a7a_microsoftaitour-microsoftagentframework-activity-7405267032239464448-6tCJ

---

# Agentic AI Protocols Implementation on Azure (MCP + A2A + AG-UI)

This repository provides a complete implementation of an **Agentic AI workflow** using:

- **MCP Tool Server**
- **Multi-Agent Execution (A2A)**
- **AG-UI Trigger Layer**
- Deployment on **Azure Kubernetes Service (AKS)**
- **OpenTelemetry Distributed Tracing + Jaeger Observability**

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture Workflow](#architecture-workflow)
- [Phase 0 — VM Setup](#phase-0--vm-setup--prerequisites)
- [Phase 1 — Create Azure Container Registry](#phase-1--create-azure-container-registry-acr)
- [Phase 2 — Project Structure](#phase-2--project-structure)
- [Phase 3 — MCP Tool Server](#phase-3--mcp-tool-server-fastapi)
- [Phase 4 — Agent-1 Planner](#phase-4--agent-1-planner-agent)
- [Phase 5 — Agent-2 Executor](#phase-5--agent-2-executor-agent)
- [Phase 6 — AG-UI Trigger Layer](#phase-6--ag-ui-layer-user-trigger)
- [Phase 7 — OpenTelemetry Tracing](#phase-7--opentelemetry-distributed-tracing)
- [Phase 8 — Containerize Agents](#phase-8--containerize-agents)
- [Phase 9 — Deploy on AKS](#phase-9--deploy-on-azure-kubernetes-service-aks)
- [Phase 10 — Kubernetes YAML Deployments](#phase-10--aks-yaml-deployments)
- [Phase 11 — End-to-End Test](#phase-11--end-to-end-test-on-aks)
- [Completion Checklist](#completed-end-to-end)

---

## 🎯 Overview

This project demonstrates a full **Agentic AI Protocol Pipeline** deployed on Azure.

It integrates:

- **MCP (Model Context Protocol)** for tool discovery  
- **A2A (Agent-to-Agent execution)** for multi-agent orchestration  
- **AG-UI (Trigger Layer)** for user-driven workflow execution  
- **OpenTelemetry + Jaeger** for distributed observability  

This repo is a complete template for building production-ready multi-agent systems on AKS.

---

## 🏗 Architecture Workflow

```
User → AG-UI Trigger Layer
          ↓
   Agent-1 Planner (Azure OpenAI)
          ↓
   Agent-2 Executor (Docker Build + Push)
          ↓
     Azure Container Registry (ACR)
          ↓
   Observability via Jaeger Tracing
```

---

### PHASE 0 — VM Setup & Prerequisites

Run the following commands on your Linux VM:

```bash
docker --version
az version
python3 --version
git --version
```

Install Docker:

```bash
sudo apt update
sudo apt install -y docker.io

sudo systemctl start docker
sudo systemctl enable docker

sudo usermod -aG docker $USER
newgrp docker
```

---

## ✅ PHASE 1 — Create Azure Container Registry (ACR)

Create ACR:

```bash
az acr create   --resource-group jaya-rg-agentic-protocol   --name acragentt   --sku Basic
```

### Login

```bash
az acr login --name acragentt
```

---

## ✅ PHASE 2 — Project Structure

```
agentic-docker-poc/
├── mcp-server/              # MCP Tool Backend
├── dockerfile-agent/        # Agent-1 Planner
├── build-push-agent/        # Agent-2 Executor
├── ag-ui/                   # User Trigger Layer
├── shared/                  # Shared Dockerfile output
└── telemetry.py             # OpenTelemetry tracing
```

---

## ✅ PHASE 3 — MCP Tool Server (FastAPI)

### Step 3.1 Setup

```bash
cd mcp-server
python3 -m venv venv
source venv/bin/activate

pip install fastapi uvicorn
```

### Step 3.2 Run MCP Server

```bash
uvicorn app:app --host 0.0.0.0 --port 9000
```

### Step 3.3 Verify Tool Discovery

```bash
curl http://localhost:9000/mcp/tools
```

---

## ✅ PHASE 4 — Agent-1 (Planner Agent)

### Step 4.1 Setup

```bash
cd dockerfile-agent
python3 -m venv venv
source venv/bin/activate

pip install openai azure-identity python-dotenv
```

### Step 4.2 Azure OpenAI Variables

```bash
export AZURE_OPENAI_API_KEY="YOUR_KEY"
export AZURE_OPENAI_ENDPOINT="https://YOUR-RESOURCE.openai.azure.com/"
export AZURE_OPENAI_DEPLOYMENT="agent-gpt4o"
```

### Step 4.3 Run Planner

```bash
python app.py
```

Dockerfile saved into:

```
shared/Dockerfile
```

---

## ✅ PHASE 5 — Agent-2 (Executor Agent)

### Step 5.1 Setup

```bash
cd build-push-agent
python3 -m venv venv
source venv/bin/activate

pip install python-dotenv
```

### Step 5.2 Set ACR Variables

```bash
export ACR_NAME=acragentt
export IMAGE_NAME=agent-runner
export IMAGE_TAG=v1
```

### Step 5.3 Run Executor

```bash
python app.py
```

Expected:

- Docker image built  
- Image pushed to ACR  

---

## ✅ PHASE 6 — AG-UI Layer (User Trigger)

### Step 6.1 Setup

```bash
cd ag-ui
python3 -m venv venv
source venv/bin/activate

pip install fastapi uvicorn requests
```

### Step 6.2 Run AG-UI

```bash
uvicorn app:app --host 0.0.0.0 --port 7000
```

Swagger UI:

```
http://<VM-IP>:7000/docs
```

### Step 6.3 Trigger Workflow

POST `/run`

```json
{
  "task": "Build docker image and push to ACR",
  "image_name": "agent-runner",
  "image_tag": "v2"
}
```

---

## ✅ PHASE 7 — OpenTelemetry Distributed Tracing

### Step 7.1 Install Dependencies

```bash
pip install  opentelemetry-api  opentelemetry-sdk  opentelemetry-instrumentation-fastapi  opentelemetry-instrumentation-requests  opentelemetry-exporter-otlp
```

### Step 7.2 Run Jaeger

```bash
docker run -d --name jaeger   -e COLLECTOR_OTLP_ENABLED=true   -p 16686:16686   -p 4318:4318   jaegertracing/all-in-one:latest
```

Jaeger UI:

```
http://<VM-IP>:16686
```

---

## ✅ PHASE 8 — Containerize Agents

### Agent-2

```bash
docker build -t acragentt.azurecr.io/agent2-executor:v1 .
docker push acragentt.azurecr.io/agent2-executor:v1
```

### Agent-1

```bash
docker build -t acragentt.azurecr.io/agent1-planner:v1 .
docker push acragentt.azurecr.io/agent1-planner:v1
```

---

## ✅ PHASE 9 — Deploy on AKS

Attach ACR:

```bash
az aks update   --resource-group jaya-rg-agentic-protocol   --name agentic-aks   --attach-acr acragentt
```

Get Credentials:

```bash
az aks get-credentials   --resource-group jaya-rg-agentic-protocol   --name agentic-aks
```

Namespace:

```bash
kubectl create namespace agentic
```

---

## ✅ PHASE 10 — AKS YAML Deployments

```bash
kubectl apply -f jaeger.yaml
kubectl apply -f agent2.yaml
kubectl apply -f agent1.yaml
```

---

## ✅ PHASE 11 — End-to-End Test on AKS

Check Pods:

```bash
kubectl get pods -n agentic
kubectl get svc -n agentic
```

Trigger Workflow:

```bash
curl -X POST http://<AGUI-IP>:7000/run   -H "Content-Type: application/json"   -d '{
    "task":"Build docker image and push to ACR",
    "image_name":"agent-runner",
    "image_tag":"v1"
  }'
```

---

# ✅ Completed End-to-End

✔ MCP Tool Server  
✔ Agent-1 Planner  
✔ Agent-2 Executor  
✔ AG-UI Trigger Layer  
✔ OpenTelemetry Tracing  
✔ Jaeger Observability  
✔ Containerization  
✔ AKS Deployment  
✔ End-to-End Workflow Success  
