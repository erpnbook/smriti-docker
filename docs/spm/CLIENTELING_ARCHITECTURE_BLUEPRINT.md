# SMRITI Clienteling Engine — Architecture Blueprint v1.0

---

### Author Profile (Start)
* **Author**: Jawahar R. Mallah
* **Designation**: Founder & Chief Architect
* **Organization**: AITDL – AI Technology & Development Lab
* **Professional Experience**: 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.

#### Author Note
This architecture blueprint defines the Customer Intelligence Layer of SMRITI Retail OS. By consolidating transactional, loyalty, and predictive data into a unified, read-only Customer Graph, we provide a single source of truth for Clienteling, Product Digital Twin, and AI Copilot engines.

> "Light begins with learning."
> 
> — Jawahar R. Mallah  
> Founder & Chief Architect, AITDL

---

## 1. Domain Scope & Bounded Context

The **Clienteling Engine** sits under the Customer Intelligence Layer of SMRITI Retail OS. It operates on top of the newly introduced **Unified SMRITI Customer Graph** layer.

```
Customer Growth (CGE)  ──┐
Sales Force (SFM/SFC) ──┼─→ SMRITI Customer Graph ──→ Clienteling ──→ POS Overlays
Demand / AI (PDT)     ──┘
```

---

## 2. Unified Customer Graph (Phase 5A)

Before feeding individual customer interfaces or the POS, SMRITI compiles all customer interactions into a single derived layer: **`SMRITI Customer Graph`**. This ensures data consistency across the CGE, PDT, and Clienteling engines.

- **Unified Attributes**:
  - `purchases`: Total count and product details.
  - `returns`: Track return rates to isolate product mismatch.
  - `wallet_activity`: Loyalty balances and transaction history.
  - `campaign_response`: Coupon redemptions and tier transitions.
  - `preferred_brands`: Dynamic ranking of brands purchased.
  - `favorite_executive`: Mapped from transaction attributions.
  - `visit_frequency`: Calculated days between sales invoices.
  - `predicted_next_visit`: Derived via predictive analytics.
  - `lifetime_value`: Net sales value generated.

---

## 3. Governance Rule: Customer Profile Read-Only Invariant

To prevent data drift and preserve the integrity of performance metrics, SMRITI enforces a strict governance invariant:

> [!IMPORTANT]
> **FRZ-CLI-001: Customer Profile Read-Only Invariant**
> - **Derived & Read-Only**: `SMRITI Customer Profile` must be completely derived and read-only. Standard users, cashier terminals, and managers cannot manually edit or overwrite values.
> - **Regeneratable**: The profile must support full regeneration from primary databases (`tabSales Invoice`, `tabSMRITI Loyalty Ledger`, `tabSMRITI Attribution Ledger`, `tabSMRITI Product Digital Twin`) on demand or periodically.
> - **No Direct Database Mutates**: Direct writes to profile records from client interfaces are blocked.

---

## 4. Proposed Data Model

### `SMRITI Customer Profile` DocType
This DocType holds the clienteling parameters compiled from the Unified Customer Graph.

- **Key Fields**:
  - `customer` (Link -> Customer, PK)
  - `preferred_brand` (Link -> Brand)
  - `preferred_category` (Link -> Category)
  - `preferred_size` (Data)
  - `preferred_color` (Data)
  - `last_visit_date` (Date)
  - `visit_frequency_days` (Float)
  - `favorite_executive` (Link -> Employee)
  - `average_basket_value` (Currency)
  - `likely_purchase_prediction` (Data)
  - `prediction_confidence` (Percent)

---

## 5. Executive Relationship Performance KPIs

SMRITI utilizes the Customer Graph to derive relationship-first salesperson performance metrics:

### Relationship Revenue Index (RRI)
Measures the percentage of an executive's sales generated from their assigned customer base:
$$RRI = \left( \frac{\text{Owned Customer Revenue}}{\text{Total Attributed Revenue}} \right) \times 100$$

### Retention Influence Score (RIS)
Counts the unique repeat customers engaged and checked out by the salesperson within a 90-day window:
$$RIS = \text{Count of unique repeat customers checked out by Executive}$$

### Growth Contribution (GC)
Calculates revenue growth generated from the salesperson's assigned customer portfolio:
$$GC = \text{Current Month Assigned Revenue} - \text{Baseline Assigned Revenue}$$

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
