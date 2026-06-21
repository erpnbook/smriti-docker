---
title: Formula Registry
version: 1.0
last_updated: 2026-06-19
applies_to: SMRITI Retail OS v2.2.0
---

# SMRITI Formula Registry (DOC-02)

The **Formula Registry** is a central governance ledger in SMRITI Retail OS. It registers every mathematical, financial, and forecasting formula used across the platform (such as Weeks of Cover, Sales Velocity, or Transfer Benefit). This prevents "black-box" computations and ensures that formulas are audited, versioned, and documented.

---

## 📋 Schema Definition (`SMRITI Formula Definition`)

The Formula Registry is backed by the `SMRITI Formula Definition` DocType. Each record contains:

*   **Formula ID**: Unique code (e.g. `INV-002`).
*   **Formula Name**: Human-readable name (e.g. "Weeks of Cover").
*   **Formula Category**: Category tag (e.g. `Inventory`, `Forecasting`, `Sales`).
*   **Formula Expression**: String showing the raw mathematical expression (e.g. `current_stock / weekly_velocity`).
*   **Formula Language**: The documentation syntax (e.g., `documentation`).
*   **Business Meaning**: Clear business description for store managers.
*   **Worked Example**: Arithmetic step-by-step walkthrough using real numbers.
*   **Interpretation Guide**: Reference bands (Critical, Monitor, Healthy).
*   **Recommended Action**: Next steps for a store operator when the metric reaches certain bands.
*   **Implementation Reference**: Code file and function where the formula is executed (e.g. `services/forecasting_service.py::calculate_weeks_of_cover`).
*   **Business Owner**: The corporate owner accountable for the formula logic.

---

## ⚡ Caching & Auditing

*   **Redis Caching**: When a formula is loaded by the front-end or service layer, it is cached in Redis at key `smriti:explain:{formula_id}:{version}` with a **TTL of 3600 seconds** (1 hour). Subsequent requests load from cache to ensure sub-second response times.
*   **Access Auditing**: Every fetch of a formula (cache hit or miss) is audited. The system automatically creates a `SMRITI PSV Activity Log` entry with:
    *   `action_type` = `"Formula Explained"`
    *   `event_type` = `"FORMULA_EXPLAINED"`
    *   `reference_name` = `{formula_id}`
    *   `details` = `Version: {version}`

---

## 🧮 Core Registered Formulas

The registry seeds the following 10 core formulas by default:

| Formula ID | Name | Category | Expression | Code Reference |
| :--- | :--- | :--- | :--- | :--- |
| **INV-001** | Sales Velocity | Inventory | `total_sales_qty / lookback_weeks` | `dictionary_service.py` |
| **INV-002** | Weeks of Cover | Inventory | `current_stock / weekly_velocity` | `explain_service.py` |
| **INV-003** | Dead Stock Score | Inventory | `inactive_days * stock_value` | `dictionary_service.py` |
| **INV-004** | Inventory Turnover | Inventory | `cogs / average_inventory_value` | `dictionary_service.py` |
| **FRC-001** | Forecast Confidence | Forecasting | `1.0 - (std_dev / mean)` | `dictionary_service.py` |
| **TRF-001** | Transfer Benefit Score | Distribution | `margin_gain - freight_cost` | `dictionary_service.py` |
| **SAL-001** | Sell Through % | Sales | `sold_qty / opening_stock_qty` | `dictionary_service.py` |
| **AUD-001** | Stock Accuracy % | Audit | `1.0 - (abs_variance / ledger_stock)` | `dictionary_service.py` |
| **OHS-001** | Outlet Health Score | Outlet | `0.6 * sync_score + 0.4 * audit_score` | `dictionary_service.py` |
| **VAR-001** | Size Curve Health | Inventory | `overlap_coefficient(stock, sales)` | `dictionary_service.py` |

---

## Support & Helpdesk
For questions or support, please contact the SMRITI Helpdesk at **support@aitdl.com**.
