# SMRITI Documentation Manifest

Version: 1.0.0  
Author: Jawahar R. Mallah, Founder & Chief Architect, AITDL  
Status: Active  

---

## Welcome to the SMRITI Retail OS Documentation Hub

This manifest serves as the entry point and structural blueprint for all documentation within the SMRITI Retail OS repository. Any developer, AI agent, or contributor must read this manifest and the associated governance files before creating, editing, moving, or deleting any documentation.

---

## Documentation Architecture

All documentation is organized into **nine (9) structured folders** and **four (4) core governance files** at the root of the `docs/` directory.

### Core Governance Roots
- [DOCUMENTATION_MANIFEST.md](file:///d:/Smriti_Retail_OS/docs/DOCUMENTATION_MANIFEST.md) *(This file)* — Overall architecture, folder mappings, and entry guide.
- [DOCUMENTATION_CONSTITUTION.md](file:///d:/Smriti_Retail_OS/docs/DOCUMENTATION_CONSTITUTION.md) — Mandatory governance rules, permission matrix, decision tree, and zero-duplicate policies.
- [DOCUMENTATION_STYLE_GUIDE.md](file:///d:/Smriti_Retail_OS/docs/DOCUMENTATION_STYLE_GUIDE.md) — Writing standards, markdown formats, heading structures, worked example layouts, and YAML frontmatter templates.
- [DOCUMENTATION_INDEX.md](file:///d:/Smriti_Retail_OS/docs/DOCUMENTATION_INDEX.md) — The authoritative registry cataloging every document, stable IDs, statuses, and ownership metadata.

### Folder Mapping & Taxonomy

```text
docs/
├── 01-product/          # Product overview, features, roadmap, licensing, commercial
├── 02-user-guide/       # Cashier, billing, inventory, POS, daily operations
├── 03-admin-guide/      # Users, permissions, trial administration, company setup, backup, scheduler
├── 04-installation/     # Installation, Docker, Bench setup, migration, upgrade
├── 05-developer/        # Services, source code, hooks, testing, coding standards
├── 06-api/              # REST APIs, whitelisted methods, integration, webhooks
├── 07-kb/               # Errors, troubleshooting, FAQ, recovery guides
├── 08-architecture/     # Core architecture, formula registry, KGF, explainability, state machines
└── 09-release-notes/    # Version history, sprint notes, migration guides, breaking changes
```

---

## Documentation Lifecycle

All documents cycle through the following status values:
1. **Draft**: Newly created files undergoing initial writing.
2. **Review**: Completed files awaiting architect or peer review.
3. **Approved**: Verified files ready for publication.
4. **Active**: The official current documentation for a feature.
5. **Deprecated**: Outdated but preserved for historical context.
6. **Archived**: Moved out of active circulation but retained in history.

---

## AI Agent & Developer Workflow

Before doing any work, follow the **Phase 0 Governance Gate**:
1. Check the [DOCUMENTATION_INDEX.md](file:///d:/Smriti_Retail_OS/docs/DOCUMENTATION_INDEX.md) to see if a document on the topic already exists.
2. If it exists, update the existing document. **Do not create a new one.**
3. If it does not exist, create the document under the appropriate folder, assign a stable **Document ID**, and register it in `DOCUMENTATION_INDEX.md`.
4. Ensure all changes include updated **Revision History** and follow the templates in `DOCUMENTATION_STYLE_GUIDE.md`.

---

## Maintenance & Auditing

The documentation is audited once per sprint to generate a **Documentation Health Report** detailing compliance metrics, broken links, and missing metadata. Keep the system clean, DRY, and accurate.

> "Always decision-ready."  
> — Jawahar R. Mallah, Founder & Chief Architect, AITDL
