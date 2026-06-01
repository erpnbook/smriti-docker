# Smriti Retail OS — Developer Troubleshooting Guide

> **Environment**: Dockerized ERPNext / Frappe v15 + `smriti_retail_os` custom app  
> **Compose file**: `pwd.yml` / `compose.yaml` in `D:\demotest\smriti_retail\`  
> **Source**: `D:\Smriti_Retail_OS\` (bind-mounted into containers)

---

## Table of Contents

1. [Quick Health Check](#1-quick-health-check)
2. [502 Bad Gateway](#2-502-bad-gateway)
3. [CSS / JS MIME Type Errors (Blank/Unstyled UI)](#3-css--js-mime-type-errors-blankunstyled-ui)
4. [Asset Symlink Hash Mismatch](#4-asset-symlink-hash-mismatch)
5. [Invalid Credentials / Can't Log In](#5-invalid-credentials--cant-log-in)
6. [Socket.IO "Invalid Origin" Error](#6-socketio-invalid-origin-error)
7. [Site Not Initialized / App Not Installed](#7-site-not-initialized--app-not-installed)
8. [Boot Loops / Container Keeps Restarting](#8-boot-loops--container-keeps-restarting)
9. [Unit Tests Failing](#9-unit-tests-failing)
10. [Bench Commands Reference](#10-bench-commands-reference)
11. [Full Reset Procedure](#11-full-reset-procedure)

---

## 1. Quick Health Check

Run these first to understand overall container health:

```powershell
# Check all container statuses
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Check logs for any container (replace name as needed)
docker logs smriti_retail-backend-1 --tail 50
docker logs smriti_retail-frontend-1 --tail 50
docker logs smriti_retail-queue-long-1 --tail 30
docker logs smriti_retail-scheduler-1 --tail 30
```

**Expected healthy output:**

| Container | Status |
|---|---|
| smriti_retail-frontend-1 | Up |
| smriti_retail-backend-1 | Up |
| smriti_retail-queue-short-1 | Up |
| smriti_retail-queue-long-1 | Up |
| smriti_retail-scheduler-1 | Up |
| smriti_retail-db-1 | Up |
| smriti_retail-redis-cache-1 | Up |
| smriti_retail-redis-queue-1 | Up |

---

## 2. 502 Bad Gateway

### Symptoms
- Browser shows `502 Bad Gateway nginx/1.22.1`
- The login page never loads

### Root Cause
The Nginx (frontend) container cached the backend container's old IP address. When Docker restarts the backend, it gets a new IP, and Nginx can't reach it.

### Fix
```powershell
docker restart smriti_retail-frontend-1
```

Wait ~10 seconds, then refresh the browser. This forces Nginx to re-resolve the `backend` DNS name.

### Prevention
In `frappe.conf` Nginx config, ensure the resolver is set:
```nginx
resolver 127.0.0.11 valid=30s;
```
This makes Nginx re-resolve the backend hostname every 30 seconds automatically.

---

## 3. CSS / JS MIME Type Errors (Blank/Unstyled UI)

### Symptoms
Browser console shows:
```
Refused to apply style from 'http://localhost:8080/assets/frappe/dist/css/desk.bundle.XXXX.css'
because its MIME type ('text/html') is not a supported stylesheet MIME type
```
The ERPNext desk loads but has **no styling** (plain HTML).

### Root Cause
Nginx cannot find the requested CSS/JS file (because the file hash doesn't match what's on disk), so it falls back to serving `index.html` — which has MIME type `text/html`.

This happens because `sites/assets/frappe` is a **symlink** pointing to the local app's `public/` directory inside the container. When two containers mount different versions of `apps/frappe/`, they each compile different bundles with different hash suffixes. The backend serves an `assets.json` referencing its own hashes, but Nginx resolves the symlink to its own (older/different) bundles.

### Fix
See **Section 4** below — replace symlinks with real copies.

---

## 4. Asset Symlink Hash Mismatch

### Diagnosis
```powershell
# Check what hashes the BACKEND has
docker exec smriti_retail-backend-1 ls /home/frappe/frappe-bench/sites/assets/frappe/dist/css/

# Check what hashes the FRONTEND (Nginx) has
docker exec smriti_retail-frontend-1 ls /home/frappe/frappe-bench/sites/assets/frappe/dist/css/
```

If the filenames differ (e.g. `desk.bundle.O6JOEGF7.css` vs `desk.bundle.B6MACVOP.css`), you have a hash mismatch.

### Fix — Replace Symlinks with Real Copies

Save this as `fix_assets.py` and copy it into the backend container:

```python
import os
import shutil

