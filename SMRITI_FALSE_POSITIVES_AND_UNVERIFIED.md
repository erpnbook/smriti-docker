# SMRITI Audit False Positives

## 1. Unoptimized Stock Queries (`tabBin`)
- **Reason**: Programmatic `SUM` on `tabBin` is the idiomatic and most efficient way to get real-time stock in ERPNext. The previous claim of "bottleneck" was an assumption not supported by standard Frappe performance benchmarks for a single store.

## 2. Non-Standard Schema Definition
- **Reason**: Defining DocTypes in `setup.py` is a valid architectural choice for verticalized "Experience Layer" applications that require automated environment provisioning.

## 3. Worker Starvation at Scale
- **Reason**: While a theoretical risk, there is no evidence in the current repository that background jobs are currently unoptimized or causing lag for the 1-store/5-counter scope.

---

# SMRITI Unverified Findings

## 1. Multi-Store Permission Collision
- **Reason**: **UNVERIFIED**. I have not tested the interaction of `SMRITI Company Settings` across multiple companies in a single site. The code exists to support it, but collision behavior remains speculative.

## 2. Global State Conflict
- **Reason**: **UNVERIFIED**. The use of `frappe.db.get_default` for backup settings is confirmed, but its impact on a multi-tenant site requires a live runtime check of how Frappe handles defaults in a multi-tenant context.

## 3. Plain-Text Credentials in `pwd.yml`
- **Reason**: **UNVERIFIED**. While `123` is present in the example and `pwd.yml`, I cannot verify if the user's actual production environment uses the same insecure configuration.
