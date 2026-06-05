# SMRITI Retail OS — Supplier Lookup Fix Report

This report documents the resolution of the supplier lookup issue where active Individual suppliers were not appearing in standard Purchase Orders.

---

## 🛠️ Files Modified

* **Modified**: [purchase_order.js](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/public/js/purchase_order.js)

---

## 🔄 Before / After Filter Logic

### Before
In [purchase_order.js](file:///d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/public/js/purchase_order.js#L68-L73):
```javascript
function _smriti_po_setup(frm) {
    // Filter suppliers — active only
    frm.set_query("supplier", function () {
        return { filters: { disabled: 0, supplier_type: "Company" } };
    });
    ...
}
```
* **Effect**: Only suppliers with `supplier_type` set to `"Company"` were displayed. Suppliers created via SMRITI dashboard's `quick_create_supplier` (which default to `"Individual"`) were completely excluded.

### After
```javascript
function _smriti_po_setup(frm) {
    // Filter suppliers — active only
    frm.set_query("supplier", function () {
        return { filters: { disabled: 0 } };
    });
    ...
}
```
* **Effect**: All active suppliers (`disabled: 0`), regardless of type (`Company` or `Individual`), are now displayed in the selection field.

---

## 🧪 Validation and Verification Results

1. **Suppliers List Verification**:
   * Verified that the database contains `Test Advanced Supplier` (Individual) and that it is active (`disabled: 0`).
2. **Desk Purchase Order Form**:
   * Logged in as `admin@erpnbook.com` (Store Manager role, which subjects them to the custom script query filters).
   * Opened a new **Purchase Order** (`/app/purchase-order/new`).
   * Clicked the **Supplier** field. Both `Test Advanced Supplier` (Individual) and standard Company suppliers now correctly populate and are fully selectable.
3. **Purchase Receipt (GRN) Verification**:
   * Opened a new **Purchase Receipt** (`/app/purchase-receipt/new`).
   * Verified that the Supplier dropdown behaves identically to the Purchase Order page, without regression.
4. **Automated Test Results**:
   * Ran the `smriti_retail_os` backend test suite:
     * **Result**: All tests ran and verified successfully.

---

## ⚠️ Regression Risks & Mitigation

* **Risk**: Accidentally selecting inactive or disabled suppliers.
  * *Mitigation*: The filter `{ disabled: 0 }` explicitly ensures that disabled suppliers remain hidden in the dropdown.
* **Risk**: Linking a supplier without a mapped billing or shipping address.
  * *Mitigation*: SMRITI's dynamic hooks (`hooks_logic.py:sync_supplier_address_and_credit_days`) automatically execute on-save handlers to create default address links if not already present.
