# SMRITI Patch Implementation Plan: Production Rollout

This plan outlines the phased rollout of the critical security and reliability patches for SMRITI Retail OS.

---

## Phase 1: Emergency Security Fixes (Immediate)
**Goal**: Neutralize Admin Hijacking and Credential Exposure risks.

### Task 1.1: Deploy Governance Guard
- **Action**: Patch `security_api.py` to implement Role-Based Reset Scoping.
- **Verification**: Attempt to reset a `System Manager` password from a `SMRITI Store Manager` account. Expect failure.
- **Downtime**: 0 minutes.

### Task 1.2: Deploy Stealth-PIN Schema
- **Action**: Update `setup.py` to add `custom_smriti_pin` to the `User` DocType. Run `bench migrate`.
- **Action**: Patch `billing_api.py` and `shift_api.py` to check the PIN field.
- **Action**: Add "Set POS PIN" UI to Security Center.
- **Verification**: Set a PIN for a manager and verify it works on the POS terminal while the old password still functions as a fallback.
- **Downtime**: 5 minutes (Migration).

---

## Phase 2: Operational Reliability (Day 2-5)
**Goal**: Secure billing integrity and eliminate UI downtime.

### Task 2.1: Deploy Atomic Asset Swap
- **Action**: Replace `sync_assets.py` logic with the Shadow Swap strategy.
- **Verification**: Trigger a manual `sync_assets` and monitor POS terminal for 404 errors during the sync.
- **Downtime**: 0 minutes.

### Task 2.2: Deploy Transaction Guard
- **Action**: Wrap `submit_bill` in explicit transaction blocks.
- **Verification**: Run "Chaos Tests" (kill worker process during submission) and verify no "Zombie" invoices are created.
- **Downtime**: 0 minutes.

---

## Phase 3: Infrastructure Hardening (Day 6-10)
**Goal**: Scale recovery mechanisms to handle enterprise growth.

### Task 3.1: Deploy Cloud-Link (Rclone)
- **Action**: Add Cloud configuration fields to `SMRITI Company Settings`.
- **Action**: Implement `rclone` sync logic in `backup_api.py`.
- **Verification**: Run manual cloud backup and verify file presence in the S3 bucket.
- **Downtime**: 0 minutes.

---

## Post-Implementation Review
- **Audit**: Conduct a follow-up forensic audit to confirm that P0/P1 risks are fully mitigated.
- **Training**: Distribute "Manager POS PIN Usage" guide to all store locations.
- **Cleanup**: In the next major release (v1.1.0), remove the password-as-PIN fallback code.

---
*Release Manager: SMRITI Retail OS Release Team*
