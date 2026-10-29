# run_all.ps1
# This script starts the GlobalEstate AI stack (backend + frontend) and ensures the model is trained.
# Run it from PowerShell:  ./run_all.ps1

$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$frontendDir = Join-Path $projectRoot 'frontend'
$backendDir   = $projectRoot

# ------------------------------------------------------------
# 1️⃣ Install frontend dependencies (npm ci) if needed
# ------------------------------------------------------------
Write-Host '=== Installing frontend dependencies ==='
Push-Location $frontendDir
if (-not (Test-Path 'node_modules')) {
    npm ci
} else {
    Write-Host 'node_modules already present – skipping install.'
}
Pop-Location

# ------------------------------------------------------------
# 2️⃣ Train Spark model if metadata is missing
# ------------------------------------------------------------
$metadataPath = Join-Path $backendDir 'backend\models\usa_california_lr_metadata.json'
if (-not (Test-Path $metadataPath)) {
    Write-Host '=== Model metadata not found – training Spark model ==='
    Push-Location $backendDir
    python "backend\scripts\train_model.py" --force
    Pop-Location
} else {
    Write-Host 'Model already trained – metadata file exists.'
}

# ------------------------------------------------------------
# 3️⃣ Start FastAPI backend (uvicorn)
# ------------------------------------------------------------
Write-Host '=== Starting FastAPI backend on http://0.0.0.0:8000 ==='
Start-Process -FilePath 'python' -ArgumentList '-m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload' -WorkingDirectory $backendDir -NoNewWindow
# Give the server a moment to bind the port
Start-Sleep -Seconds 5

# ------------------------------------------------------------
# 4️⃣ Start Next.js development server
# ------------------------------------------------------------
Write-Host '=== Starting Next.js dev server on http://localhost:3000 ==='
Start-Process -FilePath 'cmd.exe' -ArgumentList "/c", "npm run dev" -WorkingDirectory $frontendDir -NoNewWindow

Write-Host "All services are up. Open http://localhost:3000 in your browser to view the app."

