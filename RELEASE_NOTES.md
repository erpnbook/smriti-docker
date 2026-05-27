# 🚀 Release Notes — SMRITI Retail OS v1.0.0 (Production Release)

We are proud to present **SMRITI Retail OS `v1.0.0`**, the first fully stable production release of the Docker Orchestration stack for ERPNext + India Compliance + SMRITI Experience Layer!

This release represents a complete hardening of container mounts, database schema initializations, physical asset compilation, Nginx caching, and isolated unit test runner boundaries.

---

## 🎯 Release Highlights (`v1.0.0`)

### 1. 🏗️ Robust Container Bootstrap (`pwd.yml`)
- Fixed missing volume mounts in `pwd.yml` for custom apps (`smriti_retail_os` and `india_compliance`).
- Backend processes (`configurator`, `queue-long`, `queue-short`, and `scheduler`) compile dependencies correctly.
- Completely prevents container startup crashes and ensures seamless site creation.

### 2. ⚡ Physical Asset Pipeline (No Symlinks)
- Implemented a custom physical asset hard-sync utility (`sync_assets.py`) that unlinks complex app symlinks inside the bench `/assets/` directory.
- Directly hard-copies compiled esbuild bundles (like `desk.bundle.css`, `erpnext.bundle.css`) straight to the shared Nginx assets volume.
- Resolves all browser console MIME-type stylesheet failures (`text/html` strictly checked blocking).

### 3. 🗄️ Automated Database Provisioning
- Automatically creates and binds all missing retail custom fields (MRP, stock HTML summaries, birthday, anniversary, credit terms) inside MariaDB via `setup.py`.
- Realigned reporting and shift APIs to target official ERPNext v16 tables (`Sales Invoice Payment` and `billing_address_gstin`).

### 4. 🎨 Shoper9 Pure Mode (Sales Invoice Makeover)
- Simplifies complex invoice grids for store cashiers to show only `Item Code`, `Item Name`, `Qty`, `Rate`, and `Amount`.
- Dynamic glassmorphism dashboard overlay featuring backdrop-blur controls and elegant state slates (Draft, Submitted, Cancelled).
- Bypasses System Managers automatically to maintain standard ERPNext desk workflows for administrators.

### 5. 🧪 100% Passing Test Suite
- Hardened test setups to isolate company boundaries (`_Test Company`), active fiscal years, and clean DB child table structures.
- **19/19 tests completed with OK status**.

---

## 🛠️ Update & Install Instructions

### 1. Updating your existing Docker Compose stack:
```bash
# Pull the latest stable release
cd apps/smriti_retail_os
git pull origin main
cd ../..

# Run migrations & rebuild bundles inside container
docker exec smriti_retail_os-backend-1 bench --site frontend migrate
docker exec smriti_retail_os-backend-1 bench --site frontend build --app smriti_retail_os
docker exec smriti_retail_os-backend-1 bench --site frontend execute smriti_retail_os.sync_assets.sync_assets
docker exec smriti_retail_os-backend-1 bench --site frontend clear-cache
```

### 2. Fresh Installation:
```bash
git clone https://github.com/erpnbook/smriti-docker.git
cd smriti-docker
mkdir -p apps
git clone --branch v1.0.0 https://github.com/erpnbook/smriti.git apps/smriti_retail_os
git clone --branch version-16 https://github.com/resilient-tech/india_compliance.git apps/india_compliance
docker compose -f pwd.yml up -d
```
*(Wait 2 minutes for creation, then run setup hooks and asset sync).*

---

## 👥 Contributors & Base
- **Verification Engine**: Antigravity AI Code Assistant (by Google DeepMind team)
- **Frameworks**: Frappe Framework v16 & ERPNext v16
- **Integrations**: India Compliance v16
