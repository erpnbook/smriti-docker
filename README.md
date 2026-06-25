# SMRITI Retail OS™ — Workspace

<div align="center">

  <img src="apps/smriti_retail_os/smriti_retail_os/public/images/logo.svg" alt="SMRITI Retail OS" width="120" />

  ### Retail Intelligence Platform — Workspace Repository

  [![Version](https://img.shields.io/badge/SMRITI-v1.2.10-1A2B5C?style=for-the-badge)](https://github.com/erpnbook/smriti)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
  [![ERPNext: v16](https://img.shields.io/badge/ERPNext-v16-2563EB?style=for-the-badge)](https://github.com/frappe/erpnext)
  [![Docs: 211 entries](https://img.shields.io/badge/Docs-211_Entries-22c55e?style=for-the-badge)](#documentation)

  **Developed by AITDL – AI Technology & Development Lab**
  Powered by ERPNext® & Frappe® Framework

</div>

---

> **Author**: Jawahar R. Mallah — Founder & Chief Architect, AITDL
> **Experience**: 20+ years in Retail Technology, Distribution Systems, POS Solutions, ERP Implementations & Enterprise Application Design
> *"Always decision-ready."*

---

## 1. Product Identity

| Field | Value |
|---|---|
| **Official Name** | SMRITI Retail OS™ |
| **Developer** | AITDL – AI Technology & Development Lab |
| **Author** | Jawahar R. Mallah, Founder & Chief Architect |
| **Current Version** | `v1.2.10` |
| **License** | MIT — Free for commercial use |
| **Copyright** | © 2026 AITDL NETWORK & ERPNbook.com. All Rights Reserved. |
| **Trademark Policy** | Use "SMRITI Retail OS™ powered by ERPNext®". Never imply co-branding with ERPNext. |
| **Domain Policy** | Partner domains must not contain "erpnext" or "frappe" |

### Mandatory Attribution Notice

All public-facing interfaces and manuals must display:

> **SMRITI Retail OS™**
> Developed by AITDL
> Powered by ERPNext® & Frappe® Framework

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   SMRITI Retail OS™                         │
│  UI Layer  │  API Layer  │  Service Layer  │  Repository   │
├─────────────────────────────────────────────────────────────┤
│                   Frappe Framework v16                      │
│  ORM  │  REST API  │  Auth  │  Boot Session  │  Hooks      │
├─────────────────────────────────────────────────────────────┤
│                     ERPNext v16                             │
│  System of Record: Accounting, Inventory, POS, Compliance  │
├─────────────────────────────────────────────────────────────┤
│                  India Compliance v16                       │
│  GST  │  e-Invoice  │  e-Waybill  │  GSTR Reports          │
└─────────────────────────────────────────────────────────────┘
```

### ERPNext Responsibilities (System of Record)
- Accounting / General Ledger / GST / Tax Engine
- Sales Invoice / Purchase Invoice
- Stock Ledger / Inventory Valuation
- Warehouses / Companies / Customers / Suppliers
- Users / Roles / Permissions / Audit Trails

### SMRITI Responsibilities (Experience & Intelligence Layer)
- UI / UX / Retail Workflows / Dashboard Layer
- POS Experience / Store Operations
- Reporting Experience / Business Analytics
- PSV (Party Stock Visibility) / PSA
- Reorder Intelligence / Exception Management
- Channel Governance Engine (CGE)
- Formula Registry / Explain Engine
- Trial CRM / Platform Administration
- Mobile Experiences / PWA

---

## 3. Core Subsystems

| Subsystem | Abbreviation | Description |
|---|---|---|
| Predictive Distribution Twin | PDT | Real-time stock coverage analytics, velocity tracking, safety stock alerts |
| Channel Governance Engine | CGE | Validation rules, price list resolution, exception handling across channels |
| Party Stock Visibility | PSV | Shadow ledger for distributor-held channel stock (read-only ERPNext) |
| Party Stock Accounts | PSA | Financial view of PSV transactions |
| SMRITI Formula Registry | — | Central registry for all computed retail KPIs |
| SMRITI Explain Engine | — | ⓘ Explain modals on every dashboard metric |
| Clienteling | SFC | Customer relationship intelligence |
| Store Floor Management | SFM | Store operations and attribution |

---

## 4. Architecture Constitution — Golden Rules

The following rules are LOCKED. They apply to all developers, contributors, and AI agents.

| # | Rule | Status |
|---|---|---|
| 1 | Do NOT replace the architecture — extend only | 🔒 LOCKED |
| 2 | Service-First Design: UI → API → Service → DB | 🔒 LOCKED |
| 3 | ERPNext is the System of Record for inventory | 🔒 LOCKED |
| 4 | Tally is the System of Record for financial accounting | 🔒 LOCKED |
| 5 | Every business concept has exactly one owner | 🔒 LOCKED |
| 6 | PSV reads ERPNext masters; never modifies SLE or GL | 🔒 LOCKED |
| 7 | No shadow databases — extend existing masters | 🔒 LOCKED |
| 8 | Pricing is a separate domain — inventory never holds prices | 🔒 LOCKED |
| 9 | Business actions require human approval; analytics may be automatic | 🔒 LOCKED |
| 10 | Every critical action must be auditable (User, Time, Before, After, Reason) | 🔒 LOCKED |
| 11 | Future features must be hidden behind feature flags until activated | 🔒 LOCKED |
| 12 | Backward compatibility must be preserved | 🔒 LOCKED |
| 13 | Governance Gate: Review → Approval → Implementation → Verification | 🔒 LOCKED |
| 14 | No unrelated new projects without governance approval | 🔒 LOCKED |
| 15 | Explainability-First: Every metric must have ⓘ Explain documentation | 🔒 LOCKED |

---

## 5. SMRITI-First UI Policy (Rule 7 — LOCKED)

> **Every new page, module, form, report, or UI component MUST be a dedicated SMRITI standalone page. Frappe Desk (/desk, /app) must NEVER be exposed to end users.**

### What Is FORBIDDEN

| ❌ Wrong | ✅ Correct |
|---|---|
| Opens `/desk#Form/Sales Invoice/new` | Opens `/billing` (SMRITI page) |
| Opens `/app/sales-invoice` | Opens SMRITI modal/form |
| `frappe.new_doc("Sales Invoice")` from UI | `smriti_api.create_invoice()` via `frappe.call()` |

### Coming Soon Policy

Never expose raw Frappe UI as a workaround:

```
/smriti-coming-soon?feature=Purchase+Orders&progress=60&eta=Q3+2026
```

### Routing Standard (Frappe v16+)

```javascript
// CORRECT
frappe.set_route("stock-center");
window.location.href = "/app/stock-center";

// FORBIDDEN
window.location.href = "/page/stock-center";
window.location.href = "/desk/page/stock-center";
```

---

## 6. Documentation

SMRITI Retail OS maintains a governed documentation library of **211+ registered documents**.

### Documentation Structure

```
docs/
├── DOCUMENTATION_INDEX.md          ← Master registry (211 entries)
├── DOCUMENTATION_CONSTITUTION.md   ← Governance rules
├── DOCUMENTATION_STYLE_GUIDE.md    ← Formatting standards
│
├── 01-product/    ← Product overviews, executive summaries
├── 02-user-guide/ ← Step-by-step user guides
├── 03-admin-guide/← Setup and configuration guides
├── 04-operations/ ← Runbooks, SOPs
├── 05-developer/  ← Architecture, implementation guides
├── 06-api/        ← API endpoint references
├── 07-kb/         ← Troubleshooting, FAQ
├── 08-governance/ ← Policies, BRDs, constitution
└── reports/       ← Health audits, compliance reports
```

### POS Profile Documentation Set (Sprint 3C)

| ID | Document | Category |
|---|---|---|
| PROD-012 | [POS Profile Overview](./docs/01-product/pos_profile_overview.md) | Product |
| USER-030 | [POS Profile Usage Guide](./docs/02-user-guide/pos_profile_usage.md) | User Guide |
| ADMIN-009 | [POS Profile Setup Guide](./docs/03-admin-guide/pos_profile_setup.md) | Admin |
| DEV-071 | [POS Profile Developer Reference](./docs/05-developer/pos_profile_developer.md) | Developer |
| API-002 | [POS Profile API Reference](./docs/06-api/pos_profile_api.md) | API |
| KB-031 | [POS Profile Troubleshooting](./docs/07-kb/pos_profile_troubleshooting.md) | KB |

### Documentation Governance

Every document must include YAML metadata:

```yaml
---
id: "<CATEGORY-NNN>"
title: "<Title>"
category: "<Category>"
status: "Published"
version: "<X.Y.Z>"
created: "<YYYY-MM-DD>"
author: "Jawahar R. Mallah"
---
```

**Health Audit**: `docs/reports/documentation_health_report.md`
**Last Audit**: PASS — 0 blockers, 92.76% compliance

---

## 7. Workspace Links

### Core Reference Docs

| Document | Purpose |
|---|---|
| [INSTALL.md](./INSTALL.md) | Environment setup, 5-step onboarding wizard |
| [DEPLOYMENT.md](./DEPLOYMENT.md) | Docker deployment, env variables, Backup/Restore/DR runbooks |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | Master architecture guide — container mapping, API layers, data flows |
| [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) | Port issues, asset pipelines, device connectivity |
| [CHANGELOG.md](./CHANGELOG.md) | Release history (Keep a Changelog format), test suite metrics |
| [LABEL_STUDIO.md](./LABEL_STUDIO.md) | Label Studio v2.1 — ZPL templates, USB printing, LAN connections |

### Governance Docs

| Document | Purpose |
|---|---|
| [BRD-01 Branding & Attribution](./docs/08-governance/BRD-01_BRANDING_ATTRIBUTION_DOCUMENTATION.md) | Product names, attributions, dynamic footers, domain names |
| [AI Content Policy (AI-GOV-01)](./docs/08-governance/AI_CONTENT_POLICY.md) | Directives for AI coding agents |

### App Repository README

For full technical reference (API docs, architecture, AI agent guide):
👉 **[apps/smriti_retail_os/README.md](./apps/smriti_retail_os/README.md)**

---

## 8. Author Profile

| Field | Detail |
|---|---|
| **Author** | Jawahar R. Mallah |
| **Designation** | Founder & Chief Architect |
| **Organization** | AITDL – AI Technology & Development Lab |
| **Experience** | 20+ years in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation & Enterprise Application Design |

> *"Software should not only process data but also explain decisions. Every report, score, KPI, alert, recommendation, and prediction within SMRITI must be understandable by business users without requiring technical expertise."*
>
> — Jawahar R. Mallah, Founder & Chief Architect, AITDL

---

## 9. License

```
MIT License
Copyright (c) 2026 AITDL NETWORK & ERPNbook.com. All Rights Reserved.

All open-source licensing notices for ERPNext and Frappe
must be preserved in source code files.
```

---

<div align="center">

**SMRITI Retail OS™ — Always Decision-Ready.**

*Retail Operations + Inventory Intelligence + Party Stock Visibility + AI-assisted Decision Support*

**AITDL – AI Technology & Development Lab**
`www.aitdl.com` | `smriti.aitdl.com`

</div>
