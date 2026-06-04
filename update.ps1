#Requires -Version 5.1
# =============================================================================
#  SMRITI RETAIL OS - Windows Updater
#  Usage:  .\update.ps1
# =============================================================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

# -- Colour helpers ------------------------------------------------------------
function Write-Header  { param($msg) Write-Host "`n================================================" -ForegroundColor Cyan
                                     Write-Host   "  $msg" -ForegroundColor Cyan
                                     Write-Host   "================================================`n" -ForegroundColor Cyan }
function Write-Step    { param($msg) Write-Host "  -> $msg" -ForegroundColor Yellow }
function Write-OK      { param($msg) Write-Host "  [OK] $msg" -ForegroundColor Green }
function Write-Warn    { param($msg) Write-Host "  [!!] $msg" -ForegroundColor DarkYellow }
function Write-Fail    { param($msg) Write-Host "  [XX] $msg" -ForegroundColor Red; exit 1 }
function Write-Banner  {
    Write-Host "================================================" -ForegroundColor Magenta
    Write-Host "      SMRITI RETAIL OS - UPDATER v1.0.0         " -ForegroundColor Magenta
    Write-Host "================================================" -ForegroundColor Magenta
}

$COMPOSE_FILE = "pwd.yml"
$SITE_NAME = "smriti_retail"

Write-Banner

# PHASE 1 - PRE-FLIGHT
Write-Header "Phase 1 - Pre-flight Checks"
Write-Step "Checking Docker daemon..."
try {
    $null = docker info 2>&1
    if ($LASTEXITCODE -ne 0) { throw }
    Write-OK "Docker daemon is running."
} catch {
    Write-Fail "Docker daemon is not running. Please start Docker Desktop and try again."
}

# PHASE 2 - GIT PULL
Write-Header "Phase 2 - Pulling Updates from GitHub"
Write-Step "Updating orchestrator repository..."
git pull origin main
if ($LASTEXITCODE -ne 0) { Write-Warn "Failed to update orchestrator repository. Continuing..." }
else { Write-OK "Orchestrator repository updated." }

Write-Step "Updating apps/smriti_retail_os..."
if (Test-Path "apps\smriti_retail_os") {
    Push-Location "apps\smriti_retail_os"
    git pull origin main
    $gitStatus = $LASTEXITCODE
    Pop-Location
    if ($gitStatus -ne 0) { Write-Warn "Failed to update smriti_retail_os. Continuing..." }
    else { Write-OK "smriti_retail_os app updated." }
} else {
    Write-Fail "apps/smriti_retail_os directory not found! Run this script from the Smriti Retail OS root."
}

# PHASE 3 - LAUNCH AND REBUILD
Write-Header "Phase 3 - Rebuilding & Migrating inside Docker"

# Find backend container name dynamically
$folderName = (Get-Item -Path ".").Name -replace '[^a-z0-9]', '_'
$backendContainer = "${folderName}-backend-1"

Write-Step "Checking backend container ($backendContainer)..."
$running = docker inspect --format='{{.State.Status}}' $backendContainer 2>&1
if ($running -ne "running") {
    Write-Step "Starting containers..."
    docker compose -f $COMPOSE_FILE up -d
    Start-Sleep -Seconds 5
}

Write-Step "1. Compiling frontend assets..."
docker exec $backendContainer bench build --app smriti_retail_os
if ($LASTEXITCODE -ne 0) { Write-Warn "Bench build failed. Continuing..." }

Write-Step "2. Migrating database schemas..."
docker exec $backendContainer bench --site $SITE_NAME migrate
if ($LASTEXITCODE -ne 0) { Write-Fail "Migration failed! Database may be in inconsistent state." }
Write-OK "Database migrated successfully."

Write-Step "3. Syncing production assets to Nginx..."
docker exec $backendContainer /home/frappe/frappe-bench/env/bin/python /home/frappe/frappe-bench/apps/smriti_retail_os/smriti_retail_os/sync_assets.py
if ($LASTEXITCODE -ne 0) { Write-Warn "Sync assets failed. Continuing..." }
Write-OK "Assets synced."

Write-Step "4. Clearing cache..."
docker exec $backendContainer bench --site $SITE_NAME clear-cache
Write-OK "Cache cleared."

Write-Step "5. Restarting backend services..."
docker exec $backendContainer bench restart
Write-OK "Services restarted."

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "     SMRITI RETAIL OS UPDATED SUCCESSFULLY!               " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host ""
