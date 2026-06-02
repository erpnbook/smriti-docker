# SMRITI Verified Critical Risks (Forensic Audit)

This report contains only risks verified through direct source code analysis of `D:\Smriti_Retail_OS`.

---

## 1. Privilege Escalation via User Password Reset
- **Classification**: **VERIFIED_P0**
- **File**: `apps/smriti_retail_os/smriti_retail_os/security_api.py`
- **Function**: `reset_user_password(email, password)`
- **Code Snippet**:
  ```python
  def reset_user_password(email, password):
      """Updates standard user password securely."""
      check_store_manager_or_admin()
      check_administrator_protection(email)
      # ...
      update_password(email, password)
  ```
- **Reproduction Steps**:
  1. Login as a user with `SMRITI Store Manager` role.
  2. Call `smriti_retail_os.security_api.reset_user_password` with the email of any `System Manager` (non-Administrator).
  3. The `check_administrator_protection` only blocks resets for the "Administrator" user, allowing managers to hijack any other administrative account.
- **Business Impact**: A malicious store-level employee can take full control of the entire ERPNext Desk, modify financial records, or export sensitive company data.

---

## 2. Insecure Manager Overrides (Password as PIN)
- **Classification**: **VERIFIED_P1**
- **File**: `apps/smriti_retail_os/smriti_retail_os/billing_api.py`
- **Function**: `validate_manager_override(pin, action_type, invoice_name=None)`
- **Code Snippet**:
  ```python
  for mgr in set(managers):
      # ...
      try:
          # Use frappe.auth.check_password to authenticate the manager's password
          frappe.auth.check_password(mgr, pin)
  ```
- **Reproduction Steps**:
  1. Perform a restricted action on the POS (e.g., Delete Item).
  2. When prompted for "PIN", enter the Manager's full ERPNext login password.
  3. The system validates the primary password instead of a dedicated, shorter PIN.
- **Business Impact**: Managers are forced to type their primary system credentials in front of cashiers and customers (shoulder surfing). Once a cashier observes the password, they gain full administrative access to the manager's account.

---

## 3. Email Backup Failure (Enterprise Scale)
- **Classification**: **VERIFIED_P1**
- **File**: `apps/smriti_retail_os/smriti_retail_os/backup_api.py`
- **Function**: `_email_backup(file_path, settings)`
- **Code Snippet**:
  ```python
  with open(file_path, "rb") as attachment:
      part = MIMEBase("application", "octet-stream")
      part.set_payload(attachment.read())
      # ...
  smtp.sendmail(user, recipient, msg.as_string())
  ```
- **Reproduction Steps**:
  1. Grow the database until the compressed `.sql.gz` backup exceeds 25MB (typical SMTP limit).
  2. Trigger the backup.
  3. The `smtp.sendmail` call will fail or be rejected by the recipient's mail server.
- **Business Impact**: The primary off-site recovery mechanism fails silently as data grows. In a disaster scenario, the company will discover they have no recent off-site backups.

---

## 4. Unsafe Manager PIN Logic Redundancy
- **Classification**: **VERIFIED_P1**
- **File**: `apps/smriti_retail_os/smriti_retail_os/shift_api.py`
- **Function**: `_validate_manager_pin(pin, action_type, reference_name=None)`
- **Code Snippet**:
  ```python
  def _validate_manager_pin(pin, action_type, reference_name=None):
      # ...
      try:
          frappe.auth.check_password(mgr, pin)
  ```
- **Reproduction Steps**: Identical to Finding #2, but occurs during Day-Close variance overrides.
- **Business Impact**: Duplication of insecure credential handling logic increases the attack surface and technical debt.

---
*Audit performed on 2026-06-02. Verified via repository source code.*
