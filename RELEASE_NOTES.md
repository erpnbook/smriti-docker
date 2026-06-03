# 🚀 Release Notes — SMRITI Retail OS

---

## 🆕 v1.1.0 — Barcode & B2B Invoice Hardening (2026-06-03)

### 🔖 1. Barcode Hardening — Option B Architecture (`barcode_api.py`, `item_master_api.py`)
- Added `custom_is_primary` (Check) field to `Item Barcode` child table
- Enforced exactly **one primary barcode per item** across all import paths
- System-wide EAN-13 collision protection (checks `Item Barcode` table + `Item.item_code` namespace)
- Secondary barcodes preserved across style creation, variant updates, pivot & standard imports
- Barcode print fallback: `Primary → First → Item Code`
- Missing barcode detection report for active sellable variants (excludes templates)

### 📷 2. Sizewise Invoice — Barcode Scan Bar (`sizewise_invoice_api.py`, `sizewise_invoice.html`)
- New `resolve_barcode()` API: resolves EAN-13, vendor barcodes, and item_code barcodes
- Dedicated scan bar UI with pulsing scanner icon, inline status label, USB/BT hint
- Finds or auto-creates Article+Color row in the pivot grid; increments size qty +1 per scan
- Auto-adds unknown size columns dynamically on scan
- Green/red CSS flash feedback on the input and size cell
- **Global HID keyboard-wedge listener** — works even when scanner fires without input focus

### 🛠️ 3. Item Master Excel Import Fixes (`item_master_api.py`, `item_master.html`)
- **Bug 1** — Re-import false rejection: allowed re-import if barcode belongs to same variant
- **Bug 2** — Excel blank cell NaN guard: `"nan"/"none"/"null"` normalized to empty string
- **Bug 3** — `custom_is_primary` None-safety: `int(b.get(...) or 0)` coercion
- Fixes applied to **both** `validate_import_rows` and `import_item_master`
- Added `SIS` to Purchase Class dropdown

### 🛠️ 4. HSN Code Handling & Fallback Hardening (`item_master_api.py`)
- Extracted digits only using regex to strip Excel quote strings (`"`), spaces, dashes, or `NA`/`N/A`
- Added auto-formatting and padding (e.g. `6402` &rarr; `640200`) to comply with India Compliance's 6/8 digit validations
- Added smart fallback default (`641590`) for blank or invalid HSN columns
- Automatically ensures the HSN code is registered in the database, avoiding foreign key errors on insertion

---

## 📦 v1.0.0 — Production Release

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

### 5. 🧪 Hardened 81-Test Suite (100% Passing)
- Hardened test setups to isolate company boundaries (`_Test Company`), active fiscal years, and clean DB child table structures.
- **81/81 tests completed with OK status**.

### 6. 🛡️ System Audit & Hardening
- Removed critical security vulnerability in `get_admin_session_for_pdf` by removing guest access and enforcing a System Manager role check.
- Fixed malformed translation file `en.csv` that generated 352+ error log entries on every page load.
- Re-engineered `check.ps1` to automatically detect running container names from Docker Compose project name, ensuring accurate health reporting.

---

## 🛠️ Update & Install Instructions

### 1. Updating your existing Docker Compose stack:
```bash
# Pull the latest stable release
cd apps/smriti_retail_os
git pull origin main
cd ../..

# Run migrations & rebuild bundles inside container
docker exec smriti_retail-backend-1 bench --site smriti_retail migrate
docker exec smriti_retail-backend-1 bench build --app smriti_retail_os
docker exec smriti_retail-backend-1 bench --site smriti_retail execute smriti_retail_os.sync_assets.sync_assets
docker exec smriti_retail-backend-1 bench --site smriti_retail clear-cache
```

### 2. Fresh Installation:
```bash
git clone https://github.com/erpnbook/smriti-docker.git
cd smriti-docker
mkdir -p apps
git clone --branch v1.0.0 https://github.com/erpnbook/smriti.git apps/smriti_retail_os
git clone --branch version-16 https://github.com/resilient-tech/india-compliance.git apps/india_compliance
docker compose -f pwd.yml up -d
```
*(Wait 2 minutes for creation, then run setup hooks and asset sync).*

---

## 👥 Contributors & Base
- **Verification Engine**: Antigravity AI Code Assistant (by Google DeepMind team)
- **Frameworks**: Frappe Framework v16 & ERPNext v16
- **Integrations**: India Compliance v16
