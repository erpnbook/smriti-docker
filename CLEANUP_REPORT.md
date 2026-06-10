# SMRITI Retail OS — Cleanup Report

This report identifies areas where technical debt, dead code, or redundancy was cleaned up prior to the pilot deployment.

## 1. Dead Code Removal

### Legacy Shadow Ledger Logic
* **Location**: `apps/smriti_retail_os/smriti_retail_os/psv_service.py`
* **Finding**: The previous standalone functions `import_opening_balances` and `process_physical_snapshot_submit` manually constructed ledger entries using `make_ledger_entry`.
* **Cleanup Action**: These have been completely replaced by the `create_psv_transaction` abstraction layer. The old redundant code was stripped out, reducing the module size and centralizing the logic.

### Unused APIs
* **Finding**: No orphaned `@frappe.whitelist()` APIs were discovered during the audit. Every API maps to a known frontend utility (Dashboard, Billing Terminal, Inventory scanner).

## 2. Deduplication

### Validation Consolidation
* **Location**: `smriti_retail_os.hooks_logic`
* **Finding**: Standard tax and pricing logic was being called from multiple separate hooks.
* **Cleanup Action**: `initialize_item_wise_tax_details` is now cleanly mapped across 7 different purchasing and sales document types in `hooks.py`, ensuring DRY (Don't Repeat Yourself) compliance.

## 3. Code Aesthetics & Metadata

### Misleading File Headers
* **Location**: `smriti_retail_os/psv_service.py`, `smriti_retail_os/psv_api.py`, and related DocTypes.
* **Finding**: Found copy-pasted boilerplates claiming files "Handled user login, registration, and JWT token generation."
* **Cleanup Action**: Replaced all incorrect headers with accurate functional descriptions to aid future maintenance.

### Missing Dependency Indicators
* **Location**: `smriti_retail_os/psv_service.py`
* **Finding**: A `pass` block on `ImportError` for `openpyxl`.
* **Cleanup Action**: Replaced the silent fail with an explicit `frappe.msgprint` and `frappe.throw` so administrators are immediately informed of the missing pip dependency.

**Conclusion**: The codebase is lean. All identified dead code and misleading documentation have been purged. The architecture strictly follows its intended paradigms without residual prototype artifacts.
