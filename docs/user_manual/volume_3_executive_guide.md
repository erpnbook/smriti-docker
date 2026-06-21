# SMRITI Retail OS User Manual — Volume 3: Executive Dashboard & Analytics Guide

Welcome to the **SMRITI Retail OS Executive Dashboard & Analytics Guide**. This guide is written for Shop Owners, Brand Managers, Directors, and Executive Decision Makers. It explains analytical metrics, forecasting models, and sandbox simulation tools.

---

## Chapter 1: PSV Dashboard (पार्टी स्टॉक विजिबिलिटी डैशबोर्ड)

### 1. Purpose (उद्देश्य)
The **[PSV](dictionary:PSV) Dashboard** provides a real-time, consolidated view of all network inventory, sales velocities, and stock status across your entire distributor and retail network.
- **Business Problem Solved**: Eliminates blind spots (स्टॉक का पता न होना). Executives see exactly how much stock is in transit, at outlets, and selling daily.

### 2. Real-Life Example (वास्तविक जीवन का उदाहरण)
The Brand Director of StepFit Shoes opens the dashboard on Monday morning to see:
- Total Network Stock: **45,000 pairs**
- Active Outlets: **38 stores**
- Weekly [Sales Velocity](dictionary:Sales Velocity): **2,800 pairs**
- Critical [Stockout Risk](dictionary:Stockout Risk): **4 stores** in Delhi Region.

### 3. Step-by-Step Dashboard Guide (डैशबोर्ड देखने की प्रक्रिया)
1. **Menu Path**: SMRITI Home → Dashboards → **PSV Dashboard**
2. **Filters**: Select Company, Territory, or Customer Group.
3. **Drill Down**: Click on any store card to see item-level stock cards.

[Screenshot: PSV Dashboard Main View]

### 4. Metric Explanations (मैट्रिक्स स्पष्टीकरण)

| Metric | Simple Explanation | Calculation Example |
| :--- | :--- | :--- |
| **Total Channel Stock** | Total stock currently sitting in all partner stores. | Sum of all [PSA](dictionary:PSA) balances. |
| **Weekly Sales Velocity** | Number of units sold in the last 7 days. | Sum of [Sales Velocity](dictionary:Sales Velocity) for the last 7 days. |
| **Stockout Risk Ratio** | Percentage of active products currently out of stock. | $\frac{\text{Out-of-Stock Variants}}{\text{Total Registered Variants}} \times 100$ |

### 5. Example Dashboard View (उदाहरण दृश्य)
- **Filters**: Region = `Maharashtra`
- **Dashboard Displays**:
  - Total Stock: `12,500 units`
  - Daily Velocity: `320 units/day`
  - Coverage: `39 days` (Healthy).

### 6. Actionable Decisions (कार्रवाई योग्य निर्णय)
- If coverage falls below 14 days, expedite production. If coverage exceeds 60 days, halt fresh purchase orders.

---

## Chapter 2: Broken Size Analysis (टूटी हुई आकार विश्लेषण)

### 1. Purpose (उद्देश्य)
Footwear and apparel sell in style curves (e.g., standard size sets). **Broken Size Analysis** identifies outlets that have stock of a style, but are missing key sizes (e.g. Size 7 and 8 are out, but 6 and 9 are sitting on shelf).
- **Business Problem Solved**: Prevents "invisible lost sales". If a customer wants Size 8 and it's missing, they walk out. The style looks "stocked" in the ledger but is unsellable.

### 2. Real-Life Example (वास्तविक जीवन का उदाहरण)
At **Pune Plaza**, the sneaker style `Flyrunner Blue` has:
- Size 6: 12 units
- Size 7: 0 units (Broken Size!)
- Size 8: 0 units (Broken Size!)
- Size 9: 15 units
SMRITI flags this style curve as **"Broken"** and lists `7, 8` as missing sizes.

### 3. Process (प्रक्रिया)
1. **Menu Path**: SMRITI Home → Reports → Broken Size Report
2. **Scan Report**: Look for styles flagged as `Broken`.
3. **Action**: Create a transfer request to send missing sizes from the central warehouse.

[Screenshot: Broken Size Analysis Table]

### 4. Field Explanation (फील्ड स्पष्टीकरण)

| Field | Meaning | Example |
| :--- | :--- | :--- |
| **Template Style** | Main product template. | `Flyrunner Blue Sneaker` |
| **Curve Status** | Shows if all sizes in the set are in stock. | `Broken` |
| **Missing Sizes** | List of sizes with 0 inventory. | `7, 8` |
| **Wasted Inventory** | Stock of other sizes that is sitting idle. | `27 units` (Sizes 6 and 9) |

### 5. FAQs
1. **Why is a style flagged as broken if we have 50 units in stock?**
   - Because those 50 units are all in extreme sizes (e.g. size 6 and 9), while fast-moving middle sizes (7 and 8) are out of stock.

---

## Chapter 3: Outlet Health Score (आउटलेट स्वास्थ्य स्कोर)

### 1. Purpose (उद्देश्य)
The **[Outlet Health Score](dictionary:Outlet Health Score)** measures the data compliance and operational quality of a store.
- **Business Problem Solved**: Prevents garbage-in-garbage-out. If a store manager doesn't upload sales daily or fails to submit snapshots, SMRITI's forecasts become unreliable. This score rates the store's data discipline.

