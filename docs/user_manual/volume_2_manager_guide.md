# SMRITI Retail OS User Manual — Volume 2: Manager & Supervisor Guide

---

### Author Profile (Start)
* **Author**: Jawahar R. Mallah
* **Designation**: Founder & Chief Architect
* **Organization**: AITDL – AI Technology & Development Lab
* **Professional Experience**: 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.

#### Author Note
This manual is based on practical field experience gathered across retail operations, distribution management, inventory control, software architecture, business automation, and enterprise solution development. The objective is to make SMRITI Retail OS understandable and usable by both technical and non-technical users.

> "Light begins with learning."
> 
> — Jawahar R. Mallah
> Founder & Chief Architect, AITDL

#### Document Metadata
* **Document Version**: 1.2.0
* **Release Date**: 2026-06-22
* **Intended Audience**: Sales Managers, Distributor Supervisors, Audit Leads, and Store Owners
* **Learning Objectives**: Understand rebalancing recommendations, manual audit variance reconciliations, landed cost shadow allocations, customer intelligence graph settings, and data-center reporting governance rules.
* **Support**: support@aitdl.example.com
* **Revision History**:
  * `v1.0.0` (2026-06-20): Initial manager guide guidelines.
  * `v1.1.0` (2026-06-22): Integrated Landed Cost shadow-ledger rules and Reporting Governance.
  * `v1.2.0` (2026-06-22): Integrated Customer Intelligence Graph (CIG) governance and Clienteling settings.

---

## Chapter 1: Audit & Variance Management (ऑडिट और विसंगति प्रबंधन)

### 1. Purpose (उद्देश्य)
The **Audit & Variance Management** module automatically reconciles physical counts (from [Physical Snapshots](dictionary:Physical Snapshot)) with the SMRITI shadow ledger. 
- **Business Problem Solved**: Identifying stock shrinkage (चोरी या खोया हुआ स्टॉक) and posting ledger correction entries to align system balances.

### 2. Real-Life Example (वास्तविक जीवन का उदाहरण)
At **Pune Plaza Footwear**, the SMRITI system records `Flyrunner-Blue-8` stock as **50 pairs**. 
During the monthly audit, the physical count is verified as **45 pairs**. SMRITI registers a **negative variance of 5 pairs** (₹12,495 retail value).

### 3. Step-by-Step Entry/Reconciliation Process (प्रक्रिया)
1. **Menu Path**: SMRITI Home → Operations → Audit Console → **Reconciliation Sheet**
2. **Select Parameters**: Select the target [PSA](dictionary:PSA) and the audit date.
3. **Analyze Variance**: The screen will highlight rows with differences in red.
4. **Approve Adjustments**: The supervisor selects the reconciliation reason code (e.g. `THEFT`, `DAMAGE`, `DATA_ENTRY_ERROR`) and clicks **Approve & Adjust Ledger**.

[Screenshot: Audit Variance Console]

### 4. Field-by-Field Explanation (फील्ड स्पष्टीकरण)

| Field Name | Type | Mandatory? | Simple Explanation | Example Value |
| :--- | :--- | :--- | :--- | :--- |
| **Audit Doc ID** | Link | **Yes** | Link to the submitted Physical Snapshot. | `AUD-2026-004` |
| **System Qty** | Float | Read-only | Expected stock quantity in the shadow ledger. | `50.0` |
| **Physical Qty** | Float | Read-only | Counted stock quantity. | `45.0` |
| **Variance Qty** | Float | Read-only | Difference (Physical Qty - System Qty). | `-5.0` |
| **Reconciliation Reason** | Select | **Yes** | Reason code for the difference. | `THEFT` |
| **Supervisor Notes** | Long Text | No | Remarks explaining the audit outcome. | `CCTV footage requested.` |

### 5. Example Transaction (उदाहरण प्रविष्टि)
- **Store**: `Pune Plaza Footwear`
- **Item**: `Flyrunner-Blue-8`
- **Variance**: `-5`
- **Approved Reason**: `DAMAGE`
- **Expected Output**: SMRITI adjusts the shadow ledger balance to 45.0 and logs a "SMRITI Liability Snapshot" record.

