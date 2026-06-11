import re

def patch():
    path = "apps/smriti_retail_os/smriti_retail_os/psv_service.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Header
    content = content.replace(
        "# @description: Handles user login, registration, and JWT token generation.",
        "# @description: Core service logic for SMRITI Party Stock Visibility."
    )

    # 2. openpyxl
    content = re.sub(
        r'except ImportError:\s*# Fallback mock.*?\s*pass',
        'except ImportError:\n            frappe.throw(_("Python library \'openpyxl\' is required to parse Excel files."))',
        content, flags=re.DOTALL
    )

    # 3. Add Universal Transaction Engine
    engine_code = """
# --- UNIVERSAL TRANSACTION ENGINE ---

def create_psv_transaction(psa, transaction_type, items, company=None, reference_doctype=None, reference_name=None, remarks=None, posting_date=None):
    if not company:
        company = frappe.db.get_value("SMRITI Party Stock Account", psa, "company")
        
    fingerprint = None
    if reference_doctype and reference_name:
        fingerprint = f"{transaction_type}::{reference_doctype}::{reference_name}"
        existing = frappe.db.get_value("SMRITI PSV Transaction", {"mapping_fingerprint": fingerprint, "docstatus": 1}, "name")
        if existing:
            return existing

    doc = frappe.new_doc("SMRITI PSV Transaction")
    doc.party_stock_account = psa
    doc.transaction_type = transaction_type
    doc.company = company
    doc.reference_doctype = reference_doctype
    doc.reference_name = reference_name
    doc.remarks = remarks
    if posting_date:
        doc.posting_date = posting_date
        
    for item in items:
        if not item.get("item_code") or not item.get("qty"):
            continue
        doc.append("items", {
            "item_code": item.get("item_code"),
            "qty": item.get("qty"),
            "rate": item.get("rate") or 0.0,
            "reason": item.get("reason") or ""
        })
        
    if not doc.items:
        return None
        
    doc.insert(ignore_permissions=True)
    doc.submit()
    return doc.name

# ─── SALES INVOICE HOOKS ───────────────────────────────────────────────────"""
    content = content.replace("# ─── SALES INVOICE HOOKS ───────────────────────────────────────────────────", engine_code)

    # 4. update import_opening_balances and add process_opening_balance
    new_opening = """def import_opening_balances(company, party_stock_account, items_data):
    return create_psv_transaction(
        psa=party_stock_account,
        transaction_type="OPENING",
        items=items_data,
        company=company,
        remarks="Initial Opening Balance Import"
    )

@frappe.whitelist()
def process_opening_balance(company, party_stock_account, items):
    if isinstance(items, str):
        import json
        items = json.loads(items)
    return import_opening_balances(company, party_stock_account, items)

# ─── OPERATIONAL HEALTH ALERTS"""
    content = re.sub(
        r'def import_opening_balances\(company, party_stock_account, items_data\):.*?# ─── OPERATIONAL HEALTH ALERTS',
        new_opening, content, flags=re.DOTALL
    )

    # 5. process_sales_upload_submit
    new_sales_submit = """def process_sales_upload_submit(doc):
    frappe.db.set_value(doc.doctype, doc.name, "status", "Imported")
    items_data = [{"item_code": i.item_code, "qty": i.qty_sold} for i in doc.items]
    create_psv_transaction(doc.party_stock_account, "SALES_UPLOAD", items_data, doc.company, doc.doctype, doc.name, f"Imported from {doc.name}")"""
    content = re.sub(
        r'def process_sales_upload_submit\(doc\):.*?def process_sales_upload_cancel',
        new_sales_submit + '\n\ndef process_sales_upload_cancel', content, flags=re.DOTALL
    )

    # 6. process_sales_upload_cancel
    new_sales_cancel = """def process_sales_upload_cancel(doc):
    frappe.db.set_value(doc.doctype, doc.name, "status", "Draft")
    tx_name = frappe.db.get_value("SMRITI PSV Transaction", {"reference_doctype": doc.doctype, "reference_name": doc.name, "docstatus": 1})
    if tx_name:
        frappe.get_doc("SMRITI PSV Transaction", tx_name).cancel()"""
    content = re.sub(
        r'def process_sales_upload_cancel\(doc\):.*?# ─── PHYSICAL SNAPSHOT LOGIC',
        new_sales_cancel + '\n\n# ─── PHYSICAL SNAPSHOT LOGIC', content, flags=re.DOTALL
    )

    # 7. process_physical_snapshot_submit
    new_audit_submit = """def process_physical_snapshot_submit(doc):
    if doc.status != "Approved":
        frappe.throw(_("Audit Snapshots must be explicitly approved before submitting."))
    doc.approved_by = frappe.session.user
    doc.approved_on = now_datetime()
    items_data = [{"item_code": i.item_code, "qty": i.variance, "reason": i.variance_reason} for i in doc.items if i.variance != 0.0]
    if items_data:
        create_psv_transaction(doc.party_stock_account, "AUDIT_ADJUSTMENT", items_data, doc.company, doc.doctype, doc.name, "Physical Snapshot Approved", get_datetime(doc.audit_date))"""
    content = re.sub(
        r'def process_physical_snapshot_submit\(doc\):.*?def process_physical_snapshot_cancel',
        new_audit_submit + '\n\ndef process_physical_snapshot_cancel', content, flags=re.DOTALL
    )

    # 8. process_physical_snapshot_cancel
    new_audit_cancel = """def process_physical_snapshot_cancel(doc):
    doc.approved_by = None
    doc.approved_on = None
    tx_name = frappe.db.get_value("SMRITI PSV Transaction", {"reference_doctype": doc.doctype, "reference_name": doc.name, "docstatus": 1})
    if tx_name:
        frappe.get_doc("SMRITI PSV Transaction", tx_name).cancel()"""
    content = re.sub(
        r'def process_physical_snapshot_cancel\(doc\):.*?def import_opening_balances',
        new_audit_cancel + '\n\ndef import_opening_balances', content, flags=re.DOTALL
    )

    # 9. process_sales_invoice_submit
    new_inv_submit = """def process_sales_invoice_submit(doc, method=None):
    if not doc.get("custom_party_stock_account"): return
    try:
        tx_type = "RETURN" if doc.is_return else "TRANSFER_OUT"
        items_data = [{"item_code": i.item_code, "qty": i.qty, "rate": i.rate} for i in doc.items]
        if items_data:
            create_psv_transaction(doc.custom_party_stock_account, tx_type, items_data, doc.company, doc.doctype, doc.name, "Generated from Sales Invoice", get_posting_datetime(doc))
    except Exception as e:
        frappe.log_error(title=f"PSV Error: {doc.name}", message=frappe.get_traceback())
        frappe.get_doc({"doctype": "SMRITI PSV Exception Record", "party_stock_account": doc.custom_party_stock_account, "exception_type": "Hook Failure", "reference_doctype": doc.doctype, "reference_name": doc.name, "description": str(e), "status": "Pending Reconciliation"}).insert(ignore_permissions=True)
        frappe.db.commit()"""
    content = re.sub(
        r'def process_sales_invoice_submit\(doc, method=None\):.*?def process_sales_invoice_cancel',
        new_inv_submit + '\n\ndef process_sales_invoice_cancel', content, flags=re.DOTALL
    )

    # 10. process_sales_invoice_cancel
    new_inv_cancel = """def process_sales_invoice_cancel(doc, method=None):
    if not doc.get("custom_party_stock_account"): return
    try:
        tx_name = frappe.db.get_value("SMRITI PSV Transaction", {"reference_doctype": doc.doctype, "reference_name": doc.name, "docstatus": 1})
        if tx_name: frappe.get_doc("SMRITI PSV Transaction", tx_name).cancel()
    except Exception as e:
        frappe.log_error(title=f"PSV Cancel Error: {doc.name}", message=frappe.get_traceback())
        frappe.get_doc({"doctype": "SMRITI PSV Exception Record", "party_stock_account": doc.custom_party_stock_account, "exception_type": "Hook Failure", "reference_doctype": doc.doctype, "reference_name": doc.name, "description": str(e), "status": "Pending Reconciliation"}).insert(ignore_permissions=True)
        frappe.db.commit()"""
    content = re.sub(
        r'def process_sales_invoice_cancel\(doc, method=None\):.*?(?=\n# ───|\Z)',
        new_inv_cancel, content, flags=re.DOTALL
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Patch applied successfully.")

if __name__ == "__main__":
    patch()
