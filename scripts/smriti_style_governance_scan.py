#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SMRITI UI Governance Scanner
Scans the codebase for UI Engine token violations as defined in:
docs/architecture/ui/SMRITI_UI_CONFIGURATION_ENGINE_V1.md §10
"""

import os
import re
import sys
import json

# Target Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WWW_DIR = os.path.join(BASE_DIR, "apps", "smriti_retail_os", "smriti_retail_os", "www")
CSS_DIR = os.path.join(BASE_DIR, "apps", "smriti_retail_os", "smriti_retail_os", "public", "css")
JS_DIR = os.path.join(BASE_DIR, "apps", "smriti_retail_os", "smriti_retail_os", "public", "js")

# Excluded files/folders
EXCLUDE_FILES = [
    "smriti_tokens.css",      # This is the token definition file itself
    "smriti_ui_resolver.js",   # Resolver internal code
    "smriti_theme_manager.js", # Theme manager runtime contract
    "__init__.py"
]

# Regex Patterns
HEX_COLOR_PATTERN = re.compile(r"#[0-9a-fA-F]{3,6}")
RGB_RGBA_HSL_PATTERN = re.compile(r"\b(rgb|rgba|hsl|hsla)\([^)]*\)")
FONT_SIZE_PATTERN = re.compile(r"font-size\s*:\s*([^;!]+)")
BORDER_RADIUS_PATTERN = re.compile(r"border-radius\s*:\s*([^;!]+)")
BOX_SHADOW_PATTERN = re.compile(r"box-shadow\s*:\s*([^;!]+)")
MARGIN_PADDING_PATTERN = re.compile(r"\b(margin|padding|gap)(-top|-bottom|-left|-right)?\s*:\s*([^;!]+)")
INLINE_STYLE_ATTR_PATTERN = re.compile(r'\bstyle\s*=\s*"([^"]*)"')

def check_literal_value(val):
    """Returns True if the value contains a hardcoded literal (px, rem, hex, etc.) and doesn't use var(--smriti)"""
    val = val.strip().lower()
    if not val:
        return False
    # If it is purely a var() reference or inherit/initial/transparent/none/auto, it's not a violation
    if val in ["inherit", "initial", "unset", "transparent", "none", "auto", "0"]:
        return False
    
    # If it contains var(--smriti-), it's correct
    if "var(--smriti-" in val:
        return False
        
    # Check if it has px, rem, em, % (other than 100%), or color hex
    if "px" in val or "rem" in val or "em" in val or "#" in val or "rgb" in val or "rgba" in val or "hsl" in val:
        return True
    
    # If it's a raw number (like box-shadow or padding/margin values)
    if re.search(r'\b\d+(?!\%)', val):
        return True
        
    return False

def scan_html_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    violations = {
        "inline_styles": 0,
        "hex_colors": 0,
        "rgba_colors": 0,
        "font_sizes": 0,
        "border_radius": 0,
        "box_shadows": 0,
        "spacing": 0
    }
    
    # 1. Check style="" attributes
    inline_styles = INLINE_STYLE_ATTR_PATTERN.findall(content)
    violations["inline_styles"] = len(inline_styles)
    
    # Audit inline styles for specific violations
    for style_str in inline_styles:
        # Check colors
        if HEX_COLOR_PATTERN.search(style_str):
            violations["hex_colors"] += len(HEX_COLOR_PATTERN.findall(style_str))
        if RGB_RGBA_HSL_PATTERN.search(style_str):
            violations["rgba_colors"] += len(RGB_RGBA_HSL_PATTERN.findall(style_str))
        # Check other properties in inline styles
        parts = style_str.split(";")
        for part in parts:
            if ":" not in part:
                continue
            prop, val = part.split(":", 1)
            prop = prop.strip().lower()
            val = val.strip().lower()
            if "font-size" in prop and check_literal_value(val):
                violations["font_sizes"] += 1
            elif "border-radius" in prop and check_literal_value(val):
                violations["border_radius"] += 1
            elif "box-shadow" in prop and check_literal_value(val):
                violations["box_shadows"] += 1
            elif any(p in prop for p in ["margin", "padding", "gap"]) and check_literal_value(val):
                violations["spacing"] += 1

    # 2. Check <style> blocks
    style_blocks = re.findall(r"<style[^>]*>(.*?)</style>", content, re.DOTALL)
    for block in style_blocks:
        # Scan hex colors not inside var()
        hexes = HEX_COLOR_PATTERN.findall(block)
        violations["hex_colors"] += len([h for h in hexes if f"var(--smriti-" not in block[max(0, block.find(h)-30):block.find(h)+30]])
        
        # Scan rgb/rgba
        rgbs = RGB_RGBA_HSL_PATTERN.findall(block)
        violations["rgba_colors"] += len(rgbs)
        
        # Scan font-size
        for fs in FONT_SIZE_PATTERN.findall(block):
            if check_literal_value(fs):
                violations["font_sizes"] += 1
                
        # Scan border-radius
        for br in BORDER_RADIUS_PATTERN.findall(block):
            if check_literal_value(br):
                violations["border_radius"] += 1
                
        # Scan box-shadow
        for bs in BOX_SHADOW_PATTERN.findall(block):
            if check_literal_value(bs):
                violations["box_shadows"] += 1
                
        # Scan margin/padding/gap
        for mp in MARGIN_PADDING_PATTERN.findall(block):
            val = mp[2]
            if check_literal_value(val):
                violations["spacing"] += 1

    return violations

