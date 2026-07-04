# CHANGELOG — smriti-docker (erpnbook/smriti-docker)

## [2.4.1] — 2026-07-04

### Changed
- docs: bump bundled smriti_retail_os app reference to v2.1.0 (Engineering Governance)
- chore: extend .gitignore to exclude verification screenshots and local test artifact files

### Added
- docs(arch): import architecture governance files from cloud migration
  - architecture_baseline.json
  - ARCHITECTURE_MIGRATION_BACKLOG.md
  - check_architecture_boundaries.py

### Bundled App Versions
- smriti_retail_os: 2.1.0 (was 2.0.0)
- frappe: v16.19.1 (unchanged)
- erpnext: v16.19.1 (unchanged)

---

## [2.4.0] — 2026-07-02

### Added
- feat: automate custom folder icon on Windows during installation [35282e4]
- docs(ui): create SMRITI UI Governance Constitution (Rules UG-01 to UG-10) [94abd63]
- docs(ui): integrate design system, token migration constitution, validate_tokens [2c79145]
- docs(connectivity): create user manual, developer specs, KB articles for UIE [docs commit]
- docs(kb): update troubleshooting guides and index for sprint 3 theme changes [157c40b]
- docs: add Issues 39, 40, 41, 42 to master troubleshooting guide [ddaf250, ad9d041]
- Consolidate SMRITI UI Verification and Governance Rules 1-10 in AGENTS.md [d57ff2b]

### Changed
- docs: rename installation directory Smriti9 across all guides [f19bb81]
- docs: update barcode print layouts, tokens, QZ Tray support [49f151d]
- docs: update all documents for Barcode Studio navigation consolidation [3dd65a5]
- docs: update INSTALL.md with Windows folder icon customization details [a845a76]
- chore: recompile SDC discovery catalog (multiple updates) [multiple]
- chore: update discovery index for UIE, SCF, and nav manager [multiple]
- build: comment out demo company seeding script in Docker env config [558e2cb]

### Fixed
- fix(install): remove non-ASCII emojis from install.ps1 [ea8a1ea]
- fix(install): move markdown tip out of code block, polish success banner [7d6af9d]
- fix(git): enforce LF line endings for shell scripts [60f1601]

---

## [2.3.5] — Previous Release
