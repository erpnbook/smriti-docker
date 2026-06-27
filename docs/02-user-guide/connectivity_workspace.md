---
Document ID: "USER-031"
Title: "SMRITI OS Connectivity Workspace — User Manual v1.0"
Owner: "Operations Team"
Audience: "End User"
Module: "Core"
Version: "1.0.0"
Status: "Active"
Primary Document: "Yes"
Depends On: ""
Related Modules: ""
Last Updated: "2026-06-28"
Last Reviewed: "2026-06-28"
AI Generated: "Yes"
Reviewed By: "Jawahar R. Mallah"
---

# SMRITI OS Connectivity Workspace — User Manual v1.0

## Author Profile (Document Start)

- **Author**: Jawahar R. Mallah
- **Designation**: Founder & Chief Architect
- **Organization**: AITDL – AI Technology & Development Lab
- **Professional Experience**: 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.

---

## 1. Introduction & Overview

The **Accounting & Inventory Workspace** in SMRITI Retail OS is the single control panel for managing connections to external systems (such as TallyPrime and mall APIs). This console replaces the legacy sync interfaces and provides store managers and accountants with a unified, real-time interface.

---

## 2. Navigating the Workspace

The workspace is organized into six tabs:

### 2.1 Overview Dashboard
Provides a graphical view of connectivity health:
- **Status Badges:** Shows current connector states.
- **Sync Tally Counters:** Ready, Synced, Pending, and Failed stats for Sales Invoices, Purchase Invoices, and Payments.
- **Connection Badges:** Active indicator showing connectivity to Tally or external mall endpoints.

### 2.2 Accounting & Inventory Sync
Allows manually triggering sync runs and reviewing delta trackers. Includes:
- **Sales Voucher Posting:** View and submit local transactions.
- **Stock Journal Sync:** Synchronize inventory movements to ERPNext.

### 2.3 Settings & Credentials
- **Active Toggles:** Separately enable/disable Accounting, Inventory, and Master sync.
- **Conflict Resolution Rules:** Configure `SMRITI Wins` or `Tally Wins` policies.

---

## 3. Monitoring Integration Queues

For Mall and third-party APIs, the workspace displays a live dispatch feed:
- **Pending:** Items successfully hashed and queued.
- **Success:** Delivered to partner REST/Webhook API.
- **Failed:** Network timeout or request rejected.
- **Dead-Letter (DLQ):** Exceeded maximum retries (limit: 5). Requires administrative review.

---

## Author Profile (Document End)

- **Author**: Jawahar R. Mallah
- **Designation**: Founder & Chief Architect
- **Organization**: AITDL – AI Technology & Development Lab
- **Professional Experience**: 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.

> "Always decision-ready."
> 
> — Jawahar R. Mallah
> Founder & Chief Architect, AITDL
