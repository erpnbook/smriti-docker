---
title: Licensing Security Architecture
version: 1.0
last_updated: 2026-06-18
applies_to: SMRITI Retail OS v1.x
---

# SMRITI OS Licensing Security Architecture

This document describes the cryptographic design, signature schemas, and installation binding rules governing SMRITI's offline licensing system.

## 🔑 HMAC-SHA256 Signature Schema

SMRITI validates licenses using cryptographic signatures, allowing activation checks without active internet connections.

### Signature Validation Formula
```text
HMAC-SHA256(secret_key, "SMRT" | version | Base64URL(payload_json))
```

1. **Secret Resolution**: SMRITI resolves the secret key by checking:
   - `smriti_license_secret` in the site config.
   - `SMRITI_LICENSE_SECRET` environment variables.
   - Development fallback keys (triggers console warnings).
2. **Signature Comparison**: The calculated hash is compared to the hex signature suffix of the license key (`SMRT-1-payload-signature`) using a constant-time comparison helper (`frappe.security.csrf_token.compare_secrets` or python's `hmac.compare_digest`).

---

## 🔒 Installation Binding

To prevent the reuse of license keys across multiple client sites, keys are bound to a specific server installation:
- **Installation ID**: When SMRITI is initialized, it generates a unique installation ID (UUID) and saves it to the global configuration.
- **Payload binding**: SMRITI license payloads specify an installation target:
  - `iid = "uuid-string"`: Key is valid only if the local installation ID matches the payload target.
  - `iid = "*"`: Floating license key (can be used on any installation, typically reserved for sandbox environments or large retail chains with centralized license profiles).
- **Modification Block**: The system rejects keys where the signature has been tampered with or where the payload does not match the local installation UUID.
