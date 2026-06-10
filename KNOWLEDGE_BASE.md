# 📚 SMRITI Retail OS — Knowledge Base

> **Single-source overview.** This document is the entry point to all project documentation, completed features, open risks, architecture decisions, and operational runbooks.  
> **Author:** Jawahar R Mallah (<jawahar.mallah@gmail.com>)  
> **Last Updated:** 2026-06-11 · **Version:** v2.5 (CLOSED)

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
| **Backup Storage Security** | Backup files (`.gz`/`.tar`) are stored in `private/backups` where Nginx blocks direct public HTTP access. Downloads require a valid System Manager/Administrator session. Cloud sync utilizes encrypted TLS tunnels and S3 KMS-based encryption-at-rest. | [backup_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/backup_api.py) |
| **v1.8.2a Protected Config Denylist** | `PROTECTED_CONFIG_PATTERNS` in `security_constants.py` defines glob patterns (e.g. `*site_config*.json`, `*.key`, `*.pem`, `*.p12`) that are filtered out of all backup history listings and intercepted at the `before_request` level in `boot.py`. Any direct `/backups/<protected_file>` download is rejected with `403 PermissionError` and logged to the Activity Log. | [security_constants.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/security_constants.py), [boot.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/boot.py) |
| **v1.8.2a In-Memory Config Export** | `export_site_config()` in `backup_api.py` reads site config, redacts all fields in `SENSITIVE_EXPORT_FIELDS` (replacing values with `"*** REDACTED ***"`), and streams the result as a direct download. No file is ever written to disk. Requires System Manager role + password re-authentication. Guests are rejected before password check. | [backup_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/backup_api.py) |
| **v1.8.2a Fail-Closed Design** | This module follows fail-closed design. Any condition that cannot guarantee security integrity aborts the operation rather than silently degrading. This applies to: Guest session detection, role enforcement, password re-authentication, denylist matching, and audit log writes. | [backup_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/backup_api.py) |
| **Key Recovery (v1.8.3 scope)** | Dual-custodian key recovery is **UNBLOCKED for v1.8.3**. Architecture (post-review 2026-06-10): All Key Recovery UI lives inside the existing `/backup` page under a new **"Backup Security"** section — same Navy sidebar, SMRITI cards, SMRITI modals. **No separate page. No Frappe Form. No List View.** `SMRITI Key Custodian` DocType stores metadata only (email, verified, dates, status, hashed OTP, and 15-minute OTP expiry) — no key fragments. Key fragments (simple midpoint split) are generated in-memory by `key_recovery_service.py` and sent via email (after verifying SMTP configuration). Key rotation uses versioning in `frappe.conf` and filenames (e.g. `*-v[version].smriti.enc`) instead of re-encryption. `verify_custodian_emails()` and `send_recovery_key()` stubs in `backup_api.py` will delegate to `key_recovery_service.py`. Feature flag `enable_backup_encryption` controls rollout. | [implementation_plan.md](file:///C:/Users/netma/.gemini/antigravity-ide/brain/26cd6eeb-7016-4a5b-8bfc-ebd3e0c01e3d/implementation_plan.md) |
| **v1.8.2a Audit Closure Artifacts** | Three governance-quality artifacts captured on 2026-06-10: (1) Exported JSON showing `db_password → *** REDACTED ***`; (2) `ls private/backups/ \| grep site_config` → exit 1, zero results, confirming no file is written to disk during export; (3) `setup_activity_log_options()` idempotency verified — calling twice produces exactly one entry each for `"Blocked Download Attempt"` and `"Config Exported"`. | [walkthrough.md](file:///C:/Users/netma/.gemini/antigravity-ide/brain/26cd6eeb-7016-4a5b-8bfc-ebd3e0c01e3d/walkthrough.md) |
| **Label Studio Realtime Updates (V2.2)** | Switched printer queue dashboard updates from polling to namespaced Socket.io events (`smriti.barcode.print_status`). Restricts event delivery to `user=doc.requested_by` to prevent cross-user leakage in multi-cashier environments. Captures operator IP and user agent in `SMRITI Print Job` for auditing. | [barcode_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/barcode_api.py), [barcode.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/barcode.html) |
| **Print Template Versioning & Lock (V2.3)** | Created separate parent DocType `SMRITI Print Template Version` to store history snapshots. Computes SHA-256 checksums on template contents + mappings + layouts on save, and enforces optimistic locking (`expected_checksum`) during version restore to prevent concurrent overwrite conflicts. | [smriti_print_template.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/smriti_retail_os/doctype/smriti_print_template/smriti_print_template.py), [barcode_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/barcode_api.py) |
| **Visual Designer & DPI Portability (V2.4a/b)** | Added tab-navigation layout editor. Stores elements as JSON coordinates (mm-based, 1mm = 8px on screen). Converts mm coordinates to ZPL/TSPL dots at compile time (`dots = mm * dpi / 25.4`). Handles versioned metadata wrappers (`layout_version: 1`, `compiler_version: 1`) with backward compatibility for unwrapped layouts. Blocks canvas editing for legacy/raw templates. Supports client-side undo/redo (20 states). | [barcode.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/barcode.html) |
| **Pre-Print Validation Engine & SVG Preview (V2.5)** | Replaced div preview with high-fidelity vector SVG preview. Simulates DPI grid and renders mock barcodes/QR codes/images. Added diagnostics validation (blocking errors for absolute boundary breaches, print-safe margin incursions on barcodes/QRs, and non-decorative element collisions; warnings for text overflow and text/image margin incursions). | [barcode_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/barcode_api.py), [barcode.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/barcode.html) |

### v1.8.3 Security Audit Event Matrix

| Event | Operation | Details |
|---|---|---|
| **Encryption Enabled** | `"Backup Encryption Enabled"` | User who enabled + active key fingerprint |
| **Encryption Disabled** | `"Backup Encryption Disabled"` | User who disabled |
| **Key Rotated** | `"Backup Key Rotated"` | User + old fingerprint + new fingerprint |
| **Custodian Verified** | `"Custodian Verified"` | Custodian email + verification timestamp |
| **Recovery Fragments Sent** | `"Recovery Fragments Sent"` | Masked recipient emails |
| **GPG Missing** | `"GPG Executable Missing"` | Site name + timestamp (Fail Closed trigger) |
| **Encrypted Restore** | `"Encrypted Backup Restored"` | Plaintext filename + user + key version |

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
| 38 | **Global Branding Locks & Branded Error Overrides (v1.8.0)** | 2026-06-10 | `test_branding_integrity.py`, `hooks.py`, `404.html`, `403.html` |
| 39 | **Secure Backup Download Routing Fix (v1.8.1)** | 2026-06-10 | `backup.html`, `platform_center.html`, `smriti_backup.js` |
| 40 | **Backup Security Design documentation (v1.8.2)** | 2026-06-10 | `KNOWLEDGE_BASE.md` |
| 41 | **P0 Security Hotfix — Protected Config Denylist, Export Redaction, Boot Guards (v1.8.2a)** | 2026-06-10 | `security_constants.py`, `backup_api.py`, `platform_api.py`, `boot.py`, `test_backup_security_hotfix.py` |
| 42 | **v1.8.2a Governance Closure — Audit Artifacts Archived** | 2026-06-10 | `walkthrough.md` — exported JSON redaction sample, `private/backups` listing (zero `site_config` results), Activity Log migration idempotency PASS |
| 43 | **v1.8.3 Backup Encryption — Implementation Plan Created** | 2026-06-10 | `implementation_plan.md` — AES-256-GCM encryption service, dual-custodian key recovery, SMTP verification, `/smriti-key-recovery` SMRITI page, tests 9–12 |
| 44 | **SMRITI Label Studio V2.2/V2.3/V2.4a/b (Sockets, Version History, Designer & Metadata Wrappers)** | 2026-06-10 | `barcode_api.py`, `smriti_print_template.py`, `barcode.html`, `test_barcode_api.py` |
| 45 | **SMRITI Label Studio V2.5 (Preview & Pre-Print Validation Engine)** | 2026-06-11 | `barcode_api.py`, `test_barcode_api.py`, `barcode.html` |

---

## 6. Open Risk Register

| Risk ID | Severity | Title | Status | File |
|---|---|---|---|---|
| **P0-01** | 🔴 Critical | Privilege escalation via Store Manager password reset | ✅ **FIXED** | `security_api.py` |
| **P0-02** | 🔴 Critical | Backup files unencrypted at rest — `site_config` exposure risk | 🔵 **IN PLAN (v1.8.3)** | `gpg_service.py` (new) |
| **P1-01** | 🟠 High | Manager overrides use primary login password (shoulder-surfing risk) | ✅ **FIXED** | `billing_api.py`, `shift_api.py` |
| **P1-03** | 🟠 High | Email backup fails silently when DB backup exceeds 25MB SMTP limit | **OPEN** | `backup_api.py` |
| **P2-01** | 🟡 Medium | `sync_assets.py` uses `shutil.rmtree` — not atomic | **OPEN** | `sync_assets.py` |

---

## 7. Development Roadmap Summary

### Phase 1 — Footwear Pilot Deployment (Current)
- ✅ Deploy to Client #1 (Footwear Retailer)
- ✅ Modules Active: Billing, Inventory, Masters, Loyalty, Reports, Day End
- ✅ Hidden: PSV, PSA, Distributor modules (via `Business Type` config)
- ✅ **v1.8.2a Security Hardening CLOSED** — Protected config denylist, export redaction, boot guards, 8 automated tests, all governance artifacts archived.
- 🔵 **v1.8.3 Backup Encryption** — UNBLOCKED. GPG AES-256 symmetric encryption, versioned key rotation, dual-custodian recovery (simple midpoint split), SMTP verification, tests 9–13.
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
| `smriti_retail_os.backup_api.get_backup_history` | `backup_api.py` | Returns backup archive list — protected files filtered via `PROTECTED_CONFIG_PATTERNS` |
| `smriti_retail_os.backup_api.export_site_config` | `backup_api.py` | System Manager + password re-auth required. Streams redacted config JSON in-memory. No disk write. |
| `smriti_retail_os.backup_api.log_audit_event` | `backup_api.py` | Internal helper — writes to Frappe Activity Log. Never raises on failure. |
| `smriti_retail_os.backup_api.get_encryption_status` *(v1.8.3)* | `backup_api.py` | Returns `{key_present, gpg_available, custodians_set, encryption_enabled}` for recovery dashboard |
| `smriti_retail_os.barcode_api.get_print_template_versions` | `barcode_api.py` | Returns linked version history snapshots for a template |
| `smriti_retail_os.barcode_api.restore_print_template_version` | `barcode_api.py` | Restores template version after validating expected_checksum optimistic lock |
| `smriti_retail_os.barcode_api.enqueue_print_job` | `barcode_api.py` | Enqueues raw printer job, captures user audit details, and publishes Socket.io status updates |
| `smriti_retail_os.barcode_api.validate_layout_diagnostics` | `barcode_api.py` | Validates print template layout and returns diagnostics for margin incursion, collision detection, and text overflow |

*(Note: API calls must comply with Service-First architecture defined in GEMINI.md)*

---

## 10. Testing & QA

### Automated Test Suite
- **Run Command**:
  ```bash
  docker exec smriti_retail-backend-1 bench --site smriti_retail run-tests --app smriti_retail_os
  ```
- **Test Coverage**: 174 passing tests (142 pre-v1.8.2a + 8 v1.8.2a security tests + 7 v1.8.3 encryption/recovery tests + 17 barcode api, async queue, and validation engine tests) covering core workflows, report engines, PSV Shadow Ledger, brand integrity, and backup/printing security controls.
- **Barcode & Studio Test Suite**: `smriti_retail_os.tests.test_barcode_api` — 25 tests covering async print job enqueuing/processing, Socket.io user-scoped targeting, version snapshotting, DPI portable coordinate translation, legacy guards, margin checking, text overflow, element collisions, and wrapped/unwrapped layout compatibility.
- **Security Test Module**: `smriti_retail_os.tests.test_backup_security_hotfix` — 15 tests for config denylist, 403 enforcement, Activity Log, export redaction, restore cleanup, GPG encryption/decryption, OTP expiration, key splitting, GPG fail-closed behavior, and sidecar verification.

### Cryptographic Brand Enforcement
To prevent unauthorized modification or accidental deletion of corporate branding elements and routing compliance rules, a cryptographic validation suite is integrated into the automated tests (`test_branding_integrity.py`). This suite checks line-ending-normalized SHA-256 hashes of critical files:
- **Global SVG Logos**: `public/images/smriti_logo.svg`, `public/images/logo.svg`, `public/logo.svg`
- **Login Background Wallpaper**: `public/images/login_wallpaper.svg`
- **Login and Error Pages**: `www/smriti-login.html`, `www/404.html`, `www/403.html`, `www/smriti-404.html`, `www/smriti-403.html`
- **Route Integrity**: Verifies that custom routing rules for `/login` -> `smriti-login`, `/404` -> `smriti-404`, and `/403` -> `smriti-403` are registered in `hooks.py`.

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
| SMRITI Retail OS | **v1.8.2a** (closed ✅) → **v1.8.3** (planning 🔵) |
| Frappe Framework | **v16** |
| ERPNext | **v16** |
| India Compliance | **v16** |

### v1.8.3 New Files (Planned)
| File | Type | Purpose |
|---|---|---|
| `gpg_service.py` | New service | GPG symmetric encrypt/decrypt using stdin. Key versioning. No Frappe dependency — fully unit-testable. |
| `key_recovery_service.py` | New service | OTP generation (15-min expiry), custodian verification, key fragment dispatch (simple midpoint split) via `frappe.sendmail()`. |
| `SMRITI Key Custodian` DocType | New DocType | Metadata only: email, verified, dates, status, otp_hash, otp_expiry. No key fragments stored. No Frappe UI exposed. |

**UI lives in existing SMRITI pages (no new routes):**
| Page | Change | Description |
|---|---|---|
| `/backup` | Extended | New "Backup Security" section with Encryption Status card + Key Custodians card + SMRITI modals |
| `/platform-center` | Extended | Encryption status widget + custodian count badge |

> [!IMPORTANT]
> `/app/smriti-key-custodian`, Frappe List View, Frappe Form View, and Frappe Workspace are **never exposed**. All custodian management happens through SMRITI cards and modals inside `/backup`.

### Key Version Retention Policy

> [!IMPORTANT]
> **Key Version Retention Policy**: Encryption key versions must not be removed until all backups encrypted using that version have expired according to the configured backup retention policy.
>
> **Example**:
> - Retention Period = 90 days
> - v1 key may only be retired after all v1 backups have been deleted and verified absent.

---
*This knowledge base is maintained by **Jawahar R Mallah** and the SMRITI project team. For issues, open a GitHub issue at [erpnbook/smriti-docker](https://github.com/erpnbook/smriti-docker).*