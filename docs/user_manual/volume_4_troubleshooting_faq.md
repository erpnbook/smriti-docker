# SMRITI Retail OS User Manual — Volume 4: Troubleshooting & FAQ Handbook

This handbook provides quick resolution steps for common errors and answers 160 Frequently Asked Questions (10 per module) across all SMRITI modules.

---

## 1. Customer Master FAQs & Troubleshooting

### FAQs
1. **Q: Customer Name change kaise karein after submit?**
   - A: Master page par toggle "Edit" karein (if permissions allow) ya record cancel karke Amend button click karein.
2. **Q: Can we set credit limits in non-INR currency?**
   - A: Yes, billing currency link change karein before saving draft.
3. **Q: How to block a customer temporarily?**
   - A: Checkbox "Disabled" ko tick karein aur save karein.
4. **Q: Duplicate Customer error: How to merge?**
   - A: System Manager panel se 'Customer Merge' tool open karein, main and duplicate accounts select karke merge confirm karein.
5. **Q: Customer Group list where is it configured?**
   - A: Setup menu se Customer Group doctype list check karein.
6. **Q: Territory link mandatory kyu hai?**
   - A: Correct tax calculation rules or geographical rebalancing formulas apply karne ke liye correct territory required hai.
7. **Q: Customer outstanding credit data is wrong. How to refresh?**
   - A: Financial accounts reconcile karein ERPNext side par, check if payments entries are submitted.
8. **Q: Does disabling a customer delete old sales history?**
   - A: No, old logs remain intact. New sales upload is blocked.
9. **Q: Credit limit lock can be bypassed?**
   - A: Only by Administrators using temporary bypass flags.
10. **Q: Customer address in multi-languages?**
    - A: Address fields provide multi-language text formats.

### Troubleshooting
- **Error**: `Duplicate entry for Customer 'X'`.
  - **Resolution**: Check if the customer has already been registered. Use search filters to verify.

---

## 2. Item Master FAQs & Troubleshooting

### FAQs
1. **Q: Template item and variant item mein differences kya hai?**
   - A: Template design config model hai (e.g. Flyrunner Sneaker). Variant actual stock code hai (e.g. Flyrunner-Blue-8).
2. **Q: Standard pricing update parameters automatically?**
   - A: Price lists update automatically when price list changes are submitted.
3. **Q: Barcode generation breaks. Why?**
   - A: Ensure HSN/EAN field is populated correctly in Item Master.
4. **Q: Can variants have different prices than template?**
   - A: Yes, you can override standard rate in individual Variant records.
5. **Q: What happens if HSN code is wrong?**
   - A: Tax rates in billing invoices will apply incorrectly, violating audit checks.
6. **Q: How to delete unused variants?**
   - A: If stock ledger entries do not exist, open Variant and click Delete.
7. **Q: Do we need size charts?**
   - A: Yes, size attributes are configured inside Item Attributes master.
8. **Q: Weight field import benefits?**
   - A: Helps calculate freight cost penalties during network transfers.
9. **Q: Brand grouping where is it linked?**
   - A: Link brand name inside Item Group or custom Brand master field.
10. **Q: Standard UOM (Unit of Measure) conversion?**
    - A: Footwear standard UOM is 'Box' or 'Pair'. Do not change after transactions.

### Troubleshooting
- **Error**: `Cannot link Variant. Template 'X' is not submitted`.
  - **Resolution**: First submit the main template item, then create/save the variant items.

---

## 3. Party Stock Account (PSA) FAQs & Troubleshooting

### FAQs
1. **Q: Zone field change karne se calculations par kya effect hoga?**
   - A: Region based transit freight variables shift automatically (e.g. Mumbai to Nagpur rebalancing freight changes).
2. **Q: One outlet, multiple counters: How many PSAs?**
   - A: Create one PSA per inventory stock point. If counters share stock, create one.
3. **Q: Customer link changes permitted?**
   - A: No, Customer field is locked after submitting PSA.
4. **Q: Virtual PSA where is it used?**
   - A: Used to track distributor channel stocks before physical receipt.
5. **Q: How to close a store PSA?**
   - A: Uncheck "Active" flag. SMRITI will block stock dispatches.
6. **Q: Location name mapping rules?**
   - A: Keep it simple: Location city + Store area (e.g. Mumbai Borivali).
