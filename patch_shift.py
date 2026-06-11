import re

def patch_shift():
    path = "apps/smriti_retail_os/smriti_retail_os/shift_api.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    old_logic = """def _validate_manager_pin(pin, action_type, reference_name=None):
    \"\"\"
    Validates manager password and logs override as a Comment.
    Checks custom_smriti_pin first, then falls back to primary password.
    Mirrors billing_api.validate_manager_override logic.
    \"\"\"
    from frappe.utils.password import check_password as check_smriti_pin
    import frappe.auth

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

    new_logic = """def _validate_manager_pin(pin, action_type, reference_name=None):
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

    if old_logic in content:
        content = content.replace(old_logic, new_logic)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Patched shift_api.py")
    else:
        print("Could not find old_logic in shift_api.py")

def patch_security():
    path = "apps/smriti_retail_os/smriti_retail_os/security_api.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    old_logic = """def check_administrator_protection(email):
    \"\"\"Raises PermissionError if trying to modify the Administrator account by a non-Administrator.\"\"\"
    is_admin_target = False
    if email == "Administrator":
        is_admin_target = True
    else:
        admin_email = frappe.db.get_value("User", "Administrator", "email")
        if admin_email and email == admin_email:
            is_admin_target = True

    if is_admin_target:
        if frappe.session.user != "Administrator":
            frappe.throw(
                _("Access Denied: Only the Administrator user can modify the Administrator account."),
                frappe.PermissionError
            )"""

    new_logic = """def check_administrator_protection(email):
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

    if old_logic in content:
        content = content.replace(old_logic, new_logic)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Patched security_api.py")
    else:
        print("Could not find old_logic in security_api.py")

def patch_kb():
    path = "KNOWLEDGE_BASE.md"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    old_kb = """| **P0-01** | 🔴 Critical | Privilege escalation via Store Manager password reset | **OPEN** | `security_api.py` |
| **P1-01** | 🟠 High | Manager overrides use primary login password (shoulder-surfing risk) | **OPEN** | `billing_api.py` |"""

    new_kb = """| **P0-01** | 🔴 Critical | Privilege escalation via Store Manager password reset | ✅ **FIXED** | `security_api.py` |
| **P1-01** | 🟠 High | Manager overrides use primary login password (shoulder-surfing risk) | ✅ **FIXED** | `billing_api.py`, `shift_api.py` |"""
    
    if old_kb in content:
        content = content.replace(old_kb, new_kb)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Patched KB")
    else:
        print("Could not find old_kb in KNOWLEDGE_BASE.md")

if __name__ == "__main__":
    patch_shift()
    patch_security()
    patch_kb()