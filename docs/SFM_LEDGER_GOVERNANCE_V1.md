# SMRITI Sales Force Management (SFM) — Ledger Governance (v1.0.0)

---

### Author Profile (Start)
* **Author**: Jawahar R. Mallah
* **Designation**: Founder & Chief Architect
* **Organization**: AITDL – AI Technology & Development Lab
* **Professional Experience**: 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.

#### Author Note
This governance directive is based on practical field experience gathered across retail operations, distribution management, inventory control, software architecture, business automation, and enterprise solution development. The objective is to make SMRITI Retail OS understandable and usable by both technical and non-technical users.

> "Light begins with learning."
> 
> — Jawahar R. Mallah
> Founder & Chief Architect, AITDL

---

## 1. Immutability Directive (Rule SFM-GOV-001)

SMRITI Attribution Ledger is classified as an operational sub-ledger. Once written, records in `tabSMRITI Attribution Ledger` **SHALL NOT** be updated, modified, or hard-deleted.
- Standard Frappe write/delete permissions for the `SMRITI Attribution Ledger` DocType are restricted to the `Administrator` role ONLY.
- All other roles (`System Manager`, `SMRITI Store Manager`, `Sales Manager`) only have **Read** privileges on the ledger.
- System updates are handled purely by service functions executing under `ignore_permissions=True`.

---

## 2. Ledger Status Lifecycle (Rule SFM-GOV-002)

Every ledger entry is initialized with a status. The allowable states are:
1. **Active**: The row represents a currently valid attribution credit.
2. **Superseded**: The row has been superseded by a correction entry (e.g. employee reallocation, credit percentage adjustment). Stays in the ledger for historical tracing, but is excluded from active calculations.
3. **Reversed**: The row has been cancelled (e.g. invoice cancelled, return processed). Stays in the ledger, balanced out by a corresponding negative reversal row.

---

## 3. Reversal Mechanics (Rule SFM-GOV-003)

When a `POS Invoice` or `Sales Invoice` is cancelled, the ledger MUST be reconciled using reversal entries.
1. The service looks up all ledger entries where `invoice_reference` matches the cancelled invoice and `ledger_status == "Active"`.
2. For each entry, it:
   - Generates a **Reversal Entry**:
     - Copies all fields (`employee`, `customer`, `ownership_type`, `company`, `store`, `warehouse`, etc.).
     - Sets `revenue_credit` = `-1 * original_revenue_credit`.
     - Sets `credit_percentage` = `original_credit_percentage`.
     - Sets `ledger_status` = `"Reversed"`.
     - Sets `reversal_reference` = Original Ledger Entry `name`.
     - Inserts the reversal entry.
   - Updates the **Original Entry**:
     - Sets `ledger_status` = `"Reversed"`.
     - Sets `reversal_reference` = Reversal Ledger Entry `name`.
     - Saves the original entry.
3. This guarantees that summing `revenue_credit` across the ledger naturally cancels out the cancelled transaction amount.
