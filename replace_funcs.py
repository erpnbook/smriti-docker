import sys

def replace_functions():
    path = "apps/smriti_retail_os/smriti_retail_os/psv_service.py"
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 1. Replace process_physical_snapshot_submit
    start = -1
    end = -1
    for i, line in enumerate(lines):
        if line.startswith("def process_physical_snapshot_submit(doc):"):
            start = i
        elif start != -1 and line.startswith("def process_physical_snapshot_cancel(doc):"):
            end = i
            break
            
    new_func = """def process_physical_snapshot_submit(doc):
    \"\"\"Generates a PSV Transaction for the audit variance.\"\"\"
    if doc.status != "Approved":
        frappe.throw(_("Audit Snapshots must be explicitly approved by a Store Manager or Administrator before submitting."))

    # Save approval details
    doc.approved_by = frappe.session.user
    doc.approved_on = now_datetime()

    items_data = []
    for item in doc.items:
        if item.variance == 0.0:
            continue
        items_data.append({
            "item_code": item.item_code,
            "qty": item.variance, # Ledger expects + for surplus, - for shrinkage
            "reason": item.variance_reason
        })

    if items_data:
        create_psv_transaction(
            psa=doc.party_stock_account,
            transaction_type="AUDIT_ADJUSTMENT",
            items=items_data,
            company=doc.company,
            reference_doctype=doc.doctype,
            reference_name=doc.name,
            remarks=f"Physical Snapshot Approved",
            posting_date=get_datetime(doc.audit_date)
        )

"""
    lines = lines[:start] + [new_func] + lines[end:]

    # 2. Replace process_physical_snapshot_cancel
    start = -1
    end = -1
    for i, line in enumerate(lines):
        if line.startswith("def process_physical_snapshot_cancel(doc):"):
            start = i
        elif start != -1 and line.startswith("def validate_sales_invoice_cancel(doc, method=None):"):
            end = i
            break
            
    new_cancel = """def process_physical_snapshot_cancel(doc):
    \"\"\"Reverses physical stock audit adjustments by cancelling PSV Transaction\"\"\"
    doc.approved_by = None
    doc.approved_on = None

    tx_name = frappe.db.get_value("SMRITI PSV Transaction", {"reference_doctype": doc.doctype, "reference_name": doc.name, "docstatus": 1}, "name")
    if tx_name:
        tx = frappe.get_doc("SMRITI PSV Transaction", tx_name)
        tx.cancel()

"""
    lines = lines[:start] + [new_cancel] + lines[end:]

    # 3. Replace process_sales_invoice_submit
    start = -1
    end = -1
    for i, line in enumerate(lines):
        if line.startswith("def process_sales_invoice_submit(doc, method=None):"):
            start = i
        elif start != -1 and line.startswith("def process_sales_invoice_cancel(doc, method=None):"):
            end = i
            break
            
    new_inv_submit = """def process_sales_invoice_submit(doc, method=None):
    \"\"\"
    Called on Sales Invoice on_submit hook.
    CRITICAL: Wrapped in try/except — PSV errors must NEVER block Sales Invoice submission.
    \"\"\"
    if not doc.get("custom_party_stock_account"):
        return

    try:
        posting_dt = get_posting_datetime(doc)
        tx_type = "RETURN" if doc.is_return else "TRANSFER_OUT"

        items_data = []
        for item in doc.items:
            items_data.append({
                "item_code": item.item_code,
                "qty": item.qty,
                "rate": item.rate
            })

        if items_data:
            create_psv_transaction(
                psa=doc.custom_party_stock_account,
                transaction_type=tx_type,
                items=items_data,
                company=doc.company,
                reference_doctype=doc.doctype,
                reference_name=doc.name,
                remarks=f"Generated from Sales Invoice",
                posting_date=posting_dt
            )
    except Exception as e:
        frappe.log_error(title=f"PSV Shadow Ledger Error: {doc.name}", message=frappe.get_traceback())
        
        frappe.get_doc({
            "doctype": "SMRITI PSV Exception Record",
            "party_stock_account": doc.custom_party_stock_account,
            "exception_type": "Hook Failure",
            "reference_doctype": doc.doctype,
            "reference_name": doc.name,
            "description": f"Failed to create PSV Transaction during invoice submission: {str(e)}",
            "status": "Pending Reconciliation"
        }).insert(ignore_permissions=True)
        frappe.db.commit()

"""
    lines = lines[:start] + [new_inv_submit] + lines[end:]

    # 4. Replace process_sales_invoice_cancel
    start = -1
    end = -1
    for i, line in enumerate(lines):
        if line.startswith("def process_sales_invoice_cancel(doc, method=None):"):
            start = i
        elif start != -1 and line.startswith("def get_posting_datetime(doc):"):
            end = i
            break
            
    new_inv_cancel = """def process_sales_invoice_cancel(doc, method=None):
    \"\"\"
    Called on Sales Invoice on_cancel hook.
    CRITICAL: Wrapped in try/except to prevent blocking cancellation.
    \"\"\"
    if not doc.get("custom_party_stock_account"):
        return

    try:
        tx_name = frappe.db.get_value("SMRITI PSV Transaction", {"reference_doctype": doc.doctype, "reference_name": doc.name, "docstatus": 1}, "name")
        if tx_name:
            tx = frappe.get_doc("SMRITI PSV Transaction", tx_name)
            tx.cancel()
    except Exception as e:
        frappe.log_error(title=f"PSV Shadow Ledger Cancellation Error: {doc.name}", message=frappe.get_traceback())
        
        frappe.get_doc({
            "doctype": "SMRITI PSV Exception Record",
            "party_stock_account": doc.custom_party_stock_account,
            "exception_type": "Hook Failure",
            "reference_doctype": doc.doctype,
            "reference_name": doc.name,
            "description": f"Failed to cancel PSV Transaction during invoice cancellation: {str(e)}",
            "status": "Pending Reconciliation"
        }).insert(ignore_permissions=True)
        frappe.db.commit()

# --- SALES INVOICE HOOKS ---───
"""
    lines = lines[:start] + [new_inv_cancel] + lines[end:]

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("All functions replaced successfully")

if __name__ == "__main__":
    replace_functions()
