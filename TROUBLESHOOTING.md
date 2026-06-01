# 🛠️ Smriti Retail OS — Docker Troubleshooting Guide

> This guide documents real issues encountered during deployment and how to fix them.

---

## 📋 Quick Reference — Diagnostic Commands

```powershell
# 1. List ALL running containers and their status
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 2. Check logs for a specific container (last 50 lines)
docker logs smriti_retail-backend-1 --tail 50

# 3. List all containers (including stopped ones)
docker ps -a --format "table {{.Names}}\t{{.Status}}"

# 4. Check what's mounted inside the container
docker exec smriti_retail-backend-1 ls -la /home/frappe/frappe-bench/apps/

# 5. Check a specific app's files inside the container
docker exec smriti_retail-backend-1 ls -la /home/frappe/frappe-bench/apps/smriti_retail_os/

# 6. Check container environment variables
docker inspect smriti_retail-backend-1 | findstr -i "env"
```

---

## 🔴 Issue 1: "No such container: demotest-backend-1"

### Symptom
```
Error response from daemon: No such container: demotest-backend-1
```

### Root Cause
Docker Compose names containers based on the **folder name** where `compose.yaml` lives, **not** what you expect.

| Folder Name | Container Name Pattern |
|---|---|
| `smriti_retail` | `smriti_retail-backend-1` |
| `demotest` | `demotest-backend-1` |
| `my_project` | `my_project-backend-1` |

### Fix
Always first run `docker ps` to find the **actual** container names:

```powershell
docker ps --format "table {{.Names}}\t{{.Status}}"
```

Then use the correct name:
```powershell
# ✅ Correct
docker exec -it smriti_retail-backend-1 bench --site smriti_retail migrate

# ❌ Wrong (assumes folder name = "demotest")
docker exec -it demotest-backend-1 bench --site smriti_retail migrate
```

> [!TIP]
> The container name = `<folder_name>-<service_name>-1`. The folder name is the name of the directory containing `compose.yaml`.

---

## 🔴 Issue 2: Backend keeps Restarting — "neither 'setup.py' nor 'pyproject.toml' found"

### Symptom
```
docker ps  →  smriti_retail-backend-1  Restarting (1) 58 seconds ago
```
```
docker logs smriti_retail-backend-1 --tail 20
→ ERROR: file:///home/frappe/frappe-bench/apps/smriti_retail_os does not appear to be a Python project:
   neither 'setup.py' nor 'pyproject.toml' found.
```

### Root Cause
The `apps/smriti_retail_os/` folder on the Windows host is **empty**. The volume mount puts an empty folder into the container, so pip cannot install the app.

### Verify
```powershell
# On Windows host — should show files like pyproject.toml, hooks.py, etc.
Get-ChildItem D:\demotest\smriti_retail\apps\smriti_retail_os

# Inside the container — should show same files
docker exec smriti_retail-frontend-1 ls -la /home/frappe/frappe-bench/apps/smriti_retail_os/
```

If the folder is empty on the host → the app source was never copied there.

### Fix
Copy the app source from your main workspace:

```powershell
# Copy smriti_retail_os app source
Copy-Item -Path "D:\Smriti_Retail_OS\apps\smriti_retail_os\*" `
          -Destination "D:\demotest\smriti_retail\apps\smriti_retail_os\" `
          -Recurse -Force

# Copy india_compliance app source (if also empty)
Copy-Item -Path "D:\Smriti_Retail_OS\apps\india_compliance\*" `
          -Destination "D:\demotest\smriti_retail\apps\india_compliance\" `
          -Recurse -Force

# Restart the crashed containers
cd D:\demotest\smriti_retail
docker compose restart backend scheduler queue-long queue-short
```

Then wait ~30 seconds and verify:
```powershell
docker ps --format "table {{.Names}}\t{{.Status}}"
# All containers should show "Up X seconds" — not "Restarting"
```

---

## 🔴 Issue 3: "sites/common_site_config.json found" — Site Already Exists

### Symptom
```
Site smriti_retail already exists, use `--force` to proceed anyway
```

### Root Cause
The site was already created in a previous run. Docker setup scripts detect this and skip re-creation, but the message can look alarming.

### What to Do
**This is usually fine.** It means the site was previously initialized. Just wait for containers to become healthy.

If you need to **force re-create** the site (⚠️ destroys all data):
```powershell
cd D:\demotest\smriti_retail
docker compose down -v   # removes volumes including DB data
docker compose up -d     # starts fresh
```

If you just want to **run migrations** on the existing site:
```powershell
docker exec -it smriti_retail-backend-1 bench --site smriti_retail migrate
```

---

## 🔴 Issue 4: "ERPNEXT_VERSION variable is not set"

### Symptom
```
level=warning msg="The "ERPNEXT_VERSION" variable is not set. Defaulting to a blank string."
```

### Root Cause
The `.env` file is missing or the variable is not set.

### Fix
```powershell
# Check if .env exists
Get-Item D:\demotest\smriti_retail\.env

