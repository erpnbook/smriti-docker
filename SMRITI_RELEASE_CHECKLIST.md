# SMRITI Retail OS — Release Governance Checklist

This checklist defines the mandatory operational gates that must pass before any version release or code deployment can occur. These gates transition release governance from documentation into strict automated and manual enforcement.

## Release Blockers (Release Gate Criteria)

A release is **BLOCKED** if any of the following validation checks fail:

| # | Validation Check | Target Scope | Command | Expected Outcome | Status |
| :-: | :--- | :--- | :--- | :--- | :---: |
| **1** | **Unit Tests** | Custom App Suite | `bench run-tests --app smriti_retail_os` | 100% of tests pass | ✅ PASS |
| **2** | **Migration** | Schema Sync | `bench migrate` | Completes with zero errors | ✅ PASS |
| **3** | **Health Check** | Database Integrity Check | `bench execute smriti_retail_os.scripts.smriti_post_migrate_healthcheck.run` | All 10 checks print `PASS` | ✅ PASS |
| **4** | **Restore Test** | Data Recovery Verification | `bench restore <db_sql_path> --force --db-root-username root --db-root-password admin` | Site successfully restores with identical record counts | ✅ PASS |
| **5** | **Install Validation** | Fresh Installation Sync | `bench install-app smriti_retail_os` | Fresh site installs cleanly with zero manually-applied schema updates | ✅ PASS |

---

## Pre-Release Step-by-Step Protocol

Follow these steps exactly before generating a git release tag:

### Step 1: Run Unit Tests
Verify all 277+ backend tests are passing cleanly:
```bash
docker exec smriti_retail-backend-1 bench --site smriti_retail run-tests --app smriti_retail_os
```

### Step 2: Run Post-Migrate Health Check
Execute the health check script on the production-scale site:
```bash
docker exec smriti_retail-backend-1 bench --site smriti_retail execute smriti_retail_os.scripts.smriti_post_migrate_healthcheck.run
```

### Step 3: Run Fresh Installation Test
Confirm standard manifests sync on a blank site context without manual updates:
```bash
docker exec smriti_retail-backend-1 bench new-site smriti_release_test --db-root-username root --db-root-password admin --admin-password admin --force
docker exec smriti_retail-backend-1 bench --site smriti_release_test install-app smriti_retail_os
```

### Step 4: Run Restore Validation
Backup the staging database and restore it to confirm zero data loss:
```bash
docker exec smriti_retail-backend-1 bench --site smriti_retail backup --with-files
docker exec smriti_retail-backend-1 bench --site smriti_release_test restore <backup_sql_gz_path> --with-public-files <public_tar> --with-private-files <private_tar> --force --db-root-username root --db-root-password admin
```

### Step 5: Clean Up Release Test Sites
After verification, clean up temporary release testing sites:
```bash
docker exec smriti_retail-backend-1 bench drop-site smriti_release_test --db-root-username root --db-root-password admin --force
```

---

*Governance locked on: 2026-06-18*
*Compliance Officer: Jawahar R Mallah*
