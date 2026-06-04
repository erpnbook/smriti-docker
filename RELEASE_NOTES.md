# 🚀 Release Notes — SMRITI Retail OS

---

## 🆕 v1.2.1 — Warehouse Hardening & Custom Warehouse Override (2026-06-04)

### 🏢 1. Company-matching Default Warehouse (`purchase_api.py`, `inventory_api.py`)
- Added `_get_default_warehouse(company)` helper to resolve warehouses with target company filters.
- Prevents database mismatch issues (e.g., `Warehouse Stores - TCL does not belong to company _Test Company`).
- Automatically queries first by name `"Stores"` (non-group) belonging to the target company, then falls back to any non-group warehouse for the company, and finally any warehouse for the company.

### 🎛️ 2. Custom Warehouse Selection on Creation (`purchase_api.py`, `inventory_api.py`)
- Added optional `warehouse` parameter to whitelisted API endpoints: `create_purchase_order`, `create_purchase_receipt`, and `create_grn`.
- Allows custom warehouse overrides to be passed directly from the frontend or creation payload.

### 🧪 3. Expanded Test Suite
- Added new test cases verifying custom warehouse overrides in `test_purchase_api.py`.
- Verified all **87 tests** pass cleanly.

---

## 🆕 v1.2.0 — Advanced PWA & Supplier Hardening (2026-06-04)

### 📲 1. Advanced PWA — All 4 Phases (`sw.js`, `smriti_pwa.js`, `smriti_offline_store.js`)

**Phase 1 — Foundation**
- Updated `manifest.json`: Added app shortcuts (POS Billing, Item Master, B2B Invoice, Purchase Manager), PNG icon references, orientation `any`, categories
- Generated 192×192 and 512×512 PNG icons deployed to `public/images/`
- Service Worker exposed at root `/sw.js` via `www/sw.py` + `website_route_rules` — gives full `scope: '/'` control

**Phase 2 — Smart Multi-Strategy Caching** (`sw.js` v2.0)
- `Cache First` → `/assets/`, `/files/`, `/favicon` (static resources, instant serve)
- `Network First` → `/api/`, `/method/` (live data; falls back to cached JSON offline)
- `Stale While Revalidate` → all 15 SMRITI pages (instant load + background refresh)
- Auto-purges stale cache versions on `activate`; new SW skips waiting immediately

**Phase 3 — Offline IndexedDB Store** (`smriti_offline_store.js`)
- `SmritiOfflineStore`: Full IndexedDB abstraction (`SmritiRetailOS` DB, v1 schema)
- `pending_invoices`: save/count/delete/incrementRetry — offline POS bill queue
- `items_cache`: bulk load + substring search (item_code + item_name) — offline barcode lookup
- `customers_cache`: bulk load + search (name + mobile_no)
- `sync_log`: timestamped audit trail of all sync events
- Background Sync auto-submits queued invoices via `sync-pending-invoices` tag when back online

**Phase 4 — Push Notifications** (`sw.js`)
- Handles `push` events: shows branded notifications with icon, badge, vibrate
- `notificationclick`: focuses existing window or opens deep-link URL

**PWA Controller** (`smriti_pwa.js`)
- Registers SW, detects updates → shows animated **"New Version Available"** banner
- Captures `beforeinstallprompt` → shows **"📲 Install SMRITI App"** button
- Online/offline detection → shows toast (Frappe or vanilla fallback)
- Triggers `sync-pending-invoices` background sync immediately on reconnection
- Auto-injects `<link rel="manifest">` into `<head>` on all pages

**Offline Fallback Page** (`offline.html`, `offline.py`)
- Glassmorphic dark design with animated blobs
- Live IndexedDB stats: pending invoice count + cached item count
- Offline capabilities grid, retry button, auto-reload on `online` event

### 🔗 2. Supplier Lookup Filter Fix (`purchase_order.js`)
- Removed `supplier_type: "Company"` filter from Purchase Order/Receipt supplier query
- All active suppliers (Individual + Company) now appear in PO/GRN supplier fields
- Individual suppliers created via SMRITI dashboard are now correctly visible

### ✅ 3. Supplier Vendor Code Validation (`item_master_api.py`, `setup.py`)
- Added `custom_vendor_code` unique field on Supplier DocType
- `_validate_vendor_code()` helper rejects unregistered vendor codes in all 3 import paths
- Supplier linkage now resolves exclusively via `custom_vendor_code` lookup

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
- Hardened `resolve_barcode()` API with user read permission checks (`frappe.has_permission`)
- Implemented parent template field fallbacks (inherits `custom_mrp`, `custom_gst_percentage`, `gst_hsn_code`, `custom_sub_category` from template if blank on variant)
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

### 🛠️ 4. Data Cleaning & HSN Fallback Hardening (`item_master_api.py`)
- Added a robust `_clean_str()` helper that sanitizes all pasted cells, automatically removing wrapping quotes, Excel stray quotes (`"`), and converting various Excel null representations (`nan`, `none`, `null`) into clean empty strings `""`
- Extracted digits only using regex to strip HSN format characters, dashes, dots, or placeholder text
- Added auto-formatting and padding (e.g. `6402` &rarr; `640200`) to comply with India Compliance's 6/8 digit validations
- Added smart fallback default HSN (`641590`) for blank or invalid HSN columns
- Automatically registers resolved HSN codes in the database, avoiding foreign key validation crashes on insertion

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
