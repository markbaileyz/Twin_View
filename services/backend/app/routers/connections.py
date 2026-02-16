from datetime import datetime, timezone
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/connections", tags=["connections"])

_CONNECTIONS: dict[str, dict] = {}


class VcenterConnectRequest(BaseModel):
    host: str
    username: str
    password: str
    insecure_tls: bool = False
    display_name: str = ""


class SshConnectRequest(BaseModel):
    host: str
    port: int = 22
    username: str
    auth_type: str = "password"
    password: str | None = None
    private_key: str | None = None
    passphrase: str | None = None


@router.get("")
def list_connections():
    return {"connections": list(_CONNECTIONS.values())}


@router.post("/vcenter")
def connect_vcenter(req: VcenterConnectRequest):
    name = req.display_name or f"vcenter:{req.host}"
    _CONNECTIONS[name] = {
        "source_name": name,
        "type": "vcenter",
        "status": "connected",
        "connected_at": datetime.now(timezone.utc).isoformat(),
    }
    return {"status": "connected", "source_name": name}


@router.post("/ssh")
def connect_ssh(req: SshConnectRequest):
    session_id = f"ssh:{req.username}@{req.host}:{req.port}"
    _CONNECTIONS[session_id] = {
        "source_name": session_id,
        "type": "ssh",
        "status": "connected",
        "connected_at": datetime.now(timezone.utc).isoformat(),
    }
    return {"session_id": session_id, "status": "connected"}


@router.delete("/{source_name}")
def disconnect(source_name: str):
    _CONNECTIONS.pop(source_name, None)
    return {"status": "disconnected"}
