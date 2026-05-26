from smriti_retail_os.boot import _apply_branding
import frappe

b = frappe._dict({
    'app_name': '',
    'brand_html': '',
    'sysdefaults': {'app_name': 'ERPNext'},
    'installed_apps': [{'name': 'erpnext', 'title': 'ERPNext'}],
    'sidebar_pages': {'pages': [{'name': 'Selling', 'app': 'erpnext', 'app_title': 'ERPNext'}]},
})

_apply_branding(b)

print("app_name:", b.app_name)
print("sysdefaults app_name:", b.sysdefaults.get('app_name'))
print("installed_apps title:", b.installed_apps[0]['title'])
print("sidebar page app_title:", b.sidebar_pages['pages'][0]['app_title'])
