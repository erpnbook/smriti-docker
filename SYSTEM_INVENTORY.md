# SMRITI Retail OS — System Inventory

This document serves as the authoritative inventory of all custom modules, configurations, and scripts deployed in the SMRITI Retail OS application.

## 1. Custom DocTypes
* `SMRITI Party Physical Item`
* `SMRITI Party Physical Snapshot`
* `SMRITI Party Sales Item`
* `SMRITI Party Sales Upload`
* `SMRITI Party Stock Account`
* `SMRITI Party Stock Ledger Entry`
* `SMRITI Print Template`
* `SMRITI PSV Activity Log`
* `SMRITI PSV Exception Record`
* `SMRITI PSV Reorder Rule`
* `SMRITI PSV Settings`
* `SMRITI PSV Transaction`
* `SMRITI PSV Transaction Item`

## 2. Custom Pages (Workspaces/UI)
* `psv_opening_balance`
* `smriti_backup`
* `smriti_barcode`
* `smriti_billing`
* `smriti_desk`
* `smriti_inventory`
* `smriti_item_master`
* `smriti_loyalty`
* `smriti_purchase`
* `smriti_reports`
* `smriti_shift`

## 3. Custom Reports
* `PSV Party Stock Balance`
* `PSV Reconciliation`
* `PSV Reorder Report`
* `PSV Sell-Through`
* `PSV Stock Ageing`

## 4. API Endpoints
The system relies on numerous `@frappe.whitelist()` backend controllers in the following core API modules:
* `backup_api.py`
* `balance_engine.py`
* `barcode_api.py`
* `billing_api.py`
* `company_api.py`
* `inventory_api.py`
* `item_master_api.py`
* `ledger_engine.py`
* `master_api.py`
* `platform_api.py`
* `psv_api.py`
* `psv_service.py`
* `purchase_api.py`
* `reports_api.py`
* `security_api.py`
* `setup_wizard_api.py`
* `shift_api.py`

## 5. Scheduled Tasks (Schedulers)
Configured in `hooks.py`:
* **Daily:**
  * `smriti_retail_os.backup_api.run_scheduled_backup`
  * `smriti_retail_os.psv_service.run_psv_daily_health_check`

## 6. Document Hooks (`doc_events`)
* **Item:** `before_save` (sync_item_taxes_and_prices), `on_update` (after_item_save)
* **Customer:** `on_update` (sync_customer_address)
* **Supplier:** `on_update` (sync_supplier_address_and_credit_days)
* **POS Invoice:** `before_validate` (initialize_item_wise_tax_details, validate_and_reconcile_retail_invoice)
* **Sales Invoice:** 
  * `before_validate` (initialize_item_wise_tax_details, validate_and_reconcile_retail_invoice)
  * `before_cancel` (validate_sales_invoice_cancel)
  * `on_submit` (process_sales_invoice_submit)
  * `on_cancel` (process_sales_invoice_cancel)
* **Purchase Receipt, Purchase Invoice, Purchase Order, Sales Order, Delivery Note, Quotation, Supplier Quotation:** 
  * `before_validate` (initialize_item_wise_tax_details)
* **Company:** `after_insert`, `on_update` (ensure_company_settings)
* **Address:** `on_update` (after_address_save)
