# SMRITI Retail OS — Production Troubleshooting Manual

This guide documents common issues encountered during installation, container orchestration, and daily operations of **SMRITI Retail OS**, along with their root causes and verified solutions.

---

## 📋 Quick Diagnostic Toolkit

Run these checks inside the repository folder to diagnose container and network health:

```powershell
# 1. Verify container states and mapped host ports
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 2. Check recent logs of the backend container
docker logs smriti_retail-backend-1 --tail 50

# 3. Check recent logs of the Nginx frontend proxy
docker logs smriti_retail-frontend-1 --tail 50

# 4. Check files inside the backend container mount
docker exec smriti_retail-backend-1 ls -la /home/frappe/frappe-bench/apps/smriti_retail_os/
```

---

## 🔌 1. SMRITI Label Studio & QZ Tray Issues

### 🔴 QZ Tray Not Connected / Not Running
- **Symptom**: SMRITI Label Studio (`/barcode`) shows `🔴 QZ Tray Not Running` and cannot detect USB/local printers.
- **Root Cause**: The QZ Tray local daemon is not running on the client computer, or the browser is blocking WebSocket connections to `localhost:8182`.
- **Fix**:
  1. Download and install QZ Tray from the official website on the local computer.
  2. Launch QZ Tray and verify its icon appears in the system tray.
  3. Allow localhost certificate: Open `https://localhost:8182` in a browser tab. If a security warning is shown, select **Advanced → Proceed to localhost (unsafe)** to whitelist the connection.
  4. Refresh the SMRITI Label Studio page to allow `initQZ()` to connect.

### 🔴 local USB Printer Not Detected
- **Symptom**: QZ Tray status shows green (`🟢 Connected`) but the local printer dropdown is empty.
- **Root Cause**: The thermal printer driver is not installed on the system, or the device is turned off/disconnected.
- **Fix**:
  1. Ensure the label printer is powered on and connected to a USB port.
  2. Install the manufacturer's printer driver (Zebra/TSC/etc.).
  3. Verify the printer appears in the OS Settings (Printers & Scanners).
  4. Click the **Refresh Printers** button in Label Studio.

---

## 🐳 2. Container & Docker Orchestration Issues

### 🔴 "No such container: demotest-backend-1"
- **Symptom**: Commands like `docker exec` fail with `No such container`.
- **Root Cause**: Docker Compose names containers using the parent directory name as a prefix (`<directory_name>-<service_name>-1`). If you cloned the repository to a folder named `smriti_retail`, your backend is named `smriti_retail-backend-1`, not `demotest-backend-1`.
- **Fix**:
  Run `docker ps` to find the actual running container names, and ensure you use the correct name prefix in your commands:
  ```powershell
  # Check actual names
  docker ps --format "{{.Names}}"
  
  # Execute with correct container name
  docker exec -it smriti_retail-backend-1 bench migrate
  ```

### 🔴 Backend in Restart Loop: "neither 'setup.py' nor 'pyproject.toml' found"
- **Symptom**: Backend container cycles through `Restarting` and logs show `does not appear to be a Python project`.
- **Root Cause**: The host folder `apps/smriti_retail_os` is empty. Because the directory is bind-mounted, an empty directory inside the container blocks pip from installing the application metadata.
- **Fix**:
  Ensure you have run the clone commands in `INSTALL.md` or copied your workspace files into `apps/smriti_retail_os/` before launching the stack:
  ```powershell
  # Verify files exist on host
  Get-ChildItem apps\smriti_retail_os\
  ```

### 🔴 "ERPNEXT_VERSION variable is not set"
- **Symptom**: Docker compose prints warnings: `The "ERPNEXT_VERSION" variable is not set. Defaulting to blank string`.
- **Root Cause**: The environment configuration file `.env` is missing or variables are empty.
- **Fix**:
  Copy the example configuration file and set target versions:
  ```bash
  cp example.env .env
  ```

### 🔴 Nginx "502 Bad Gateway"
- **Symptom**: Opening `http://localhost:8765` (or your configured `HTTP_PUBLISH_PORT`) in the browser returns a `502 Bad Gateway` error.
- **Root Cause**: The Nginx container cached the backend container's old IP address after a restart.
- **Fix**:
  Restart the Nginx frontend proxy to force it to re-resolve backend DNS mappings:
  ```bash
  docker restart smriti_retail-frontend-1
  ```

