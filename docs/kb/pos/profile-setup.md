---
title: POS Profile Setup
version: 1.0
last_updated: 2026-06-18
applies_to: SMRITI Retail OS v1.x
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
