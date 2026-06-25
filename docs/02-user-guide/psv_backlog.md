# SMRITI Retail OS — PSV Phase 1.3 Backlog

This backlog documents all deferred enhancement requests, analytical models, and feature expansions scheduled for **PSV Phase 1.3** following the official freezing of **PSV Phase 1.2** on **2026-06-11**.

---

## 1. Deferred Analytical & Intelligence Features

### A. Coverage Days & Inventory Aging
- **Coverage Days (Weeks of Cover Expansion)**: Transition from weekly stock cover metrics to daily dynamic sales velocity forecasting and cover-day alerts.
- **Inventory Aging Intelligence**: Real-time age bucketing based on FIFO ledger allocation, integrating stock aging snapshots with actual sales speed to identify high-risk aging stock.

### B. Financial & Capital Analysis
- **Capital Locked Analysis**: Calculate and visualize the absolute cost of capital tied up in dead stock, slow-movers, and over-allocated channels. Integrate with ERPNext landing cost to show true working capital impact.

### C. Automated Replenishment & Purchasing
- **Reorder Engine**: Build an automated trigger-based replenishment engine that monitors distributor stock levels against localized lead times.
- **Purchase Suggestions**: Generate automatic purchase orders in ERPNext from SMRITI’s PSV recommendations, routing them through approval layers without manual entry.

### D. Exceptions & Recovery
- **Dead Stock Recovery Intelligence**: Automate targeted promotions, inter-store redistribution suggestions, and clearance campaigns to liquidate items classified as "Slow Movers".

---

## 2. Feedback & Pilot Phase Tracking
- **Pilot Distributor Testing**: Track pilot run feedback from active footwear distributors.
- **Usage Analytics**: Capture user interactions on Widget 12, modal clicks, and exports to optimize user flow.
