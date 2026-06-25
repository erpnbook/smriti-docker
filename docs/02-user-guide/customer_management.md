---
title: Customer Management
version: 1.0
last_updated: 2026-06-18
applies_to: SMRITI Retail OS v1.x
---

# SMRITI OS Customer Management Guide

This guide details managing customer records, configuring walk-in accounts, and establishing credit limits for retail accounts.

## 👤 Walk-In Customer Profiles

Every POS Profile must designate a default customer account to capture cash transactions where the buyer does not register contact info:
- **Naming**: Typically `Walk-in Customer` or `Default Retail Customer`.
- **Settings**: Must be marked as active and have `disabled = 0`.
- **Payment Method**: Generally restricted to immediate Cash, Card, or UPI settlements.
- **Ledger Entries**: Sales receipts are debited and credited instantly, leaving a zero balance on the customer's account.

---

## ➕ Creating New Customer Accounts

Cashiers can register new customers directly from the POS interface or managers can import them. To register a profile:
1. Navigate to the POS billing cart and click the `Customer` field.
2. Select **Create New Customer**.
3. Input customer fields:
   - **Customer Name**: Full corporate or individual name.
   - **Mobile Number**: Primary contact for digital receipt notifications.
   - **GSTIN**: Necessary if processing B2B sales invoices with tax credits.
   - **Customer Group**: Category (e.g. `Individual`, `Retail`, `Wholesale`).

---

## 💳 Customer Credit Limits

SMRITI allows billing transactions on account credit. To configure credit boundaries:
1. Open the Customer profile card.
2. Navigate to the **Credit Limits** section.
3. Configure the settings:
   - **Credit Limit**: Specify a maximum outstanding balance (e.g., Rs. 50,000).
   - **Bypass Rule**: System Manager permissions are required to submit POS invoices that push outstanding amounts past this threshold.
   - **Terms**: Set maximum credit days (e.g., `Net 30`) to flag aging customer bills in outstanding reports.
