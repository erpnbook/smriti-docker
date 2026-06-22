# SMRITI Retail OS — PSV Executive One-Pager
## SMRITI Inventory Visibility Intelligence Center (PSV)

---

### About This Document & Author Profile

- **Author**: Jawahar R. Mallah
- **Designation**: Founder & Chief Architect
- **Organization**: AITDL – AI Technology & Development Lab
- **Professional Experience**: 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.
- **Author Note**: This document is based on practical field experience gathered across retail operations, distribution management, inventory control, software architecture, business automation, and enterprise solution development. The objective is to make SMRITI Retail OS understandable and usable by both technical and non-technical users.

> "Light begins with learning."
> 
> — Jawahar R. Mallah
> Founder & Chief Architect, AITDL

#### Document Metadata
- **Documentation Version**: 1.0.0
- **Release Date**: 2026-06-23
- **Intended Audience**: CEO, Owner, Distributor Director, Sales Head
- **Learning Objectives**: Understand the core capability, KPIs, ROI calculations, and business value of SMRITI Party Stock Visibility (PSV).
- **Contact / Support Section**: [support@erpnbook.com](mailto:support@erpnbook.com)
- **Revision History**: 
  - `v1.0.0` (2026-06-23) - Initial Release by Jawahar R. Mallah.

---

## 1. What is PSV? (Party Stock Visibility)
SMRITI Party Stock Visibility (PSV) is a premium, real-time retail operational layer built on top of ERPNext. While ERPNext serves as the transaction and general ledger engine of record, SMRITI PSV acts as the intelligence frontend and experience layer that tracks distributor inventory, sales velocity, and coverage.

PSV maintains an independent **Inventory Visibility Layer** that reads ERPNext master data but operates on its own isolated stock movement log. This guarantees that company ledger entries are never modified by distributor uploads, while offering the brand full visibility into stock status across all external channel partners (footwear brands, FMCG networks, franchise outlets, etc.).

---

## 2. Why Brands Need PSV: The Distribution Visibility Gap
Traditional brands sell to distributors or franchise stores, losing sight of the inventory once it leaves the primary warehouse. This creates the **Distribution Visibility Gap**:
* **The Stockout Trap**: Brands do not know when a distributor runs out of a popular item, leading to lost sales and brand dilution.
* **The Dead Stock Trap**: Low-velocity items accumulate at distributor locations, locking up capital and leading to forced discounts or return claims.
* **Fulfillment Delays**: Orders are placed reactively without lead-time analysis, stalling supply chain efficiency.

SMRITI PSV closes this gap by providing an end-to-end, multi-store distributor visibility network.

---

## 3. Executive Dashboard Snapshot

| KPI | Meaning |
| :--- | :--- |
| **Weeks of Cover** | How long inventory will last |
| **Sell-Through %** | How quickly products move |
| **Capital Locked** | Money trapped in inventory |
| **Inventory Freshness** | Aging health of stock |

---

## 4. Top 4 Core KPIs

### A. Weeks of Cover (WOC)
* **Business Meaning**: Measures how many weeks the current distributor stock will last based on recent sales velocity.
* **Formula**: 
  $$\text{WOC} = \frac{\text{Current Shadow Balance}}{\text{Sales Velocity (Daily Average)} \times 7}$$
* **Worked Example**: If a distributor has 140 units of a variant in stock, and the daily sales average over the last 4 weeks is 2 units:
  $$\text{Sales Velocity} = 2.0 \text{ units/day}$$
  $$\text{WOC} = \frac{140}{2 \times 7} = \frac{140}{14} = 10.0 \text{ Weeks of Cover}$$
* **Interpretation**: WOC < 3 is **Critical** (reorder immediately), WOC < 7 is **Warning** (monitor closely), WOC 7–14 is **Healthy**.

### B. Sell-Through %
* **Business Meaning**: The percentage of dispatched inventory sold by the distributor to end-users during a period.
* **Formula**:
  $$\text{Sell-Through \%} = \left( \frac{\text{Quantity Sold}}{\text{Quantity Dispatched}} \right) \times 100$$
