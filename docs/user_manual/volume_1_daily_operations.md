# SMRITI Retail OS User Manual — Volume 1: Daily Operations Guide

Welcome to the **SMRITI Retail OS Daily Operations Guide**. This manual is designed for store operators, salesmen, stock auditors, and distributor managers. You do not need any technical background, coding skills, or database knowledge to use SMRITI. We explain everything using simple business language, practical retail examples, and Hinglish (mixed English and Hindi) explanations where helpful.

---

## Chapter 1: Customer Master (ग्राहक पंजी)

### 1. Purpose (उद्देश्य)
SMRITI operates on a partner-driven model. The **Customer Master** module exists to register every party (Distributor, Retailer, Multi-Brand Outlet, or Franchisee) who buys goods from your company. 
- **Business Problem Solved**: Without a single, locked customer register, sales data gets mixed up, credit terms are breached, and stock visibility is lost across outlets. This module gives every distributor and store a unique identity in the system.

### 2. Real-Life Example (वास्तविक जीवन का उदाहरण)
Imagine you run a footwear brand, **"StepFit Shoes"**. You sell to three outlets:
1. **Mumbai Grand Mall** (Franchise Outlet)
2. **Pune Plaza Footwear** (Distributor Outlet)
3. **Nagpur Shoe Palace** (Multi-Brand Retailer)

Before you upload sales data or check inventory, you must register these three stores as customers in the Customer Master.

### 3. Step-by-Step Entry Process (प्रविष्टि प्रक्रिया)
1. **Menu Path**: SMRITI Home → Master Data → Customer Master → **New Customer**
2. **Fill in Required Fields**: Enter the Customer Name, Group, and Tax Territory.
3. **Save and Submit**: 
   - Click **Save** (ड्राफ्ट सेव करें) in the top-right corner.
   - Review details, then click **Submit** (जमा करें) to make the record permanent.

[Screenshot: Customer Master Form]

| Step | Action | Button to Click | System Behavior |
| :--- | :--- | :--- | :--- |
| 1 | Create Draft | Save | Saves details as Draft; changes allowed. |
| 2 | Finalize | Submit | Locks record; no changes allowed without amendment. |

### 4. Field-by-Field Explanation (फील्ड स्पष्टीकरण)

| Field Name (फील्ड का नाम) | Type | Mandatory? | Simple English & Hinglish Explanation | Example Value |
| :--- | :--- | :--- | :--- | :--- |
| **Customer Name** | Text | **Yes** | Party का नाम (Name of the outlet or distributor). | `Pune Plaza Footwear` |
| **Customer Group** | Link | **Yes** | Category type. (Distributor, Retail Outlet, or Corporate). | `Distributor` |
| **Territory** | Link | **Yes** | State or Region location. (Tax and shipping zone determination). | `Maharashtra` |
| **Billing Currency** | Link | No | Currency for transactions (Defaults to INR). | `INR` |
| **Credit Limit** | Float | No | Maximum outstanding amount allowed. (उधार सीमा). | `500,000` |

### 5. Example Transaction (उदाहरण प्रविष्टि)
Let's register **Nagpur Shoe Palace**:
- **Customer Name**: Nagpur Shoe Palace
- **Customer Group**: Retailer
- **Territory**: Maharashtra - Zone 2
- **Credit Limit**: 200,000 INR
- **Expected Output**: A unique customer ID `CUST-0034` is generated. You can now link sales invoices to this party.

### 6. Reports & Analysis (रिपोर्ट और विश्लेषण)
- **Report Name**: **Customer Balances & Aging Report**
- **How to Read**: Shows total credit outstanding (बकाया राशि) and how old the debt is (30 days, 60 days, etc.).
- **Management Action**: If outstanding credit exceeds 90 days, suspend stock dispatches.

### 7. Common Mistakes (सामान्य गलतियां)
1. **Creating Duplicate Customers**: Registering `Nagpur Shoe Palace` and `Nagpur Shoe Palace Ltd.` separately.
   - *How to Fix*: Check active customer names before creating a new one. Merge duplicate records using the Customer Merge tool.
2. **Missing Tax Territory**: Leaving Territory blank, causing incorrect GST calculation.
   - *How to Fix*: Edit draft and select the correct territory before submitting.