# If missing, copy from example
Copy-Item D:\demotest\smriti_retail\example.env D:\demotest\smriti_retail\.env

# Edit .env and set ERPNEXT_VERSION
notepad D:\demotest\smriti_retail\.env
```

Set the value:
```env
ERPNEXT_VERSION=version-15
```

> [!NOTE]
> This warning doesn't crash anything — it's cosmetic. But fixing it avoids confusion.

---

## 🔴 Issue 5: wait-for-it: waiting 120 seconds for db:3306

### Symptom
```
wait-for-it: waiting 120 seconds for db:3306
```

### Root Cause
The database container (`db`) is not ready yet. This is normal on first startup — MariaDB takes 30–90 seconds to initialize.

### What to Do
**Wait.** If after 2 minutes the backend still crashes, check:
```powershell
# Is the DB container healthy?
docker ps --format "table {{.Names}}\t{{.Status}}" | Select-String "db"
# Should show: smriti_retail-db-1   Up X minutes (healthy)

# Check DB logs
docker logs smriti_retail-db-1 --tail 30
```

If DB is failing, check disk space:
```powershell
Get-PSDrive C | Select-Object Used, Free
```

---

## 🟡 Issue 6: Running Migrations After Code Changes

### When to Run
Run `bench migrate` after:
- Pulling new code from GitHub
- Adding new DocTypes or fields
- Updating app version

### Command
```powershell
# First confirm the backend is UP (not Restarting)
docker ps --format "table {{.Names}}\t{{.Status}}"

# Then run migration
docker exec -it smriti_retail-backend-1 bench --site smriti_retail migrate
```

### If Migration Fails
```powershell
# Check migration logs inside container
docker exec smriti_retail-backend-1 cat /home/frappe/frappe-bench/logs/migrate.log

# Check recent bench logs
docker exec smriti_retail-backend-1 cat /home/frappe/frappe-bench/logs/bench.log | tail -50
```

---

## 🟡 Issue 7: Frontend Shows Old Code / Changes Not Reflected

### Fix — Clear Cache and Rebuild Assets
```powershell
# Clear server cache
docker exec smriti_retail-backend-1 bench --site smriti_retail clear-cache

# Rebuild JS/CSS assets
docker exec smriti_retail-backend-1 bench build --app smriti_retail_os

# Or rebuild all assets
docker exec smriti_retail-backend-1 bench build
```

---

## 🔴 Issue 8: "ModuleNotFoundError: No module named 'erpnextindia_compliance'"

### Symptom
```
ModuleNotFoundError: No module named 'erpnextindia_compliance'
```
Containers like `queue-long`, `queue-short`, `scheduler` keep restarting.

### Root Cause
The `apps.txt` file inside the container is **corrupted** — entries got merged together or duplicated.

### Verify
```powershell
docker exec smriti_retail-backend-1 cat /home/frappe/frappe-bench/sites/apps.txt
```

**Bad output** (merged/duplicated):
```
smriti_retail_os
erpnextindia_compliance   ← "erpnext" + "india_compliance" merged!
erpnext
frappe
india_compliance
erpnext                    ← duplicate
frappe                     ← duplicate
```

**Good output**:
```
frappe
erpnext
india_compliance
smriti_retail_os
```

### Fix
```powershell
docker exec smriti_retail-backend-1 bash -c "printf 'frappe\nerpnext\nindia_compliance\nsmriti_retail_os\n' > /home/frappe/frappe-bench/sites/apps.txt"

# Restart affected containers
docker compose restart scheduler queue-long queue-short
```

> [!WARNING]
> The order matters: `frappe` must come first, then `erpnext`, then dependent apps. Each app name must be on its own line with no extra spaces.

---

## 🔴 Issue 9: "404 Not Found: smriti_retail does not exist" — Site Never Created

### Symptom
```
bench --site smriti_retail migrate
→ Error: 404 Not Found: smriti_retail does not exist.
```

### Root Cause
The `smriti_retail` site was never created. The `create-site` service in `pwd.yml` either failed or was never run. Also, `common_site_config.json` may be empty `{}`.

### Verify
```powershell
# Check what sites exist
docker exec smriti_retail-backend-1 ls /home/frappe/frappe-bench/sites/
# If you only see: apps.json  apps.txt  assets  common_site_config.json
# → No site directory = site was never created

# Check config
docker exec smriti_retail-backend-1 cat /home/frappe/frappe-bench/sites/common_site_config.json
# If output is just {} → config is empty, needs to be set first
```

### Fix — Step 1: Set config (if empty)
```powershell
docker exec smriti_retail-backend-1 bash -c "
  bench set-config -g db_host db &&
  bench set-config -gp db_port 3306 &&
  bench set-config -g redis_cache 'redis://redis-cache:6379' &&
  bench set-config -g redis_queue 'redis://redis-queue:6379' &&
  bench set-config -g redis_socketio 'redis://redis-queue:6379' &&
  bench set-config -gp socketio_port 9000
