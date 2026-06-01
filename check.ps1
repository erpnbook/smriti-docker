#Requires -Version 5.1
# =============================================================================
#  SMRITI RETAIL OS - Pre-flight Validator & Health Checker
#  Run BEFORE install to verify prerequisites
#  Run AFTER install to verify everything is working
#  Usage:  .\check.ps1
# =============================================================================

$COMPOSE_FILE = "pwd.yml"
$APP_URL      = "http://localhost:8080"
$PASS = 0
$FAIL = 0
$WARN = 0

function Write-Check {
    param([string]$label, [string]$result, [string]$color = "Green", [string]$detail = "")
    if ($color -eq "Green") { $icon = "[OK]" }
    elseif ($color -eq "DarkYellow") { $icon = "[!!]" }
    else { $icon = "[XX]" }
    Write-Host ("  {0,-5} {1,-42} {2}" -f $icon, $label, $result) -ForegroundColor $color
    if ($detail) { Write-Host "         $detail" -ForegroundColor DarkGray }
}

function Pass { param([string]$l,[string]$r,[string]$d="") $script:PASS++; Write-Check $l $r "Green" $d }
function Fail { param([string]$l,[string]$r,[string]$d="") $script:FAIL++; Write-Check $l $r "Red" $d }
function Warn { param([string]$l,[string]$r,[string]$d="") $script:WARN++; Write-Check $l $r "DarkYellow" $d }

Write-Host ""
Write-Host "  =======================================================" -ForegroundColor Cyan
Write-Host "   SMRITI RETAIL OS - System Health Check" -ForegroundColor Cyan
Write-Host "  =======================================================" -ForegroundColor Cyan
Write-Host ""

# =============================================================================
# SECTION A - Prerequisites
# =============================================================================
Write-Host "  [ A ] Prerequisites" -ForegroundColor White
Write-Host "  -------------------------------------------------------" -ForegroundColor DarkGray

# Docker installed?
try {
    $dv = docker --version 2>&1
    if ($LASTEXITCODE -eq 0) { Pass "Docker installed" "$dv" }
    else { Fail "Docker installed" "NOT FOUND" "Install from https://docs.docker.com/get-docker/" }
} catch { Fail "Docker installed" "NOT FOUND" "Install from https://docs.docker.com/get-docker/" }

# Docker daemon running?
try {
    $null = docker info 2>&1
    if ($LASTEXITCODE -eq 0) { Pass "Docker daemon" "Running" }
    else { Fail "Docker daemon" "NOT RUNNING" "Start Docker Desktop" }
} catch { Fail "Docker daemon" "NOT RUNNING" "Start Docker Desktop" }

# Docker Compose v2?
try {
    $cv = docker compose version 2>&1
    if ($LASTEXITCODE -eq 0) { Pass "Docker Compose v2" "$cv" }
    else { Fail "Docker Compose v2" "NOT FOUND" "Update Docker Desktop" }
} catch { Fail "Docker Compose v2" "NOT FOUND" "Update Docker Desktop" }

# Git installed?
try {
    $gv = git --version 2>&1
    if ($LASTEXITCODE -eq 0) { Pass "Git installed" "$gv" }
    else { Fail "Git installed" "NOT FOUND" "Install from https://git-scm.com/" }
} catch { Fail "Git installed" "NOT FOUND" "Install from https://git-scm.com/" }

# Port 8080 free?
$portInUse = Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue
if ($portInUse) {
    $proc = Get-Process -Id $portInUse[0].OwningProcess -ErrorAction SilentlyContinue
    $portMsg = "Used by: " + $proc.ProcessName + " PID " + $proc.Id
    Warn "Port 8080" "IN USE" $portMsg
} else {
    Pass "Port 8080" "Free"
}

# =============================================================================
# SECTION B - Project Files
# =============================================================================
Write-Host ""
Write-Host "  [ B ] Project Files" -ForegroundColor White
Write-Host "  -------------------------------------------------------" -ForegroundColor DarkGray

# pwd.yml present?
if (Test-Path $COMPOSE_FILE) { Pass "$COMPOSE_FILE" "Found" }
else { Fail "$COMPOSE_FILE" "MISSING" "Run this script from the Smriti Retail OS directory" }

# .env present?
if (Test-Path ".env") { Pass ".env file" "Found" }
else { Warn ".env file" "MISSING" "Run .\install.ps1 or copy example.env to .env" }

# smriti_retail_os app source?
if (Test-Path "apps\smriti_retail_os\pyproject.toml") {
    Pass "apps/smriti_retail_os" "Populated - pyproject.toml found"
} elseif (Test-Path "apps\smriti_retail_os") {
    $count = (Get-ChildItem "apps\smriti_retail_os" -ErrorAction SilentlyContinue).Count
    $msg = "EMPTY - $count files found"
    Fail "apps/smriti_retail_os" $msg "Run .\install.ps1 to clone the app source"
} else {
    Fail "apps/smriti_retail_os" "DIRECTORY MISSING" "Run .\install.ps1 to clone the app source"
}

