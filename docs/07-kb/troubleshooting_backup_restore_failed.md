---
title: Backup & Restore Runbook
version: 1.0
last_updated: 2026-06-18
applies_to: SMRITI Retail OS v1.x
---

# Support Runbook — Backup or Restore Failures

This runbook guides administrators in troubleshooting database backup extractions, GPG decryption errors, and database restore failures.

## 🚨 Symptom
- Executing `bench backup` fails with database lock warnings.
- Restoring an encrypted backup file returns `"GPG: Decryption Failed"` or `"Invalid Passphrase"`.
- The database restore command exits with SQL constraint violations.

---

## 🔍 Diagnostics Step-by-Step

### Step 1: Troubleshoot GPG Decryption Errors
If decryption fails:
1. Ensure both key custodians have provided their correct fragments.
2. Verify that they are merged in the correct order (Fragment 01 + Fragment 02).
3. Test decryption manually via the terminal to capture verbose errors:
   ```bash
   gpg --verbose --decrypt --passphrase "full_merged_key" --output test_decrypted.sql.gz smriti_backup-v1.enc
   ```
4. If GPG logs `"GPG: public key decryption failed: Bad passphrase"`, the key is incorrect. You must retrieve the original key fragments.

### Step 2: Resolve Database Lock Warnings during Backup
If backups fail because tables are locked:
- SMRITI background tasks might be running heavy reports.
- *Resolution*: Force database dump extraction using the `--skip-lock-tables` option:
  ```bash
  bench --site smriti_retail backup --with-files --skip-lock-tables
  ```

### Step 3: Resolve SQL Constraint Violations during Restore
If restoring database records fails:
- Mismatched custom DocType schemas or active connections can block tables.
- *Resolution*: Terminate active database processes and force schema recreation:
  ```bash
  # Put site in maintenance mode
  bench --site smriti_retail set-maintenance-mode on
  # Force restore database structure
  bench --site smriti_retail restore decrypted_backup.sql.gz --force --db-root-username root --db-root-password admin
  # Turn maintenance mode off
  bench --site smriti_retail set-maintenance-mode off
  ```
