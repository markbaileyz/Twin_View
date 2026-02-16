# CCL_TwinView

CCL_TwinView is an Electron + React + FastAPI desktop workspace for VMware operations telemetry, clustering, drift visibility, and RVTools analysis.

## Quick start

```bash
pnpm install
bash services/backend/start-backend.sh --reload
pnpm --filter @ccl/desktop dev
```

Backend: `http://127.0.0.1:8008`  
Telemetry WS: `ws://127.0.0.1:8008/ws/telemetry`
