import frappe
frappe.init('frontend', sites_path='sites')
frappe.connect()

profiles = frappe.db.sql("SELECT name, module_profile_name FROM `tabModule Profile`", as_dict=True)
print("=== Module Profiles ===")
for p in profiles:
    print(p)

print("\n=== Blocked Modules (Cashier) ===")
cashier = frappe.db.sql(
    "SELECT module FROM `tabBlock Module` WHERE parent='SMRITI Cashier Profile'",
    as_dict=True
)
for m in cashier:
    print(" BLOCKED:", m.module)

print("\n=== Blocked Modules (Manager) ===")
manager = frappe.db.sql(
    "SELECT module FROM `tabBlock Module` WHERE parent='SMRITI Store Manager Profile'",
    as_dict=True
)
for m in manager:
    print(" BLOCKED:", m.module)

frappe.destroy()
