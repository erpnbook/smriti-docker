import frappe
frappe.init(site="frontend")
frappe.connect()

rows = frappe.db.get_all(
    "Error Log",
    fields=["title", "creation", "error"],
    order_by="creation desc",
    limit=25
)

for r in rows:
    print("=" * 80)
    print(f"TITLE: {r.title}")
    print(f"TIME:  {r.creation}")
    print(f"ERROR: {str(r.error)[:600]}")
    print()