7. **Q: Zone changes require system restart?**
   - A: No. Cache values update in real-time.
8. **Q: Can PSA hold company stock?**
   - A: No. PSA is only for distributor or channel stock.
9. **Q: Outstanding balances on PSA?**
   - A: Checked via PSV balance engine.
10. **Q: Active flag checked by hooks?**
    - A: Yes. Delivery Note submits fail if destination PSA is disabled.

### Troubleshooting
- **Error**: `PSA 'Pune WH' is not active`.
  - **Resolution**: Open PSA master, set checkbox "Active" = 1, save, and submit.

---

## 4. Sales Upload FAQs & Troubleshooting

### FAQs
1. **Q: Sales file parsing fails. Why?**
   - A: Column headers must exactly match `item_code` and `qty` lowercase.
2. **Q: Duplicate uploads prevention?**
   - A: SMRITI checks file hash. Re-uploading the same file raises validation errors.
3. **Q: Can we upload negative quantities?**
   - A: No. Returns must be uploaded via return vouchers or physical snapshots.
4. **Q: What is posting date format?**
   - A: Standard YYYY-MM-DD.
5. **Q: Daily upload time limits?**
   - A: Upload before 11 PM to prevent Outlet Health Score dropping.
6. **Q: How to correct wrong entries?**
   - A: Cancel the Sales Upload voucher, edit inputs, and re-submit.
7. **Q: Can we upload Excel sheets with multiple sheets?**
   - A: SMRITI reads the first active sheet in workbooks.
8. **Q: How to upload bulk sales?**
   - A: Use the SMRITI standard template from Operations.
9. **Q: Missing items during upload?**
   - A: Ensure all codes are registered in the Item Master first.
10. **Q: Upload speeds?**
    - A: Parses 5,000 rows in less than 5 seconds.

### Troubleshooting
- **Error**: `TypeError: cannot parse sheet`.
  - **Resolution**: Export sheet as CSV/TSV format, check headers, and re-upload.

---

## 5. Party Stock Ledger FAQs & Troubleshooting

### FAQs
1. **Q: Ledger row edit options?**
   - A: Read-only. Row adjustments are only made by canceling/modifying documents.
2. **Q: Ledger entries missing after sales upload?**
   - A: Rebuild cache or refresh Redis. Ensure the upload voucher is submitted.
3. **Q: Qty values color meanings?**
   - A: Green indicates stock additions (+), Red indicates sales/dispatches (-).
4. **Q: Cumulative balance calculation?**
   - A: Sum of all transactions from opening date to current timestamp.
5. **Q: Negative balance checks?**
   - A: SMRITI ledger enforces zero balance floor; transactions cannot push stock negative.
6. **Q: Can we export ledger?**
   - A: Yes, click 'Export' button on report header.
7. **Q: Voucher links?**
   - A: Click on Voucher No to open source file.
8. **Q: Sorting rules?**
   - A: Sorted by Posting Datetime.
9. **Q: Ledger lock times?**
   - A: Auto locks daily at midnight.
10. **Q: Shadow ledger vs stock ledger?**
    - A: Shadow ledger tracks distributor retail channels; stock ledger tracks company depots.

### Troubleshooting
- **Error**: `Negative balance warning at row 34`.
  - **Resolution**: Check for missed delivery note entries prior to sales uploads.

---

## 6. Physical Snapshot FAQs & Troubleshooting

### FAQs
1. **Q: Audit count differs from ledger. What happens?**
   - A: SMRITI auto-adds discrepancy adjustments.
2. **Q: Can multiple managers submit audit at the same time?**
   - A: No, queue locks prevent concurrent audit updates.
3. **Q: Ideal snapshot times?**
   - A: Store closing times to prevent transaction overlaps.
4. **Q: How to count boxes?**
   - A: Use barcode scanners.
5. **Q: Missing items in snapshot?**
   - A: Items not listed in snapshot remain at current ledger balance.
6. **Q: Audit frequency defaults?**
   - A: Enforced every 30 days.
7. **Q: Can we cancel submitted snapshot?**
   - A: Only administrators can reverse audit snapshots.
8. **Q: What is threshold check?**
   - A: Alerts are triggered if variance exceeds 5%.
9. **Q: Does it affect accounts?**
   - A: Updates shadow ledger liability records.
