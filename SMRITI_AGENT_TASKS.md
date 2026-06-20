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

## Phase 4: Operational Telemetry Intelligence (ACP-BARCODE-002A)

### Task ID: TEL-01 (DocType Provisioning)
- **Priority**: P1 (High)
- **Files**: `apps/smriti_retail_os/smriti_retail_os/setup.py`
- **Dependencies**: None
- **Acceptance Criteria**:
  1. Add `create_smriti_telemetry_doctypes()` to provision `SMRITI Barcode Scan Event` (raw) and `SMRITI Barcode Telemetry Snapshot` (aggregated) custom DocTypes.
  2. Map all fields described in the data model sections of `ACP_BARCODE_002A.md`.
  3. Hook execution inside `setup_smriti_retail_os()`.
- **Risk Level**: Medium (Schema additions)

### Task ID: TEL-02 (Telemetry Logging API)
- **Priority**: P1 (High)
- **Files**: `apps/smriti_retail_os/smriti_retail_os/barcode_api.py`
- **Dependencies**: TEL-01
- **Acceptance Criteria**:
  1. Implement `@frappe.whitelist()` API `log_barcode_scan_event(event_data)`.
  2. Validate incoming fields: map attempts, success status, and template ID.
  3. Determine and assign the correct `governance_event_id` (`SCAN-EVT-001`, `SCAN-EVT-002`, or `SCAN-EVT-003`) based on attempts and success/failure.
- **Risk Level**: Low

### Task ID: TEL-03 (Retention Scheduler)
- **Priority**: P2 (Medium)
- **Files**:
  - `apps/smriti_retail_os/smriti_retail_os/barcode_api.py`
  - `apps/smriti_retail_os/smriti_retail_os/hooks.py`
- **Dependencies**: TEL-01
- **Acceptance Criteria**:
  1. Implement `delete_expired_scan_events()` to delete `SMRITI Barcode Scan Event` records older than 90 days.
  2. Register this function in `hooks.py` under the scheduler `daily` event.
- **Risk Level**: Low

### Task ID: TEL-04 (Aggregation & Score Calculation)
- **Priority**: P1 (High)
- **Files**: `apps/smriti_retail_os/smriti_retail_os/barcode_api.py`
- **Dependencies**: TEL-02, TEL-05
- **Acceptance Criteria**:
  1. Implement `aggregate_scan_telemetry(period="Daily")` that collects raw events for a period, summarizes counts (successes, retries, failures), and creates snapshot records.
  2. Implement formula computation for `SMRITI-SCAN-REL-01` (Scan Reliability Score) and save it in the snapshot. Handle division by zero edge-cases (defaults to 100.0).
- **Risk Level**: Medium

### Task ID: TEL-05 (Formula Seeding)
- **Priority**: P1 (High)
- **Files**: `apps/smriti_retail_os/smriti_retail_os/patches/seed_printability_formula.py` (or a new patch)
- **Dependencies**: None
- **Acceptance Criteria**:
  1. Seed formula `SMRITI-SCAN-REL-01` inside the formula registry.
  2. Include business meaning, expression, and metadata inside the seeding script.
- **Risk Level**: Low

---

## Validation & Rollback Checklist

### Validation
- [ ] `bench run-tests --app smriti_retail_os` passes.
- [ ] Manual POS billing flow (Held -> Recall -> Submit) verified.
- [ ] Manager override works with new PIN.
- [ ] Rclone sync verified via command line `rclone ls`.
- [ ] Telemetry events successfully logged (`SCAN-EVT-001/002/003` values checked in database).
- [ ] Daily aggregation job executes and generates snapshots with correct `SMRITI-SCAN-REL-01` calculations.
- [ ] Raw events older than 90 days are pruned by retention cleaner.

### Rollback
- [ ] `git checkout hooks.py setup.py billing_api.py security_api.py backup_api.py sync_assets.py barcode_api.py`
- [ ] If schema changed: `bench migrate` (Note: Custom fields must be manually deleted if rollback is permanent).

