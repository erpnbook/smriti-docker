---
title: Warehouse Setup Guide
version: 1.0
last_updated: 2026-06-18
applies_to: SMRITI Retail OS v1.x
---

# SMRITI OS Warehouse Setup Guide

This guide details configuring SMRITI Retail OS warehouse structures, managing parent-child hierarchies, and setting up warehouses for physical stock audits.

## 🗂️ Warehouse Structure Hierarchy

SMRITI organizes storage facilities using tree-structured hierarchies. This organizes stock consolidation while enabling store-specific transactions:

```text
All Warehouses (Root Group)
└── Store Warehouses (Group)
    ├── Store-01 (Store Warehouse)
    └── Store-02 (Store Warehouse)
└── Central Warehouses (Group)
    ├── Transit Warehouse (Standard)
    └── Returns Warehouse (Standard)
```

- **Group Warehouses**: Cannot hold stock directly. Used purely for aggregating child balances (e.g. `Store Warehouses` group).
- **Standard Warehouses**: Active stock storage points. All actual inventory transactions (Receipts, Transfers, Invoices) target standard warehouses.

---

## ⚙️ Configuring Store Warehouses

When setting up a store warehouse in SMRITI:
1. Navigate to **Masters** → **Warehouse Master**.
2. Create a new warehouse.
3. Configure settings:
   - **Warehouse Name**: Use a descriptive name (e.g. `Store 01 - Main`).
   - **Parent Warehouse**: Select the matching group warehouse.
   - **Account**: Associate a dedicated Stock Ledger account (enables automatic stock value mapping).

---

## 🔍 Stock Audit & Counting Scopes

Under SMRITI's inventory-first constitution, physical stock checks verify system ledger balances. To set up a warehouse for audits:
- **Active Scopes**: Ensure the target warehouse is marked as `Active` to allow selection in the Stock Audit page (`/app/stock-audit`).
- **Showroom vs Storage Exclusions**: You can flag secondary storage locations or transit warehouses to exclude them from the SMRITI Redistribution Engine scan, preventing suggestions from targeting closed storage bins.
- **Parent Consolidations**: When running the SMRITI Current Stock Position report, selecting a group warehouse (like `Store Warehouses`) automatically sums balances of all children, simplifying regional analysis.
