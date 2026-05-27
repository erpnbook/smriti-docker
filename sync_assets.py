import os
import shutil
import frappe

def sync_assets():
    print("[SMRITI] Starting hard-sync of assets (No Symlinks)...")
    
    frappe.init(site="frontend")
    frappe.connect()

    bench_path = "/home/frappe/frappe-bench"
    assets_path = os.path.join(bench_path, "sites", "assets")
    
    # Standard apps to sync
    apps = ["frappe", "erpnext", "india_compliance", "smriti_retail_os"]
    
    # 1. Clean up sites/assets
    if os.path.islink(assets_path):
        os.unlink(assets_path)
    elif os.path.isdir(assets_path):
        shutil.rmtree(assets_path)
    
    os.makedirs(assets_path, exist_ok=True)

    # 2. Copy files instead of linking
    for app in apps:
        app_public_path = os.path.join(bench_path, "apps", app, app, "public")
        if not os.path.exists(app_public_path):
            continue
            
        target_path = os.path.join(assets_path, app)
        print(f"  - Copying {app} assets...")
        shutil.copytree(app_public_path, target_path, dirs_exist_ok=True)
        
    print("[SMRITI] Asset sync complete. Real files are now in sites/assets.")

if __name__ == "__main__":
    sync_assets()
