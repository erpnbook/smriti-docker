# SMRITI Retail OS User Manual — Volume 5: Training Workbook

## About This Manual & Author Profile

### Metadata
- **Author**: Jawahar R. Mallah
- **Designation**: Founder & Chief Architect
- **Organization**: AITDL – AI Technology & Development Lab
- **Professional Experience**: 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.
- **Documentation Version**: v1.0.0
- **Release Date**: 2026-06-19
- **Intended Audience**: Shop Owner, Distributor, Sales Manager, Stock Auditor, Store Operator, Non-Technical User, First-Time User
- **Learning Objectives**: Apply SMRITI Retail OS knowledge through 52 practical exercises.
- **Contact / Support**: support@aitdl.com

### Author Note
This manual is based on practical field experience gathered across retail operations, distribution management, inventory control, software architecture, business automation, and enterprise solution development. The objective is to make SMRITI Retail OS understandable and usable by both technical and non-technical users.

### Documentation Principle
The author believes that software should not only process data but also explain decisions. Every report, score, KPI, alert, recommendation, and prediction within SMRITI must be understandable by business users without requiring technical expertise.

### Revision History
| Version | Date | Author | Description |
| :--- | :--- | :--- | :--- |
| v1.0.0 | 2026-06-19 | Jawahar R. Mallah | Initial Release for SMRITI PDT v2.0 |

> "Light begins with learning."
> 
> — Jawahar R. Mallah
> Founder & Chief Architect, AITDL

---

This workbook contains 52 practical exercises designed to train new team members on SMRITI Retail OS. Complete the exercises sequentially based on your role.

---

## Part 1: Store Operator Exercises (1 to 10)

### Exercise 1: Register a New Distributor Customer
- **Scenario**: A new distributor, **"Royal Footwear Pune"**, wants to purchase sneakers.
- **Actions**:
  1. Navigate to Customer Master. Click **New Customer**.
  2. Enter Name = `Royal Footwear Pune`, Customer Group = `Distributor`, Territory = `Maharashtra`.
  3. Click **Save** then **Submit**.
- **Expected Result**: System generates code `CUST-XXXX`. Check status is "Submitted".

### Exercise 2: Add a Footwear Product Template
- **Scenario**: You are adding a new sandal model, **"Aeroguard Sandals"**.
- **Actions**:
  1. Open Item Master. Click **New Item**.
  2. Code = `SF-AERO-SND`, Name = `Aeroguard Sandals`, Has Variants = Checked.
  3. Save.
- **Expected Result**: Template created.

### Exercise 3: Generate Size Variants
- **Scenario**: Generate sizes `7, 8, 9` for Aeroguard Sandals.
- **Actions**:
  1. Open `SF-AERO-SND` Template.
  2. Select "Size" attribute and add values `7, 8, 9`.
  3. Click **Create Variants**.
- **Expected Result**: System creates `SF-AERO-SND-7`, `SF-AERO-SND-8`, and `SF-AERO-SND-9`.

### Exercise 4: Setup Store Outlet Account (PSA)
- **Scenario**: Create a PSA for the showroom of Royal Footwear Pune.
- **Actions**:
  1. Open PSA, click **New**.
  2. Name = `Royal Pune Showroom`, Customer = `Royal Footwear Pune`, Zone = `West`.
  3. Submit.
- **Expected Result**: PSA registered and active.

### Exercise 5: Import Opening Stock Balances
- **Scenario**: Upload opening balance of 100 pairs of `SF-AERO-SND-8` to Royal Pune Showroom.
- **Actions**:
  1. Go to Operations → Opening Balance.
  2. Select PSA = `Royal Pune Showroom`, item = `SF-AERO-SND-8`, qty = 100.
  3. Submit.
- **Expected Result**: PSA balance shows 100 units.

### Exercise 6: Upload Daily Sales File
- **Scenario**: Pune Showroom sells 12 pairs of `SF-AERO-SND-8` on June 19th.
- **Actions**:
  1. Open Sales Upload. Select PSA = `Royal Pune Showroom`, Date = `2026-06-19`.
  2. Attach TSV sheet containing `SF-AERO-SND-8, 12`.
  3. Click Parse, then Submit.
- **Expected Result**: Showroom stock balance drops to 88 units.

### Exercise 7: Check Party Stock Ledger
- **Scenario**: Verify the transaction history of `SF-AERO-SND-8` at Royal Pune Showroom.
- **Actions**:
  1. Open Party Stock Ledger report.
  2. Filter by PSA and Item.
- **Expected Result**: Shows 100 (Receipt) and -12 (Sales), balance = 88.

### Exercise 8: Handle Invalid Code Upload Error
- **Scenario**: Upload a sales sheet containing invalid code `SF-AERO-SND-13`.
- **Actions**:
  1. Upload spreadsheet. Click Parse.
