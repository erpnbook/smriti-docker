# SMRITI PSV Executive FAQ (Top 25 CEO Questions)
## SMRITI Inventory Visibility Sales Enablement Suite

---

### Author Profile (Start)
- **Author**: Jawahar R. Mallah
- **Designation**: Founder & Chief Architect
- **Organization**: AITDL – AI Technology & Development Lab
- **Professional Experience**: 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.
- **Author Note**: This FAQ is compiled based on actual questions raised by CEOs, business owners, and CFOs during enterprise implementations of SMRITI Retail OS. The objective is to clarify operational boundaries, investment returns, and implementation safety.

> "Light begins with learning."
> 
> — Jawahar R. Mallah
> Founder & Chief Architect, AITDL

#### Document Metadata
- **Document Version**: 1.0.0
- **Release Date**: 2026-06-23
- **Intended Audience**: C-Level Executives, Brand Directors, CFOs, and Retail Entrepreneurs.
- **Learning Objectives**: Address concerns regarding distributor collaboration, data security, ROI timelines, system boundaries, and operational overhead.

---

## 💼 Section 1: Business Value & ROI

### Q1: How much inventory reduction is realistic after implementing SMRITI PSV?
**Response**: Most retail networks achieve a **15% to 25% reduction** in overall channel inventory within the first 6 months. By eliminating blind spots, you stop shipping slow-moving styles and sizes to depots where they accumulate. Instead, you maintain higher velocity lines with a smaller, more active inventory footprint.

### Q2: How quickly can our brand expect to see measurable results?
**Response**: Operational visibility is immediate upon connecting your first distributor. Financial returns (recovered sales and capital release) typically show in **30 to 45 days** as the system flags stockouts of high-demand items and highlights excess stocks eligible for Network Stock Transfers.

### Q3: What is the estimated ROI of SMRITI PSV, and how is it calculated?
**Response**: The system delivers value through two channels:
1.  **Revenue Recovery**: Recapturing lost sales from stockouts (reducing stockouts from 8% to 4% returns 30% gross margins on that recovered volume directly to profit).
2.  **Working Capital Release**: Shifting dead stock out of stagnant zones via transfers, releasing locked cash back to your bank account.
On average, brands see a full return on their software investment within **3 to 4 months** of going live.

### Q4: Our brand is currently small, with only a few distributors. Is PSV worth the investment?
**Response**: Yes. Implementing PSV early establishes structured data habits and inventory discipline. It ensures you do not waste limited cash on dead stock. SMRITI is built to scale; it supports small brands with 3 distributors and expands as they grow to 500+ locations.

### Q5: We already have standard ERP reports. Why do we need SMRITI PSV?
**Response**: Traditional ERP reports are **static and retrospective**—they show what happened in the past. SMRITI PSV provides **actionable, real-time intelligence**. Instead of a report listing stock levels, SMRITI alerts you to a critical Weeks of Cover (WOC) shortage and suggests the exact stock transfer to resolve it.

---

## 🔒 Section 2: Data Privacy & Distributor Cooperation

### Q6: Distributors are highly protective of their data. Why would they share it with us?
**Response**: SMRITI changes the relationship from transaction-based to collaborative:
*   Distributors get access to WOC metrics and automated reorder suggestions, helping them run a leaner business with higher turns.
*   By sharing secondary sales data, they get replenishment stock before they run out, protecting their local retail sales.
*   SMRITI allows controlled data access; distributors only see their own warehouse data, while the brand sees the aggregate network.

### Q7: How does SMRITI address distributor data privacy concerns?
**Response**: SMRITI maintains a strict **Inventory Visibility Layer** that segregates distributor data. It does not access their accounts, payroll, or supplier pricing. It only monitors sales quantities, stock balances, and returns. All data is transferred securely and is not shared with third parties.

### Q8: What happens if a distributor uses a different local accounting system (e.g. TallyPrime)?
**Response**: SMRITI does not require distributors to change their software. SMRITI imports secondary sales and inventory snapshots using secure, automated data mapping templates. As long as their local system can export a basic CSV or Excel sheet, SMRITI can parse it.

### Q9: Can we onboard distributors gradually, or do they all need to go live at once?
**Response**: Adoption is designed to be **gradual and modular**. We recommend starting with a pilot phase of **2 to 3 key distributors** in one region. Once their operations stabilize and they see their stockout rates drop, you can onboard other distributors region by region.

---

## ⚙️ Section 3: Technical Architecture & System Boundaries

### Q10: Does SMRITI PSV duplicate inventory records or modify our core ERPNext Stock Ledgers?
**Response**: SMRITI does **not** modify your core ERPNext Stock Ledger or General Ledger. It runs as an independent, upgrade-safe frontend Inventory Visibility Layer. ERPNext remains the system of record for brand-owned transactions, while SMRITI aggregates secondary data separately to avoid audit complications.

