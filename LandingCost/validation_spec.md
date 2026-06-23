# SMRITI Landed Cost Allocation — Validation & Controller Spec

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
* **Document Version**: 1.1.0
* **Release Date**: 2026-06-22
* **Intended Audience**: SMRITI Core Engineering & Implementation Teams
* **Learning Objectives**: Understand the validated rules, execution sequence, database constraints, and performance controls for the SMRITI Landed Cost Allocation engine.
* **Support**: support@aitdl.example.com
* **Revision History**:
  * `v1.0.0` (2026-06-22): Initial Architecture Review.
  * `v1.1.0` (2026-06-22): Integrated G1-G8 Architecture board resolutions.

---

## 1. `validate()` — runs on every save (Draft state)

```python
def validate(doc):
    # --- Receipt-level checks ---
    if not doc.purchase_receipts:
        throw("At least one Purchase Receipt is required.")

    receipts = [get_doc("Purchase Receipt", r.purchase_receipt) for r in doc.purchase_receipts]

    for r in receipts:
        if r.docstatus != 1:
            throw(f"Purchase Receipt {r.name} must be Submitted.")
        if r.company != doc.company:
            throw(f"Purchase Receipt {r.name} belongs to a different Company.")

    currencies = {r.currency for r in receipts}
    if len(currencies) > 1:
        throw("All selected Purchase Receipts must use the same Currency.")

    doc.currency = list(currencies)[0]  # Sync parent doc currency

    # --- Cost Line checks ---
    if not doc.cost_lines:
        throw("At least one Cost Line is required.")

    for line in doc.cost_lines:
        if line.amount <= 0:
            throw(f"Cost Line '{line.cost_component}': amount must be greater than zero.")

        # G8 Rule: Ensure allocation_basis is populated. Fallback to doc default if blank.
        if not line.allocation_basis:
            line.allocation_basis = doc.allocation_method

        if line.source_type in ("Same Vendor Bill", "Third Party Bill"):
            if not line.source_reference:
                throw(f"Cost Line '{line.cost_component}': source_reference is mandatory "
                      f"for Source Type '{line.source_type}'.")
            
            inv = get_doc("Purchase Invoice", line.source_reference)
            if inv.docstatus != 1:
                throw(f"Referenced Purchase Invoice {inv.name} must be Submitted. "
                      f"Draft or Cancelled invoices cannot be used as a landed cost source.")

            # G7 Rule: Exact Currency Match Enforcement (Phase 1 Domestic constraint)
            if inv.currency != doc.currency:
                throw(f"Currency mismatch on Cost Line '{line.cost_component}': "
                      f"Referenced Purchase Invoice {inv.name} is in {inv.currency}, "
                      f"which does not match the Receipt currency {doc.currency}. "
                      f"Phase 1 enforces a strict currency match to prevent exchange rate corruption.")

            # G7 Rule: Same Vendor Bill Supplier match check
            if line.source_type == "Same Vendor Bill":
                receipt_suppliers = {r.supplier for r in receipts}
                if len(receipt_suppliers) > 1 or inv.supplier not in receipt_suppliers:
                    throw(f"Supplier mismatch on Cost Line '{line.cost_component}': "
                          f"Invoice supplier ({inv.supplier}) must match the supplier "
                          f"of the linked Purchase Receipt(s) for a Same Vendor Bill.")
                
                if line.amount > inv.grand_total:
                    throw(f"Cost Line amount ({line.amount}) exceeds the referenced Purchase "
                          f"Invoice total ({inv.grand_total}) -- check for double-counting.")

        if line.allocation_basis not in ("Value", "Qty", "Manual"):
            throw(f"Cost Line '{line.cost_component}': allocation_basis must be Value, Qty, or Manual.")

    if doc.allocation_method not in ("Value", "Qty", "Manual"):
        throw("allocation_method must be Value, Qty, or Manual.")

    if doc.valuation_basis != "Purchase Only":
        throw("valuation_basis must be 'Purchase Only' in Phase 1.")

    # --- Computed summary fields (G5: Exclude non-stock items) ---
    doc.base_purchase_value = sum(row.qty * row.rate for r in receipts for row in r.items if row.is_stock_item)
    doc.additional_cost = sum(l.amount for l in doc.cost_lines if l.affects_inventory_cost)
    doc.estimated_landed_cost = doc.base_purchase_value + doc.additional_cost

    # Value-basis zero-guard (G5: based exclusively on stock item value)
    using_value_basis = (doc.allocation_method == "Value" or
                          any(l.allocation_basis == "Value" for l in doc.cost_lines))
    if using_value_basis and doc.base_purchase_value == 0:
        throw("Value-basis allocation is prohibited when Total Base Purchase Value (Stock Items) = 0. "
              "Choose Qty or Manual allocation_basis instead.")

    if doc.base_purchase_value > 0:
        doc.landed_cost_percent = (doc.additional_cost / doc.base_purchase_value) * 100
    else:
        doc.landed_cost_percent = 0

    total_stock_qty = sum(row.qty for r in receipts for row in r.items if row.is_stock_item)
    doc.cost_per_unit = (doc.estimated_landed_cost / total_stock_qty) if total_stock_qty > 0 else 0

    # Early manual validation totals check (using G1 manual input child table)
    if doc.allocation_method == "Manual" or any(l.allocation_basis == "Manual" for l in doc.cost_lines):
        validate_manual_allocation_totals(doc)
```

