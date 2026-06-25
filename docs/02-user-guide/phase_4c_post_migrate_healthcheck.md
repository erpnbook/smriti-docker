# SMRITI Retail OS — Phase 4C Post-Migrate Health Check Report

This report presents the validation results for the automated post-migration health checking suite of SMRITI Retail OS.

## Health Check Command

The reusable post-migrate verification script is registered under the custom app scripts directory. It can be run after any migration or app update to verify platform integrity:

```bash
bench --site smriti_retail execute smriti_retail_os.scripts.smriti_post_migrate_healthcheck.run
```

## Health Check Output Summary

All 10 checks passed successfully in both the production-scale site (`smriti_retail`) and the fresh testing site (`smriti_install_test`):

```text
================ SMRITI POST-MIGRATE HEALTH CHECK ================
PASS  DocType Registry
PASS  Missing Tables
PASS  Missing Fields
PASS  Custom Fields
PASS  Property Setters
PASS  Fixtures
PASS  Seed Records
PASS  Company Settings
PASS  Report Templates
PASS  Print Jobs
==================================================================
```

## Checked Metrics & Verification Rules

1. **DocType Registry**: Verifies that all 14 Custom DocTypes exist in the active Frappe metadata dictionary.
2. **Missing Tables**: Verifies that physical database tables exist for all non-single DocTypes.
3. **Missing Fields**: Compares the database columns with the field properties inside the manifests to verify they are synchronized.
4. **Custom Fields**: Confirms that SMRITI-owned custom fields on standard DocTypes (e.g. `Address` and `Contact`) exist.
5. **Property Setters**: Checks that customized schema overrides are correctly synchronized.
6. **Fixtures**: Verifies SMRITI standard roles (`SMRITI Cashier`, `SMRITI Store Manager`) and the workspaces are correctly registered.
7. **Seed Records**: Confirms standard operational seeds (like Payment Modes) are present.
8. **Company Settings**: Verifies that SMRITI Company Settings documents are fully readable.
9. **Report Templates**: Confirms standard report templates are loaded and queryable.
10. **Print Jobs**: Checks print job table loading.

---

*Report compiled on: 2026-06-18*
*Validation status: 100% COMPLETE & PASSING ✅*
