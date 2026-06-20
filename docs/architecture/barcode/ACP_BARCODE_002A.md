# ACP-BARCODE-002A — BARCODE SCAN TELEMETRY COLLECTION FRAMEWORK

## Document Classification
* **Document ID:** ACP-BARCODE-002A
* **Version:** 1.1
* **Status:** APPROVED (Chief Architect Governance Review with 5 Amendments)
* **Authority:** SMRITI Governance Framework
* **Owner:** Jawahar R. Mallah, Founder & Chief Architect
* **Organization:** AITDL
* **Effective Date:** 2026-06-20

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

During Phase 3A, SMRITI Barcode Studio implemented design-time validations (Quiet Zones, Virtual HRT, and Printability Scoring) to ensure high-quality physical barcode layouts. However, physical scan reliability in retail stores is subject to environmental and operational factors (e.g., printer printhead degradation, low ink, dirty scanner lenses, operator scanning angles, or low-contrast paper).

To enable future Predictive Barcode Twin capabilities (Phase 5) and machine learning optimizations (PDT), we must establish a clean, explainable, and audit-friendly telemetry pipeline. 

`ACP-BARCODE-002A` defines the **SMRITI Scan Telemetry Collection Framework**. It focuses strictly on data collection, validation, aggregation, and metrics governance, separating telemetry acquisition from the downstream learning/prediction engines.

---

## 3. Prerequisite Gate (PREREQUISITE-002A)

Before the development of Phase 4/5 features is allowed to start, the following prerequisites must be approved:
1. **Telemetry Dictionary Approved:** Complete semantic definitions of all tracked scan metrics.
2. **Telemetry Retention Policy Approved:** Explicit retention policies for high-frequency raw tables vs. low-frequency aggregated tables.
3. **Scan Event Definitions Approved:** Formalization of scan failure, retry, and success events using Governance IDs.

---

## 4. Telemetry Dictionary

This dictionary defines the exact business meanings of the telemetry metrics collected by the SMRITI Barcode scanner interface.

| Metric | Business Definition | Telemetry Trigger |
| :--- | :--- | :--- |
| **scan_success** | The barcode symbol was successfully decoded into an alphanumeric string matching a valid item or identifier. | Final scan status is successful. |
| **first_pass_success** | The barcode was successfully decoded on the very first attempt (scan attempts = 1). | Scanned successfully with exactly 1 beam/camera capture attempt. |
| **retry_scan** | The barcode required multiple scanner trigger pulls or camera frames to successfully decode (scan attempts > 1). | Scanned successfully but only after multiple attempts. |
| **scan_failure** | The barcode could not be decoded after maximum attempts or was bypassed by manual typing of the barcode digits. | Operator gave up scanning and manually entered the code or aborted the item scan. |

---

## 5. Telemetry Retention & Backup Policy

* **Live Data Retention:**
  - **Raw Telemetry Events (`SMRITI Barcode Scan Event`):** Retention period is **90 Days** in the active transactional database. An automatic daily system job (`delete_expired_scan_events`) will delete records older than 90 days.
  - **Aggregated Telemetry Snapshots (`SMRITI Barcode Telemetry Snapshot`):** Retained **permanently** for reporting, trend analysis, and prediction model training.
* **Backup Policy:**
  - Raw telemetry events are **not** excluded from database backups. Raw telemetry is extremely valuable for root-cause and historical forensics (e.g., investigating a hardware issue reported from a prior month).
  - Raw events are subject to the standard database backup retention policy, ensuring historical events exist in backups long after they have been pruned from the active live database.

---

## 6. Aggregation Scheduler

Aggregation snapshots must not run during active store operational hours to avoid locking tables or processing incomplete days.
* **Scheduled Time:** **03:00 AM daily** (store local time).
* **Reason:** Allows sufficient buffer for delayed bill uploads, offline terminal syncs, nightly stock postings, and imports to settle, ensuring absolute aggregate accuracy.

---

## 7. Scan Event Definitions & Governance ID Registry

To prevent governance codes from becoming magic numbers or undocumented constants, all telemetry event codes are registered formally under a new DocType.

