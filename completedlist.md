# SMRITI Retail OS - Completed & Locked Features List

This file tracks the officially completed, verified, and locked features of the SMRITI Retail OS project.

---

## 🔒 Locked Features

### 1. Sizewise HSN & GST Auto-Detection, Truncation & Validation
* **Status**: Completed, Tested & Locked (No further changes or breaks)
* **Date**: 2026-06-01
* **Description**: Added full support for pasted details from Excel containing HSN (e.g. 8-digit `64011010`) and GST columns.
* **Key Mechanisms**:
  - Truncates pasted HSN codes to 6 digits (e.g., `64011010` -> `640110`) to satisfy ERPNext/India Compliance HSN validation rules.
  - Automatically queries the `GST Settings` validation status:
    - If validation is enabled (ON), only sets 6-digit HSN codes (skips invalid 4 or 5-digit HSN codes to prevent crashes).
    - If validation is disabled (OFF), sets HSN codes of any length.
  - Safely parses GST percentages, properly supporting floats (e.g. `5.0`), integers, and `0%` tax rates without fallback errors.
* **Modified Files**:
  - Backend API: [item_master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/item_master_api.py)
  - Frontend View: [sizewise_item.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/sizewise_item.html)
