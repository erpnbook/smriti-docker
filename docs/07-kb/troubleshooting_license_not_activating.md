---
title: License Not Activating Runbook
version: 1.0
last_updated: 2026-06-18
applies_to: SMRITI Retail OS v1.x
---

# Support Runbook — License Key Not Activating

This runbook helps administrators diagnose and resolve cryptographic license key verification failures during store setup.

## 🚨 Symptom
The administrator enters a license key on the registration tab (`/app/smriti-license`) and receives one of these errors:
- `"Invalid Signature / Signature Mismatch"`
- `"Installation Binding Mismatch"`
- `"Expired Key"`

---

## 🔍 Diagnostics Step-by-Step

### Step 1: Verify Site Config Secret
HMAC signatures depend on the local secret key. Ensure your secret is set:
1. View the site configuration file:
   ```bash
   cat sites/smriti_retail/site_config.json
   ```
2. Verify that `smriti_license_secret` exists and matches the secret used by ERPNBook to sign the key.
3. *Resolution*: If the secret is missing or is using the development fallback key (`SMRITI-DEV-SECRET-...`), update `site_config.json` with your production key and clear the cache:
   ```bash
   bench --site smriti_retail clear-cache
   ```

### Step 2: Validate Installation UUID
License keys are bound to a specific server Installation ID:
1. Query the local installation ID:
   ```bash
   docker exec -it smriti_retail-backend-1 bench --site smriti_retail execute smriti_retail_os.api.licensing.get_installation_id
   ```
2. Compare the output to the `iid` parameter embedded in the license key payload.
3. *Resolution*: If they do not match, request a new license key bound to the correct Installation ID from `support@erpnbook.com`.

### Step 3: Check System Clock
HMAC expiration checks rely on the host system clock:
- Verify that the server timezone and date are set correctly:
  ```bash
  date
  ```
- *Resolution*: Sync the system clock with an NTP server to resolve false expiration errors:
  ```bash
  sudo ntpdate pool.ntp.org
  ```
