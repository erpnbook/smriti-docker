import os
import re

paths = [
    'd:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www',
    'F:/smriti_retail/apps/smriti_retail_os/smriti_retail_os/www'
]

patterns = [
    (re.compile(r'smriti_sidebar_standalone\.js(?:\?[^"\']*)?'), 'smriti_sidebar_standalone.js?v=2.0.4'),
    (re.compile(r'smriti_nav_config\.js(?:\?[^"\']*)?'), 'smriti_nav_config.js?v=2.0.4'),
]

for www_dir in paths:
    if not os.path.exists(www_dir):
        print(f"Path does not exist: {www_dir}")
        continue
    updated = []
    for fn in os.listdir(www_dir):
        if not fn.endswith('.html'):
            continue
        fpath = os.path.join(www_dir, fn)
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = content
            for pattern, replacement in patterns:
                new_content = pattern.sub(replacement, new_content)
            if new_content != content:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated.append(fn)
        except Exception as e:
            print(f'ERROR {fn}: {e}')
    print(f'Updated {len(updated)} files in {www_dir}: {", ".join(updated)}')
