#Requires -Version 5.1
# =============================================================================
#  SMRITI RETAIL OS - Windows Installer
#  Usage:  .\install.ps1
#          .\install.ps1 -AdminPassword "MySecret123"
#          .\install.ps1 -SkipClone   (if apps/ folders already populated)
# =============================================================================

param(
    [string]$AdminPassword = "admin",
    [switch]$SkipClone,
    [switch]$Force   # destroy existing volumes and start fresh
)

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
    Write-Host "      SMRITI RETAIL OS - INSTALLER v1.0.0       " -ForegroundColor Magenta
    Write-Host "================================================" -ForegroundColor Magenta
}

# -- Constants -----------------------------------------------------------------
$COMPOSE_FILE   = "pwd.yml"
$SMRITI_REPO    = "https://github.com/erpnbook/smriti.git"
$SMRITI_BRANCH  = "main"
$IC_REPO        = "https://github.com/resilient-tech/india-compliance.git"
$IC_BRANCH      = "version-16"
$SITE_NAME      = "smriti_retail"

function Get-EnvMap {
    $map = @{}
    if (Test-Path ".env") {
        Get-Content ".env" | ForEach-Object {
            $line = $_.Trim()
            if ($line -and -not $line.StartsWith("#") -and $line -match "^([^=]+)=(.*)$") {
                $key = $Matches[1].Trim()
                $val = $Matches[2].Trim()
                $map[$key] = $val
            }
        }
    }
    return $map
}

$envMap = Get-EnvMap
$HttpPort = $envMap["HTTP_PUBLISH_PORT"]
if ([string]::IsNullOrWhiteSpace($HttpPort)) { $HttpPort = "8765" }
$APP_URL        = "http://localhost:$HttpPort"

Write-Banner

# =============================================================================
# PHASE 1 - PRE-FLIGHT CHECKS
# =============================================================================
Write-Header "Phase 1 - Pre-flight Checks"

# 1a. Docker installed?
Write-Step "Checking Docker installation..."
try {
    $null = docker --version 2>&1
    $dockerVer = docker --version
    Write-OK "Docker found: $dockerVer"
} catch {
    Write-Fail "Docker is not installed or not in PATH. Install from https://docs.docker.com/get-docker/"
}

# 1b. Docker daemon running?
Write-Step "Checking Docker daemon..."
try {
    $null = docker info 2>&1
    if ($LASTEXITCODE -ne 0) { throw }
    Write-OK "Docker daemon is running."
} catch {
    Write-Fail "Docker daemon is not running. Please start Docker Desktop and try again."
}

# 1c. Docker Compose v2?
Write-Step "Checking Docker Compose..."
try {
    $null = docker compose version 2>&1
    if ($LASTEXITCODE -ne 0) { throw }
    $composeVer = docker compose version
    Write-OK "Docker Compose found: $composeVer"
} catch {
    Write-Fail "Docker Compose v2 not found. Update Docker Desktop or install the plugin."
}

# 1d. Git installed?
Write-Step "Checking Git..."
try {
    $null = git --version 2>&1
    $gitVer = git --version
    Write-OK "Git found: $gitVer"
} catch {
    Write-Fail "Git is not installed. Install from https://git-scm.com/"
}

# 1e. Port free?
Write-Step "Checking if port $HttpPort is free..."
$portInUse = Get-NetTCPConnection -LocalPort $HttpPort -ErrorAction SilentlyContinue
if ($portInUse) {
    Write-Warn "Port $HttpPort is already in use. Another service may conflict."
    Write-Warn "Continuing anyway - you can change the port in .env if needed."
} else {
    Write-OK "Port $HttpPort is free."
}

# 1f. Check compose file exists
Write-Step "Checking $COMPOSE_FILE..."
if (-not (Test-Path $COMPOSE_FILE)) {
    Write-Fail "$COMPOSE_FILE not found. Run this script from the Smriti Retail OS directory."
}
Write-OK "$COMPOSE_FILE found."

# =============================================================================
# PHASE 2 - CLONE APP SOURCES
# =============================================================================
Write-Header "Phase 2 - App Source Setup"

