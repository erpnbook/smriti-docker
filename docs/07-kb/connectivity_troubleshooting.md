---
Document ID: "KB-032"
Title: "Connectivity & UIE Troubleshooting Guide"
Owner: "Support Team"
Audience: "Support Engineer"
Module: "Core"
Version: "1.0.0"
Status: "Active"
Primary Document: "Yes"
Depends On: ""
Related Modules: ""
Last Updated: "2026-06-28"
Last Reviewed: "2026-06-28"
AI Generated: "Yes"
Reviewed By: "Jawahar R. Mallah"
---

# Connectivity & UIE Troubleshooting Guide

## Author Profile (Document Start)

- **Author**: Jawahar R. Mallah
- **Designation**: Founder & Chief Architect
- **Organization**: AITDL – AI Technology & Development Lab
- **Professional Experience**: 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.

---

## 1. Troubleshooting Sync Queue Issues

When transactions fail to reach external endpoints (such as TallyPrime or Mall APIs), support engineers should execute the following verification steps:

### 1.1 Checking Sync Logs
Verify transmission failures inside `SMRITI UIE Sync Log`:
1. Search for records matching the Document ID or transaction hash.
2. Inspect the **HTTP Status** and **Response Content** columns.
3. Review the execution duration (`duration_ms`) to identify potential endpoint timeouts.

### 1.2 Inspecting the Dead-Letter Queue (DLQ)
A transaction transitions to **Dead-Letter** state after 5 failed retries:
1. Locate the item in the `SMRITI UIE Sync Queue` list.
2. Read the **Dead Letter Reason** column containing the last error message.
3. To retry a DLQ item after fixing the connection, reset its status to `Pending` and clear the `retry_count` back to `0`.

---

## 2. Tally Connection Debugging

### 2.1 Verifying the SOAP Port
Tally Prime operates on a local SOAP port (e.g. `http://localhost:9000`).
* Try executing `curl -X POST http://localhost:9000` from the app server terminal to ensure the port is exposed and receiving requests.

### 2.2 Handling Schema Errors
If Tally throws XML parsing errors (such as missing ledgers):
1. Verify if **Auto-Create Ledgers** is enabled in `SMRITI Tally Settings`.
2. Inspect `Tally.imp` (located at `F:\Tally.ERP9\Tally.imp`) for detailed parser error stacks.

---

## Author Profile (Document End)

- **Author**: Jawahar R. Mallah
- **Designation**: Founder & Chief Architect
- **Organization**: AITDL – AI Technology & Development Lab
- **Professional Experience**: 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.

> "Always decision-ready."
> 
> — Jawahar R. Mallah
> Founder & Chief Architect, AITDL
