# ACP-BARCODE-003 — SMRITI BARCODE STUDIO V2.4A LAYOUT AND OPERATIONS UPGRADE

## Document Classification
* **Document ID:** ACP-BARCODE-003
* **Version:** 1.0
* **Status:** APPROVED (Chief Architect Governance Review)
* **Authority:** SMRITI Governance Framework
* **Owner:** Jawahar R. Mallah, Founder & Chief Architect
* **Organization:** AITDL
* **Effective Date:** 2026-06-21

---

## 1. Author Profile & Credibility

### Author Profile
- **Author:** Jawahar R. Mallah
- **Designation:** Founder & Chief Architect
- **Organization:** AITDL – AI Technology & Development Lab
- **Professional Experience:** 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.

### Author Note
This manual is based on practical field experience gathered across retail operations, distribution management, inventory control, software architecture, business automation, and enterprise solution development. The objective is to make SMRITI Retail OS understandable and usable by both technical and non-technical users.

### Quote
> "Light begins with learning."
> 
> — Jawahar R. Mallah
> Founder & Chief Architect, AITDL

---

## 2. Background & Objective

Warehouse barcode printing in footwear and apparel retail involves high-volume SKU management. Operators regularly print barcode labels for incoming goods or clear outstanding SKU print backlogs. The legacy Barcode Studio interface lacked workflow ergonomics, sequential loading tools, and granular transaction filtering. 

`ACP-BARCODE-003` defines the architectural changes, database lookup rules, and frontend layout modifications introduced in **SMRITI Barcode Studio V2.4a**. This upgrade transforms the design-time canvas into a robust, widescreen, 3-panel operations workplace built for warehouse throughput.

---

## 3. Technical Specifications & Business Rules

### 3.1. Warehouse Article Range Loader
To streamline batch printing, operators can fetch a sequential range of article codes.
* **Mechanism**: Input parameters `From Article` (e.g., `BBM-0001`) and `To Article` (e.g., `BBM-0100`) are parsed using standard regular expressions.
* **Generation Logic**: The system identifies the alphanumeric split. The prefix (`BBM-`) is extracted, and the numeric suffix is incremented sequentially (from `0001` to `0100` maintaining padding format).
* **Database Resolution**: Evaluates generated style codes against active database items in a single query:
  $$\text{Target Styles} = \{ \text{Item} \mid \text{Item.item\_code} \in \text{Range} \}$$

### 3.2. Automatic Variant Expansion
Fashion retail models require size-color variant combinations to be generated from a parent style code.
* **Logic**: When style codes (either loaded via range loader or input directly) are submitted, the expansion engine scans the database for variant SKUs.
* **Query Optimization**: Runs a bulk query:
  ```sql
  SELECT name, item_name, custom_brand, custom_color, custom_size 
  FROM `tabItem` 
  WHERE variant_of = %s AND disabled = 0;
  ```
* **Insertion**: Generates variant rows (e.g. `BBM-001-NAVY-S`) and appends them to the worksheet.

### 3.3. Interactive Worksheet Grid
Renders a 9-column interactive grid for detailed print queue management:
1. `Select` (Checkboxes for batch actions)
2. `Article` (SKU Code)
3. `Item Name` (Description)
4. `Brand` (Product Brand)
5. `Color` (Variant Color)
6. `Size` (Variant Size)
7. `Barcode` (Primary/Resolved Barcode)
8. `MRP` (Derived Maximum Retail Price)
9. `Qty / Labels` (Input print quantity count)

### 3.4. Dynamic Mapping Preview
The left sidebar includes an interactive preview rendering actual database values mapped to ZPL/TSPL tags:
* `{barcode}` $\rightarrow$ `8901234567890` (Primary resolved barcode)
* `{item_code}` $\rightarrow$ `BBM-0001-NAVY-S`
* `{item_name}` $\rightarrow$ `Flyrunner Sports Shoe`
* `{brand}` $\rightarrow$ `Adidas`
* `{mrp}` $\rightarrow$ `1999`

### 3.5. Transaction Expansion Modal
When fetching transaction logs (Purchase Receipts, POs, GRNs), the system displays the total items found and opens a selection dialog with filters:
* **Select All**: Check all items in the transaction.
* **Only Missing Labels**: Selects items where no primary barcode exists in the database.
* **Only New SKUs**: Filters items that have not been printed in recent history.

### 3.6. Box & Carton Packing Rules
Quantity calculations support carton-level packing configurations.
* **Formula**:
  $$\text{Labels Qty} = \text{Boxes} \times \text{Multiplier}$$
  *Where multiplier is defined in Item Master pack settings (e.g., 1 Box = 12 Pairs).*

### 3.7. Rate & MRP Fallback Rules
To prevent blank price labels, missing prices are resolved using a 3-layer lookup chain:
1. **Level 1**: Variant-specific `custom_mrp` or `standard_rate` on the Item Variant record.
2. **Level 2**: Active Price Lists matching standard selling or MRP lists for the SKU.
3. **Level 3 (Fallback)**: Core template prices inherited from the parent template item.

### 3.8. Persistent Reprint Queue
Saves print job histories locally in the browser (`localStorage`) to allow instant reprint operations for recent batches without re-querying transactions.

---

## 4. UI/UX Ergonomics & Layout

A widescreen **3-Panel Layout** organizes the operations center:
* **Panel 1 (Left Sidebar)**: Settings panel holding template selectors, printer configurations, and dynamic mapping previews.
* **Panel 2 (Center Worksheet)**: Houses the interactive 9-column grid with bulk quantity modifiers.
* **Panel 3 (Right Drawer)**: Contains range loading tools and collapsible transaction filters.
* **Sticky Footer Toolbar**: Always-visible bottom toolbar containing action triggers (Print, Clear, Re-verify) with dynamic disabled-state indicators based on row selection.

---

## 5. Document Revision History

| Date | Version | Description | Author |
| :--- | :--- | :--- | :--- |
| 2026-06-21 | 1.0 | Initial release detailing SMRITI Barcode Studio V2.4a layout and operational enhancements. | Jawahar R. Mallah |
