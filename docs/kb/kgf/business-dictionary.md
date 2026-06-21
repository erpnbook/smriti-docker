---
title: Business Dictionary
version: 1.0
last_updated: 2026-06-19
applies_to: SMRITI Retail OS v2.2.0
---

# SMRITI Business Dictionary (DOC-04)

The **Business Dictionary** is the central glossary of SMRITI Retail OS. It maps and documents all key retail operational terms (such as PSA, PSV, PDT, WOC, Dead Stock, Size Curves) and links them to the **Formula Registry** and related terms. This ensures that cashiers, store managers, and executives have a unified, searchable reference.

---

## 📋 Schema Definition (`SMRITI Business Term`)

The Business Dictionary is backed by the `SMRITI Business Term` DocType. Each record contains:

*   **Term ID**: Unique glossary key (e.g. `PSA`, `PDT`).
*   **Term Name**: Descriptive name (e.g. "Predictive Distribution Twin").
*   **Term Category**: Category Select (e.g. `Distribution`, `Inventory`, `Forecasting`, `Sales`, `Audit`, `Outlet`).
*   **Term Version**: Glossary versioning (e.g. `1.0.0`).
*   **Replaces Term**: Self-link to a deprecated version of the term.
*   **Status**: Draft, Under Review, Approved, Deprecated (Enforces that only Approved terms can be active).
*   **Definition**: Plain-English definition.
*   **Hinglish Definition**: A localized explanation blending English terminology with Hindi sentence structure to assist ground-level operators.
*   **Term Aliases**: JSON array of aliases for enhanced searchability (e.g. `["Replenishment Engine", "Stock Planner"]`).
*   **FAQ**: JSON list of questions and answers.
*   **Common Mistakes**: JSON list of common operational errors and mitigation advice.
*   **Related Formulas**: Child table (`SMRITI Related Formula`) linking to the Formula Registry.
*   **Related Terms**: Child table (`SMRITI Related Term`) linking to other business terms.
*   **Manual & Training References**: References to printed user guides and training workbook modules.

---

## ⚡ Seeding & Link Validation

*   **Two-Phase Seeding**: To prevent `LinkValidationError` exceptions caused by forward-referencing child tables (e.g. term A linking to term B before term B is created), the seeding patch `seed_default_terms.py` runs in two phases:
    1.  **Phase 1**: Seeds the parent `SMRITI Business Term` records with all text, category, and JSON data.
    2.  **Phase 2**: Resolves database hashes and updates `related_formulas` and `related_terms` child tables with correct document name links.

---

## ⚡ Caching & Auditing

*   **Redis Caching**: Term details are cached in Redis at key `smriti:dictionary:{term_id}:{version}` with a **TTL of 3600 seconds** (1 hour). 
*   **Access Auditing**: Every lookup (cache hit or miss) is recorded in `SMRITI PSV Activity Log` with:
    *   `action_type` = `"Dictionary Accessed"`
    *   `event_type` = `"DICTIONARY_ACCESSED"`
    *   `reference_name` = `{term_id}`

---

## Support & Helpdesk
For questions or support, please contact the SMRITI Helpdesk at **support@aitdl.com**.
