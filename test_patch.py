import re

_BRAND_NAME = "SMRITI Retail OS"
_REBRAND_APPS = {"erpnext", "frappe"}
_BRAND_RE = re.compile(r"ERPNext|Frappe\s+(Technologies|Framework)", re.IGNORECASE)

def _replace(text):
    text = re.sub(r"ERPNext", _BRAND_NAME, text)
    return text

def _patch_page(page):
    if not isinstance(page, dict):
        return
    if page.get("app_title") and _BRAND_RE.search(page["app_title"]):
        page["app_title"] = _replace(page["app_title"])
    if (page.get("app") or "").lower() in _REBRAND_APPS:
        page["app_title"] = _BRAND_NAME

b = {
    "app_name": "ERPNext",
    "sysdefaults": {"app_name": "ERPNext"},
    "installed_apps": [{"name": "erpnext", "title": "ERPNext"}],
    "sidebar_pages": {
        "pages": [{"name": "Selling", "app": "erpnext", "app_title": "ERPNext"}]
    },
}

# patch sidebar
for p in b["sidebar_pages"]["pages"]:
    _patch_page(p)

# patch installed apps
for app in b["installed_apps"]:
    if (app.get("name") or "").lower() in _REBRAND_APPS:
        app["title"] = _BRAND_NAME

# patch sysdefaults
b["sysdefaults"]["app_name"] = _BRAND_NAME
b["app_name"] = _BRAND_NAME

print("app_name:", b["app_name"])
print("sysdefaults app_name:", b["sysdefaults"]["app_name"])
print("installed_apps title:", b["installed_apps"][0]["title"])
print("sidebar app_title:", b["sidebar_pages"]["pages"][0]["app_title"])

all_ok = (
    b["app_name"] == _BRAND_NAME and
    b["sysdefaults"]["app_name"] == _BRAND_NAME and
    b["installed_apps"][0]["title"] == _BRAND_NAME and
    b["sidebar_pages"]["pages"][0]["app_title"] == _BRAND_NAME
)
print("ALL TESTS PASSED" if all_ok else "SOME TESTS FAILED")
