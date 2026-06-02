# SMRITI Recovery Architecture

## 1. The Recovery Layer Strategy
SMRITI's Recovery Layer is designed for **On-Site Operational Continuity**. Unlike standard cloud-only backups, it prioritizes localized restore capabilities to minimize store downtime.

### 1.1 Automated Recovery Hooks
- **Auto-Repair**: The system utilizes the `after_migrate` hook to run `setup_smriti_retail_os` and `sync_assets`.
- **Benefit**: If a site's assets are corrupted or the schema is partially lost, a simple `bench migrate` acts as a **Deep Repair Wizard**.

## 2. Backup Strategy Audit
### 2.1 Native Integration (`backup_api.py`)
- **Strategy**: Wraps `frappe.utils.backups.new_backup` to ensure 100% compatibility with the Frappe restore engine.
- **Off-site Sync**: Supports Email-based backups for small/medium databases.
- **Finding (P1)**: Email-based backups will fail for enterprise-grade databases (>25MB attachments). 
- **Recommendation**: Replace Email backup with S3/Rclone integration for multi-store scalability.

### 2.2 Local Retention
- **Policy**: Configurable retention (default 30 days) via `_cleanup_old_backups`.
- **Risk (P2)**: Local backups share the same volume as the live DB. A disk-level failure in the Docker volume destroys both.

## 3. Disaster Recovery (DR) Scenarios
| Scenario | SMRITI Recovery Path | Confidence |
|---|---|---|
| **Database Corruption** | `restore_backup(file_name)` via Backend API | High |
| **Asset Corruption** | Automated `sync_assets` on container boot | Very High |
| **Site Config Loss** | Manual restore from `site_config_backup.json` | Medium |
| **Orchestration Failure** | Re-run `install.ps1` (Hard Reset) | High |

## 4. Operational Continuity (Billing Resilience)
- **Billing Fallback**: `billing_api.py` includes a fallback to standard **Sales Invoices** if the POS Shift API fails or no shift is open.
- **Integrity**: Programmatic `docstatus` checks in `close_shift` ensure that shifts cannot be closed with unsubmitted invoices.

---
*Reference: `backup_api.py`, `shift_api.py`, `sync_assets.py`*
