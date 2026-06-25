---
title: Product Catalogue Import
version: 1.0
last_updated: 2026-06-18
applies_to: SMRITI Retail OS v1.x
---

# SMRITI OS Product Catalogue Import Guide

This guide describes how to format, import, and validate your product catalog within SMRITI Retail OS, satisfying the critical Go-Live catalog checks.

## 📄 File Formatting Requirements

Product imports are processed using Excel (`.xlsx`) or CSV templates. Format the import sheet with the following standard columns:

| Item Code | Item Name | Item Group | Default UOM | Disabled | Is Sales Item | Maintain Stock | Default HSN |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ITEM-001` | Leather Boot | Footwear | Nos | No | Yes | Yes | `640399` |
| `ITEM-002` | Running Shoe | Footwear | Nos | No | Yes | Yes | `640399` |

- **Disabled**: Must be explicitly set to `No` to ensure product visibility at the registers.
- **Is Sales Item**: Must be set to `Yes` for billing selection.
- **Maintain Stock**: Must be set to `Yes` to enforce warehouse deduction checks.
- **Default HSN**: 6 or 8-digit tax code required for GST mapping.

---

## 🚀 Catalog Import Protocol

1. Navigate to **Masters** → **Item Master** list.
2. Select **Import Data** (Data Import utility).
3. Download the standard blank template.
4. Populate item attributes following the naming conventions.
5. Upload the file and run validation. Correct any UOM or Category errors before committing.
6. Click **Start Import** to insert records.

---

## 💰 Price Configuration & MRP Mappings

A catalog requires price assignments before cashiers can check out items:
- **Price Lists**: SMRITI references two price lists:
  - `Standard Selling`: The base price pre-tax.
  - `MRP`: Maximum Retail Price (inclusive of all taxes).
- **Price Assignment**: Navigate to **Pricing** → **Item Price** and map prices for your imported items under both lists:
  ```text
  ITEM-001 | Standard Selling = Rs. 1,000
  ITEM-001 | MRP              = Rs. 1,180
  ```
  Ensure prices are active to satisfy the Go-Live Price List checklist item.
