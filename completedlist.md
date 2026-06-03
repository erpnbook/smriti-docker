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