### 8. Business Interpretation (व्यावसायिक व्याख्या)
- **Warning Sign**: Credit Limit utilization is at 98% with an average payment delay of 45 days.
- **Decision**: Restrict fresh order approvals until payment is received.

### 9. Frequently Asked Questions (FAQs)
1. **Can I delete a Customer once submitted?**
   - No, if transactions exist. You can only set the status to "Disabled".
2. **What does Credit Limit do?**
   - It blocks Sales Upload or Invoicing if the outstanding balance exceeds this value.
3. **How do I change a customer's address?**
   - Click on the "Address" link inside the Customer Master and add a new address.
4. [Remaining 7 FAQs detailed in Volume 4 Troubleshooting Handbook]

### 10. Troubleshooting (समस्या निवारण)
- **Error**: `Credit Limit Exceeded for Customer Nagpur Shoe Palace`.
- **Resolution**: Request payment from the customer, or have a Sales Manager temporarily increase the Credit Limit in settings.

---

## Chapter 2: Item Master (सामग्री पंजी)

### 1. Purpose (उद्देश्य)
SMRITI sells size-wise and variant-wise products. The **Item Master** is the single source of truth for all products, sizes, prices, and GST HSN codes.
- **Business Problem Solved**: If salesmen use different names for the same shoe size (e.g., "Size 8", "UK8", "8 Number"), inventory tracking breaks down completely. Item Master standardizes codes.

### 2. Real-Life Example (वास्तविक जीवन का उदाहरण)
StepFit Shoes sells a sneaker model: **"Flyrunner Blue"**. It comes in sizes: **6, 7, 8, 9**.
Instead of creating 4 separate products manually, you create one **Template Item** (`Flyrunner Blue`) and generate 4 **Variant Items** (`Flyrunner-Blue-6`, `Flyrunner-Blue-7`, etc.).

### 3. Step-by-Step Entry Process (प्रविष्टि प्रक्रिया)
1. **Menu Path**: SMRITI Home → Inventory → Item Master → **New Item**
2. **For Template**: Check the box **"Has Variants"** (वेरिएंट हैं).
3. **Specify Attributes**: Select "Size" attribute and add values `6, 7, 8, 9`.
4. **Click "Save" and "Create Variants"** to auto-generate the size codes.

[Screenshot: Item Master Sizing Form]

### 4. Field-by-Field Explanation (फील्ड स्पष्टीकरण)

| Field Name | Type | Mandatory? | Explanation | Example Value |
| :--- | :--- | :--- | :--- | :--- |
| **Item Code** | Text | **Yes** | Product का unique code. (Barcode representation). | `SF-FLY-BLU` |
| **Item Name** | Text | **Yes** | Product name. | `Flyrunner Blue Sneaker` |
| **Has Variants** | Checkbox | No | Tick if product has multiple sizes or colors. | Checked (1) |
| **Standard Selling Rate** | Float | No | Selling price per unit (₹). | `2,499.00` |
| **GST HSN Code** | Link | **Yes** | GST Tax classification code. | `64041190` (Footwear) |

### 5. Example Transaction (उदाहरण प्रविष्टि)
- **Template Code**: `SF-FLY-BLU`
- **Attribute**: `Shoe Size`
- **Values**: `7, 8, 9`
- **Result**: System auto-creates `SF-FLY-BLU-7`, `SF-FLY-BLU-8`, and `SF-FLY-BLU-9` in the database.

### 6. Reports & Analysis (रिपोर्ट और विश्लेषण)
- **Report Name**: **Item Master Directory & Sizing Grid**
- **How to Read**: Displays list of active products with their GST HSN codes and prices.
- **Action**: Check for items missing HSN codes to prevent billing blocks.

### 7. Common Mistakes (सामान्य गलतियां)
- **Creating size variants manually**: Creating `SF-FLY-BLU-7` as a standard item instead of generating it through the template. This breaks size-curve reporting.
- *How to Fix*: Delete the manually created item, and generate variants via the template.

### 8. Business Interpretation (व्यावसायिक व्याख्या)
- **Warning Sign**: Item variant prices differ within the same category (e.g. Size 7 is ₹2499, Size 8 is ₹2699 due to manual entry errors). Standardize templates.