### 6. Reports & Analysis (रिपोर्ट और विश्लेषण)
- **Report Name**: **Store Shrinkage & Variance Summary**
- **How to Read**: Displays total stock variance percentage for each store.
- **Action**: Any outlet showing variance greater than 3% requires a manager audit.

### 7. Common Mistakes (सामान्य गलतियां)
- **Adjusting ledger without checking pending invoices**: Adjusting a negative variance of 10 units when a delivery truck containing 10 units is still unloading at the dock.
- *How to Fix*: Ensure all pending delivery notes and sales uploads are submitted before approving audits.

### 8. Business Interpretation (व्यावसायिक व्याख्या)
- **Warning Sign**: Recurrent small positive variances followed by negative variances. This suggests store operators are logging fake audits to hide sales.

### 9. Frequently Asked Questions (FAQs)
1. **Can I undo a variance adjustment?**
   - No, once submitted. You must submit a fresh audit snapshot to correct it.
2. [Remaining FAQs in Volume 4]

### 10. Troubleshooting (समस्या निवारण)
- **Error**: `Cannot submit. Pending transactions exist for this PSA`.
- **Resolution**: Go to SMRITI Dashboard, check for unsubmitted Sales Uploads or Delivery Notes for this [PSA](dictionary:PSA), submit them, and retry the audit approval.

---

## Chapter 2: Transfer Recommendation (स्टॉक ट्रांसफर सुझाव)

### 1. Purpose (उद्देश्य)
The **Transfer Recommendation** module optimizes inventory distribution across outlets. It calculates when an overstocked store should transfer items to a stock-out store.
- **Business Problem Solved**: Prevents lost sales at one store while another store holds [dead stock](dictionary:Dead Stock). It computes the [Transfer Benefit Score](formula:TRF-001) to ensure freight and delay costs do not exceed the transfer benefit.

### 2. Real-Life Example (वास्तविक जीवन का उदाहरण)
- **Mumbai Showroom** has **0 stock** of `Flyrunner-Blue-8` and sells 3 pairs a day. ([Stockout Risk](dictionary:Stockout Risk) = High).
- **Pune Showroom** has **50 pairs** of `Flyrunner-Blue-8` and sells only 0.2 pairs a day. (Overstock = High).
- SMRITI calculates the transfer economics and recommends shifting 20 pairs from Pune to Mumbai.

### 3. Step-by-Step Process (प्रक्रिया)
1. **Menu Path**: SMRITI Home → Inventory → Transfer Recommendations
2. **Review Recommendations**: The system displays suggested transfers.
3. **Approve Transfer**: Click **Create Stock Transfer** (स्टॉक ट्रांसफर बनाएं) to auto-generate the transfer request.

[Screenshot: Stock Transfer Recommendation list]

### 4. Calculation Explanation (गणना स्पष्टीकरण)
The economic model checks:
$$\text{Transfer Benefit Score} = (\text{Item Retail Price} - \text{Freight Cost} - \text{Transit Delay Penalty}) \times \text{Transfer Qty}$$
- **Same Zone (e.g. West to West)**: Freight = ₹6.0, Delay Penalty = ₹5.0 per unit.
- **Different Zone (e.g. West to North)**: Freight = ₹18.0, Delay Penalty = ₹20.0 per unit.
- **Example calculation**:
  - Item Price = ₹2,499. Transfer Qty = 20 pairs.
  - Same Zone: Benefit = $(2499 - 6.0 - 5.0) \times 20 = 2488 \times 20 = \text{₹49,760}$ (Highly recommended!).

### 5. Example Recommendation (उदाहरण सुझाव)
- **Source**: `Pune Plaza Footwear`
- **Target**: `Mumbai Grand Mall`
- **Item**: `SF-FLY-BLU-8`
- **Quantity**: `20`
- **Reason Code**: `EXCESS_WOC_AT_SOURCE,POSITIVE_TRANSFER_BENEFIT`

### 6. Reports & Analysis (रिपोर्ट और विश्लेषण)
- **Report Name**: **Rebalancing Opportunity Log**
- **Action**: Check weekly recommendations and approve local transfers.

