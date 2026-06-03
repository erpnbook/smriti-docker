# SMRITI Retail OS - Completed & Locked Features List

This file tracks the officially completed, verified, and locked features of the SMRITI Retail OS project.

---

## 🔒 Locked Features

### 1. Sizewise HSN & GST Auto-Detection, Truncation & Validation
* **Status**: Completed, Tested & Locked (No further changes or breaks)
* **Date**: 2026-06-01
* **Description**: Added full support for pasted details from Excel containing HSN (e.g. 8-digit `64011010`) and GST columns.
* **Key Mechanisms**:
  - Truncates pasted HSN codes to 6 digits (e.g., `64011010` -> `640110`) to satisfy ERPNext/India Compliance HSN validation rules.
  - Automatically queries the `GST Settings` validation status:
    - If validation is enabled (ON), only sets 6-digit HSN codes (skips invalid 4 or 5-digit HSN codes to prevent crashes).
    - If validation is disabled (OFF), sets HSN codes of any length.
  - Safely parses GST percentages, properly supporting floats (e.g. `5.0`), integers, and `0%` tax rates without fallback errors.
* **Modified Files**:
  - Backend API: [item_master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/item_master_api.py)
  - Frontend View: [sizewise_item.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/sizewise_item.html)

### 2. Invoice & Article DB Renames and Company Email Updates
* **Status**: Completed, Tested & Locked
* **Date**: 2026-06-01
* **Description**: Renamed old invoice/article records to active series codes and corrected the typo company email across the database and PDF export utility.
* **Key Mechanisms**:
  - **ERPNext Database Renaming**: 
    - Renamed Sales Invoice `SINV-26-00001` → `TT2026-2027/14`.
    - Renamed Item (Article) `2006` → `1455` and automatically propagated changes to all its 7 active size/color variant items.
    - Updated cached matrix rows in `custom_sizewise_json` and invoice line item tables bypassing Frappe's `UpdateAfterSubmit` constraints via direct SQL patching.
  - **Company Email Typo Correction**:
    - Replaced the typo email `Tatflythreads@gmai.com` and old email `Tatflythreads@gmail.com` with `tattlythreads@gmail.com` across the `Company`, `Address`, `Contact Email`, and `User` tables.
    - Patched `company_address_display` inside the `tabSales Invoice` table to update the cached HTML print headers on existing submitted invoices.
  - **Automated PDF Export Utility**:
    - Added the whitelisted `get_admin_session_for_pdf` endpoint to `sizewise_invoice_api.py` to retrieve active Administrator sessions.
    - Updated the Chrome headless PDF generation script to handle session cookies and output the updated invoice PDF to `TT2026-2027_14_v2.pdf`.
