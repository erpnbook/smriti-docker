#!/usr/bin/env bash
# =============================================================================
#  SMRITI RETAIL OS — Linux / macOS Installer
#  Usage:  bash install.sh
#          bash install.sh --password MySecret123
#          bash install.sh --skip-clone     (if apps/ folders already populated)
#          bash install.sh --force          (destroy volumes, fresh start)
# =============================================================================

set -euo pipefail

# ── Defaults ─────────────────────────────────────────────────────────────────
ADMIN_PASSWORD="admin"
SKIP_CLONE=0
FORCE=0
COMPOSE_FILE="pwd.yml"
SMRITI_REPO="https://github.com/erpnbook/smriti.git"
SMRITI_BRANCH="main"
IC_REPO="https://github.com/resilient-tech/india-compliance.git"
IC_BRANCH="version-16"
HTTP_PUBLISH_PORT=8765
if [ -f .env ]; then
    ENV_PORT=$(grep -E '^\s*HTTP_PUBLISH_PORT\s*=' .env | cut -d= -f2 | tr -d '[:space:]')
    if [ ! -z "$ENV_PORT" ]; then
        HTTP_PUBLISH_PORT="$ENV_PORT"
    fi
fi
HTTP_PORT="$HTTP_PUBLISH_PORT"
APP_URL="http://localhost:$HTTP_PORT"
SITE_NAME="smriti_retail"

# ── Parse arguments ───────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --password) ADMIN_PASSWORD="$2"; shift 2 ;;
        --skip-clone) SKIP_CLONE=1; shift ;;
        --force) FORCE=1; shift ;;
        *) echo "Unknown argument: $1"; exit 1 ;;
    esac
done

# ── Colour helpers ────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; MAGENTA='\033[0;35m'; GRAY='\033[0;90m'; NC='\033[0m'

step()  { echo -e "${YELLOW}  ▶  $1${NC}"; }
ok()    { echo -e "${GREEN}  ✔  $1${NC}"; }
warn()  { echo -e "${YELLOW}  ⚠  $1${NC}"; }
fail()  { echo -e "${RED}  ✘  $1${NC}"; exit 1; }
header(){ echo -e "\n${CYAN}╔══════════════════════════════════════════════╗"; \
           echo -e "  $1"; \
           echo -e "╚══════════════════════════════════════════════╝${NC}\n"; }

banner() {
echo -e "${MAGENTA}
  ███████╗███╗   ███╗██████╗ ██╗████████╗██╗
  ██╔════╝████╗ ████║██╔══██╗██║╚══██╔══╝██║
  ███████╗██╔████╔██║██████╔╝██║   ██║   ██║
  ╚════██║██║╚██╔╝██║██╔══██╗██║   ██║   ██║
  ███████║██║ ╚═╝ ██║██║  ██║██║   ██║   ██║
  ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝
       R E T A I L   O S   —   v 1 . 0 . 0
${NC}"
}

banner

# =============================================================================
# PHASE 1 — PRE-FLIGHT CHECKS
# =============================================================================
header "Phase 1 — Pre-flight Checks"

step "Checking Docker..."
if ! command -v docker &>/dev/null; then fail "Docker not installed. See https://docs.docker.com/get-docker/"; fi
ok "Docker found: $(docker --version)"

step "Checking Docker daemon..."
if ! docker info &>/dev/null; then fail "Docker daemon not running. Start Docker and try again."; fi
ok "Docker daemon is running."

step "Checking Docker Compose v2..."
if ! docker compose version &>/dev/null; then fail "Docker Compose v2 not found. Update Docker or install the plugin."; fi
ok "Docker Compose: $(docker compose version)"

step "Checking Git..."
if ! command -v git &>/dev/null; then fail "Git not installed. Install from https://git-scm.com/"; fi
ok "Git: $(git --version)"

step "Checking port $HTTP_PORT..."
if lsof -Pi :$HTTP_PORT -sTCP:LISTEN -t &>/dev/null 2>&1; then
    warn "Port $HTTP_PORT is in use. Another service may conflict."
else
    ok "Port $HTTP_PORT is free."
fi

step "Checking $COMPOSE_FILE..."
if [[ ! -f "$COMPOSE_FILE" ]]; then fail "$COMPOSE_FILE not found. Run from the Smriti Retail OS directory."; fi
ok "$COMPOSE_FILE found."

