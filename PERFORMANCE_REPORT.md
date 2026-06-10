# SMRITI Retail OS — Performance Report

This document highlights the performance optimizations verified within the codebase to ensure scalability for the pilot deployment.

## 1. Query Optimizations

### N+1 Query Elimination
* **Location**: `apps/smriti_retail_os/smriti_retail_os/psv_service.py`
* **Finding**: Earlier iterations fetched balances inside a `for` loop during Sales Uploads.
* **Resolution**: Successfully replaced with `get_bulk_party_balances` from `balance_engine.py`, fetching all required balances in a single optimized `frappe.db.sql` query before processing the loop.

### Avoidance of Full ORM Instantiation
* **Location**: Core API modules (`billing_api.py`, `inventory_api.py`)
* **Finding**: Heavy reliance on `frappe.db.get_value()` and `frappe.db.sql(..., as_dict=True)` instead of `frappe.get_doc()`. 
* **Risk/Benefit**: By avoiding the instantiation of full Frappe Document objects in high-volume areas (like validating 100 items on a POS bill), the memory footprint and CPU overhead are drastically reduced.

## 2. Database Indexes & Schema

### Unique Constraints
* **Location**: `SMRITI PSV Transaction`
* **Finding**: The `mapping_fingerprint` field is correctly flagged as `unique: 1`. This forces MariaDB/InnoDB to create a unique index, ensuring the duplicate protection check `frappe.db.get_value(..., "name")` performs an immediate index lookup rather than a full table scan.

### Aggregation Offloading
* **Location**: `reports_api.py` and PSV script reports.
* **Finding**: The system offloads heavy math to the database. Instead of pulling all ledger entries into Python and summing them, it utilizes `SUM()` and `GROUP BY` in SQL.
* **Benefit**: Reduces network bandwidth between the Database and Web server, and speeds up report generation to milliseconds.

## 3. Dashboard Bottlenecks

### Caching
* **Location**: `SMRITI Party Stock Account` Master
* **Finding**: Used `frappe.get_cached_doc` in `validate_tracking_mode` to prevent redundant database hits when evaluating multiple lines of a transaction.

**Conclusion**: The system is highly optimized for performance and is free of common ORM-induced bottlenecks like N+1 queries or memory-heavy bulk document loading.
