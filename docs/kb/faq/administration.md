---
title: Administration FAQ
version: 1.0
last_updated: 2026-06-18
applies_to: SMRITI Retail OS v1.x
---

# Frequently Asked Questions — Administration

### Q1: What constitutes a critical blocker on the Go-Live Readiness page?
**A**: Any checklist item returning a status of `FAIL` is a critical blocker. An active blocker sets the overall readiness status to `NOT READY`, preventing release certification. Examples include having 0 active items in the catalogue, 0 warehouses, or no POS Profiles.

### Q2: How is the Go-Live Readiness Score calculated?
**A**: The score represents the percentage of passed checklist items out of the 14 validation checks. A score of **90%+ with zero critical blockers** is required for production cutover approval.

### Q3: Why is Backup Encryption shown as an INFO warning?
**A**: Backup encryption is a highly recommended security practice for enterprise environments, but it is not a blocker for core register billing. The system displays this item with an `INFO` status, allowing pilot rollouts while tracking the task for completion.

### Q4: How do I re-run the readiness checks after fixing an issue?
**A**: Open the Go-Live Readiness page (`/smriti-go-live`) and click the **Re-run Checks** button in the topbar. The backend will re-evaluate all parameters and update the readiness score in real-time.

### Q5: Can I bypass the Go-Live Readiness Checklist blocks?
**A**: No. SMRITI constitution does not allow manual overrides of critical validation checklist failures. Blockers must be resolved (e.g. seeding sellable items or creating warehouse accounts) to pass validation.
