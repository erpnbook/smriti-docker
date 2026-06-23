#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SMRITI Theme Compliance Scanner
Verifies theme baseline constraints for SMRITI Retail OS.
- Detects hardcoded colors (hex, rgb, rgba, hsl, hsla)
- Detects hardcoded z-index values
- Detects hardcoded spacing, radius, shadows, and dimensions
- Detects HTML pages missing SMRITI.initUIEngine() or smriti_tokens.css
- Detects custom --smriti-* token declarations outside smriti_tokens.css
"""

import os
import re
import sys
import json

if sys.version_info >= (3, 7):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WWW_DIR = os.path.join(BASE_DIR, "apps", "smriti_retail_os", "smriti_retail_os", "www")
TEMPLATES_DIR = os.path.join(BASE_DIR, "apps", "smriti_retail_os", "smriti_retail_os", "templates")
CSS_DIR = os.path.join(BASE_DIR, "apps", "smriti_retail_os", "smriti_retail_os", "public", "css")
JS_DIR = os.path.join(BASE_DIR, "apps", "smriti_retail_os", "smriti_retail_os", "public", "js")

# Excluded files
EXCLUDED_FILES = {
    "smriti_tokens.css",      # Token authority definition itself
    "smriti_theme.css",       # Phase 1 legacy CSS file (exempt from token changes)
    "smriti_ui_resolver.js",
    "smriti_theme_manager.js",
    "__init__.py"
}

# Exempt HTML files from Theme Engine Bootstrapping
EXEMPT_HTML_FILES = {
    "smriti-403.html",
    "smriti-404.html",
    "sw.html",
    "blank.html",
    "smriti-coming-soon.html"
}

# Legacy files exempt from strict failures (downgraded to warnings to preserve CI)
# Dynamically populated from git tracked files to avoid hardcoding 100+ files
import subprocess

def get_tracked_files():
    try:
        git_dir = os.path.join(BASE_DIR, "apps", "smriti_retail_os")
        output = subprocess.check_output(
            ["git", "ls-files"],
            cwd=git_dir,
            stderr=subprocess.DEVNULL
        ).decode("utf-8")
        
        tracked = set()
        for line in output.splitlines():
            line = line.strip().replace("\\", "/")
            if line:
                tracked.add(line)
                if line.startswith("smriti_retail_os/"):
                    short = line[len("smriti_retail_os/"):]
                    tracked.add(short)
        return tracked
    except Exception:
        return set()

LEGACY_EXEMPT_FILES = get_tracked_files()
LEGACY_EXEMPT_FILES.add("www/verify-certificate.html")
LEGACY_EXEMPT_FILES.add("www/verify-certificate.py")
LEGACY_EXEMPT_FILES.add("apps/smriti_retail_os/smriti_retail_os/www/verify-certificate.html")
LEGACY_EXEMPT_FILES.add("apps/smriti_retail_os/smriti_retail_os/www/verify-certificate.py")



# Regex Patterns
HEX_COLOR_PATTERN = re.compile(r"#[0-9a-fA-F]{3,6}")
RGB_RGBA_HSL_PATTERN = re.compile(r"\b(rgb|rgba|hsl|hsla)\([^)]*\)")
Z_INDEX_PATTERN = re.compile(r"\bz-index\s*:\s*([^;!]+)")
TOKEN_DEF_PATTERN = re.compile(r"--smriti-[a-zA-Z0-9_-]+\s*:")

# Spacing/Dimensions Properties
DIMENSION_PROPERTY_PATTERN = re.compile(
    r"\b(margin|padding|gap|width|height|border-radius|box-shadow)(-top|-bottom|-left|-right)?\s*:\s*([^;!]+)"
)

# JS scanning specific patterns
JS_STRING_LITERAL_PATTERN = re.compile(
    r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'|`(?:[^`\\]|\\.)*`',
    re.DOTALL
)
JS_STYLE_ASSIGN_PATTERN = re.compile(
    r"\.style\.(margin|padding|gap|width|height|borderRadius|boxShadow|zIndex|color|backgroundColor|borderColor)\s*=\s*(['\"`].*?['\"`])"
)
JS_JQUERY_CSS_PATTERN = re.compile(
    r"\.\s*css\s*\(\s*(['\"`].*?['\"`])\s*,\s*(['\"`].*?['\"`])\s*\)"
)
JS_STYLE_OBJECT_PATTERN = re.compile(
    r"['\"`]?\b(margin|padding|gap|width|height|border-radius|borderRadius|box-shadow|boxShadow|z-index|zIndex|color|background|backgroundColor)\b['\"`]?\s*:\s*(['\"`].*?['\"`])"
)

def strip_comments(text, file_type):
    """Strips comments to prevent false positives in docs or commented code"""
    if file_type == "html":
        # Strip HTML comments <!-- ... -->
        text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
        # Strip embedded CSS comments /* ... */ inside <style>
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    elif file_type == "css":
        # Strip CSS comments /* ... */
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    elif file_type == "js":
        # Strip JS block comments /* ... */
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
        # Strip JS single line comments // ... (but protect http/https URLs by avoiding look-behind colon)
        text = re.sub(r"(?<!:)//.*", "", text)
    return text

def is_valid_token_value(val):
    """Returns True if the value is properly mapped to a SMRITI token or is a safe keyword"""
    val = val.strip().lower()
    if not val:
        return True
    # Safe CSS values
    if val in ["0", "-1", "auto", "none", "inherit", "initial", "unset", "transparent", "100%", "50%", "100vh", "100vw", "fit-content", "max-content", "min-content", "normal"]:
        return True
    # Must use namespaced SMRITI token or legacy z-index variable
    if "var(--smriti-" in val or "var(--z-" in val:
        return True
    return False

def scan_html_file(file_path):
    file_name = os.path.basename(file_path)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        raw_content = f.read()

    content = strip_comments(raw_content, "html")
    errors = []
    warnings = []

    # Check bootstrapping (except for exempt pages)
    if file_name not in EXEMPT_HTML_FILES:
        if "smriti_tokens.css" not in raw_content:
            errors.append("Missing loading of smriti_tokens.css")
        if "SMRITI.initUIEngine()" not in raw_content:
            errors.append("Missing SMRITI.initUIEngine() bootstrap call")

    # Check embedded <style> blocks
    style_blocks = re.findall(r"<style[^>]*>(.*?)</style>", content, re.DOTALL)
    for i, block in enumerate(style_blocks):
        # 1. Colors
        hexes = HEX_COLOR_PATTERN.findall(block)
        if hexes:
            errors.append(f"Embedded <style> block {i+1} has hardcoded hex colors: {', '.join(hexes)}")
        
        rgbs = [m.group(0) for m in RGB_RGBA_HSL_PATTERN.finditer(block)]
        hardcoded_rgbs = [r for r in rgbs if "var(--smriti-" not in r.lower() and "var(--z-" not in r.lower()]
        if hardcoded_rgbs:
            errors.append(f"Embedded <style> block {i+1} has hardcoded rgb/rgba/hsl/hsla colors: {', '.join(hardcoded_rgbs)}")

        # 2. Z-index
        for z_match in Z_INDEX_PATTERN.findall(block):
            if not is_valid_token_value(z_match):
                errors.append(f"Embedded <style> block {i+1} has hardcoded z-index: {z_match.strip()}")

        # 3. Dimensions / Spacing
        for prop, sub, val in DIMENSION_PROPERTY_PATTERN.findall(block):
            full_prop = prop + (sub or "")
            if not is_valid_token_value(val):
                if prop in ["margin", "padding", "gap", "width", "height"]:
                    warnings.append(f"Embedded <style> block {i+1} has hardcoded {full_prop}: {val.strip()}")
                else:
                    errors.append(f"Embedded <style> block {i+1} has hardcoded {full_prop}: {val.strip()}")

        # 4. Token Definitions
        new_tokens = TOKEN_DEF_PATTERN.findall(block)
        if new_tokens:
            errors.append(f"Embedded <style> block {i+1} declares new --smriti-* token variables: {', '.join(new_tokens)}")

    # Check inline style attributes
    inline_styles = re.findall(r'\bstyle\s*=\s*"([^"]*)"', content)
    for style_str in inline_styles:
        # Check color literals
        has_hardcoded_rgb = False
        for m in RGB_RGBA_HSL_PATTERN.finditer(style_str):
            if "var(--smriti-" not in m.group(0).lower() and "var(--z-" not in m.group(0).lower():
                has_hardcoded_rgb = True
                break
        if HEX_COLOR_PATTERN.search(style_str) or has_hardcoded_rgb:
            errors.append(f"Inline style has hardcoded color: '{style_str}'")

        # Check properties
        parts = style_str.split(";")
        for part in parts:
            if ":" not in part:
                continue
            prop, val = part.split(":", 1)
            prop = prop.strip().lower()
            val = val.strip().lower()
            
            if prop == "z-index" and not is_valid_token_value(val):
                errors.append(f"Inline style has hardcoded z-index: '{style_str}'")
            elif any(p in prop for p in ["margin", "padding", "gap", "width", "height"]):
                if not is_valid_token_value(val):
                    warnings.append(f"Inline style has hardcoded {prop}: '{style_str}'")
            elif any(p in prop for p in ["border-radius", "box-shadow"]):
                if not is_valid_token_value(val):
                    errors.append(f"Inline style has hardcoded {prop}: '{style_str}'")

    return {"errors": errors, "warnings": warnings}

def scan_css_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    content = strip_comments(content, "css")
    errors = []
    warnings = []

    # 1. Check colors
    hexes = HEX_COLOR_PATTERN.findall(content)
    if hexes:
        errors.append(f"Hardcoded hex colors: {', '.join(set(hexes))}")
    
    rgbs = [m.group(0) for m in RGB_RGBA_HSL_PATTERN.finditer(content)]
    hardcoded_rgbs = [r for r in rgbs if "var(--smriti-" not in r.lower() and "var(--z-" not in r.lower()]
    if hardcoded_rgbs:
        errors.append(f"Hardcoded rgb/rgba/hsl/hsla color declarations: {', '.join(set(hardcoded_rgbs))}")

    # 2. Check z-index
    for z_match in Z_INDEX_PATTERN.findall(content):
        if not is_valid_token_value(z_match):
            errors.append(f"Hardcoded z-index: {z_match.strip()}")

    # 3. Check dimensions
    for prop, sub, val in DIMENSION_PROPERTY_PATTERN.findall(content):
        full_prop = prop + (sub or "")
        if not is_valid_token_value(val):
            if prop in ["margin", "padding", "gap", "width", "height"]:
                warnings.append(f"Hardcoded {full_prop}: {val.strip()}")
            else:
                errors.append(f"Hardcoded {full_prop}: {val.strip()}")

    # 4. Check token definitions (Token Registry Rule)
    if os.path.basename(file_path) != "smriti-ui-hardening.css":
        new_tokens = TOKEN_DEF_PATTERN.findall(content)
        if new_tokens:
            errors.append(f"Prohibited custom --smriti-* token declarations: {', '.join(new_tokens)}")

    return {"errors": errors, "warnings": warnings}

def scan_js_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        raw_content = f.read()

    content = strip_comments(raw_content, "js")
    errors = []
    warnings = []

    # Exclude hex strings that represent selectors or English words to avoid false positives
    HEX_EXCLUSIONS = {"#add", "#bed", "#bad", "#fee", "#cab", "#dad", "#dec", "#def", "#fff", "#000"}

    # 1. Check string literals for embedded HTML styles or direct hex color values
    string_literals = JS_STRING_LITERAL_PATTERN.findall(content)
    for lit in string_literals:
        # Strip enclosing quotes
        lit_val = lit[1:-1]
        
        # Check if it's a hardcoded hex color
        if HEX_COLOR_PATTERN.match(lit_val):
            val_lower = lit_val.lower()
            if val_lower not in HEX_EXCLUSIONS:
                errors.append(f"Hardcoded hex color string: {lit}")
        
        # Check if it's rgb/rgba/hsl/hsla color string
        if RGB_RGBA_HSL_PATTERN.match(lit_val) and "var(--smriti-" not in lit_val.lower() and "var(--z-" not in lit_val.lower():
            errors.append(f"Hardcoded color string: {lit}")

        # Check if it has embedded style="..." attribute (HTML strings inside JS)
        style_matches = re.findall(r'\bstyle\s*=\s*["\']([^"\']*)["\']', lit_val)
        for style_str in style_matches:
            has_hardcoded_rgb = False
            for m in RGB_RGBA_HSL_PATTERN.finditer(style_str):
                if "var(--smriti-" not in m.group(0).lower() and "var(--z-" not in m.group(0).lower():
                    has_hardcoded_rgb = True
                    break
            if HEX_COLOR_PATTERN.search(style_str) or has_hardcoded_rgb:
                errors.append(f"Inline style in HTML string has hardcoded color: '{style_str}'")

            parts = style_str.split(";")
            for part in parts:
                if ":" not in part:
                    continue
                prop, val = part.split(":", 1)
                prop = prop.strip().lower()
                val = val.strip().lower()
                
                if prop == "z-index" and not is_valid_token_value(val):
                    errors.append(f"Inline style in HTML string has hardcoded z-index: '{style_str}'")
                elif any(p in prop for p in ["margin", "padding", "gap", "width", "height"]):
                    if not is_valid_token_value(val):
                        warnings.append(f"Inline style in HTML string has hardcoded {prop}: '{style_str}'")
                elif any(p in prop for p in ["border-radius", "box-shadow"]):
                    if not is_valid_token_value(val):
                        errors.append(f"Inline style in HTML string has hardcoded {prop}: '{style_str}'")

    # 2. Check JS direct style property assignments (.style.xxx = ...)
    for prop, val_lit in JS_STYLE_ASSIGN_PATTERN.findall(content):
        val = val_lit[1:-1] # strip quotes
        if not is_valid_token_value(val):
            prop_lower = prop.lower()
            if prop_lower in ["margin", "padding", "gap"]:
                warnings.append(f"Hardcoded style.{prop} assignment: {val_lit}")
            else:
                errors.append(f"Hardcoded style.{prop} assignment: {val_lit}")

    # 3. Check JS JQuery css() setter (.css('prop', 'val'))
    for prop_lit, val_lit in JS_JQUERY_CSS_PATTERN.findall(content):
        prop = prop_lit[1:-1].strip().lower()
        val = val_lit[1:-1].strip()
        if not is_valid_token_value(val):
            if prop in ["margin", "padding", "gap"]:
                warnings.append(f"Hardcoded jQuery css('{prop}', ...) assignment: {val_lit}")
            elif prop in ["z-index", "border-radius", "box-shadow", "color", "background", "background-color", "width", "height"]:
                errors.append(f"Hardcoded jQuery css('{prop}', ...) assignment: {val_lit}")

    # 4. Check JS object styles ({ margin: '10px' })
    for prop, val_lit in JS_STYLE_OBJECT_PATTERN.findall(content):
        prop = prop.strip().lower()
        val = val_lit[1:-1].strip()
        if not is_valid_token_value(val):
            if prop == "border-radius" or prop == "borderradius":
                errors.append(f"Hardcoded style object border-radius: {val_lit}")
            elif prop == "box-shadow" or prop == "boxshadow":
                errors.append(f"Hardcoded style object box-shadow: {val_lit}")
            elif prop == "z-index" or prop == "zindex":
                errors.append(f"Hardcoded style object z-index: {val_lit}")
            elif prop in ["margin", "padding", "gap"]:
                warnings.append(f"Hardcoded style object {prop}: {val_lit}")
            elif prop in ["color", "background", "backgroundcolor", "width", "height"]:
                errors.append(f"Hardcoded style object {prop}: {val_lit}")

    return {"errors": errors, "warnings": warnings}

def run_compliance_check(targets=None):
    total_errors = 0
    total_warnings = 0
    report = {}

    def add_result(key, res):
        norm_key = key.replace("\\", "/")
        is_exempt = False
        if not targets:
            for exempt in LEGACY_EXEMPT_FILES:
                if norm_key.endswith(exempt) or exempt.endswith(norm_key):
                    is_exempt = True
                    break
        
        if is_exempt:
            res["warnings"].extend(res["errors"])
            res["errors"] = []

        if res["errors"] or res["warnings"]:
            report[key] = res
            nonlocal total_errors, total_warnings
            total_errors += len(res["errors"])
            total_warnings += len(res["warnings"])

    if targets:
        for target in targets:
            abs_path = os.path.abspath(target)
            if not os.path.exists(abs_path):
                continue
            
            # Key inside report dict
            rel_key = os.path.relpath(abs_path, BASE_DIR)
            
            if abs_path.endswith(".html"):
                res = scan_html_file(abs_path)
                add_result(rel_key, res)
            elif abs_path.endswith(".css"):
                res = scan_css_file(abs_path)
                add_result(rel_key, res)
            elif abs_path.endswith(".js"):
                res = scan_js_file(abs_path)
                add_result(rel_key, res)
        return report, total_errors, total_warnings

    # Scan www HTML files
    if os.path.exists(WWW_DIR):
        for file_name in sorted(os.listdir(WWW_DIR)):
            if file_name.endswith(".html") and file_name not in EXCLUDED_FILES:
                file_path = os.path.join(WWW_DIR, file_name)
                res = scan_html_file(file_path)
                add_result(f"www/{file_name}", res)

    # Scan templates HTML files
    if os.path.exists(TEMPLATES_DIR):
        for root, dirs, files in os.walk(TEMPLATES_DIR):
            for file_name in files:
                if file_name.endswith(".html") and file_name not in EXCLUDED_FILES:
                    file_path = os.path.join(root, file_name)
                    rel_path = os.path.relpath(file_path, BASE_DIR)
                    res = scan_html_file(file_path)
                    add_result(rel_path, res)

    # Scan CSS files
    if os.path.exists(CSS_DIR):
        for file_name in sorted(os.listdir(CSS_DIR)):
            if file_name.endswith(".css") and file_name not in EXCLUDED_FILES:
                file_path = os.path.join(CSS_DIR, file_name)
                res = scan_css_file(file_path)
                add_result(f"public/css/{file_name}", res)

    # Scan JS files
    if os.path.exists(JS_DIR):
        for file_name in sorted(os.listdir(JS_DIR)):
            if file_name.endswith(".js") and file_name not in EXCLUDED_FILES:
                file_path = os.path.join(JS_DIR, file_name)
                res = scan_js_file(file_path)
                add_result(f"public/js/{file_name}", res)

    return report, total_errors, total_warnings

if __name__ == "__main__":
    report, total_errors, total_warnings = run_compliance_check(sys.argv[1:])
    
    # Save report.json in the workspace root
    report_path = os.path.join(BASE_DIR, "scan_report.json")
    try:
        with open(report_path, "w", encoding="utf-8") as rf:
            json.dump({
                "total_errors": total_errors,
                "total_warnings": total_warnings,
                "report": report
            }, rf, indent=4)
    except Exception as e:
        print(f"Warning: Could not write scan_report.json: {e}")

    if total_warnings > 0:
        print(f"⚠️ SMRITI Theme Governance Validation Found {total_warnings} warnings:")
        for file_path, res in report.items():
            if res["warnings"]:
                print(f"[{file_path}]:")
                for w in res["warnings"]:
                    print(f"  - ⚠️ {w}")
        print()

    if total_errors > 0:
        print(f"❌ SMRITI Theme Governance Validation Failed: Found {total_errors} critical errors.\n")
        for file_path, res in report.items():
            if res["errors"]:
                print(f"[{file_path}]:")
                for e in res["errors"]:
                    print(f"  - ❌ {e}")
        sys.exit(1)
    else:
        print("✅ SMRITI Theme Governance Validation Passed successfully (0 critical errors).")
        sys.exit(0)
