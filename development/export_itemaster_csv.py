# -*- coding: utf-8 -*-
import frappe
import csv
import os

TEMPLATE_HEADERS = [
    "BARCODE NO", "PURCHASE CLASS", "DEPARTMENT", "MERCHANDISE CATEGORY",
    "Category", "Sub category", "ITEM DESCRIPTION", "HEELS", "GENDER",
    "UPPER MATERIAL", "OUTSOLE", "VENDOR CODE", "PRODUCT STYLE CODE",
    "BRAND NAME", "COLOR", "SIZE", "COST PRICE", "PLANNED MRP",
    "PRODUCT TAX", "IMAGE LINK", "HSN CODE", "Product Tax Group"
]

def run():
    print("Exporting items to CSV...")
    
    # We query for all variants of the articles we imported
    target_articles = ["20016", "1455", "20001", "10019", "2097"]
    
    # Find all variants
    variants = frappe.get_all(
        "Item",
        filters={"variant_of": ["in", target_articles]},
        fields=["name", "item_name", "variant_of", "item_group", "custom_mrp", "valuation_rate", "gst_hsn_code"]
    )
    
    csv_rows = []
    
    for v in variants:
        # Get color and size from attributes
        color = frappe.db.get_value("Item Variant Attribute", {"parent": v.name, "attribute": "Color"}, "attribute_value") or ""
        size = frappe.db.get_value("Item Variant Attribute", {"parent": v.name, "attribute": "Size"}, "attribute_value") or ""
        
        # Get barcode
        barcode = frappe.db.get_value("Item Barcode", {"parent": v.name}, "barcode") or ""
        
        # Get template details
        template = frappe.get_doc("Item", v.variant_of)
        
        row = {
            "BARCODE NO": barcode,
            "PURCHASE CLASS": template.custom_purchase_class or "",
            "DEPARTMENT": v.item_group or "Products",
            "MERCHANDISE CATEGORY": template.custom_merchandise_category or "",
            "Category": template.custom_merchandise_category or "",
            "Sub category": template.custom_sub_category or "",
            "ITEM DESCRIPTION": template.item_name or "",
            "HEELS": template.custom_heel_type or "",
            "GENDER": template.custom_gender or "",
            "UPPER MATERIAL": template.custom_upper_material or "",
            "OUTSOLE": template.custom_outsole or "",
            "VENDOR CODE": "",
            "PRODUCT STYLE CODE": v.variant_of,
            "BRAND NAME": template.brand or "SMRITI",
            "COLOR": color,
            "SIZE": size,
            "COST PRICE": v.valuation_rate or 0.0,
            "PLANNED MRP": v.custom_mrp or 0.0,
            "PRODUCT TAX": template.custom_gst_percentage or "18",
            "IMAGE LINK": template.image or "",
            "HSN CODE": v.gst_hsn_code or "64041990",
            "Product Tax Group": ""
        }
        csv_rows.append(row)
        
    output_path = "/home/frappe/frappe-bench/smriti_items_export.csv"
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=TEMPLATE_HEADERS)
        writer.writeheader()
        for row in csv_rows:
            writer.writerow(row)
            
    print(f"Successfully exported {len(csv_rows)} variants to {output_path}")
