# 🚀 SMRITI RETAIL OS — Installation Guide

> **Version**: v1.0.0 | **Stack**: ERPNext v16 + Frappe v16 + India Compliance + Smriti Retail OS  
> **Time required**: ~10 minutes (mostly waiting for Docker to pull images)

---

## ⚡ One-Command Install

### Windows (PowerShell)

```powershell
# 1. Clone the repository
git clone https://github.com/erpnbook/smriti-docker.git smriti_retail
cd smriti_retail

# 2. Run the installer (does everything automatically)
.\install.ps1
```

> [!TIP]
> If Windows blocks the execution with a `SecurityError` (running scripts is disabled on this system), run the installer with a bypass policy instead:
> ```powershell
> PowerShell -ExecutionPolicy Bypass -File .\install.ps1
> ```

### Linux / macOS (Bash)

```bash
# 1. Clone the repository
git clone https://github.com/erpnbook/smriti-docker.git smriti_retail
cd smriti_retail

# 2. Run the installer
bash install.sh
```

The installer will:
- ✅ Check all prerequisites (Docker, Git, port 8080)
- ✅ Clone app source code into `apps/`
- ✅ Start all containers
- ✅ Wait for site creation (2–5 min)
- ✅ Run post-install setup & asset sync
- ✅ Open the app in your browser

---

## 📋 Prerequisites

Before running the installer, make sure you have:

| Requirement | Version | Install Link |
|---|---|---|
| **Docker Desktop** | Latest | https://docs.docker.com/get-docker/ |
| **Docker Compose v2** | Included in Docker Desktop | — |
| **Git** | Any | https://git-scm.com/ |
| **Free RAM** | ≥ 4 GB | — |
| **Free disk** | ≥ 10 GB | — |
| **Port 8080** | Must be free | — |

### Verify prerequisites manually

```powershell
# Windows
docker --version          # Docker version 27.x.x
docker compose version    # Docker Compose version v2.x.x
git --version             # git version 2.x.x
```

```bash
# Linux / macOS
docker --version && docker compose version && git --version
```

---

## 🗂️ Manual Step-by-Step (Advanced)

If you prefer full control or the one-command installer doesn't work for your setup:

### Step 1 — Clone the orchestration repo

```bash
git clone https://github.com/erpnbook/smriti-docker.git smriti_retail
cd smriti_retail
```

### Step 2 — Populate the app source folders

The `apps/` folder must contain the actual Python source code for both custom apps.
These are **not** included in the Docker image — they are bind-mounted at runtime.

```bash
# Clone smriti_retail_os app
git clone --branch v1.0.0 https://github.com/erpnbook/smriti.git apps/smriti_retail_os

# Clone india_compliance app
git clone --branch version-16 https://github.com/resilient-tech/india-compliance.git apps/india_compliance
```

> [!CAUTION]
> If `apps/smriti_retail_os/` is empty or missing `pyproject.toml`, the **backend container will crash in a restart loop**. Always verify:
> ```powershell
> # Windows
> Get-ChildItem apps\smriti_retail_os   # must show pyproject.toml
> # Linux/macOS
> ls apps/smriti_retail_os              # must show pyproject.toml
> ```

### Step 3 — Set up environment file

```bash
# Copy the example env file
cp example.env .env
```

The defaults in `.env` work for local development. For production, review and update passwords.

### Step 4 — Launch all containers

```bash
docker compose -f pwd.yml up -d
```

This starts 9 containers:
- `backend` — Gunicorn (Frappe/ERPNext Python app)
- `frontend` — Nginx (serves UI + proxies API)
- `db` — MariaDB 11.8
- `websocket` — Socket.IO
- `queue-short`, `queue-long` — RQ workers
- `scheduler` — Background job scheduler
- `redis-cache`, `redis-queue` — Redis instances
- `configurator` — One-time config writer (exits after success)
- `create-site` — One-time site creator (exits after success)

### Step 5 — Monitor site initialization

The first boot takes **2–5 minutes**. Watch the progress:

```bash
docker logs -f smriti_retail-create-site-1
```

Wait until you see:
```
Installed smriti_retail_os
```

> [!NOTE]
> The `configurator` and `create-site` containers exit with code 0 after completing their jobs. This is normal — they are one-time setup services.

### Step 6 — Run SMRITI post-install setup

Once `create-site` has exited successfully:

```bash
# Run initial SMRITI configuration
docker exec smriti_retail-backend-1 bench --site smriti_retail execute smriti_retail_os.setup.setup_smriti_retail_os

# Run Excel spreadsheet company details sync
docker exec smriti_retail-backend-1 bench --site smriti_retail execute smriti_retail_os.setup_tattly_threads.run

# Sync compiled assets to Nginx (prevents CSS/JS MIME-type errors)
docker exec smriti_retail-backend-1 bench --site smriti_retail execute smriti_retail_os.sync_assets.sync_assets
```

> [!IMPORTANT]
> The asset sync step is critical. Without it, the UI may load as **plain unstyled HTML** because Nginx can't find the compiled CSS/JS bundles.

### Step 7 — Access the system