### 7. Common Mistakes (सामान्य गलतियां)
- **Ignoring transit delays**: Transferring seasonal items across distant zones (e.g., Mumbai to Delhi) during monsoon delays. SMRITI adjusts the score down to penalize cross-zone transit times.

### 8. Business Interpretation (व्यावसायिक व्याख्या)
- **Decision**: Approve transfer if the Benefit Score is positive. Reject if negative.

### 9. FAQs
1. **What is a Transit Delay Penalty?**
   - The cost of having inventory locked in transport, which makes it unavailable for sale during transit.

### 10. Troubleshooting (समस्या निवारण)
- **Error**: `No transfer recommended despite stockout`.
- **Resolution**: Check if neighboring stores have excess stock above their safety levels. If all stores are at or below safety stock, the system recommends a Purchase order instead.

---

## Chapter 3: Administration & Settings (प्रशासनिक सेटिंग्स)

### 1. Purpose (उद्देश्य)
This module allows administrators and supervisors to configure the global variables, reorder rules, and limits that govern SMRITI's predictive models.
- **Business Problem Solved**: Customizes SMRITI to fit your business lead times, safety margins, and forecasting parameters.

### 2. Real-Life Example (वास्तविक जीवन का उदाहरण)
During festival season (e.g., Diwali), supplier delivery times increase from **7 days** to **14 days**. The administrator updates the global [Lead Time](dictionary:Lead Time) settings to 14 days to prevent stockouts.

### 3. Step-by-Step Configuration Process (प्रक्रिया)
1. **Menu Path**: SMRITI Home → Administration → SMRITI PSV Settings
2. **Define Rules**: Create a `SMRITI PSV Reorder Rule` for specific item groups.
3. **Save**: Click Save. No server restarts are needed.

[Screenshot: SMRITI PSV Settings Page]

### 4. Field-by-Field Explanation (फील्ड स्पष्टीकरण)

| Field Name | Type | Mandatory? | Explanation | Example Value |
| :--- | :--- | :--- | :--- | :--- |
| **Default Lead Time Days** | Int | **Yes** | Time taken by supplier to deliver stock (in days). | `7` |
| **Default Safety Stock** | Float | **Yes** | Minimum stock buffer to keep at stores. | `15.0` |
| **Reorder Avg Weeks** | Int | **Yes** | Lookback window for [Sales Velocity](formula:INV-001) math. | `4` |
| **Forecast Model** | Select | **Yes** | Model used (Defaults to Exponential Moving Average). | [EMA](dictionary:EMA) |

### 5. Example Settings Configuration (उदाहरण प्रविष्टि)
- **Rule Scope**: Item Group = `Sports Shoes`
- **Lead Time**: `10`
- **Safety Stock**: `20.0`
- **Result**: All sports shoes will maintain a minimum safety buffer of 20 pairs.

### 6. Reports & Analysis (रिपोर्ट और विश्लेषण)
- **Report Name**: **Reorder Rule Registry**
- **Action**: Audit store reorder rules monthly to ensure safety stock levels align with updated sales trends and target [Inventory Turnover](formula:INV-004) ratios.

### 7. Common Mistakes (सामान्य गलतियां)
- **Setting excessive safety stock**: Setting a safety stock of 1000 pairs for a store that sells only 5 pairs a week. This locks up valuable capital.
- *How to Fix*: Check the store's average weekly sales before updating safety stock limits.

### 8. Business Interpretation (व्यावसायिक व्याख्या)
- **Decision**: Update target days cover to higher values for fast-moving items, and lower values for slow-moving fashion items.

### 9. FAQs
1. **Can store operators edit these settings?**
   - No. Only users with the "Administrator" or "System Manager" role have write access.

### 10. Troubleshooting (समस्या निवारण)
- **Error**: `Validation Error: Max Stock must be greater than Safety Stock`.
- **Resolution**: Set `max_stock` to a value higher than `safety_stock` in the reorder rule and click save.

---

## Chapter 4: Knowledge Governance Framework (KGF) (ज्ञान प्रशासन ढांचा)

