# SMRITI PSV Go-Live Readiness Checklist

---

### Author Profile (Start)
- **Author**: Jawahar R. Mallah
- **Designation**: Founder & Chief Architect
- **Organization**: AITDL – AI Technology & Development Lab
- **Professional Experience**: 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.

> "Light begins with learning."
> 
> — Jawahar R. Mallah
> Founder & Chief Architect, AITDL

---

## 1. Objective of the Checklist
This checklist establishes the final readiness gate before activating the **SMRITI Inventory Visibility Layer** for a brand and its distributor network. It ensures data, security, and configuration settings are validated.

---

## 2. Go-Live Gates & Checklist Items

### Phase 1: Core Configuration & Mapping
- [ ] **SMRITI PSV Settings**: Setup default reorder lookback days (default 30 days) and stale threshold limits.
- [ ] **Party Stock Accounts (PSA)**: Create a PSA record for every distributor, linking the customer record in ERPNext to the SMRITI Partner ID.
- [ ] **HSN Tax Templates**: Verify that ERPNext Item HSN codes are mapped to correct GST templates (e.g. dynamic brackets for apparel/footwear).

### Phase 2: Inventory & Costing Setup
- [ ] **Standard Costing**: Confirm that cost price or standard landed cost is populated in the Item Master for all SKUs (required for Capital Locked math).
- [ ] **Opening Stock Load**: Process the opening inventory for all distributor depots via SMRITI Opening Stock Upload.
- [ ] **Checksum Fingerprint Verification**: Run test re-imports to confirm the MD5 fingerprint engine blocks duplicate uploads.

### Phase 3: Partner Portals & Logins
- [ ] **User Role Permissions**: Assign SMRITI Distributor and Store Manager roles to distributor staff.
- [ ] **Rule 9 Verification**: Confirm that distributor logins do not have access to Frappe Desk (`/desk`) and are redirected to SMRITI custom routes.
- [ ] **Local Offline Billing**: Verify that POS billing works offline when network connection is severed.

### Phase 4: Planners & Replenishment Setup
- [ ] **ROP Rule Definitions**: Create SMRITI PSV Reorder Rules for specific item categories, assigning Lead Times and Safety Stocks.
- [ ] **WOC Alert Thresholds**: Configure Green, Watch, and Action zones in PSV settings.
- [ ] **Exception Alert limits**: Confirm exception logs trigger properly for negative shadow balances.

---

## 3. Go-Live Sign-Off Gate

This module is ready for live deployment once all checks in Phases 1–4 are marked complete.

---

### Author Profile (End)
- **Author**: Jawahar R. Mallah
- **Designation**: Founder & Chief Architect
- **Organization**: AITDL – AI Technology & Development Lab
- **Professional Experience**: 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.

> "Light begins with learning."
> 
> — Jawahar R. Mallah
> Founder & Chief Architect, AITDL

---
*SMRITI Retail OS Enablement Suite | AITDL Network*
