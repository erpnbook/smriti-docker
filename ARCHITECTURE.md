# SMRITI Retail OS — Master Architecture & Technical Reference

This document serves as the master technical blueprint and architectural reference for **SMRITI Retail OS**.

---

## 1. Platform Overview
SMRITI Retail OS is architected as a **Sophisticated Experience Layer (SEL)** built on top of **Frappe v16** and **ERPNext v16**. 

Unlike traditional customizations that directly alter ERP core files, SMRITI acts as an overlay translation layer. It intercepts complex ERPNext forms (such as stock ledgers and accounting journals) and simplifies them into cashier-friendly, single-screen retail dashboards tailored for high-volume footwear and apparel environments, while preserving the full integrity of the underlying ERP backend.

---

## 2. Docker Architecture
The deployment utilizes Docker Compose to orchestrate 9 separate containers:
- **`frontend` (Nginx)**: Proxy gateway that handles routing for the ERP desk on container port `8080` (exposed on host port `8765` by default) and the cashier billing terminal on container port `9000` (can be optionally mapped to host port `9000` for strict cashier lockdown). Serves pre-compiled static assets.
- **`backend` (Gunicorn)**: Main application server running the WSGI Frappe/ERPNext logic.
- **`websocket` (Socket.IO)**: Manages real-time message relays and background queue sync alerts.
- **`db` (MariaDB)**: Relational database engine.
- **`redis-cache`** & **`redis-queue`**: Memory caching and job broker services.
- **`queue-short`** & **`queue-long`**: RQ workers separating transactional jobs from long-running bulk imports.
- **`scheduler`**: Background job daemon triggering automated tasks.

**Volume Management**: SMRITI utilizes the shared named volume `smriti_retail_sites` and runs the custom `sync_assets.py` utility during container bootstrap. This utility unlinks traditional Frappe app symlinks and copies physical bundles directly into Nginx volumes to bypass browser MIME-type and 404 blockages.

---

## 3. Setup Wizard
The onboarding wizard (`setup_wizard_api.py`) automates the initial system provisioning for a fresh retail site. It executes sequentially:
1. **Step 1: Administrator**: Provisions credentials and enforces complex passwords.
2. **Step 2: Company**: Sets up the Legal Entity and basic accounting defaults.
3. **Step 3: Defaults**: Configures standard POS cash registers and payment modes.
4. **Step 4: GST**: Links GSTIN parameters and registers regional tax split configurations.
5. **Step 5: Deploy**: Executes setup migration triggers and opens access to the desk.

---

## 4. Platform Center
The Platform Center (`/platform_center`) serves as the technical administrative panel. It enables operators to monitor container services, check database pool sizes, measure WebSocket latency response benchmarks, and audit system log entries.

---

## 5. Billing Engine
The Billing Engine (`billing_api.py`) is optimized for cash counters:
- **Idempotency Guard**: Restricts duplicate invoice creations by validating a unique client-side `billing_session_id`.
- **Background Dispatch**: Enqueues secondary computations (like loyalty ledger updates and payment entry creations) to short RQ workers to return instant checkout feedback to cashiers.
- **Role Isolation**: Cashiers are automatically redirected to the standalone `/billing` layout on port `9000` (if host port `9000` is mapped) or they can access `/billing` directly on the default port `8765` (e.g. `http://localhost:8765/billing`), bypassing standard ERP Desk access.

---

## 6. Purchase Engine
The Purchase Engine (`purchase_api.py`) simplifies inventory replenishment:
- **Quick Purchase Orders**: A clean interface for registering supply contracts and pricing.
- **GRN Creation**: Translates PO templates directly into standard ERPNext Purchase Receipts.
- **Supplier Validation**: Cross-checks mapped vendor codes to prevent record duplications on creation.

---

## 7. Inventory Engine
Stock and stock transfers are managed through the Inventory Engine (`inventory_api.py`):
- **Warehouse Realignment**: Uses the `_get_default_warehouse(company)` helper to query and align warehouse types with the target company context, preventing cross-company posting ledger validation crashes.
- **Variant Grid Splits**: Translates size-by-color purchase spreadsheets into standard stock entries.

---

## 8. Barcode Center
The Barcode Center (`barcode_api.py`) regulates the store barcode namespaces:
- **Primary Barcode Architecture**: Enforces exactly one primary barcode per item variant via the `custom_is_primary` attribute in `Item Barcode` tables.
- **EAN-13 Collision Guard**: Rejects duplicate barcode imports across child tables and master code namespaces.

---

## 9. Label Studio
Label Studio (`/barcode`) is a high-availability retail tag printing client:
- **Template Designer**: Technical managers design custom labels using raw ZPL or TSPL print codes.
- **Interface Support**: Streams raw printer commands to local USB thermal printers (via QZ Tray WebSocket) or direct LAN socket connections (TCP port `9100`).
- **Style / Article Search**: Operates debounced search queries matching barcodes, style codes, and variant records.

---

## 10. API Layer
All frontend features interact with the backend via whitelisted endpoints (`@frappe.whitelist()`). Major APIs include:
- `smriti_retail_os.billing_api.submit_bill`: Saves and submits POS invoices.
- `smriti_retail_os.barcode_api.send_to_network_printer`: Streams raw template code to network printers.
- `smriti_retail_os.item_master_api.import_pivot_item_master`: Performs bulk variant imports.

---

## 11. Security Model
The Security Model (`security_api.py`) governs user access permissions:
- **Governance Tiers**: Standard cashier and store manager accounts are strictly blocked from editing System Manager configurations or altering past sales records.
- **Administrative Protection**: Restricts the whitelisted `reset_user_password` function to prevent store-level staff from resetting system administrator passwords.
- **PIN Overrides**: Restricts sensitive manager actions (such as invoice deletions or overrides) using a dedicated, hashed `custom_smriti_pin` stored on the User DocType, preventing main password exposure.

---

## 12. Backup & Recovery
SMRITI employs a double-tier backup and recovery strategy (`backup_api.py`):
- **Local DB Dumps**: Standard daily backups are generated and compressed inside the site's private directory.
- **S3 & rclone Integration**: Since database tarballs can easily exceed SMTP limit thresholds (**25MB**), SMRITI bypasses email transfers and uploads compressed backups directly to secure S3 buckets using `rclone`.
- **Disaster Recovery**: Restores databases, public files, and private folders using the `bench restore` CLI utility inside the backend container.

---

## 13. Future Expansion (SmartPOS Roadmap)
The long-term development roadmap targets:
- **AI Stock Predictor**: Proactive inventory warnings using rolling sales logs.
- **Smart POS Hardware Integration**: Standalone Android and iOS SmartPOS SDK support.
- **Offline Sync Optimization**: Enhanced peer-to-peer ledger sync models.