Open your browser at:

```
http://localhost:8080
```

| Field | Value |
|---|---|
| **Username** | `Administrator` |
| **Password** | `admin` |

> [!WARNING]
> Change the default `admin` password immediately in production. Go to **Settings → Change Password**.

---

## ✅ Verify Your Installation

Run the health checker at any time:

```powershell
# Windows
.\check.ps1
```

This checks:
- All 9 containers are `Up`
- App source folders are populated
- HTTP connectivity to `http://localhost:8080`
- Login page is reachable

Expected output when healthy:
```
  ✔  Docker installed          Docker version 27.x.x
  ✔  Docker daemon             Running
  ✔  Docker Compose v2         Docker Compose version v2.x.x
  ✔  Git installed             git version 2.x.x
  ✔  Port 8080                 Free
  ✔  pwd.yml                   Found
  ✔  .env file                 Found
  ✔  apps/smriti_retail_os     Populated
  ✔  apps/india_compliance     Populated
  ✔  Container: backend        Up
  ✔  Container: frontend       Up
  ...
  ✔  HTTP http://localhost:8080  200 OK
```

---

## 🔄 Updating to a New Version

```bash
# 1. Pull latest app code
cd apps/smriti_retail_os
git pull origin main
cd ../..

# 2. Run database migrations
docker exec smriti_retail-backend-1 bench --site smriti_retail migrate

# 3. Rebuild and sync assets
docker exec smriti_retail-backend-1 bench build --app smriti_retail_os
docker exec smriti_retail-backend-1 bench --site smriti_retail execute smriti_retail_os.sync_assets.sync_assets

# 4. Clear cache
docker exec smriti_retail-backend-1 bench --site smriti_retail clear-cache
```

---

## 🧨 Full Reset (Fresh Start)

> [!CAUTION]
> This **deletes all data**. Use only in development.

```powershell
# Windows
docker compose -f pwd.yml down -v   # removes all containers + volumes
.\install.ps1 --force               # fresh install
```

```bash
# Linux / macOS
docker compose -f pwd.yml down -v
bash install.sh --force
```

---

## 🗑️ How to Uninstall & Stop

If you want to stop the services, wipe the environment, or completely uninstall SMRITI Retail OS from your machine:

### 1. Stop the Services (Temporary)
To temporarily stop all running SMRITI Docker containers without losing any database data or configurations:
```bash
docker compose -f pwd.yml down
```

### 2. Completely Uninstall (Deletes All Data)
To completely remove all SMRITI Docker containers, backend volumes, network bridges, and local database storage:
```bash
docker compose -f pwd.yml down -v
```

> [!WARNING]
> If Docker reports **`Resource is still in use`** (or fails to delete network/volumes), it is because the dangling `asset-guard` container is still active. Stop and remove it manually before rerunning down:
> ```bash
> docker stop smriti_retail-smriti-asset-guard-1
> docker rm smriti_retail-smriti-asset-guard-1
> # Now retry:
> docker compose -f pwd.yml down -v
> ```

### 3. Remove Source Files (Optional)
To delete all local orchestration configuration files and bind-mounted applications:

**Windows (PowerShell):**
```powershell
cd ..
Remove-Item -Recurse -Force smriti_retail
```

**Linux / macOS (Bash):**
```bash
cd ..
rm -rf smriti_retail
```

---

## ❓ Common Issues

| Symptom | Quick Fix |
|---|---|
| Backend keeps restarting | `apps/smriti_retail_os/` is empty → re-run `.\install.ps1` |
| `502 Bad Gateway` | `docker restart smriti_retail-frontend-1` |
| Blank/unstyled UI | Run asset sync: `bench --site smriti_retail execute smriti_retail_os.sync_assets.sync_assets` |
| `Invalid credentials` | `docker exec smriti_retail-backend-1 bench --site smriti_retail set-admin-password NewPass` |
| Container name wrong | Run `docker ps` to find actual names (depends on folder name) |
| `ERPNEXT_VERSION not set` | Copy `example.env` to `.env` |
| Script execution disabled | Run `PowerShell -ExecutionPolicy Bypass -File .\install.ps1` |

For detailed solutions, see [TROUBLESHOOTING.md](./TROUBLESHOOTING.md).

---

## 🏗️ Architecture

```
Browser (port 8080)
     │
     ▼
[frontend] Nginx
  ├── Serves static assets from: sites/assets/
  └── Proxies /api/, /app/ → [backend]:8000
     │
     ▼
[backend] Gunicorn (Frappe + ERPNext + Smriti)
     ├── [db] MariaDB 11.8
     ├── [redis-cache] + [redis-queue]
     ├── [queue-short] + [queue-long] RQ Workers
     ├── [scheduler] Beat Scheduler
     └── [websocket] Socket.IO
```

**Key design note**: `apps/smriti_retail_os/` and `apps/india_compliance/` are **bind-mounted** from the host into the containers. This means the app source code lives on your machine and is pip-installed into the container's virtualenv at startup — making development and updates easy without rebuilding images.

---

*Last updated: May 2026 | Smriti Retail OS v1.0.0*
