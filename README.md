<div align="center">
  <img src="apps/smriti_retail_os/smriti_retail_os/public/images/logo.svg" alt="SMRITI Retail OS" width="120" />
  <h1>SMRITI Retail OS</h1>
  <p>Official Docker Orchestration for the SMRITI Retail Experience Layer.</p>
  <p><b>Stable Production Release: <code>v1.0.0</code></b> 🚀</p>
</div>

---

## What is this?

This repository contains the official Docker Compose configuration and orchestration required to run **SMRITI Retail OS**. It provides a fully pre-configured, production-ready environment that integrates:

- **Frappe Framework v16**
- **ERPNext v16** (Core Business Logic, Inventory, Accounting)
- **India Compliance** (GST, E-Invoicing, Audit Trail)
- **SMRITI Retail OS App (`v1.0.0`)** (Premium Retail Experience Layer, POS Billing, Material Transfers)

---

## Features of this Setup

- **Automated Installation & Config**: The updated `pwd.yml` workflow automatically mounts required folders, installs custom apps, and sets up site credentials.
- **Robust Physical Asset Sync**: Custom built-in hard-sync utility (`sync_assets`) that unlinks complex app symlinks and copies physical bundles straight to Nginx, completely bypassing Nginx MIME-type/404 errors.
- **Day-to-day Operations Optimized**: Fully pre-allocated queues (long, short) and background workers.
- **Prone to High Stability**: Integrated with 19/19 passing automated test suite covers.

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose v2](https://docs.docker.com/compose/)
- [git](https://git-scm.com/)

---

## Quick Start (Fresh Installation)

To launch the SMRITI Retail environment locally:

1. **Clone this orchestration repository**:
   ```bash
   git clone https://github.com/erpnbook/smriti-docker.git smriti_retail
   cd smriti_retail
   ```

2. **Fetch the stable app releases**:
   ```bash
   mkdir -p apps
   git clone --branch v1.0.0 https://github.com/erpnbook/smriti.git apps/smriti_retail_os
   git clone --branch version-16 https://github.com/resilient-tech/india_compliance.git apps/india_compliance
   ```

3. **Launch the containers**:
   ```bash
   docker compose -f pwd.yml up -d
   ```

4. **Monitor site initialization**:
   The first boot takes about 2-5 minutes to configure MariaDB and compile assets. Monitor progress with:
   ```bash
   docker logs -f smriti_retail_os-create-site-1
   ```

5. **Execute SMRITI initial setup & Asset Sync**:
   Once site creation completes:
   ```bash
   # Run the custom configuration setup
   docker exec smriti_retail_os-backend-1 bench --site frontend execute smriti_retail_os.setup.setup_smriti_retail_os
   
   # Sync assets physically to Nginx
   docker exec smriti_retail_os-backend-1 bench --site frontend execute smriti_retail_os.sync_assets.sync_assets
   ```

6. **Access the System**:
   - **URL**: [http://localhost:8080](http://localhost:8080)
   - **Username**: `Administrator`
   - **Password**: `admin`

---

## Updating an Existing Environment to `v1.0.0`

If you are already running an older version of the container setup, update to the stable production version by running:

```bash
# 1. Pull the stable app code
cd apps/smriti_retail_os
git pull origin main
cd ../..

# 2. Run migrations inside the backend container
docker exec smriti_retail_os-backend-1 bench --site frontend migrate

# 3. Build and hard-sync compiled production assets
docker exec smriti_retail_os-backend-1 bench --site frontend build --app smriti_retail_os
docker exec smriti_retail_os-backend-1 bench --site frontend execute smriti_retail_os.sync_assets.sync_assets

# 4. Clear cache
docker exec smriti_retail_os-backend-1 bench --site frontend clear-cache
```

---

## Running Automated Tests

To ensure the local container stack matches SMRITI's absolute stability standards, execute the full unit test suite:

```bash
docker exec smriti_retail_os-backend-1 bench --site frontend run-tests --app smriti_retail_os
```
*(All 19/19 tests must complete with **`OK`** status).*

---

## SMRITI UI Conventions

- **Shoper9 Pure Mode**: Simplifies complex ERPNext views (like Sales Invoices) down to essential POS columns (`Item Code`, `Item Name`, `Qty`, `Rate`, `Amount`), hiding accounting/warehouse clutter for cashiers.
- **Glassmorphic Dashboards**: Stunning custom cards with backdrop blur filters and dynamic hover actions that match modern web layouts.
- **System Manager Bypass**: Standard System Managers are completely unaffected and see the un-altered, full-featured ERPNext interface.

---

## License

This orchestration setup is provided under the MIT License.