def scan_css_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    violations = {
        "inline_styles": 0, # N/A for CSS files
        "hex_colors": 0,
        "rgba_colors": 0,
        "font_sizes": 0,
        "border_radius": 0,
        "box_shadows": 0,
        "spacing": 0
    }
    
    # Hex colors
    violations["hex_colors"] = len(HEX_COLOR_PATTERN.findall(content))
    
    # rgb/rgba/hsl
    violations["rgba_colors"] = len(RGB_RGBA_HSL_PATTERN.findall(content))
    
    # Font sizes
    for fs in FONT_SIZE_PATTERN.findall(content):
        if check_literal_value(fs):
            violations["font_sizes"] += 1
            
    # Border radius
    for br in BORDER_RADIUS_PATTERN.findall(content):
        if check_literal_value(br):
            violations["border_radius"] += 1
            
    # Box shadows
    for bs in BOX_SHADOW_PATTERN.findall(content):
        if check_literal_value(bs):
            violations["box_shadows"] += 1
            
    # Spacing
    for mp in MARGIN_PADDING_PATTERN.findall(content):
        val = mp[2]
        if check_literal_value(val):
            violations["spacing"] += 1
            
    return violations

def scan_js_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    violations = {
        "inline_styles": 0,
        "hex_colors": 0,
        "rgba_colors": 0,
        "font_sizes": 0,
        "border_radius": 0,
        "box_shadows": 0,
        "spacing": 0
    }
    
    # Look for hex color literals as JS strings e.g. '#6366f1' or "#fff"
    # Match strings starting with # inside quotes
    js_hex_pattern = re.compile(r'[\'"`]#[0-9a-fA-F]{3,6}[\'"`]')
    violations["hex_colors"] = len(js_hex_pattern.findall(content))
    
    # Look for rgba/rgb literals in strings
    js_rgb_pattern = re.compile(r'[\'"`](rgba?|hsla?)\([^)]*\)[\'"`]')
    violations["rgba_colors"] = len(js_rgb_pattern.findall(content))
    
    # Look for .style.fontSize or .style.margin etc. hardcoded strings
    style_assignments = re.findall(r'\.style\.([a-zA-Z]+)\s*=\s*([\'"`][^\'"`]+[\'"`])', content)
    for prop, val_str in style_assignments:
        val = val_str[1:-1].strip() # strip quotes
        prop_lower = prop.lower()
        if prop_lower == "fontsize" and check_literal_value(val):
            violations["font_sizes"] += 1
        elif prop_lower == "borderradius" and check_literal_value(val):
            violations["border_radius"] += 1
        elif prop_lower == "boxshadow" and check_literal_value(val):
            violations["box_shadows"] += 1
        elif any(p in prop_lower for p in ["margin", "padding", "gap", "top", "left", "right", "bottom"]) and check_literal_value(val):
            violations["spacing"] += 1
            
    return violations

def run_scan():
    report = {
        "html_files": {},
        "css_files": {},
        "js_files": {}
    }
    
    # 1. Scan HTML files in WWW_DIR
    if os.path.exists(WWW_DIR):
        for file_name in sorted(os.listdir(WWW_DIR)):
            if file_name.endswith(".html") and file_name not in EXCLUDE_FILES:
                file_path = os.path.join(WWW_DIR, file_name)
                report["html_files"][file_name] = scan_html_file(file_path)
                
    # 2. Scan CSS files in CSS_DIR
    if os.path.exists(CSS_DIR):
        for file_name in sorted(os.listdir(CSS_DIR)):
            if file_name.endswith(".css") and file_name not in EXCLUDE_FILES:
                file_path = os.path.join(CSS_DIR, file_name)
                report["css_files"][file_name] = scan_css_file(file_path)
                
    # 3. Scan JS files in JS_DIR
    if os.path.exists(JS_DIR):
        for file_name in sorted(os.listdir(JS_DIR)):
            if file_name.endswith(".js") and file_name not in EXCLUDE_FILES:
                file_path = os.path.join(JS_DIR, file_name)
                report["js_files"][file_name] = scan_js_file(file_path)
                
    return report

if __name__ == "__main__":
    scan_report = run_scan()
    print(json.dumps(scan_report, indent=2))
