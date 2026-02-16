from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/llm", tags=["llm"])


class ChatRequest(BaseModel):
    message: str
    context_window_minutes: int = 15


class SummaryRequest(BaseModel):
    context_window_minutes: int = 15


@router.get('/status')
def status():
    return {"ollama_available": False, "model": "mistral", "models_available": []}


@router.post('/chat')
def chat(req: ChatRequest):
    return {
        "reply": "Not enough data in current telemetry to answer that question.",
        "citations": [],
        "ollama_available": False,
    }


@router.post('/summary')
def summary(req: SummaryRequest):
    return {
        "summary": "Not enough data in current telemetry.",
        "cluster_ids": [],
        "ollama_available": False,
    }
