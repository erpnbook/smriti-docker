# SMRITI Retail OS — Phase 3 Installation & Upgrade Matrix

This document tracks the installation and upgrade validation scenarios required under Gate 5 before Phase 3C (Runtime Cleanup) can be initiated.

## Installation & Upgrade Matrix

| Scenario | Target Environment | Executed Command | Status | Verification Metrics |
| :--- | :--- | :--- | :--- | :--- |
| **Existing Site Upgrade** | `smriti_retail` (MariaDB/Docker) | `bench migrate` | ✅ PASS | Synced 14 JSON manifests; converted `custom` to `0` for all target DocTypes. No data loss. |
| **Incremental bench migrate** | `smriti_retail` (MariaDB/Docker) | `bench migrate` | ✅ PASS | Execution completes with zero-op changes and no duplicate/orphan doctype conflicts. |
| **Fresh Site Install** | Blank site `smriti_test` | `bench install-app smriti_retail_os` | ⏳ PENDING | To be verified in the staging/testing environment prior to Phase 3C cutover. |
| **bench update** | Upgrade testbed | `bench update` | ⏳ PENDING | Verification of git pull + dependency resolution + auto-migration. |
| **Restore from Backup** | Backup verification env | `bench restore <backup_path>` | ⏳ PENDING | Verify SMRITI Backup engine payloads can be successfully restored with manifest compatibility. |

---

*Baseline compiled on: 2026-06-18*
*Release Gate Status: PENDING Observation Window*