### 1. Purpose (उद्देश्य)
The **Knowledge Governance Framework (KGF)** is the transparency and compliance engine of SMRITI. It ensures that every mathematical formula, forecast model, performance metric, or business KPI displayed to managers or cashiers is fully explainable and registered, preventing any "black-box" decision-making.
- **Business Problem Solved**: Eliminates confusion and builds trust by letting ground-level operators immediately understand *how* a value was calculated, *what* the value means for their daily operations, and *what actions* they must take next.

### 2. Real-Life Example (वास्तविक जीवन का उदाहरण)
A store manager at **Royal Pune Showroom** looks at their reorder report and sees a [Weeks of Cover (WOC)](formula:INV-002) metric of **1.5 weeks** for a popular running shoe variant. 
Instead of guessing how the 1.5 figure was arrived at, the manager clicks the **ⓘ Explain** icon next to the number. A clean modal pops up, showing:
- [WOC](dictionary:WOC) means the estimated weeks current stock will last.
- The mathematical formula: `current_stock / weekly_velocity`.
- A live worked example: `Current Stock = 30 pairs, Weekly Velocity = 20 pairs/week. WOC = 30 / 20 = 1.5`.
- A recommendation band showing that 1.5 is "Critical", advising the manager to immediately place a reorder.

### 3. Step-by-Step Process (प्रक्रिया)
1. **Explain any KPI**: Click the **ⓘ Explain** button next to any calculated metric on any SMRITI dashboard or report.
2. **Read the Explanation**: The Universal Explain Modal displays the business meaning, mathematical expression, data sources, worked example, and recommended action steps.
3. **Lookup Glossaries**: Click the **📖 Dictionary Entry** button inside the modal to navigate directly to the central **Business Dictionary** (/smriti-dictionary) to explore related terms (like [PDT](dictionary:PDT) or [PSA](dictionary:PSA)), Hinglish explanations, FAQs, and common mistakes.
4. **Manage Formulas (Admin/Managers)**: Go to **Help Desk → Formula Registry** (/smriti-formula-registry) to view, audit, or approve new mathematical formulas used across the platform.

### 4. Field-by-Field Explanation (SMRITI Formula Definition)

| Field Name | Type | Mandatory? | Simple Explanation | Example Value |
| :--- | :--- | :--- | :--- | :--- |
| **Formula ID** | Data | **Yes** | Unique identifier of the formula. | [INV-002](formula:INV-002) |
| **Formula Name** | Data | **Yes** | Human-readable name of the metric. | `Weeks of Cover` |
| **Formula Expression**| Data | **Yes** | Mathematical representation of the formula. | `current_stock / weekly_velocity` |
| **Business Meaning** | Long Text | **Yes** | What the metric measures in simple terms. | `How many weeks your stock will last.` |
| **Worked Example** | Long Text | **Yes** | Step-by-step arithmetic walk-through. | `30 / 20 = 1.5 weeks.` |
| **Interpretation Guide**| Long Text | **Yes** | Explanation of metric bands (Critical/Healthy).| `WOC < 2: Critical; WOC > 4: Overstock` |
| **Recommended Action**| Long Text | **Yes** | Concrete action for the operator. | `Place reorder immediately if Critical.` |

### 5. Example Registry Entry (उदाहरण प्रविष्टि)
- **Formula ID**: [INV-003](formula:INV-003)
- **Name**: [Dead Stock Score](dictionary:Dead Stock)
- **Expression**: `inactive_days * stock_value`
- **Worked Example**: `Inactive Days = 90 days. Stock Value = ₹10,000. Dead Stock Score = 90 * 10,000 = 900,000.`
- **Recommended Action**: If score > 500,000, mark for outlet rebalancing or discount clearance.

### 6. Reports & Analysis (रिपोर्ट और विश्लेषण)
- **Log Name**: **SMRITI PSV Activity Log**
- **How to Read**: Tracks all user accesses to formulas and dictionary terms. 
- **Action**: Look at the most frequently clicked explanations to identify which metrics require additional team training.

### 7. Common Mistakes (सामान्य गलतियां)
- **Deploying calculated metrics without registry entry**: Developers adding a new KPI to a custom report without creating a corresponding record in the central Formula Registry. The dashboard will block showing the metric or fail explainability audits.
- *How to Fix*: Always register the formula and obtain manager approval before enabling it on live dashboards.

