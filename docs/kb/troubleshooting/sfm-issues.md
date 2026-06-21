---
title: SFM/SFC Troubleshooting Runbook
version: 1.0
last_updated: 2026-06-22
author: Jawahar R Mallah <jawahar.mallah@gmail.com>
applies_to: SMRITI Retail OS v1.x
---

# Support Runbook — Sales Force Commission & Management Issues

> **Author:** Jawahar R Mallah (<jawahar.mallah@gmail.com>)  
> **Last Updated:** 2026-06-22  

This runbook guides support engineers in diagnosing and resolving Sales Force Commission (SFC) calculation discrepancies, rule mapping errors, and settlement authorization locks.

## 🚨 Symptoms
- A sales representative claims their monthly commission is missing or calculated incorrectly.
- The manager gets a 500 error when attempting to compile a monthly settlement draft.
- Commission rule overrides are not resolving with correct priority.

---

## 🔍 Diagnostics Step-by-Step

### Step 1: Verify Customer Ownership Timeline
Ensure the customer has an active owner record matching the invoice posting date:
1. Search the `SMRITI Customer Ownership` list for the target customer.
2. Verify that `posting_date` falls between the `start_date` and `end_date` of the active record.
3. Check that `is_active` is checked (`1`).

### Step 2: Validate Target Split Sum Invariant
If a sales upload fails or splits do not register, check that target splits sum to 100:
1. Check the `SMRITI Sales Target` or transaction attribution records.
2. Confirm the split formula: `primary_split_pct + secondary_split_pct = 100`.
3. If they do not sum to 100, update target allocations.

### Step 3: Rule Precedence Audit
If an incorrect commission rate is applied, trace the precedence resolution order:
1. **Employee-Level (Active, Highest Priority)**: Checks for rules mapped to the specific Employee with the highest `priority` value.
2. **Employee-Level (Active)**: Mapped to Employee but without custom priority.
3. **Company-Level (Active)**: Global rules for the Company.
4. **Settings-Level**: Global fallback rates in `SMRITI Commission Settings`.

### Step 4: Verify Attributed Revenue Threshold
If gross commission compiles to `0.0`, verify if the employee met their threshold:
1. Go to the SFC Studio dashboard and check the **Attributed Revenue** column.
2. Check the active commission rule's `min_revenue_threshold`.
3. If `Attributed Revenue` < `min_revenue_threshold`, the gross commission is correctly set to `0.0`.

---

## 🛠️ Escalation Matrix

If the SFC payout calculations still fail after completing the diagnostics:
1. **Level 1**: Contact the Store Manager to verify manual adjustment lines inside the Settlement.
2. **Level 2**: File a ticket with the SMRITI IT Support Desk (`support@erpnbook.com`) attaching the transaction invoice ID and target employee code.
