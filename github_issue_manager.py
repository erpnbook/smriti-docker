#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @file: github_issue_manager.py
# @description: Automatic GitHub Issue Sync and Manager tool for SMRITI Retail OS.
# @author: Jawahar R Mallah <jawahar.mallah@gmail.com>
# @version: 1.0.0
# @license: MIT

import os
import re
import sys
import json
import hashlib
import urllib.request
import urllib.error

CONFIG_FILE = ".github_config.json"
CACHE_FILE = ".github_todos.json"

def load_config():
    """Load configuration from config file or environment variables."""
    config = {
        "repo": "erpnbook/smriti-docker",  # Default repo, can be erpnbook/smriti
        "token": os.environ.get("GITHUB_TOKEN", ""),
        "author_name": "Jawahar R Mallah",
        "author_email": "jawahar.mallah@gmail.com"
    }
    
    # Try reading from config file if exists
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                file_config = json.load(f)
                config.update(file_config)
        except Exception as e:
            print(f"[-] Warning: Failed to read {CONFIG_FILE}: {e}")
            
    # Try reading from root .env if token is missing
    if not config["token"] and os.path.exists(".env"):
        try:
            with open(".env", "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("GITHUB_TOKEN="):
                        config["token"] = line.split("=", 1)[1].strip().strip('"').strip("'")
                        break
        except Exception:
            pass
            
    return config

def save_config(config):
    """Save configuration to file."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        print(f"[+] Saved configuration to {CONFIG_FILE}")
    except Exception as e:
        print(f"[-] Error saving configuration: {e}")

def load_cache():
    """Load sync cache mapping hashes to GitHub issue numbers."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_cache(cache):
    """Save sync cache to file."""
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=4)
    except Exception as e:
        print(f"[-] Error saving cache: {e}")

def github_request(config, path, method="GET", data=None):
    """Perform an authenticated HTTP request to GitHub API."""
    token = config.get("token")
    repo = config.get("repo")
    
    if not token:
        print("[-] Error: GitHub API Token is missing. Set it in .github_config.json or GITHUB_TOKEN environment variable.")
        sys.exit(1)
        
    url = f"https://api.github.com/repos/{repo}{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "SMRITI-GitHub-Issue-Manager/1.0"
    }
    
    req_data = None
    if data is not None:
        req_data = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
        
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as res:
            res_data = res.read().decode("utf-8")
            return json.loads(res_data) if res_data else {}
    except urllib.error.HTTPError as e:
        print(f"[-] GitHub API Error ({e.code}): {e.reason}")
        try:
            error_body = e.read().decode("utf-8")
            err_json = json.loads(error_body)
            print(f"    Message: {err_json.get('message')}")
        except Exception:
            pass
        raise e
    except Exception as e:
        print(f"[-] Connection Error: {e}")
        raise e

def create_issue(config, title, body, labels=None):
    """Create a new issue on GitHub."""
    author = config.get("author_name", "Jawahar R Mallah")
    # Append author attribution to description
    full_body = f"{body}\n\n---\n*Issue opened by {author} via SMRITI Issue Sync Manager.*"
    
    payload = {
        "title": title,
        "body": full_body,
        "labels": labels or ["bug", "todo"]
    }
    
    res = github_request(config, "/issues", "POST", payload)
    issue_number = res.get("number")
    issue_url = res.get("html_url")
    print(f"[+] Created Issue #{issue_number}: {title}")
    print(f"    URL: {issue_url}")
    return issue_number

def close_issue(config, issue_number, comment=None):
    """Close an issue on GitHub and add a resolution comment."""
    author = config.get("author_name", "Jawahar R Mallah")
    
    # 1. Add comment first
    if not comment:
        comment = f"Resolved and closed by {author}."
    else:
        comment = f"{comment}\n\n---\n*Commented and resolved by {author}*"
        
    try:
        github_request(config, f"/issues/{issue_number}/comments", "POST", {"body": comment})
    except Exception:
        print(f"[-] Warning: Failed to post closing comment to Issue #{issue_number}")
        
    # 2. Patch state to closed
    res = github_request(config, f"/issues/{issue_number}", "PATCH", {"state": "closed"})
    print(f"[+] Closed Issue #{issue_number} on GitHub.")
    return res