"
```

### Fix — Step 2: Create the site
```powershell
docker exec smriti_retail-backend-1 bench new-site ^
  --mariadb-user-host-login-scope='%' ^
  --admin-password=admin ^
  --db-root-username=root ^
  --db-root-password=admin ^
  --install-app erpnext ^
  --install-app india_compliance ^
  --install-app smriti_retail_os ^
  --set-default smriti_retail
```

This takes 2-5 minutes. After completion:
```powershell
# Build frontend assets
docker exec smriti_retail-backend-1 bench --site smriti_retail build --app smriti_retail_os --app india_compliance

# Open the site
Start-Process "http://localhost:8080"
# Login: Administrator / admin
```

> [!IMPORTANT]
> If `common_site_config.json` is empty, you **must** set the config before creating the site, otherwise `bench new-site` will fail because it can't connect to the database.

---

## 🔴 Issue 10: "running scripts is disabled" — Windows PowerShell Execution Policy Restriction

### Symptom
```powershell
.\install.ps1 : File D:\smriti_retail\install.ps1 cannot be loaded because running scripts is disabled on this system.
For more information, see about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170.
CategoryInfo          : SecurityError: (:) [], PSSecurityException
FullyQualifiedErrorId : UnauthorizedAccess
```

### Root Cause
Windows security blocks the execution of unsigned third-party scripts by default. The local PowerShell Execution Policy is set to `Restricted`.

### Fix
You do not need to change your global Windows security configuration. Run the installer script with a one-time execution policy bypass:

```powershell
PowerShell -ExecutionPolicy Bypass -File .\install.ps1
```

Alternatively, if you want to permanently allow local scripts for your current Windows user, run this command:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then run the installer as usual:
```powershell
.\install.ps1
```

---

## ✅ Full Health Check — Run This First

Before debugging any issue, run this full health check:

```powershell
# Step 1: Are all containers running?
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Step 2: Are app files present in the container?
docker exec smriti_retail-frontend-1 ls /home/frappe/frappe-bench/apps/smriti_retail_os/

# Step 3: Is the site accessible?
Start-Process "http://localhost:8080"

# Step 4: Check backend logs for errors
docker logs smriti_retail-backend-1 --tail 30
```

### Expected Healthy Output for Step 1:
| Container | Status |
|---|---|
| `smriti_retail-frontend-1` | Up X minutes |
| `smriti_retail-backend-1` | Up X minutes |
| `smriti_retail-scheduler-1` | Up X minutes |
| `smriti_retail-queue-long-1` | Up X minutes |
| `smriti_retail-queue-short-1` | Up X minutes |
| `smriti_retail-websocket-1` | Up X minutes |
| `smriti_retail-redis-queue-1` | Up X minutes |
| `smriti_retail-redis-cache-1` | Up X minutes |
| `smriti_retail-db-1` | Up X minutes (healthy) |

> [!IMPORTANT]
> If **any** container shows `Restarting` → run `docker logs <container-name> --tail 30` to find the error.

---

## 📂 Understanding the Folder → Container Name Mapping

```
D:\demotest\smriti_retail\        ← compose.yaml lives here
         ↓
Folder name = "smriti_retail"
         ↓
Container names:
  smriti_retail-backend-1
  smriti_retail-frontend-1
  smriti_retail-db-1
  smriti_retail-scheduler-1
  smriti_retail-queue-long-1
  smriti_retail-queue-short-1
  smriti_retail-websocket-1
  smriti_retail-redis-queue-1
  smriti_retail-redis-cache-1
```

## 📂 Volume Mount — Where App Source Goes

```
Windows Host                            →   Inside Container
D:\demotest\smriti_retail\apps\
  smriti_retail_os\    (must have files) →  /home/frappe/frappe-bench/apps/smriti_retail_os/
  india_compliance\    (must have files) →  /home/frappe/frappe-bench/apps/india_compliance/
```

> [!CAUTION]
> If either `apps/<app_name>/` folder is empty on the host, the backend will crash in a restart loop. Always verify files exist with `Get-ChildItem D:\demotest\smriti_retail\apps\smriti_retail_os`.

---

## 🔄 Complete Reset (Nuclear Option)

If everything is broken and you want a fresh start:

```powershell
cd D:\demotest\smriti_retail

# Stop and remove all containers + volumes (⚠️ DELETES ALL DATA)
docker compose down -v

# Re-copy app source files
Copy-Item -Path "D:\Smriti_Retail_OS\apps\smriti_retail_os\*" `
          -Destination "D:\demotest\smriti_retail\apps\smriti_retail_os\" `
          -Recurse -Force

Copy-Item -Path "D:\Smriti_Retail_OS\apps\india_compliance\*" `
          -Destination "D:\demotest\smriti_retail\apps\india_compliance\" `
          -Recurse -Force

# Start fresh
docker compose up -d

# Watch logs
docker compose logs -f backend
```

---

*Last updated: June 2026 | Smriti Retail OS Docker Deployment*