### 9. Frequently Asked Questions (FAQs)
1. **What is HSN Code?**
   - Harmonized System of Nomenclature code used by GST to determine tax rate.
2. [Remaining FAQs detailed in Volume 4]

### 10. Troubleshooting (समस्या निवारण)
- **Error**: `GST HSN Code is mandatory for Footwear category`.
- **Resolution**: Select the active HSN code field and link it to code `64041190`.

---

## Chapter 3: Party Stock Account - PSA (पार्टी स्टॉक खाता)

### 1. Purpose (उद्देश्य)
A **Party Stock Account (PSA)** represents a physical location where stock is stored (e.g. Distributor Warehouse, Retail Shop Counter, Franchise Store).
- **Business Problem Solved**: Tracks stock at external partner stores. The PSA connects a Customer Master ID with an inventory balance sheet (Shadow Ledger).

### 2. Real-Life Example (वास्तविक जीवन का उदाहरण)
StepFit Shoes registers **Pune Plaza Footwear** as a customer. Pune Plaza has a main warehouse and a showroom. You create two PSAs:
1. `Pune Plaza - Main WH` (Zone: West)
2. `Pune Plaza - Showroom` (Zone: West)

### 3. Step-by-Step Entry Process (प्रविष्टि प्रक्रिया)
1. **Menu Path**: SMRITI Home → Masters → Party Stock Account → **New PSA**
2. **Fill Fields**: Link to the Customer, select the Location, and define the Zone (East, West, North, South).
3. **Submit**: Save and click submit.

[Screenshot: PSA Configuration Page]

### 4. Field-by-Field Explanation (फील्ड स्पष्टीकरण)

| Field Name | Type | Mandatory? | Explanation | Example Value |
| :--- | :--- | :--- | :--- | :--- |
| **Account Name** | Text | **Yes** | Unique identifier for store location. | `Pune Plaza Showroom` |
| **Customer** | Link | **Yes** | Link to Customer Master register. | `Pune Plaza Footwear` |
| **Zone** | Select | **Yes** | Region (Important for transport cost math). | `West` |
| **Active** | Checkbox | No | Set to 0 if store is shut down. | Checked (1) |

### 5. Example Transaction (उदाहरण प्रविष्टि)
- **Account Name**: `Nagpur Outlet 1`
- **Customer**: `Nagpur Shoe Palace`
- **Zone**: `West`
- **Output**: Account created. When StepFit ships stock to Nagpur, it will post to `Nagpur Outlet 1` PSA.

### 6. Reports & Analysis (रिपोर्ट और विश्लेषण)
- **Report Name**: **PSA Directory & Location Map**
- **Action**: Verify store zones to ensure correct logistics routing.

### 7. Common Mistakes (सामान्य गलतियां)
- **Wrong Zone selection**: Assigning a North Indian store to the South Zone. This distorts the rebalancing cost calculations.
- *How to Fix*: Correct the Zone field and save.

### 8. Business Interpretation (व्यावसायिक व्याख्या)
- **Decision**: Multiple PSAs in the same city (e.g. Pune) allow quick inter-store stock transfers at low freight cost.

### 9. FAQs
1. **Can a PSA belong to multiple customers?**
   - No, a PSA is owned by exactly one customer.

### 10. Troubleshooting (समस्या निवारण)
- **Error**: `Customer Link invalid`.
- **Resolution**: Ensure the Customer is active and submitted in the Customer Master first.

---

## Chapter 4: Sales Upload (बिक्री अपलोड)

### 1. Purpose (उद्देश्य)
Outlets sell goods to walk-in retail customers. SMRITI must record these sales daily to keep shadow stock balances accurate. Since outlets use different billing systems, the **Sales Upload** module accepts simple Excel/TSV sheets.
- **Business Problem Solved**: Avoids manual entry of thousands of daily retail receipts. Upload the daily summary sheet in seconds.

### 2. Real-Life Example (वास्तविक जीवन का उदाहरण)
On Friday evening, **Mumbai Grand Mall** sells:
- 10 pairs of `Flyrunner-Blue-8`
- 5 pairs of `Flyrunner-Blue-9`
The store manager exports the bill list to a TSV file and uploads it into SMRITI.

