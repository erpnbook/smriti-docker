# SMRITI Retail OS — PSV Phase 1.3 Candidate Roadmap

Following UAT verification and pilot feedback, the PSV roadmap has been refined to enforce a strict boundary between the **Intelligence Layer** (Wave 1/2) and the **Automation Layer** (Wave 3). This prevents operational disruption and cash flow risks before the analytical models are fully trusted.

---

## 🗺️ Governance & Decision Gates
* **Pilot Loop Requirement**: No candidate feature in Phase 1.3 or 1.4 shall be promoted to active development without at least one completed Pilot Distributor review cycle.
* **Vertical Isolation Principle**: Vertical-specific features (e.g. Footwear Vertical Module) must remain decoupled as optional modules.
  * **PSV Phase 1.3A-P1A Conditional Feature**: Activates only if `Footwear Vertical Mode` is explicitly enabled in SMRITI Company Settings or PSV System Settings. No-op on other configurations.

---

## 📈 Phase 1.3A — Intelligence Layer (Wave 1)
These extend existing PSV analytics without changing operational workflows or automating transactions.

### 1. Capital Locked Analysis
* **Goal**: Enable distributors to see where working capital is stagnating.
* **Deliverables**:
  * Locked Capital Dashboard Widget
  * Dead Stock Capital valuation
  * Slow Mover Capital valuation
  * Excess Inventory Capital valuation
  * Channel-wise capital allocation summary
  * Working capital impact analysis
* **Priority**: Critical

### 2. Coverage Days Intelligence
* **Goal**: Upgrade stock cover model from weekly velocity bins to high-precision daily coverage.
* **Deliverables**:
  * Daily velocity calculation
  * Coverage-day forecasting
  * Stockout warning alerts
  * Overstock warning alerts
* **Priority**: Critical

### 3. Inventory Aging Intelligence
* **Goal**: Complete the inventory health picture.
* **Deliverables**:
  * FIFO age buckets (30 / 60 / 90 / 180 days)
  * Age vs. Sell-Through ratio analysis
  * Age vs. GMROI mapping (e.g., Old+Profitable, Old+Unprofitable)
* **Priority**: Critical

---

## 🔍 Phase 1.3B — Recovery Intelligence (Wave 2)
Generates non-automated recommendations to help users resolve inventory bottlenecks.

### Dead Stock Recovery Intelligence
* **Rule**: Recommendation Only. SMRITI will not perform auto-transfers or auto-discounts. Keep humans in control.
* **Deliverables**:
  * Redistribution suggestions (e.g., Transfer to Branch B)
  * Bundling recommendations (e.g., Bundle slow item with fast item)
  * Promotion suggestions (e.g., Run clearance offer)
  * Order reduction recommendations
* **Priority**: High

---

## 📊 Phase 1.3C — Pilot Intelligence (Wave 2)
Focuses on telemetry and feedback ingestion during the pilot phase to guide design choices.

### 1. Usage Analytics
* **Goal**: Track user interactions to identify dashboard utility.
* **Deliverables**:
  * Widget interaction tracking (opens/collapses)
  * Modal view counts
  * Excel/CSV export usage metrics
  * Most active PSV dashboard sections
* **Priority**: Medium

### 2. Pilot Feedback Tracking
* **Goal**: Centralize feedback to serve as the gateway for Phase 1.4.
* **Deliverables**:
  * Distributor feedback registry
  * Feature request logging
  * Adoption & satisfaction score tracking
* **Priority**: Medium

---

## ⚙️ Phase 1.4 — Automation Layer (Wave 3)
Operational automation features. Scheduled only after successful validation of Phase 1.3 pilots.

### 1. Reorder Engine
* **Rule**: Requires validated pilot data to avoid dangerous over-ordering.
* **Requirements**: Lead time, MOQ, supplier behavior, seasonality, safety stock.
* **Priority**: Later (Deferred)

### 2. Purchase Suggestions
* **Rule**: Requires approval workflows and audit trails due to direct cash flow impact.
* **Requirements**: Automated Purchase Order creation in ERPNext, approval layers, exception handling.
* **Priority**: Later (Deferred)

---

## 🏷️ Final Priority Wave Order

| Wave | Phase | Feature / Deliverable | Priority |
|---|---|---|---|
| **Wave 1** | Phase 1.3A | Capital Locked Analysis | Critical |
| **Wave 1** | Phase 1.3A | Coverage Days Intelligence | Critical |
| **Wave 1** | Phase 1.3A | Inventory Aging Intelligence | Critical |
| **Wave 2** | Phase 1.3B | Dead Stock Recovery (Recommendations) | High |
| **Wave 2** | Phase 1.3C | Usage Analytics (Telemetry) | Medium |
| **Wave 2** | Phase 1.3C | Pilot Feedback Tracking (Gate to 1.4) | Medium |
| **Wave 3** | Phase 1.4 | Reorder Engine (MOQ, Safety Stock) | Later |
| **Wave 3** | Phase 1.4 | Purchase Suggestions (Auto-PO in ERPNext) | Later |
