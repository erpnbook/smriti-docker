---
Document ID: "ADMIN-009"
Title: "SMRITI OS POS Profile Setup Guide"
Owner: "Administration Team"
Audience: "Administrator"
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

# SMRITI OS POS Profile Setup Guide

This guide details creating and configuring SMRITI POS Profiles, linking payment modes, and setting up cashier-to-store mapping rules.

## 🛠️ Creating a POS Profile

A POS Profile governs billing terminal rules for a specific checkout lane or store. To create a profile:
1. Open the POS configuration interface.
2. Select your Company and click **New POS Profile**.
3. Name the profile descriptively (e.g. `Store 01 - Express lane`).
4. Set core operational settings:
   - **Warehouse**: The default stock source (e.g. `Store 01 - Main`).
   - **Selling Price List**: The default price source (e.g. `Standard Selling`).
   - **Customer**: Fallback walk-in customer (e.g. `Walk-in Customer`).

---

## 💳 Payment Modes Configuration

SMRITI POS terminals support split-payment checkouts. Map active payment methods under the **Payments** table in the POS Profile:

| Payment Method | Account | Mode Type |
| :--- | :--- | :--- |
| **Cash** | Cash Account | Cash |
| **Credit Card** | Bank Account | Card |
| **UPI / Wallet** | Wallet Clearing Account | Phone / Online |
| **Store Credit** | Customer Outstanding | Credit |

*Note: Ensure each payment method is linked to an active Chart of Accounts ledger to avoid journal submission failures during cashier shift closures.*

---

## 👥 Cashier & User Mapping

To prevent cashiers from opening unauthorized terminals, POS profiles enforce explicit user mapping:
- **Cashier Table**: Add cashier user accounts to the profile's authorized users list.
- **Single-Open Constraint**: A cashier can only have one active shift open on a single POS profile at any time.
- **Store-level Restrictions**: Restrict POS warehouse choices to ensure cashiers cannot select stock bins belonging to other geographic regions.

## 📝 Worked Example Configuration

Below is a complete configuration payload example for an Express Checkout lane, representing how the POS Profile document is structured and saved:

```json
{
  "doctype": "POS Profile",
  "name": "Store 01 - Express Lane 01",
  "company": "SMRITI Retail India Private Limited",
  "warehouse": "Store 01 - Main - SRIPL",
  "selling_price_list": "Standard Selling",
  "currency": "INR",
  "write_off_account": "Temporary Write Off Account - SRIPL",
  "write_off_cost_center": "Main Cost Center - SRIPL",
  "payments": [
    {
      "mode_of_payment": "Cash",
      "default_account": "Cash - SRIPL",
      "default": 1
    },
    {
      "mode_of_payment": "UPI / GPay",
      "default_account": "UPI Clearing - SRIPL",
      "default": 0
    },
    {
      "mode_of_payment": "Credit Card",
      "default_account": "HDFC Card Clearing - SRIPL",
      "default": 0
    }
  ],
  "applicable_for_users": [
    {
      "user": "cashier01@smriti.local"
    },
    {
      "user": "cashier02@smriti.local"
    }
  ]
}
```

### Configuration Parameters Explained:
1. **`warehouse`**: Dictates that all sales transactions on this terminal default to deducting inventory from `Store 01 - Main - SRIPL`.
2. **`selling_price_list`**: Validates prices directly against the Standard Selling catalog.
3. **`payments`**: Maps specific payment modes to clearing accounts. UPI transactions clear through the `UPI Clearing` account rather than standard bank or cash ledgers.
4. **`applicable_for_users`**: Ensures only `cashier01@smriti.local` and `cashier02@smriti.local` are authenticated to boot this profile.

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