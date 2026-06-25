# SMRITI Documentation Constitution

Version: 1.0.0  
Author: Jawahar R. Mallah, Founder & Chief Architect, AITDL  
Status: Active  

---

## Purpose

This document defines the mandatory documentation governance rules for every AI agent, developer, contributor, and automation working on SMRITI Retail OS. These rules ensure documentation remains consistent, searchable, maintainable, and explainable. No AI agent or developer may create, modify, merge, move, or delete documentation without following these standards.

---

## Zero Duplicate Policy (DRY Knowledge)

**Principle:** SMRITI Retail OS follows a **Single Source of Truth (SSOT)** documentation model. There shall be **only one authoritative document for each topic**. 

Duplicate knowledge is strictly prohibited. Rather than duplicating explanations (e.g. details on authentication or data structures) across multiple guides, you must link/cross-reference the authoritative document ID (e.g. "See [API-004](file:///d:/Smriti_Retail_OS/docs/06-api/auth.md)").

---

## AI Agent Permission Matrix

| Action | AI Allowed | Description |
| --- | --- | --- |
| **Create new document** | ✅ Only if topic doesn't exist | Check `DOCUMENTATION_INDEX.md` first. |
| **Update document** | ✅ | Allowed for corrections/clarifications. |
| **Expand document** | ✅ | Append or add sections to active documents. |
| **Move document** | ✅ | Use `git mv` to preserve git log. |
| **Rename document** | ⚠️ Requires index update | Document ID must remain stable. |
| **Delete document** | ❌ Never | Deletion requires explicit human approval. |
| **Archive document** | ⚠️ With approval | Move status to `Archived` in registry. |
| **Merge document** | ⚠️ Only after conflict report | Follow standard compare-and-extract process. |

---

## AI Decision Tree Workflow

```text
Need to document a feature?
        │
        ▼
Search DOCUMENTATION_INDEX
        │
        ▼
Found?
 YES ─────────► Update Existing Document (Append/Expand/Cross-reference)
 NO
        │
Create New Document (Assign Prefix ID & Ownership Header)
        │
Update DOCUMENTATION_INDEX
        │
Update Cross References
        │
Update Revision History
        │
PASS
```

---

## Core Governance Rules

### Rule 1 — Single Source of Truth
Every topic must have exactly one primary document. Duplicate documentation is prohibited. If similar documents exist, merge them, keep one authoritative document, and redirect references.

### Rule 2 — Audience First
Every document must target one primary audience (Product/Executive, End User, Administrator, Installer, Developer, API Integrator, Support Engineer, Architect). Do not mix multiple audiences in one document unless necessary.

### Rule 3 — Documentation Categories
Every document must belong to exactly one of the 9 defined categories under `docs/` (`01-product` to `09-release-notes`).

### Rule 4 — Standard Document Structure
Every document must follow the standard metadata header and template defined in `DOCUMENTATION_STYLE_GUIDE.md`.

### Rule 5 — Never Delete Knowledge
AI agents must never remove useful information. Instead, move, merge, mark deprecated, or archive. Deletion requires explicit human approval.

### Rule 6 — Append Before Rewrite
When expanding documentation, append new sections whenever practical. Do not rewrite an entire document unless requested. Preserve git history.

### Rule 7 — Explainability
Whenever formulas, workflows, algorithms, or business rules are documented, include: Purpose, Inputs, Outputs, Formula, Worked Example, Exceptions, Business Meaning, and Related Rules.

### Rule 8 — Cross References
Every document must contain Related Documents references. Never leave isolated documents without links.

### Rule 9 — Naming Convention
Use descriptive lowercase names using underscores. Avoid `notes.md`, `test2.md`, `misc.md`, or `final_v2.md`.

### Rule 10 — Folder Ownership
Every document belongs to only one folder. Avoid duplicate files across folders.

### Rule 11 — Images
Store images separately in `docs/images/`. Reference images via markdown syntax; do not duplicate screenshots.

### Rule 12 — Examples
Include sample data, commands, expected results, and common mistakes in all manuals.

### Rule 13 — Developer Documents
Developer documents must include architecture, sequence diagrams, data flow, dependencies, testing, extension points, and known limitations.

### Rule 14 — User Documents
User guides should avoid internal implementation details. Focus on tasks, screenshots, examples, and troubleshooting.

### Rule 15 — API Documents
Every endpoint must document: Purpose, Authentication, Parameters, Request, Response, Errors, and Examples.

### Rule 16 — Troubleshooting Format
Every troubleshooting article follows: Problem, Symptoms, Cause, Resolution, Verification, Prevention, and Related Articles.

### Rule 17 — Release Notes
Never edit historical release notes. Append new versions only.

### Rule 18 — Version History
Every document must maintain a Revision History table (Version, Date, Author, Summary of Changes).

### Rule 19 — AI Change Log
Whenever an AI agent edits documentation, record the change in the document's Revision History and the AI Change Log in the index. Do not silently change documents.

### Rule 20 — Documentation Index
Every new or modified document must be registered or updated in the master `DOCUMENTATION_INDEX.md`.

### Rule 21 — Merge Rules
When merging, compare documents, extract unique information, append to the primary document, update links, and mark the duplicate as archived. Never delete first.

### Rule 22 — Quality Checklist
Before saving a document verify: Correct audience, Correct folder, Standard structure, No duplicate topic, Related documents added, Examples included, Revision history updated.

### Rule 23 — AI Agent Workflow
Before modifying documentation: Locate existing document, Check for duplicates, Update existing document when possible, Create new document only if the topic does not exist, Update cross references, Update index, Update revision history.

### Rule 24 — Success Criteria
Documentation is compliant only when every topic has one authoritative document, no duplicate knowledge exists, all documents are indexed, and cross references are complete.

### Rule 25 — Index Search First
Before creating any document, the AI agent must search `DOCUMENTATION_INDEX.md` to ensure the topic or a similar file does not exist.

### Rule 26 — Update Over Create
If a matching topic exists in the index, the AI agent must update the existing document rather than creating a new file.

### Rule 27 — Forbidden Filenames
AI agents must never create filenames containing `copy`, `copy2`, `v2`, `new`, `updated`, `final`, `latest`, `draft`, `revision`.

### Rule 28 — No Topic Splitting
Never split one topic across multiple documents without explicit architecture approval.

### Rule 29 — Atomic Commits & Index Sync
Every commit that modifies any documentation file must also include updates to the master `DOCUMENTATION_INDEX.md`.

### Rule 30 — Governance Escalation
If unsure where a document belongs or how to merge overlapping contents, the AI agent must stop and request human approval.

---

> "Always decision-ready."  
> — Jawahar R. Mallah, Founder & Chief Architect, AITDL
