---
title: Troubleshooting CGE Issues
version: 1.0
last_updated: 2026-06-18
applies_to: SMRITI Retail OS v1.x
---

# Troubleshooting SMRITI CGE Issues

This runbook helps diagnose and resolve common errors related to loyalty rules, coupon campaigns, wallet ledgers, and accounting entries.

---

## 🚨 Problem 1: Campaign Budget Limit Exceeded

### Symptoms
Cashier receives the following error message during checkout:
```text
Campaign budget limit exceeded for campaign [Campaign Name].
```

### Cause
The combined value of committed discounts (`budget_consumed`) and pending cart checkouts (`budget_reserved`) has reached the campaign's `budget_limit`, and the campaign has `stop_on_limit` enabled.

### Resolution
1. **Extend Campaign Budget**: Go to `/app/smriti-coupon-campaign`, select the campaign, and increase the `budget_limit`.
2. **Release Stale Reservations**: If there are abandoned carts holding active reservations, run the manual cache release command or wait for the 30-minute auto-expiry cron:
   ```bash
   bench --site smriti_retail execute smriti_retail_os.cge.service.cge_service.CGECampaignManager.release_expired_reservations
   ```

---

## 🚨 Problem 2: Link Validation Error on Rule Trace Logs

### Symptoms
During rule matching, the transaction crashes with:
```text
LinkValidationError: Could not find Invoice: [Invoice ID]
```

### Cause
SMRITI attempted to save a **SMRITI Rule Evaluation Log** referencing a mock or unsaved Sales Invoice (e.g. during price validation or tests) which does not yet exist in MariaDB.

### Resolution
Ensure that the `log_doc.insert` call uses the `ignore_links=True` parameter to bypass link validation for unsaved mock structures:
```python
log_doc.insert(ignore_permissions=True, ignore_links=True)
```
This is already implemented in `cge_service.py` under the CGE v1.0 baseline.

---

## 🚨 Problem 3: Journal Entry Posting Fails on Wallet Transaction

### Symptoms
Error logged in the Error Log:
```text
Error posting CGE Journal Entry: Account [Account Name] not found.
```

### Cause
The standard double-entry cashback accounts (`Promotion Expense` or `Cashback Liability`) do not exist in the chart of accounts for the given company, and automated account provisioning failed due to missing group parent accounts.

### Resolution
1. Open ERPNext and search for **Chart of Accounts**.
2. Verify that your Company has a parent group of type **Liability** (e.g. `Current Liabilities - [abbr]`) and **Expense** (e.g. `Indirect Expenses - [abbr]`).
3. Manually create the accounts if auto-creation failed:
   - Account Name: `Cashback Liability` | Parent Account: `Current Liabilities` | Account Type: `Liability`
   - Account Name: `Promotion Expense` | Parent Account: `Indirect Expenses` | Account Type: `Expense`
4. Post a counter-reversal in SMRITI Wallet Ledger if the transaction failed.
