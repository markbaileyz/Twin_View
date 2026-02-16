import time
from fastapi import APIRouter

APP_START_TS = time.time()
router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    return {
        "status": "ok",
        "version": "0.1.0",
        "uptime_seconds": int(time.time() - APP_START_TS),
        "db_ok": True,
        "ollama": {"available": False, "models": [], "error": None},
    }
