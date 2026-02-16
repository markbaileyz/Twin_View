from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from app.db.engine import engine
from app.db.models import Base
from app.routers import clusters, connections, demo, drift, events, health, inventory, llm, rvtools
from app.ws.broadcaster import telemetry_broadcaster

APP_VERSION = "0.1.0"


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="CCL_TwinView", version=APP_VERSION, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:\\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(events.router)
app.include_router(clusters.router)
app.include_router(demo.router)
app.include_router(llm.router)
app.include_router(connections.router)
app.include_router(drift.router)
app.include_router(rvtools.router)
app.include_router(inventory.router)


@app.websocket('/ws/telemetry')
async def ws_telemetry(ws: WebSocket):
    await telemetry_broadcaster.subscribe(ws)
