# SMRITI Retail OS — Supplier Lookup Diagnostic Report

This report documents the verification steps and data-level diagnostics performed to identify why existing suppliers are not appearing in the Supplier selection fields.

---

## 🔍 Diagnostic Checklist & Results

### 1. Verification of Existing Suppliers
* **Database Query**: Executed `frappe.get_all('Supplier', fields=['name', 'supplier_name', 'supplier_type', 'disabled'])` in the active site `smriti_retail`.
* **Result**:
  ```json
  [
    {
      "name": "Test Advanced Supplier",
      "supplier_name": "Test Advanced Supplier",
      "supplier_type": "Individual",
      "disabled": 0
    }
  ]
  ```
* **Status**: **Verified**. An active supplier exists in the database.

### 2. Status & Expiry Auditing
* **Active Check**: The field `disabled` is set to `0` (Active).
* **Status**: **Verified**. The supplier record is enabled.

### 3. Role Permission Analysis
* **Permission Query**: Checked `Custom DocPerm` and standard metadata permissions for the `Supplier` DocType.
* **DocPerm Records**:
  ```json
  [
    {
      "role": "SMRITI Store Manager",
      "read": 1,
      "write": 1,
      "create": 1,
      "doctype": "Custom DocPerm"
    }
  ]
  ```
* **Status**: **Verified**. The role `SMRITI Store Manager` (held by user `admin@smriti.io` and `Administrator`) has full read/write permissions on the `Supplier` master. No database-level permission block is causing the blank field.

### 4. Company Ownership Check
* **Status**: **Verified**. Suppliers in ERPNext are global entities. No company-specific filtering at the database layer is restricting the record.

---

## ⚠️ Identified Root Cause
The lookup failure is caused by a **mismatch between client-side query filters and backend creation defaults**:

1. **Client-Side Exclusion**:
   In [purchase_order.js](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/public/js/purchase_order.js), the standard `Purchase Order` form setup filters suppliers with:
   ```javascript
   frm.set_query("supplier", function () {
       return { filters: { disabled: 0, supplier_type: "Company" } };
   });
   ```
   This filter is applied to any user who is **not** a `System Manager` (which includes standard store managers like `admin@smriti.io`).

2. **Backend Type Mismatch**:
   In [master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/master_api.py), the `quick_create_supplier` method (which creates suppliers from the dashboard) hardcodes:
   ```python
   supp.supplier_type = "Individual"
   ```
   
As a result, any quick-created supplier is stored as an `Individual` and is completely filtered out of the selection dropdown on the Purchase Order screen.
