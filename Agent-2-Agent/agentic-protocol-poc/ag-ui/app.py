from fastapi import FastAPI
from pydantic import BaseModel
import requests
import uuid

from telemetry import setup_tracing
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

app = FastAPI()
setup_tracing("ag-ui")

FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()

#Request schema (AG-UI → Planner)
class TaskRequest(BaseModel):
    task: str
    image_name: str
    image_tag: str

@app.post("/run")
def run_task(req: TaskRequest):
    payload = {
        "task_id": str(uuid.uuid4()),
        "action": "build_and_push",
        "task": req.task,
        "image_name": req.image_name,
        "image_tag": req.image_tag
    }

    # A2A call → Agent-2
    response = requests.post(
        "http://localhost:8001/execute",
        json=payload,
        timeout=300
    )

    return {
        "status": "sent_to_agent2",
        "agent2_response": response.json()
    }