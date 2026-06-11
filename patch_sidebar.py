import re

def patch_sidebar():
    path = "apps/smriti_retail_os/smriti_retail_os/public/js/smriti_sidebar_standalone.js"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    old_func_start = "SMRITI.renderFlexibleSidebar = function(activePageId) {"
    
    new_func_start = """SMRITI.renderFlexibleSidebar = async function(activePageId) {
    const target = document.getElementById("smriti-sidebar-target");
    if (!target) return;

    let business_type = "Footwear";
    try {
        if (window.frappe && frappe.boot && frappe.boot.smriti_business_type) {
            business_type = frappe.boot.smriti_business_type;
        } else {
            const res = await fetch("/api/method/smriti_retail_os.company_api.get_business_type");
            const data = await res.json();
            if (data.message) business_type = data.message;
        }
    } catch(e) {}

    const filteredSchema = JSON.parse(JSON.stringify(SMRITI.sidebarSchema));
    filteredSchema.forEach(cat => {
        if (cat.items) {
            cat.items = cat.items.filter(item => {
                if (business_type === "Footwear") {
                    if (['psa', 'psv_opening_balance', 'sales_upload'].includes(item.id)) return false;
                } else {
                    // FMCG / Others
                    if (['sizewise_item', 'sizewise_invoice'].includes(item.id)) return false;
                }
                return true;
            });
        }
    });"""

    content = content.replace(old_func_start + '\n    const target = document.getElementById("smriti-sidebar-target");\n    if (!target) return;', new_func_start)
    
    # Replace SMRITI.sidebarSchema.forEach with filteredSchema.forEach
    content = content.replace("SMRITI.sidebarSchema.forEach(block => {", "filteredSchema.forEach(block => {")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Sidebar JS patched")

if __name__ == "__main__":
    patch_sidebar()
