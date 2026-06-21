# SMRITI Retail OS™

<div align="center">
  <img src="apps/smriti_retail_os/smriti_retail_os/public/images/logo.svg" alt="SMRITI Retail OS" width="120" />
  <h2>Developed by AITDL</h2>
  <p><b>Powered by ERPNext® & Frappe® Framework</b></p>
  <p>SMRITI Retail OS is a Retail Intelligence Platform that extends ERPNext through advanced operational, analytical, and governance capabilities. 🚀</p>
  <p><b>Stable Production Release: <code>v1.2.10</code></b></p>
</div>

---

## 1. Product Identity

* **Official Name**: SMRITI Retail OS™
* **Developer Entity**: AITDL – AI Technology & Development Lab
* **Attribution Requirement**: All primary public-facing interfaces and manuals must display the following attribution notice:
  > **SMRITI Retail OS™**  
  > Developed by AITDL  
  > Powered by ERPNext® & Frappe® Framework

---

## 2. Architecture Overview

SMRITI Retail OS follows an experience-first, API-driven architecture model designed to decouple the frontend user experience from backend schema structures:

```text
       SMRITI Retail OS (Custom Frontend & www pages)
                           ↓
                 Service APIs & Controllers
                           ↓
                  Frappe Framework Layer
                           ↓
                     ERPNext Core
                           ↓
                     Database Layer
```

* **ERPNext Backend**: Retains role as the primary System of Record for accounting, general ledger, taxes (GST), sales/purchase invoices, inventory valuation, stock ledger, and warehouse/customer master data.
* **SMRITI Frontend Layer**: Owns POS cashier checkout, operational store workflows, replenishment reorders, shadow ledgers for distributor inventory, and the explainable metrics reporting dashboard.

---

## 3. Core Subsystems & Modules

SMRITI extends ERPNext through five specialized business intelligence engines:

* **Predictive Distribution Twin (PDT)**: Real-time stock coverage analytics, sales velocity tracking, and safety stock reorder alerting.
* **Channel Governance Engine (CGE)**: Enforces validation rules, price list resolutions, and exception-handling schemes across all channel connections.
* **Party Stock Visibility (PSV) & PSA**: Shadow ledger architecture providing real-time tracking of distributor-held channel stock without altering ERPNext stock ledger entries.
* **SMRITI Formula Registry**: Centralized registry for all computed retail KPIs (e.g., GMROI, WOC, dead stock scores, scan reliability scores) to enforce formula consistency.
* **SMRITI Explain Engine**: Context-specific **ⓘ Explain** modals integrated across dashboards to break down math formulas and recommended actions for store staff.

---

## 4. Attribution & Branding Guidelines

* **Trademark Policy**: Compound branding that implies ERPNext is co-branded or owned by SMRITI is strictly prohibited. Use "SMRITI Retail OS™ powered by ERPNext®".
* **Domain Policy**: Partner, reseller, or store domains must not contain "erpnext" or "frappe". Approved placeholders for development/testing: `erpnbook.com`, `smriti.aitdl.com`, `yourdomain.com`.

---

## 5. Licensing Notice

* **License**: SMRITI Retail OS is released under the **MIT License**.
* **Copyright**: Copyright © 2026 AITDL NETWORK & ERPNbook.com. All Rights Reserved.
* **Attributions**: All open-source licensing notices for ERPNext and Frappe must be preserved in source code files.

---

## 6. Documentation Links

Refer to the primary developer and operator manuals below:

* 🧙‍♂️ **[INSTALL.md](./INSTALL.md)**: Onboarding instructions, environment setup, and the 5-step onboarding wizard guide.
* 🏷️ **[LABEL_STUDIO.md](./LABEL_STUDIO.md)**: Label Studio v2.1 operator manual (designing templates, USB printing, direct LAN connections, and print analytics).
* 🚀 **[DEPLOYMENT.md](./DEPLOYMENT.md)**: Deployment parameters, environment files, and Backup/Restore/Disaster Recovery runbooks.
* 🛠️ **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)**: Troubleshooting index for ports, asset pipelines, and local device connectivity.
* 📋 **[CHANGELOG.md](./CHANGELOG.md)**: Release history (Keep a Changelog format) and automated test suite metrics.
* 🏗️ **[ARCHITECTURE.md](./ARCHITECTURE.md)**: Master architecture guide detailing container mapping, API layers, and data flows.

---

## 7. Governance Links

Centralized platform standards and AI policies:

* ⚖️ **[BRD-01 Branding & Attribution Standard](./docs/governance/BRD-01_BRANDING_ATTRIBUTION_DOCUMENTATION.md)**: Official guidelines for product names, attributions, dynamic footers, and domain names.
* 🤖 **[AI Content Policy (AI-GOV-01)](./docs/governance/AI_CONTENT_POLICY.md)**: Directives for AI coding agents generating code, manuals, explanations, and metadata.