### 7.1. SMRITI Telemetry Event Definition (Registry DocType)
* **DocType Name:** `SMRITI Telemetry Event Definition`
* **Naming:** Exact event ID (e.g., `SCAN-EVT-001`)
* **Fields:**
  - `name` (Data, Primary Key, e.g., `SCAN-EVT-001`)
  - `event_name` (Data, e.g., `Barcode Scan Success`)
  - `description` (Small Text)

### 7.2. Seeded Governance IDs
* **`SCAN-EVT-001` (Barcode Scan Success):** Applied when `scan_success` is true and `first_pass_success` is true. Represents optimal print and scanning conditions.
* **`SCAN-EVT-002` (Barcode Scan Retry):** Applied when `scan_success` is true but `first_pass_success` is false (`attempts > 1`). Signifies potential design, print quality, or hardware degradation that requires monitoring.
* **`SCAN-EVT-003` (Barcode Scan Failure):** Applied when `scan_success` is false and either manual override is triggered or the item scan is aborted. Signifies critical print/media issues or hardware failure.

---

## 8. Data Models

We propose three custom DocTypes in SMRITI:

### 8.1. SMRITI Barcode Scan Event (Raw Event Table — IMMUTABLE)
* **DocType Name:** `SMRITI Barcode Scan Event`
* **Naming:** `SCN-EVT-.YYYY.-.MM.-.#####` (Series)
* **Immutability Enforcement:** Any update/edit operations are strictly blocked by the controller (`before_save`). Only inserts and scheduler deletions are allowed.
* **Idempotency Protection:** Enforced by unique field `event_uuid` to filter out network retries from POS terminals.
* **Fields:**
  - `event_id` (Data, read-only)
  - `event_uuid` (Data, unique, read-only, indexable)
  - `timestamp` (Datetime, read-only)
  - `store_id` (Link to `Warehouse`, indexable, read-only)
  - `template_id` (Link to `SMRITI Print Template`, indexable, read-only)
  - `barcode_family` (Select: EAN-13, EAN-8, UPC-A, UPC-E, Code128, Code39, QR Code, read-only)
  - `printer_profile` (Link to `SMRITI Printer Profile` or Data, read-only)
  - `scan_method` (Select: Handheld Laser, Fixed Omnidirectional, Mobile Camera, Manual Input, read-only)
  - `scan_attempts` (Int, default: 1, read-only)
  - `scan_success` (Check, default: 0, read-only)
  - `first_pass_success` (Check, default: 0, read-only)
  - `governance_event_id` (Link to `SMRITI Telemetry Event Definition`, read-only)
  - `pos_invoice` (Link to `Sales Invoice`, nullable, read-only)
  - `pos_invoice_item` (Data, nullable, read-only)

### 8.2. SMRITI Barcode Telemetry Snapshot (Aggregated Table)
* **DocType Name:** `SMRITI Barcode Telemetry Snapshot`
* **Naming:** `SCN-SNAP-.YYYY.-.MM.-.#####` (Series)
* **Fields:**
  - `snapshot_date` (Date)
  - `period` (Select: Daily, Weekly, Monthly)
  - `store_id` (Link to `Warehouse`, indexable)
  - `template_id` (Link to `SMRITI Print Template`, indexable)
  - `barcode_family` (Select: EAN-13, EAN-8, UPC-A, UPC-E, Code128, Code39, QR Code)
  - `printer_profile` (Link to `SMRITI Printer Profile` or Data)
  - `total_scans` (Int, default: 0)
  - `total_successes` (Int, default: 0)
  - `first_pass_successes` (Int, default: 0)
  - `retry_successes` (Int, default: 0)
  - `failures` (Int, default: 0)
  - `scan_reliability_score` (Float, default: 0.0)
  - `first_pass_success_rate` (Float, default: 0.0)

---

## 9. Formula Registry: Scan Reliability Score (`SMRITI-SCAN-REL-01`)

To satisfy **Rule 10 (Explainable Metrics)**, **Rule 11 (Formula Registry Policy)**, and **Rule 13 (Explainability-First)**, we register the `Scan Reliability Score` in the SMRITI Formula Registry.

