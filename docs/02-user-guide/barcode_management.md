---
Document ID: "USER-001"
Title: "Barcode Management & Hardening Guide"
Owner: "Operations Team"
Audience: "End User"
Module: "Core"
Version: "1.0.0"
Status: "Active"
Primary Document: "Yes"
Depends On: ""
Related Modules: ""
Last Updated: "2026-06-25"
Last Reviewed: "2026-06-25"
AI Generated: "Yes"
Reviewed By: "Jawahar R. Mallah"
---

# Barcode Management & Hardening Guide

This guide describes how to manage **Primary and Secondary Barcodes** in SMRITI Retail OS, including manual entry rules, bulk imports, printing fallbacks, and auditing missing barcodes.

---

## 1. Primary vs. Secondary Barcodes

SMRITI Retail OS supports multi-barcode setups (Option B) to accommodate multi-channel operations:
- **Primary Barcode**: The default barcode scanned at billing terminals and printed on retail price tags. Exactly one primary barcode is enforced per size-variant.
- **Secondary Barcodes**: Vendor-supplied barcodes, global GTINs, or marketplace codes. Scanning any secondary barcode will correctly resolve the same item.

---

## 2. Importing Barcodes from Excel

The **Sizewise Item Master Bulk Importer** supports loading both primary and secondary barcodes.

### Column Mapping

| Excel Column Header | Type | Purpose |
|---|---|---|
| `BARCODE NO` | Primary | The main retail barcode (auto-generated if left blank). |
| `SECONDARY BARCODES` | Secondary | Comma-separated list of additional barcodes (e.g. `VND123, GTIN8890`). |

### Import Preservation Rules
- Updating a style variant or re-running an import **will not delete** your existing secondary barcodes.
- The importer automatically detects duplicate secondary barcodes and prevents them from being registered if they conflict with other items in the system.

---

## 3. Manual Barcode Constraints

When typing barcodes manually in the Size Config matrix:
1. **Allowed Characters**: Letters (`A-Z`, `a-z`), numbers (`0-9`), hyphens (`-`), and underscores (`_`).
2. **Disallowed Characters**: Spaces, punctuation, and symbols (e.g., `#`, `@`, `*`, `$`).
3. **Length**: Must be between **3 and 30 characters**.
4. **Collision Prevention**: The system checks if the manual barcode collides with any existing barcode or `Item Code` in the database.

---

## 4. Barcode Resolution & Printing Fallback

When printing tags via `/barcode` or resolving items at the POS:
1. The system checks for a **Primary Barcode**.
2. If no barcode is marked primary, it falls back to the **first created barcode**.
3. If no barcodes exist at all, it uses the **Item Code**.

---

## 5. Identifying Items Missing Barcodes

To scan your inventory for active products without barcodes:
- Store managers can query the active missing barcodes list from the backend to identify items that need print runs or vendor barcode linking.
- Only active, sellable variants (not templates) are scanned.

## Revision History

| Version | Date | Author | Summary of Changes |
| --- | --- | --- | --- |
| 1.0.0 | 2026-06-25 | Jawahar R. Mallah | Reorganized & standardized |


---

## Author Profile

- **Author**: Jawahar R. Mallah
- **Designation**: Founder & Chief Architect
- **Organization**: AITDL – AI Technology & Development Lab
- **Professional Experience**: 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.

> "Always decision-ready."  
> — Jawahar R. Mallah  
> Founder & Chief Architect, AITDL