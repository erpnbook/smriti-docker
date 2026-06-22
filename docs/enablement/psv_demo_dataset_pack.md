# SMRITI PSV Demo Dataset Pack — Scenario & Business Guide

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

## 1. Business Narrative & Objectives
To deliver a repeatable, high-impact demonstration of SMRITI Party Stock Visibility (PSV), this dataset maps three distinct distributor scenarios in Maharashtra (Mumbai, Pune, Nashik).

The dataset is engineered to show:
1.  **Mumbai Depot (The Excess Stock Scenario)**: High inventory levels of slow-moving size curves, locking up capital.
2.  **Pune Depot (The Stockout Risk Scenario)**: Rapid checkouts leading to depletion of standard sizes (S and M).
3.  **Nashik Depot (The Dead Stock Scenario)**: Seasonal variant lines sitting stagnant for over 90 days.

---

## 2. Depot Scenario Breakdowns

### Scenario A: Mumbai Depot (Surplus & Capital Lockup)
*   **Context**: Mumbai is the largest regional distributor, but suffers from poor reorder governance.
*   **Data Highlights**:
    *   Surplus units of Denim size 32 (surplus of 120 units).
    *   WOC stands at a bloated **35 weeks** (Green zone target is 7–14 weeks).
    *   Working Capital locked: **₹4,50,000** on Denim variants alone.
*   **Demo Action**: Planners view this excess on the dashboard and verify that Mumbai does not need replenishment from the factory.

### Scenario B: Pune Depot (High Velocity & Stockout Risk)
*   **Context**: Pune is experiencing rapid sales velocity, but has received no recent dispatches.
*   **Data Highlights**:
    *   Standard sizes of Sneakers are at **0 units** in stock.
    *   WOC is at **0 weeks** (Action Zone).
    *   Lost sales opportunity is growing daily.
*   **Demo Action**: Run the **Network Stock Transfer Simulator** to re-route Mumbai's surplus to Pune.

### Scenario C: Nashik Depot (Dead Stock Exposure)
*   **Context**: Nashik received a large shipment of Graphic Tees 95 days ago that has failed to rotate.
*   **Data Highlights**:
    *   Stock quantity: 380 units.
    *   Sales velocity: 1 unit/week.
    *   Aging profile: 100% in the **90+ Days (Dead)** band.
*   **Demo Action**: Run a targeted clearance markdown campaign or schedule returns.

---

## 3. Repeatable Demo Flow

Planners can execute this demo sequence step-by-step:

### Step 1: Open the PSV Dashboard
*   *Expected View*: Mumbai shows high stock, Pune shows red alerts, Nashik shows poor freshness.
*   *Screenshot Marker*: `[Screenshot: PSV Dashboard Depot Comparison]`

### Step 2: Reorder Suggestion
*   *Expected View*: SMRITI filters out Mumbai but triggers a "Critical Replenishment Alert" for Pune.
*   *Screenshot Marker*: `[Screenshot: Reorder Recommendation List]`

### Step 3: Run the Stock Transfer Simulator
*   *Expected View*: Suggests moving 100 units from Mumbai (120 surplus) to Pune (0 stock).
*   *Screenshot Marker*: `[Screenshot: Inter-Store Transfer Approval Matrix]`

### Step 4: Verify ROI Recovery
*   *Expected View*: The calculator computes ₹60,000 in protected margins for Pune, and frees ₹1,50,000 in locked capital for Mumbai.
*   *Screenshot Marker*: `[Screenshot: Margin Recovery Analytics Page]`

---

## 4. Dataset Reference Files
*   **CSV File**: [psv_demo_dataset.csv](file:///d:/Smriti_Retail_OS/docs/enablement/psv_demo_dataset.csv)
*   **Layout Guide**: [psv_demo_dataset_layout.md](file:///d:/Smriti_Retail_OS/docs/enablement/psv_demo_dataset_layout.md)

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
