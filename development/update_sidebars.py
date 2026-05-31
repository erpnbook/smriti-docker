# -*- coding: utf-8 -*-
import os

www_dir = "d:/Smriti_Retail_OS/apps/smriti_retail_os/smriti_retail_os/www"
files = [
    "desk.html", "billing.html", "shift.html", "inventory.html",
    "purchase.html", "barcode.html", "products.html", "customers.html",
    "suppliers.html", "sales_invoices.html"
]

target_inactive = """            <a class="sidebar-item" href="/products">
                <span class="emoji">🛍️</span>
                <span>Products Catalog</span>
                <button class="popout-btn" title="Open in Popout Window" onclick="openPopout(event, '/products')">
                    <span class="material-symbols-outlined">open_in_new</span>
                </button>
            </a>"""

replacement_inactive = """            <a class="sidebar-item" href="/products">
                <span class="emoji">🛍️</span>
                <span>Products Catalog</span>
                <button class="popout-btn" title="Open in Popout Window" onclick="openPopout(event, '/products')">
                    <span class="material-symbols-outlined">open_in_new</span>
                </button>
            </a>
            <a class="sidebar-item" href="/item_master">
                <span class="emoji">📋</span>
                <span>Item Master Import</span>
                <button class="popout-btn" title="Open in Popout Window" onclick="openPopout(event, '/item_master')">
                    <span class="material-symbols-outlined">open_in_new</span>
                </button>
            </a>"""

target_active = """            <a class="sidebar-item active" href="/products">
                <span class="emoji">🛍️</span>
                <span>Products Catalog</span>
                <button class="popout-btn" title="Open in Popout Window" onclick="openPopout(event, '/products')">
                    <span class="material-symbols-outlined">open_in_new</span>
                </button>
            </a>"""

replacement_active = """            <a class="sidebar-item active" href="/products">
                <span class="emoji">🛍️</span>
                <span>Products Catalog</span>
                <button class="popout-btn" title="Open in Popout Window" onclick="openPopout(event, '/products')">
                    <span class="material-symbols-outlined">open_in_new</span>
                </button>
            </a>
            <a class="sidebar-item" href="/item_master">
                <span class="emoji">📋</span>
                <span>Item Master Import</span>
                <button class="popout-btn" title="Open in Popout Window" onclick="openPopout(event, '/item_master')">
                    <span class="material-symbols-outlined">open_in_new</span>
                </button>
            </a>"""

# Normalize string endings to handle both LF and CRLF
def normalize(s):
    return s.replace('\r\n', '\n').strip()

for f_name in files:
    path = os.path.join(www_dir, f_name)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    normalized_content = content.replace('\r\n', '\n')
    
    if normalize(target_inactive) in normalized_content:
        normalized_content = normalized_content.replace(normalize(target_inactive), normalize(replacement_inactive))
        print(f"Updated inactive sidebar in {f_name}")
    elif normalize(target_active) in normalized_content:
        normalized_content = normalized_content.replace(normalize(target_active), normalize(replacement_active))
        print(f"Updated active sidebar in {f_name}")
    else:
        print(f"WARNING: Target not found in {f_name}!")
        
    # Write back preserving or using standard endings
    with open(path, "w", encoding="utf-8") as f:
        f.write(normalized_content)
