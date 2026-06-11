import frappe

frappe.init(site='smriti_retail')
frappe.connect()

doc = frappe.get_doc('SMRITI Print Template', 'TEST_VISUAL_V24A')
print('Current version:', doc.custom_version)
print('Raw template len:', len(doc.raw_template or ''))
doc.raw_template = (doc.raw_template or '') + ' '
doc.save(ignore_permissions=True)
frappe.db.commit()
print('Saved version:', doc.custom_version)

versions = frappe.db.get_all('SMRITI Print Template Version', filters={'template': 'TEST_VISUAL_V24A'}, fields=['name', 'version_number'])
print('Versions created:', versions)
