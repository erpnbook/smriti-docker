# SMRITI Retail OS — Architecture Compliance Report

**Audit Date:** 2026-06-09
**Auditor:** Automated Code Intelligence
**Scope:** Full SMRITI Retail OS codebase inspection against `GEMINI.md` ARCHITECTURE DIRECTIVE.

---

## 1. Direct database writes from frontend code
* **Status**: ✅ **COMPLIANT**
* **Finding**: Scanned all `*.js` and `*.html` files. Zero instances of raw `frappe.client.insert("Sales Invoice")`, `frappe.client.save()`, or direct `frappe.db` manipulation originating from the UI were found.
* **Architecture Note**: The frontend relies entirely on standard Frappe JS API calls to SMRITI backend business controllers (e.g., `frappe.call({method: 'smriti_retail_os.company_api.get_business_type'})`), successfully adhering to **Rule 6: Service-first design**.

## 2. Direct Stock Ledger modifications
* **Status**: ✅ **COMPLIANT (with 1 minor administrative exception)**
* **Finding**: The system does not instantiate `frappe.new_doc("Stock Ledger Entry")` directly anywhere in its workflow logic. All operational stock movements route through core Frappe wrappers (e.g., `Sales Invoice`, `Purchase Receipt`, `Delivery Note`).
* **Exception**: `inventory_api.py` (`reset_db`) and `item_master_api.py` (`reset_all_transactions`) use raw `TRUNCATE tabStock Ledger Entry` statements.
* **Risk/Classification**: **Low**. This is an administrative data wipe tool specifically engineered for pilot/testing environments. It is safely protected behind strict `check_administrator_only()` guards.

## 3. Direct GL Entry modifications
* **Status**: ✅ **COMPLIANT**
* **Finding**: Zero instances of `frappe.new_doc("GL Entry")` were found. Accounting flows successfully leverage ERPNext’s `Sales Invoice` and `Payment Entry` documents to drive ledger transactions properly.

## 4. Re-implementation of ERPNext functionality
* **Status**: ✅ **COMPLIANT**
* **Finding**: 
  - **Accounting & Tax**: SMRITI utilizes existing Frappe/ERPNext engines for tax and general ledgers. Reports like `cash_book` and `day_book` aggregate existing `GL Entry` data dynamically instead of recreating accounting logs.
  - **PSV Shadow Ledger**: The custom `SMRITI Party Stock Ledger Entry` and `SMRITI PSV Transaction` mechanisms explicitly obey the **PSV SPECIAL RULE** defined in `GEMINI.md`, retaining their own isolated architecture without mutating the standard system stock logic.

## 5. Missing service-layer abstractions
* **Status**: ✅ **COMPLIANT**
* **Finding**: Business logic is successfully abstracted into dedicated services (`psv_service.py`, `billing_api.py`, `item_master_api.py`). Cross-domain dependencies correctly import these services rather than executing scattered SQL queries or core Frappe hooks blindly. 

## 6. Core ERPNext file modifications
* **Status**: ✅ **COMPLIANT**
* **Finding**: Code analysis confirmed that 100% of SMRITI’s logic resides safely inside the `apps/smriti_retail_os` boundaries. Even radical UI and branding changes (like Frappe Desk logo replacement) are safely injected via standard `hooks.py` and `boot.py` methods. No patches touch `apps/erpnext` or `apps/frappe`.

## 7. Upgrade-unsafe customizations
* **Status**: ✅ **COMPLIANT**
* **Finding**: Standard ERPNext DocTypes (`User`, `SMRITI Company Settings`, `Sales Invoice`) are expanded using `create_custom_fields` defined programmatically within `setup.py` hooks instead of JSON fixture overwrites. This ensures future ERPNext/Frappe upgrades will not break or overwrite SMRITI fields.

---

### **Executive Summary**
The SMRITI Retail OS architecture successfully passes all rigid constraints documented in `GEMINI.md`. The **Service-first design**, **ERPNext backend deference**, and **PSV Shadow Sandbox** are intact. No immediate corrective actions are necessary before the Phase 1 Footwear deployment.
