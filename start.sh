#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$ROOT_DIR/services/backend"

cleanup() {
  if [ -n "${BACKEND_PID:-}" ] && kill -0 "$BACKEND_PID" >/dev/null 2>&1; then
    kill "$BACKEND_PID" || true
  fi
}
trap cleanup EXIT

cd "$BACKEND_DIR"
[ -d .venv ] || python3 -m venv .venv
source .venv/bin/activate
if [ ! -f .deps-installed ] || [ requirements.txt -nt .deps-installed ]; then
  pip install -r requirements.txt
  date > .deps-installed
fi
uvicorn app.main:app --host 127.0.0.1 --port 8008 &
BACKEND_PID=$!

cd "$ROOT_DIR"
for _ in $(seq 1 30); do
  if curl -sf http://127.0.0.1:8008/health >/dev/null; then
    break
  fi
  sleep 1
done

pnpm --filter @ccl/desktop dev