### 2. Real-Life Example (वास्तविक जीवन का उदाहरण)
- **Mumbai Showroom**: Uploads sales daily, completes physical counts weekly. Health Score = **98% (Excellent)**.
- **Nagpur Palace**: Misses sales uploads for 5 days, has not audited stock for 2 months. Health Score = **42% (Poor)**.

### 3. Metric Explanation (गणना स्पष्टीकरण)
The score is calculated from:
1. **Sales Upload Latency (50% weight)**: Days since last upload.
2. **Physical Count Integrity (50% weight)**: Time elapsed since last physical snapshot.

---

## Chapter 4: Sell Through Analytics (बिक्री-दर विश्लेषण)

### 1. Purpose (उद्देश्य)
**[Sell Through Analytics](dictionary:Sell Through)** calculates the percentage of received inventory that has been sold to end customers over a lookback period.
- **Business Problem Solved**: Tells you if stock is actually selling, or just sitting in distributor warehouses.

### 2. Real-Life Example (वास्तविक जीवन का उदाहरण)
StepFit ships **500 pairs** of Flyrunners to **Pune Plaza**. Pune Plaza sells **350 pairs** in 30 days.
- $\text{Sell Through \%} = \frac{350}{500} \times 100 = \text{\textbf{70\%}}$ (Excellent performance!).

### 3. Decision Matrix (निर्णय तालिका)

| Sell Through Range | Classification | Action |
| :--- | :--- | :--- |
| **> 60%** | Fast Moving | Replenish immediately. |
| **30% - 60%** | Moderate | Monitor and maintain current levels. |
| **< 30%** | Slow Moving / Dead | Run promotion or transfer stock. |

---

## Chapter 5: PDT Dashboard (उत्पाद डिजिटल ट्विन डैशबोर्ड)

### 1. Purpose (उद्देश्य)
The **[PDT](dictionary:PDT) Dashboard** displays the digital twin metrics for every single SKU. 
- **Business Problem Solved**: Moves operations from reactive ("How much stock do we have?") to predictive ("What will happen to this stock in the next 14 days?").

### 2. Real-Life Example (वास्तविक जीवन का उदाहरण)
For `Flyrunner-Blue-8` at Mumbai Grand Mall:
- **PDT State**: `Critical`
- **Weekly Velocity**: `21.5 units/week` ([Sales Velocity](dictionary:Sales Velocity))
- **[Weeks of Cover](dictionary:WOC)**: `1.4 weeks`
- **Predicted Stockout Date**: `2026-06-29`
- **Recommended Action**: Transfer 20 units from Pune.

---

## Chapter 6: Stock-Out Prediction (स्टॉक-आउट भविष्यवाणी)

### 1. Purpose (उद्देश्य)
Calculates the exact date when an item will run out of stock based on its daily sales velocity.
- **Business Problem Solved**: Gives supply chains early warnings to manufacture and ship goods before the store actually runs dry.

### 2. Real-Life Example & Calculation (गणना स्पष्टीकरण)
- Current Stock = **60 units**.
- Weekly Velocity = **14 units**.
- Daily Velocity = $\frac{14}{7} = \textbf{2 units/day}$.
- Days to Stockout = $\frac{60}{2} = \textbf{30 days}$.
- Expected Stockout Date = Today + 30 days = **July 19th, 2026**.

---

## Chapter 7: Simulation Sandbox (सिमुलेशन सैंडबॉक्स)

### 1. Purpose (उद्देश्य)
The **Simulation Sandbox** is a risk-free testing environment. Executives can model what-if scenarios (e.g. "What if sales double?" or "What if freight rates increase by 50%?") in-memory, without altering actual live database records.
- **Business Problem Solved**: Allows strategic planning and testing of business assumptions without corrupting the operational ledger data.

### 2. Real-Life Example (वास्तविक जीवन का उदाहरण)
The Sales VP wants to run a "Monsoon Discount Campaign" that is expected to increase [Sales Velocity](dictionary:Sales Velocity) by **1.8x** but will increase transit delays due to rain. They input these parameters in the sandbox and view the simulated [Weeks of Cover](dictionary:WOC) and stockout dates across the network.

### 3. Step-by-Step Sandbox Guide (सिमुलेशन चलाने की प्रक्रिया)
1. **Menu Path**: SMRITI Home → Operations → Simulation Sandbox
2. **Set Parameters**:
   - Velocity Multiplier = `1.8`
   - Target Outlets = `All Maharashtra Stores`
3. **Run Simulation**: Click **Execute Simulation**.
4. **Analyze Results**: Review the generated recommendations (e.g. replenishment quantities will jump from 500 to 900 units).

[Screenshot: Simulation Sandbox Interface]

### 4. FAQs
1. **Will sandbox simulations affect my active store stock values?**
   - No, all calculations are executed in-memory and are not written to the live ledger.
2. [Remaining 9 FAQs detailed in Volume 4]

---

## Support & Helpdesk
Thank you for using SMRITI Retail OS. For additional support, please contact the Helpdesk at **support@aitdl.com**.