---

## 2. `on_submit()` — populates snapshot and updates analytical costs

```python
def on_submit(doc):
    snapshot_rows = []

    # G4 Rule: Pre-calculate total quantity of stock items to prevent N+1 query performance bottleneck
    receipts_cache = {}
    total_qty = 0
    for rl in doc.purchase_receipts:
        r_doc = get_doc("Purchase Receipt", rl.purchase_receipt)
        receipts_cache[rl.purchase_receipt] = r_doc
        total_qty += sum(item.qty for item in r_doc.items if item.is_stock_item)

    # Generate snapshot rows for stock items only
    for receipt_name, receipt in receipts_cache.items():
        # G5 Rule: Exclude non-stock items
        stock_items = [item for item in receipt.items if item.is_stock_item]

        for item_row in stock_items:
            row_base_value = item_row.qty * item_row.rate

            for cost_line in doc.cost_lines:
                if not cost_line.affects_inventory_cost:
                    continue  # excluded charges don't get allocated/snapshotted

                basis = cost_line.allocation_basis or doc.allocation_method

                if basis == "Value":
                    allocated = (cost_line.amount * row_base_value) / doc.base_purchase_value if doc.base_purchase_value > 0 else 0
                elif basis == "Qty":
                    allocated = (cost_line.amount * item_row.qty) / total_qty if total_qty > 0 else 0
                elif basis == "Manual":
                    # G1 Rule: Retrieve from the child table SMRITI Landed Cost Manual Allocation
                    allocated = get_manual_allocation_from_db(doc, cost_line.name, item_row.name)
                else:
                    throw(f"Unrecognized allocation basis: {basis}")

                snapshot_rows.append({
                    "purchase_receipt": receipt.name,
                    "purchase_receipt_row": item_row.name,   # stable child-row name, NOT index
                    "allocated_to_sku": item_row.item_code,
                    "cost_component": cost_line.cost_component,
                    "qty": item_row.qty,
                    "base_value": row_base_value,
                    "allocated_cost": flt(allocated, 2),     # apply system currency precision
                    "currency": receipt.currency,
                    "allocation_method_used": basis,
                    "timestamp": now_datetime(),
                })

    # G6 Rule: Apply rounding remainders to prevent minor penny leaks
    adjust_rounding_remainders(doc, snapshot_rows)

    doc.set("audit_snapshot", snapshot_rows)
    doc.db_update()   # atomic write

    # G2 Rule: Update Item.estimated_landed_cost_last analytical cost fields
    update_item_analytical_costs(doc, snapshot_rows)
```

---

## 3. Helper Logic & Concurrency Guards

### 3.1 G2 Rule — Chronicle Order ("Latest Allocation" resolution)
To determine if a submitted document is the chronologically newest allocation for an item, we query submitted allocations (`docstatus = 1`) and compare:
1. `posting_date` (primary comparison)
2. `creation` timestamp (tiebreaker for allocations submitted on the same posting date)

```python
def check_if_latest_allocation(sku, current_posting_date, current_creation):
    """
    Checks if there is any other submitted SMRITI Landed Cost Allocation for the SKU
    with a newer posting_date, or a newer creation timestamp on the same posting_date.
    """
    newer_allocations = frappe.db.sql("""
        SELECT parent.name 
        FROM `tabSMRITI Allocation Audit Snapshot` child
        JOIN `tabSMRITI Landed Cost Allocation` parent ON child.parent = parent.name
        WHERE child.allocated_to_sku = %s
          AND parent.docstatus = 1
          AND (
              parent.posting_date > %s 
              OR (parent.posting_date = %s AND parent.creation > %s)
          )
        LIMIT 1
    """, (sku, current_posting_date, current_posting_date, current_creation))

    return len(newer_allocations) == 0
```

### 3.2 G2 Rule — Updating Item Master Analytical Cost
```python
def update_item_analytical_costs(doc, snapshot_rows):
    sku_costs = {}
    for row in snapshot_rows:
        sku = row["allocated_to_sku"]
        if sku not in sku_costs:
            sku_costs[sku] = {"base_value": 0.0, "allocated_cost": 0.0, "qty": 0.0}
        
        sku_costs[sku]["base_value"] += row["base_value"]
        sku_costs[sku]["allocated_cost"] += row["allocated_cost"]
        sku_costs[sku]["qty"] += row["qty"]

    for sku, data in sku_costs.items():
        if data["qty"] > 0:
            unit_cost = flt((data["base_value"] + data["allocated_cost"]) / data["qty"], 2)
            if check_if_latest_allocation(sku, doc.posting_date, doc.creation):
                frappe.db.set_value("Item", sku, "estimated_landed_cost_last", unit_cost)
```

