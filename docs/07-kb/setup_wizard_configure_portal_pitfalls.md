---
title: "Setup Wizard & Configure Portal Provisioning Pitfalls"
description: "A comprehensive troubleshooting guide covering critical issues and errors encountered during Setup Wizard deployment and Configure Portal settings synchronization."
author: "SMRITI Development Team"
date: "2026-06-02"
---

# 🛡️ Setup Wizard & Configure Portal Provisioning Pitfalls

This guide details critical issues resolved during the development and stabilization of the SMRITI Setup & Configuration Wizard and the Configure Portal settings synchronization.

---

## 1. Customer Group Tree Node Violation

### The Problem
During Step 5 (Deployment) of the Setup Wizard, the console throws:
```text
CRITICAL ERROR: Cannot select a Group type Customer Group. Please select a non-group Customer Group.
FAILURE: Cannot select a Group type Customer Group. Please select a non-group Customer Group.
```

### Root Cause
In ERPNext, `Customer Group` is a tree-based DocType. The system enforces a strict rule: **Transactions and Customers must be assigned to leaf nodes (non-group nodes)**. You cannot assign a Customer (like `Walk-in Customer`) directly to a parent group node (such as `All Customer Groups`).

On fresh databases, if you only have the root parent node `All Customer Groups`, attempting to link the Walk-in Customer directly to it raises a validation exception.

### Resolution
Ensure the setup script validates the group type of the selected Customer Group. If it is a group, automatically create a leaf node under it (e.g. `Individual` or a custom sub-group) and associate the customer with this leaf node.

```python
customer_group = args.get("customer_group") or "All Customer Groups"
# If the target is a parent group, resolve to or create a leaf sub-group
is_group = frappe.db.get_value("Customer Group", customer_group, "is_group")
if is_group:
    leaf_group = "Individual - " + company_abbr
    if not frappe.db.exists("Customer Group", leaf_group):
        cg = frappe.new_doc("Customer Group")
        cg.customer_group_name = leaf_group
        cg.parent_customer_group = customer_group
        cg.is_group = 0
        cg.insert(ignore_permissions=True)
    customer_group = leaf_group
```

---

## 2. Mode of Payment Defaults & Linked Ledger Accounts

### The Problem
The deployment fails with:
```text
CRITICAL FAILURE: ["{\"message\":\"Please set default Cash or Bank account in Mode of Payments Cash, Bank, UPI\",\"as_table\":false,\"title\":\"Missing Account\"...
```

### Root Cause
ERPNext allows defining general `Mode of Payment` documents globally (e.g., `Cash`, `Bank`, `UPI`). However, for a Mode of Payment to be usable in transactions or inside a POS Profile for a specific company, it must have a **default ledger account linked for that specific Company**. If the link is missing, invoice posting will throw `Missing Account` validation errors.

### Resolution
For every Mode of Payment activated in the setup wizard, programmatically verify and append a row in the Mode of Payment's `accounts` table mapping the company to its corresponding ledger account.

```python
def link_mode_of_payment_account(mode_of_payment, company, account):
    doc = frappe.get_doc("Mode of Payment", mode_of_payment)
    # Check if company already linked
    exists = False
    for row in doc.accounts:
        if row.company == company:
            exists = True
            break
            
    if not exists:
        doc.append("accounts", {
            "company": company,
            "default_account": account
        })
        doc.save(ignore_permissions=True)
        frappe.db.commit()
```

---

## 3. Mandatory Fields in Programmatic POS Profile Creation

### The Problem
When trying to create a `POS Profile` during deployment, the operation fails with validation errors stating that write-off accounts are mandatory.

### Root Cause
In ERPNext v15/v16, creating a `POS Profile` requires specifying:
1. `write_off_account`: The ledger account used to write off small differences in point-of-sale invoices.
2. `write_off_cost_center`: The cost center associated with the write-offs.

If these are not populated, the document validation logic blocks the insert.

### Resolution
Resolve standard write-off account and cost center defaults for the newly created Company, and set them explicitly on the `POS Profile` before calling `.insert()`.

```python
pos_profile = frappe.new_doc("POS Profile")
pos_profile.name = args.get("pos_profile_name")
pos_profile.company = company_name
pos_profile.warehouse = warehouse_name

# Resolve mandatory write-off properties
write_off_account = frappe.db.get_value("Account", {
    "account_type": "Write Off",
    "company": company_name
}, "name")
# Fallback to a standard expense account if specialized write-off account isn't found
if not write_off_account:
    write_off_account = frappe.db.get_value("Account", {
        "account_name": "Write Off", 
        "company": company_name
    }, "name")

cost_center = frappe.db.get_value("Cost Center", {
    "is_group": 0,
    "company": company_name
}, "name")

pos_profile.write_off_account = write_off_account
pos_profile.write_off_cost_center = cost_center
pos_profile.insert(ignore_permissions=True)
```

---

## 4. Standalone Pages and CSRF Token Injection

### The Problem
In the **Configure Portal** (`/configure`), trying to load brands or save settings outputs error notifications:
```text
Failed to load brands: ["{\"message\":\"Invalid Request\"...
Failed to save settings: ["{\"message\":\"Invalid Request\"...
```

### Root Cause
Frappe employs strict **Cross-Site Request Forgery (CSRF)** checks on all whitelisted REST API calls (`/api/method/...`). 
In standard Frappe templates that extend base layouts (`{% extends "templates/web.html" %}`), the `csrf_token` is automatically injected into the page header and Javascript namespace. 

However, `/configure` and `/setup-wizard` are designed as **standalone, direct-render HTML pages** (without base layout inheritance) to enforce custom dark whitelabel styling. Without explicit handling, `{{ csrf_token }}` in the template renders as an empty string, causing the API requests to fail with a `403/500 Invalid Request` status.

### Resolution
1. In the page controller (e.g. `configure.py`), retrieve and append the active session CSRF token to the context:
   ```python
   def get_context(context):
       context.no_cache = 1
       context.title = "SMRITI Config Portal"
       context.csrf_token = frappe.sessions.get_csrf_token()
   ```

2. In the HTML/Javascript call helper, include the token under the `X-Frappe-CSRF-Token` header:
   ```javascript
   const headers = {
     'Content-Type': 'application/json',
     'Accept': 'application/json'
   };
   
   if (window.csrf_token) {
     headers['X-Frappe-CSRF-Token'] = window.csrf_token;
   }
   
   // Use in fetch calls
   fetch('/api/method/...', {
     method: 'POST',
     headers: headers,
     body: JSON.stringify(data)
   })
   ```
