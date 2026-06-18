---
title: GST Configuration
version: 1.0
last_updated: 2026-06-18
applies_to: SMRITI Retail OS v1.x
---

# SMRITI OS GST Configuration Guide

This guide details configuring India GST templates, mapping Item-wise HSN codes, and setting up POS profiles for automatic tax calculation.

## 📄 Creating GST Tax Templates

SMRITI utilizes standard **Sales Taxes and Charges Templates** to apply taxes during checkout. Set up the templates for standard tax slabs:

### Example: GST 18% Template
1. Create a new Sales Taxes and Charges Template named `GST 18%`.
2. Add the tax ledger rows:

| Type | Account Head | Rate (%) | Description |
| :--- | :--- | :---: | :--- |
| **On Net Total** | CGST Account | 9.0 | Central GST (9%) |
| **On Net Total** | SGST Account | 9.0 | State GST (9%) |

For interstate customers, configure a matching `IGST 18%` template mapping the full 18% rate to the Integrated GST ledger.

---

## 🏷️ HSN Code & Item-Wise Tax Mapping

SMRITI relies on the **India Compliance** application to validate and calculate taxes at the item row level. Configure tax mapping:
- **HSN Code validation**: Ensure every item variant is assigned a valid 6 or 8-digit HSN code (e.g. `640399` for leather footwear).
- **Item-wise Tax Override**: For products with dynamic tax slabs (e.g., items priced under Rs. 1,000 taxed at 5% and over Rs. 1,000 taxed at 12%), configure tax rules:
  1. Open the Item card and locate the **Tax** section.
  2. Map the GST category to the respective slab template.

---

## ⚙️ POS Profile Integration

To enable auto-calculation of GST during register checkout:
1. Open the target **POS Profile**.
2. Set the default **Sales Taxes and Charges Template** (e.g., `GST 18%`).
3. Check **Apply Tax Automatically** to ensure CGST/SGST calculation is executed immediately on product scans.