# =============================================================================
# PHASE 2 — CLONE APP SOURCES
# =============================================================================
header "Phase 2 — App Source Setup"

if [[ $SKIP_CLONE -eq 1 ]]; then
    warn "--skip-clone set — skipping git clone steps."
else
    # smriti_retail_os
    step "Setting up apps/smriti_retail_os..."
    mkdir -p apps/smriti_retail_os
    if [[ -f "apps/smriti_retail_os/pyproject.toml" ]]; then
        ok "apps/smriti_retail_os already populated — skipping."
    else
        if [[ -z "$(ls -A apps/smriti_retail_os 2>/dev/null)" ]]; then
            step "Cloning smriti_retail_os ($SMRITI_BRANCH)..."
            git clone --branch "$SMRITI_BRANCH" --depth 1 "$SMRITI_REPO" apps/smriti_retail_os
            ok "smriti_retail_os cloned."
        else
            warn "apps/smriti_retail_os has files but no pyproject.toml — check contents."
        fi
    fi

    # india_compliance
    step "Setting up apps/india_compliance..."
    mkdir -p apps/india_compliance
    if [[ -f "apps/india_compliance/pyproject.toml" ]]; then
        ok "apps/india_compliance already populated — skipping."
    else
        if [[ -z "$(ls -A apps/india_compliance 2>/dev/null)" ]]; then
            step "Cloning india_compliance ($IC_BRANCH)..."
            git clone --branch "$IC_BRANCH" --depth 1 "$IC_REPO" apps/india_compliance
            ok "india_compliance cloned."
        else
            warn "apps/india_compliance has files but no pyproject.toml — check contents."
        fi
    fi
fi

# =============================================================================
# PHASE 3 — ENVIRONMENT SETUP
# =============================================================================
header "Phase 3 — Environment Setup"

step "Checking .env file..."
if [[ ! -f ".env" ]]; then
    if [[ -f "example.env" ]]; then
        cp example.env .env
        ok ".env created from example.env"
    else
        cat > .env << 'EOF'
ERPNEXT_VERSION=v16.19.1
DB_HOST=db
DB_PORT=3306
REDIS_CACHE=redis-cache:6379
REDIS_QUEUE=redis-queue:6379
EOF
        ok "Minimal .env created."
    fi
else
    ok ".env already exists."
fi

# Reload environment variables in case .env was just created
if [ -f .env ]; then
    ENV_PORT=$(grep -E '^\s*HTTP_PUBLISH_PORT\s*=' .env | cut -d= -f2 | tr -d '[:space:]')
    if [ ! -z "$ENV_PORT" ]; then
        HTTP_PUBLISH_PORT="$ENV_PORT"
    fi
fi
HTTP_PORT="$HTTP_PUBLISH_PORT"
APP_URL="http://localhost:$HTTP_PORT"

if [[ $FORCE -eq 1 ]]; then
    warn "--force set — removing existing volumes (ALL DATA WILL BE DELETED)..."
    docker compose -f "$COMPOSE_FILE" down -v 2>/dev/null || true
    ok "Volumes removed. Starting fresh."
fi

# =============================================================================
# PHASE 4 — LAUNCH CONTAINERS
# =============================================================================
header "Phase 4 — Launching Containers"

step "Starting all services..."
docker compose -f "$COMPOSE_FILE" up -d
ok "All containers launched."

# =============================================================================
# PHASE 5 — WAIT FOR SITE CREATION
# =============================================================================
header "Phase 5 — Waiting for Site Initialization"

