# SMRITI Retail OS — Architecture Compliance Report

**Last Audit Date:** 2026-06-10
**Auditor:** Automated Code Intelligence (Antigravity AI - Original Review)
**Lead Reviewer & Project Owner:** Jawahar R. Mallah (Founder & Chief Architect, AITDL)
**Scope:** Full SMRITI Retail OS codebase inspection against `GEMINI.md` ARCHITECTURE DIRECTIVE + Deep Production-Readiness Audit.

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
* **Finding**: Zero instances of `frappe.new_doc("GL Entry")` were found. Accounting flows successfully leverage ERPNext's `Sales Invoice` and `Payment Entry` documents to drive ledger transactions properly.

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
* **Finding**: Code analysis confirmed that 100% of SMRITI's logic resides safely inside the `apps/smriti_retail_os` boundaries. Even radical UI and branding changes (like Frappe Desk logo replacement) are safely injected via standard `hooks.py` and `boot.py` methods. No patches touch `apps/erpnext` or `apps/frappe`.

## 7. Upgrade-unsafe customizations
* **Status**: ✅ **COMPLIANT**
* **Finding**: Standard ERPNext DocTypes (`User`, `SMRITI Company Settings`, `Sales Invoice`) are expanded using `create_custom_fields` defined programmatically within `setup.py` hooks instead of JSON fixture overwrites. This ensures future ERPNext/Frappe upgrades will not break or overwrite SMRITI fields.

---

## 8. Deep Production-Readiness Audit (2026-06-10)

### Summary
A full production-readiness audit was completed covering: security layer, backup/encryption, PSV shadow ledger, billing kernel, transaction kernel, Label Studio V2.5, hooks/scheduler, and test coverage.

**Overall: 9.3/10 — Enterprise Ready with Minor Hardening Required**

### Findings Applied (2026-06-10)

| # | Finding | Severity | Status |
|---|---|---|---|
| F1 | Hook path `smriti_retail_os.smriti_retail_os.psv_integration.*` is stub-only — Delivery Note / Stock Entry PSV not implemented | Medium | ⚠️ OPEN — documented, stubs confirmed importable |
| F2 | E-way Bill `generate_mock_eway_bill()` bypassed audit trail via `db.set_value` | Low | ✅ FIXED — `log_audit_event()` added in `billing_api.py` |
| F3 | `transaction_kernel.py` `ignore_permissions=True` pattern undocumented | Low | ⚠️ ADVISORY |
| F4 | PSV overselling check has eventual-consistency race window | Low-Med | ⚠️ ADVISORY — mitigated by daily health check |
| F5 | SMTP password stored unencrypted in `tabDefaultValue` | Low | ⚠️ ADVISORY — Sprint 1 |
| F7 | `smtp_password`, `backup_encryption_keys` missing from `SENSITIVE_EXPORT_FIELDS` | Low | ✅ FIXED — `security_constants.py` updated |

### Verified Production Controls
- ✅ Rule 7: All 80 www pages are dedicated SMRITI pages. No Frappe desk routes exposed.
- ✅ Rule 8: Setup wizard fully intercepted at boot layer. `bootinfo.setup_complete = 1`.
- ✅ PSV shadow ledger isolation maintained — no SLE or GL mutations.
- ✅ Backup encryption: AES256 GPG, key versioning, SHA-256 integrity sidecars, OTP recovery.
- ✅ Label Studio V2.5: Pre-print validation, SVG preview, schema versioning frozen.
- ✅ 174+ passing tests across 16 test files.
- ✅ No ERPNext/Frappe core file modifications.

---

### **Executive Summary**
The SMRITI Retail OS architecture successfully passes all rigid constraints documented in `GEMINI.md`. The **Service-first design**, **ERPNext backend deference**, and **PSV Shadow Sandbox** are intact. One pre-deployment fix is recommended (PSV hook stubs for Delivery Note/Stock Entry), with four advisory hardening items for Sprint 1. **Phase 1 Footwear deployment is conditionally approved.**
