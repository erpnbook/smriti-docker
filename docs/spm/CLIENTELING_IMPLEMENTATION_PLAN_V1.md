# SMRITI Clienteling & Walk-In Intelligence — Phase 1 Implementation Plan (v1.2.0)

---

### Author Profile (Start)
* **Author**: Jawahar R. Mallah
* **Designation**: Founder & Chief Architect
* **Organization**: AITDL – AI Technology & Development Lab
* **Professional Experience**: 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.

#### Author Note
This implementation manual is based on practical field experience gathered across retail operations, distribution management, inventory control, software architecture, business automation, and enterprise solution development. The objective is to make SMRITI Retail OS understandable and usable by both technical and non-technical users.

> "Light begins with learning."
> 
> — Jawahar R. Mallah
> Founder & Chief Architect, AITDL

---

## 1. Purpose & Scope

This document specifies the technical implementation plan for **SMRITI Phase 5A (Unified Customer Graph)**, **Walk-In Intelligence**, and the **SMRITI Clienteling Engine**. 

It implements the [CUSTOMER_GRAPH_ARCHITECTURE_V1.md](file:///d:/Smriti_Retail_OS/docs/spm/CUSTOMER_GRAPH_ARCHITECTURE_V1.md) specification by outlining database schemas, background jobs, hook definitions, and test plans.

Our core objectives are:
1. **Materialize the Customer Graph**: Create the system database layer (`SMRITI Customer Graph`) to store computed transactional metrics.
2. **Expose the Presentation Layer**: Compile the presentation snapshot (`SMRITI Customer Profile`) for sub-10ms checkout lookups.
3. **Log Clienteling Interactions**: Provision `SMRITI Customer Interaction` to record customer touchpoints (Phone, WhatsApp, Store Visits) and track outcome events.
4. **Implement Walk-In Funnel**: Trace footfalls through a state machine (`Registered` -> `Browsing` -> `Assisted` -> `Converted` / `Exited`).
5. **Decouple and Defer Execution**: Perform calculations asynchronously in background worker queues on document events to avoid locking checkout operations.

---

## 2. User Review Required

> [!IMPORTANT]
> **FRZ-CLI-001: Customer Profile Read-Only Invariant**
> The `SMRITI Customer Graph` and `SMRITI Customer Profile` DocTypes are entirely derived and read-only. Standard users and cashier interfaces cannot write to them. Any edits must occur through background job queues triggered by system events.

> [!WARNING]
> **Asynchronous Job Latency**
> Because graph calculations are deferred to background queue execution (`frappe.enqueue`), updates to the profile snapshot may have a sub-second delay post-invoice event.

---

## 3. DocType Schema Definitions

We will register five new DocTypes under the `clienteling` module:

### A. `SMRITI Customer Graph` (System Layer)
*Materialized, derived database record representing the customer graph.*

| Fieldname | Label | Type | Options / Length | Mandatory | Properties / Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `customer` | Customer | Link | Customer | Yes | Primary Key / Index. |
| `purchases_count` | Total Purchases | Int | | No | Count of non-return invoices. |
| `returns_count` | Total Returns | Int | | No | Count of return invoices. |
| `net_revenue` | Net Revenue | Currency | | No | Sales grand totals minus returns. |
| `wallet_balance` | Wallet Balance | Currency | | No | Loyalty Ledger point balance. |
| `campaign_responses_count` | Campaign Responses | Int | | No | Active coupon responses. |
| `attributed_revenue` | Attributed Revenue | Currency | | No | Sum of sales from Attribution Ledger. |
| `owned_customer_revenue`| Owned Revenue | Currency | | No | Revenue matching `SMRITI Customer Ownership`.|
| `preferred_brand` | Preferred Brand | Link | Brand | No | Derived brand mode from line items. |
| `preferred_category` | Preferred Category | Link | Item Group | No | Derived category mode from line items. |
| `preferred_size` | Preferred Size | Data | 50 | No | Size mode. |
| `preferred_color` | Preferred Color | Data | 50 | No | Color mode. |
| `last_visit_date` | Last Visit Date | Date | | No | Posting date of last invoice. |
| `visit_frequency_days` | Visit Frequency (Days) | Float | | No | Average days between visits. |
| `favorite_executive` | Favorite Executive | Link | Employee | No | Mode executive from Attribution Ledger. |
| `is_dirty` | Is Dirty | Check | | Yes | Default: 0. Set to 1 on event hooks. |
| `dirty_source` | Dirty Source | Data | 255 | No | Audit: Source DocType of changes. |
| `dirty_document` | Dirty Document | Data | 255 | No | Audit: Doc ID triggering changes. |
| `graph_version` | Graph Version | Data | 50 | Yes | Default: "v1". |
| `calculation_status` | Calc Status | Select | Pending<br>Processing<br>Completed<br>Failed | Yes | Default: Pending. |
| `last_calculated_on` | Last Calculated On | Datetime | | No | Calculation timestamp. |

---

### B. `SMRITI Customer Profile` (Presentation Layer)
*Materialized presentation snapshot for POS lookups.*

| Fieldname | Label | Type | Options / Length | Mandatory | Properties / Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `customer` | Customer | Link | Customer | Yes | Primary Key / Index. |
| `preferred_brand` | Preferred Brand | Link | Brand | No | Read from Graph. |
| `preferred_category` | Preferred Category | Link | Item Group | No | Read from Graph. |
| `preferred_size` | Preferred Size | Data | 50 | No | Read from Graph. |
| `preferred_color` | Preferred Color | Data | 50 | No | Read from Graph. |
| `last_visit_date` | Last Visit Date | Date | | No | Read from Graph. |
| `visit_frequency_days` | Visit Frequency (Days) | Float | | No | Read from Graph. |
| `favorite_executive` | Favorite Executive | Link | Employee | No | Read from Graph. |
| `average_basket_value` | Avg Basket Value (ABV) | Currency | | No | Calculated: Net Revenue / Purchases. |
| `lifetime_value` | Lifetime Value (LTV) | Currency | | No | Equals Net Revenue from Graph. |
| `likely_purchase_prediction` | Predicted SKU | Link | Item | No | Pulled from PDT. |
| `prediction_confidence` | Prediction Confidence | Percent | | No | Pulled from PDT. |
| `next_visit_prediction` | Predicted Next Visit | Date | | No | Pulled from PDT. |
| `engagement_score` | Engagement Score | Percent | | No | Activity score algorithm. |
| `is_dirty` | Is Dirty | Check | | Yes | Default: 0. |
| `dirty_source` | Dirty Source | Data | 255 | No | Audit: Source of change. |
| `dirty_document` | Dirty Document | Data | 255 | No | Audit: Doc ID of change. |
| `graph_version` | Graph Version | Data | 50 | Yes | Default: "v1". |
| `calculation_status` | Calc Status | Select | Pending<br>Processing<br>Completed<br>Failed | Yes | Default: Pending. |
| `last_calculated_on` | Last Calculated On | Datetime | | No | Calculation timestamp. |

---

### C. `SMRITI Customer Interaction` (Interaction Ledger)
*Tracks customer touchpoints and relationship logs.*

| Fieldname | Label | Type | Options / Length | Mandatory | Properties / Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `customer` | Customer | Link | Customer | Yes | Indexed. |
| `interaction_date` | Date | Date | | Yes | Default: Today. |
| `interaction_time` | Time | Time | | Yes | Default: Now. |
| `interaction_type` | Interaction Type | Select | Phone Call<br>WhatsApp Follow-Up<br>Birthday Greeting<br>Store Visit<br>Personal Shopping Session<br>Other | Yes | |
| `employee` | Employee | Link | Employee | Yes | Handled by executive. |
| `interaction_outcome` | Outcome | Select | Interested<br>Not Interested<br>Follow-Up Required<br>Converted | Yes | Default: Interested. |
| `store` | Store | Link | Warehouse | Yes | Limit to active retail warehouses. |
| `channel` | Channel | Select | In-Person<br>WhatsApp<br>Phone<br>SMS<br>Email | Yes | |
| `details` | Details | Small Text | | No | Notes on interaction. |
| `ref_doc_type` | Ref DocType | Data | 255 | No | Associated document schema. |
| `ref_doc_name` | Ref Name | Data | 255 | No | Associated record ID. |

---

### D. `SMRITI Walk In Visit` (State Machine Tracker)
*Logs store walk-in funnel steps.*

| Fieldname | Label | Type | Options / Length | Mandatory | Properties / Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `visit_date` | Visit Date | Date | | Yes | Default: Today. |
| `visit_time` | Visit Time | Time | | Yes | Default: Now. |
| `store` | Store | Link | Warehouse | Yes | Limit to active retail warehouses. |
| `executive` | Sales Executive | Link | Employee | No | Assigned representative (if Assisted). |
| `customer` | Customer | Link | Customer | No | Linked customer (if identified). |
| `customer_phone` | Customer Phone | Data | 50 | No | Captured for contact tracing. |
| `status` | Funnel Status | Select | Registered<br>Browsing<br>Assisted<br>Converted<br>Exited | Yes | Default: Registered. |
| `reason_for_no_purchase` | Exit Reason | Select | Pricing<br>Stock Out<br>Size Issue<br>Design Mismatch<br>Just Browsing<br>Other | No | Mandatory if status = "Exited". |
| `sales_invoice` | Attributed Invoice | Link | Sales Invoice | No | Linked invoice (if Converted). |
| `pos_invoice` | Attributed POS Invoice | Link | POS Invoice | No | Linked POS invoice. |
| `engagement_duration` | Engagement (Minutes) | Int | | No | Duration in minutes. |
| `remarks` | Remarks | Small Text | | No | Notes. |

---

### E. `SMRITI Walk In Analytics` (Conversion Analytics)
*Materialized daily performance snapshots per store. Never manually edited.*

| Fieldname | Label | Type | Options / Length | Mandatory | Properties / Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `date` | Date | Date | | Yes | |
| `store` | Store | Link | Warehouse | Yes | |
| `total_walk_ins` | Total Walk-Ins | Int | | Yes | Sum of all visits. |
| `total_conversions` | Conversions | Int | | Yes | Converted count. |
| `conversion_rate` | Conversion Rate | Percent | | Yes | (Conversions / Walk-Ins) * 100. |
| `total_revenue` | Revenue | Currency | | Yes | Sum of Converted transaction grand totals. |
| `avg_engagement_minutes` | Avg Engagement | Float | | Yes | |

---

## 4. Services Layer Design

### `clienteling_service.py`
Path: `smriti_retail_os/clienteling/service/clienteling_service.py`

Handles asynchronous Customer Graph updates and Profile regenerations.

```python
# -*- coding: utf-8 -*-
import frappe
from frappe.utils import flt, getdate, today, now_datetime

def mark_dirty(customer, source=None, source_document=None):
    """
    Sets dirty status on both Graph and Profile and queues background update.
    Called directly by event hooks to ensure checkout isn't blocked.
    """
    if not customer:
        return
        
    for doctype in ["SMRITI Customer Graph", "SMRITI Customer Profile"]:
        if frappe.db.exists(doctype, customer):
            frappe.db.set_value(doctype, customer, {
                "is_dirty": 1,
                "calculation_status": "Pending",
                "dirty_source": source,
                "dirty_document": source_document
            })
            
    # Queue asynchronous job
    frappe.enqueue(
        "smriti_retail_os.clienteling.service.clienteling_service.regenerate_customer_data",
        queue="default",
        timeout=300,
        customer=customer,
        source=source,
        source_document=source_document
    )

def regenerate_customer_data(customer, source=None, source_document=None):
    """
    Executes background calculation of SMRITI Customer Graph and SMRITI Customer Profile.
    """
    # Mark as processing
    for doctype in ["SMRITI Customer Graph", "SMRITI Customer Profile"]:
        if frappe.db.exists(doctype, customer):
            frappe.db.set_value(doctype, customer, "calculation_status", "Processing")
            
    try:
        # 1. Update Customer Graph
        graph_doc = update_customer_graph(customer, source, source_document)
        
        # 2. Update Customer Profile
        update_customer_profile(customer, graph_doc, source, source_document)
    except Exception as e:
        for doctype in ["SMRITI Customer Graph", "SMRITI Customer Profile"]:
            if frappe.db.exists(doctype, customer):
                frappe.db.set_value(doctype, customer, "calculation_status", "Failed")
        raise e

def update_customer_graph(customer, source=None, source_document=None):
    if not frappe.db.exists("SMRITI Customer Graph", customer):
        doc = frappe.new_doc("SMRITI Customer Graph")
        doc.customer = customer
    else:
        doc = frappe.get_doc("SMRITI Customer Graph", customer)
        
    # Transaction Aggregates
    invoices = frappe.db.get_all(
        "Sales Invoice",
        filters={"customer": customer, "docstatus": 1},
        fields=["name", "posting_date", "grand_total", "is_return"]
    )
    pos_invoices = frappe.db.get_all(
        "POS Invoice",
        filters={"customer": customer, "docstatus": 1},
        fields=["name", "posting_date", "grand_total", "is_return"]
    )
    all_sales = invoices + pos_invoices
    
    purchases = [s for s in all_sales if not s.is_return]
    returns = [s for s in all_sales if s.is_return]
    
    purchases_count = len(purchases)
    returns_count = len(returns)
    
    net_revenue = sum(flt(s.grand_total) for s in purchases) - sum(flt(s.grand_total) for s in returns)
    
    # Visit frequency calculation
    dates = sorted(list(set([getdate(s.posting_date) for s in purchases])))
    visit_frequency = 0.0
    last_visit = None
    if dates:
        last_visit = dates[-1]
        if len(dates) > 1:
            intervals = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
            visit_frequency = flt(sum(intervals) / len(intervals))
            
    # Preferred item attributes mode
    items = get_purchased_item_details(customer)
    preferred_brand = get_mode(items, "brand")
    preferred_category = get_mode(items, "item_group")
    preferred_size = get_mode(items, "size")
    preferred_color = get_mode(items, "color")
    
    # Favorite Executive from Attribution Ledger
    favorite_executive = frappe.db.get_value(
        "SMRITI Attribution Ledger",
        filters={"customer": customer, "docstatus": 1},
        fieldname="employee",
        order_by="creation desc"
    )
    
    # Revenue splits from customer ownership mapping
    attributed_revenue = frappe.db.get_value(
        "SMRITI Attribution Ledger",
        filters={"customer": customer, "docstatus": 1},
        fieldname="sum(allocated_amount)"
    ) or 0.0
    
    owned_customer_revenue = 0.0
    # Lookup customer ownership relationship
    owner = frappe.db.get_value("SMRITI Customer Ownership", {"customer": customer}, "employee")
    if owner:
        owned_customer_revenue = frappe.db.get_value(
            "SMRITI Attribution Ledger",
            filters={"customer": customer, "employee": owner, "docstatus": 1},
            fieldname="sum(allocated_amount)"
        ) or 0.0
        
    # Loyalty points balance
    wallet_balance = flt(frappe.db.get_value(
        "SMRITI Loyalty Ledger",
        filters={"customer": customer},
        fieldname="sum(loyalty_points_delta)"
    ))
    
    # Save Graph Data
    doc.purchases_count = purchases_count
    doc.returns_count = returns_count
    doc.net_revenue = net_revenue
    doc.wallet_balance = wallet_balance
    doc.attributed_revenue = attributed_revenue
    doc.owned_customer_revenue = owned_customer_revenue
    doc.preferred_brand = preferred_brand
    doc.preferred_category = preferred_category
    doc.preferred_size = preferred_size
    doc.preferred_color = preferred_color
    doc.last_visit_date = last_visit
    doc.visit_frequency_days = visit_frequency
    doc.favorite_executive = favorite_executive
    doc.is_dirty = 0
    doc.dirty_source = source
    doc.dirty_document = source_document
    doc.graph_version = "v1"
    doc.calculation_status = "Completed"
    doc.last_calculated_on = now_datetime()
    doc.save(ignore_permissions=True)
    return doc

def update_customer_profile(customer, graph_doc, source=None, source_document=None):
    if not frappe.db.exists("SMRITI Customer Profile", customer):
        doc = frappe.new_doc("SMRITI Customer Profile")
        doc.customer = customer
    else:
        doc = frappe.get_doc("SMRITI Customer Profile", customer)
        
    # Read derived variables from Customer Graph
    doc.preferred_brand = graph_doc.preferred_brand
    doc.preferred_category = graph_doc.preferred_category
    doc.preferred_size = graph_doc.preferred_size
    doc.preferred_color = graph_doc.preferred_color
    doc.last_visit_date = graph_doc.last_visit_date
    doc.visit_frequency_days = graph_doc.visit_frequency_days
    doc.favorite_executive = graph_doc.favorite_executive
    
    # Retrieve Formula Expressions from Registry (Strictly pull without hardcoding)
    abv_expr = frappe.db.get_value("SMRITI Formula Registry", "ABV", "formula_expression")
    ltv_expr = frappe.db.get_value("SMRITI Formula Registry", "LTV", "formula_expression")
    
    # Evaluate formulas safely with fallbacks if missing
    context = {"net_revenue": graph_doc.net_revenue, "purchases_count": graph_doc.purchases_count}
    
    if ltv_expr:
        try:
            doc.lifetime_value = eval(ltv_expr, {}, context)
        except Exception:
            doc.lifetime_value = graph_doc.net_revenue
    else:
        doc.lifetime_value = graph_doc.net_revenue
        
    if abv_expr:
        try:
            doc.average_basket_value = eval(abv_expr, {}, context) if graph_doc.purchases_count > 0 else 0.0
        except Exception:
            doc.average_basket_value = graph_doc.net_revenue / graph_doc.purchases_count if graph_doc.purchases_count > 0 else 0.0
    else:
        doc.average_basket_value = graph_doc.net_revenue / graph_doc.purchases_count if graph_doc.purchases_count > 0 else 0.0
        
    # Pull PDT Predictions
    pdt_pred = get_pdt_predictions(customer)
    doc.likely_purchase_prediction = pdt_pred.get("likely_purchase")
    doc.prediction_confidence = pdt_pred.get("confidence", 0.0)
    doc.next_visit_prediction = pdt_pred.get("predicted_next_visit")
    
    # Engagement Score Calculation
    doc.engagement_score = calculate_engagement_score(graph_doc.purchases_count, graph_doc.net_revenue, graph_doc.returns_count)
    doc.is_dirty = 0
    doc.dirty_source = source
    doc.dirty_document = source_document
    doc.graph_version = "v1"
    doc.calculation_status = "Completed"
    doc.last_calculated_on = now_datetime()
    doc.save(ignore_permissions=True)

def get_purchased_item_details(customer):
    return frappe.db.sql("""
        SELECT i.brand, i.item_group, i.custom_size as size, i.custom_color as color
        FROM `tabSales Invoice Item` sii
        JOIN `tabSales Invoice` si ON sii.parent = si.name
        JOIN `tabItem` i ON sii.item_code = i.name
        WHERE si.customer = %s AND si.docstatus = 1 AND si.is_return = 0
        UNION ALL
        SELECT i.brand, i.item_group, i.custom_size as size, i.custom_color as color
        FROM `tabPOS Invoice Item` pii
        JOIN `tabPOS Invoice` pi ON pii.parent = pi.name
        JOIN `tabItem` i ON pii.item_code = i.name
        WHERE pi.customer = %s AND pi.docstatus = 1 AND pi.is_return = 0
    """, (customer, customer), as_dict=True)

def get_mode(items, field):
    values = [i.get(field) for i in items if i.get(field)]
    if not values:
        return None
    return max(set(values), key=values.count)

def get_pdt_predictions(customer):
    try:
        from smriti_retail_os.pdt.service import prediction_service
        return prediction_service.get_customer_prediction(customer)
    except ImportError:
        return {"likely_purchase": None, "confidence": 0.0, "predicted_next_visit": None}

def calculate_engagement_score(purchases, net_revenue, returns):
    score = 0.0
    if purchases > 0:
        score += min(purchases * 10, 50)
    if net_revenue > 0:
        score += min((net_revenue / 5000) * 10, 40)
    return_ratio = returns / purchases if purchases > 0 else 0
    score -= min(return_ratio * 30, 20)
    return max(0.0, min(100.0, score))
```

---

### `walk_in_service.py`
Path: `smriti_retail_os/clienteling/service/walk_in_service.py`

Manages walk-in visits state and aggregates analytics.

```python
# -*- coding: utf-8 -*-
import frappe
from frappe.utils import flt, today

def update_walk_in_status(visit_id, status, reason=None, invoice_type=None, invoice_id=None, duration=None):
    """
    Executes valid state transitions inside the walk-in state machine.
    """
    doc = frappe.get_doc("SMRITI Walk In Visit", visit_id)
    valid_states = ["Registered", "Browsing", "Assisted", "Converted", "Exited"]
    
    if status not in valid_states:
        frappe.throw(f"Invalid state: {status}")
        
    doc.status = status
    if status == "Exited":
        doc.reason_for_no_purchase = reason
    elif status == "Converted":
        if invoice_type == "Sales Invoice":
            doc.sales_invoice = invoice_id
        elif invoice_type == "POS Invoice":
            doc.pos_invoice = invoice_id
            
    if duration is not None:
        doc.engagement_duration = duration
        
    doc.save(ignore_permissions=True)
    return doc
```

---

## 5. Event Hook Integration

Add hooks to automatically mark profiles dirty on transaction events:

```python
# smriti_retail_os/hooks.py
doc_events = {
    "Sales Invoice": {
        "on_submit": "smriti_retail_os.clienteling.service.clienteling_service.on_invoice_submit",
        "on_cancel": "smriti_retail_os.clienteling.service.clienteling_service.on_invoice_cancel"
    },
    "POS Invoice": {
        "on_submit": "smriti_retail_os.clienteling.service.clienteling_service.on_pos_invoice_submit",
        "on_cancel": "smriti_retail_os.clienteling.service.clienteling_service.on_pos_invoice_cancel"
    }
}
```

```python
# inside clienteling_service.py
def on_invoice_submit(doc, method):
    mark_dirty(doc.customer, source="Sales Invoice", source_document=doc.name)

def on_invoice_cancel(doc, method):
    mark_dirty(doc.customer, source="Sales Invoice", source_document=doc.name)

def on_pos_invoice_submit(doc, method):
    mark_dirty(doc.customer, source="POS Invoice", source_document=doc.name)

def on_pos_invoice_cancel(doc, method):
    mark_dirty(doc.customer, source="POS Invoice", source_document=doc.name)
```

---

## 6. Verification Plan & Tests

### Automated Unit Tests
We will add a test suite at `apps/smriti_retail_os/smriti_retail_os/tests/test_clienteling.py` covering:

1. **Materialization Invariant**: Test that direct database writes to `SMRITI Customer Profile` are blocked, and updates only succeed when queued asynchronously.
2. **State Machine Transitions**: Validate that `SMRITI Walk In Visit` updates progress exactly from `Registered` -> `Browsing` -> `Assisted` -> `Converted` / `Exited`.
3. **Formula Registry Compliance**: Assert that LTV, ABV, RRI, and WCR calculations match Formula Registry expressions.
4. **test_profile_regeneration_queue**: Confirm that submitting an invoice sets `is_dirty = 1` and enqueues background worker job executing successfully.
5. **test_formula_registry_fallback**: If formulas are missing from `SMRITI Formula Registry`, calculations fallback gracefully to standard divisions without crash.
6. **test_graph_profile_consistency**: Validate that all shared field values in `SMRITI Customer Graph` and `SMRITI Customer Profile` match exactly after execution.

#### Test Execution Command
```bash
docker exec smriti_retail-backend-1 bench --site smriti_retail test smriti_retail_os.tests.test_clienteling
```

---

## 7. Freeze Approval

By signing off on this document, the customer and development team freeze the architecture scope and approve the implementation phase.

- **Client Project Sponsor**: ARCHITECTURE FREEZE APPROVED
- **AITDL Chief Architect**: Jawahar R. Mallah

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
