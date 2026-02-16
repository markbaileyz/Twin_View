@echo off
setlocal
start "CCL Backend" cmd /c "cd /d services\backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8008"
for /l %%i in (1,1,30) do (
  curl -sf http://127.0.0.1:8008/health >nul 2>nul && goto :healthy
  timeout /t 1 >nul
)
echo Backend failed to start
exit /b 1
:healthy
call pnpm --filter @ccl/desktop dev
