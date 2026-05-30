<div align="center">
  <img src="apps/smriti_retail_os/smriti_retail_os/public/images/logo.svg" alt="SMRITI Retail OS" width="120" />
  <h1>SMRITI Retail OS</h1>
  <p>Official Docker Orchestration for the SMRITI Retail Experience Layer.</p>
  <p><b>Stable Production Release: <code>v1.0.0</code></b> 🚀</p>
</div>

---

## ⚡ Quick Install

**Windows (PowerShell):**
```powershell
git clone https://github.com/erpnbook/smriti-docker.git smriti_retail
cd smriti_retail
.\install.ps1
```

> [!TIP]
> If Windows blocks the execution with a `SecurityError` (running scripts is disabled), run the installer with a bypass policy instead:
> ```powershell
> PowerShell -ExecutionPolicy Bypass -File .\install.ps1
> ```

**Linux / macOS (Bash):**
```bash
git clone https://github.com/erpnbook/smriti-docker.git smriti_retail
cd smriti_retail
bash install.sh
```

> 📖 **For a full step-by-step guide, see [INSTALL.md](./INSTALL.md)**

Once complete → open **http://localhost:8080** — login with `Administrator / admin`

---

## What is this?

This repository contains the official Docker Compose configuration and orchestration required to run **SMRITI Retail OS**. It provides a fully pre-configured, production-ready environment that integrates:

- **Frappe Framework v16**
- **ERPNext v16** (Core Business Logic, Inventory, Accounting)
- **India Compliance** (GST, E-Invoicing, Audit Trail)
- **SMRITI Retail OS App (`v1.0.0`)** (Premium Retail Experience Layer, POS Billing, Material Transfers)

---

## Prerequisites

| Requirement | Install Link |
|---|---|
| Docker Desktop | https://docs.docker.com/get-docker/ |
| Git | https://git-scm.com/ |
| 4 GB RAM free | — |
| Port 8080 free | — |

---

## Features of this Setup

- **One-Command Installer**: `install.ps1` (Windows) and `install.sh` (Linux/macOS) handle everything end-to-end — cloning apps, launching containers, creating the site, and syncing assets.
- **Pre-flight Validator**: Run `.\check.ps1` before or after install to verify prerequisites and container health.
- **Automated Installation & Config**: The `pwd.yml` workflow automatically mounts required folders, installs custom apps, and sets up site credentials.
- **Robust Physical Asset Sync**: Custom built-in hard-sync utility (`sync_assets`) that unlinks complex app symlinks and copies physical bundles straight to Nginx, completely bypassing Nginx MIME-type/404 errors.
- **Day-to-day Operations Optimized**: Fully pre-allocated queues (long, short) and background workers.
- **High Stability**: Integrated 19/19 passing automated test suite.

---

## Verify Your Installation

```powershell
# Windows — run health check at any time
.\check.ps1
```

Expected: all checks show ✔

---

## Running Automated Tests

```bash
docker exec smriti_retail-backend-1 bench --site frontend run-tests --app smriti_retail_os
```
*(All 19/19 tests must complete with **`OK`** status)*

---

## Updating to a New Version

To pull the latest changes and update the application inside Docker:

```bash
# 1. Pull the latest code in the app directory
cd apps/smriti_retail_os && git pull origin main && cd ../..

# 2. Build assets inside the container
docker exec smriti_retail-backend-1 bench build --app smriti_retail_os

# 3. Migrate database (if schema changed)
docker exec smriti_retail-backend-1 bench --site frontend migrate

# 4. Sync assets to the shared volume
docker exec smriti_retail-backend-1 /home/frappe/frappe-bench/env/bin/python /home/frappe/frappe-bench/apps/smriti_retail_os/smriti_retail_os/sync_assets.py

# 5. Clear cache
docker exec smriti_retail-backend-1 bench --site frontend clear-cache
```

---

## SMRITI UI Conventions

- **Shoper9 Pure Mode**: Simplifies complex ERPNext views (like Sales Invoices) down to essential POS columns (`Item Code`, `Item Name`, `Qty`, `Rate`, `Amount`), hiding accounting/warehouse clutter for cashiers.
- **Glassmorphic Dashboards**: Stunning custom cards with backdrop blur filters and dynamic hover actions that match modern web layouts.
- **System Manager Bypass**: Standard System Managers are completely unaffected and see the un-altered, full-featured ERPNext interface.

---

## Troubleshooting

| Symptom | Quick Fix |
|---|---|
| Backend keeps restarting | `apps/smriti_retail_os/` is empty — re-run `.\install.ps1` |
| `502 Bad Gateway` | `docker restart smriti_retail-frontend-1` |
| Blank/unstyled UI | Run asset sync step in INSTALL.md |
| `Invalid credentials` | `bench --site frontend set-admin-password NewPass` |

See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for complete solutions.

---

## License

This orchestration setup is provided under the MIT License.
