# SMRITI Agent Tasks: Implementation Blueprint

This document converts the approved architectural patches into actionable tasks for AI coding agents.

---

## Phase 1: Emergency Security Fixes (Immediate)

### Task ID: SEC-01
- **Priority**: P0 (Emergency)
- **Files**: `apps/smriti_retail_os/smriti_retail_os/security_api.py`
- **Dependencies**: None
- **Acceptance Criteria**:
  1. `reset_user_password` must verify that the target user **does not** have the `System Manager` or any role with `desk_access=1`.
  2. If the target has forbidden roles, raise `frappe.PermissionError`.
  3. Existing `check_administrator_protection` must remain active as a secondary guard.
- **Risk Level**: Low

### Task ID: SEC-02
- **Priority**: P0 (Emergency)
- **Files**: 
  - `apps/smriti_retail_os/smriti_retail_os/setup.py`
  - `apps/smriti_retail_os/smriti_retail_os/billing_api.py`
  - `apps/smriti_retail_os/smriti_retail_os/shift_api.py`
- **Dependencies**: SEC-01
- **Acceptance Criteria**:
  1. **CRITICAL**: Remove the destructive `frappe.delete_doc` logic in `setup.py` Line 588.
  2. Add `custom_smriti_pin` field to `User` DocType (Fieldtype: `Password`, Label: `SMRITI POS PIN`).
  3. Update `validate_manager_override` and `_validate_manager_pin` to use `frappe.utils.password.check_password` against the new `custom_smriti_pin` field.
  4. Retain primary password check as a fallback if `custom_smriti_pin` is not set (Backward Compatibility).
- **Risk Level**: Medium (Schema change)

---

## Phase 2: Operational Reliability (Infrastructure Hardening)

### Task ID: REL-01
- **Priority**: P1 (High)
- **Files**: `apps/smriti_retail_os/smriti_retail_os/sync_assets.py`
- **Dependencies**: None
- **Acceptance Criteria**:
  1. Replace `shutil.rmtree` and `shutil.copytree` logic with an `rsync`-based atomic strategy.
  2. Use command: `rsync -a --atomic --delay-updates <src> <dst>`.
  3. Ensure the script checks for the existence of `rsync` before execution.
- **Risk Level**: Low

### Task ID: REL-02
- **Priority**: P1 (High)
- **Files**: `apps/smriti_retail_os/smriti_retail_os/billing_api.py`
- **Dependencies**: SEC-02
- **Acceptance Criteria**:
  1. Implement **Idempotency Checks** in `submit_bill`.
  2. The frontend must send a unique `billing_session_id`.
  3. Before creating an Invoice, check if an Invoice with the same `billing_session_id` already exists.
  4. Move non-critical `Payment Entry` and `Loyalty` updates to a background job using `frappe.enqueue` to ensure eventual consistency without DB locking.
- **Risk Level**: High (Requires regression testing)

---

## Phase 3: Infrastructure Scaling

### Task ID: CLD-01
- **Priority**: P2 (Medium)
- **Files**: 
  - `apps/smriti_retail_os/smriti_retail_os/setup.py`
  - `apps/smriti_retail_os/smriti_retail_os/backup_api.py`
- **Dependencies**: None
- **Acceptance Criteria**:
  1. Add `Cloud Backup Provider`, `S3 Bucket`, `S3 Access Key`, and `S3 Secret Key` (Fieldtype: `Password`) to `SMRITI Company Settings`.
  2. Implement `rclone_sync` method in `backup_api.py` that utilizes these credentials.
  3. Replace the SMTP attachment in `_email_backup` with a notification email containing the status of the cloud sync.
- **Risk Level**: Low

---

## Validation & Rollback Checklist

### Validation
- [ ] `bench run-tests --app smriti_retail_os` passes.
- [ ] Manual POS billing flow (Held -> Recall -> Submit) verified.
- [ ] Manager override works with new PIN.
- [ ] Rclone sync verified via command line `rclone ls`.

### Rollback
- [ ] `git checkout hooks.py setup.py billing_api.py security_api.py backup_api.py sync_assets.py`
- [ ] If schema changed: `bench migrate` (Note: Custom fields must be manually deleted if rollback is permanent).