10. **Q: Offline snapshot support?**
    - A: Yes, save offline spreadsheet and upload when online.

### Troubleshooting
- **Error**: `Audit Date cannot be in the future`.
  - **Resolution**: Set the date field to today's date or select a past date.

---

## 7. PSV Dashboard FAQs & Troubleshooting

### FAQs
1. **Q: Dashboard data delay?**
   - A: Refreshes dynamically every 5 minutes.
2. **Q: Stock counts do not match?**
   - A: Check filters. Ensure correct company and zone are selected.
3. **Q: What does Red status indicate?**
   - A: Store stock cover is critical (less than 14 days).
4. **Q: Can we share dashboard cards?**
   - A: Click export PDF or share link.
5. **Q: Multi-currency support?**
   - A: Currency displays standard INR values.
6. **Q: Visual layout options?**
   - A: Supports dark and light UI modes.
7. **Q: Missing metrics?**
   - A: Rebuild twin cache parameters.
8. **Q: Can sales reps see full dashboard?**
   - A: Reps only see their assigned territory outlets.
9. **Q: Mobile view?**
   - A: Yes, fully responsive dashboard.
10. **Q: Reorder indicators?**
    - A: Flashing red icon shows reorder rule breaches.

### Troubleshooting
- **Error**: `No data returned for selected PSA`.
  - **Resolution**: Check if active sales uploads exist. Run a manual twin cache rebuild.

---

## 8. Broken Size Analysis FAQs & Troubleshooting

### FAQs
1. **Q: Broken status meaning?**
   - A: Fast-selling sizes are at 0 stock while other sizes sit on the shelf.
2. **Q: Broken size trigger limit?**
   - A: Core sizes (e.g. Size 7, 8) at 0 triggers broken status.
3. **Q: How to define core size set?**
   - A: Configure core size flags in Item Attributes.
4. **Q: Rebalancing actions for broken sizes?**
   - A: System recommends transfers of missing sizes from neighboring overstocked stores.
5. **Q: Does it check color variants?**
   - A: Yes, evaluates size curves per style-color template.
6. **Q: Frequency of analysis?**
   - A: Computed during the daily background twin rebuild.
7. **Q: Can we exclude slow models?**
   - A: Yes, untick 'Analyze curve' in Item master.
8. **Q: Wasted inventory cost?**
   - A: Financial value of non-moving sizes in a broken curve.
9. **Q: Size curves for apparel?**
   - A: Supports S, M, L, XL charts.
10. **Q: Broken size threshold?**
    - A: Default is any missing core size.

### Troubleshooting
- **Error**: `Broken sizes report empty`.
  - **Resolution**: Ensure item templates have correct 'Has Variants' attributes and active stock.

---

## 9. Outlet Health Score FAQs & Troubleshooting

### FAQs
1. **Q: Low Health Score impact?**
   - A: Blocks automatic transfer recommendations (unreliable data).
2. **Q: How to improve score?**
   - A: Upload sales sheets daily; perform counts on schedule.
3. **Q: Latency calculation logic?**
   - A: Days since last upload. 0 days = 100%, >5 days = 0%.
4. **Q: Compliance weights?**
   - A: 50% Upload latency, 50% Snapshot frequency.
5. **Q: Can we override score?**
   - A: No, score is system-calculated.
6. **Q: Alerts on low health?**
   - A: Automailers are dispatched to territory sales managers.
7. **Q: Target health level?**
   - A: Ideal target is >90%.
8. **Q: Grace period for score drop?**
   - A: 24 hours grace period for Sunday store closures.
9. **Q: Is it visible to store managers?**
   - A: Yes, displayed on SMRITI home screen.
10. **Q: Penalty rules?**
    - A: Stores below 60% health are flagged for manual audit.

### Troubleshooting
- **Error**: `Health score remains 0% after upload`.
  - **Resolution**: Check if the upload voucher has been Submitted. Draft uploads do not affect the score.

---

## 10. Sell Through Analytics FAQs & Troubleshooting

### FAQs
1. **Q: Sell through period defaults?**
   - A: Standard lookback is 30 days.
2. **Q: Sell Through formula?**
   - A: $\frac{\text{Sales Qty}}{\text{Starting Inventory + Receipts}} \times 100$.
3. **Q: Low sell through actions?**
   - A: Implement markdowns, or transfer stock out of the outlet.
