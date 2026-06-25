---
title: Go-Live Checklist Runbook
version: 1.0
last_updated: 2026-06-18
applies_to: SMRITI Retail OS v1.x
---

# Support Runbook — Go-Live Checklist Failures

This runbook guides support engineers in diagnosing and resolving system configuration failures flagged by the Go-Live Readiness page.

## 🚨 Symptom
The Go-Live page `/smriti-go-live` returns a status of `NOT READY` or displays warning indicators (`WARN` / `FAIL`).

---

## 🔍 Diagnostics Step-by-Step

### Step 1: Troubleshoot "CSRFTokenError"
If the checklist fails to load and returns a CSRF validation error:
1. Clear your browser cookies and cache.
2. Ensure you are logged in as a user with the `System Manager` or `SMRITI System Admin` role.
3. Verify that `smriti-go-live.py` is successfully updated to fetch the standard session token:
   ```python
   context.csrf_token = frappe.sessions.get_csrf_token()
   ```

### Step 2: Resolve Product Catalogue Blocks (`FAIL`)
If the checklist flags a catalog failure:
- Ensure the database contains at least **5 items** marked as sellable.
- Run this database query to check active items:
  ```sql
  SELECT count(*) FROM `tabItem` WHERE disabled=0 AND is_sales_item=1 AND maintain_stock=1;
  ```
- *Resolution*: If the count is less than 5, seed standard items or run the catalogue import spreadsheet.

### Step 3: Resolve Default Company / Warehouse Setup Mismatches
If store setup checks fail:
- Ensure that the primary company has at least one active cost center.
- Verify that POS Profiles are not linked to inactive or archived warehouses.
- *Resolution*: Open your active POS Profile settings, verify warehouse assignments, and re-run the checks.
