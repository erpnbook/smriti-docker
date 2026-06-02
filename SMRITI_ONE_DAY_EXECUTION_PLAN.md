# SMRITI One-Day Execution Plan (War Room Mode)

**Goal**: Complete all 5 critical patches today with 0% residual P0/P1 risk.  
**Strategy**: Parallelize non-dependent workstreams; sequential deployment for schema-impacting changes.

## 1. Workstream Assignments

| Stream | Focus Area | Tasks | Primary Lead |
|---|---|---|---|
| **Stream A** | **Security** | SEC-01, SEC-02 | Security Agent |
| **Stream B** | **Billing** | REL-02 | Senior Backend Agent |
| **Stream C** | **Infrastructure** | REL-01 | DevOps Agent |
| **Stream D** | **Backup** | CLD-01 | Infrastructure Agent |

---

## 2. Optimized Timeline (12-Hour Sprint)

### Hour 0-1: Environment Preparation & Safety Lock
- **Action**: Create `production_release_v1_0_patch` branch.
- **Action**: Take full snapshot of the production-equivalent database.
- **Action**: Initialize all 4 AI Streams with their respective `SMRITI_AGENT_TASKS.md` segments.

### Hour 1-3: Parallel Implementation (The "Build" Phase)
- **Stream A**: Implement SEC-01 (Governance Guard) and SEC-02 (PIN Field Schema in `setup.py`).
- **Stream C**: Implement REL-01 (Rsync Atomic Swap).
- **Stream D**: Implement CLD-01 (Rclone Infrastructure setup in `backup_api.py`).

### Hour 3-4: The "Critical Pivot" (Stream B Start)
- **Stream B**: Begin REL-02 (Idempotency + Enqueue logic). This depends on SEC-02's schema stability.
- **Stream A**: Testing SEC-01/02 in a isolated container.

### Hour 4-6: Integration & Conflict Resolution
- **Action**: Merge Stream A and Stream C into the patch branch. 
- **Action**: Run `bench migrate` in staging to verify `setup.py` no longer deletes the `custom_smriti_pin`.

### Hour 6-8: Intensive Testing (The "Chaos" Phase)
- **Stream B**: Stress test `submit_bill` with network latency simulation.
- **Stream C**: Verify Nginx asset availability during `rsync` atomic swaps.
- **Stream D**: Validate S3 connectivity and pre-signed URL generation.

### Hour 8-10: Staging Final Validation
- **Action**: Full end-to-end POS flow: Open Shift -> Bill (with Manager PIN) -> Submit -> Day Close -> Backup.
- **Action**: Audit `SMRITI_FINAL_VERIFIED_BLOCKERS.md` to ensure every proof-of-failure now results in a "Success/Blocked" state.

### Hour 10-12: Production Deployment & Monitoring
- **Action**: Deployment to production via `bench migrate`.
- **Action**: Live monitoring of worker logs (`bench watch`).
- **Action**: Final Master Checklist Sign-off.

---

## 3. Execution Metrics & Rollback

| Task ID | Implementation Time | Testing Time | Rollback Strategy |
|---|---|---|---|
| **SEC-01** | 30m | 30m | Git Revert `security_api.py` |
| **SEC-02** | 90m | 60m | Delete Custom Field; Revert `setup.py` |
| **REL-01** | 60m | 30m | Revert `sync_assets.py` (No data impact) |
| **REL-02** | 180m | 120m | Revert `billing_api.py` |
| **CLD-01** | 120m | 60m | Disable S3 settings in UI |

---
*Command Authority: War Room Lead AI*