# india_compliance app source?
if (Test-Path "apps\india_compliance\pyproject.toml") {
    Pass "apps/india_compliance" "Populated - pyproject.toml found"
} elseif (Test-Path "apps\india_compliance") {
    $count = (Get-ChildItem "apps\india_compliance" -ErrorAction SilentlyContinue).Count
    $msg = "EMPTY - $count files found"
    Fail "apps/india_compliance" $msg "Run .\install.ps1 to clone the app source"
} else {
    Fail "apps/india_compliance" "DIRECTORY MISSING" "Run .\install.ps1 to clone the app source"
}

# assets folder?
if (Test-Path "assets") {
    Pass "assets/ folder" "Found"
} else {
    Warn "assets/ folder" "MISSING" "Assets will be compiled on first boot - takes ~5 min"
}

# =============================================================================
# SECTION C - Container Health (only if Docker is running)
# =============================================================================
Write-Host ""
Write-Host "  [ C ] Container Health" -ForegroundColor White
Write-Host "  -------------------------------------------------------" -ForegroundColor DarkGray

$dockerRunning = $false
try { $null = docker info 2>&1; $dockerRunning = ($LASTEXITCODE -eq 0) } catch {}

if ($dockerRunning) {
    # Auto-detect Docker Compose project name from running containers
    $folderName = ""
    try {
        $runningContainer = docker ps --format '{{.Names}}' 2>&1 | Select-String '-backend-1$' | Select-Object -First 1
        if ($runningContainer) {
            $folderName = ($runningContainer -replace '-backend-1$', '')
        }
    } catch {}
    if (-not $folderName) {
        $folderName = (Get-Item -Path ".").Name.ToLower() -replace '[^a-z0-9_]', '_'
    }

    $expectedContainers = @(
        "backend", "frontend", "db", "websocket",
        "scheduler", "queue-long", "queue-short",
        "redis-cache", "redis-queue"
    )

    foreach ($svc in $expectedContainers) {
        $cName = "${folderName}-${svc}-1"
        try {
            $state = docker inspect --format='{{.State.Status}}' $cName 2>&1
            if ($state -eq "running") {
                Pass "Container: $svc" "Up"
            } elseif ($state -match "restarting") {
                $lastErr = docker logs $cName --tail 3 2>&1 | Select-Object -Last 1
                Fail "Container: $svc" "RESTARTING" "Last log: $lastErr"
            } elseif ($state -match "exited") {
                $exitCode = docker inspect --format='{{.State.ExitCode}}' $cName 2>&1
                if ($exitCode -eq "0") {
                    Pass "Container: $svc" "Exited OK - one-time job"
                } else {
                    $exitMsg = "EXITED code $exitCode"
                    Fail "Container: $svc" $exitMsg "Run: docker logs $cName --tail 30"
                }
            } else {
                Warn "Container: $svc" "$state"
            }
        } catch {
            Warn "Container: $svc" "NOT FOUND" "Run .\install.ps1 to create containers"
        }
    }
} else {
    Warn "Container checks" "SKIPPED" "Docker daemon not running"
}

# =============================================================================
# SECTION D - Application Connectivity
# =============================================================================
Write-Host ""
Write-Host "  [ D ] Application Connectivity" -ForegroundColor White
Write-Host "  -------------------------------------------------------" -ForegroundColor DarkGray

try {
    $resp = Invoke-WebRequest -Uri $APP_URL -TimeoutSec 8 -UseBasicParsing -ErrorAction Stop
    if ($resp.StatusCode -eq 200) {
        Pass "HTTP $APP_URL" "200 OK - App is reachable!"
    } else {
        $statusMsg = "Status " + $resp.StatusCode
        Warn "HTTP $APP_URL" $statusMsg
    }
} catch [System.Net.WebException] {
    Fail "HTTP $APP_URL" "CONNECTION REFUSED" "Containers may still be starting or crashed"
} catch {
    Warn "HTTP $APP_URL" "Could not connect" "$($_.Exception.Message)"
}

# Test login page specifically
try {
    $loginResp = Invoke-WebRequest -Uri "$APP_URL/login" -TimeoutSec 8 -UseBasicParsing -ErrorAction Stop
    if ($loginResp.Content -match "login|frappe|smriti") {
        Pass "Login page" "Reachable"
    } else {
        Warn "Login page" "Unexpected content"
    }
} catch {
    Warn "Login page" "Could not connect"
}

# =============================================================================
# SUMMARY
# =============================================================================
Write-Host ""
Write-Host "  =======================================================" -ForegroundColor Cyan
$total = $PASS + $FAIL + $WARN
Write-Host ("  Summary: {0} passed  |  {1} warnings  |  {2} failed  of {3} checks" -f $PASS, $WARN, $FAIL, $total) -ForegroundColor Cyan
Write-Host "  =======================================================" -ForegroundColor Cyan

if ($FAIL -eq 0 -and $WARN -eq 0) {
    Write-Host "  Everything looks great! Open http://localhost:8080 to use Smriti Retail OS." -ForegroundColor Green
} elseif ($FAIL -eq 0) {
    Write-Host "  Minor warnings above - system may still work. Review items marked [!!]." -ForegroundColor DarkYellow
} else {
    Write-Host "  Fix the failed checks above, then run .\install.ps1 or .\check.ps1 again." -ForegroundColor Red
    Write-Host "  See TROUBLESHOOTING.md for detailed fix instructions." -ForegroundColor DarkGray
}
Write-Host ""
