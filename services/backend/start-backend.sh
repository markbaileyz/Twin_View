#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
[ -d .venv ] || python3 -m venv .venv
source .venv/bin/activate
if [ ! -f .deps-installed ] || [ requirements.txt -nt .deps-installed ]; then
  pip install -r requirements.txt
  date > .deps-installed
fi
ARGS=""
if [ "${1:-}" = "--reload" ]; then ARGS="--reload"; fi
exec uvicorn app.main:app --host 127.0.0.1 --port 8008 $ARGS