### 8. Business Interpretation (व्यावसायिक व्याख्या)
- **Standard**: Every number shown to a store partner must have a clear business translation. "Numbers without explanations cause confusion; clear definitions drive faster action."

### 9. FAQs
1. **How is the explain modal so fast?**
   - The system utilizes Redis caching (key `smriti:explain:{formula_id}:{version}`) with a **1-hour TTL** to serve definitions in sub-milliseconds.
2. **Who can update dictionary definitions or formulas?**
   - Only AITDL Core Team members and chief administrators can approve changes, ensuring that business definitions remain standardized.

### 10. Troubleshooting (समस्या निवारण)
- **Error**: `Formula definition not found or is in Draft status`.
- **Resolution**: Open the Formula Registry, find the Formula ID, ensure the status is changed from `Draft` to `Approved` and `Is Active` is checked.

---

---

## Chapter 5: Landed Cost & Shadow Ledger Valuation (लागत और शैडो लेजर मूल्यांकन)

### 1. Purpose (उद्देश्य)
This module allows managers to perform **analytical shadow-ledger costing** for items without mutating the core accounting books or the official database inventory valuation (`valuation_rate`).
- **Business Problem Solved**: Merging additional purchasing costs (transport, handling, customs) directly into standard stock valuation creates tax reconciliation issues and alters audited company books. Shadow-ledger costing keeps the company accounting completely clean while allowing merchandising managers to evaluate correct gross margins.

### 2. Validation & Concurrency Rules (सत्यापन और समवर्ती नियम)
As a manager, you must understand the safety gates that SMRITI enforces:
1.  **Chronological Latest Costing (G2 Rule)**: On submission, SMRITI calculates the SKU's unit landed cost. It updates the `Item` master's `estimated_landed_cost_last` ONLY if this allocation is the chronologically newest submitted document. It checks `posting_date` first, and uses the `creation` timestamp as a tiebreaker.
2.  **Cancel Reversion Gate (G3 Rule)**: If you cancel an allocation, the system automatically runs a reversion query. It scans remaining submitted allocations to restore the chronologically newest active unit landed cost, or resets it to standard `valuation_rate` if no allocations remain. This prevents stale cost calculations.
3.  **Penny Discrepancy Rounding (G6 Rule)**: To prevent decimal penny leaks, SMRITI gathers rounding remainders per cost line and adds or subtracts them from the last active stock item row.
4.  **Strict Currency Match (G7 Rule)**: Foreign exchange conversions are disabled in Phase 1 to prevent currency rate manipulation risks. Referenced invoices must exactly match receipt currencies.

### 3. Explainable Metric Details (Rule 10 - DOC-01)
Here are the definitions and metrics registered for Landed Cost:

#### Unit Landed Cost (SMRITI-LND-COST-01)
- **Business Meaning**: The complete analytical unit cost of the item including purchase value and allocated auxiliary costs.
- **Formula**:
  $$\text{Unit Landed Cost} = \frac{\text{Base Value} + \text{Allocated Cost}}{\text{Qty}}$$
- **Worked Example**:
  - SKU `SF-FLY-BLU-8` Base Purchase Value = ₹20,000 (20 units @ ₹1,000).
  - Allocated Freight Cost = ₹400.
  - Quantity = 20 units.
  - $\text{Unit Landed Cost} = \frac{20000 + 400}{20} = \text{₹1,020.00}$.
- **Data Sources**: `tabSMRITI Allocation Audit Snapshot`, `tabPurchase Receipt Item`.
- **Interpretation Guide**:
  - Target: Should be within 5% to 15% of the base purchase rate. If it exceeds 20%, investigate transportation inefficiency.
- **Recommended Action**: Use this unit cost to set minimum retail prices (MRPs) and evaluate gross margins.

---

## Chapter 6: Reporting Governance & Security Center (रिपोर्टिंग शासन)

### 1. Purpose (उद्देश्य)
SMRITI implements the **Reporting Governance & Security Auditing** (ACP-REPORTS-001) framework to secure critical data lists, prevent cache leaks, and audit export events.

