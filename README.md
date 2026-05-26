<div align="center">
  <img src="apps/smriti_retail_os/smriti_retail_os/public/images/logo.svg" alt="SMRITI Retail OS" width="120" />
  <h1>SMRITI Retail OS</h1>
  <p>Official Docker Orchestration for the SMRITI Retail Experience Layer.</p>
</div>

## What is this?

This repository contains the Docker configuration and orchestration required to run **SMRITI Retail OS**. It provides a pre-configured environment that integrates:

- **Frappe Framework v16**
- **ERPNext v16** (Core Business Logic)
- **India Compliance** (GST, E-Invoicing, Audit Trail)
- **SMRITI Retail OS** (Premium Experience Layer & Custom POS)

## Features of this Setup

- **Automated Installation**: The `pwd.yml` workflow automatically installs all required apps and performs database migrations.
- **Shared Assets Volume**: Includes a dedicated volume for compiled CSS and JS, ensuring the custom SMRITI Light Theme loads instantly on the frontend.
- **Automated Builds**: Running `bench build` is integrated into the site creation lifecycle.
- **Performance Optimized**: Configured with dedicated workers for short and long queues, and optimized Redis caching.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose v2](https://docs.docker.com/compose/)
- [git](https://git-scm.com/)

## Quick Start

The fastest way to launch the SMRITI Retail environment locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/erpnbook/smriti-docker.git
   cd smriti-docker
   ```

2. **Launch the containers**:
   ```bash
   docker compose -f pwd.yml up -d
   ```

3. **Wait for initialization**:
   The first boot takes about 2-5 minutes as it sets up the database and installs SMRITI OS. You can monitor progress with:
   ```bash
   docker logs -f smriti_retail_os-create-site-1
   ```

4. **Access the System**:
   - **URL**: [http://localhost:8080](http://localhost:8080)
   - **Username**: `Administrator`
   - **Password**: `admin`

## Repository Structure

- `pwd.yml`: The primary orchestration file for local development and staging.
- `apps/`: (Mount Point) Contains the source code for SMRITI Retail OS and India Compliance.
- `sites/`: (Volume) Persistent storage for site configurations and file uploads.
- `assets/`: (Volume) Shared storage for compiled frontend assets.

## SMRITI UI Conventions

- **Clean Naming**: All internal modules are named without "SMRITI" prefixes (e.g., *Retail Billing*, *Inventory Operations*) to ensure a professional, uncluttered interface.
- **Premium Light Theme**: Default high-contrast theme optimized for retail store lighting conditions.

## License

This orchestration setup is provided under the MIT License.
