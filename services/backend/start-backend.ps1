param(
  [switch]$Reload
)

$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

if (!(Test-Path .deps-installed) -or ((Get-Item requirements.txt).LastWriteTime -gt (Get-Item .deps-installed).LastWriteTime)) {
  python -m pip install -r requirements.txt
  Get-Date | Out-File .deps-installed -Encoding utf8
}

if ($Reload) {
  python -m uvicorn app.main:app --host 127.0.0.1 --port 8008 --reload
} else {
  python -m uvicorn app.main:app --host 127.0.0.1 --port 8008
}
