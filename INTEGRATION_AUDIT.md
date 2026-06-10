# SMRITI Retail OS — Integration Audit

This report verifies the core integration pipelines across SMRITI modules and standard ERPNext dependencies to ensure data flows correctly without breaking standard schema logic.

## 1. Module Integrations

### Billing → Inventory
* **Status**: ✅ **VERIFIED**
* **Mechanism**: SMRITI `billing_api.py` utilizes standard `POS Invoice` and `Sales Invoice` document creation. Stock deduction is inherently handled by ERPNext's core `Stock Ledger Entry` generation upon submission. `update_stock` flag is respected.

### Inventory → PSV (Shadow Ledger)
* **Status**: ✅ **VERIFIED**
* **Mechanism**: The integration relies on `psv_service.py` document hooks registered in `hooks.py`. 
  * Sales Invoices trigger `process_sales_invoice_submit`.
  * The process creates a `SMRITI PSV Transaction` (Type: `TRANSFER_OUT` or `RETURN`), guaranteeing the shadow ledger stays synced with physical inventory movement without touching core accounting ledgers.

### PSV → Reports
* **Status**: ✅ **VERIFIED**
* **Mechanism**: Custom reports (`PSV Party Stock Balance`, `PSV Sell-Through`, etc.) directly query the `balance_engine.py` APIs (`get_all_party_balances`). No caching mismatches observed.

### Purchase → Inventory
* **Status**: ✅ **VERIFIED**
* **Mechanism**: `purchase_api.py` directly submits `Purchase Receipt` documents, linking back to the `Purchase Order`. Standard `UpdateAfterSubmit` and accounting/stock ledgers apply natively.

### Returns → Inventory & PSV
* **Status**: ✅ **VERIFIED**
* **Mechanism**: Returns logic dynamically sets `is_return = 1`. In PSV, `process_sales_invoice_submit` correctly intercepts this flag and passes `tx_type = "RETURN"`, adding stock back to the Party Stock Account shadow ledger.

### Dashboard → APIs
* **Status**: ✅ **VERIFIED**
* **Mechanism**: `/psa` frontend utilizes `smriti_retail_os.psv_api.get_dashboard_summary` asynchronously. Loading does not block UI rendering.

## 2. Dependency & Routing Audit
* **Broken Links**: None detected. All `reference_doctype` dynamic links are correctly configured.
* **Missing Routes**: None detected. Nginx proxy and `website_route_rules` inside `hooks.py` accurately map `/billing`, `/setup-wizard`, `/psa`, and `/purchase` to their respective `.html` files.
* **Permissions**: Role profiles `SMRITI Store Manager` and `SMRITI Cashier` have verified explicit DocPerms. No missing basic module permissions.

**Conclusion**: The system integration layer is intact and correctly relies on Frappe's document lifecycle hooks rather than raw SQL writes for module cross-communication.
