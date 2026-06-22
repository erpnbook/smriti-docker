# SMRITI PSV Demo Dataset — Layout & Field Guide

---

### Author Profile (Start)
- **Author**: Jawahar R. Mallah
- **Designation**: Founder & Chief Architect
- **Organization**: AITDL – AI Technology & Development Lab
- **Professional Experience**: 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.

> "Light begins with learning."
> 
> — Jawahar R. Mallah
> Founder & Chief Architect, AITDL

---

## 1. Document Schema & Excel Column Mapping

When distributors upload spreadsheets or CRM exports via the SMRITI portal, the file structure must map directly to the SMRITI PSV Transaction schema:

| Excel Header | DB Field | Data Type | Sample Value | Business Meaning |
| :--- | :--- | :--- | :--- | :--- |
| **Transaction Date** | `posting_date` | Date | `2026-06-23` | Date the sales/dispatches were recorded. |
| **Distributor ID** | `party_stock_account` | Link | `DIST-MUM-01` | Unique SMRITI Party Stock Account ID. |
| **Distributor Name** | `customer_name` | Read-only | `Mumbai Depot` | Mapped ERPNext Customer name. |
| **Location** | `territory` | Read-only | `Mumbai` | Mapped ERPNext Customer location. |
| **SKU Code** | `item_code` | Link | `DNM-BLU-32` | Standard SMRITI/ERPNext SKU ID. |
| **Variant Size** | `variant_size` | Data | `Size 32` | Product size parameter (e.g. Size 32). |
| **Color** | `color` | Data | `Blue` | Product color parameter (e.g. Blue). |
| **Landed Cost** | `valuation_rate` | Currency | `600.00` | Landed Cost used for Capital Locked math. |
| **MRP** | `price_list_rate` | Currency | `1500.00` | Maximum Retail Price. |
| **Opening Balance**| `opening_qty` | Float | `200.0` | Initial stock level at the start of period. |
| **Primary Dispatch Qty**|`primary_in` | Float | `500.0` | Inward dispatches from Brand Warehouse. |
| **Secondary Sales Qty**|`secondary_out`| Float | `80.0` | Consumer sales checked out at retail register. |
| **Adjustments Qty** | `adjustment_qty`| Float | `-50.0` | Variances found during physical snapshots. |
| **Closing Balance** | `closing_qty` | Float | `620.0` | System-computed end-period inventory level. |

---

## 2. Calculated Metric Fields (UI Layer)

The following metrics are derived dynamically from the dataset using central formulas defined in the SMRITI PSV Formula Registry:

### A. Sales Velocity (Daily)
*   **Formula ID**: `PSV-VEL-001`
*   **Worked Math**: `Secondary Sales Qty / Days in Lookback Window`
*   *Example*: `80 / 32 = 2.5 units/day`

### B. Weeks of Cover (WOC)
*   **Formula ID**: `PSV-WOC-001`
*   **Worked Math**: `Closing Balance / (Sales Velocity * 7)`
*   *Example*: `620 / (2.5 * 7) = 620 / 17.5 = 35.4 Weeks`

### C. Aging Status
*   **Formula ID**: `PSV-AGE-001`
*   *Fresh*: Stock received under 30 days.
*   *Active*: Stock received 31–60 days.
*   *Aging*: Stock received 61–90 days.
*   *Dead Stock*: Stock received over 90 days.

---

### Author Profile (End)
- **Author**: Jawahar R. Mallah
- **Designation**: Founder & Chief Architect
- **Organization**: AITDL – AI Technology & Development Lab
- **Professional Experience**: 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.

> "Light begins with learning."
> 
> — Jawahar R. Mallah
> Founder & Chief Architect, AITDL

---
*SMRITI Retail OS Enablement Suite | AITDL Network*