4. **Q: Does it include returns?**
   - A: Net sales (Sales minus returns) are used.
5. **Q: Filter options?**
   - A: Filter by Category, Brand, Zone, and PSA.
6. **Q: Ideal sell-through %?**
   - A: >70% for hot styles, >50% for standard categories.
7. **Q: Calculation run time?**
   - A: Calculated instantly during twin rebuilds.
8. **Q: Can we run year-to-date reports?**
   - A: Yes, change the timespan range parameter.
9. **Q: Slow-moving category lists?**
    - A: Displays items with sell-through less than 20%.
10. **Q: Target inventory cap checks?**
    - A: Evaluated relative to sell-through trends.

### Troubleshooting
- **Error**: `Division by zero in sell-through calculation`.
  - **Resolution**: Triggered when a store has 0 starting stock and receipts. The system automatically handles this by returning 0.0%.

---

## 11. PDT Dashboard FAQs & Troubleshooting

### FAQs
1. **Q: Twin State meanings?**
   - A: `Healthy`, `Monitor`, `Replenish Soon`, `Critical`, `Stockout`, `Overstock`, `Dead Stock`.
2. **Q: PDT rebuild lock?**
   - A: Prevents queue storming by checking lock key `pdt_rebuild:{company}:{psa}:{item}`.
3. **Q: Metadata JSON contents?**
   - A: Holds versioning, duration, and source event tags for audit traceability.
4. **Q: Forecast version?**
   - A: Current release tag is PDT-2.0.1.
5. **Q: Freshness SLA levels?**
   - A: Fresh (<1hr), Aging (<24hrs), Stale (>24hrs).
6. **Q: Redis role?**
   - A: Accelerates dashboard load times by caching results.
7. **Q: Twin quality score?**
   - A: Calculated from data variance and latency checks.
8. **Q: Can we force twin rebuilds?**
   - A: Click "Trigger Rebuild" inside PDT panel.
9. **Q: Forecast Model options?**
   - A: Currently uses Exponential Moving Average (EMA).
10. **Q: Twin details view?**
    - A: Displays predictions, coverage, and recommendations in one screen.

### Troubleshooting
- **Error**: `Twin state shows Stale`.
  - **Resolution**: Check background job scheduler queue status. Run a force rebuild.

---

## 12. Stock-Out Prediction FAQs & Troubleshooting

### FAQs
1. **Q: Forecast lookback range?**
   - A: Defaults to last 28 days of sales data.
2. **Q: What is daily sales velocity EMA?**
   - A: Exponential Moving Average that weights recent days higher than past days.
3. **Q: Confidence score?**
   - A: Exponential decay metric calculated from standard deviation.
4. **Q: Predicted stockout calculation?**
   - A: $\frac{\text{Current Stock}}{\text{Daily Velocity EMA}}$.
5. **Q: Why does stockout date show None?**
   - A: The store has 0 sales velocity; stock will last indefinitely.
6. **Q: Volatility changes?**
   - A: Sudden sales spikes drop confidence levels.
7. **Q: Does it adjust for season?**
   - A: Uses seasonality factor defaults.
8. **Q: Forecast parameter changes?**
   - A: Updated in SMRITI settings.
9. **Q: Lead days calculations?**
   - A: Calculates predicted stockouts relative to shipping lead days.
10. **Q: Expected stockout alerts?**
    - A: Flashing red warning if stockout date is less than lead days.

### Troubleshooting
- **Error**: `Volatility confidence shows 100% with no sales`.
  - A: Correct. Certain forecast of zero daily sales.

---

## 13. Transfer Recommendation FAQs & Troubleshooting

### FAQs
1. **Q: Rebalancing target rules?**
   - A: Targets overstocked stores first.
2. **Q: Benefit score formula?**
   - A: $\text{Economic Benefit} = \text{Item Price} - \text{Freight} - \text{Transit Delay Penalty}$.
3. **Q: Freight costs per unit?**
   - A: Same zone: ₹6, Different zone: ₹18.
4. **Q: Transit Delay Penalties per unit?**
   - A: Same zone: ₹5, Different zone: ₹20.
5. **Q: Recommendation types?**
   - A: `TRANSFER` (inter-PSA) or `PURCHASE` (external).
6. **Q: Can we reject recommendations?**
   - A: Yes, click 'Dismiss Recommendation' to clear.
