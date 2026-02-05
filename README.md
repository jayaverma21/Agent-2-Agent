# Agent-2-Agent
Linkdin post- https://www.linkedin.com/posts/saurabh-vartak-8448a7a_microsoftaitour-microsoftagentframework-activity-7405267032239464448-6tCJ?utm_source=share&utm_medium=member_desktop&rcm=ACoAAERHeLcBY_xVb1v3w6iW6KKzfhkepx9IHzA


# Agentic AI Protocols on Azure (MCP + A2A + AG-UI)

This repository demonstrates an **end-to-end Agentic AI Proof-of-Concept** using three key open protocols:

- **Model Context Protocol (MCP)**  
- **Agent-to-Agent Protocol (A2A)**  
- **Agent User Interface Protocol (AG-UI)**  

Implemented following **Microsoft Agent Framework principles**, deployed on **Azure Kubernetes Service (AKS)**, with full observability using **OpenTelemetry + Jaeger / Application Insights**.

---

## 🚀 Project Objective

Traditional LLM applications face challenges like:

- Custom tool integrations for each model  
- Lack of multi-agent orchestration standards  
- No consistent UI interaction layer  
- Limited production observability  

This project solves it using:

✅ MCP for structured tool context  
✅ A2A for agent collaboration  
✅ AG-UI for user execution control  
✅ AKS for scalable deployment  
✅ OpenTelemetry for full traceability  

---

## 🧩 Key Protocols

---

### 1️⃣ Model Context Protocol (MCP)

MCP is an open standard that allows AI models to connect with external tools and data sources securely.

**Responsibilities:**

- Tool discovery  
- Context filtering  
- Structured tool outputs  
- Secure access control  

Example:

User:  
> "DB server ke alawa saare VMs band kar do"

MCP server exposes only:

- VM list excluding DB VM  
- Required metadata  

So the model receives only minimal + relevant context.

---

### 2️⃣ Agent-to-Agent Protocol (A2A)

A2A enables multiple AI agents to collaborate without custom bridges.

In this PoC:

- Agent-1 (Planner) generates Dockerfile  
- Agent-2 (Executor) builds + pushes image to ACR  

---

### 3️⃣ Agent User Interface Protocol (AG-UI)

AG-UI standardizes interaction between user and agents.

In this project:

- Implemented using FastAPI Swagger UI  
- Users trigger workflows via `/run`

---

## 🏗 Architecture Flow

```text
User
 ↓ (AG-UI)
FastAPI UI Layer
 ↓
Planner Agent (Agent-1)
 ↓ (A2A call)
Executor Agent (Agent-2)
 ↓
Docker Build + Push → Azure Container Registry
 ↓
Traces Exported via OpenTelemetry
 ↓
Jaeger / Application Insights
