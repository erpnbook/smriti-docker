# SMRITI Patch Architecture: Security & Reliability Release

As the Lead Security Architect, I have designed the following production-safe patches for SMRITI Retail OS. These designs prioritize operational continuity and zero-core-modification.

---

## 1. Patch: Governance Guard (Privilege Escalation)
**A. Root Cause**: `check_administrator_protection` only validates against the literal `Administrator` string, allowing `SMRITI Store Manager` to reset passwords for `System Manager` accounts.  
**B. Recommended Fix**: Implement **Role-Based Reset Scoping**. Update the validator to ensure that `SMRITI Store Manager` can *only* reset passwords for users whose *highest* role is `SMRITI Cashier`. Any account with `System Manager` or `Administrator` roles becomes programmatically "untouchable" by managers.  
**C. Alternative Fix**: A hardcoded "Protected Users" child table in `SMRITI Company Settings`.  
**D. Database Changes**: None.  
**E. API Changes**: Update `check_administrator_protection` in `security_api.py`.  
**F. UI Changes**: None.  
**G. Migration Strategy**: Immediate logic update; no data migration required.  
**H. Rollback Strategy**: Revert `security_api.py` to previous version.  
**I. Effort**: 2 Hours.  
**J. Production Risk**: Low.

---

## 2. Patch: Stealth-PIN (POS Credential Protection)
**A. Root Cause**: Reliance on `frappe.auth.check_password` forces managers to expose system-wide credentials on the POS.  
**B. Recommended Fix**: **Dedicated Hashed PIN**. Add a `custom_smriti_pin` field to the `User` DocType. Store a 4-6 digit numeric PIN using Frappe's `Password` field type (for automatic hashing). Update `validate_manager_override` to verify against this field using `frappe.utils.password.check_password`.  
**C. Alternative Fix**: Shared "Manager Token" stored in `SMRITI Company Settings`.  
**D. Database Changes**: Add `custom_smriti_pin` field to `User` via `setup.py`.  
**E. API Changes**: Update `billing_api.py` and `shift_api.py` validation logic.  
**F. UI Changes**: Add "Set POS PIN" button in SMRITI Security Center.  
**G. Migration Strategy**: Add field -> Prompt Managers to set PIN on first login after patch.  
**H. Rollback Strategy**: Keep existing password fallback logic in code for 1 release cycle.  
**I. Effort**: 1 Day.  
**J. Production Risk**: Medium (Staff training required).

---

## 3. Patch: Cloud-Link (Backup Scalability)
**A. Root Cause**: SMTP protocol limitations (25MB) prevent off-site recovery for established stores.  
**B. Recommended Fix**: **Rclone Integration**. Utilize `rclone` (pre-installed in Smriti Docker) to sync the `private/backups` directory to S3-compatible storage. Replace SMTP attachment logic with a "Backup Link" email containing a pre-signed download URL.  
**C. Alternative Fix**: Split-volume multi-part ZIPs (not recommended).  
**D. Database Changes**: Add Cloud Provider fields (Bucket, Key, Secret, Region) to `smriti_backup_settings`.  
**E. API Changes**: New `sync_to_cloud` method in `backup_api.py`.  
**F. UI Changes**: New "Cloud Storage" tab in Backup Settings.  
**G. Migration Strategy**: Concurrent support for Email + Cloud for 30 days.  
**H. Rollback Strategy**: Disable Cloud Sync; keep Local Backup enabled.  
**I. Effort**: 3 Days.  
**J. Production Risk**: Low.

---

## 4. Patch: Atomic Asset Swap (Zero-Downtime Sync)
**A. Root Cause**: `shutil.rmtree` on the live assets directory during `_run_sync`.  
**B. Recommended Fix**: **Atomic Move (Shadow Swap)**. Sync assets to `sites/assets_temp`. Once complete, use `os.rename` to swap `assets` to `assets_old` and `assets_temp` to `assets`. Finally, delete `assets_old`. This reduces the "404 window" from minutes to milliseconds.  
**C. Alternative Fix**: Use `rsync` with `--delay-updates`.  
**D. Database Changes**: None.  
**E. API Changes**: Refactor `sync_assets.py`.  
**F. UI Changes**: None.  
**G. Migration Strategy**: Update script in Docker entrypoint.  
**H. Rollback Strategy**: Revert to previous `sync_assets.py` logic.  
**I. Effort**: 4 Hours.  
**J. Production Risk**: Medium (Requires volume lock verification).

---

## 5. Patch: Transaction Guard (Billing Integrity)
**A. Root Cause**: Non-atomic multi-document submission in `submit_bill`.  
**B. Recommended Fix**: **Explicit Transaction Wrapping**. Wrap the `Save -> Submit -> PaymentEntry -> Loyalty` sequence in an explicit `frappe.db.begin()` block. Use `try/except` to ensure `frappe.db.rollback()` on any failure, preventing "Zombie" Invoices.  
**C. Alternative Fix**: Move Payment Entry creation to a background job (creates delay).  
**D. Database Changes**: None.  
**E. API Changes**: Refactor `submit_bill` in `billing_api.py`.  
**F. UI Changes**: None.  
**G. Migration Strategy**: Core logic update.  
**H. Rollback Strategy**: Revert `billing_api.py`.  
**I. Effort**: 1 Day.  
**J. Production Risk**: High (Requires exhaustive regression testing of the billing flow).

---
*Architect Signature: Lead Security Architect, SMRITI Retail OS*