### Q11: How does SMRITI handle connection dropouts or offline periods at distributor locations?
**Response**: SMRITI does not require persistent 24/7 internet connectivity at distributor depots. The secondary sales logs can be queued locally and uploaded in daily batches. If a connection goes down, the system preserves the logs and syncs automatically when the link is restored.

### Q12: How long does a standard SMRITI PSV implementation take?
**Response**: A standard setup takes **2 to 4 weeks**. This includes configuring the Inventory Visibility Layer, setting up partner portal logins, mapping import sheets, and training planners. 

### Q13: Does implementing SMRITI require modifying our core ERPNext code?
**Response**: No. SMRITI is built on a **service-first architecture** that interacts with ERPNext through standard, whitelisted APIs. This ensures your core ERP remains clean and fully upgradeable without breaking any custom SMRITI frontends.

### Q14: How does SMRITI prevent duplicate file uploads from distributors?
**Response**: SMRITI generates a unique cryptographic fingerprint (MD5 checksum) for every uploaded data file. If a distributor attempts to upload the same file twice, the system flags the duplicate and blocks the second import, preserving data integrity.

### Q15: What is SMRITI's strategy for reconciling data with TallyPrime?
**Response**: SMRITI operates under a **Tally-First Accounting Strategy**. SMRITI owns real-time inventory, dispatches, secondary sales tracking, and reorder intelligence. Tally remains the absolute owner of financial books of accounts, general ledgers, tax computations, and annual closing statements. 

---

## 📈 Section 4: Operational Workflows & Exception Handling

### Q16: How does the system handle "Negative Balance" exceptions on the dashboard?
**Response**: Negative balances occur when secondary sales files are uploaded before the brand's primary dispatch invoices are imported. SMRITI flags these in the **Exception Monitoring Center** and prompts the planner to upload the missing dispatch invoices to auto-reconcile the balance.

### Q17: Does SMRITI automatically place purchase orders or trigger stock transfers?
**Response**: No. Under **Rule 10 (Approval before Automation)**, SMRITI provides recommendations and suggestions, but **never executes transactions automatically**. Every stock transfer and replenishment order requires explicit human review and approval before execution.

### Q18: What is "Size Curve Health," and why is it important for footwear and apparel?
**Response**: Standard inventory systems track total units, which can hide stockouts. A distributor might have 50 pairs of shoes in stock, but they are all Size 5 and Size 11 (excess), while Size 7 and 8 are completely sold out. SMRITI tracks the **Size Curve Health** to ensure you hold the right ratio of sizes matching local consumer demand.

### Q19: What is the "Outlet Health Score" (OHS), and how is it calculated?
**Response**: The Outlet Health Score is an operational compliance index that rates a distributor or outlet's data discipline. It is computed as:
$$\text{OHS} = 0.6 \times \text{Data Sync Score} + 0.4 \times \text{Physical Audit Score}$$
It ensures distributors upload sales logs on time and conduct bi-weekly physical stock verifications to keep data accurate.

### Q20: What happens if a distributor reports a return of an item they never received?
**Response**: SMRITI flags this as a **Return Serial Mismatch** exception. Planners can cross-reference the return barcode against the original dispatch logs to identify if the distributor scanned the wrong box or mixed stock from another supplier.

---

## 👑 Section 5: Strategic Governance & Scalability

### Q21: Can we start with one region, such as Western India, before scaling nationally?
**Response**: Yes. This is our recommended path. Scaling by region allows you to align local logistics, refine delivery lead times, and build case studies that encourage faster adoption among distributors in other regions.

### Q22: How does SMRITI PSV scale when handling 100+ distributors with over 10,000 SKUs?
**Response**: SMRITI is designed for high-throughput retail. It uses Redis caching for performance-critical calculations like WOC and Sell-Through %, keeping dashboard loads sub-second. Transaction processing is queued in the background to ensure no system lag during peak upload windows.

### Q23: Who owns the business formulas used in SMRITI PSV?
**Response**: All formulas are registered centrally in the **SMRITI Formula Registry (DOC-02)**. This registry documents the mathematical logic, variables, and data sources for each metric, ensuring transparency and prevent "black-box" formulas.

### Q24: How does SMRITI ensure that field planners can access the system on the move?
**Response**: The SMRITI frontend is responsive and optimized for mobile, tablet, and desktop screens. Planners can view Weeks of Cover alerts, approve stock transfers, and check distributor health scores from any device on the field.

### Q25: What level of support and SLAs does AITDL provide for SMRITI PSV?
**Response**: We provide comprehensive enterprise support, including 24/7 critical system monitoring, dedicated account manager access, and a guaranteed 4-hour SLA response for any critical data sync exceptions flagged in the Exception Center.

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
*SMRITI Sales Enablement Suite — Executive FAQ v1.0.0 | AITDL Network*