### 3.3 G3 Rule — `on_cancel()` Reversion Query Path
On cancellation, the snapshot is kept intact but the SKU's cost is reverted by querying remaining submitted snapshot records.

```python
def on_cancel(doc):
    # The Audit Snapshot is NOT deleted or recomputed on cancel.
    # It remains as a historical record per Section 1.3 immutability principle.
    
    # G3 Rule: Find the most recent remaining submitted allocation in SMRITI Allocation Audit Snapshot
    impacted_skus = {row.allocated_to_sku for row in doc.audit_snapshot}
    
    for sku in impacted_skus:
        latest_snap = frappe.db.sql("""
            SELECT child.base_value, child.allocated_cost, child.qty, parent.posting_date, parent.creation
            FROM `tabSMRITI Allocation Audit Snapshot` child
            JOIN `tabSMRITI Landed Cost Allocation` parent ON child.parent = parent.name
            WHERE child.allocated_to_sku = %s
              AND parent.docstatus = 1
            ORDER BY parent.posting_date DESC, parent.creation DESC
            LIMIT 1
        """, (sku,), as_dict=True)
        
        if latest_snap:
            snap = latest_snap[0]
            unit_cost = flt((snap.base_value + snap.allocated_cost) / snap.qty, 2) if snap.qty > 0 else 0
            frappe.db.set_value("Item", sku, "estimated_landed_cost_last", unit_cost)
        else:
            # Fallback to standard valuation_rate if no allocations remain
            val_rate = frappe.db.get_value("Item", sku, "valuation_rate") or 0
            frappe.db.set_value("Item", sku, "estimated_landed_cost_last", val_rate)
```

### 3.4 G6 Rule — Penny Rounding Remainder Distribution
```python
def adjust_rounding_remainders(doc, snapshot_rows):
    """Distributes minor decimal discrepancy to the last item row of the allocation."""
    for cost_line in doc.cost_lines:
        if not cost_line.affects_inventory_cost:
            continue
        
        allocated_sum = sum(
            row["allocated_cost"] for row in snapshot_rows 
            if row["cost_component"] == cost_line.cost_component
        )
        difference = flt(cost_line.amount - allocated_sum, 2)
        
        # Apply remainder to the last snapshot row matching this cost component
        if abs(difference) > 0:
            for row in reversed(snapshot_rows):
                if row["cost_component"] == cost_line.cost_component:
                    row["allocated_cost"] = flt(row["allocated_cost"] + difference, 2)
                    break
```

---

## 4. Manual Allocations Details (G1 Child Table)

### 4.1 Schema Definition: `SMRITI Landed Cost Manual Allocation`
Child table of `SMRITI Landed Cost Allocation` with the following columns:
- `cost_line_ref`: Link (`SMRITI Landed Cost Line`) - refers to the specific cost row.
- `purchase_receipt`: Link (`Purchase Receipt`)
- `purchase_receipt_row`: Data - stable `name` of the item row inside the PR.
- `allocated_amount`: Currency - user inputted amount.

### 4.2 Manual Controller Validations
```python
def get_manual_allocation_from_db(doc, cost_line_id, item_row_name):
    # Fetch from manual allocation child table rows
    val = sum(
        row.allocated_amount for row in doc.manual_allocations 
        if row.cost_line_ref == cost_line_id and row.purchase_receipt_row == item_row_name
    )
    if val < 0:
        throw(f"Manual allocation row amount cannot be negative.")
    return val

def validate_manual_allocation_totals(doc):
    tolerance = 0.01
    
    # Verify totals per Cost Line
    for cost_line in doc.cost_lines:
        if cost_line.allocation_basis != "Manual":
            continue
            
        total = sum(
            row.allocated_amount for row in doc.manual_allocations 
            if row.cost_line_ref == cost_line.name
        )
        
        if abs(total - cost_line.amount) > tolerance:
            throw(f"Manual allocation rows for '{cost_line.cost_component}' sum to {total}, "
                  f"which does not match the Cost Line amount {cost_line.amount} "
                  f"(tolerance: {tolerance}).")
```

---

## 5. UI Ergonomics & Defaults (G8 Rule)

1. **Client Script Hook (`before_row_insert`)**:
   When the user adds a new row to `cost_lines`, a client script triggers to auto-populate `allocation_basis` with the parent document's `allocation_method` value, ensuring instant visibility in the grid.
2. **Uniqueness Index**:
   Add a unique constraint on child table `SMRITI Landed Cost Manual Allocation` for `(parent, cost_line_ref, purchase_receipt_row)` to prevent users from adding duplicate manual allocation rows for the same cost-item pair.

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

---
