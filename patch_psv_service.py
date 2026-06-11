import re

def patch():
    path = "apps/smriti_retail_os/smriti_retail_os/psv_service.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # process_physical_snapshot_submit
    old_submit_snapshot = r'''def process_physical_snapshot_submit\(doc\):
    """Writes audit variance entries to Shadow Ledger"""
    if doc\.status != "Approved":
        frappe\.throw\(_\("Audit Snapshots must be explicitly approved by a Store Manager or Administrator before submitting\."\)\)

    # Save approval details
    doc\.approved_by = frappe\.session\.user
    doc\.approved_on = now_datetime\(\)

    for item in doc\.items:
        if item\.variance == 0\.0:
            continue

        adj_type = "Surplus Correction" if item\.variance > 0\.0 else "Shrinkage"
        make_ledger_entry\(
            company=doc\.company,
            posting_datetime=get_datetime\(doc\.audit_date\),
            party_stock_account=doc\.party_stock_account,
            item_code=item\.item_code,
            qty=item\.variance, # Positive for surplus, negative for shrinkage
            voucher_type="Adjustment",
            voucher_no=doc\.name,
            adjustment_type=adj_type,
            reason=item\.variance_reason,
            approved_by=doc\.approved_by,
            approved_on=doc\.approved_on
        \)

    log_activity\(
        action_type="Approve Snapshot",
        party_stock_account=doc\.party_stock_account,
        reference_doctype=doc\.doctype,
        reference_name=doc\.name,
        details=f"Physical snapshot approved and posted with {len\(doc\.items\)} adjustment rows\."
    \)'''

    new_submit_snapshot = '''def process_physical_snapshot_submit(doc):
    """Generates a PSV Transaction for the audit variance."""
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
        )'''
    content = re.sub(old_submit_snapshot, new_submit_snapshot, content, flags=re.MULTILINE)

    # process_physical_snapshot_cancel
    old_cancel_snapshot = r'''def process_physical_snapshot_cancel\(doc\):
    """Reverses physical stock audit adjustments"""
    doc\.approved_by = None
    doc\.approved_on = None

    for item in doc\.items:
        if item\.variance == 0\.0:
            continue

        make_ledger_entry\(
            company=doc\.company,
            posting_datetime=now_datetime\(\),
            party_stock_account=doc\.party_stock_account,
            item_code=item\.item_code,
            qty=item\.variance \* -1\.0, # Reverse entry
            voucher_type="Adjustment",
            voucher_no=f"VOID-{doc\.name}",
            reason=_\("Snapshot Cancelled"\)
        \)

    log_activity\(
        action_type="Cancel Snapshot",
        party_stock_account=doc\.party_stock_account,
        reference_doctype=doc\.doctype,
        reference_name=doc\.name,
        details=f"Physical snapshot cancelled\. Adjustments reversed\."
    \)'''
    new_cancel_snapshot = '''def process_physical_snapshot_cancel(doc):
    """Reverses physical stock audit adjustments by cancelling PSV Transaction"""
    doc.approved_by = None
    doc.approved_on = None

    tx_name = frappe.db.get_value("SMRITI PSV Transaction", {"reference_doctype": doc.doctype, "reference_name": doc.name, "docstatus": 1}, "name")
    if tx_name:
        tx = frappe.get_doc("SMRITI PSV Transaction", tx_name)
        tx.cancel()'''
    content = re.sub(old_cancel_snapshot, new_cancel_snapshot, content, flags=re.MULTILINE)

    # process_sales_invoice_submit
    old_invoice_submit = r'''def process_sales_invoice_submit\(doc, method=None\):
    """
    Called on Sales Invoice on_submit hook\.
    CRITICAL: Wrapped in try/except — PSV errors must NEVER block Sales Invoice submission\.
    """
    if not doc\.get\("custom_party_stock_account"\):
        return

    try:
        posting_dt = get_posting_datetime\(doc\)
        multiplier = -1\.0 if doc\.is_return else 1\.0
        voucher_type = "Return" if doc\.is_return else "Dispatch"

        for item in doc\.items:
            make_ledger_entry\(
                company=doc\.company,
                posting_datetime=posting_dt,
                party_stock_account=doc\.custom_party_stock_account,
                item_code=item\.item_code,
                qty=item\.qty \* multiplier,
                voucher_type=voucher_type,
                voucher_no=doc\.name
            \)

        action = "Return" if doc\.is_return else "Dispatch"
        log_activity\(
            action_type=f"{action} Posted",
            party_stock_account=doc\.custom_party_stock_account,
            reference_doctype=doc\.doctype,
            reference_name=doc\.name,
            details=f"{action} processed for {len\(doc\.items\)} items\."
        \)
    except Exception as e:
        # 1\. Log the error robustly
        frappe\.log_error\(title=f"PSV Shadow Ledger Error: {doc\.name}", message=frappe\.get_traceback\(\)\)
        
        # 2\. Create an operational alert \(Exception Record\)
        frappe\.get_doc\({
            "doctype": "SMRITI PSV Exception Record",
            "party_stock_account": doc\.custom_party_stock_account,
            "exception_type": "Hook Failure",
            "reference_doctype": doc\.doctype,
            "reference_name": doc\.name,
            "description": f"Failed to post ledger entries during invoice submission: {str\(e\)}",
            "status": "Pending Reconciliation"
        }\)\.insert\(ignore_permissions=True\)
        frappe\.db\.commit\(\)'''
        
    new_invoice_submit = '''def process_sales_invoice_submit(doc, method=None):
    """
    Called on Sales Invoice on_submit hook.
    CRITICAL: Wrapped in try/except — PSV errors must NEVER block Sales Invoice submission.
    """
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
        # 1. Log the error robustly
        frappe.log_error(title=f"PSV Shadow Ledger Error: {doc.name}", message=frappe.get_traceback())
        
        # 2. Create an operational alert (Exception Record)
        frappe.get_doc({
            "doctype": "SMRITI PSV Exception Record",
            "party_stock_account": doc.custom_party_stock_account,
            "exception_type": "Hook Failure",
            "reference_doctype": doc.doctype,
            "reference_name": doc.name,
            "description": f"Failed to create PSV Transaction during invoice submission: {str(e)}",
            "status": "Pending Reconciliation"
        }).insert(ignore_permissions=True)
        frappe.db.commit()'''
    content = re.sub(old_invoice_submit, new_invoice_submit, content, flags=re.MULTILINE)

    # process_sales_invoice_cancel
    old_invoice_cancel = r'''def process_sales_invoice_cancel\(doc, method=None\):
    """
    Called on Sales Invoice on_cancel hook\.
    CRITICAL: Wrapped in try/except to prevent blocking cancellation\.
    """
    if not doc\.get\("custom_party_stock_account"\):
        return

    try:
        posting_dt = now_datetime\(\)
        multiplier = 1\.0 if doc\.is_return else -1\.0 # Reverse of submit logic
        voucher_type = "Return" if doc\.is_return else "Dispatch"

        for item in doc\.items:
            make_ledger_entry\(
                company=doc\.company,
                posting_datetime=posting_dt,
                party_stock_account=doc\.custom_party_stock_account,
                item_code=item\.item_code,
                qty=item\.qty \* multiplier,
                voucher_type=voucher_type,
                voucher_no=f"VOID-{doc\.name}",
                reason=_\("Invoice Cancelled"\)
            \)

        action = "Return" if doc\.is_return else "Dispatch"
        log_activity\(
            action_type=f"Cancel {action}",
            party_stock_account=doc\.custom_party_stock_account,
            reference_doctype=doc\.doctype,
            reference_name=doc\.name,
            details=f"Invoice cancelled\. Negative ledger entries reversed\."
        \)
    except Exception as e:
        frappe\.log_error\(title=f"PSV Shadow Ledger Cancellation Error: {doc\.name}", message=frappe\.get_traceback\(\)\)
        
        frappe\.get_doc\({
            "doctype": "SMRITI PSV Exception Record",
            "party_stock_account": doc\.custom_party_stock_account,
            "exception_type": "Hook Failure",
            "reference_doctype": doc\.doctype,
            "reference_name": doc\.name,
            "description": f"Failed to post reversal ledger entries during invoice cancellation: {str\(e\)}",
            "status": "Pending Reconciliation"
        }\)\.insert\(ignore_permissions=True\)
        frappe\.db\.commit\(\)'''
        
    new_invoice_cancel = '''def process_sales_invoice_cancel(doc, method=None):
    """
    Called on Sales Invoice on_cancel hook.
    CRITICAL: Wrapped in try/except to prevent blocking cancellation.
    """
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
        frappe.db.commit()'''
    content = re.sub(old_invoice_cancel, new_invoice_cancel, content, flags=re.MULTILINE)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        print("Patched successfully")

if __name__ == "__main__":
    patch()
