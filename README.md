<div align="center">
  <img src="apps/smriti_retail_os/smriti_retail_os/public/images/logo.svg" alt="SMRITI Retail OS" width="120" />
  <h1>SMRITI Retail OS</h1>
  <p>Official Docker Orchestration for the SMRITI Retail Experience Layer.</p>
  <p><b>Stable Production Release: <code>v1.2.10</code></b> 🚀</p>
</div>

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
- **DO NOT** use default passwords like `admin` in production.
- Operators must configure a secure, unique password inside the Setup Wizard on first boot.

Once setup is complete, access the billing terminal at:
- **Billing Desk**: `http://localhost:9000/billing` (isolated cashier login)
- **ERPNext Desk**: `http://localhost:8080/app` (manager / administrator login)

---

## 🗺️ Documentation Index

For deep technical setups, operations, and architectural reviews, consult SMRITI's specialized manuals:

- 🧙‍♂️ **[INSTALL.md](./INSTALL.md)**: Full Fresh, Upgrade, and Development setup instructions, including the 5-step Setup Onboarding wizard guide.
- 🏷️ **[LABEL_STUDIO.md](./LABEL_STUDIO.md)**: SMRITI Label Studio v2.1 guide (ZPL/TSPL templates, Live Autocomplete search, QZ Tray USB, LAN sockets, Print Analytics).
- 🚀 **[DEPLOYMENT.md](./DEPLOYMENT.md)**: Container orchestration configuration (`pwd.yml`), volume mounts, ports, and Backup/Restore/Disaster Recovery runbooks.
- 🛠️ **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)**: Consolidated troubleshoot manual (Docker mapping, Nginx 502, CSS MIME-types, Socket origins, QZ Tray).
- 📋 **[CHANGELOG.md](./CHANGELOG.md)**: Version history log (Keep a Changelog format), test suite growth, and release versioning strategy.
- 🏗️ **[ARCHITECTURE.md](./ARCHITECTURE.md)**: Master technical reference explaining SEL concept, API layers, and Docker container mappings.

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
