# SMRITI Governance Audit

## 1. Governance Architecture: "The Air Gap"
SMRITI implements a hard programmatic split between the **Business Owner (Admin)** and the **Security Architect (Administrator)**.

### 1.1 Administrator vs Business Owner
- **Administrator (root)**: Reserved for recovery, schema updates, and high-risk security operations (handled by `check_administrator_only`).
- **Admin (Business Owner)**: Specifically **blocked** from the SMRITI Security Center via `check_store_manager_or_admin` in `security_api.py`.
- **Finding (P0)**: This is a robust governance feature that prevents "accidental elevation" by store owners, but it relies on string-matching ("Admin", "admin@smriti.io").
- **Recommendation**: Formalize this into a "System Admin" flag on the User DocType to avoid email-dependency.

### 1.2 Permission Separation
- **Store Managers**: Scoped to "Company" and "Warehouse" permissions only. Programmatically enforced in `add_user_permission`.
- **Cashiers**: Strictly limited to the POS interface with ZERO access to User administration.
- **Auditability**: `SMRITI Address Audit Log` provides a governance layer for physical store metadata, though it is currently limited to specific fields.

## 2. Privilege Escalation Paths
### 2.1 The "Reset Password" Vector
- **Risk (P1)**: The `reset_user_password` API allows a Store Manager to reset passwords for any user EXCEPT the Administrator.
- **Scenario**: A malicious Store Manager could reset a System Manager's password to gain full Desk access.
- **Fix**: Restrict Store Managers to only resetting passwords for users with "SMRITI Cashier" roles.

### 2.2 Billing Role Hijacking
- **Risk (P2)**: `billing_api.py` uses `frappe.auth.check_password(mgr, pin)` for overrides. Since this validates the user's primary password, if a manager uses a weak password, it can be easily compromised on the POS terminal via shoulder-surfing.
- **Fix**: Implement a non-reversible salt+hash for the dedicated PIN field.

## 3. Recovery from Permission Corruption
- **Mechanism**: SMRITI relies on `after_migrate` hooks in `hooks.py` to re-instantiate standard roles and permissions.
- **Audit**: This provides a "Self-Healing" governance layer. Even if a local System Manager accidentally deletes the "SMRITI Cashier" role, the next `bench migrate` will restore it from `setup.py`.

---
*Reference: `security_api.py`, `hooks.py`, `billing_api.py`*
