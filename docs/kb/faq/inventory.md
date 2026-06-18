---
title: Inventory FAQ
version: 1.0
last_updated: 2026-06-18
applies_to: SMRITI Retail OS v1.x
---

# Frequently Asked Questions — Inventory Management

### Q1: Why is stock showing negative balances in my store warehouse?
**A**: SMRITI blocks negative stock checkout in POS by default. However, if back-office sales or manual Stock Entries are submitted with stock updates enabled when physical quantities have not yet been received in the system (e.g. GRN pending), the database ledger will register a negative balance. Ensure all Purchase Receipts are submitted before physical sales checkouts.

### Q2: How do I transfer stock between warehouses?
**A**:
1. Open the inventory management screen and select **Stock Entry**.
2. Set the purpose to **Material Transfer**.
3. Define the **Source Warehouse** and **Target Warehouse**.
4. Add the items and quantities.
5. Click **Submit** (requires SMRITI Store Manager or System Manager roles).

### Q3: How often are the stock aging snapshots recalculated?
**A**: Stock aging snapshots are generated incrementally using background tasks. Recalculation runs during off-peak hours as defined in PSV System Settings to prevent database locking during high-traffic store hours.

### Q4: What happens to negative entries in the FIFO aging calculation?
**A**: Negative ledger entries (representing sales and stock outflows) consume stock using FIFO logic. The aging engine only scans positive ledger entries (like Purchase Receipts or Stock Receipts) to trace the origin date of the remaining balance.

### Q5: Can I exclude a showroom warehouse from stock redistribution?
**A**: Yes. Open the Warehouse settings card or navigate to SMRITI PSV settings. Add the target warehouse to the **Redistribution Exclusions** list. The engine will skip this warehouse, preventing suggested transfers from targeting its display stock.
