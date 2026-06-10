# 📚 SMRITI Retail OS — Knowledge Base

> **Single-source overview.** This document is the entry point to all project documentation, completed features, open risks, architecture decisions, and operational runbooks.  
> **Last Updated:** 2026-06-10 · **Version:** v1.7.0

> [!TIP]
> Keep this document updated after any development session to keep the knowledge base current.

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

**SMRITI Retail OS** is a premium retail experience layer built on top of **Frappe v16** and **ERPNext v16**. It acts as a _Sophisticated Experience Layer_ (SEL) — transforming the complex ERPNext UI into a cashier-friendly, India GST-compliant POS and merchandising platform tailored for multi-industry businesses (Footwear, FMCG, Garments, etc.).

### Core Value Proposition

| Layer | Description |
|---|---|
| **POS Billing Terminal** | High-performance, role-locked cashier interface with barcode scanning, hold/recall, manager overrides |
| **Sizewise Item Master** | Pivot-grid Excel import for style × size × color variant management |
| **SMRITI Pure Retail Mode** | Hides ERPNext desk complexity from cashiers while preserving full ERPNext for admins |
| **India GST Compliance** | Integrated with `india_compliance` for HSN auto-detection, GSTIN validation, and tax templates |
| **Supplier Registry** | Complete vendor management with GST address syncing and Vendor Code validation |
| **B2B Invoice (Sizewise)** | Pivot-grid B2B invoice creation with HID barcode scanner support |
| **PSV-Prime Engine** | **Flagship Module**: Business-Type Activated Core Extension for Party Stock Visibility (PSV). Reclassified from add-on to core industry extension. | [PSV_PRIME_MANUAL.md](C:/Users/netma/.gemini/tmp/smriti-retail-os/memory/PSV_PRIME_MANUAL.md) |

---

## 2. Stack & Architecture

```
┌───────────────────────────────────────────────────────────────┐
│  SMRITI Retail OS  (Custom Frappe App — smriti_retail_os)     │
│  ┌────────────┐  ┌───────────────┐  ┌──────────────────────┐  │
│  │ billing_api│  │item_master_api│  │ psv_ledger_service   │  │
│  │ shift_api  │  │barcode_api    │  │ psv_upload_service   │  │
│  │ security_api│  │ company_api  │  │ psv_analysis_service │  │
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
| **Architecture Directive** | Locked `GEMINI.md` mandating ERPNext as the System of Record and SMRITI as the Experience Layer. Enforces Service-First design and forbids raw DB writes from UI. | [GEMINI.md](file:///d:/Smriti_Retail_OS/GEMINI.md) |
| **Industry Configuration Layer** | Multi-industry support via `custom_business_type` setting. Dynamically toggles features (e.g., hides PSV for Footwear, enables for FMCG) to maintain a single core codebase. | [company_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/company_api.py), [smriti_sidebar_standalone.js](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/public/js/smriti_sidebar_standalone.js) |
| **PSV 3-Layer Sub-Ledger** | Robust 3-layer architecture: Layer 1 (Customer custom fields), Layer 2 (PSV Transaction Engine), Layer 3 (High-speed PSV Balance Table). | [psv_ledger_service.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/psv_ledger_service.py) |
| **HSN-First GST Architecture** | `gst_hsn_code` is the primary source of truth for GST %. `custom_gst_percentage` is auto-derived via the lookup chain. | [hooks_logic.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/hooks_logic.py) — `get_gst_rate_from_hsn()` |
| **Dynamic State Fallback** | Address state resolution reads `Company.state` instead of hardcoded strings — ensures correct CGST/SGST splits. | [hooks_logic.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/hooks_logic.py) — `_get_company_state_fallback()` |
| **Physical Asset Sync** | Unlinks symlinks and hard-copies compiled bundles to Nginx shared volume. | [sync_assets.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/sync_assets.py) |
| **ERPNext-First Data** | Company/Address/Supplier data lives in standard ERPNext DocTypes; SMRITI reads/writes through standard APIs. | [company_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/company_api.py) |
| **Role-Based Routing** | Cashiers hit `/billing`; System Managers see unaltered ERPNext desk. | [hooks.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/hooks.py) |
| **Metadata-Driven Reporting Engine** | `SMRITIReportEngine` uses `SMRITI Report Template` DocType + dynamic SQL builder with MD5 caching + Redis TTL. | [reports_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/reports_api.py) |
| **Hashed POS Manager PIN Override** | Store manager override PINs are stored securely in `custom_smriti_pin` using `update_password` hashing, rather than raw text or primary passwords, avoiding shoulder-surfing risks. | [test_billing_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/tests/test_billing_api.py) |
| **Stock Reconciliation Fields** | ERPNext maps the difference account to `expense_account` (labeled "Difference Account" in UI). Specifying `difference_account` is ignored, falling back to P&L defaults and causing opening entry balance sheet errors. | [inventory_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/inventory_api.py) |
| **Negative Balance Exception Logs** | Invoices/dispatches cancellation reversing shadow ledger entries must log a `SMRITI PSV Exception Record` and update status if it results in negative stock balances. | [smriti_psv_transaction.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/smriti_retail_os/doctype/smriti_psv_transaction/smriti_psv_transaction.py) |

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
│   │       ├── psv_service.py          ← Universal Transaction Engine
│   │       ├── reports_api.py          ← SMRITIReportEngine + 20 reports
│   │       ├── hooks.py
│   │       ├── setup.py                ← Seeds DocTypes, custom fields
│   │       ├── www/                    ← Frontend pages (HTML/JS/CSS)
│   │       ├── public/js/              ← Desk overrides & Standalone UI logic
│   │       └── tests/                  ← Test suites
│   └── india_compliance/               ← GST compliance app
├── docs/                               ← VitePress documentation site
├── compose.yaml / pwd.yml              ← Docker Compose orchestration
├── install.ps1 / install.sh            ← Installers
├── GEMINI.md                           ← Locked Architecture Directive
└── KNOWLEDGE_BASE.md                   ← THIS FILE
```

