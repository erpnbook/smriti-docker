# SMRITI Patch Architecture Review

**Reviewer**: Principal Frappe/ERPNext Architect  
**Status**: Critical Framework Alignment Review

---

## 1. Patch: Governance Guard (Privilege Escalation)
- **Hidden Risks**: High. Role-based scoping in `reset_user_password` is fragile. If a user has *multiple* roles, simply checking if "SMRITI Cashier" is present might overlook that they also have "System Manager" or "Accounts Manager" roles.
- **Frappe Framework Conflicts**: None.
- **ERPNext Upgrade Risks**: Low.
- **Migration Risks**: None.
- **Performance Risks**: Low.
- **Rollback Risks**: Low.
- **CTO Verdict**: **APPROVE_WITH_CHANGES**
- **Required Changes**: Do not just check for the presence of "SMRITI Cashier". You must ensure the target user **does not** possess any role with `desk_access=1` or specifically `System Manager` role. The logic must be: "If requester is Store Manager, target must ONLY have non-desk roles or SMRITI Cashier role."

---

## 2. Patch: Stealth-PIN (POS Credential Protection)
- **Hidden Risks**: Medium. Data loss during migration. If `setup.py` contains logic that deletes the field (as seen in Line 588 of `setup.py`), any saved PINs will be wiped on the next `bench migrate`.
- **Frappe Framework Conflicts**: Using `Password` field type for a 4-digit PIN is slightly non-standard but functional. However, standard Frappe `check_password` logic might trigger rate-limiting or security logs intended for full account passwords.
- **ERPNext Upgrade Risks**: Low, as it is a Custom Field.
- **Migration Risks**: **CRITICAL**. You must remove the `frappe.delete_doc("Custom Field", "User-custom_smriti_pin", ...)` line from `setup.py` before deploying this patch, or the PINs will be deleted immediately after creation.
- **Performance Risks**: Low.
- **Rollback Risks**: Low.
- **CTO Verdict**: **APPROVE_WITH_CHANGES**
- **Required Changes**: 
  1. Use `Data` field type with `Password` property or a custom implementation to avoid conflict with main account password rate-limiting.
  2. **Mandatory**: Fix the destructive logic in `setup.py` Line 588.

---

## 3. Patch: Cloud-Link (Backup Scalability)
- **Hidden Risks**: Security. Storing S3 Keys/Secrets in `SMRITI Company Settings` (a Custom DocType) makes them visible to anyone with access to that DocType.
- **Frappe Framework Conflicts**: Redundancy. Frappe already has "S3 Backup" settings in the core. Overriding this with a custom SMRITI implementation might confuse system admins.
- **ERPNext Upgrade Risks**: Low.
- **Migration Risks**: High effort to configure for 100+ stores manually.
- **Performance Risks**: Rclone is a separate process. If triggered synchronously via API, it could lead to Gunicorn timeouts.
- **CTO Verdict**: **APPROVE_WITH_CHANGES**
- **Required Changes**: Use Frappe's `Password` field type for S3 Secrets. Trigger the Rclone sync via `frappe.enqueue` to avoid blocking the request thread.

---

## 4. Patch: Atomic Asset Swap (Zero-Downtime Sync)
- **Hidden Risks**: Volume Locking. In a Docker environment, `os.rename` can fail if the destination directory is being actively read by Nginx or locked by another process.
- **Frappe Framework Conflicts**: None.
- **ERPNext Upgrade Risks**: None.
- **Migration Risks**: None.
- **Multi-store Risks**: High IO during the swap if 100 containers restart at once.
- **CTO Verdict**: **REJECT**
- **Architectural Alternative**: Use **`rsync` with the `--atomic` and `--delay-updates` flags**. `rsync` is a production-grade tool designed for this exact purpose. It handles partial copies in a hidden directory and performs the swap natively. It is far safer than manual `shutil` operations in a multi-tenant Docker environment.

---

## 5. Patch: Transaction Guard (Billing Integrity)
- **Hidden Risks**: **Deadlocks**. Wrapping complex ERPNext logic like `invoice_doc.submit()` (which triggers GL entries, Stock Ledger entries, and potentially hundreds of hooks) inside an *additional* explicit `frappe.db.begin()` can cause MariaDB deadlocks under high concurrency.
- **Frappe Framework Conflicts**: Frappe already wraps every web request in a transaction. `submit()` itself is a transactional operation.
- **ERPNext Upgrade Risks**: High. If core ERPNext changes its internal transaction handling, this manual wrapper might break.
- **CTO Verdict**: **REJECT**
- **Architectural Alternative**: Use **IDEMPOTENCY KEYS**. Instead of a giant transaction, ensure each step (Invoice, Payment, Loyalty) checks if it has already been performed for the current "Billing Session ID". Use a **Background Job (`frappe.enqueue`)** for non-critical post-submission steps (like Loyalty points or non-critical Payment reconciliations) with a retry mechanism. This keeps the POS responsive and ensures eventual consistency without risking DB locks.

---
*Review Summary: Phases 1 and 2 (Security) are approved with minor logic adjustments. Phase 4 and 5 require significant architectural pivots to align with Frappe/ERPNext production standards.*
