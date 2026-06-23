import re

# ──────────────────────────────────────────
# 1. Patch hooks.py — add 4 new route rules
# ──────────────────────────────────────────
hooks_path = '/home/frappe/frappe-bench/apps/smriti_retail_os/smriti_retail_os/hooks.py'

new_routes = '''    {"from_route": "/release-notes",          "to_route": "release_notes"},       # www/release_notes.html
    {"from_route": "/support",                 "to_route": "smriti_support"},       # www/smriti_support.html
    {"from_route": "/psv-reconciliation",      "to_route": "psv_reconciliation"},   # www/psv_reconciliation.html
    {"from_route": "/psv-exception-analysis",  "to_route": "psv_exception_analysis"}, # www/psv_exception_analysis.html
    {"from_route": "/exception-analysis",      "to_route": "psv_exception_analysis"}, # alias
'''

insert_after = '    {"from_route": "/psv-opening-balance","to_route": "psv-opening-balance"}, # www/psv-opening-balance.html'

with open(hooks_path, 'r') as f:
    content = f.read()

if '/release-notes' in content:
    print('hooks.py: routes already present, skipping.')
else:
    content = content.replace(insert_after, insert_after + '\n' + new_routes)
    with open(hooks_path, 'w') as f:
        f.write(content)
    print('hooks.py: added 4 new route rules.')

# ──────────────────────────────────────────
# 2. Patch nav_config.js — activate 4 items
# ──────────────────────────────────────────
nav_path = '/home/frappe/frappe-bench/apps/smriti_retail_os/smriti_retail_os/public/js/smriti_nav_config.js'

with open(nav_path, 'r') as f:
    nav = f.read()

changes = [
    # reconciliation
    (
        '{ id: "reconciliation",\n          label: "Reconciliation",\n          status: "coming_soon",\n          progress: 0,\n          eta: "PSV Phase 1.3" }',
        '{ id: "reconciliation",\n          label: "Reconciliation",\n          route: "/psv-reconciliation",\n          standalone_route: "/psv-reconciliation",\n          status: "active" }'
    ),
    # exception_analysis
    (
        '{ id: "exception_analysis",\n          label: "Exception Analysis",\n          status: "coming_soon",\n          progress: 0,\n          eta: "PSV Phase 1.3" }',
        '{ id: "exception_analysis",\n          label: "Exception Analysis",\n          route: "/psv-exception-analysis",\n          standalone_route: "/psv-exception-analysis",\n          status: "active" }'
    ),
    # release_notes
    (
        '{ id: "release_notes",\n          label: "Release Notes",\n          status: "coming_soon",\n          progress: 0,\n          eta: "Q3 2026" }',
        '{ id: "release_notes",\n          label: "Release Notes",\n          route: "/release-notes",\n          standalone_route: "/release-notes",\n          status: "active" }'
    ),
    # support
    (
        '{ id: "support",\n          label: "Support",\n          status: "coming_soon",\n          progress: 0,\n          eta: "Q3 2026" }',
        '{ id: "support",\n          label: "Support",\n          route: "/support",\n          standalone_route: "/support",\n          status: "active" }'
    ),
]

patched = 0
for old, new in changes:
    if old in nav:
        nav = nav.replace(old, new)
        patched += 1
    else:
        print(f'WARNING: pattern not found for: {old[:60]}')

with open(nav_path, 'w') as f:
    f.write(nav)

print(f'nav_config.js: patched {patched}/4 coming_soon items to active.')
