@echo off
setlocal
where node >nul 2>nul || (echo Node.js 18+ required & exit /b 1)
where python >nul 2>nul || (echo Python 3.11+ required & exit /b 1)
where pnpm >nul 2>nul || (call npm install -g pnpm)
call pnpm install || exit /b 1
python -m pip install -r services\backend\requirements.txt || exit /b 1
echo Setup complete.
