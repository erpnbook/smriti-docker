import re

def patch():
    path = "apps/smriti_retail_os/smriti_retail_os/www/configure.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add HTML field
    html_field = """<div class="mb-8">
                  <label class="lbl">Business Type (Industry)</label>
                  <select id="cfg-custom-business-type" class="inp">
                    <option value="Footwear">Footwear</option>
                    <option value="FMCG">FMCG</option>
                    <option value="Garments">Garments</option>
                    <option value="Pharma">Pharma</option>
                    <option value="Cosmetics">Cosmetics</option>
                    <option value="General Retail">General Retail</option>
                  </select>
                </div>
                <div class="mb-8">
                  <label class="lbl">Store Trade Name (Receipt Title)</label>"""
    content = content.replace('<div class="mb-8">\n                  <label class="lbl">Store Trade Name (Receipt Title)</label>', html_field)

    # 2. Add loading logic
    content = content.replace("document.getElementById('cfg-custom-store-type').value = settings.custom_smriti_store_type || '';",
                              "document.getElementById('cfg-custom-store-type').value = settings.custom_smriti_store_type || '';\n      document.getElementById('cfg-custom-business-type').value = settings.custom_business_type || 'Footwear';")

    # 3. Add saving logic
    content = content.replace("const storeType      = document.getElementById('cfg-custom-store-type').value;",
                              "const storeType      = document.getElementById('cfg-custom-store-type').value;\n    const businessType   = document.getElementById('cfg-custom-business-type').value;")
    
    content = content.replace("custom_smriti_store_type: storeType,",
                              "custom_smriti_store_type: storeType,\n      custom_business_type: businessType,")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("configure.html patched")

if __name__ == "__main__":
    patch()