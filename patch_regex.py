import re

def patch():
    # 1. Patch shift_api.py
    path_shift = "apps/smriti_retail_os/smriti_retail_os/shift_api.py"
    with open(path_shift, "r", encoding="utf-8") as f:
        content = f.read()

    new_shift = """def _validate_manager_pin(pin, action_type, reference_name=None):
    \"\"\"
    Validates manager password and logs override as a Comment.
    Strictly requires custom_smriti_pin (no fallback to primary password).
    \"\"\"
    from frappe.utils.password import check_password as check_smriti_pin

    managers = frappe.db.get_all(
        "Has Role",
        filters={"role": ["in", ["SMRITI Store Manager", "System Manager"]]},
        pluck="parent"
    )

    for mgr in set(managers):
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
    content = re.sub(r'def _validate_manager_pin\(pin, action_type, reference_name=None\):.*?if authenticated:', new_shift, content, flags=re.DOTALL)
    with open(path_shift, "w", encoding="utf-8") as f:
        f.write(content)

    # 2. Patch security_api.py
    path_sec = "apps/smriti_retail_os/smriti_retail_os/security_api.py"
    with open(path_sec, "r", encoding="utf-8") as f:
        content = f.read()

    new_sec = """def check_administrator_protection(email):
    \"\"\"Raises PermissionError if trying to modify the Administrator account or any System Manager by a non-Administrator/System Manager.\"\"\"
    if frappe.session.user == "Administrator" or "System Manager" in frappe.get_roles(frappe.session.user):
        return

    is_admin_target = False
    if email == "Administrator":
        is_admin_target = True
    else:
        admin_email = frappe.db.get_value("User", "Administrator", "email")
        if admin_email and email == admin_email:
            is_admin_target = True

    target_roles = []
    if frappe.db.exists("User", email):
        target_roles = frappe.get_roles(email)

    if is_admin_target or "System Manager" in target_roles or "Administrator" in target_roles:
        frappe.throw(
            _("Access Denied: Store Managers cannot modify System Manager or Administrator accounts."),
            frappe.PermissionError
        )"""
    content = re.sub(r'def check_administrator_protection\(email\):.*?frappe.PermissionError\n\s*\)', new_sec, content, flags=re.DOTALL)
    with open(path_sec, "w", encoding="utf-8") as f:
        f.write(content)

    print("Patched shift and security via regex")

if __name__ == "__main__":
    patch()