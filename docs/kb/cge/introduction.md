---
title: Customer Growth Engine (CGE)
version: 1.0
last_updated: 2026-06-18
applies_to: SMRITI Retail OS v1.x
---

# SMRITI Customer Growth Engine (CGE) — Introduction

The **SMRITI Customer Growth Engine (CGE)** is a high-performance marketing, loyalty, and customer retention layer built directly on top of ERPNext. It extends ERPNext's transaction engine by providing store owners, managers, and marketing heads with a unified control system for loyalty points, coupon budgets, and promotional wallet balances.

---

## 🏛️ Architecture & Core Modules

SMRITI CGE v1.0 consists of four major functional areas:

```
                  ┌───────────────────────────────┐
                  │          SMRITI UI            │
                  └───────────────┬───────────────┘
                                  │
                  ┌───────────────▼───────────────┐
                  │       CGERuleEvaluator        │
                  └──────┬────────┬────────┬──────┘
                         │        │        │
         ┌───────────────┘        │        └───────────────┐
 ┌───────▼───────┐        ┌───────▼───────┐        ┌───────▼───────┐
 │ Loyalty Rules │        │ Coupon Budget │        │    Cashback   │
 │   & Tiers     │        │  Reservation  │        │ Double-Entry  │
 └───────────────┘        └───────────────┘        └───────────────┘
```

1. **Loyalty Engine**: Auto-resolves customer point multipliers based on customer tier definitions and priority-based item rules (Brand, Group, Style, Season, Store, Customer Group, Tier).
2. **Coupon Campaign Manager**: Controls budget reservations during checkouts, preventing over-consumption of marketing budgets.
3. **Cashback Wallet Ledger**: Manages promotional cashback balances with strict audit logs and double-entry accounting in ERPNext.
4. **Liability Snapshot Engine**: Tracks outstanding cashback and loyalty points exposure nightly for financial audits.

---

## 🛡️ Rule 8 Compliance (System of Record Boundary)

As a core directive of the SMRITI Retail OS architecture, **SMRITI CGE does not duplicate or replace ERPNext master data or transaction structures**:
- **System of Record**: ERPNext remains the absolute owner of Customers, Items, Coupon Codes, Sales Invoices, and General Ledger (GL) entries.
- **Extension Layer**: SMRITI CGE adds custom attributes and validation hooks to standard DocTypes, running evaluation pipelines during checkout, but commits financial liability records directly into the ERPNext GL via double-entry Journal Vouchers.
- **Zero Shadow Master Tables**: Customer points are aggregated from `tabLoyalty Point Entry`. All coupons are validated against standard `tabCoupon Code`.

---

## 🚀 Performance Targets

To support fast-paced checkout lanes, SMRITI CGE is architected for sub-second execution:
- **Promotion matching**: `< 50ms`
- **Coupon validation**: `< 50ms`
- **Loyalty resolution**: `< 50ms`
- **Total evaluation overhead**: `< 200ms`
