import json
from fastapi import WebSocket


class Broadcaster:
    def __init__(self) -> None:
        self._subscribers: set[WebSocket] = set()

    async def subscribe(self, ws: WebSocket) -> None:
        await ws.accept()
        self._subscribers.add(ws)
        try:
            while True:
                await ws.receive_text()
        except Exception:
            self._subscribers.discard(ws)

    async def broadcast(self, message: dict) -> None:
        payload = json.dumps(message, default=str)
        dead = []
        for ws in self._subscribers:
            try:
                await ws.send_text(payload)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self._subscribers.discard(ws)


telemetry_broadcaster = Broadcaster()
