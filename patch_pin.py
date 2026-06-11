import re

def patch():
    path = "apps/smriti_retail_os/smriti_retail_os/billing_api.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    old_logic = """def validate_manager_override(pin, action_type, invoice_name=None):
    \"\"\"
    Validates entered PIN against users with SMRITI Store Manager or System Manager role.
    Checks custom_smriti_pin first, then falls back to primary login password.
    \"\"\"
    if not pin:
        return {"authorized": False, "message": _("PIN is required.")}

    from frappe.utils.password import check_password as check_smriti_pin
    import frappe.auth

    # Find users with manager roles
    managers = frappe.db.get_all(
        "Has Role",
        filters={"role": ["in", ["SMRITI Store Manager", "System Manager"]]},
        pluck="parent"
    )

    for mgr in set(managers):
        # Only active users
        if not frappe.db.get_value("User", mgr, "enabled"):
            continue

        authenticated = False
        try:
            # 1. Try SMRITI Dedicated PIN first
            if frappe.db.get_value("User", mgr, "custom_smriti_pin"):
                try:
                    check_smriti_pin(mgr, pin, fieldname="custom_smriti_pin")
                    authenticated = True
                except frappe.AuthenticationError:
                    pass

            # 2. Fallback to primary password
            if not authenticated:
                frappe.auth.check_password(mgr, pin)
                authenticated = True

            if authenticated:"""

    new_logic = """def validate_manager_override(pin, action_type, invoice_name=None):
    \"\"\"
    Validates entered PIN against users with SMRITI Store Manager or System Manager role.
    Strictly requires custom_smriti_pin (no fallback to login password).
    \"\"\"
    if not pin:
        return {"authorized": False, "message": _("PIN is required.")}

    from frappe.utils.password import check_password as check_smriti_pin

    # Find users with manager roles
    managers = frappe.db.get_all(
        "Has Role",
        filters={"role": ["in", ["SMRITI Store Manager", "System Manager"]]},
        pluck="parent"
    )

    for mgr in set(managers):
        # Only active users
        if not frappe.db.get_value("User", mgr, "enabled"):
            continue

        authenticated = False
        try:
            # Strictly use SMRITI Dedicated PIN
            if frappe.db.get_value("User", mgr, "custom_smriti_pin"):
                try:
                    check_smriti_pin(mgr, pin, fieldname="custom_smriti_pin")
                    authenticated = True
                except frappe.AuthenticationError:
                    pass

            if authenticated:"""

    if old_logic in content:
        content = content.replace(old_logic, new_logic)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Patched billing_api.py")
    else:
        print("Could not find old_logic in billing_api.py")

if __name__ == "__main__":
    patch()