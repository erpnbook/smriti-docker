# 📚 SMRITI Retail OS — Knowledge Base

> **Single-source overview.** This document is the entry point to all project documentation, completed features, open risks, architecture decisions, and operational runbooks.  
> **Last Updated:** 2026-06-05 · **Version:** v1.2.6

> [!TIP]
> Ask Antigravity to "update knowledge base" after any session to keep this file current.

---

## 🗺️ Table of Contents

1. [What is SMRITI Retail OS?](#1-what-is-smriti-retail-os)
2. [Stack & Architecture](#2-stack--architecture)
3. [Repository Structure](#3-repository-structure)
4. [Documentation Index](#4-documentation-index)
5. [Completed & Locked Features](#5-completed--locked-features)
6. [Open Risk Register](#6-open-risk-register)
7. [Development Roadmap Summary](#7-development-roadmap-summary)
8. [Operational Runbooks](#8-operational-runbooks)
9. [Key API Reference](#9-key-api-reference)
10. [Testing & QA](#10-testing--qa)
11. [Deployment & Infrastructure](#11-deployment--infrastructure)

---

## 1. What is SMRITI Retail OS?

**SMRITI Retail OS** is a premium retail experience layer built on top of **Frappe v16** and **ERPNext v16**. It acts as a _Sophisticated Experience Layer_ (SEL) — transforming the complex ERPNext UI into a cashier-friendly, India GST-compliant POS and merchandising platform tailored for footwear/apparel retail.

### Core Value Proposition

| Layer | Description |
|---|---|
| **POS Billing Terminal** | High-performance, role-locked cashier interface with barcode scanning, hold/recall, manager overrides |
| **Sizewise Item Master** | Pivot-grid Excel import for style × size × color variant management |
| **Shoper9 Pure Mode** | Hides ERPNext desk complexity from cashiers while preserving full ERPNext for admins |
| **India GST Compliance** | Integrated with `india_compliance` for HSN auto-detection, GSTIN validation, and tax templates |
| **Supplier Registry** | Complete vendor management with GST address syncing and Vendor Code validation |
| **B2B Invoice (Sizewise)** | Pivot-grid B2B invoice creation with HID barcode scanner support |

---

## 2. Stack & Architecture

```
┌───────────────────────────────────────────────────────────────┐
│  SMRITI Retail OS  (Custom Frappe App — smriti_retail_os)     │
│  ┌────────────┐  ┌───────────────┐  ┌──────────────────────┐  │
│  │ billing_api│  │item_master_api│  │ sizewise_invoice_api │  │
│  │ shift_api  │  │barcode_api    │  │ master_api           │  │
│  │ security_api│  │ company_api  │  │ backup_api           │  │
│  └────────────┘  └───────────────┘  └──────────────────────┘  │
├───────────────────────────────────────────────────────────────┤
│  ERPNext v16 + Frappe v16 + India Compliance v16              │
├───────────────────────────────────────────────────────────────┤
│  MariaDB  │  Redis (Queues + Cache)  │  Nginx (Asset Guard)   │
├───────────────────────────────────────────────────────────────┤
│  Docker Compose (pwd.yml)  ·  9 Containers                    │
└───────────────────────────────────────────────────────────────┘
```

### Key Architectural Decisions

| Decision | Rationale | Reference |
|---|---|---|
| **HSN-First GST Architecture** | `gst_hsn_code` is the primary source of truth for GST %. `custom_gst_percentage` is auto-derived via the lookup chain: `HSN Code → GST HSN Code.taxes → Item Tax Template → SUM(tax_rate)`. Falls back to manual entry when HSN has no configured taxes. | [hooks_logic.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/hooks_logic.py) — `get_gst_rate_from_hsn()` |
| **Dynamic State Fallback** | Address state resolution reads `Company.state` instead of hardcoded `"Karnataka"` — ensures correct CGST/SGST splits for any Indian state | [hooks_logic.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/hooks_logic.py) — `_get_company_state_fallback()` |
| **Physical Asset Sync** | Unlinks symlinks and hard-copies compiled bundles to Nginx shared volume — eliminates MIME-type 404 errors | [sync_assets.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/sync_assets.py) |
| **Code-driven Schema** | Custom fields and DocTypes created via `setup.py` Python migration, not JSON manifests | [setup.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/setup.py) |
| **ERPNext-First Data** | Company/Address/Supplier data lives in standard ERPNext DocTypes; SMRITI reads/writes through standard APIs | [company_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/company_api.py) |
| **Role-Based Routing** | Cashiers hit `/billing`; System Managers see unaltered ERPNext desk | [hooks.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/hooks.py) |
| **Vendor Code on Supplier** | `custom_vendor_code` unique field on Supplier DocType links external ERP/supplier codes | [setup.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/setup.py) |

Full architecture detail: [ARCHITECTURE_REPORT.md](file:///d:/Smriti_Retail_OS/ARCHITECTURE_REPORT.md)

---

## 3. Repository Structure

```
smriti_retail_os/
├── apps/
│   ├── smriti_retail_os/        ← Main custom app
│   │   └── smriti_retail_os/
│   │       ├── billing_api.py
│   │       ├── item_master_api.py
│   │       ├── sizewise_invoice_api.py
│   │       ├── barcode_api.py
│   │       ├── master_api.py
│   │       ├── company_api.py
│   │       ├── security_api.py
│   │       ├── shift_api.py
│   │       ├── backup_api.py
│   │       ├── hooks.py
│   │       ├── hooks_logic.py
│   │       ├── setup.py
│   │       ├── setup_wizard_api.py
│   │       ├── sync_assets.py
│   │       ├── website_context.py
│   │       ├── www/              ← Frontend pages (HTML/JS/CSS)
│   │       │   ├── billing.html
│   │       │   ├── sizewise_item.html
│   │       │   ├── sizewise_invoice.html
│   │       │   ├── item_master.html
│   │       │   ├── suppliers.html
│   │       │   ├── configure.html
│   │       │   └── setup_wizard.html
│   │       ├── public/js/        ← ERPNext desk JS overrides
│   │       │   ├── sales_invoice.js
│   │       │   └── purchase_order.js
│   │       ├── translations/
│   │       │   └── en.csv
│   │       └── tests/
│   │           └── test_item_master_api.py
│   └── india_compliance/         ← GST compliance app
├── docs/                         ← VitePress documentation site
├── the docs/                     ← Developer & troubleshooting manuals
├── compose.yaml / pwd.yml        ← Docker Compose orchestration
├── install.ps1 / install.sh      ← One-command installers
├── check.ps1                     ← Health check script
├── sync_assets.py                ← Nginx asset hard-sync utility
└── KNOWLEDGE_BASE.md             ← THIS FILE
```

---

## 4. Documentation Index

### Installation & Operations

| Document | Purpose |
|---|---|
| [README.md](file:///d:/Smriti_Retail_OS/README.md) | Quick install guide, features overview, troubleshooting table |
| [INSTALL.md](file:///d:/Smriti_Retail_OS/INSTALL.md) | Full step-by-step installation walkthrough |
| [TROUBLESHOOTING.md](file:///d:/Smriti_Retail_OS/TROUBLESHOOTING.md) | Comprehensive fix guide for common issues |
| [TROUBLESHOOTING2.md](file:///d:/Smriti_Retail_OS/TROUBLESHOOTING2.md) | Extended troubleshooting (container, MIME, auth) |

### Architecture & Design

| Document | Purpose |
|---|---|
| [ARCHITECTURE_REPORT.md](file:///d:/Smriti_Retail_OS/ARCHITECTURE_REPORT.md) | System architecture, module map, design decisions |
| [SMRITI_ENTERPRISE_READINESS.md](file:///d:/Smriti_Retail_OS/SMRITI_ENTERPRISE_READINESS.md) | Multi-store scalability analysis and gaps |
| [SMRITI_PATCH_ARCHITECTURE.md](file:///d:/Smriti_Retail_OS/SMRITI_PATCH_ARCHITECTURE.md) | Patch strategy and architecture decisions |

### Release & Feature History

| Document | Purpose |
|---|---|
| [RELEASE_NOTES.md](file:///d:/Smriti_Retail_OS/RELEASE_NOTES.md) | Version-by-version changelog (v1.0.0, v1.1.0) |
| [completedlist.md](file:///d:/Smriti_Retail_OS/completedlist.md) | Detailed locked feature register with implementation notes |
| [TASK_COMPLETION_REPORT.md](file:///d:/Smriti_Retail_OS/TASK_COMPLETION_REPORT.md) | Summary task completion evidence |

### Security & Audit

| Document | Purpose |
|---|---|
| [SMRITI_VERIFIED_CRITICALS.md](file:///d:/Smriti_Retail_OS/SMRITI_VERIFIED_CRITICALS.md) | Forensic audit — verified P0/P1 risks with reproduction steps |
| [SMRITI_FINAL_VERIFIED_BLOCKERS.md](file:///d:/Smriti_Retail_OS/SMRITI_FINAL_VERIFIED_BLOCKERS.md) | Final blocker list before production sign-off |
| [SMRITI_FALSE_POSITIVES_AND_UNVERIFIED.md](file:///d:/Smriti_Retail_OS/SMRITI_FALSE_POSITIVES_AND_UNVERIFIED.md) | Audit items confirmed as false positives |
| [SMRITI_GOVERNANCE_AUDIT.md](file:///d:/Smriti_Retail_OS/SMRITI_GOVERNANCE_AUDIT.md) | Governance controls and compliance status |
| [AUDIT_CRITIQUE.md](file:///d:/Smriti_Retail_OS/AUDIT_CRITIQUE.md) | External critique and response |

### Planning & Roadmap

| Document | Purpose |
|---|---|
| [DEVELOPMENT_ROADMAP.md](file:///d:/Smriti_Retail_OS/DEVELOPMENT_ROADMAP.md) | 12-month feature roadmap with ROI matrix |
| [SMRITI_AGENT_TASKS.md](file:///d:/Smriti_Retail_OS/SMRITI_AGENT_TASKS.md) | Task IDs (SEC-01, SEC-02, REL-01, REL-02, CLD-01) with acceptance criteria |
| [SMRITI_PRE_DEPLOYMENT_CHECKLIST.md](file:///d:/Smriti_Retail_OS/SMRITI_PRE_DEPLOYMENT_CHECKLIST.md) | Pre-deployment validation checklist and smoke tests |
| [SMRITI_RELEASE_STRATEGY.md](file:///d:/Smriti_Retail_OS/SMRITI_RELEASE_STRATEGY.md) | Release branching and versioning strategy |
| [SMRITI_ONE_DAY_EXECUTION_PLAN.md](file:///d:/Smriti_Retail_OS/SMRITI_ONE_DAY_EXECUTION_PLAN.md) | Accelerated execution plan |
| [SMRITI_RECOVERY_ARCHITECTURE.md](file:///d:/Smriti_Retail_OS/SMRITI_RECOVERY_ARCHITECTURE.md) | Disaster recovery and backup architecture |

### Walkthroughs (Implementation Logs)

| Document | Date | Topic |
|---|---|---|
| [docs/walkthrough.md](file:///d:/Smriti_Retail_OS/docs/walkthrough.md) | Various | General features walkthrough |
| [docs/walkthrough29-05-26.md](file:///d:/Smriti_Retail_OS/docs/walkthrough29-05-26.md) | 2026-05-29 | Initial deployment fixes |
| [docs/walkthrough29-05-26-sizewise-verification.md](file:///d:/Smriti_Retail_OS/docs/walkthrough29-05-26-sizewise-verification.md) | 2026-05-31 | Pre-import verification & on-the-fly insert |
| [docs/walkthrough-supplier-registry.md](file:///d:/Smriti_Retail_OS/docs/walkthrough-supplier-registry.md) | 2026-06-03 | Supplier Registry implementation |
| [docs/walkthrough-vendor-mapping-itemmaster.md](file:///d:/Smriti_Retail_OS/docs/walkthrough-vendor-mapping-itemmaster.md) | 2026-06-04 | Vendor Code → Supplier linkage in Item Master import |
| [docs/walkthrough-thesmes.md](file:///d:/Smriti_Retail_OS/docs/walkthrough-thesmes.md) | Various | Themes and UI customization |
| [SUPPLIER_LOOKUP_FIX_REPORT.md](file:///d:/Smriti_Retail_OS/SUPPLIER_LOOKUP_FIX_REPORT.md) | 2026-06-04 | Supplier lookup filter fix |
| [SUPPLIER_FILTER_ANALYSIS.md](file:///d:/Smriti_Retail_OS/SUPPLIER_FILTER_ANALYSIS.md) | 2026-06-04 | Analysis of supplier filter issue |
| [SUPPLIER_LOOKUP_DIAGNOSTIC.md](file:///d:/Smriti_Retail_OS/SUPPLIER_LOOKUP_DIAGNOSTIC.md) | 2026-06-04 | Diagnostic trace for supplier lookup |
| [the docs/walkthrough.md](file:///d:/Smriti_Retail_OS/the docs/walkthrough.md) | Various | Developer manual walkthrough |
| [the docs/developer_manual.md](file:///d:/Smriti_Retail_OS/the docs/developer_manual.md) | Various | Developer onboarding guide |

### Branding & Community

| Document | Purpose |
|---|---|
| [BRANDING_POLICY.md](file:///d:/Smriti_Retail_OS/BRANDING_POLICY.md) | Brand identity guidelines |
| [CODE_OF_CONDUCT.md](file:///d:/Smriti_Retail_OS/CODE_OF_CONDUCT.md) | Community code of conduct |
| [CONTRIBUTING.md](file:///d:/Smriti_Retail_OS/CONTRIBUTING.md) | Contribution guide for developers |
| [MAINTAINERS.md](file:///d:/Smriti_Retail_OS/MAINTAINERS.md) | Maintainer team and responsibilities |
| [LICENSE](file:///d:/Smriti_Retail_OS/LICENSE) | MIT License |

---

## 5. Completed & Locked Features

> Full detail available in [completedlist.md](file:///d:/Smriti_Retail_OS/completedlist.md)

| # | Feature | Date | Key Files |
|---|---|---|---|
| 1 | **Sizewise HSN & GST Auto-Detection, Truncation & Validation** | 2026-06-01 | [item_master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/item_master_api.py), [sizewise_item.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/sizewise_item.html) |
| 2 | **Invoice & Article DB Renames + Company Email Fix** | 2026-06-01 | [sizewise_invoice_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/sizewise_invoice_api.py) |
| 3 | **Deep Audit & System Hardening** | 2026-06-01 | [check.ps1](file:///d:/Smriti_Retail_OS/check.ps1), [sizewise_invoice_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/sizewise_invoice_api.py), [en.csv](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/translations/en.csv) |
| 4 | **Store Address Management & Setup Wizard Hardening** | 2026-06-02 | [setup_wizard_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/setup_wizard_api.py), [hooks_logic.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/hooks_logic.py), [configure.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/configure.html) |
| 5 | **Enhanced Supplier Registry (Full ERPNext Field Support)** | 2026-06-03 | [master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/master_api.py), [suppliers.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/suppliers.html) |
| 6 | **Barcode Hardening — Primary + Secondary Architecture** | 2026-06-03 | [barcode_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/barcode_api.py), [item_master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/item_master_api.py) |
| 7 | **Sizewise Invoice — HID Barcode Scanner Support** | 2026-06-03 | [sizewise_invoice_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/sizewise_invoice_api.py), [sizewise_invoice.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/sizewise_invoice.html) |
| 8 | **Item Master Excel Import — Barcode Bug Fixes (×3)** | 2026-06-03 | [item_master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/item_master_api.py), [item_master.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/item_master.html) |
| 9 | **Data Cleaning & HSN Fallback Hardening** | 2026-06-03 | [item_master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/item_master_api.py) |
| 10 | **Supplier Vendor Code Validation (Import + Single Save)** | 2026-06-04 | [item_master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/item_master_api.py), [setup.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/setup.py) |
| 11 | **Supplier Lookup Filter Fix (Individual + Company)** | 2026-06-04 | [purchase_order.js](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/public/js/purchase_order.js) |
| 12 | **Pre-Import Verification Panel (Sizewise Pivot)** | 2026-05-31 | [item_master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/item_master_api.py), [sizewise_item.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/sizewise_item.html) |
| 13 | **Advanced PWA — Offline, Background Sync, IndexedDB, Push Notifications** | 2026-06-04 | [sw.js](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/public/js/sw.js), [smriti_pwa.js](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/public/js/smriti_pwa.js), [smriti_offline_store.js](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/public/js/smriti_offline_store.js), [offline.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/offline.html) |
| 14 | **Warehouse Hardening & Custom Warehouse Override** | 2026-06-04 | [purchase_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/purchase_api.py), [inventory_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/inventory_api.py) |
| 15 | **New Company Creation — "Could not find Row #N: Company" Fix** | 2026-06-05 | [setup_wizard_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/setup_wizard_api.py), [company_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/company_api.py) |
| 16 | **Code Review Fixes — HSN-First GST, Dynamic State, E-Invoice Compliance** | 2026-06-05 | [hooks_logic.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/hooks_logic.py), [billing_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/billing_api.py), [item.js](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/public/js/item.js), [security_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/security_api.py) |
| 17 | **HSN-First GST% Auto-Derivation & Boilerplate Header Cleanup** | 2026-06-05 | [item_master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/item_master_api.py), [item.js](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/public/js/item.js), [smriti_item_master.js](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/smriti_retail_os/page/smriti_item_master/smriti_item_master.js) |
| 18 | **Deep System Review & Architecture Hardening** | 2026-06-05 | [security_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/security_api.py), [hooks_logic.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/hooks_logic.py), [transaction_kernel.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/transaction_kernel.py), [item_master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/item_master_api.py), [reports_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/reports_api.py) |

---

## 6. Open Risk Register

> Full detail: [SMRITI_VERIFIED_CRITICALS.md](file:///d:/Smriti_Retail_OS/SMRITI_VERIFIED_CRITICALS.md)

| Risk ID | Severity | Title | Status | File |
|---|---|---|---|---|
| **P0-01** | 🔴 Critical | Privilege escalation via Store Manager password reset | **OPEN** | [security_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/security_api.py) — Task: SEC-01 |
| **P1-01** | 🟠 High | Manager overrides use primary login password (shoulder-surfing risk) | **OPEN** | [billing_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/billing_api.py) — Task: SEC-02 |
| **P1-02** | 🟠 High | Same insecure PIN logic duplicated in shift close | **OPEN** | [shift_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/shift_api.py) — Task: SEC-02 |
| **P1-03** | 🟠 High | Email backup fails silently when DB backup exceeds 25MB SMTP limit | **OPEN** | [backup_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/backup_api.py) — Task: CLD-01 |
| **P1-04** | 🟠 High | No idempotency in `submit_bill` — double submission risk | **OPEN** | [billing_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/billing_api.py) — Task: REL-02 |
| **P2-01** | 🟡 Medium | `sync_assets.py` uses `shutil.rmtree` — not atomic | **OPEN** | [sync_assets.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/sync_assets.py) — Task: REL-01 |

### Agent Task Blueprint

See [SMRITI_AGENT_TASKS.md](file:///d:/Smriti_Retail_OS/SMRITI_AGENT_TASKS.md) for detailed acceptance criteria for each task:

| Task ID | Priority | Description |
|---|---|---|
| **SEC-01** | P0 | Block Store Manager from resetting System Manager passwords |
| **SEC-02** | P0 | Introduce dedicated `custom_smriti_pin` field; decouple PIN from login password |
| **REL-01** | P1 | Replace `shutil` with `rsync`-based atomic asset sync |
| **REL-02** | P1 | Implement billing idempotency + background `frappe.enqueue` for payment entries |
| **CLD-01** | P2 | Add S3/rclone cloud backup with credential fields in Company Settings |

---

## 7. Development Roadmap Summary

> Full roadmap: [DEVELOPMENT_ROADMAP.md](file:///d:/Smriti_Retail_OS/DEVELOPMENT_ROADMAP.md)

### Phase 1 — Stabilization & Security (Months 1–3)
- ✅ Secure secret management (`.env` + environment vars)
- 🔲 Dedicated hashed PIN field for managers (`custom_smriti_pin`)
- 🔲 Convert `setup.py` DocType definitions to standard Frappe JSON manifests
- 🔲 First wave of API unit tests

### Phase 2 — Performance & Reliability (Months 4–6)
- 🔲 Redis-based caching for POS item/stock lookups
- 🔲 `sync_assets.py` → incremental/`rsync`-based sync
- 🔲 PWA offline mode for billing terminal

### Phase 3 — Enterprise Features & Governance (Months 7–9)
- 🔲 JWT-based auth for standalone billing terminal
- 🔲 Expanded audit trail for all POS manager override events
- 🔲 Multi-currency standardization

### Phase 4 — AI & Innovation (Months 10–12)
- 🔲 AI Inventory Predictor for stock-out alerts
- 🔲 Smart Barcode Resolver (fuzzy search / OCR)
- 🔲 Full Frappe v17 regression testing suite

---

## 8. Operational Runbooks

### Install / Re-Install

**Windows (PowerShell):**
```powershell
git clone https://github.com/erpnbook/smriti-docker.git smriti_retail
cd smriti_retail
PowerShell -ExecutionPolicy Bypass -File .\install.ps1
```

**Linux / macOS:**
```bash
git clone https://github.com/erpnbook/smriti-docker.git smriti_retail
cd smriti_retail && bash install.sh
```

After install → [http://localhost:8080/setup-wizard](http://localhost:8080/setup-wizard)

### Health Check
```powershell
# Windows — verifies all 9 containers are running
.\check.ps1
```

### Update Application
```bash
# 1. Pull latest code
cd apps/smriti_retail_os && git pull origin main && cd ../..

# 2. Migrate DB
docker exec smriti_retail-backend-1 bench --site smriti_retail migrate

# 3. Rebuild assets
docker exec smriti_retail-backend-1 bench build --app smriti_retail_os

# 4. Sync assets to Nginx volume
docker exec smriti_retail-backend-1 bench --site smriti_retail execute smriti_retail_os.sync_assets.sync_assets

# 5. Clear cache
docker exec smriti_retail-backend-1 bench --site smriti_retail clear-cache
```

### Run Test Suite
```bash
docker exec smriti_retail-backend-1 bench --site smriti_retail run-tests --app smriti_retail_os
# Expected: 87/87 OK
```

### Reset Admin Password
```bash
docker exec -it smriti_retail-backend-1 bench --site smriti_retail set-admin-password NewPass
```

### Common Issues & Quick Fixes

| Symptom | Fix |
|---|---|
| Backend keeps restarting | `apps/smriti_retail_os/` empty → re-run `.\install.ps1` |
| `502 Bad Gateway` | `docker restart smriti_retail-frontend-1` |
| Blank/unstyled UI | Run asset sync step above |
| Invalid credentials | Reset admin password command above |
| All containers shown as NOT FOUND in `check.ps1` | Was fixed — script now auto-detects Docker Compose project name |
| `en.csv` translation errors in logs | Was fixed — malformed translation file corrected |
| **`Could not find Row #N: Company: <name>` during new company creation** | **Fixed (v1.2.3)** — `flags.ignore_links = True` added to `Mode of Payment`, `POS Profile`, and `ensure_company_settings` saves. See §12 below. |

Full guide: [TROUBLESHOOTING.md](file:///d:/Smriti_Retail_OS/TROUBLESHOOTING.md)

---

## 12. Known Bugs & Resolutions

### BUG-001 — `Could not find Row #N: Company: <name>` on New Company Creation

**Status:** ✅ Verified Fixed — v1.2.3 (2026-06-05) · All 5 checks passed

**Symptom:**  
When creating a new company through the Setup Wizard, Frappe throws:
```
Could not find Row #2: Company: Test Company Ltd
```
The error appears even when creating a *different* company (e.g. "Verify Test Co") — the name in the error is the *previously deleted* company.

**True Root Cause (two independent triggers):**

| # | Trigger | Caller | Why it fails |
|---|---|---|---|
| 1 | `ERPNext company.py → set_mode_of_payment_account()` | Fires on every `Company.on_update` | Iterates ALL Mode of Payment docs, appends a row for the new company, saves **without `ignore_links`** — Frappe validates ALL rows including stale ones for deleted companies |
| 2 | `india_compliance → delete_gst_settings_for_company()` | Fires on `Company.on_trash` | Saves `GST Settings` doc containing stale rows for deleted companies |

**Root DB cause:** A previously created company (e.g. `Test Company Ltd` from testing) was deleted via `frappe.delete_doc`, but ERPNext and India Compliance **do not clean up child table rows** in `tabMode of Payment Account` and `tabGST Account`. These orphan rows cause Link validation to fail on every subsequent Company save.

**Three-Layer Fix Applied:**

**Layer 1 — Code: Orphan purge in wizard MoP loop** ([setup_wizard_api.py ~L511](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/setup_wizard_api.py))
```python
# Strip any MoP account rows whose Company no longer exists
clean_accounts = [acc for acc in unique_accounts if frappe.db.exists("Company", acc.company)]
mop_doc.accounts = clean_accounts
mop_doc.flags.ignore_links = True   # belt-and-suspenders
mop_doc.save(ignore_permissions=True)
```

**Layer 2 — Code: `ignore_links` in `ensure_company_settings` hook** ([company_api.py ~L357](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/company_api.py))
```python
new_doc.flags.ignore_links = True   # hook fires inside Company.after_insert before outer commit
new_doc.insert(ignore_permissions=True)
```

**Layer 3 — One-time DB cleanup** (run once on affected site)
```sql
-- Delete stale Mode of Payment Account rows for deleted companies
DELETE FROM `tabMode of Payment Account`
WHERE company NOT IN (SELECT name FROM `tabCompany`);

-- Delete stale GST Account rows for deleted companies  
DELETE FROM `tabGST Account`
WHERE company NOT IN (SELECT name FROM `tabCompany`);
```
Scripts: [`scratch/purge_stale_mop.py`](file:///d:/Smriti_Retail_OS/scratch/purge_stale_mop.py) · [`scratch/purge_stale_gst.py`](file:///d:/Smriti_Retail_OS/scratch/purge_stale_gst.py)

**Rows deleted from this site:**
- `tabMode of Payment Account`: 1 row (Cash → Test Company Ltd)
- `tabGST Account`: 4 rows (CGST/SGST/IGST/Cess → Test Company Ltd)

**Verification Result (2026-06-05):**
```
[OK] run_setup_wizard() returned success=True
[OK] Company exists in DB
[OK] SMRITI Company Settings created
[OK] Warehouse created (Main Store - VTC)
[OK] POS Profile created (Standard POS Profile)
RESULT: ALL 5 CHECKS PASSED - BUG-001 FIXED
```

> [!IMPORTANT]
> If this error reappears on a fresh install or after deleting companies, run the two purge scripts above against the site. Always use `delete_company()` in [company_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/company_api.py) instead of raw `frappe.delete_doc("Company", ...)` — it cleans up SMRITI Settings but ERPNext's own MoP/GST rows still need the purge scripts if companies were deleted through the ERPNext desk.

---

## 9. Key API Reference

### Backend Whitelisted Endpoints

| Endpoint | File | Purpose |
|---|---|---|
| `smriti_retail_os.billing_api.submit_bill` | [billing_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/billing_api.py) | Submit POS Sales Invoice |
| `smriti_retail_os.billing_api.validate_manager_override` | [billing_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/billing_api.py) | Validate manager PIN for override actions |
| `smriti_retail_os.item_master_api.import_item_master` | [item_master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/item_master_api.py) | Excel bulk import of items/variants |
| `smriti_retail_os.item_master_api.import_pivot_item_master` | [item_master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/item_master_api.py) | Pivot-matrix style × color × size import |
| `smriti_retail_os.item_master_api.validate_import_rows` | [item_master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/item_master_api.py) | Dry-run validation before import |
| `smriti_retail_os.item_master_api.validate_pivot_values` | [item_master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/item_master_api.py) | Validate categories/colors/sub-cats against DB |
| `smriti_retail_os.sizewise_invoice_api.resolve_barcode` | [sizewise_invoice_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/sizewise_invoice_api.py) | Resolve barcode → article/color/size/MRP |
| `smriti_retail_os.barcode_api.validate_barcode` | [barcode_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/barcode_api.py) | Validate barcode format and uniqueness |
| `smriti_retail_os.master_api.quick_create_supplier` | [master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/master_api.py) | Create supplier with GST address sync |
| `smriti_retail_os.company_api.get_store_address` | [company_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/company_api.py) | Read registered office address from ERPNext |
| `smriti_retail_os.company_api.save_store_address` | [company_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/company_api.py) | Save registered office address to ERPNext |
| `smriti_retail_os.security_api.reset_user_password` | [security_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/security_api.py) | Reset store-level user password (governance-gated) |
| `smriti_retail_os.backup_api.take_backup_now` | [backup_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/backup_api.py) | Trigger manual backup |
| `smriti_retail_os.sizewise_invoice_api.get_admin_session_for_pdf` | [sizewise_invoice_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/sizewise_invoice_api.py) | Retrieve admin session for headless PDF export (System Manager role required) |

### Frontend Pages

| URL | HTML File | Purpose |
|---|---|---|
| `/billing` | [billing.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/billing.html) | POS billing terminal (cashier-locked) |
| `/sizewise_item` | [sizewise_item.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/sizewise_item.html) | Sizewise Item Master CRUD + pivot paste import |
| `/item_master` | [item_master.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/item_master.html) | Excel-format item import page |
| `/sizewise_invoice` | [sizewise_invoice.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/sizewise_invoice.html) | B2B invoice with barcode scanner |
| `/suppliers` | [suppliers.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/suppliers.html) | Supplier Registry |
| `/configure` | [configure.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/configure.html) | Store configuration |
| `/setup-wizard` | [setup_wizard.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/setup_wizard.html) | One-time setup wizard |

---

## 10. Testing & QA

### Automated Test Suite
- **Location**: [tests/](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/tests/)
- **Test Count**: **94/94 passing** (verified as of 2026-06-05)
- **Run Command**:
  ```bash
  docker exec smriti_retail-backend-1 bench --site smriti_retail run-tests --app smriti_retail_os
  ```

### Key Test Files
| File | What It Tests |
|---|---|
| [test_item_master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/tests/test_item_master_api.py) | Item import, vendor code validation, barcode logic |

### Verification Scripts
| Script | Purpose |
|---|---|
| [check.ps1](file:///d:/Smriti_Retail_OS/check.ps1) | Container health check (auto-detects project name) |
| [verify_deep_audit.py](file:///d:/Smriti_Retail_OS/verify_deep_audit.py) | Deep code audit verification |
| [verify_profiles.py](file:///d:/Smriti_Retail_OS/verify_profiles.py) | POS profile verification |
| [test_boot_patch.py](file:///d:/Smriti_Retail_OS/test_boot_patch.py) | Boot patch smoke test |
| [test_patch.py](file:///d:/Smriti_Retail_OS/test_patch.py) | Patch validation test |

---

## 11. Deployment & Infrastructure

### Container Architecture
```
smriti_retail-backend-1     → Frappe/ERPNext app server
smriti_retail-frontend-1    → Nginx (port 8080 exposed)
smriti_retail-websocket-1   → Socket.io for real-time POS
smriti_retail-queue-long-1  → Long-running background jobs
smriti_retail-queue-short-1 → Short background jobs
smriti_retail-scheduler-1   → Cron job scheduler
smriti_retail-db-1          → MariaDB
smriti_retail-redis-queue-1 → Redis (job queue)
smriti_retail-redis-cache-1 → Redis (cache)
```

### Key Config Files
| File | Purpose |
|---|---|
| [compose.yaml](file:///d:/Smriti_Retail_OS/compose.yaml) | Primary Docker Compose config |
| [pwd.yml](file:///d:/Smriti_Retail_OS/pwd.yml) | Full production Docker Compose with all mounts |
| [.env](file:///d:/Smriti_Retail_OS/.env) | Environment variables (DB passwords, site config) |
| [frappe.conf.template](file:///d:/Smriti_Retail_OS/frappe.conf.template) | Nginx/Frappe configuration template |
| [docker-bake.hcl](file:///d:/Smriti_Retail_OS/docker-bake.hcl) | Docker Bake multi-platform build config |

### Asset Management

The `sync_assets.py` utility physically copies compiled JS/CSS bundles from the app directory into the Nginx shared volume, bypassing Docker symlink limitations:

```bash
# Run manually if UI looks unstyled:
docker exec smriti_retail-backend-1 bench --site smriti_retail execute smriti_retail_os.sync_assets.sync_assets
```

### Versions

| Component | Version |
|---|---|
| SMRITI Retail OS | **v1.2.6** (current) |
| Frappe Framework | **v16** |
| ERPNext | **v16** |
| India Compliance | **v16** |
| MariaDB | **10.x** |
| Python | **3.11+** |

---

*This knowledge base is maintained by the SMRITI project team and Antigravity AI Code Assistant.*  
*For issues, open a GitHub issue at [erpnbook/smriti-docker](https://github.com/erpnbook/smriti-docker).*
