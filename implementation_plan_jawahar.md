# Smriti Retail OS — Easier Installation Plan

## Problem Summary

Users attempting to install Smriti Retail OS are hitting multiple friction points,
all documented in `TROUBLESHOOTING.md` and `TROUBLESHOOTING2.md`. The core issues are:

1. **Hardcoded Windows path** `D:/Smriti_Retail_OS/assets` in `pwd.yml` — breaks on every other machine
2. **Empty `apps/` folders** — users clone repo but forget to populate `apps/smriti_retail_os/` and `apps/india_compliance/`
3. **No validation before `docker compose up`** — errors surface minutes later inside containers with cryptic logs
4. **Manual 6-step process** — most users miss steps 5 (asset sync) or get container names wrong
5. **No post-install health check** — users don't know if installation succeeded

---

## User Review Required

> [!WARNING]
> `pwd.yml` currently has hardcoded `D:/Smriti_Retail_OS/assets` bind mounts that **will fail on anyone else's machine**. We propose to fix this using a relative path `./assets` or a named volume. Please confirm.

> [!IMPORTANT]
> The installer script will **auto-clone** `apps/smriti_retail_os` from GitHub. Please confirm the public GitHub URL for the app repo (currently assumed: `https://github.com/erpnbook/smriti.git --branch v1.0.0`).

> [!IMPORTANT]
> Default credentials will remain `Administrator / admin` for the generated site. Do you want to prompt the user for a custom admin password during install?

---

## Open Questions

1. Should the installer support **Linux/macOS** too (via `install.sh`) or **Windows-only** (PowerShell)?
2. Should the `assets/` folder be a **named Docker volume** (simpler, cross-platform) or a **bind mount** (easier to debug)?
3. Should we add a **one-command installer** wrapper (e.g., `irm https://... | iex` for PowerShell)?

---

## Proposed Changes

### Component 1 — Fix Hardcoded Paths in `pwd.yml`

#### [MODIFY] [pwd.yml](file:///d:/Smriti_Retail_OS/pwd.yml)

Replace all occurrences of `D:/Smriti_Retail_OS/assets` with `./assets`
so any user cloning the repo can run it without editing the file.

Also replace `./apps/smriti_retail_os` and `./apps/india_compliance` with
properly documented relative paths.

---

### Component 2 — Automated Windows Installer Script

#### [NEW] [install.ps1](file:///d:/Smriti_Retail_OS/install.ps1)

A single PowerShell script that:

1. **Pre-flight checks**: verifies Docker is installed and running, Git is available, port 8080 is free
2. **Clones app sources** into `./apps/smriti_retail_os` and `./apps/india_compliance` if not present
3. **Copies the `assets/` folder** from the current directory (no hardcoded path)
4. **Runs `docker compose -f pwd.yml up -d`**
5. **Waits and streams logs** from `create-site` container
6. **Runs post-install** asset sync and setup commands
7. **Prints a success banner** with the URL and credentials

```powershell
# Usage: .\install.ps1
# Or with custom password: .\install.ps1 -AdminPassword "MyPassword"
```

---

### Component 3 — Linux/macOS Installer Script

#### [NEW] [install.sh](file:///d:/Smriti_Retail_OS/install.sh)

Same steps as `install.ps1` but for bash (Linux/macOS/WSL).

---

### Component 4 — Pre-flight Validator

#### [NEW] [check.ps1](file:///d:/Smriti_Retail_OS/check.ps1)

A standalone diagnostic script users can run at any time to validate their environment:

| Check | What it verifies |
|---|---|
| Docker running | `docker info` succeeds |
| Port 8080 free | Nothing else is binding port 8080 |
| App source present | `apps/smriti_retail_os/pyproject.toml` exists |
| Container health | All 9 containers are Up (post-install) |
| Site accessible | HTTP 200 from `http://localhost:8080` |

---

### Component 5 — Improved `pwd.yml` (No Hardcoded Paths)

Replace the hardcoded `D:/Smriti_Retail_OS/assets` bind-mount with `./assets`
across all 6 service definitions (backend, configurator, create-site, frontend, queue-long, queue-short, scheduler).

---

### Component 6 — Rewritten README.md

#### [MODIFY] [README.md](file:///d:/Smriti_Retail_OS/README.md)

Restructure into clear sections:
- **One-Command Install** (Windows + Linux) at the very top
- **Manual Step-by-Step** for advanced users
- **Troubleshooting** link to `TROUBLESHOOTING.md`
- **Requirements** (Docker, Git, 8080 free)
- **Upgrade guide**

---

### Component 7 — INSTALL.md (New Dedicated Install Guide)

#### [NEW] [INSTALL.md](file:///d:/Smriti_Retail_OS/INSTALL.md)

A detailed installation guide separate from README covering:
- Windows (Docker Desktop) step-by-step with screenshots described
- Linux/macOS (Docker Engine) step-by-step
- Common first-boot issues and quick fixes
- Post-install verification checklist

---

## Verification Plan

### Automated Tests
- Run `.\check.ps1` after install to confirm all containers are healthy
- Verify `http://localhost:8080` returns HTTP 200
- Confirm `Administrator/admin` login works

### Manual Verification
- Walk through `.\install.ps1` on a clean Windows machine (no existing volumes)
- Verify the script recovers gracefully if `apps/` folders already exist
- Verify hardcoded path fix: clone to a different directory and confirm `docker compose up` still works
