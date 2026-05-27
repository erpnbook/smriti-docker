# SMRITI Retail OS — Developer Manual

Welcome to the SMRITI Retail OS Developer Manual. This document provides a complete technical guide to the system's architecture, custom overrides, branding logic, and development workflow.

---

## 1. Architecture Overview

SMRITI Retail OS is designed as a custom, lightweight, whitelabeled layer on top of **Frappe Framework v16** and **ERPNext v16**. 

### System Topology
The application runs in a multi-container Docker environment composed of:
1. **Frontend (Nginx):** Serves static files and proxies API requests to Gunicorn and websockets to Socket.io.
2. **Backend (Gunicorn):** Handles core database, API requests, and web sessions.
3. **Websocket (NodeJS):** Manages real-time notifications and events.
4. **Database (MariaDB 11.8):** Stores application schemas and relational records.
5. **Redis Cache / Queue:** Caches active objects and handles background task workers (long/short/scheduler).
6. **Asset Guard:** Runs in the background to ensure security and whitelabeling compliance.

---

## 2. Key Codebase Components

The system is split into two custom app folders mounted into the Frappe bench:
* **`apps/smriti_retail_os`:** Contains custom layouts, simplified billing forms,Loyalty & Promotions, barcode tag layouts, and the whitelabeling layer.
* **`apps/india_compliance`:** Manages Indian GST rules, e-way bills, and e-invoicing.

### Core Public Assets
All CSS and JS client logic resides inside the app package folder:
* **JS Layout Controller:** `smriti_retail_os/public/js/main.js`
* **Custom Styling Systems:** `smriti_retail_os/public/css/smriti_branding.css`
* **POS Billing System:** `smriti_retail_os/public/js/smriti_billing.js`
* **Reports View:** `smriti_retail_os/public/js/smriti_reports.js`

---

## 3. Whitelabeling & Client Safety Net

To deliver a 100% SMRITI-branded experience, the client-side uses a layered safety net implemented in `main.js`:

1. **frappe.boot Data Patching (`_patch_frappe_boot`):**
   Prior to UI rendering, we patch internal boot objects like `frappe.boot.app_name`, `frappe.boot.sysdefaults.app_name`, and app switcher maps to replace references to "ERPNext" or "Frappe" with "SMRITI Retail OS".

2. **DOM TreeWalker Scrubber (`_do_scrub`):**
   Traverses the active DOM tree nodes to find and replace text occurrences of "ERPNext", "Frappe Technologies", and hides external copyright links.

3. **MutationObserver Scrubber:**
   Runs the DOM scrubber continuously whenever new nodes or modals are appended to the document root, preventing flashes of unbranded content.

---

## 4. Toggleable Sidebar Mechanics

The Desk sidebar can be dynamically toggled between the **Left** and **Right** sides of the viewport.

### JS Component Insertion
Inside `main.js`, `_setup_sidebar_toggle()` handles button injection and state:
* Reads cached preference from `localStorage.getItem('smriti-sidebar-position')` (defaults to `left`).
* Checks if a toggle button (`.smriti-sidebar-toggle-sidebtn`) exists in `.sidebar-header`. If missing, it injects a Material Symbol button (`swap_horiz`).
* Clicking the button toggles `.smriti-sidebar-right` on the `body` element and updates `localStorage`.

### CSS Flex Layout
When the `.smriti-sidebar-right` class is applied to `body`, the layout switches automatically:
```css
/* Swaps sidebar (first child) and main content (second child) positions */
body.smriti-sidebar-right {
  flex-direction: row-reverse !important;
}

/* Flips borders and places the resize handle on the left edge */
body.smriti-sidebar-right .body-sidebar {
  border-right: none !important;
  border-left: 1px solid var(--smriti-border) !important;
}
body.smriti-sidebar-right .sidebar-resize-handle {
  right: auto !important;
  left: -4px !important;
  cursor: w-resize !important;
}
```

---

## 5. Asset Compiling & Syncing Pipeline

Because the container's `/sites` directory is a shared Docker volume and standard assets live inside the container's local file system, assets must be physically synced.

### Merging Manifests (`sync_assets.py`)
`sync_assets.py` runs during boot and after compilation. It merges container-local manifests with shared volume manifests:
```python
merged = {}
merged.update(src_data)  # Load container-local (old base image hashes)
merged.update(dst_data)  # Overwrite/add with newly compiled shared volume hashes
```
This preserves custom app bundles (like `india_compliance.bundle.js` and `smriti_retail_os` JS/CSS files) and aligns correct stylesheet hashes.

### Development Workflow
When making changes to client CSS or JS files:
1. Edit the source code on Windows (in `apps/smriti_retail_os/`).
2. Run `bench build` inside the backend container to compile bundles.
3. Run `sync_assets.py` to copy and merge the new bundles into the shared Nginx volume.
4. Run `bench clear-cache` to force browsers to fetch the updated files.
