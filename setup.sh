#!/usr/bin/env bash
set -euo pipefail

if ! command -v node >/dev/null 2>&1; then
  echo "Node.js is required (>=18)."; exit 1
fi
if ! command -v pnpm >/dev/null 2>&1; then
  npm install -g pnpm
fi
PYTHON_BIN=""
if command -v python3 >/dev/null 2>&1; then PYTHON_BIN=python3; elif command -v python >/dev/null 2>&1; then PYTHON_BIN=python; else echo "Python 3.11+ required"; exit 1; fi

pnpm install
cd services/backend
[ -d .venv ] || "$PYTHON_BIN" -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd - >/dev/null

echo "Setup complete. Run ./start.sh"