- **Expected Result**: Parsing stops with warning `Item variant not found`. Correct code to 9 and retry.

### Exercise 9: Upload Multi-Item Sales File
- **Scenario**: Upload sales of 5 pairs of Size 7, and 10 pairs of Size 8.
- **Actions**:
  1. Prepare CSV: `SF-AERO-SND-7, 5` and `SF-AERO-SND-8, 10`.
  2. Upload and submit.
- **Expected Result**: Balances decrease accordingly.

### Exercise 10: Toggle Store Active Status
- **Scenario**: Royal Pune Showroom shuts down for renovation.
- **Actions**:
  1. Open PSA record, untick "Active" checkbox. Save.
- **Expected Result**: Try importing sales for this store; system raises an error.

---

## Part 2: Stock Auditor Exercises (11 to 20)

### Exercise 11: Create a Monthly Stock Count Snapshot
- **Scenario**: Audit Royal Pune Showroom. Counted stock of Size 8 is 70 pairs (Ledger shows 73).
- **Actions**:
  1. Open Physical Snapshot. Select PSA and Audit Date.
  2. Add item `SF-AERO-SND-8`, Qty = 70.
  3. Save & Submit.
- **Expected Result**: Ledger adjusts automatically by -3 units.

### Exercise 12: Run Physical Audit Variance Report
- **Scenario**: View shrinkage levels for Royal Pune Showroom.
- **Actions**:
  1. Open Physical Audit Variance Report.
  2. Filter by PSA.
- **Expected Result**: Displays discrepancy count (-3) and variance percentage.

### Exercise 13: Audit a Large Shipment Receipt
- **Scenario**: Verify receipt of 500 pairs of sneakers.
- **Actions**:
  1. Match Delivery Note voucher quantities against physical boxes received.
  2. Note discrepancies in Audit Notes.
- **Expected Result**: Ledger shows positive stock matching Delivery Note.

### Exercise 14: Log a Stock Theft Adjustment
- **Scenario**: CCTV shows 2 pairs of sandals stolen.
- **Actions**:
  1. Create Physical Snapshot, enter corrected shelf counts.
  2. In Audit Console, select reason `THEFT` and approve.
- **Expected Result**: Stock drops by 2; write-off is logged in liability ledger.

### Exercise 15: Identify Unsubmitted Snapshots
- **Scenario**: Find out which stores have count drafts that are not submitted.
- **Actions**:
  1. Filter Physical Snapshots list by Status = "Draft".
- **Expected Result**: Shows all unsubmitted audits. Send reminders.

### Exercise 16: Audit Size Curve Completeness
- **Scenario**: Check if Pune Showroom is missing core sizes.
- **Actions**:
  1. Run Broken Size Report for Pune PSA.
- **Expected Result**: High-value styles with missing middle sizes are flagged.

### Exercise 17: Track High Discrepancy Outlets
- **Scenario**: Identify outlets with greater than 4% stock shrinkage.
- **Actions**:
  1. Open Audit Variance report, filter by variance % descending.
- **Expected Result**: Focus audits on the top listed stores.

### Exercise 18: Audit Log Reconciliation
- **Scenario**: Verify who approved a stock adjustment of 50 units.
- **Actions**:
  1. Open SMRITI Benefit Audit Log. Search by date.
- **Expected Result**: Displays auditor user ID, timestamp, and reason code.

### Exercise 19: Clear Invalid Draft Snapshots
- **Scenario**: Delete a duplicate draft physical count snapshot.
- **Actions**:
  1. Open draft snapshot, click Delete.
- **Expected Result**: Record removed from list.

### Exercise 20: Audit Verification Checklist
- **Scenario**: Complete the monthly audit checklist.
- **Actions**:
  1. Reconcile sales, verify receipts, and run final variance adjustments.
- **Expected Result**: Store health score increases.

---

## Part 3: Sales Manager Exercises (21 to 30)

### Exercise 21: Setup Variant Reorder Rule
- **Scenario**: Maintain safety stock of 20 pairs for `SF-AERO-SND-8` at Royal Pune Showroom.
- **Actions**:
  1. Open Reorder Rule. Click New.
  2. Set PSA = `Royal Pune Showroom`, Variant = `SF-AERO-SND-8`, Safety Stock = 20.
  3. Submit.
- **Expected Result**: PDT calculation uses 20 pairs safety buffer.

### Exercise 22: Configure Item Group Reorder Rule
- **Scenario**: Set global safety stock of 10 for all sandals.
- **Actions**:
  1. Create Reorder Rule. Set Item Group = `Sandals`, Safety Stock = 10.
  2. Submit.
- **Expected Result**: Applies to all sandals lacking specific variant rules.