### 3. Step-by-Step Entry Process (प्रविष्टि प्रक्रिया)
1. **Menu Path**: SMRITI Home → Operations → Sales Upload → **New Sales Upload**
2. **Select Parameters**: Set Company, PSA, and Posting Date.
3. **Upload File**: Click **Attach** and upload the daily sales Excel/TSV sheet.
4. **Validate**: Click **Parse Data**. The system will scan for invalid sizes.
5. **Submit**: Click **Submit** to process ledger entries.

[Screenshot: Sales Upload Sheet Parsing]

### 4. Field-by-Field Explanation (फील्ड स्पष्टीकरण)

| Field Name | Type | Mandatory? | Explanation | Example Value |
| :--- | :--- | :--- | :--- | :--- |
| **Party Stock Account** | Link | **Yes** | PSA location where sales occurred. | `Mumbai Grand Mall` |
| **Posting Date** | Date | **Yes** | Date of actual sales. | `2026-06-19` |
| **Attached File** | File | **Yes** | Excel/TSV file containing columns: `item_code`, `qty`. | `mumbai_sales_19062026.tsv` |

### 5. Example Transaction (उदाहरण प्रविष्टि)
- **PSA**: `Mumbai Grand Mall`
- **File Content**:
  | item_code | qty |
  | :--- | :--- |
  | `SF-FLY-BLU-8` | 10 |
- **Expected Output**: Balance for `SF-FLY-BLU-8` at `Mumbai Grand Mall` drops by 10 units in the shadow ledger.

### 6. Reports & Analysis (रिपोर्ट और विश्लेषण)
- **Report Name**: **Sales Upload Log & Progress**
- **Action**: Check if any store has missed uploading data for more than 48 hours.

### 7. Common Mistakes (सामान्य गलतियां)
- **Uploading wrong file format**: Trying to upload a PDF or image instead of Excel/CSV/TSV.
- *How to Fix*: Export file as CSV from the store POS system and retry.

### 8. Business Interpretation (व्यावसायिक व्याख्या)
- **Warning Sign**: Sales upload shows high quantities of a single size sold on a single day. Check for manual data entry exaggeration or wholesale dumping.

### 9. FAQs
1. **Does uploading sales affect accounting ledger?**
   - No. It only affects the SMRITI shadow inventory balance.

### 10. Troubleshooting (समस्या निवारण)
- **Error**: `Row 12: Item Variant Code SF-FLY-BLU-13 not found in Item Master`.
- **Resolution**: Check the variant code in the Excel sheet. Correct the size label (e.g. 13 does not exist) and re-upload.

---

## Chapter 5: Party Stock Ledger (पार्टी स्टॉक लेजर)

### 1. Purpose (उद्देश्य)
The **Party Stock Ledger** is a read-only transaction ledger that registers every stock movement:
- **Stock In (Receipts)**: Shipment received from company factory (+ qty).
- **Stock Out (Sales)**: Sales uploaded by store manager (- qty).
- **Adjustments**: Physical count audit corrections.
- **Business Problem Solved**: Tracks audit trails of inventory leakage. Every shoe must be accounted for.

### 2. Real-Life Example (वास्तविक जीवन का उदाहरण)
On June 1st, **Pune Plaza** receives 100 shoes. (Ledger Balance = 100).
On June 2nd, they sell 10 shoes. (Ledger balance = 90).
On June 3rd, they receive another 50. (Ledger balance = 140).
The ledger lists these transactions sequentially.

### 3. Step-by-Step View Process (लेजर देखने की प्रक्रिया)
1. **Menu Path**: SMRITI Home → Reports → Party Stock Ledger
2. **Filters**: Select Company, PSA, and Item Code.
3. **Run**: Click **Show Report**.

[Screenshot: Ledger Entry List]

### 4. Field-by-Field Explanation (फील्ड स्पष्टीकरण)

| Field Name | Type | Explanation | Example |
| :--- | :--- | :--- | :--- |
| **Posting Datetime** | Datetime | Date and time of stock transaction. | `2026-06-19 12:00:00` |
| **Voucher Type** | Text | Document source (Sales, Delivery Note, Snapshot). | `Sales Upload` |
| **Voucher No** | Link | Link to source document. | `SU-0012` |
| **Quantity (Qty)** | Float | Change in stock (+ is stock in, - is sales). | `-5.0` |
| **Cumulative Balance** | Float | Final stock balance after transaction. | `85.0` |

