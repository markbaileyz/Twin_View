from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0", "uptime_seconds": 0, "db_ok": True, "ollama": {"available": False, "models": [], "error": None}}