### A. Business Meaning
The Scan Reliability Score evaluates the real-world scan usability of printed barcode templates. It translates raw operational telemetry into a clear percentage index representing scanning efficiency at checkout lanes. A high score means scanning is seamless, while a low score indicates slow checkouts due to scan retries or manual typing overrides.

### B. Formula Definition
$$Scan\ Reliability\ Score\ (SRS) = \left( \frac{FirstPassSuccesses + 0.5 \times RetrySuccesses}{TotalScans} \right) \times 100$$

*Where:*
* $TotalScans = FirstPassSuccesses + RetrySuccesses + Failures$.
* $FirstPassSuccesses$ = Count of events matching `SCAN-EVT-001` (successful on 1st attempt).
* $RetrySuccesses$ = Count of events matching `SCAN-EVT-002` (successful but required $>1$ attempt).
* $Failures$ = Count of events matching `SCAN-EVT-003` (failed completely or overridden by keyboard input).
* If $TotalScans = 0$, $SRS = 0.0$ (No scans recorded).

### C. Worked Example
A store logs checkout telemetry for a print template over 24 hours:
- $FirstPassSuccesses = 80$
- $RetrySuccesses = 15$
- $Failures = 5$
- $TotalScans = 80 + 15 + 5 = 100$

$$SRS = \left( \frac{80 + 0.5 \times 15}{100} \right) \times 100 = \left( \frac{80 + 7.5}{100} \right) \times 100 = 87.5\%$$
*The template receives a Scan Reliability Score of **87.5%**.*

### D. Data Source Mapping
- **Numerator Inputs:** Count of `SMRITI Barcode Scan Event` filtered by `template_id` where `governance_event_id` is `SCAN-EVT-001` ($FirstPassSuccesses$) or `SCAN-EVT-002` ($RetrySuccesses$).
- **Denominator Inputs:** Count of all `SMRITI Barcode Scan Event` records filtered by `template_id` within the snapshot timeframe.

### E. Interpretation Guide
* **95.0% – 100.0%:** **Excellent (Green)**. Optimal physical scanning. No actions needed.
* **85.0% – 94.9%:** **Monitor (Yellow)**. Elevated retries. Check for printer ink degradation or slight barcode smudging.
* **Below 85.0%:** **Critical (Red)**. Severe checkout friction. Triggers a SMRITI notification recommending template layout revision or printer head cleaning.

### F. Recommended Actions
1. **If Yellow:** Verify print quality using a manual test print. Ensure thermal printhead is free of dust.
2. **If Red:** Prompt SMRITI administrator to run layout diagnostics via the Barcode Studio. Check if quiet zones are too narrow or barcode density is too high for the printer's active DPI.

### G. Edge Case Handling
- **Division by Zero:** If $TotalScans = 0$, $SRS = 0.0$.
- **Null values:** Count operations default null database records to $0$.

### H. UI Explainability (ⓘ Explain Modal)
When rendering the Scan Reliability Score in the SMRITI Reports/Dashboard, clicking the **ⓘ Explain** icon next to the score will open a modal populated with:
- The active formula expression.
- Live inputs ($TotalScans$, $FirstPassSuccesses$, $RetrySuccesses$, $Failures$).
- The step-by-step arithmetic evaluation matching the Worked Example format.
- The interpretation category (Excellent, Monitor, Critical) and the corresponding recommended action.

---

## 10. Security Review & Role Verification

The telemetry event logging endpoint `log_barcode_scan_event` is whitelisted but restricted to protect system integrity:
1. **Authenticated Sessions Only:** Anonymous/guest submissions are rejected.
2. **Role Enforcement:** The requesting user must possess either the `SMRITI POS User` (or standard `POS User` roles as configured in SMRITI) or `System Manager` roles. Employees without POS or manager roles are blocked from submitting telemetry.

---

## 11. Document Revision History

| Date | Version | Description | Author |
| :--- | :--- | :--- | :--- |
| 2026-06-20 | 1.0 | Initial draft proposal for telemetry collection governance. | Jawahar R. Mallah |
| 2026-06-20 | 1.1 | Integrated 5 mandatory amendments: store dimension, UUID idempotency, read-only event immutability, formula clarification, and governance event definition DocType. | Jawahar R. Mallah |
