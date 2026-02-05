import os
import subprocess
from pathlib import Path
from fastapi import FastAPI

from telemetry import setup_tracing
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# 1️⃣ Create app FIRST
app = FastAPI()

# 2️⃣ Setup tracing
setup_tracing("executor-agent")

# 3️⃣ Instrument app
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()

# ENV VARS
ACR_NAME = os.environ["ACR_NAME"]
IMAGE_NAME = os.environ["IMAGE_NAME"]
IMAGE_TAG = os.environ["IMAGE_TAG"]

IMAGE_FULL = f"{ACR_NAME}.azurecr.io/{IMAGE_NAME}:{IMAGE_TAG}"

def run(command: str):
    print(f"[Agent-2] Running: {command}")
    subprocess.check_call(command, shell=True)

@app.post("/execute")
def execute(payload: dict):
    dockerfile_path = Path("../shared/Dockerfile")

    if not dockerfile_path.exists():
        return {"status": "FAILED", "reason": "Dockerfile missing"}

    run(f"docker build -f ../shared/Dockerfile -t {IMAGE_FULL} ..")
    run(f"docker push {IMAGE_FULL}")

    return {
        "task_id": payload.get("task_id"),
        "status": "SUCCESS",
        "image": IMAGE_FULL
    }