### 🔴 Socket.IO "Invalid Origin" Error
- **Symptom**: Browser console logs `Error connecting to socket.io: Invalid origin`.
- **Root Cause**: The websocket container rejects incoming Socket.IO requests from origins not explicitly permitted in configuration settings.
- **Fix**:
  Configure allowed origins in `common_site_config.json` (replacing `8765` with your host port if customized):
  ```bash
  docker exec smriti_retail-backend-1 bench config set-common-config -c allow_cors_origin "http://localhost:8765"
  docker compose restart websocket
  ```

### 🔴 "wait-for-it: waiting 120 seconds for db:3306"
- **Symptom**: Backend startup logs halt at database socket connection checks.
- **Root Cause**: MariaDB takes 30-90 seconds to initialize database tables on first launch.
- **Fix**:
  Wait for the check to complete. If it times out, verify database health:
  ```powershell
  docker logs smriti_retail-db-1
  ```

### 🔴 Container "create-site" Fails with Exit Code 1
- **Symptom**: The initialization container `create-site-1` exits with an error status, and the installer script halts with `[XX] docker compose up failed`.
- **Root Causes**:
  1. **Incomplete App Source**: The `apps/smriti_retail_os/` or `apps/india_compliance/` directories are empty or missing (usually because the user ran `docker compose` directly instead of using the automated installation scripts).
  2. **Corrupted Database/Volume State**: A previous half-initialized run left partial tables, causing migration errors on subsequent boots.
  3. **WSL2 / Docker Memory Depletion (OOM)**: ERPNext provisions 1000+ tables. If the system RAM allocated to Docker is low, the database container crashes during `bench new-site`.
- **Fixes**:
  1. **Force Reset and Clean Re-run** (highly recommended):
     Use the installer script's built-in reset command to destroy half-created volumes and database states, then start fresh:
     ```powershell
     PowerShell -ExecutionPolicy Bypass -File .\install.ps1 -Force
     ```
  2. **Check App Directory Files**:
     Verify that `apps/smriti_retail_os/pyproject.toml` and `apps/india_compliance/pyproject.toml` exist.
  3. **Allocate More Memory to WSL2**:
     Add `memory=6GB` (or `8GB`) to `%USERPROFILE%\.wslconfig` and restart WSL using `wsl --shutdown` in PowerShell.
  4. **Run Diagnostics Logs**:
     Retrieve the container logs to find the exact line of failure:
     ```powershell
     docker logs smriti_retail-create-site-1
     ```

---

## 🎨 3. UI & Static Asset Sync Issues

### 🔴 Blank or Unstyled UI (CSS/JS MIME-type blockages)
- **Symptom**: The login or desk page loads as plain HTML with no CSS styling. Browser console shows:
  `Refused to apply style because its MIME type ('text/html') is not a supported stylesheet MIME type`.
- **Root Cause**: Nginx cannot resolve symbolic links or is requesting file hashes that mismatch those compiled by the backend server.
- **Fix**:
  Force a physical rebuild and copy compiled bundles straight to the Nginx shared volume using SMRITI's asset synchronization utility:
  ```bash
  docker exec smriti_retail-backend-1 bench build --app smriti_retail_os
  docker exec smriti_retail-backend-1 bench --site smriti_retail execute smriti_retail_os.sync_assets.sync_assets
  docker restart smriti_retail-frontend-1
  ```

---

## 🔑 4. Authentication & Site Database Issues

### 🔴 "Invalid credentials" (Lost Admin Password)
- **Symptom**: Correct password attempts reject logins.
- **Root Cause**: The database user credentials have been modified, or password hashing caches are out of sync.
- **Fix**:
  Run a console reset command inside the backend container:
  ```bash
  docker exec smriti_retail-backend-1 bench --site smriti_retail set-admin-password "YourNewSecurePassword!"
  ```

