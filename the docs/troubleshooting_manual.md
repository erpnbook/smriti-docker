# SMRITI Retail OS — Troubleshooting Manual

This manual provides solutions to common issues encountered during development, installation, and operation of SMRITI Retail OS.

---

## 1. Asset 404 & MIME Type Refusal Warnings
### Symptom
* Browser console shows: `Refused to apply style from '...' because its MIME type ('text/html') is not a supported stylesheet MIME type`.
* Custom app elements (like India Compliance GST settings) crash with `ReferenceError: gst_settings is not defined`.
* Stylesheets or layout components are visually broken.

### Diagnosis
In a multi-container Docker environment, Nginx serves compiled static files from a shared volume (`sites/assets`). When you run `bench build`, esbuild compiles assets and updates the manifest `assets.json`.
If `assets.json` is missing custom app keys or is overwritten with old container-local manifests, Frappe falls back to requesting files directly from the web root, yielding 404 HTML pages. Because strict MIME type checking (`nosniff`) is active, the browser rejects this HTML.

### Solution
Run a full build and force-sync the manifests inside the backend container:
```powershell
# 1. Compile fresh assets for all apps
docker exec -w /home/frappe/frappe-bench demoinstall2t-backend-1 bench build

# 2. Merge assets.json manifests and copy physical assets to shared volume
docker exec -w /home/frappe/frappe-bench demoinstall2t-backend-1 bench --site frontend execute smriti_retail_os.sync_assets.sync_assets

# 3. Clear server cache
docker exec -w /home/frappe/frappe-bench demoinstall2t-backend-1 bench --site frontend clear-cache
```

---

## 2. Websocket Socket.io Connection Failures (400 Bad Request)
### Symptom
* Browser console shows: `Error connecting to socket.io: Unauthorized / Bad Request` or `fetch failed`.
* Real-time notifications and background task updates are not received.

### Diagnosis
The browser attempts to establish a websocket/polling connection to the `websocket` container on port `8080`. The connection is rejected if the request origin `http://localhost:8080` is not whitelisted in the site's configurations.

### Solution
Explicitly configure CORS origins in the database configuration:
```powershell
# 1. Configure allowed origins
docker exec -w /home/frappe/frappe-bench demoinstall2t-backend-1 bench set-config allow_cors_origin "http://localhost:8080"

# 2. Clear cache
docker exec -w /home/frappe/frappe-bench demoinstall2t-backend-1 bench --site frontend clear-cache
```

---

## 3. Nginx 502 Bad Gateway
### Symptom
* Accessing `http://localhost:8080` immediately returns `502 Bad Gateway`.

### Diagnosis
Nginx starts up before the Gunicorn backend container is fully initialized. Nginx resolves the backend host IP address during its initial load; if Gunicorn is not yet listening, Nginx caches a stale IP or fails to resolve it, leading to a persistent 502.

### Solution
Ensure that `pwd.yml` has the backend healthcheck and dependency constraints active:
```yaml
services:
  backend:
    healthcheck:
      test: ["CMD-SHELL", "curl -s -o /dev/null -w '%{http_code}' http://localhost:8000 | grep -E '^(200|404)$'"]
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 30s

  frontend:
    depends_on:
      backend:
        condition: service_healthy
```
This forces the Nginx frontend to wait until Gunicorn is fully healthy before starting.

---

## 4. Git Conflicts During Asset Sync
### Symptom
* Running `git pull` on the host machine throws: `error: Your local changes to the following files would be overwritten by merge`.

### Diagnosis
Manually copying files (like `main.js`, `smriti_branding.css`, or `sync_assets.py`) directly from your workspace directory to your local container volume mount directory creates unstaged local changes in the target repository.

### Solution
Reset the unstaged changes in the target directory and pull the clean commit from origin:
```powershell
# Discard local copy changes and fast-forward pull from origin
git -C D:\demoinstall2t\apps\smriti_retail_os checkout -- .
git -C D:\demoinstall2t\apps\smriti_retail_os pull origin main
```
