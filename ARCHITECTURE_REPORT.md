# Architecture Report: SMRITI Retail OS

## 1. Executive Summary
SMRITI Retail OS is architected as a **Sophisticated Experience Layer** (SEL) built on top of the Frappe v16 and ERPNext v16 framework. Unlike traditional ERPNext customizations that modify the core business logic, Smriti Retail OS prioritizes **UI/UX Transformation** and **Operational Simplification** for the retail environment. It maintains the integrity of the underlying ERP while providing a high-performance, distraction-free interface for cashiers.

## 2. Core Modules & Component Mapping

### 2.1 Custom Experience Apps
- **`smriti_retail_os`**: The primary logic engine. It handles:
  - **Billing API (`billing_api.py`)**: A high-performance wrapper for POS and Sales Invoices.
  - **Inventory API (`inventory_api.py`)**: Streamlined material transfers and stock lookups.
  - **Security API (`security_api.py`)**: Enforces "Governance Tiers" and restricts administrative access for retail roles.
- **`india_compliance`**: Integrated to handle GST, E-Invoicing, and Indian tax regulatory requirements.

### 2.2 UI Transformation ("Shoper9 Pure Mode")
- **Client-Side Hijacking**: The system uses `doctype_js` hooks (e.g., `public/js/sales_invoice.js`) to transform complex ERPNext forms into a "Pure" mode.
- **Role-Based Redirection**: Cashiers are redirected via `role_home_page` hooks to a standalone `/billing` terminal, completely bypassing the standard ERPNext Desk.

## 3. Infrastructure & Deployment Architecture

### 3.1 Docker Orchestration (`pwd.yml`)
The system uses a multi-container Docker Compose setup:
- **`backend`**: Frappe/ERPNext application server.
- **`frontend`**: Nginx server serving assets and proxying requests.
- **`websocket`**: For real-time POS updates.
- **Workers**: Separated long and short queues for background jobs.

### 3.2 The "Asset Guard" Strategy (`sync_assets.py`)
A unique architectural feature of Smriti Retail OS is its **Physical Asset Syncing**. Standard Frappe on Docker often suffers from 404/MIME-type errors due to complex symlinks in shared volumes. 
- **Mechanism**: `sync_assets.py` unlinks symlinks and physically copies assets from app directories into the `sites/assets` shared volume.
- **Triggers**: Executed on fresh install, container boot, and after every `bench migrate`.

## 4. Data Model & Extensibility

### 4.1 Custom DocTypes
- **`SMRITI Company Settings`**: A centralized, multi-tenant configuration DocType that stores branding, series prefixes, and operational defaults.
- **Virtual Masters**: DocTypes like `SMRITI Heel Type`, `SMRITI Outsole`, etc., provide structured attributes for the retail sector (Footwear/Apparel).
- **Audit Logs**: `SMRITI Address Audit Log` tracks critical store-level metadata changes.

### 4.2 Schema Implementation
- **Code-Driven Schema**: Custom DocTypes and fields are defined in `setup.py` and instantiated via Python during migration, rather than using standard JSON manifest files.

## 5. Integration Model
- **India Compliance**: Deeply coupled with `smriti_retail_os` for automated GST percentage mapping and tax template resolution in the `billing_api.py`.
- **Nginx Bridge**: Port 9000 is used as a specialized ingress for the billing terminal to ensure high availability and isolation from standard Desk traffic.

---
*Evidence Reference: `apps/smriti_retail_os/smriti_retail_os/hooks.py`, `setup.py`, `billing_api.py`, `sync_assets.py`*
