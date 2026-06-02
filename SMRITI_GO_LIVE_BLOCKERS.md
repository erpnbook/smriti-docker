# SMRITI Go-Live Blockers (Retail CTO Review)

This report identifies only "Business Stoppers" verified from the source code.

---

## 1. BLK-01: Admin Account Hijacking via Manager Reset
- **Severity**: **CRITICAL**
- **Evidence**: `security_api.py:100` (`reset_user_password`)
- **Reproduction**: A Store Manager can reset the password of any System Manager.
- **Why it stops business**: A disgruntled manager can lock the owner out of the system, delete all sales data, and export the customer list before a single Day-Close is completed.
- **Fix Effort**: **Low** (Add role check in `reset_user_password`).

## 2. BLK-02: POS Shoulder-Surfing Vulnerability
- **Severity**: **HIGH**
- **Evidence**: `billing_api.py:560` and `shift_api.py:310`
- **Reproduction**: Manager uses their full ERPNext password to approve a cashier's voided item.
- **Why it stops business**: Cashiers observing the password gain full control over the manager's account. This leads to untraceable inventory theft and fraudulent "held" bill manipulations.
- **Fix Effort**: **Medium** (Implement hashed `custom_pin` field).

## 3. BLK-03: Silent Off-site Backup Failure
- **Severity**: **HIGH**
- **Evidence**: `backup_api.py:300` (`_email_backup`)
- **Reproduction**: Database grows >25MB. SMTP server rejects the email.
- **Why it stops business**: Standard retail DBs hit 25MB within weeks. If the store's local server fails (disk crash), there is zero recovery path. The business loses all inventory and outstanding credit history.
- **Fix Effort**: **Medium** (Integrate Rclone/S3).

## 4. BLK-04: Asset Sync Race Condition (Nginx 404/502)
- **Severity**: **MEDIUM**
- **Evidence**: `sync_assets.py:30` (`shutil.rmtree(dst_dir)`)
- **Reproduction**: Containers restart while the store is busy. `sync_assets` deletes the shared asset folder to copy fresh files.
- **Why it stops business**: During the copy process (which can take minutes), the billing terminal will show "404 Not Found" or have no CSS/JS. Cashiers cannot bill customers during this window.
- **Fix Effort**: **Medium** (Use atomic `rsync` or temp-folder-swap).

## 5. BLK-05: Missing Transaction Integrity in Billing
- **Severity**: **MEDIUM**
- **Evidence**: `billing_api.py:200` (`submit_bill` lacks explicit `frappe.db.begin` or atomic transaction wrapping for multi-doc creation).
- **Reproduction**: Network interruption during the final submission of a loyalty-linked POS Invoice.
- **Why it stops business**: Partial data commits (e.g., Invoice created but Loyalty Points not deducted or Shift Summary not updated) lead to stock/financial reconciliation nightmares.
- **Fix Effort**: **Low** (Wrap `submit_bill` in a transaction block).

---
*CTO Assessment: SMRITI is NOT production-ready until BLK-01 and BLK-02 are patched.*