### 🔴 "404 Not Found: smriti_retail does not exist"
- **Symptom**: Bench commands fail claiming the site does not exist.
- **Root Cause**: The `smriti_retail` site folder was deleted, or `common_site_config.json` was cleared.
- **Fix**:
  1. Verify the site directory is present:
     ```bash
     docker exec smriti_retail-backend-1 ls /home/frappe/frappe-bench/sites/
     ```
  2. If missing, restore the site database using SMRITI's restore procedures, or initialize a fresh database:
     ```bash
     docker exec smriti_retail-backend-1 bench new-site smriti_retail --admin-password=YourSecurePassword
     ```

### 🔴 ModuleNotFoundError: No module named 'erpnextindia_compliance'
- **Symptom**: Background queues fail starting, claiming modules are missing.
- **Root Cause**: The `apps.txt` file inside the sites folder is corrupted (e.g. `erpnext` and `india_compliance` lines merged together).
- **Fix**:
  Rewrite `apps.txt` with correct single-line entries:
  ```bash
  docker exec smriti_retail-backend-1 bash -c "printf 'frappe\nerpnext\nindia_compliance\nsmriti_retail_os\n' > /home/frappe/frappe-bench/sites/apps.txt"
  docker compose restart scheduler queue-long queue-short
  ```

---

## 🧪 5. Unit Tests Failing

### 🔴 "LinkValidationError: Transit not found in Warehouse Type"
- **Symptom**: Unit tests fail during setUp execution because of missing core database records.
- **Root Cause**: The test site runs on an empty database sandbox and requires basic Warehouse Type schemas to exist.
- **Fix**:
  Create the missing record in the test class setUp:
  ```python
  frappe.get_doc({
      "doctype": "Warehouse Type",
      "name": "Transit"
  }).insert(ignore_if_duplicate=True)
  ```

### 🔴 "MandatoryError: cost_center" on Invoice Saves
- **Symptom**: Invoice generation tests crash complaining that Cost Center fields are empty.
- **Root Cause**: In ERPNext v16, cost centers are mandatory for accounting ledger splits.
- **Fix**:
  Query the default company cost center and set it on child items:
  ```python
  company = frappe.defaults.get_defaults().get("company")
  cc = frappe.get_value("Company", company, "cost_center")
  for item in invoice.items:
      item.cost_center = cc
  ```

---

## ⌨️ 6. Bench Commands Reference

All command entries must run within the context of the backend container:

```bash
docker exec -it smriti_retail-backend-1 bench --site smriti_retail <command>
```

| Operational Goal | Bench Command |
|---|---|
| Run Migrations | `bench --site smriti_retail migrate` |
| Rebuild CSS/JS Assets | `bench build` |
| Clear Server Caches | `bench --site smriti_retail clear-cache` |
| Reset Administrator Password | `bench --site smriti_retail set-admin-password <new_password>` |
| Execute Unit Tests | `bench --site smriti_retail run-tests --app smriti_retail_os` |

---

## ⚡ 7. Execution Policy Restrictions (Windows)

### 🔴 SecurityError: Running scripts is disabled on this system
- **Symptom**: Running `.\install.ps1` or `.\check.ps1` returns a PowerShell `SecurityError`.
- **Root Cause**: Windows client OS disables script execution by default.
- **Fix**:
  Run the scripts using a one-time execution policy bypass:
  ```powershell
  PowerShell -ExecutionPolicy Bypass -File .\install.ps1
  ```

---

## ⚠️ 8. Full Stack Reset Procedure (Nuclear Option)

Use this only in local development to purge corrupted containers and start fresh:
> [!CAUTION]
> This command will permanently delete all local database ledgers and file attachments.

```powershell
# 1. Stop containers and destroy mapped volumes
docker compose -f pwd.yml down -v

# 2. Re-create the docker container environment
docker compose -f pwd.yml up -d

# 3. Create a fresh site and install packages (takes 2-5 minutes)
docker exec smriti_retail-backend-1 bench new-site smriti_retail \
  --mariadb-root-password=admin \
  --admin-password=YourSecurePassword \
  --install-app erpnext \
  --install-app india_compliance \
  --install-app smriti_retail_os

# 4. Copy and build assets
docker exec smriti_retail-backend-1 bench --site smriti_retail execute smriti_retail_os.sync_assets.sync_assets
docker restart smriti_retail-frontend-1
```