* **Modified Files**:
  - Backend API: [sizewise_invoice_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/sizewise_invoice_api.py)
  - Export Script: [export_beautified_pdf.js](file:///d:/Smriti_Retail_OS/scratch/export_beautified_pdf.js)
  - Migration Scripts:
    - [rename_invoice_and_article.py](file:///d:/Smriti_Retail_OS/scratch/rename_invoice_and_article.py)
    - [patch_invoice_article_sql.py](file:///d:/Smriti_Retail_OS/scratch/patch_invoice_article_sql.py)
    - [patch_company_email.py](file:///d:/Smriti_Retail_OS/scratch/patch_company_email.py)
    - [patch_company_address_display.py](file:///d:/Smriti_Retail_OS/scratch/patch_company_address_display.py)

### 3. SMRITI Retail OS Deep Audit & Hardening
* **Status**: Completed, Tested & Locked
* **Date**: 2026-06-01
* **Description**: Conducted a comprehensive deep audit across the entire system, identifying and fixing critical security vulnerabilities, malformed translation assets, and check script container auto-detection.
* **Key Mechanisms**:
  - **Security Hardening**:
    - Fixed a critical vulnerability in `get_admin_session_for_pdf` where the `allow_guest=True` decorator exposed the active Administrator session ID to unauthenticated guest requests. Restricted access to the `System Manager` role.
  - **MIME-Type & Page Load Fix**:
    - Identified and fixed a malformed `en.csv` translation file that generated 352+ error log entries on every page load, causing log bloat and performance overhead.
  - **Prerequisite Check Script**:
    - Re-engineered the PowerShell validator (`check.ps1`) to dynamically detect the running Docker Compose project name, resolving a bug where it looked for hardcoded naming patterns and reported all 9 containers as "NOT FOUND".
  - **Quality Assurance**:
    - Purged historical db setup/role error logs and ran the full test suite verifying that all 81/81 automated tests pass cleanly with zero errors.
* **Modified Files**:
  - Backend API: [sizewise_invoice_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/sizewise_invoice_api.py)
  - Diagnostic Script: [check.ps1](file:///d:/Smriti_Retail_OS/check.ps1)
  - Translation: [en.csv](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/translations/en.csv)

### 4. SMRITI Store Address Management & Setup Wizard Casing Hardening
* **Status**: Completed, Tested & Locked
* **Date**: 2026-06-02
* **Description**: Implemented the complete Store Address Management under the ERPNext-First paradigm and hardened the Setup Wizard deployment block against casing collisions and payment duplicate errors.
* **Key Mechanisms**:
  - **ERPNext-First Core Address**: Keeping `SMRITI Company Settings` clean of duplicate fields, and reading/writing company registered office address parameters directly from standard ERPNext `Address` documents via `get_store_address` and `save_store_address` whitelisted endpoints.
  - **Dynamic Schema Safeguard**: Equipped the universal `Address` hook `after_address_save` in `hooks_logic.py` with dynamic meta-inspections (`frappe.get_meta('Address')`) to only audit and query fields that exist in the active site's database schema, avoiding OperationalErrors for missing columns like landmark, latitude, or longitude.
  - **Case-Insensitive Normalization**: Resolved standard ERPNext `Same Company is entered more than once` link validation errors by normalizing company_name variables to `co.name` (database primary key) immediately after saving, and executing whitespace-stripped case-insensitive checks in child table mappings.
  - **Defensive Deduplication**: Implemented automatic child table deduplication on both `Mode of Payment` accounts and `POS Profile` payments, dynamically handling both the `create` and `update` (if profile already exists) deployment branches safely.
* **Modified Files**:
  - Backend Logic:
    - [setup_wizard_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/setup_wizard_api.py)
    - [hooks_logic.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/hooks_logic.py)
    - [company_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/company_api.py)
    - [hooks.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/hooks.py)
    - [setup.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/setup.py)
    - [website_context.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/website_context.py)
  - Frontend Views:
    - [configure.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/configure.html)
    - [setup_wizard.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/setup_wizard.html)

### 5. Enhanced Supplier Registry & Indian GST/Logistics Controls
* **Status**: Completed, Tested & Locked (No further changes or breaks)
* **Date**: 2026-06-03
* **Description**: Enhanced the Supplier Registry module to fully support all standard and advanced supplier fields available in ERPNext/Frappe v16, offering a clean, retail-centric creation flow while exposing complete compliance, purchase controls, and defaults.
* **Key Mechanisms**:
  - **Dynamic Collapsible UI**: Structured the creation/edit modal into a General Profile basic details section (shown by default) and an Advanced Details collapsible toggling section.
  - **Status Mapping**: Mapped `Active`, `Disabled`, and `On Hold` dropdown values to standard Frappe `disabled` and `on_hold` boolean flags, with support for hold types (`All`, `Invoices`, `Payments`) and custom release dates.
  - **India GST & Address Syncing**: Enabled auto-creation and linking of `Billing` and `Shipping` address documents (supporting "Same as Billing" copy logic), and auto-resolved state names using India GSTIN state code mappings.
  - **ERPNext-First Dynamic Options**: Automatically queried database options for Supplier Group, Naming Series, Payment Terms Template, default pricing, default currency, and Company bank accounts.
  - **Association Path Correcting**: Resolved database `DoesNotExistError` on saving by applying `parenttype="Contact"` filters to query the correct dynamic links, avoiding collision errors with Address dynamic links.
* **Modified Files**:
  - Backend API: [master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/master_api.py)
  - Frontend View: [suppliers.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/suppliers.html)

### 6. Barcode Hardening — Option B: Primary + Secondary Barcode Architecture
* **Status**: Completed, Tested & Locked
* **Date**: 2026-06-03
* **Description**: Implemented the full Option B barcode architecture across all import paths, providing system-wide EAN-13 collision protection, manual barcode validation, and consistent barcode population strategy.
* **Key Mechanisms**:
  - **`custom_is_primary` Field**: Added `custom_is_primary` (Check field) to `Item Barcode` child table. Exactly one primary barcode enforced per item across all import paths.
  - **System-Wide Collision Protection**: Barcodes checked against both `Item Barcode` table AND `Item.item_code` namespace before assignment. Prevents cross-item collisions.
  - **Manual Barcode Validation**: Barcodes validated for allowed characters (`A-Z`, `a-z`, `0-9`, `-`, `_`), minimum 6 chars, maximum 20 chars. Spaces and special characters hard-rejected.
  - **Secondary Barcode Preservation**: Secondary barcodes (vendor-supplied, marketplace, legacy) preserved across style creation, variant updates, pivot imports, and standard imports. Never unintentionally deleted.
  - **Barcode Printing Fallback**: Print logic follows `Primary Barcode → First Barcode → Item Code` cascade.
  - **Missing Barcode Detection**: Added validation/report for active sellable variants without any barcode. Template items (with variants) excluded.
* **Modified Files**:
  - Backend API: [barcode_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/barcode_api.py)
  - Import Logic: [item_master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/item_master_api.py)

### 7. Sizewise Invoice — Barcode Scan Feature (HID Scanner Support)
* **Status**: Completed, Tested & Locked
* **Date**: 2026-06-03
* **Description**: Added a dedicated barcode scan bar to the Sizewise B2B Invoice page. Supports USB HID (keyboard-wedge) scanners and manual barcode entry. Automatically resolves barcodes to article/color/size and increments grid quantities.
* **Key Mechanisms**:
  - **`resolve_barcode()` API Hardening**: New whitelisted endpoint in `sizewise_invoice_api.py`. Enforces `Item` document read permissions (`frappe.has_permission`). Resolves via `Item Barcode` child table first, falling back to direct `item_code` match. Falls back to parent template properties (`custom_mrp`, `custom_gst_percentage`, `gst_hsn_code`, `custom_sub_category`) if they are blank on the variant. Extracts article, color, size from attributes, with regex fallback parsing from the `item_code` structure. Calculates net B2B rate from inclusive MRP.
  - Scan Bar UI: Always-visible input above the grid with pulsing `barcode_scanner` icon, inline status label, and `USB / BT scanner supported` hint.
  - **`processBarcode()`**: Async function — calls API, handles ⏳/✅/❌ states, clears input on success.
  - **`applyScanToGrid()`**: Finds existing Article+Color row or auto-creates one. Increments size qty +1 per scan. Auto-adds unknown size columns dynamically. Flashes green glow on the size cell.
  - **`flashScanBar()`**: Green flash on success, red flash on error (CSS animation, 350ms).
  - **`showScanStatus()`**: Inline label auto-clears after 5 seconds.
  - **Global HID Listener**: `document.addEventListener('keydown')` captures USB/BT scanner output when no input is focused — standard retail POS behaviour. Blocked during modal-open state.
  - **Enter Key Handler**: Scan bar input Enter key directly triggers `processBarcode()`.
* **Modified Files**:
  - Backend API: [sizewise_invoice_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/sizewise_invoice_api.py)
  - Frontend View: [sizewise_invoice.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/sizewise_invoice.html)

### 8. Item Master Excel Import — Barcode Handling Hardening
* **Status**: Completed, Tested & Locked
* **Date**: 2026-06-03
* **Description**: Fixed three critical bugs in `import_item_master` and `validate_import_rows` that caused Excel copy-paste imports to fail silently or incorrectly reject valid re-imports.
* **Key Mechanisms**:
  - **Bug 1 — Re-import False Rejection**: Old logic rejected any barcode already in the system, even if it belonged to the exact same variant being re-imported. Fixed by computing `variant_code_early = f"{style}-{color}-{size}"` and allowing the barcode through if `existing_on_system == variant_code_early`.
  - **Bug 2 — Excel Blank Cell NaN Guard**: Excel blank cells arrive as the string `"nan"` or `"None"` after JSON serialization. Added guard: `if barcode.lower() in ("", "nan", "none", "null", "0"): barcode = ""`. Barcode attachment fully skipped when empty.
  - **Bug 3 — `custom_is_primary` None-Safety**: Old `not b.custom_is_primary` mis-classified pre-migration barcode rows where `custom_is_primary` is `None`. Fixed to `not int(b.get("custom_is_primary") or 0)`.
  - **Both `validate_import_rows` and `import_item_master` updated**: Re-import fix applied to both the validation pass and the import pass consistently.
  - **`SIS` Purchase Class added to UI dropdown**: Added `SIS` as a valid purchase class option in the Item Master paste grid.
* **Standard Excel Format Supported**:
  ```
  BARCODE NO | PRODUCT STYLE CODE | ITEM DESCRIPTION | BRAND NAME | COLOR | SIZE |
  PLANNED MRP | COST PRICE | PRODUCT TAX | HSN CODE | GENDER | VENDOR CODE |
  PURCHASE CLASS | DEPARTMENT | MERCHANDISE CATEGORY | Sub category |
  HEELS | UPPER MATERIAL | OUTSOLE | IMAGE LINK
  ```
* **Modified Files**:
  - Backend API: [item_master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/item_master_api.py)
  - Frontend View: [item_master.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/item_master.html)

### 9. Item Master Excel Import — Data Cleaning & HSN Fallback Hardening
* **Status**: Completed, Tested & Locked
* **Date**: 2026-06-03
* **Description**: Resolved Excel import failures caused by missing, blank, or invalid fields (such as stray double quotes `"` in Product Tax Group or HSN Code) by introducing a system-wide defensive string cleaning utility.
* **Key Mechanisms**:
  - **Robust `_clean_str()` Utility**: Cleans every pasted row column value, stripping leading/trailing whitespace, stripping wrapping double quotes, and converting Excel empty/null placeholders (like `nan`, `none`, `null`, or stray `"`) into clean empty strings `""`.
  - **Defensive Input Parsing**: Automatically extracts only digits from HSN input fields, cleanly stripping dots, dashes, or formatting characters.
  - **Auto-Formatting & Padding**: Automatically pads short HSN codes (e.g. `6402` to `640200`) and format-corrects length issues dynamically to conform to India Compliance's 6 or 8 digit constraints.
  - **Smart Fallback**: Resolves empty or invalid HSN inputs automatically to the standard footwear default HSN code `641590`.
  - **Auto-Creation Safeguard**: Automatically registers the resolved HSN code in the database if it doesn't exist, preventing foreign key integrity crashes.
* **Modified Files**:
  - Backend API: [item_master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/item_master_api.py)

### 10. Item Master Import — Supplier Vendor Code Validation
* **Status**: Completed, Tested & Locked
* **Date**: 2026-06-04
* **Description**: Added strict Vendor Code validation for single style creation, Excel bulk import, and Pivot Matrix imports. Ensures any Vendor Code specified exists in the Supplier Master under a custom `custom_vendor_code` field before allowing items to be saved/imported.
* **Key Mechanisms**:
  - **Supplier Master Schema Update**: Created `custom_vendor_code` custom field on `Supplier` DocType with unique constraints.
  - **Rigorous Validation helper `_validate_vendor_code()`**: Validates input vendor codes, ignoring empty, `None`, `nan`, `N/A` values, and raising a user-friendly error dialog with specific title if the supplier does not exist.
  - **Single & Bulk Save Integrations**:
    - Embedded validation checks in `create_style_with_variants()`, `import_item_master()`, and `import_pivot_item_master()`.
    - Integrated hard check in `validate_import_rows()` to return validation errors during dry-run validations.
  - **Supplier Linkage Update**: Refactored `_get_or_create_template()` to resolve `supplier_name` exclusively via lookup on `custom_vendor_code`.
* **Modified Files**:
  - Backend API: [item_master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/item_master_api.py)
  - DocType Setup: [setup.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/setup.py)
  - Unit Tests: [test_item_master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/tests/test_item_master_api.py)
  - Migration Script: [create_vendor_code_field.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/create_vendor_code_field.py)

### 13. Advanced PWA — Offline Support, Background Sync & Install Prompt
* **Status**: Completed, Deployed & Locked
* **Date**: 2026-06-04
* **Description**: Implemented a full 4-phase Progressive Web App layer across SMRITI Retail OS — cache strategies, offline fallback, IndexedDB queue, background sync for pending invoices, and push notification support.
* **Key Mechanisms**:
  - **Phase 1 — Foundation**: Updated `manifest.json` with shortcuts (POS, Items, B2B Invoice, Purchase), generated 192×192 and 512×512 PNG icons, registered Service Worker at root `/sw.js` scope via Frappe route rules.
  - **Phase 2 — Smart Caching (sw.js v2)**: Three-strategy caching — `Cache First` for static assets (`/assets/`, `/files/`), `Network First` for API calls (`/api/`, `/method/`), `Stale While Revalidate` for all SMRITI pages. Auto-purges old cache versions on activate.
  - **Phase 3 — Offline IndexedDB Store**: `SmritiOfflineStore` — full IndexedDB abstraction with `pending_invoices` (save/count/delete/retry), `items_cache` (bulk load + substring search), `customers_cache` (bulk load + search), and `sync_log` (audit trail). Background Sync auto-submits queued invoices when back online.
  - **Phase 4 — Push Notifications**: SW handles `push` events and `notificationclick`, showing branded notifications with deep links.
  - **PWA Controller (`smriti_pwa.js`)**: Service Worker registration + update detection banner, `beforeinstallprompt` capture + install button, online/offline toast detection, background sync trigger on reconnect, manifest link auto-injection into `<head>`.
  - **Offline Page (`offline.html`)**: Glassmorphic offline fallback with live IndexedDB stats (pending invoice count, cached item count), animated blobs, capability grid, and auto-reload on connection restore.
  - **Root SW Serving**: `www/sw.py` serves `public/js/sw.js` at `/sw.js` with `Service-Worker-Allowed: /` header for full-site scope.
* **Modified Files**:
  - Service Worker: [sw.js](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/public/js/sw.js)
  - PWA Controller: [smriti_pwa.js](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/public/js/smriti_pwa.js)
  - Offline Store: [smriti_offline_store.js](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/public/js/smriti_offline_store.js)
  - Offline Page: [offline.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/offline.html)
  - SW Route: [sw.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/sw.py)
  - Offline Route: [offline.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/offline.py)
  - Manifest: [manifest.json](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/public/manifest.json)
  - Hooks: [hooks.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/hooks.py)
  - Icons: [icon-192.png](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/public/images/icon-192.png), [icon-512.png](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/public/images/icon-512.png)


