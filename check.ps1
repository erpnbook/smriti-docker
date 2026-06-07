#Requires -Version 5.1
# =============================================================================
#  SMRITI RETAIL OS - Pre-flight Validator & Health Checker
# =============================================================================

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

Write-Host "Checking SMRITI on port $HttpPort..."

# TCP check
$tcp = Test-NetConnection localhost -Port $HttpPort -WarningAction SilentlyContinue
if (-not $tcp.TcpTestSucceeded) {
    Write-Host "FAIL: Port $HttpPort not responding. Is Docker running?" -ForegroundColor Red
    Write-Host "Run : docker compose -f pwd.yml up -d" -ForegroundColor Yellow
    exit 1
}
Write-Host "TCP  : OK" -ForegroundColor Green

# HTTP check - status 200 only
try {
    $ping = Invoke-WebRequest "http://localhost:$HttpPort/api/method/ping" -UseBasicParsing -ErrorAction Stop
    if ($ping.StatusCode -eq 200) {
        Write-Host "HTTP : OK - SMRITI is live" -ForegroundColor Green
    } else {
        throw "Unexpected status $($ping.StatusCode)"
    }
} catch {
    Write-Host "FAIL: HTTP ping failed - $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Logs: docker compose -f pwd.yml logs backend" -ForegroundColor Yellow
    exit 1
}

# LAN IP — filter by interface name, not IP range
$LanIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {
    $_.IPAddress -notlike '169.254*' -and
    $_.IPAddress -ne '127.0.0.1' -and
    $_.InterfaceAlias -notmatch 'vEthernet|Docker|WSL|Hyper-V'
} | Select-Object -First 1).IPAddress

if ([string]::IsNullOrWhiteSpace($LanIP)) { $LanIP = "localhost" }

Write-Host ""
Write-Host "Local : http://localhost:$($HttpPort)" -ForegroundColor Cyan
Write-Host "LAN   : http://$($LanIP):$($HttpPort)" -ForegroundColor Cyan