d = '/home/frappe/frappe-bench/sites/assets'
apps = ['frappe', 'erpnext', 'india_compliance', 'smriti_retail_os']

for app in apps:
    path = os.path.join(d, app)
    if os.path.islink(path):
        target = os.readlink(path)
        print(f"Replacing symlink: {path} -> {target}")
        os.unlink(path)
        shutil.copytree(target, path, symlinks=False)
        print(f"  Done: {app}")
    elif not os.path.exists(path):
        # Symlink was previously removed but copy failed — copy directly
        src = f"/home/frappe/frappe-bench/apps/{app}/{app}/public"
        print(f"Copying missing: {src} -> {path}")
        shutil.copytree(src, path, symlinks=False)
        print(f"  Done: {app}")
    else:
        print(f"  Already real dir: {app}")
```

```powershell
# Copy and run
docker cp fix_assets.py smriti_retail-backend-1:/tmp/fix_assets.py
docker exec smriti_retail-backend-1 python3 /tmp/fix_assets.py

# Restart Nginx to pick up changes
docker restart smriti_retail-frontend-1
```

### Permanent Prevention
In `compose.yaml` / `pwd.yml`, use a **single shared named volume** (`smriti_retail_sites`) for `sites/` in ALL containers. Avoid bind-mounting `apps/` separately into the frontend container — this causes divergent symlink targets.

---

## 5. Invalid Credentials / Can't Log In

### Symptoms
Entering correct password shows `Invalid credentials. Please try again.`

### Fix A — Reset Administrator Password
```powershell
docker exec smriti_retail-backend-1 bench --site smriti_retail set-admin-password NewPassword123
```

### Fix B — Check Site Name
```powershell
# List available sites
docker exec smriti_retail-backend-1 ls /home/frappe/frappe-bench/sites/
```
The site must match what's in `common_site_config.json`:
```powershell
docker exec smriti_retail-backend-1 cat /home/frappe/frappe-bench/sites/common_site_config.json
```
Look for `"default_site": "smriti_retail"` (or whatever your site name is).

### Fix C — Rebuild Auth Cache
```powershell
docker exec smriti_retail-backend-1 bench --site smriti_retail clear-cache
docker restart smriti_retail-backend-1
```

---

## 6. Socket.IO "Invalid Origin" Error

### Symptoms
Browser console shows:
```
Error connecting to socket.io: Invalid origin
```
Real-time features (notifications, form updates) don't work.

### Root Cause
The `socketio` container rejects WebSocket connections from origins not in its allowed list.

### Fix
Add your host URL to `common_site_config.json`:
```powershell
docker exec smriti_retail-backend-1 bench config set-common-config -c allow_cors_origin "http://localhost:8080"
docker restart smriti_retail-websocket-1
```

Or edit `sites/common_site_config.json` directly to add:
```json
{
  "allow_cors_origin": "http://localhost:8080",
  "socketio_port": 9000
}
```

---

## 7. Site Not Initialized / App Not Installed

### Symptoms
- ERPNext shows `Site not found` or redirects to `/login` with a database error
- Frappe desk loads but ERPNext modules are missing

### Check Site Status
```powershell
docker exec smriti_retail-backend-1 bench --site smriti_retail list-apps
```

### Create Site from Scratch
```powershell
docker exec smriti_retail-backend-1 bench new-site smriti_retail \
  --mariadb-root-password=admin \
  --admin-password=admin \
  --install-app erpnext \
  --install-app india_compliance \
  --install-app smriti_retail_os
```

### Install a Missing App on Existing Site
```powershell
docker exec smriti_retail-backend-1 bench --site smriti_retail install-app smriti_retail_os
docker exec smriti_retail-backend-1 bench --site smriti_retail migrate
```

---

## 8. Boot Loops / Container Keeps Restarting

### Symptoms
`docker ps` shows container status cycling through `Restarting` or `Exited`.

### Diagnosis
```powershell
docker logs smriti_retail-backend-1 --tail 100
```

### Common Causes & Fixes

| Error in Logs | Cause | Fix |
|---|---|---|
| `apps.txt: No such file` | Corrupted bench setup | `docker exec ... bash -c "echo -e 'frappe\nerpnext\nsmriti_retail_os' > apps/frappe-bench/apps.txt"` |
| `common_site_config.json not found` | Missing config | Copy/create the JSON file in `sites/` |
| `Can't connect to MySQL` | DB not ready | Wait 30s, or check `smriti_retail-db-1` logs |
| `ModuleNotFoundError` | App source missing | Check bind mounts in `compose.yaml` |