### Exercise 23: Review Rebalancing Recommendations
- **Scenario**: Pune Showroom is overstocked, Mumbai Showroom is out of stock.
- **Actions**:
  1. Open Transfer Recommendations report.
- **Expected Result**: Shows suggested stock quantity and transfer route.

### Exercise 24: Approve a Network Transfer Suggestion
- **Scenario**: Approve SMRITI's suggestion to move 20 pairs.
- **Actions**:
  1. Click **Create Stock Transfer** on recommendation row.
- **Expected Result**: Auto-generates Delivery Note request.

### Exercise 25: Adjust Lead Time Settings
- **Scenario**: Supplier delays increase delivery times to 12 days.
- **Actions**:
  1. Open PSV Settings, set default lead time = 12. Save.
- **Expected Result**: Stockout predictions adjust forward by 5 days.

### Exercise 26: Exclude Seasonal Items from Rebalancing
- **Scenario**: Stop transfer suggestions for winter boots in summer.
- **Actions**:
  1. Open Item master, untick "Active Rebalancing" flag.
- **Expected Result**: Transfer recommendations ignore this item.

### Exercise 27: Audit Rule Cascade
- **Scenario**: Verify which safety stock rule applies to a sneaker variant.
- **Actions**:
  1. Check rules page. Variant rule overrides Item Group rule, which overrides Global settings.
- **Expected Result**: Displays rule hierarchy.

### Exercise 28: Resolve Recommendation Conflict
- **Scenario**: Source store stock drops below safety limit.
- **Actions**:
  1. SMRITI automatically cancels the transfer suggestion and recommends purchase.
- **Expected Result**: Recommendation changes to `PURCHASE`.

### Exercise 29: Setup Max Stock Cap
- **Scenario**: Limit Pune Showroom stock capacity to 200 units.
- **Actions**:
  1. Set Max Stock = 200 in the Reorder Rule.
- **Expected Result**: Reorder recommendations cap at 200.

### Exercise 30: Check Store Health Compliance
- **Scenario**: Identify outlets with poor data sync latency.
- **Actions**:
  1. Open Outlet Health Score report.
- **Expected Result**: Stores below 60% are flagged.

---

## Part 4: Executive Exercises (31 to 40)

### Exercise 31: View Network Stock Status
- **Scenario**: Check total boots stock across all zones.
- **Actions**:
  1. Open PSV Dashboard, filter by Category = Boots.
- **Expected Result**: Displays total boots stock and sales velocity.

### Exercise 32: Run Broken Size Analysis
- **Scenario**: Check for sales opportunities lost due to missing sizes.
- **Actions**:
  1. Open Broken Size report.
- **Expected Result**: Style lists flagged with missing size sets are displayed.

### Exercise 33: Evaluate Product Sell-Through %
- **Scenario**: Verify sneaker sales efficiency.
- **Actions**:
  1. Open Sell-Through report, set lookback = 30 days.
- **Expected Result**: Displays sell-through percentage.

### Exercise 34: Inspect PDT State Machine
- **Scenario**: Check which variants are in "Critical" state.
- **Actions**:
  1. Open PDT Dashboard, filter by State = Critical.
- **Expected Result**: Displays list of variants with low cover days.

### Exercise 35: Analyze Stock-Out Risk Dates
- **Scenario**: Find out when your top-selling model will run out of stock.
- **Actions**:
  1. Open Stockout Prediction Report.
- **Expected Result**: Displays predicted stockout date per store.

### Exercise 36: Run Sandbox Simulation for Promotion Campaign
- **Scenario**: Test impact of a 1.5x sales velocity increase.
- **Actions**:
  1. Open Simulation Sandbox. Set velocity multiplier = 1.5.
  2. Run simulation.
- **Expected Result**: Screen displays simulated stockout dates without altering database.

### Exercise 37: Evaluate Cross-Zone Freight Impact
- **Scenario**: Model a 30% increase in transport costs.
- **Actions**:
  1. Open Sandbox, increase freight penalty to 1.3x.
- **Expected Result**: Transfer benefit scores drop, and recommendations shift to local zones.

### Exercise 38: Check Capital Locked in Dead Stock
- **Scenario**: Measure the monetary value of non-moving inventory.
- **Actions**:
  1. Open PDT Dashboard, filter by State = Dead Stock.
- **Expected Result**: Displays total capital locked in dead stock.

### Exercise 39: Track Territory Sales Growth
- **Scenario**: Identify your fastest-growing sales zone.
- **Actions**:
  1. Open PSV Dashboard, group by Zone.
- **Expected Result**: Displays zone-wise velocity and growth charts.

### Exercise 40: Review Rebalancing Performance
- **Scenario**: Measure total savings from inter-store stock transfers.
- **Actions**:
  1. Open Rebalancing Performance report.