7. **Q: Automatic transfers?**
   - A: SMRITI Constitution Rule 10 prohibits automatic actions; manager approval required.
8. **Q: Source store safety stock buffer?**
   - A: Transfer suggestions never deplete source stock below its safety limits.
9. **Q: Reason code lists?**
   - A: `EXCESS_WOC_AT_SOURCE`, `POSITIVE_TRANSFER_BENEFIT`.
10. **Q: Rebalancing intervals?**
    - A: Calculated daily.

### Troubleshooting
- **Error**: `Recommendation type shows PURCHASE instead of TRANSFER`.
  - **Resolution**: Check if neighbor stores have excess stock above safety levels. If not, PROCUREMENT is recommended.

---

## 14. Simulation Sandbox FAQs & Troubleshooting

### FAQs
1. **Q: Will sandbox simulation overwrite live data?**
   - A: No. Run in-memory.
2. **Q: Multipliers available?**
   - A: Velocity multiplier, freight rate multiplier.
3. **Q: Simulation outputs?**
   - A: Simulates weeks of cover and stock-out dates.
4. **Q: Can we export simulation results?**
   - A: Click 'Export Simulation Results' to CSV.
5. **Q: Sandbox performance?**
   - A: Runs in less than 2 seconds.
6. **Q: Who can run simulations?**
   - A: Supervisors and Executives.
7. **Q: Simulation configs?**
   - A: Target specific items and outlets.
8. **Q: Multiple simulations?**
   - A: Sandbox runs are isolated in-memory per session.
9. **Q: Multiplier limits?**
   - A: Supports 0.1x to 10.0x multipliers.
10. **Q: How to reset?**
    - A: Click 'Clear Sandbox'.

### Troubleshooting
- **Error**: `Sandbox execution timed out`.
  - **Resolution**: Reduce the number of item codes or stores in filters and run again.

---

## 15. Audit & Variance Management FAQs & Troubleshooting

### FAQs
1. **Q: Variance reconciliation codes?**
   - A: `THEFT`, `DAMAGE`, `MISSING_IN_TRANSIT`, `DATA_ENTRY_ERROR`.
2. **Q: Variance approval rights?**
   - A: Enforced for Auditors and Managers only.
3. **Q: Shadow ledger adjustments?**
   - A: Ledger posts discrepancy correction entries instantly on approval.
4. **Q: What is a Liability Snapshot?**
   - A: Keeps a financial record of stock write-offs.
5. **Q: Auto-reconciliation?**
   - A: System matches item codes and highlights variances.
6. **Q: How to handle high variance?**
   - A: Flag the outlet for a manual physical audit.
7. **Q: Adjustments audit trail?**
   - A: Logged inside SMRITI Benefit Audit Log.
8. **Q: Reason requirements?**
   - A: Mandatory field for any variance adjustment.
9. **Q: Monthly limits?**
   - A: Adjustments caps apply per month.
10. **Q: Can we edit approved audits?**
    - A: Locked after submission.

### Troubleshooting
- **Error**: `Variance value exceeds approved limit`.
  - **Resolution**: High-value write-offs require Administrator login and approval.

---

## 16. Administration & Settings FAQs & Troubleshooting

### FAQs
1. **Q: Who can access settings?**
   - A: Only Administrators and System Managers.
2. **Q: Reorder Rules priority cascade?**
   - A: 1. Variant rule, 2. Item Group rule, 3. Global settings fallback.
3. **Q: Lead Time units?**
   - A: Configured in Days.
4. **Q: Safety Stock defaults?**
   - A: Applied when variant rules are not configured.
5. **Q: Rebuild interval config?**
   - A: Background rebuilds run hourly/daily.
6. **Q: SMRITI Constitution validation?**
   - A: Settings check for single source of truth rules.
7. **Q: Where is settings saved?**
   - A: SMRITI PSV Settings single doctype.
8. **Q: Can we import rules?**
   - A: Use data import tool for Reorder Rules.
9. **Q: Target Days Cover meaning?**
   - A: Desired inventory levels in days of sales.
10. **Q: Setting changes tracking?**
    - A: Logged in Audit Trail log.

### Troubleshooting
- **Error**: `Settings update failed due to validation rules`.
  - **Resolution**: Check if lead times or safety stocks are negative. Set positive values and retry.