if ($SkipClone) {
    Write-Warn "-SkipClone flag set - skipping git clone steps."
} else {
    # smriti_retail_os
    Write-Step "Setting up apps/smriti_retail_os..."
    if (Test-Path "apps\smriti_retail_os\pyproject.toml") {
        Write-OK "apps/smriti_retail_os already populated - skipping clone."
    } else {
        if (-not (Test-Path "apps\smriti_retail_os")) {
            New-Item -ItemType Directory -Path "apps\smriti_retail_os" -Force | Out-Null
        }
        $items = Get-ChildItem "apps\smriti_retail_os" -ErrorAction SilentlyContinue
        if (-not $items) {
            Write-Step "Cloning smriti_retail_os from GitHub..."
            git clone --branch $SMRITI_BRANCH --depth 1 $SMRITI_REPO "apps\smriti_retail_os"
            if ($LASTEXITCODE -ne 0) { Write-Fail "Failed to clone smriti_retail_os. Check your internet connection and the repo URL." }
            Write-OK "smriti_retail_os cloned successfully."
        } else {
            Write-Warn "apps/smriti_retail_os has files but no pyproject.toml - check contents manually."
        }
    }

    # india_compliance
    Write-Step "Setting up apps/india_compliance..."
    if (Test-Path "apps\india_compliance\pyproject.toml") {
        Write-OK "apps/india_compliance already populated - skipping clone."
    } else {
        if (-not (Test-Path "apps\india_compliance")) {
            New-Item -ItemType Directory -Path "apps\india_compliance" -Force | Out-Null
        }
        $items = Get-ChildItem "apps\india_compliance" -ErrorAction SilentlyContinue
        if (-not $items) {
            Write-Step "Cloning india_compliance from GitHub..."
            git clone --branch $IC_BRANCH --depth 1 $IC_REPO "apps\india_compliance"
            if ($LASTEXITCODE -ne 0) { Write-Fail "Failed to clone india_compliance. Check your internet connection." }
            Write-OK "india_compliance cloned successfully."
        } else {
            Write-Warn "apps/india_compliance has files but no pyproject.toml - check contents manually."
        }
    }
}

# =============================================================================
# PHASE 3 - ENVIRONMENT SETUP
# =============================================================================
Write-Header "Phase 3 - Environment Setup"

# Copy .env if missing
Write-Step "Checking .env file..."
if (-not (Test-Path ".env")) {
    if (Test-Path "example.env") {
        Copy-Item "example.env" ".env"
        Write-OK ".env created from example.env"
    } else {
        # Create a minimal .env
        @"
ERPNEXT_VERSION=v16.19.1
DB_HOST=db
DB_PORT=3306
REDIS_CACHE=redis-cache:6379
REDIS_QUEUE=redis-queue:6379
"@ | Set-Content ".env"
        Write-OK "Minimal .env created."
    }
} else {
    Write-OK ".env already exists."
}

# Reload environment variables in case .env was just created
$envMap = Get-EnvMap
$HttpPort = $envMap["HTTP_PUBLISH_PORT"]
if ([string]::IsNullOrWhiteSpace($HttpPort)) { $HttpPort = "8765" }
$APP_URL = "http://localhost:$HttpPort"

# Force-reset if requested
if ($Force) {
    Write-Warn "-Force flag set - removing existing volumes (ALL DATA WILL BE DELETED)..."
    docker compose -f $COMPOSE_FILE down -v 2>&1 | Out-Null
    Write-OK "Volumes removed. Starting fresh."
}

# =============================================================================
# PHASE 4 - LAUNCH CONTAINERS
# =============================================================================
Write-Header "Phase 4 - Launching Containers"

Write-Step "Starting all services with: docker compose -f $COMPOSE_FILE up -d"
docker compose -f $COMPOSE_FILE up -d
if ($LASTEXITCODE -ne 0) {
    Write-Fail "docker compose up failed. Check the output above for errors."
}
Write-OK "All containers launched."

# =============================================================================
# PHASE 5 - WAIT FOR SITE CREATION
# =============================================================================
Write-Header "Phase 5 - Waiting for Site Initialization"

Write-Step "Waiting for site creation (this takes 3-8 minutes on first run)..."
Write-Host "  Press Ctrl+C to stop watching at any time.`n" -ForegroundColor DarkGray

# Find the create-site container name dynamically
$folderName = (Get-Item -Path ".").Name -replace '[^a-z0-9]', '_'
$createSiteContainer = "${folderName}-create-site-1"

# Timeout after 15 minutes (create-site now waits for configurator first)
$timeout = 900
$elapsed = 0
$interval = 15
$siteReady = $false

# Brief initial wait for container to start
Start-Sleep -Seconds 5