- **Expected Result**: Displays total benefit score achieved.

---

## Part 5: Administrator Exercises (41 to 50)

### Exercise 41: Force Rebuild Product Twin Cache
- **Scenario**: Trigger recalculation for all store twins manually.
- **Actions**:
  1. Go to SMRITI API panel or PDT Dashboard.
  2. Click **Force Rebuild Cache**.
- **Expected Result**: Recalculation triggers background queue jobs.

### Exercise 42: Clear System Rebuild Locks
- **Scenario**: Rebuild lock is stuck after server restart.
- **Actions**:
  1. Clear key `pdt_rebuild:*` using Cache Clear tool or Redis CLI.
- **Expected Result**: Lock is released.

### Exercise 43: Validate Unique Constraint Index
- **Scenario**: Verify unique database constraint is active.
- **Actions**:
  1. Check database statistical schema tables.
- **Expected Result**: Index `unique_company_psa_item` exists.

### Exercise 44: Set Freshness SLA Times
- **Scenario**: Adjust stale warnings to trigger after 12 hours.
- **Actions**:
  1. Open PSV settings, set stale limit = 12. Save.
- **Expected Result**: Twins older than 12 hours show "Stale".

### Exercise 45: Monitor Background Job Queues
- **Scenario**: Check if PDT rebuild tasks are running.
- **Actions**:
  1. Open Queue Monitor page.
- **Expected Result**: Displays active, pending, and failed queue tasks.

### Exercise 46: Audit User Activity Logs
- **Scenario**: Track who changed a global lead time setting.
- **Actions**:
  1. Open SMRITI Benefit Audit Log. Filter by settings doctype.
- **Expected Result**: Displays user name and changes.

### Exercise 47: Verify API Endpoint Responses
- **Scenario**: Perform api ping checks.
- **Actions**:
  1. Ping `/api/method/smriti_retail_os.api.pdt_api.get_twin_status`.
- **Expected Result**: Returns JSON format status payload.

### Exercise 48: Configure Auto-Alerts
- **Scenario**: Setup automatic warnings for low health scores.
- **Actions**:
  1. Open Notifications settings, set triggers for Health Score < 60%.
- **Expected Result**: Automatic emails are enabled.

### Exercise 49: Backup Shadow Ledger Database
- **Scenario**: Run database snapshot backup.
- **Actions**:
  1. Go to Backup console. Click Create Backup.
- **Expected Result**: System downloads compressed SQL snapshot.

### Exercise 50: Rebuild Redis Cache Registry
- **Scenario**: Flush all cached twin pages.
- **Actions**:
  1. Click 'Flush Redis Cache' inside Admin Utilities.
- **Expected Result**: Dashboard reloads retrieve clean data from DB.

### Exercise 51: Configure a New Formula in the Formula Registry
- **Scenario**: Add a new operational KPI for "Promo Conversion Rate" to the Formula Registry.
- **Actions**:
  1. Open SMRITI Formula Registry (at route `/smriti-formula-registry`).
  2. Click **New Formula Definition**.
  3. Enter Formula ID = `INV-005`, Formula Name = `Promo Conversion Rate`, Category = `Sales`, Formula Expression = `promo_sales_qty / total_sales_qty`, Business Meaning = `Tracks promotional sales share of total sales`, Worked Example = `Promo Sales = 20, Total Sales = 100. Conversion = 20 / 100 = 0.20 or 20%`.
  4. Fill in standard interpretation guides, set status to `Approved`, and save.
- **Expected Result**: The new formula is successfully registered and cached in Redis.

### Exercise 52: Verify a Term in the Business Dictionary via the Universal Explain Modal
- **Scenario**: A cashier wants to understand what "Weeks of Cover (WOC)" means directly from the UI.
- **Actions**:
  1. Open any SMRITI dashboard and click the **ⓘ Explain** button next to the WOC metric.
  2. In the Universal Explain Modal, read the Worked Example and Business Meaning.
  3. Click the **📖 Dictionary Entry** button at the bottom of the modal.
- **Expected Result**: The system redirects to `/smriti-dictionary` (pre-filtered for WOC) and opens the Business Dictionary drawer detailing Weeks of Cover, its Hinglish definition, FAQs, and related terms.

---

## Final Acknowledgement Page

### Author Section
- **Author**: Jawahar R. Mallah
- **Designation**: Founder & Chief Architect
- **Organization**: AITDL – AI Technology & Development Lab
- **Professional Experience**: 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.

### Closure Note
Thank you for using SMRITI Retail OS. For support, please contact the AITDL Helpdesk at **support@aitdl.com**.

> "Light begins with learning."
> 
> — Jawahar R. Mallah
> Founder & Chief Architect, AITDL