FOLDER_NAME=$(basename "$(pwd)" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/_/g')
CREATE_SITE_CONTAINER="${FOLDER_NAME}-create-site-1"
BACKEND_CONTAINER="${FOLDER_NAME}-backend-1"

step "Waiting for site creation (2-5 minutes)..."
sleep 5

TIMEOUT=600
ELAPSED=0
INTERVAL=10
SITE_READY=0

while [[ $ELAPSED -lt $TIMEOUT ]]; do
    STATUS=$(docker inspect --format='{{.State.ExitCode}} {{.State.Status}}' "$CREATE_SITE_CONTAINER" 2>/dev/null || echo "not_found")
    if [[ "$STATUS" == "0 exited" ]]; then
        ok "Site creation completed!"
        SITE_READY=1
        break
    fi
    if [[ "$STATUS" =~ ^[1-9]+[0-9]*\ exited ]]; then
        echo ""
        warn "create-site exited with an error. Last logs:"
        docker logs "$CREATE_SITE_CONTAINER" --tail 50
        fail "Site creation failed. See TROUBLESHOOTING.md for help."
    fi
    LAST_LOG=$(docker logs "$CREATE_SITE_CONTAINER" --tail 1 2>/dev/null || echo "waiting...")
    MINS=$((ELAPSED / 60))
    SECS=$((ELAPSED % 60))
    echo -e "  ${GRAY}[${MINS}m${SECS}s] ${LAST_LOG}${NC}"
    sleep $INTERVAL
    ELAPSED=$((ELAPSED + INTERVAL))
done

if [[ $SITE_READY -eq 0 ]]; then
    warn "Timed out. Process may still be running. Check: docker logs $CREATE_SITE_CONTAINER --tail 50"
fi

# =============================================================================
# PHASE 6 — POST-INSTALL SETUP
# =============================================================================
header "Phase 6 — Post-Install Setup"

HEALTHY=0
for i in $(seq 1 12); do
    BSTATUS=$(docker inspect --format='{{.State.Status}}' "$BACKEND_CONTAINER" 2>/dev/null || echo "")
    if [[ "$BSTATUS" == "running" ]]; then HEALTHY=1; break; fi
    sleep 5
done

if [[ $HEALTHY -eq 1 ]]; then
    step "Running SMRITI setup..."
    docker exec "$BACKEND_CONTAINER" bench --site "$SITE_NAME" execute smriti_retail_os.setup.setup_smriti_retail_os 2>&1 || warn "Setup script failed (may already be done)"
    ok "Setup complete."

    step "Syncing assets to Nginx..."
    docker exec "$BACKEND_CONTAINER" bench --site "$SITE_NAME" execute smriti_retail_os.sync_assets.sync_assets 2>&1 || warn "Asset sync failed"
    ok "Assets synced."

    step "Clearing cache..."
    docker exec "$BACKEND_CONTAINER" bench --site "$SITE_NAME" clear-cache 2>&1 || true
    ok "Cache cleared."
else
    warn "Backend not ready yet. Run these manually when it's up:"
    echo -e "  ${GRAY}docker exec $BACKEND_CONTAINER bench --site $SITE_NAME execute smriti_retail_os.setup.setup_smriti_retail_os${NC}"
    echo -e "  ${GRAY}docker exec $BACKEND_CONTAINER bench --site $SITE_NAME execute smriti_retail_os.sync_assets.sync_assets${NC}"
fi

# =============================================================================
# SUCCESS BANNER
# =============================================================================
echo "Waiting for SMRITI to start..."
MAX_RETRIES=12
COUNT=0
READY=false

while [ $COUNT -lt $MAX_RETRIES ]; do
    if curl -sf "http://localhost:$HTTP_PORT/api/method/ping" > /dev/null 2>&1; then
        READY=true
        break
    fi
    COUNT=$((COUNT + 1))
    echo "Attempt $COUNT/$MAX_RETRIES — retrying in 10s..."
    sleep 10
done

if [ "$READY" = false ]; then
    echo "ERROR: SMRITI did not respond after 2 minutes."
    echo "Logs: docker compose -f pwd.yml logs backend"
    exit 1
fi

# Most reliable LAN IP on Linux — uses routing table, skips Docker bridge
LAN_IP=$(ip route get 1.1.1.1 2>/dev/null | awk '{print $7; exit}')
if [ -z "$LAN_IP" ]; then
    LAN_IP=$(hostname -I | awk '{print $1}')
fi

echo ""
echo "SMRITI Retail OS is ready!"
echo "Local Access : http://localhost:$HTTP_PORT"
echo "LAN Access   : http://$LAN_IP:$HTTP_PORT"
echo "Username     : Administrator"
echo "Password     : ${ADMIN_PASSWORD}"
echo ""

# Open browser (Linux/macOS)
if command -v xdg-open &>/dev/null; then
    xdg-open "$APP_URL" 2>/dev/null &
elif command -v open &>/dev/null; then
    open "$APP_URL"
fi