---

## 9. Unit Tests Failing

### Run Tests
```powershell
docker exec smriti_retail-backend-1 bench --site smriti_retail run-tests --app smriti_retail_os
```

### Common Failures

**`LinkValidationError: Transit not found in Warehouse Type`**
```python
# In setUp() of your test class, create the missing master:
frappe.get_doc({
    "doctype": "Warehouse Type",
    "name": "Transit"
}).insert(ignore_if_duplicate=True)
```

**`MandatoryError: cost_center`**  
Ensure `cost_center` is explicitly set on all Sales Invoice Item rows:
```python
company = frappe.defaults.get_defaults().get("company")
cost_center = frappe.get_value("Company", company, "cost_center")
for item in invoice.items:
    item.cost_center = cost_center
```

---

## 10. Bench Commands Reference

All bench commands must run **inside the backend container**:

```powershell
# Template
docker exec smriti_retail-backend-1 bench --site smriti_retail <command>
```

| Task | Command |
|---|---|
| Clear cache | `bench --site smriti_retail clear-cache` |
| Run migrations | `bench --site smriti_retail migrate` |
| Install app | `bench --site smriti_retail install-app <app>` |
| List installed apps | `bench --site smriti_retail list-apps` |
| Reset admin password | `bench --site smriti_retail set-admin-password <pwd>` |
| Run unit tests | `bench --site smriti_retail run-tests --app smriti_retail_os` |
| Build assets | `bench build --app frappe` |
| Rebuild assets (all) | `bench build` |
| Check asset paths | `bench --site smriti_retail execute "frappe.utils.get_url()"` |
| Restart services | `bench restart` (inside container) |

---

## 11. Full Reset Procedure

Use this when everything is broken and you want a clean slate:

> ⚠️ **This deletes all data.** Only use in development.

```powershell
# Step 1: Stop all containers
docker compose -f pwd.yml down

# Step 2: Remove volumes (wipes DB and sites)
docker volume rm smriti_retail_sites smriti_retail_logs

# Step 3: Restart fresh
docker compose -f pwd.yml up -d

# Step 4: Wait for DB to be ready (~30s), then create site
docker exec smriti_retail-backend-1 bench new-site smriti_retail `
  --mariadb-root-password=admin `
  --admin-password=admin `
  --install-app erpnext `
  --install-app india_compliance `
  --install-app smriti_retail_os

# Step 5: Fix asset symlinks (copy real bundles into shared volume)
docker cp fix_assets.py smriti_retail-backend-1:/tmp/fix_assets.py
docker exec smriti_retail-backend-1 python3 /tmp/fix_assets.py

# Step 6: Restart frontend to refresh DNS + pick up assets
docker restart smriti_retail-frontend-1

# Step 7: Open browser at http://localhost:8080
# Login: Administrator / admin
```

---

## Architecture Notes

```
Browser (port 8080)
     │
     ▼
[frontend] Nginx
  - Serves static assets from: /home/frappe/frappe-bench/sites/assets/
  - Proxies /api/, /app/, etc. to → [backend]:8000
     │
     ▼
[backend] Gunicorn (Frappe/ERPNext Python)
  - Serves assets.json with bundle hashes
  - Runs bench, migrations, etc.
     │
     ├─→ [db] MariaDB
     ├─→ [redis-cache] Redis
     ├─→ [redis-queue] Redis
     ├─→ [queue-short] RQ Worker
     ├─→ [queue-long] RQ Worker
     ├─→ [scheduler] Beat Scheduler
     └─→ [websocket] Socket.IO
```

**Key Volume**: `smriti_retail_sites` is shared between frontend and backend — this is how Nginx gets access to site files and assets.

**Critical**: `sites/assets/frappe`, `sites/assets/erpnext` etc. are normally **symlinks** inside the container. If frontend and backend containers have different app versions, the symlinks resolve to different compiled bundles → MIME errors. Always ensure both containers use the same image version, or replace symlinks with real copies (Section 4).

---

*Last updated: June 2026 | Smriti Retail OS v1.0*
