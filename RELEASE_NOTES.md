# RELEASE NOTES — smriti-docker v2.4.1
# Release Date: 2026-07-04
# Previous Release: v2.4.0
# Commits since last tag: 2

## Summary

Maintenance release to synchronize bundled app version reference to
smriti_retail_os v2.1.0 (Engineering Governance). Updates .gitignore
to exclude verification screenshot artifacts and adds architecture
governance docs from cloud migration.

## App Version Sync

| App                | Previous | Current |
|--------------------|----------|---------|
| smriti_retail_os   | 2.0.0    | 2.1.0   |
| frappe             | v16.19.1 | v16.19.1|
| erpnext            | v16.19.1 | v16.19.1|

### smriti_retail_os v2.1.0 — Engineering Governance highlights:
- Automated E2E UI Integration Regression Test Suite (5 headless DOM tests)
- Config-driven SMRITI_DEVELOPER_MODE via frappe.conf.developer_mode
- Centralized Roles constants: Accountant, Sales Manager, SMRITI Team
- RELEASE_GATE_CRITERIA.md and QUALITY_DASHBOARD.md
- Purchase Studio dynamic sidebar (L/R/T/B, collapse, popout, hash routing)

## Repository Maintenance
- `.gitignore` extended to exclude verification screenshots and local
  test artifact files from commits.
- `docs/from-cld/` — Architecture governance files imported:
  - `architecture_baseline.json`
  - `ARCHITECTURE_MIGRATION_BACKLOG.md`
  - `check_architecture_boundaries.py`

## Deployment Notes
No Docker Compose service changes.
No image rebuild required.
Pull latest: `git pull origin main`

## Known Issues
- KI-005: Demo company seeding disabled in Docker env config (intentional)
