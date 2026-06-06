# Changelog — SMRITI Retail OS

All notable changes to **SMRITI Retail OS** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned (v2.0.0 Roadmap)
- Redesign the core desktop client utilizing Frappe v17.
- Implement AI-driven stock-out prediction engines.
- Add multi-currency cashier ledger balancing.

---

## [1.2.10] — 2026-06-06

### Added
- **Style/Article Search & Autocomplete**: Added a debounced (300ms) fuzzy search suggestion dropdown on the Style / Article input field (`flt-style`) supporting keyboard navigation (`Arrow Up`, `Arrow Down`, `Enter`, `Escape`) and auto-loading to the print queue worksheet (activated via configuration).
- **Test Suite Expansion**: Added test coverage for barcode and variant autocomplete queries, growing the automated test suite to **94 passing tests**.

### Fixed
- **Test Database Pollution**: Resolved MariaDB test database cleanup issues and prevented child table pollution in subsequent unit test runs.

---

## [1.2.9] — 2026-06-05

### Added
- **SMRITI Label Studio v2.1 Release Candidate**: Integrated local printing WebSocket handlers for QZ Tray, custom signature validation settings, printer latency socket benchmarks, and visual print safety confirmation dialogs.
- **Label Studio Print Run Analytics**: Built a database dashboard counting printed labels, templates usage stats, and printer diagnostics.
- **LAN Printing raw sockets**: Added TCP socket connections to network label printers over port `9100`.

---

## [1.2.8] — 2026-06-05

### Changed
- **Domain Migration to erpnbook.com**: Migrated all system references, whitelabel headers, support links, email templates, and developer domains from `smriti.io` to `erpnbook.com`.

### Fixed
- **Duplicate Scripts Cleanup**: Cleaned up duplicate security audit scripts in the app package directory.

---

## [1.2.7] — 2026-06-05

### Added
- **Warehouse Type Bootstrapping**: Added defensive bootstrapping logic in `setup_wizard_api.py` to create standard ERPNext Warehouse Types (`Transit`, `Standard`, `Subcontracted`) before company inserts, preventing the `Could not find Warehouse Type: Transit` error.

### Fixed
- **Setup Wizard Guest Whitelist**: Whitelisted `get_setup_wizard_initial_data` and `run_setup_wizard` API endpoints to support guest onboarding flows.
- **Privilege Escalation during setup**: Escales guest session context to `Administrator` programmatically to bypass link validations during new company creations.

---

## [1.2.6] — 2026-06-05

### Changed
- **N+1 Query Optimizations**: Collapsed database loops inside `item_master_api.py` using lookup caches, reducing queries by 90% on bulk variant imports.
- **SQL Aggregations**: Refactored in-memory Python calculations in `reports_api.py` into SQL queries (`SUM`, `COUNT`, `GROUP BY`).

### Security
- **Dynamic Password Generation**: Replaced hardcoded default installer passwords with randomized secure hashes (`secrets.token_urlsafe(16)`) per user.

---

## [1.2.1] — 2026-06-04

### Added
- **Custom Warehouse Selectors**: Allowed passing optional `warehouse` parameter overrides to Purchase Order, Purchase Receipt, and GRN creation endpoints.
- **Automated Tests**: Added new test cases verifying warehouse overrides, expanding the test suite to **87 passing tests**.

### Fixed
- **Company Warehouse Mismatch**: Implemented the `_get_default_warehouse(company)` helper to query warehouses matching the target company context first, preventing database cross-company validation errors.

---

## [1.2.0] — 2026-06-04

### Added
- **Smart PWA Support**: Implemented Smart Multi-Strategy caching service workers, push notification bindings, and offline fallback interfaces.
- **Offline IndexedDB Store**: Created `SmritiOfflineStore` for local database saving of pending invoices, customer lookups, and offline barcode registers.

### Fixed
- **Supplier Lookup Filters**: Removed the restricted `supplier_type: "Company"` constraint from Purchase Orders, enabling cashiers to select Individual suppliers.

---

## [1.1.0] — 2026-06-03

### Added
- **Primary Barcode Architecture**: Added the `custom_is_primary` field to `Item Barcode` child table, enforcing exactly one primary barcode per item variant and enabling ZPL print fallbacks.
- **Sizewise Barcode Scanning**: Added HID keyboard-wedge scanner support on `/sizewise_invoice` with automatic column increments and green/red flash CSS feedback.

---

## [1.0.0] — 2026-06-02

### Added
- **Docker Orchestration**: Configured standard `pwd.yml` multi-container stack.
- **Asset Guard**: Created `sync_assets.py` to hard-copy compiled bundles to Nginx, resolving CSS/JS MIME-type blockages.
- **Shoper9 Pure Mode**: Simplified POS invoices view, filtering out complex ERP warehouse columns for standard cashiers.
- **Automated Test Suite**: Launched initial test suite with **81 passing automated tests**.

---

## Versioning & Release Strategy

SMRITI Retail OS release pipelines are separated into logical branches:

1. **`main`**: Represents the stable production release branch. All tags are generated from this branch.
2. **Maintenance Branches (`v1.2.x`)**: Used for hotfixes and patch integrations for existing installations.
3. **Development Branches (`dev`)**: Feature-specific staging environments where changes are validated before merging.

### Test Suite Growth
Quality control gates monitor automated test volumes over major milestones:
- **v1.0.0**: 81 Passing Tests (Initial release baseline)
- **v1.2.1**: 87 Passing Tests (Added custom warehouse tests)
- **v1.2.10**: 94 Passing Tests (Added search/autocomplete and clean setup assertions)

### Release Readiness Matrix
The current platform status is represented by the following readiness metrics:

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