### 2. Core Governance Policies
1.  **Tenant Cache Partitioning (FRZ-REP-003)**: Redis caching for report queries is isolated per tenant. Cashiers or managers cannot see or intercept report caches from other stores.
2.  **Export Permission Precedence (FRZ-REP-004)**: When exporting report grids to CSV/Excel, user role permissions take precedence over report templates. SMRITI records all exports in the Activity Log with the operator's IP, username, and query hash.
3.  **Optimistic Concurrency Control (FRZ-REP-005)**: Prevents two managers from saving changes to the same report template at the same time by validating template checksums.
4.  **ⓘ Explain Transparency (Rule 10)**: Every report grid header contains an explain button. Clicking it displays live worked examples, SQL query paths, and business variables to ground-level users.

---

## Chapter 7: Sales Force Commission (SFC) Rules & Settlements (बिक्री बल आयोग नियम और बस्तियाँ)

### 1. Purpose (उद्देश्य)
Managers configure commission rules, track targets, and authorize monthly payouts for the sales team.

### 2. Core Policies
- **Rule Precedence Resolution**: SMRITI prioritizes specific employee override rules over company-wide defaults. Priority values determine which active rule takes precedence during target periods.
- **Adjustment Audit Trails**: All manual additions or deductions to a draft settlement must be recorded in the adjustments table, capturing the approving manager's name and timestamp.
- **Immutability Lock**: Approving or paying a settlement freezes the document and its audit logs from future edits, securing the financial state.

---

## Chapter 8: SMRITI Clienteling & Customer Intelligence Graph (CIG) (ग्राहक बुद्धिमत्ता आरेख)

### 1. Purpose (उद्देश्य)
The **SMRITI Customer Intelligence Graph (CIG)** framework integrates customer profiling, behavioral statistics, and predictive modeling into a unified experience layer. 
- **Business Problem Solved**: Eliminates rigid customer segmentation. CIG dynamically updates customer engagement, loyalty, and risk profiles in real-time, helping stores target customers with precision.

### 2. SMRITI Clienteling Settings
Managers govern CIG behavior and thresholds centrally via the **SMRITI Clienteling Settings** single DocType (/app/smriti-clienteling-settings) to prevent code modifications:
1.  **VIP Threshold (default `80.0`)**: The minimum candidate score required to mark a customer as VIP (`is_vip = 1`) on their profile.
2.  **Dormancy Days (default `90`)**: The number of days elapsed since the last checkout visit after which a customer is flagged as dormant.
3.  **Enable Predictions (default `1`)**: Turns on/off background predictive calculations for next-visit dates and purchase categories, protecting database performance when needed.

### 3. Dynamic Formula Registry Integration
Rather than hardcoding calculation logic in Python controllers, CIG retrieves mathematical expressions dynamically from the central Formula Registry. The intelligence engine evaluates three registered formulas:
- **Churn Risk Score (TST-CHURN)**: Measures the customer's likelihood of churning based on visit cycle deviation.
- **VIP Candidate Score (TST-VIP)**: Evaluates customer value based on spending (LTV), average basket value (ABV), and checkout count.
- **Campaign Affinity Score (TST-AFFINITY)**: Evaluates response touchpoints.

> [!NOTE]
> All customer profile calculations dynamically reference these Formula IDs (TST-CHURN, TST-VIP, TST-AFFINITY) from the Formula Registry. Refer to the Formula Registry (/app/smriti-formula-registry) to check the active version and expression.

### 4. Explainability-First (ⓘ Explain Workflow)
To comply with SMRITI explainability standards, the Clienteling Studio provides a clear transparency flow for counter operators:
1. Open the Customer Profile card.
2. Click the **ⓘ Explain** icon next to any computed metric.
3. The Universal Explain Modal retrieves the registered formula definition, resolves the customer's live transaction variables, and displays a step-by-step worked example.

---

## Support & Helpdesk
Thank you for using SMRITI Retail OS. For additional support, please contact the Helpdesk at **support@aitdl.com**.


---

### Author Profile (End)
* **Author**: Jawahar R. Mallah
* **Designation**: Founder & Chief Architect
* **Organization**: AITDL – AI Technology & Development Lab
* **Professional Experience**: 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.

> "Light begins with learning."
> 
> — Jawahar R. Mallah
> Founder & Chief Architect, AITDL
