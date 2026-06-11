import sys

def patch():
    path = "apps/smriti_retail_os/smriti_retail_os/psv_service.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Header & openpyxl
    content = content.replace('''# @file: smriti_retail_os/psv_service.py
# @description: Handles user login, registration, and JWT token generation.''', '''# @file: smriti_retail_os/psv_service.py
# @description: Core service logic for SMRITI Party Stock Visibility (Dispatches, Sales Uploads, Snapshots).''')

    content = content.replace('''        except ImportError:
            # Fallback mock for testing environment without openpyxl
            pass''', '''        except ImportError:
            frappe.msgprint(_("Python library 'openpyxl' is required to parse Excel files. Please contact your system administrator."), indicator='red')
            frappe.throw(_("Missing dependency: openpyxl"))''')

    # 2. Universal Transaction Engine & import_opening_balances & process_opening_balance
    old_opening = '''def import_opening_balances(company, party_stock_account, items_data):
    """
    Programmatic helper to seed opening stock lying at a customer outlet location.
    items_data should be a list of dicts: [{'item_code': 'X', 'qty': 100}]
    """
    posting_dt = now_datetime()
    
    for row in items_data:
        make_ledger_entry(
            company=company,
            posting_datetime=posting_dt,
            party_stock_account=party_stock_account,
            item_code=row["item_code"],
            qty=row["qty"],
            voucher_type="Opening",
            voucher_no="OPENING-BALANCE-IMPORT"
        )

    log_activity(
        action_type="Opening Balance Import",
        party_stock_account=party_stock_account,
        details=f"Imported initial opening balances for {len(items_data)} items."
    )


# ─── OPERATIONAL HEALTH ALERTS & CHECKS ────────────────────────────────────────'''
    
    # Notice I'm replacing the `import_opening_balances` block and also injecting the engine
    if old_opening in content:
        pass # it matches
    else:
        # try without strict lines
        pass
        
    # Wait, replacing string by string is easier. Let's do it method by method.
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    patch()