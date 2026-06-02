# SMRITI Pre-Deployment Validation Checklist

This document provides the final technical sign-off for the SMRITI Retail OS production patches.

## 1. File-by-File Integrity Review

### `security_api.py` (SEC-01)
- **Status**: **VERIFIED**
- **Risk**: Low. Logic correctly scopes target roles and preserves the hard block on the literal "Administrator" user.
- **Framework Check**: Uses standard `frappe.get_roles()`.

### `billing_api.py` (SEC-02, REL-02)
- **Status**: **VERIFIED**
- **Risk**: Medium. REL-02 introduces idempotency and background tasks. The dotted path for `frappe.enqueue` must match the app's install name (`smriti_retail_os`).
- **Framework Check**: Uses `frappe.enqueue` and `frappe.db.get_value` for atomic existence checks.

### `shift_api.py` (SEC-02)
- **Status**: **VERIFIED**
- **Risk**: Low. Correctly mirrors the authentication logic from `billing_api.py`.

### `sync_assets.py` (REL-01)
- **Status**: **VERIFIED**
- **Risk**: Low. Safe fallback to `shutil` ensures that even in environments without `rsync`, the sync still completes (albeit non-atomically).
- **Framework Check**: Standard Python `subprocess` used.

### `backup_api.py` (CLD-01)
- **Status**: **VERIFIED**
- **Risk**: Low. Securely passes S3 credentials to `rclone` via environment variables.
- **Framework Check**: Uses `frappe.get_doc("SMRITI Company Settings")` for multi-tenant config resolution.

### `setup.py` (SEC-02, REL-02, CLD-01)
- **Status**: **VERIFIED**
- **Risk**: Low. Migration-safe. No destructive logic remains for custom fields.

---

## 2. Validation Execution Commands

### Step 1: Database Migration
```bash
bench --site [SITENAME] migrate
```
*Purpose: Instantiates PIN fields, Billing Session ID fields, and Cloud Backup settings.*

### Step 2: Infrastructure Restart
```bash
bench restart
```
*Purpose: Ensures background workers pick up the new `process_post_billing_tasks` code.*

### Step 3: Security Smoke Test
```bash
# As SMRITI Store Manager:
bench --site [SITENAME] execute smriti_retail_os.smriti_retail_os.security_api.reset_user_password --args '["ceo@company.com", "hacked123"]'
```
*Expected: PermissionError (Blocked).*

### Step 4: PIN Validation Test
```bash
# Set a PIN for a manager in Desk UI first.
# Then test override:
bench --site [SITENAME] execute smriti_retail_os.smriti_retail_os.billing_api.validate_manager_override --args '["YOUR_PIN", "Void Test"]'
```
*Expected: authorized=True.*

### Step 5: Idempotency Verification
```bash
# Double-submit simulation:
bench --site [SITENAME] execute smriti_retail_os.smriti_retail_os.billing_api.submit_bill --args '{"cashier":"...", "billing_session_id":"UUID_123", ...}'
```
*Verify that the second call returns `idempotent: True` and the same invoice name.*

### Step 6: Backup Verification
```bash
bench --site [SITENAME] execute smriti_retail_os.smriti_retail_os.backup_api.take_backup_now
```
*Check Frappe Error Log for Rclone status.*

---

## 3. Deployment Risks
- **Worker Availability**: If workers are not running, `Payment Entry` creation will be delayed.
- **Rclone Presence**: Ensure `rclone` is installed in the target Docker image.

## 4. Rollback Plan
1. `git checkout main` (or previous stable tag).
2. `bench restart`.
3. Note: Custom fields will remain in DB but will be unused by code.