* **Worked Example**: If a brand dispatches 1,000 units to a partner, and the partner sells 750 units:
  $$\text{Sell-Through \%} = \left( \frac{750}{1,000} \right) \times 100 = 75.0\%$$

### C. Capital Locked / Capital Efficiency
* **Business Meaning**: The amount of capital tied up in slow-moving or Dead Stock at distributor locations.
* **Formula**:
  $$\text{Capital Locked} = \text{Slow-Moving Stock Qty} \times \text{Landed Cost / Standard Rate}$$

### D. Inventory Freshness & Aging
* **Business Meaning**: Segregates stock by age (0-30, 31-60, 61-90, 90+ days) since dispatch to identify aging blockages early.

---

## 5. Top Dashboards & Workflows
* **Distributor Sell-Through Tracker**: Real-time sales data import via automated templates or POS integrations.
* **Reorder & Replenishment Intelligence**: Automatically calculates recommended quantities based on lead time, safety stock, and maximum caps, categorized by Priority (Critical, High, Medium, Low).
* **Exception Monitoring Center**: Flags negative shadow balances, inventory variances, and upload discrepancies.
* **Network Stock Transfer (NST)**: Suggests stock relocations from over-stocked distributor locations to under-stocked locations, maximizing brand-level margins.

---

## 6. Distribution ROI Calculator (Worked Example)
Implementing SMRITI PSV directly impacts the distributor's Return on Investment (ROI) by optimizing inventory capital.

### Baseline (Without PSV):
* **Distributor Capital Invested**: 20,00,000 INR
* **Dead Stock (Over 90 Days)**: 8,00,000 INR (40% of capital locked)
* **Annual Sales Revenue**: 40,00,000 INR
* **Net Margin**: 10% (4,00,000 INR profit)
* **Distributor ROI**: 
  $$\text{ROI} = \left( \frac{4,00,000}{20,00,000} \right) \times 100 = 20.0\%$$

### Post-PSV Optimization:
* **Dead Stock Reduced by 50%**: 4,00,000 INR freed from slow-moving stock.
* **Reinvested Capital**: The freed 4,00,000 INR is reallocated to high-velocity, high-demand styles.
* **Incremental Revenue**: Reinvested capital generates an additional 12,00,000 INR in sales.
* **New Sales Revenue**: 52,00,000 INR
* **New Net Margin Profit**: 10% (5,20,000 INR profit)
* **New Distributor ROI**:
  $$\text{New ROI} = \left( \frac{5,20,000}{20,00,000} \right) \times 100 = 26.0\%$$
* **Impact**: Distributor ROI increases from **20% to 26%** while total brand sales volume grows by **30%** without increasing capital exposure.

---

## 7. Frequently Asked Questions (FAQs)

#### Q1: Does SMRITI PSV touch our core financial accounting?
**A**: No. SMRITI PSV operates as a frontend **Inventory Visibility Layer**. It reads ERPNext data but never inserts or modifies stock ledger entries or general ledger entries in ERPNext. Accounting remains 100% owned by ERPNext/Tally.

#### Q2: How does the system handle concurrent sales uploads?
**A**: SMRITI PSV contains a Redis-backed distributed lock scoped per Party Stock Account. This prevents double-writes and race conditions during concurrent loads, ensuring data and audit trail integrity.

#### Q3: Can a distributor reimport the same file twice?
**A**: No. The system generates an MD5 checksum fingerprint of the uploaded file. If the file hash already exists, the upload is rejected automatically.

---

### Author Profile & Closing Note

- **Author**: Jawahar R. Mallah
- **Designation**: Founder & Chief Architect
- **Organization**: AITDL – AI Technology & Development Lab
- **Professional Experience**: 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.

> "Light begins with learning."
> 
> — Jawahar R. Mallah
> Founder & Chief Architect, AITDL
