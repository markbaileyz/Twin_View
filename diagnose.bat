@echo off
setlocal
where node >nul 2>nul && node --version || echo [WARN] node missing
where python >nul 2>nul && python --version || echo [WARN] python missing
where pnpm >nul 2>nul && pnpm --version || echo [WARN] pnpm missing
if exist services\backend\app\main.py (echo [OK] backend app present) else echo [FAIL] backend app missing
python -c "from app.main import app; print(app.title)" 2>nul && echo [OK] backend import || echo [WARN] backend import failed
