---
title: POS Not Loading Runbook
version: 1.0
last_updated: 2026-06-18
applies_to: SMRITI Retail OS v1.x
---

# Support Runbook — POS Terminal Not Loading

This runbook guides support engineers in diagnosing and resolving POS register loading failures at store checkout lanes.

## 🚨 Symptom
The cashier opens the register page `/app/barcode#pos-dark` or `/app/billing` and encounters:
- A blank white screen.
- An infinite loading spinner.
- An "Access Denied" error overlay.

---

## 🔍 Diagnostics Step-by-Step

### Step 1: Check Browser Console Logs
1. Press `F12` to open Developer Tools.
2. Check the Console tab for red errors:
   - If `403 (Forbidden)` appears on api requests, the cashier does not have the **SMRITI Cashier** role assigned.
   - If `CSRFTokenError` is shown, the session token cookie is expired or mismatched.

### Step 2: Validate Cashier Role Mapping
Ensure the cashier's user profile is correctly configured:
```bash
docker exec -it smriti_retail-backend-1 bench --site smriti_retail execute smriti_retail_os.api.golive_api.get_cashier_roles --args '["cashier_username"]'
```
*Resolution*: If the role is missing, assign `SMRITI Cashier` via the User settings list.

### Step 3: Check Active POS Shift Logs
POS terminals require an active shift to initialize the register:
- Open the POS Opening Entry list.
- Verify if the cashier has an open shift for the selected POS profile.
- *Resolution*: If a shift is stuck in draft or mapped to a different cashier, cancel the draft and open a new shift.

---

## 🛠️ Escalation Matrix

If the POS screen still fails to load after completing the steps above:
1. **Level 1**: Contact the local Store Manager to verify POS Profile mappings.
2. **Level 2**: File a ticket with the SMRITI IT Support Desk (`support@erpnbook.com`) attaching console logs and the target Cashier username.
