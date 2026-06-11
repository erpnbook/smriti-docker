# SMRITI Routing Governance

## Canonical Route Policy

SMRITI Retail OS MUST use only canonical Frappe App Routes.

Allowed:

/app/<page-name>

Examples:

/app/smriti-dashboard
/app/stock-center
/app/billing-center
/app/master-data
/app/reports-center

Forbidden:

/page/*
/desk/page/*
#/page/*
#/desk/page/*
window.location routes pointing to /page/*
duplicate aliases pointing to the same page

## ROUTING RULE (Frappe v16+ Standard)

When creating or linking to any SMRITI page:

- Use route name only:
    `stock-center`
    `billing-center`
    `inventory-dashboard`

- Navigate using:
    `frappe.set_route("<route>")`

- Public URL must resolve to:
    `/app/<route>`

- Never generate:
    `/page/<route>`
    `/desk/page/<route>`
    `#/page/<route>`

- Before creating a page, search for existing routes and reuse them.
- If duplicate routes exist, keep only the canonical `/app` route.

### Practical Implementation Examples

#### Creating a Page
If your page name is `stock-center`, register/create it normally in Frappe and access it as:
`/app/stock-center`

#### Navigation
Use:
```javascript
frappe.set_route("stock-center");
// or
frappe.set_route("/app/stock-center");
```
*Preferred:*
```javascript
frappe.set_route("stock-center");
```
(because Frappe builds the URL automatically).

#### Sidebar Config
Use:
```javascript
{
  label: "Stock Center",
  route: "stock-center"
}
```
*NOT:*
```javascript
{
  label: "Stock Center",
  route: "/page/stock-center"
}
```
*and NOT:*
```javascript
{
  label: "Stock Center",
  route: "/desk/page/stock-center"
}
```

#### Buttons
Use:
```javascript
frappe.set_route("stock-center");
// or
window.location.href = "/app/stock-center";
```
*Preferred:*
```javascript
frappe.set_route("stock-center");
```

#### Workspace Links
Use:
```json
{
  "link_to": "stock-center",
  "type": "Page"
}
```
which resolves to:
`/app/stock-center`

## Route Consolidation Rule

Before creating any page:

1. Search existing routes.
2. Reuse existing canonical route if available.
3. Do not create alternate URLs for the same page.
4. If legacy routes exist, redirect them to the canonical /app route.
5. Never register both:

/app/example-page
/page/example-page

for the same destination.

## Navigation Rule

All sidebar links, shortcuts, workspaces, buttons, breadcrumbs,
deep links, notifications, and redirects MUST use:

/app/<page-name>

## Code Review Rule

Reject any PR that introduces:

/page/*
/desk/page/*
duplicate route aliases
custom router wrappers that bypass Frappe routing

unless explicitly approved in architecture documentation.

## Migration Rule

When legacy routes are discovered:

OLD:
/page/example

NEW:
/app/example

Implement redirect and remove references from:

- Sidebar
- Workspace shortcuts
- Dashboard cards
- Quick links
- Notifications
- Documentation

Canonical route must remain:

/app/example

---

# AI Bootstrap & Master Constitution

This repository is governed by AITDL.md.

Before performing any task:

1. Read AITDL.md
2. Follow all governance rules
3. Run the Agent Checklist (§7)
4. Respect SMRITI First Principle (§2)
5. Respect Navigation Governance (§3)
6. Respect Security Governance (§6)

If a request conflicts with AITDL.md, AITDL.md takes precedence.

AITDL.md is the authoritative constitution for this repository.
