# SMRITI Sales Force Management (SFM) — DocType Specifications (v1.0.0)

---

### Author Profile (Start)
* **Author**: Jawahar R. Mallah
* **Designation**: Founder & Chief Architect
* **Organization**: AITDL – AI Technology & Development Lab
* **Professional Experience**: 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.

#### Author Note
This specification manual is based on practical field experience gathered across retail operations, distribution management, inventory control, software architecture, business automation, and enterprise solution development. The objective is to make SMRITI Retail OS understandable and usable by both technical and non-technical users.

> "Light begins with learning."
> 
> — Jawahar R. Mallah
> Founder & Chief Architect, AITDL

---

## 1. SMRITI Customer Ownership

### Schema & Relationships
- **Name**: `SMRITI Customer Ownership`
- **Fields**:
  - `customer` (Link -> Customer, reqd, in_list_view): Linked ERPNext Customer.
  - `primary_owner` (Link -> Employee, reqd, in_list_view): Primary relationship manager.
  - `secondary_owner` (Link -> Employee, optional): Secondary relationship manager.
  - `start_date` (Date, reqd): Beginning date of relationship ownership.
  - `end_date` (Date, optional): Close out date of ownership.
  - `is_active` (Check, default=1, in_list_view): Active flag.
  - `company` (Link -> Company, reqd): Linked company.
- **Validations**:
  - `primary_owner` and `secondary_owner` cannot be the same employee.
  - Timeline consistency: `start_date` must be less than or equal to `end_date`.
  - Chronological Integrity: When ownership is updated, the old active record has `end_date` set to `yesterday` and `is_active = 0`. The new active record has `start_date = today` and `is_active = 1`.

---

## 2. SMRITI Sales Target

### Schema & Relationships
- **Name**: `SMRITI Sales Target`
- **Fields**:
  - `employee` (Link -> Employee, reqd, in_list_view): Assigned employee.
  - `company` (Link -> Company, reqd): Target company.
  - `fiscal_year` (Link -> Fiscal Year, reqd): target financial year.
  - `month` (Select, reqd, in_list_view): `Jan` to `Dec`.
  - `target_amount` (Currency, reqd): Target revenue amount.
  - `target_qty` (Float, optional): Target quantities.
- **Validations**:
  - Unique composite index on `(employee, company, fiscal_year, month)`.

---

## 3. SMRITI SFM Settings

### Schema & Relationships
- **Name**: `SMRITI SFM Settings`
- **Classification**: Single DocType
- **Fields**:
  - `enable_sfm` (Check, default=0): Toggle SFM engine.
  - `ownership_precedence` (Check, default=1): Set whether ownership takes precedence over invoice `sales_team`.
  - `primary_split_pct` (Percent, default=70): Share for Primary Owner.
  - `secondary_split_pct` (Percent, default=30): Share for Secondary Owner.
  - `walkin_employee` (Link -> Employee, optional): Fallback executive for unassigned sales.

---

## 4. SMRITI Attribution Rule

### Schema & Relationships
- **Name**: `SMRITI Attribution Rule`
- **Classification**: Reserved (Future-proofing placeholder)
- **Fields**:
  - `rule_name` (Data, reqd)
  - `is_active` (Check)

---

## 5. SMRITI Attribution Event

### Schema & Relationships
- **Name**: `SMRITI Attribution Event`
- **Fields**:
  - `invoice_reference` (Data, reqd, in_list_view): POS Invoice / Sales Invoice name.
  - `invoice_doctype` (Data, reqd): Doctype name.
  - `customer` (Link -> Customer, reqd): Customer.
  - `company` (Link -> Company, reqd): Company.
  - `posting_date` (Date, reqd): Date.
  - `posting_time` (Time, reqd): Time.
  - `grand_total` (Currency, reqd): Total.
  - `net_total` (Currency, reqd): Revenue base.
  - `status` (Select, reqd, default="Pending", in_list_view): `Pending`, `Processed`, `Reversed`.
  - `error_message` (Small Text, optional).

---

## 6. SMRITI Attribution Ledger

### Schema & Relationships
- **Name**: `SMRITI Attribution Ledger`
- **Fields**:
  - `invoice_reference` (Data, reqd, in_list_view): Source invoice ID.
  - `invoice_doctype` (Data, reqd): Doctype name.
  - `customer` (Link -> Customer, reqd, in_list_view): Customer ID.
  - `employee` (Link -> Employee, reqd, in_list_view): Employee ID receiving credit.
  - `ownership_type` (Select, reqd, in_list_view): `Primary`, `Secondary`, `Walk-In`, `Service`.
  - `revenue_credit` (Currency, reqd): Calculated revenue credit.
  - `credit_percentage` (Percent, reqd): Allocation percentage.
  - `store` (Link -> SMRITI Store, reqd): Store entity.
  - `warehouse` (Link -> Warehouse, optional): Specific warehouse source.
  - `posting_date` (Date, reqd): Date.
  - `posting_time` (Time, reqd): Time.
  - `source_document` (Data, reqd): Source invoice.
  - `ledger_status` (Select, reqd, default="Active", in_list_view): `Active`, `Superseded`, `Reversed`.
  - `reversal_reference` (Data, optional): Reversal ledger name.
  - `company` (Link -> Company, reqd): Company.

---

## 7. SMRITI Sales KPI Snapshot

### Schema & Relationships
- **Name**: `SMRITI Sales KPI Snapshot`
- **Fields**:
  - `employee` (Link -> Employee, reqd, in_list_view): Employee.
  - `store` (Link -> SMRITI Store, reqd, in_list_view): Store.
  - `date` (Date, reqd, in_list_view): Date of aggregation.
  - `revenue` (Currency, reqd): Daily total revenue credit.
  - `transactions` (Int, reqd): Daily transaction count.
  - `customers` (Int, reqd): Unique customer count.
  - `company` (Link -> Company, reqd): Company.
