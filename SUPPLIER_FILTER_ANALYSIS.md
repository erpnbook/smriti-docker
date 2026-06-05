# SMRITI Retail OS — Supplier Filter Analysis

Detailed analysis of the query filters applied on the `supplier` field across all SMRITI modules and standard ERPNext pages.

---

## 📋 Comprehensive Filter Mapping

### 1. Standard Purchase Order Form
* **File Path**: [purchase_order.js](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/public/js/purchase_order.js)
* **Code Reference**:
  ```javascript
  function _smriti_po_setup(frm) {
      // Filter suppliers — active only
      frm.set_query("supplier", function () {
          return { filters: { disabled: 0, supplier_type: "Company" } };
      });
  }
  ```
* **Behavior**: If the user is **not** a `System Manager`, they are subjected to `_smriti_po_setup`, which restricts results to suppliers where `supplier_type == "Company"`. Individual-type suppliers are completely hidden.

### 2. Standard Purchase Receipt Form (GRN)
* **File Path**: [purchase_receipt.js](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/public/js/purchase_receipt.js)
* **Code Reference**:
  ```javascript
  function _smriti_pr_setup(frm) {
      frm.set_query("supplier", function () {
          return { filters: { disabled: 0 } };
      });
  }
  ```
* **Behavior**: Does **not** filter by `supplier_type`. It only filters out disabled suppliers, so individual suppliers appear correctly here.

### 3. SMRITI Purchase Management (Desk wrapper page)
* **File Path**: [smriti_purchase.js](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/public/js/smriti_purchase.js)
* **Code Reference**:
  ```javascript
  frappe.call({
      method: "frappe.client.get_list",
      args: {
          doctype: "Supplier",
          filters: { disabled: 0 },
          fields: ["name", "supplier_name"],
          limit_page_length: 200
      },
      ...
  ```
* **Behavior**: Does **not** restrict by `supplier_type`. It fetches all active suppliers.

### 4. Standalone SMRITI Purchase Manager
* **File Path**: [purchase.html](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www/purchase.html)
* **Code Reference**:
  ```javascript
  const res = await api('frappe.client.get_list', {
      doctype: 'Supplier',
      filters: [['supplier_name', 'like', `%${q}%`]],
      fields: ['name', 'supplier_name', 'supplier_group', 'supplier_type'],
      limit_page_length: 20
  });
  ```
* **Behavior**: Does **not** apply any `supplier_type` filters. It only performs full-text matching on `supplier_name`. However, if the query `q` is blank, it returns early and displays no list (requiring users to type to search).

---

## 🛠️ Required Fix Details

### 1. Remove Supplier Type Restriction on Purchase Orders
In [purchase_order.js](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/public/js/purchase_order.js#L68-L77), modify the query filter function so it aligns with `purchase_receipt.js` and allows both Individual and Company suppliers to appear:

```diff
-    // Filter suppliers — active only
-    frm.set_query("supplier", function () {
-        return { filters: { disabled: 0, supplier_type: "Company" } };
-    });
+    // Filter suppliers — active only
+    frm.set_query("supplier", function () {
+        return { filters: { disabled: 0 } };
+    });
```

### 2. Standardize Backend Quick-Creation Type (Optional Guard)
In [master_api.py](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/master_api.py#L174), we can ensure `quick_create_supplier` supports default parameters or sets `Company` if preferred, but removing the client-side link override restriction is the primary fix because suppliers of either type should be allowed to receive orders.

---

## 🧪 Validation and Verification Steps

After applying the fix, verify using the following steps:

1. **Desk Purchase Order Form**:
   * Log in as a Store Manager (e.g. `admin@erpnbook.com`).
   * Navigate to standard **Purchase Order** (`/app/purchase-order/new`).
   * Click on the **Supplier** field.
   * Verify that `Test Advanced Supplier` (which is of type `Individual`) is fully visible and selectable in the dropdown list.

2. **Standalone Purchase Manager**:
   * Open the SMRITI Purchase Manager (`/purchase`).
   * Switch to the **New Purchase Order** tab.
   * Click **Supplier** and type "Test".
   * Select `Test Advanced Supplier` and submit the PO.
   * Verify that the PO is successfully saved.