### 5. Example Output (लेजर का उदाहरण)

| Date | Voucher | Qty | Running Balance |
| :--- | :--- | :--- | :--- |
| 2026-06-18 | Delivery Note (DN-01) | +50 | 50 |
| 2026-06-19 | Sales Upload (SU-09) | -12 | 38 |

### 6. Reports & Analysis (रिपोर्ट और विश्लेषण)
- Compare the ledger running balance with the store physical shelf count. If running balance is 38 but physical shelf has 35, there is a discrepancy of 3 units.

### 7. Common Mistakes (सामान्य गलतियां)
- **Misinterpreting time order**: Looking at transactions sorted by date only, which can mix up order if multiple uploads happen on the same day. Always check the **Posting Datetime** column for exact sorting.

### 8. Business Interpretation (व्यावसायिक व्याख्या)
- **Decision**: Slow stock turnover in ledger indicates dead stock. Shift stock to high-velocity stores.

### 9. FAQs
1. **Can I manually add a row in the ledger?**
   - No. Ledger rows are generated automatically when you submit transactions (e.g. Sales Upload, Delivery Note).

### 10. Troubleshooting (समस्या निवारण)
- **Error**: `Ledger balance is negative`.
- **Resolution**: Ensure opening balances or Delivery Notes were submitted before uploading sales. SMRITI does not allow negative stock adjustments.

---

## Chapter 6: Physical Snapshot (भौतिक स्टॉक गणना)

### 1. Purpose (उद्देश्य)
The **Physical Snapshot** module records the actual count of inventory on the outlet's shelves at a specific moment.
- **Business Problem Solved**: System balances (Shadow Ledger) can drift due to theft, entry mistakes, or damage. Physical stock counts resolve discrepancies.

### 2. Real-Life Example (वास्तविक जीवन का उदाहरण)
The auditor visits **Nagpur Shoe Palace** on month-end. SMRITI shows a balance of 85 units for `Flyrunner-Blue-8`. The auditor physically counts the shelves and finds only 82 units. 
They submit a Physical Snapshot of 82 units.

### 3. Step-by-Step Entry Process (प्रविष्टि प्रक्रिया)
1. **Menu Path**: SMRITI Home → Operations → Physical Snapshot → **New Snapshot**
2. **Parameters**: Select PSA and Audit Date.
3. **Scan/Enter Items**: Enter the item variant codes and the physical quantities counted.
4. **Submit**: Save and click submit. SMRITI will auto-adjust the ledger balance.

[Screenshot: Physical Snapshot Form]

### 4. Field-by-Field Explanation (फील्ड स्पष्टीकरण)

| Field Name | Type | Mandatory? | Explanation | Example Value |
| :--- | :--- | :--- | :--- | :--- |
| **Party Stock Account** | Link | **Yes** | Store location being audited. | `Nagpur Shoe Palace` |
| **Audit Date** | Date | **Yes** | Date when counting happened. | `2026-06-19` |
| **Items List (Grid)** | Table | **Yes** | Table of counted item codes and quantities. | `Flyrunner-Blue-8: 82` |

### 5. Example Transaction (उदाहरण प्रविष्टि)
- **System Balance**: 85 units
- **Physical Count**: 82 units
- **Snapshot Submit**: System generates a reconciliation entry of `-3` units in the ledger to align the balance.

### 6. Reports & Analysis (रिपोर्ट और विश्लेषण)
- **Report Name**: **Physical Audit Variance Report**
- **Action**: Investigate stores with high variance (>5% of total stock) for operational leaks.

### 7. Common Mistakes (सामान्य गलतियां)
- **Counting the same shelf twice**: Double-scanning shoe boxes.
- *How to Fix*: Clear the snapshot draft and scan methodically shelf-by-shelf.

### 8. Business Interpretation (व्यावसायिक व्याख्या)
- **Warning Sign**: Recurrent negative variance adjustments at the same store indicate pilferage or poor management.

### 9. FAQs
1. **How often should we submit snapshots?**
   - Best practice is weekly for high-value items, monthly for full stores.

### 10. Troubleshooting (समस्या निवारण)
- **Error**: `Snapshot Date cannot be in the future`.
- **Resolution**: Set the Audit Date to today's date or a past date.
