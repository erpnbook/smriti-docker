# SMRITI Retail OS — Production Deployment & Disaster Recovery Guide

This guide details the steps required to deploy, configure, back up, and recover a production instance of **SMRITI Retail OS**.

---

## 1. Docker Compose Orchestration

The production environment is managed using Docker Compose and is defined in [pwd.yml](./pwd.yml). 

### 1.1 Container Stack
The system provisions 9 separate containers:
- **`backend`**: Frappe / ERPNext app server (Gunicorn).
- **`frontend` (Nginx)**: Serves static assets and proxy-routes traffic. Maps container port `8080` to host port `8765` (by default) for full Desk and billing access, and exposes an optional cashier-locked terminal on container port `9000` (can be optionally mapped to host port `9000` for strict cashier lockdown).
- **`websocket`**: Handles long-polling and real-time Socket.IO events.
- **`db`**: MariaDB database server.
- **`redis-cache`** & **`redis-queue`**: Memory caching and job broker services.
- **`queue-short`** & **`queue-long`**: RQ background job processing workers.
- **`scheduler`**: Background job daemon (Beat scheduler).

### 1.2 Named Volumes
Two primary named volumes are used for persistence and data sharing:
1. **`smriti_retail_sites`**: Shared between the `backend` and `frontend` containers to host site databases, configurations, and compiled static assets.
2. **`smriti_retail_logs`**: Stores backend server and worker application logs.

---

## 2. Environment Settings (`.env`)

A `.env` file must be created in the root folder before starting the stack. Configure the following critical environment variables:

```env
# Target versions for the container image build
FRAPPE_VERSION=version-16
ERPNEXT_VERSION=version-16

# Port mappings on the host machine
HTTP_PUBLISH_PORT=8765

# Database credentials (use strong, unique values in production)
DB_ROOT_PASSWORD=your_secure_root_db_pass
DB_PASSWORD=your_secure_db_user_pass

# Admin Setup Wizard Key (CSRF / session control)
SETUP_WIZARD_KEY=your_cryptographically_secure_key
```

---

## 3. Production Security & Account Provisioning

### 3.1 Initial Administrator Password
- The default `Administrator` account is provisioned during the execution of the initial setup wizard.
- **DO NOT** use default passwords like `admin` in production.
- Operators must configure a secure, complex password for the `Administrator` account directly within the Setup Wizard.

### 3.2 Password Rotation & Console Resets
If the administrator credentials need to be reset or rotated via the command line:
1. Execute the reset command within the running backend container:
   ```bash
   docker exec -it smriti_retail-backend-1 bench --site smriti_retail set-admin-password "YourNewSecurePassword123!"
   ```
2. Clear the server auth cache to enforce immediate session termination:
   ```bash
   docker exec -it smriti_retail-backend-1 bench --site smriti_retail clear-cache
   ```

---

## 4. Backup Strategy

Data safety requires automated off-site synchronization. SMRITI Retail OS uses a tiered backup strategy.

### 4.1 Daily Scheduled Backups
- The `scheduler` container automatically runs backups daily at midnight.
- Standard SQL dumps and site configuration files are compiled into `/sites/smriti_retail/private/backups/`.

### 4.2 Cloud Synchronizations (S3 & rclone)
- **SMTP Limit Warning**: While SMRITI includes an email-based backup feature, standard SMTP servers restrict attachments to **10MB - 25MB**. As your database grows, email backups will **fail silently**.
- **Recommended Strategy**: Use S3/rclone integration.
  1. Open the SMRITI Company Settings panel at `/configure`.
  2. Input your S3 Bucket Name, Access Key, Secret Key, and endpoint URL.
  3. SMRITI will use the container's built-in `rclone` utility to stream compressed database dumps directly to secure cloud storage.

### 4.3 Key Version Retention Policy
> [!IMPORTANT]
> Encryption key versions must not be removed until all backups encrypted using that version have expired according to the configured backup retention policy.
>
> **Example**:
> - Retention Period = 90 days
> - v1 key may only be retired after all v1 backups have been deleted and verified absent.

---

## 5. Restore Strategy

To restore a database and site state on a fresh or repaired machine:

### Step 1: Place Backups in the Private Backups Folder
Copy your backup files (`.sql.gz` database dump, `-site_config_backup.json` configuration, and tarballs for public/private files) to the backups directory:
```bash
# Target directory path
/home/frappe/frappe-bench/sites/smriti_retail/private/backups/
```

### Step 2: Execute Bench Restore
Execute the restoration script from within the backend container:
```bash
docker exec -it smriti_retail-backend-1 bench --site smriti_retail restore \
  /home/frappe/frappe-bench/sites/smriti_retail/private/backups/yyyyMMdd_hhmmss-database.sql.gz \
  --with-public-files /home/frappe/frappe-bench/sites/smriti_retail/private/backups/yyyyMMdd_hhmmss-public_files.tar \
  --with-private-files /home/frappe/frappe-bench/sites/smriti_retail/private/backups/yyyyMMdd_hhmmss-private_files.tar
```

### Step 3: Run Database Migrations & Rebuild Assets
Apply database schema changes and clear system caches:
```bash
docker exec -it smriti_retail-backend-1 bench --site smriti_retail migrate
docker exec -it smriti_retail-backend-1 bench build --app smriti_retail_os
docker exec -it smriti_retail-backend-1 bench --site smriti_retail execute smriti_retail_os.sync_assets.sync_assets
docker exec -it smriti_retail-backend-1 bench --site smriti_retail clear-cache
```

---

## 6. Disaster Recovery Plan (DRP)

In the event of complete hardware failure or data corruption, follow this recovery runbook:

1. **Deploy New Host**: Provision a fresh VM or OS instance with Docker Desktop / Docker Compose and Git installed.
2. **Clone Configuration**: Clone the orchestration repository:
   ```bash
   git clone https://github.com/erpnbook/smriti-docker.git smriti
   cd smriti
   ```
3. **Restore environment settings**: Re-create the `.env` file with matching database passwords and system configurations.
4. **Pull cloud backups**: Download the latest database dump (`.sql.gz`) and assets tarballs from your S3 storage bucket.
5. **Launch Stack**: Start the containers:
   ```bash
   docker compose -f pwd.yml up -d
   ```
6. **Initialize Site Restore**: Re-run the Restore Strategy (Section 5) using the retrieved backup files.
7. **Verify Operations**: Execute the local health check script to confirm all containers and endpoints are healthy:
   ```powershell
   .\check.ps1
   ```
