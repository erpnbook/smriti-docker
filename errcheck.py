rows = frappe.db.get_all("Error Log", fields=["title","creation","error"], order_by="creation desc", limit=20)
for r in rows:
    print("---")
    print("TITLE:", r.get("title"))
    print("TIME:", r.get("creation"))
    print("ERROR:", str(r.get("error",""))[:500])
