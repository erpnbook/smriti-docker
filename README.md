<div align="center">
  <img src="apps/smriti_retail_os/smriti_retail_os/public/images/logo.svg" alt="SMRITI Retail OS" width="120" />
  <h1>SMRITI Retail OS</h1>
  <p><b>Complete Retail Operations Platform</b></p>
  <p>Modern Retail Operating System for Footwear, Apparel, Fashion, Grocery, and Multi-Store Retail Businesses. 🚀</p>
  <p><b>Stable Production Release: <code>v1.2.10</code></b></p>
</div>

---

## ⚡ What is SMRITI Retail OS?

SMRITI Retail OS is a modern, high-performance retail platform designed specifically to handle complex inventory structures, rapid customer checkouts, and multi-store operations. It provides business operators and cashiers with a beautiful, distraction-free environment to manage sales billing, merchandising, and warehouse workflows.

---

## ✨ Features

- **Smart Billing**: Cashier-focused POS terminal with barcode scanning, hold/recall queues, and security-gated manager overrides.
- **Purchase Management**: Streamlined vendor procurement, pricing controls, and Goods Receipt Note (GRN) mappings.
- **Inventory Control**: Real-time stock counts, sizing matrix conversions, and automated store-to-store material transfers.
- **Barcode Center**: Unique EAN-13 namespace allocations, primary/secondary barcode registries, and duplicate protection.
- **Label Studio v2.1**: In-browser barcode template designer with raw ZPL/TSPL stream printing over local USB or network LAN sockets.
- **Sizewise Sales**: Sizewise matrix invoice entries with keyboard-wedge HID scanner support.
- **GST Ready**: Automated HSN code lookup tax derivation and compliant tax splits for Indian states.
- **Multi-Store Operations**: Centralized company controls with independent warehouse registers per retail outlet.
- **Setup Wizard**: 5-step onboarding wizard for rapid site provisioning.
- **Docker Deployment**: Fully containerized orchestration stack for local and cloud hosting.

---

## ⚡ Quick Install

Ensure Docker Desktop and Git are installed and running, then execute the command for your OS:

### Windows (PowerShell)
```powershell
git clone https://github.com/erpnbook/smriti-docker.git smriti_retail
cd smriti_retail
PowerShell -ExecutionPolicy Bypass -File .\install.ps1
```

### Linux / macOS (Bash)
```bash
git clone https://github.com/erpnbook/smriti-docker.git smriti_retail
cd smriti_retail
bash install.sh
```

---

## 🔒 Security Configuration Note

The master `Administrator` account is provisioned dynamically during the onboarding wizard. 
- **DO NOT** use default passwords in production.
- Operators must configure a secure, unique password inside the Setup Wizard on first boot.

Once setup is complete, access the platform endpoints:
- **Cashier Billing Terminal**: `http://localhost:8765/billing` (isolated checkout login)
- **Manager Desk**: `http://localhost:8765/app` (administration portal login)

### Access
Local machine : http://localhost:8765
LAN access    : http://<server-ip>:8765
Internet      : Not exposed by default (router port-forward required)

Internal container port:
8080 (Docker internal only)

---

## 🗺️ Documentation Index

For detailed technical references, operational guides, and version histories, consult the specialized manuals:

- 🧙‍♂️ **[INSTALL.md](./INSTALL.md)**: Onboarding instructions, including manual container setup and the 5-step onboarding wizard guide.
- 🏷️ **[LABEL_STUDIO.md](./LABEL_STUDIO.md)**: Label Studio v2.1 operator manual (designing templates, USB printing, direct LAN connections, and print analytics).
- 🚀 **[DEPLOYMENT.md](./DEPLOYMENT.md)**: Deployment parameters, environment files, and Backup/Restore/Disaster Recovery runbooks.
- 🛠️ **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)**: Troubleshooting index for ports, asset pipelines, and local device connectivity.
- 📋 **[CHANGELOG.md](./CHANGELOG.md)**: Releases history (Keep a Changelog format) and automated test suite metrics.
- 🏗️ **[ARCHITECTURE.md](./ARCHITECTURE.md)**: Master architecture guide detailing container mapping, API layers, and data flows.

---

## 📊 Module Release Readiness Matrix

The following matrix tracks the status of SMRITI's core subsystems:

| Module              | Status                      |
| ------------------- | --------------------------- |
| Setup Wizard        | ✅ Stable                    |
| Masters             | ✅ Stable                    |
| Billing Engine      | ✅ Stable                    |
| Purchase            | ✅ Stable                    |
| Inventory           | ✅ Stable                    |
| Sizewise Invoice    | ✅ Stable                    |
| Barcode Center      | ✅ Stable                    |
| Label Studio v2.1   | ✅ Stable                    |
| Analytics Dashboard | ⚠️ Requires Production Data |
| USB/QZ Printing     | ⚠️ Pilot Validation         |
| LAN Printing        | ⚠️ Pilot Validation         |
| SmartPOS Framework  | 🚧 Ongoing Expansion        |

---

## ✅ Continuous Integration & Quality Gates

SMRITI enforces 100% test passing gates prior to production releases:
- **Quality Gate**: **94/94 passing automated tests** in the test suite.
- Run tests at any time in the backend container:
  ```bash
  docker exec smriti_retail-backend-1 bench --site smriti_retail run-tests --app smriti_retail_os
  ```
