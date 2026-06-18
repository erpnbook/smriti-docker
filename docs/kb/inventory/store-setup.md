---
title: Store Setup Guide
version: 1.0
last_updated: 2026-06-18
applies_to: SMRITI Retail OS v1.x
---

# SMRITI OS Store & Company Setup

This guide details configuring SMRITI Retail OS company parameters, mapping standard corporate accounts, and setting up cost centers.

## 🏢 Company Master Configuration

SMRITI reads company profiles directly from the backend transaction engine. To set up your company:
1. Open the master settings area.
2. Verify that your core corporate record is present.
3. Configure default settings:
   - **Company Name**: e.g., `Test PSV Company`
   - **Default Currency**: e.g., `INR`
   - **Default Holiday List**: Maps working schedules.

---

## 📈 Chart of Accounts & Cost Center Mappings

SMRITI processes sales and purchase journals against a unified ledger. Ensure the following accounts are mapped to prevent submission errors:

### 1. Cost Center Mapping
Create a primary cost center matching your physical store structure:
```text
Company Cost Center (Parent)
└── Store-01 Cost Center (Child)
└── Store-02 Cost Center (Child)
```
Assign these cost centers on all inventory receipts to isolate store-level profit and loss statements.

### 2. Default Accounts Mappings
Set default accounts in your Company record:
- **Default Bank Account**: For card and digital wallet settlements.
- **Default Cash Account**: For cash drawer settlements.
- **Cost of Goods Sold (COGS)**: For automatic stock valuation adjustments during checkout.
- **Income Account**: Default sales account (e.g. `Product Sales`).
- **Expenses Account**: Default purchase/adjustment account.

---

## 📍 Setting Local Parameters

Configure regional and operational settings in SMRITI Settings:
- **Default Tax Category**: Restricts tax calculations to local templates.
- **Rounding Method**: Set to `Round to Nearest Whole Number` for clean cash transactions at the POS.
- **Default Terms and Conditions**: Appended to all receipt formats.
