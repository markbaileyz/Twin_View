@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "ROOT_DIR=%~dp0"
if "%ROOT_DIR:~-1%"=="\" set "ROOT_DIR=%ROOT_DIR:~0,-1%"
set "LOG_DIR=%ROOT_DIR%\logs"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd-HHmmss"') do set "RUN_TS=%%i"
if not defined RUN_TS set "RUN_TS=latest"

set "STARTUP_LOG=%LOG_DIR%\startup-%RUN_TS%.log"
set "STARTUP_LATEST=%LOG_DIR%\startup-latest.log"
set "BACKEND_LOG=%LOG_DIR%\backend-%RUN_TS%.log"
set "BACKEND_LATEST=%LOG_DIR%\backend-latest.log"
set "ELECTRON_LOG=%LOG_DIR%\electron-%RUN_TS%.log"
set "ELECTRON_LATEST=%LOG_DIR%\electron-latest.log"
set "HEALTH_BODY=%LOG_DIR%\health-%RUN_TS%.json"

break > "%STARTUP_LOG%"
copy /Y "%STARTUP_LOG%" "%STARTUP_LATEST%" >nul
break > "%BACKEND_LOG%"
copy /Y "%BACKEND_LOG%" "%BACKEND_LATEST%" >nul
break > "%ELECTRON_LOG%"
copy /Y "%ELECTRON_LOG%" "%ELECTRON_LATEST%" >nul

call :log "=== CCL_TwinView startup begin ==="
call :log "root=%ROOT_DIR%"
call :log "startup_log=%STARTUP_LOG%"
call :log "backend_log=%BACKEND_LOG%"
call :log "electron_log=%ELECTRON_LOG%"

call :preflight || goto :fail
call :check_port
call :start_backend || goto :fail
call :wait_health || goto :fail
call :start_electron
set "ELECTRON_EXIT=%ERRORLEVEL%"
call :log "Electron exited with code %ELECTRON_EXIT%"

if not "%BACKEND_PID%"=="" (
  call :log "Stopping backend PID %BACKEND_PID%"
  taskkill /PID %BACKEND_PID% /T /F >> "%STARTUP_LOG%" 2>&1
)

if "%ELECTRON_EXIT%"=="0" (
  call :log "=== Startup finished successfully ==="
  exit /b 0
)

goto :fail

:preflight
call :log "Running preflight checks"
for %%c in (node python pnpm) do (
  where %%c >nul 2>nul
  if errorlevel 1 (
    call :log "[ERROR] Missing dependency: %%c"
    exit /b 1
  )
)
for %%c in (node python pnpm) do (
  for /f "delims=" %%v in ('%%c --version 2^>^&1') do call :log "%%c %%v"
)
where curl >nul 2>nul
if errorlevel 1 call :log "[WARN] curl not found; health check will use PowerShell fallback"

if not exist "%ROOT_DIR%\services\backend\app\main.py" (
  call :log "[ERROR] Backend app entry missing: services\\backend\\app\\main.py"
  exit /b 1
)
if not exist "%ROOT_DIR%\apps\desktop\package.json" (
  call :log "[ERROR] Desktop package missing: apps\\desktop\\package.json"
  exit /b 1
)
if not exist "%ROOT_DIR%\node_modules" (
  call :log "node_modules missing; running pnpm install"
  pushd "%ROOT_DIR%"
  call pnpm install >> "%STARTUP_LOG%" 2>&1
  if errorlevel 1 (
    popd
    call :log "[ERROR] pnpm install failed"
    exit /b 1
  )
  popd
)
exit /b 0

:check_port
for /f "tokens=5" %%p in ('netstat -ano ^| findstr /R /C:":8008 .*LISTENING"') do (
  call :log "[WARN] Port 8008 already in use by PID %%p"
)
exit /b 0

:start_backend
call :log "Starting backend process"
for /f %%p in ('powershell -NoProfile -Command "$wd='%ROOT_DIR%\services\backend'; $log='%BACKEND_LOG%'; $p=Start-Process cmd -ArgumentList ('/c cd /d \"' + $wd + '\" ^&^& python -m uvicorn app.main:app --host 127.0.0.1 --port 8008 ^>^> \"' + $log + '\" 2^>^&1') -WindowStyle Minimized -PassThru; $p.Id"') do set "BACKEND_PID=%%p"
if "%BACKEND_PID%"=="" (
  call :log "[ERROR] Failed to obtain backend PID"
  exit /b 1
)
call :log "Backend PID=%BACKEND_PID%"
exit /b 0

:wait_health
call :log "Waiting for backend health endpoint"
set /a ATTEMPT=0
:health_loop
set /a ATTEMPT+=1
set "HTTP_CODE="
where curl >nul 2>nul
if errorlevel 1 (
  for /f %%h in ('powershell -NoProfile -Command "try { (Invoke-WebRequest -Uri http://127.0.0.1:8008/health -UseBasicParsing -TimeoutSec 2).StatusCode } catch { 0 }"') do set "HTTP_CODE=%%h"
) else (
  curl -sS -o "%HEALTH_BODY%" -w "%%{http_code}" http://127.0.0.1:8008/health > "%LOG_DIR%\health-code.tmp" 2>> "%STARTUP_LOG%"
  set /p HTTP_CODE=<"%LOG_DIR%\health-code.tmp"
)
if "%HTTP_CODE%"=="200" (
  call :log "Health check passed on attempt !ATTEMPT!"
  del "%LOG_DIR%\health-code.tmp" >nul 2>nul
  if exist "%HEALTH_BODY%" (
    type "%HEALTH_BODY%" >> "%STARTUP_LOG%"
    echo.>> "%STARTUP_LOG%"
  )
  exit /b 0
)
if !ATTEMPT! GEQ 30 (
  call :log "[ERROR] Health check failed after !ATTEMPT! attempts (last code=%HTTP_CODE%)"
  call :log "Recent backend log tail:"
  powershell -NoProfile -Command "Get-Content -Path '%BACKEND_LOG%' -Tail 60" >> "%STARTUP_LOG%" 2>&1
  del "%LOG_DIR%\health-code.tmp" >nul 2>nul
  exit /b 1
)
if !ATTEMPT! EQU 5 call :log "Still waiting for backend health... (5s)"
if !ATTEMPT! EQU 15 call :log "Still waiting for backend health... (15s)"
if !ATTEMPT! EQU 25 call :log "Still waiting for backend health... (25s)"
timeout /t 1 >nul
goto :health_loop

:start_electron
call :log "Starting Electron dev process"
pushd "%ROOT_DIR%"
call pnpm --filter @ccl/desktop dev >> "%ELECTRON_LOG%" 2>&1
set "EC=%ERRORLEVEL%"
popd
copy /Y "%ELECTRON_LOG%" "%ELECTRON_LATEST%" >nul
exit /b %EC%

:fail
call :log "=== Startup failed ==="
call :log "See logs:"
call :log "  %STARTUP_LOG%"
call :log "  %BACKEND_LOG%"
call :log "  %ELECTRON_LOG%"
if not "%BACKEND_PID%"=="" taskkill /PID %BACKEND_PID% /T /F >nul 2>nul
echo.
echo Startup failed. Review:
echo   %STARTUP_LOG%
echo   %BACKEND_LOG%
echo   %ELECTRON_LOG%
exit /b 1

:log
echo [%date% %time%] %~1
echo [%date% %time%] %~1>> "%STARTUP_LOG%"
copy /Y "%STARTUP_LOG%" "%STARTUP_LATEST%" >nul
exit /b 0