def scan_todos(base_dir="apps/smriti_retail_os"):
    """Scan the codebase for TODO/FIXME comments tagged with [Jawahar]."""
    todos = []
    # Regex matching: # TODO: [Jawahar] text OR // FIXME: [Jawahar] text
    pattern = re.compile(r'(?:#|//|--)\s*(TODO|FIXME):\s*\[Jawahar\]\s*(.*)', re.IGNORECASE)
    
    exclude_dirs = {".git", "__pycache__", "node_modules", "assets", "dist", "env"}
    
    for root, dirs, files in os.walk(base_dir):
        # Exclude directories in-place
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if not file.endswith((".py", ".js", ".html", ".css", ".md", ".json")):
                continue
                
            filepath = os.path.relpath(os.path.join(root, file), base_dir)
            fullpath = os.path.join(root, file)
            
            try:
                with open(fullpath, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, 1):
                        match = pattern.search(line)
                        if match:
                            tag = match.group(1).upper()
                            content = match.group(2).strip()
                            # Generate a unique hash for this specific TODO line content + file relative path
                            raw_id = f"{filepath}:{content}"
                            item_hash = hashlib.sha256(raw_id.encode("utf-8")).hexdigest()[:12]
                            
                            todos.append({
                                "hash": item_hash,
                                "tag": tag,
                                "content": content,
                                "file": filepath,
                                "line": line_num
                            })
            except Exception as e:
                print(f"[-] Error scanning file {fullpath}: {e}")
                
    return todos

def sync_todos(config):
    """Synchronize TODO comments in code with GitHub Issues."""
    print("[*] Scanning codebase for TODO/FIXME tags matching '[Jawahar]'...")
    current_todos = scan_todos()
    print(f"[+] Found {len(current_todos)} active tagged item(s) in codebase.")
    
    cache = load_cache()
    active_hashes = {t["hash"] for t in current_todos}
    
    # 1. Close resolved issues (hashes present in cache but no longer in the code)
    resolved_hashes = [h for h in cache if h not in active_hashes]
    if resolved_hashes:
        print(f"[*] Detected {len(resolved_hashes)} resolved item(s). Closing on GitHub...")
        for h in resolved_hashes:
            issue_number = cache[h]
            try:
                close_issue(config, issue_number, comment=f"Resolved automatically: comment removed from codebase.")
                del cache[h]
            except Exception as e:
                print(f"[-] Failed to auto-close issue #{issue_number}: {e}")
                
    # 2. Push new issues (hashes present in code but not in cache)
    for todo in current_todos:
        h = todo["hash"]
        if h not in cache:
            title = f"[{todo['tag']}] {os.path.basename(todo['file'])}: {todo['content']}"
            body = (
                f"### Code Check-in Alert\n\n"
                f"- **Type:** {todo['tag']}\n"
                f"- **File:** `{todo['file']}`\n"
                f"- **Line:** {todo['line']}\n\n"
                f"### Details\n"
                f"{todo['content']}"
            )
            try:
                issue_number = create_issue(config, title, body, labels=[todo['tag'].lower(), "smriti-todo"])
                cache[h] = issue_number
            except Exception as e:
                print(f"[-] Failed to push issue for {todo['file']}:{todo['line']}: {e}")
                
    save_cache(cache)
    print("[+] Sync completed successfully.")

def print_help():
    print("""SMRITI GitHub Issue Manager
Usage:
  python github_issue_manager.py init
    Initialize configuration file (.github_config.json)

  python github_issue_manager.py sync
    Auto-scan codebase for [Jawahar] tags, push new issues, and auto-close resolved ones

  python github_issue_manager.py open "<title>" "<body>"
    Manually open a GitHub issue (attributed to Jawahar R Mallah)

  python github_issue_manager.py close <issue_number> ["<closing comment>"]
    Manually close a GitHub issue (attributed to Jawahar R Mallah)
""")

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)
        
    cmd = sys.argv[1].lower()
    config = load_config()
    
    if cmd == "init":
        print("[*] Initializing SMRITI GitHub Issue Sync Config...")
        config["repo"] = input("Enter GitHub repository (e.g. erpnbook/smriti): ").strip() or config["repo"]
        config["token"] = input("Enter GitHub Personal Access Token (PAT): ").strip() or config["token"]
        config["author_name"] = input("Enter Author Name: ").strip() or config["author_name"]
        config["author_email"] = input("Enter Author Email: ").strip() or config["author_email"]
        save_config(config)
        
    elif cmd == "sync":
        if not config.get("token"):
            print("[-] GITHUB_TOKEN is not set. Please run 'python github_issue_manager.py init' first.")
            sys.exit(1)
        sync_todos(config)
        
    elif cmd == "open":
        if len(sys.argv) < 4:
            print("[-] Usage: python github_issue_manager.py open \"<title>\" \"<body>\"")
            sys.exit(1)
        title = sys.argv[2]
        body = sys.argv[3]
        create_issue(config, title, body)
        
    elif cmd == "close":
        if len(sys.argv) < 3:
            print("[-] Usage: python github_issue_manager.py close <issue_number> [\"comment\"]")
            sys.exit(1)
        try:
            issue_number = int(sys.argv[2])
        except ValueError:
            print("[-] Issue number must be an integer.")
            sys.exit(1)
            
        comment = sys.argv[3] if len(sys.argv) > 3 else None
        close_issue(config, issue_number, comment)
        
    else:
        print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
