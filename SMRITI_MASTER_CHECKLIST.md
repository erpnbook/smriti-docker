# SMRITI Master Release Checklist (Go-Live)

This checklist must be 100% complete before the production environment is released for billing.

## 1. Security & Governance (Stream A)
- [ ] **SEC-01**: Verified that `reset_user_password` blocks attempts to reset `System Manager` or `Administrator` accounts by non-admins.
- [ ] **SEC-02**: `User` DocType contains `custom_smriti_pin` field.
- [ ] **SEC-02**: `setup.py` no longer contains the destructive `delete_doc` for the PIN field.
- [ ] **SEC-02**: POS Override accepts the 4-6 digit `custom_smriti_pin`.
- [ ] **SEC-02**: POS Override still accepts the primary password (if no PIN is set) for backward compatibility.

## 2. Operational Reliability (Stream B & C)
- [ ] **REL-01**: Asset sync verified using `rsync` with atomic flags.
- [ ] **REL-01**: Confirmed zero 404 errors during a live asset sync while browsing the billing terminal.
- [ ] **REL-02**: `submit_bill` includes idempotency check against a unique `billing_session_id`.
- [ ] **REL-02**: Verified that `Payment Entry` and `Loyalty` updates are enqueued correctly.
- [ ] **REL-02**: Verified that a simulated network failure during `submit_bill` does not create "Zombie" invoices.

## 3. Infrastructure & Recovery (Stream D)
- [ ] **CLD-01**: S3/Cloud credentials saved in `SMRITI Company Settings` are masked (Password field type).
- [ ] **CLD-01**: `rclone` binary confirmed accessible in the backend container.
- [ ] **CLD-01**: Successful manual trigger of cloud backup with pre-signed URL verification.
- [ ] **CLD-01**: Email backup notifications no longer contain large attachments.

## 4. Final Smoke Test (Integrated)
- [ ] Open shift as Cashier.
- [ ] Add items to cart -> Hold Bill -> Recall Bill.
- [ ] Trigger Manager Override (Delete Item) using new PIN.
- [ ] Submit Bill -> Verify Invoice status and stock deduction.
- [ ] Perform Day Close -> Verify summary totals.
- [ ] Trigger manual Backup -> Verify cloud sync.

## 5. Rollback Preparedness
- [ ] Verified that a `git checkout main` and `bench migrate` restore the system to its pre-patch state.
- [ ] Database backup taken immediately prior to deployment.

---
**Approval Signature**: __________________________ (War Room Lead)  
**Date/Time**: 2026-06-02 / 12:00 PM
