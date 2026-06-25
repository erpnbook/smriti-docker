<div align="center">
  <img src="apps/smriti_retail_os/smriti_retail_os/public/images/logo.svg" alt="SMRITI Retail OS" width="100" /><br/><br/>

  # SMRITI Retail OS™
  **Enterprise Retail Operations Platform**<br/>
  Built on the ERPNext® application and the Frappe® Framework.

  ![Version](https://img.shields.io/badge/version-v1.2.10-1A2B5C)
  ![Status](https://img.shields.io/badge/status-Production%20Candidate-22c55e)
  ![License](https://img.shields.io/badge/license-MIT-yellow)
  ![ERPNext](https://img.shields.io/badge/ERPNext-v16-2563EB)
  ![Frappe](https://img.shields.io/badge/Frappe-v16-2563EB)
  ![Docs](https://img.shields.io/badge/Docs-211%20entries-22c55e)

</div>

---

| | |
|---|---|
| **Developer** | AITDL – AI Technology & Development Lab |
| **Version** | `v1.2.10` — Production Candidate |
| **Compatibility** | ERPNext v16 · Frappe v16 · India Compliance v16 |
| **License** | MIT — Free for commercial use |
| **Copyright** | © 2026 AITDL NETWORK & ERPNbook.com |

---

## 1. Product

SMRITI Retail OS is a **Retail Experience and Intelligence Layer** built on top of ERPNext. ERPNext handles the transaction engine — accounting, inventory, GST, compliance. SMRITI handles everything the retail user sees and does.

> SMRITI Retail OS™ — Built on the ERPNext® application and the Frappe® Framework.
> Developed by AITDL – AI Technology & Development Lab.

---

## 2. Features

| Area | Capabilities |
|---|---|
| **POS & Billing** | Keyboard-first cashier terminal, hold/recall, manager override, loyalty |
| **Inventory** | GRN, stock transfer, stock audit, reorder alerts |
| **Purchase** | Purchase orders, supplier management, landed cost |
| **Analytics** | Sales velocity, weeks of cover, outlet health, dead stock |
| **Channel (PSV)** | Party Stock Visibility — distributor stock via shadow ledger |
| **Formula Registry** | Central KPI registry with ⓘ Explain on every metric |
| **POS Profiles** | Create, clone, archive profiles with shift-lock protection |
| **Trial CRM** | Lead capture, trial activation, platform admin |
| **Compliance** | GST, e-Invoice, e-Waybill via India Compliance v16 |
| **PWA** | Offline-ready service worker, IndexedDB cache |

---

## 3. Architecture

```
+----------------------------------------------------------+
|                  SMRITI Retail OS™                       |
|  Experience · Intelligence · Retail Workflows · PSV      |
+----------------------------------------------------------+
                          │
                          ▼
+----------------------------------------------------------+
|              ERPNext v16  (System of Record)             |
|  Accounting · Inventory · POS · Customers · Compliance   |
+----------------------------------------------------------+
                          │
                          ▼
+----------------------------------------------------------+
|              Frappe Framework v16                        |
|  ORM · Auth · REST · Scheduler · Hooks                  |
+----------------------------------------------------------+
                          │
                          ▼
+----------------------------------------------------------+
|  Database & Infrastructure (MariaDB · Redis · Docker)    |
+----------------------------------------------------------+
```

**Accounting model**: ERPNext is the operational System of Record for transaction-level accounting (GL, GST, invoices). Statutory financial reporting (P&L, Balance Sheet) is handled by TallyPrime in deployments where Tally integration is active.

→ Full details: **[ARCHITECTURE.md](./apps/smriti_retail_os/ARCHITECTURE.md)**

---

## 4. Quick Start

### Docker

```bash
# 1. Start containers
docker compose up -d

# 2. Install app
docker compose exec smriti_retail-backend-1 \
  bench --site frontend install-app smriti_retail_os

# 3. Build assets
docker compose exec smriti_retail-backend-1 \
  bench build --app smriti_retail_os

# 4. Open browser
http://localhost:8765
```

→ **[INSTALL.md](./INSTALL.md)** — Full setup guide
→ **[DEPLOYMENT.md](./DEPLOYMENT.md)** — Docker, env variables, Backup/Restore/DR

---

## 5. Project Structure

```
Smriti_Retail_OS/                    ← This workspace
├── apps/smriti_retail_os/           ← SMRITI Frappe app
│   ├── smriti_retail_os/api/        ← Whitelisted API endpoints
│   ├── smriti_retail_os/services/   ← Business logic
│   ├── smriti_retail_os/repositories/ ← Data access
│   ├── smriti_retail_os/www/        ← Standalone pages (100+ routes)
│   ├── smriti_retail_os/tests/      ← Unit tests
│   ├── README.md                    ← App-level technical reference
│   └── ARCHITECTURE.md             ← Architecture constitution
├── docs/                            ← Documentation portal (211 entries)
│   └── DOCUMENTATION_INDEX.md      ← Master registry
├── compose.yaml                     ← Docker production config
├── INSTALL.md
├── DEPLOYMENT.md
├── ARCHITECTURE.md                  ← Workspace architecture guide
├── CHANGELOG.md
└── README.md                        ← This file
```

---

## 6. Documentation

Every SMRITI module ships with a complete documentation set:

> Product Guide · User Guide · Admin Guide · Developer Guide · API Reference · Knowledge Base

→ **[Documentation Index](./docs/DOCUMENTATION_INDEX.md)** — 211 registered documents

---

## 7. Governance

SMRITI follows the **SMRITI Architecture Constitution** — locked rules for UI policy, service-first design, system of record boundaries, auditability, and explainability.

| Rule | Summary |
|---|---|
| Rule 7 — SMRITI-First UI | No Frappe Desk (`/desk`, `/app`) ever exposed to end users |
| Rule 10 — Auditability | Every critical action logged: user, timestamp, before/after values |
| DOC-01 — Explainability | Every metric has a `ⓘ Explain` modal with formula and example |

→ **[ARCHITECTURE.md](./apps/smriti_retail_os/ARCHITECTURE.md)** — All 15 constitution rules

---

## 8. Root Documents

| Document | Purpose |
|---|---|
| [INSTALL.md](./INSTALL.md) | Environment setup and onboarding |
| [DEPLOYMENT.md](./DEPLOYMENT.md) | Docker deployment, env, Backup/Restore/DR |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | Workspace-level architecture guide |
| [CHANGELOG.md](./CHANGELOG.md) | Release history and test metrics |
| [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) | Ports, assets, device connectivity |
| [LABEL_STUDIO.md](./LABEL_STUDIO.md) | Barcode label printing (ZPL, USB, LAN) |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Contribution guidelines |
| [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) | Code of conduct |
| [BRANDING_POLICY.md](./BRANDING_POLICY.md) | Trademark and attribution rules |

---

## 9. License

```
MIT License
Copyright (c) 2026 AITDL NETWORK & ERPNbook.com. All Rights Reserved.

All open-source licensing notices for ERPNext and Frappe
must be preserved in source code files.
```

→ **[ABOUT_AUTHOR.md](./apps/smriti_retail_os/ABOUT_AUTHOR.md)** — Jawahar R. Mallah, Founder & Chief Architect, AITDL

---

<div align="center">
  <em>SMRITI Retail OS™ — Always Decision-Ready.</em><br/>
  <em>Developed by AITDL – AI Technology &amp; Development Lab</em>
</div>