---

## 4. Documentation Index

### Installation & Operations
* [README.md](file:///d:/Smriti_Retail_OS/README.md) - Quick install guide
* [INSTALL.md](file:///d:/Smriti_Retail_OS/INSTALL.md) - Full walkthrough
* [TROUBLESHOOTING.md](file:///d:/Smriti_Retail_OS/TROUBLESHOOTING.md) - Fix guide

### Architecture & Audit
* [GEMINI.md](file:///d:/Smriti_Retail_OS/GEMINI.md) - Locked Architecture Directives
* [SYSTEM_INVENTORY.md](file:///d:/Smriti_Retail_OS/SYSTEM_INVENTORY.md) - Complete system asset map
* [ARCHITECTURE_COMPLIANCE_REPORT.md](file:///d:/Smriti_Retail_OS/ARCHITECTURE_COMPLIANCE_REPORT.md) - Verification of ERPNext boundaries
* [INTEGRATION_AUDIT.md](file:///d:/Smriti_Retail_OS/INTEGRATION_AUDIT.md) - Cross-module pipeline verification
* [PRODUCTION_READINESS.md](file:///d:/Smriti_Retail_OS/PRODUCTION_READINESS.md) - Enterprise safety standards assessment
* [PERFORMANCE_REPORT.md](file:///d:/Smriti_Retail_OS/PERFORMANCE_REPORT.md) - Query/N+1 optimization audit
* [CLEANUP_REPORT.md](file:///d:/Smriti_Retail_OS/CLEANUP_REPORT.md) - Dead code and refactoring log

---

## 5. Completed & Locked Features

| # | Feature | Date | Key Files |
|---|---|---|---|
| 25 | **SMRITI Reporting Framework** | 2026-06-07 | `reports_api.py`, `reports.html` |
| 26 | **Accounting Analytics Extension** | 2026-06-07 | `reports_api.py`, `setup.py` |
| 27 | **P0/P1 Critical Bug Fix Session** | 2026-06-07 | Various APIs |
| 28 | **POS Return Invoice & Purchase Return** | 2026-06-07 | `billing_api.py`, `purchase_api.py` |
| 29 | **UI/UX Deep Audit & Streamlining** | 2026-06-07 | `reports.html`, `AUDIT_CRITIQUE.md` |
| 30 | **SMRITI Party Stock Visibility (PSV) Hardening** | 2026-06-08 | `psv_service.py`, `test_psv.py` |
| 31 | **PSV Production Hardening v1.2** | 2026-06-09 | `psv_service.py`, `psv_reorder_report.py` |
| 32 | **PSV Phase 3: Reporting & Wizard (v1.4)** | 2026-06-09 | `opening_balance.py`, `psv_party_stock_balance.py` |
| 33 | **PSV 3-Layer Sub-Ledger Engine** | 2026-06-09 | `smriti_psv_transaction.py`, `psv_service.py` |
| 34 | **Industry Config Layer (Multi-Business Type)** | 2026-06-09 | `company_api.py`, `smriti_sidebar_standalone.js` |
| 35 | **Architecture & Production Audit (5-Phase)** | 2026-06-09 | `ARCHITECTURE_COMPLIANCE_REPORT.md` |
| 36 | **Test Suite Hardening & Core Alignments (v1.6.1)** | 2026-06-09 | test_billing_api.py, inventory_api.py, smriti_psv_transaction.py |
| 37 | **Setup Wizard Improvements & Compliant Routing (v1.7.0)** | 2026-06-10 | `setup_wizard_api.py`, `setup_wizard.html` |

---

## 6. Open Risk Register

| Risk ID | Severity | Title | Status | File |
|---|---|---|---|---|
| **P0-01** | 🔴 Critical | Privilege escalation via Store Manager password reset | ✅ **FIXED** | `security_api.py` |
| **P1-01** | 🟠 High | Manager overrides use primary login password (shoulder-surfing risk) | ✅ **FIXED** | `billing_api.py`, `shift_api.py` |
| **P1-03** | 🟠 High | Email backup fails silently when DB backup exceeds 25MB SMTP limit | **OPEN** | `backup_api.py` |
| **P2-01** | 🟡 Medium | `sync_assets.py` uses `shutil.rmtree` — not atomic | **OPEN** | `sync_assets.py` |

---

## 7. Development Roadmap Summary

### Phase 1 — Footwear Pilot Deployment (Current)
- ✅ Deploy to Client #1 (Footwear Retailer)
- ✅ Modules Active: Billing, Inventory, Masters, Loyalty, Reports, Day End
- ✅ Hidden: PSV, PSA, Distributor modules (via `Business Type` config)
- **Goal:** Observe real-world usage, stabilize core ERP workflows, fix bugs based on actual retail feedback. No new features.

### Phase 2 — FMCG Pilot Expansion
- 🔲 Deploy to Client #2 (FMCG Distributor) post-Phase 1 stabilization
- 🔲 Activate: PSA, PSV, Sales Uploads, Physical Audits, Reorder Engine
- 🔲 Build PSV Mobile Audit UI & Replenishment Queue

### Phase 3 — Enterprise Features
- 🔲 Dedicated hashed PIN field for managers (`custom_smriti_pin`)
- 🔲 PWA offline mode expansion for standalone billing
- 🔲 AI Inventory Predictor / Smart Barcode Resolver

---

## 8. Operational Runbooks

### Install / Re-Install
**Windows (PowerShell):**
```powershell
git clone https://github.com/erpnbook/smriti-docker.git smriti_retail
cd smriti_retail
PowerShell -ExecutionPolicy Bypass -File .\install.ps1
```

### Health Check
```powershell
.\check.ps1
```

### Update Application
```bash
cd apps/smriti_retail_os && git pull origin main && cd ../..
docker exec smriti_retail-backend-1 bench --site smriti_retail migrate
docker exec smriti_retail-backend-1 bench build --app smriti_retail_os
docker exec smriti_retail-backend-1 bench --site smriti_retail execute smriti_retail_os.sync_assets.sync_assets
docker exec smriti_retail-backend-1 bench --site smriti_retail clear-cache
```

---

## 9. Key API Reference

### Backend Whitelisted Endpoints (Service Layer)

| Endpoint | File | Purpose |
|---|---|---|
| `smriti_retail_os.company_api.get_business_type` | `company_api.py` | Resolves current Industry Type (e.g. Footwear vs FMCG) |
| `smriti_retail_os.psv_service.create_psv_transaction` | `psv_service.py` | Universal Engine for all PSV stock movements |
| `smriti_retail_os.billing_api.submit_bill` | `billing_api.py` | Submit POS Sales Invoice |
| `smriti_retail_os.item_master_api.import_pivot_item_master` | `item_master_api.py` | Pivot-matrix style × color × size import |
| `smriti_retail_os.barcode_api.validate_barcode` | `barcode_api.py` | Validate barcode format and uniqueness |
| `smriti_retail_os.inventory_api.reset_db` | `inventory_api.py` | **Admin Only** - Hard wipe of transactions |

*(Note: API calls must comply with Service-First architecture defined in GEMINI.md)*

---

## 10. Testing & QA

### Automated Test Suite
- **Run Command**:
  ```bash
  docker exec smriti_retail-backend-1 bench --site smriti_retail run-tests --app smriti_retail_os
  ```
- **Test Coverage**: 136 passing tests covering core workflows, report engines, and the PSV Shadow Ledger.

---

## 11. Deployment & Infrastructure

### Container Architecture
```
smriti_retail-backend-1     → Frappe/ERPNext app server
smriti_retail-frontend-1    → Nginx (Asset routing)
smriti_retail-websocket-1   → Socket.io for real-time POS
smriti_retail-queue-*       → Background job processing
smriti_retail-db-1          → MariaDB
smriti_retail-redis-*       → Caching & Queues
```

### Versions
| Component | Version |
|---|---|
| SMRITI Retail OS | **v1.7.0** (current) |
| Frappe Framework | **v16** |
| ERPNext | **v16** |
| India Compliance | **v16** |

---
*This knowledge base is maintained by the SMRITI project team. For issues, open a GitHub issue at [erpnbook/smriti-docker](https://github.com/erpnbook/smriti-docker).*