Write-Host ""
while ($elapsed -lt $timeout) {
    # Check if create-site container has finished (exited 0)
    $status = docker inspect --format='{{.State.ExitCode}} {{.State.Status}}' $createSiteContainer 2>&1
    if ($status -match "^0 exited") {
        Write-OK "Site creation completed successfully!"
        $siteReady = $true
        break
    }
    if ($status -match "^[1-9]+ exited") {
        Write-Host ""
        Write-Warn "create-site container exited with an error."
        Write-Warn "Showing last 50 log lines:"
        docker logs $createSiteContainer --tail 50
        Write-Fail "Site creation failed. See logs above. Run '.\check.ps1' to diagnose."
    }

    # Show a spinner / last log line
    $lastLog = docker logs $createSiteContainer --tail 1 2>&1
    Write-Host "  [$([Math]::Floor($elapsed/60))m$($elapsed % 60)s] $lastLog" -ForegroundColor DarkGray
    Start-Sleep -Seconds $interval
    $elapsed += $interval
}

if (-not $siteReady) {
    Write-Warn "Timed out waiting for site creation after 15 minutes."
    Write-Warn "Run 'docker logs $createSiteContainer --tail 100' to check progress."
    Write-Warn "Run '.\check.ps1' to diagnose."
}

# =============================================================================
# PHASE 6 - POST-INSTALL SETUP
# =============================================================================
Write-Header "Phase 6 - Post-Install Setup"

# Detect the backend container name
$backendContainer = "${folderName}-backend-1"

Write-Step "Waiting for backend container to be healthy..."
Write-Host "  (Backend starts only after site creation completes)" -ForegroundColor DarkGray
$healthy = $false
for ($i = 0; $i -lt 30; $i++) {
    $bStatus = docker inspect --format='{{.State.Health.Status}}' $backendContainer 2>&1
    if ($bStatus -eq "healthy") { $healthy = $true; break }
    $cStatus = docker inspect --format='{{.State.Status}}' $backendContainer 2>&1
    if ($cStatus -eq "running") {
        Write-Host "  [${i}] Backend running, waiting for healthy..." -ForegroundColor DarkGray
    } else {
        Write-Host "  [${i}] Backend status: $cStatus (waiting for create-site to finish)..." -ForegroundColor DarkGray
    }
    Start-Sleep -Seconds 10
}

if ($healthy) {
    # NOTE: setup and sync_assets are already handled by the create-site container.
    # We only need to clear cache here.
    Write-Step "Clearing cache..."
    docker exec $backendContainer bench --site $SITE_NAME clear-cache 2>&1
    Write-OK "Cache cleared."
} else {
    Write-Warn "Backend container not healthy yet. The site may still be initializing."
    Write-Warn "Run '.\check.ps1' in a few minutes to verify system health."
}

# =============================================================================
# PHASE 7 - HEALTH CHECK
# =============================================================================
Write-Header "Phase 7 - Health Check"

Write-Step "Checking container health..."
docker compose -f $COMPOSE_FILE ps --format "table {{.Name}}\t{{.Status}}"

Write-Step "Testing HTTP connectivity..."
$maxRetries = 12
$retryCount = 0
$ready = $false

while ($retryCount -lt $maxRetries -and -not $ready) {
    try {
        $response = Invoke-WebRequest "http://localhost:$HttpPort/api/method/ping" -UseBasicParsing -ErrorAction Stop
        if ($response.StatusCode -eq 200) { $ready = $true }
    } catch {
        $retryCount++
        Write-Host "Waiting for SMRITI to start... ($retryCount/$maxRetries)"
        Start-Sleep -Seconds 10
    }
}

if (-not $ready) {
    Write-Host "ERROR: SMRITI did not respond after 2 minutes." -ForegroundColor Red
    Write-Host "Logs: docker compose -f pwd.yml logs backend" -ForegroundColor Yellow
    exit 1
}

$LanIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {
    $_.IPAddress -notlike '169.254*' -and
    $_.IPAddress -ne '127.0.0.1' -and
    $_.InterfaceAlias -notmatch 'vEthernet|Docker|WSL|Hyper-V'
} | Select-Object -First 1).IPAddress

if ([string]::IsNullOrWhiteSpace($LanIP)) { $LanIP = "localhost" }

Write-Host ""
Write-Host "SMRITI Retail OS is ready!" -ForegroundColor Green
Write-Host "Local Access : http://localhost:$HttpPort" -ForegroundColor Cyan
Write-Host "LAN Access   : http://${LanIP}:$HttpPort" -ForegroundColor Cyan
Write-Host "Username     : Administrator" -ForegroundColor Green
Write-Host "Password     : $AdminPassword" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "  Run  .\check.ps1  anytime to verify system health" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host ""

# Open browser
$open = Read-Host "Open browser now? [Y/n]"
if ($open -ne 'n' -and $open -ne 'N') {
    Start-Process $APP_URL
}
