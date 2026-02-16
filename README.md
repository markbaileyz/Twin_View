# CCL_TwinView

CCL_TwinView is an Electron + React + FastAPI desktop workspace for VMware operations telemetry, clustering, drift visibility, and RVTools analysis.

## What is implemented now

- FastAPI backend with persistent SQLite models for events/clusters/drift/rvtools.
- Live telemetry pipeline (normalize -> cluster -> websocket broadcast) and demo event generator.
- API surface for health, events, clusters, demo, llm, connections, drift, rvtools, inventory.
- Electron + Vite + React desktop shell with 3-zone layout and singleton stores.
- Cross-platform setup and start scripts (`setup.sh`, `start.sh`, `setup.bat`, `start.bat`).

## Quick start (macOS/Linux)

```bash
./setup.sh
./start.sh
```

## Quick start (Windows)

```bat
setup.bat
start.bat
```

Backend: `http://127.0.0.1:8008`  
Telemetry WS: `ws://127.0.0.1:8008/ws/telemetry`

## Windows startup diagnostics

`start.bat` now writes timestamped logs under `logs/`:

- `startup-YYYYMMDD-HHMMSS.log` and `startup-latest.log`
- `backend-YYYYMMDD-HHMMSS.log` and `backend-latest.log`
- `electron-YYYYMMDD-HHMMSS.log` and `electron-latest.log`

If startup fails, check `startup-latest.log` first; it includes health-check progress, backend PID, and recent backend log tail.
