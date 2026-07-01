# RELEASE NOTES — smriti-docker v2.4.0
# Release Date: 2026-07-02
# Previous Release: v2.3.5
# Commits since last tag: 41

## Summary

Documentation expansion, install script hardening, Windows UX improvements,
and UI governance framework publication.

## Features
- Windows custom folder icon automatically applied during installation
- SMRITI UI Governance Constitution published (Rules UG-01 to UG-10)
- Connectivity workspace user manual (UIE) — full documentation

## Enhancements
- Installation directory renamed to Smriti9 across all guides
- Troubleshooting guide updated: Issues 39–42 added
- Barcode Studio navigation consolidated in all docs (v2.4.2 update)
- SDC compiler discovery catalog updated for all new DocTypes
- AGENTS.md — UI Verification Governance Rules 1-10 consolidated

## Bug Fixes
- install.ps1: Non-ASCII emojis removed (prevented PowerShell parser errors)
- install.ps1: Markdown tip moved out of code block
- LF line endings enforced for shell scripts in gitattributes

## Deployment Notes
This is a documentation and install-script release.
No Docker Compose service changes.
No image version changes.
Pull latest: git pull origin main

## Known Issues
- KI-005: Demo company seeding disabled in Docker env config (intentional)
