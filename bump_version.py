import os, re

www_dir = '/home/frappe/frappe-bench/apps/smriti_retail_os/smriti_retail_os/www'

# Bump only sidebar_standalone.js from v2.0.1 → v2.0.2 in all HTML pages
# nav_config internal reference in sidebar_standalone.js stays at ?v=2.0.1 (already correct)
pattern = re.compile(r'smriti_sidebar_standalone\.js\?v=2\.0\.1')
updated = []
for fn in os.listdir(www_dir):
    if not fn.endswith('.html'):
        continue
    fpath = os.path.join(www_dir, fn)
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    nc = pattern.sub('smriti_sidebar_standalone.js?v=2.0.2', c)
    if nc != c:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(nc)
        updated.append(fn)

print(f'Bumped sidebar to v2.0.2 in {len(updated)} files')
