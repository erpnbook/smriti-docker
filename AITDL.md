# SMRITI RETAIL OS — ARCHITECTURE DIRECTIVE (LOCKED)

Rule 7: Every new page/module = dedicated SMRITI UI. Frappe/ERPNext UI never exposed.

## CORE PRINCIPLE
ERPNext/Frappe SHALL REMAIN the backend transaction and business engine.
SMRITI Retail OS SHALL REMAIN the frontend experience layer, workflow layer, and business intelligence layer.
DO NOT convert SMRITI into a separate ERP.
DO NOT duplicate ERPNext core functionality unless there is a specific business requirement.

---

## ARCHITECTURE MODEL
SMRITI Retail OS
↓
Service Layer / APIs
↓
Frappe Framework
↓
ERPNext Core
↓
Database

---

## ERPNext RESPONSIBILITIES
ERPNext remains the System of Record for:
* Accounting
* General Ledger
* GST
* Tax Engine
* Sales Invoice
* Purchase Invoice
* Stock Ledger
* Warehouses
* Companies
* Customers
* Suppliers
* Users
* Roles
* Permissions
* Audit Trails
* Financial Reports

SMRITI must leverage these engines wherever possible.

---

## SMRITI RESPONSIBILITIES
SMRITI owns:
* UI / UX
* Retail Workflows
* Dashboard Layer
* POS Experience
* Reporting Experience
* Business Analytics
* Store Operations
* Reorder Intelligence
* PSV (Party Stock Visibility)
* PSA (Party Stock Accounts)
* Exception Management
* Notification Layer
* Mobile Experiences
* Industry-Specific Extensions

---

## DEVELOPMENT RULES
1. **ERPNext first.** Before creating a new module, check whether ERPNext already provides the required capability.
2. **Reuse before rebuild.** Do not recreate:
   * Accounting
   * Tax
   * Inventory valuation
   * User management
   * Core permissions
3. **Experience over duplication.** If ERPNext already performs the backend process, improve the workflow and presentation inside SMRITI rather than rebuilding the backend logic.
4. **API-driven design.** SMRITI frontend should communicate through service APIs and abstraction layers rather than direct database manipulation wherever possible.
5. **Upgrade-safe customization.** Avoid ERPNext core modifications. Use:
   * Custom Apps
   * Hooks
   * Custom Fields
   * APIs
   * Service Layers
6. **Service-first design.** The frontend must not instantiate or manipulate Frappe documents directly (e.g., avoid `frappe.client.insert("Sales Invoice")` from UI). Instead, route all operations through dedicated business service controllers (e.g., `billing_service.create_invoice()`, `psv_service.create_transaction()`) to decouple the UI from backend schema changes.

---

## PSV SPECIAL RULE
PSV and PSA are SMRITI-owned modules. They are classified as a **Business-Type Activated Core Extension**, not an optional add-on. They become primary operational modules for businesses selling through external channels (e.g., Footwear Brands, FMCG, Distributor Networks), while remaining hidden for standard retail.

However, technically:
* They must read ERPNext master data.
* They must not modify ERPNext Stock Ledger Entries.
* They must not modify ERPNext General Ledger Entries.
* They must maintain their own shadow ledger architecture.
* PSV remains the internal architecture name, though user-facing labels may change (Channel Stock, Distributor Inventory, etc.).

---

## LONG-TERM VISION
SMRITI Retail OS is a premium retail operating layer built on top of ERPNext.
ERPNext provides the transaction engine.
SMRITI provides the user experience, operational intelligence, industry workflows, and business productivity layer.
Future development should strengthen this separation rather than blur it.

---

## Rule 7: SMRITI-First UI Development

Every new page, module, form, report, or UI component added to
SMRITI Retail OS MUST be built as a dedicated SMRITI page.

NEVER use or expose the following directly to end users:
- Frappe Desk forms (/desk or /app routes)
- ERPNext standard DocType forms
- Frappe standard List views
- Frappe standard Report builder UI
- Frappe standard Workspace pages
- Any Frappe or ERPNext URL directly

### Required Pattern for Every New Feature

WRONG:
  User clicks → opens /desk#Form/Sales Invoice/new
  User clicks → opens /app/sales-invoice
  User clicks → frappe.new_doc("Sales Invoice")
  User clicks → frappe.set_route("Form", "Customer")

CORRECT:
  User clicks → opens /billing (SMRITI custom page)
  User clicks → opens /smriti-masters (SMRITI custom page)
  User clicks → smriti_api.create_invoice() via frappe.call()
  User clicks → SMRITI modal/form renders custom UI

### Mandatory Checklist for Every New Addition

Before any new page or module is created, the developer or AI agent
MUST answer YES to all of the following:

[ ] Does this have a dedicated SMRITI www page or custom page route?
[ ] Does the user URL contain /smriti, /billing, /inventory,
    /reports, /masters or another SMRITI-owned route?
[ ] Is all backend communication going through a SMRITI service
    controller (not direct frappe.client.insert or frappe.new_doc
    from frontend)?
[ ] Is the page styled with SMRITI design system
    (Navy #1A2B5C + Blue #2563EB + Arial)?
[ ] Does the page show SMRITI logo and branding?
[ ] Is /desk and /app completely hidden from this user flow?

If any answer is NO — do not proceed.
Build the SMRITI wrapper first, then implement the feature.

### New Page — Minimum Required Files

For every new SMRITI page, these files are mandatory:

  smriti_retail_os/www/<page-name>.html   ← UI template
  smriti_retail_os/www/<page-name>.py     ← Auth + context
  smriti_retail_os/api/<feature>_api.py   ← Whitelisted backend API

Optional but recommended:
  smriti_retail_os/public/js/<page-name>.js   ← Page JS
  smriti_retail_os/public/css/<page-name>.css ← Page CSS

### New Module — Minimum Required Structure

  smriti_retail_os/
  └── <module_name>/
      ├── __init__.py
      ├── api/
      │   └── <module>_api.py      ← All whitelisted APIs
      ├── service/
      │   └── <module>_service.py  ← Business logic
      └── www/
          └── smriti-<module>.html ← SMRITI UI page

### Naming Convention

All SMRITI pages:     /smriti-<feature>
All SMRITI APIs:      smriti_retail_os.<module>.api.<feature>_api.<method>
All SMRITI services:  smriti_retail_os.<module>.service.<feature>_service.<method>
All SMRITI CSS:       smriti_<feature>.css
All SMRITI JS:        smriti_<feature>.js

### This Rule Cannot Be Overridden

No client request, deadline pressure, or shortcut justifies
exposing Frappe Desk or ERPNext UI to end users.

If a feature cannot be built with a SMRITI wrapper in time:
  → Delay the feature
  → Do NOT expose raw Frappe/ERPNext UI as a workaround

---

### If Feature Is Not Ready — Use Coming Soon Page

NEVER expose Frappe Desk or ERPNext UI as a temporary workaround.
ALWAYS use the SMRITI Coming Soon page instead.

Usage from any SMRITI page or sidebar link:

  Basic:
  /smriti-coming-soon?feature=Purchase+Orders

  With progress:
  /smriti-coming-soon?feature=Purchase+Orders&progress=60

  With ETA:
  /smriti-coming-soon?feature=Purchase+Orders&progress=60&eta=Q3+2026

  With back button:
  /smriti-coming-soon?feature=Purchase+Orders&progress=60&back=/smriti

From sidebar JS:
  function goToFeature(route, featureName, progress, eta) {
      if (!isRouteReady(route)) {
          window.location.href =
              '/smriti-coming-soon'
              + '?feature=' + encodeURIComponent(featureName)
              + '&progress=' + (progress || 0)
              + (eta ? '&eta=' + encodeURIComponent(eta) : '');
          return;
      }
      window.location.href = route;
  }

To add a new planned feature to the registry:
  Edit: smriti_retail_os/api/coming_soon_api.py
  Add entry to COMING_SOON_REGISTRY dict.
  No bench restart needed — API reads live.

---

## Rule 8: Setup Wizard = SMRITI Page Required (LOCKED — 2026-06-10)

### Trigger Condition

If the browser shows ANY of the following after login or navigation:
  - /desk/setup-wizard
  - /desk/setup-wizard/0
  - /desk#setup-wizard
  - /desk/modules
  - /app (any Frappe/ERPNext route)
  - Any Frappe Desk URL

**This is a POLICY VIOLATION. These pages must NEVER reach a user.**

### Required Action

When you see this trigger, the correct response is:

  WRONG:
    Let the setup wizard load.
    Use the Frappe wizard to configure settings.
    Navigate /desk to use ERPNext forms.
    Use frappe.set_route() to open desk forms.

  CORRECT:
    Intercept at boot.py before_request hook.
    Redirect to /smriti immediately.
    Create a dedicated SMRITI page for whatever action was needed.
    File a task to build the SMRITI equivalent if it doesn't exist yet.

### What Setup Wizard Appearing Means

The Frappe setup wizard appears in two scenarios:

1. **First install** — setup_complete = 0 in System Settings.
   Fix: boot.py already sets bootinfo.setup_complete = 1 to suppress it.

2. **Missing SMRITI page** — user/agent tried to navigate somewhere and
   Frappe fell back to its default route (/desk or setup-wizard).
   Fix: identify what action was needed → create the SMRITI page for it.

### boot.py Enforcement (Technical Implementation)

SMRITI_BLOCKED_DESK_PATHS in boot.py enforces this at the HTTP layer:
  - /desk/setup-wizard → redirect to /smriti (ALL users, including Administrator)
  - /desk/modules      → redirect to /smriti
  - /desk#Form         → redirect to /smriti
  - /desk#List         → redirect to /smriti
  - /desk#query-report → redirect to /smriti
  - /desk#setup-wizard → redirect to /smriti

To block additional Frappe paths, add to SMRITI_BLOCKED_DESK_PATHS
in smriti_retail_os/boot.py. Never remove existing entries.

### Permanent AI Agent Rule

For AI agents (Antigravity, Gemini, or any future agent) working on SMRITI:

  Before using any Frappe/ERPNext page, DocType form, list view, or URL:
  STOP. Check if a SMRITI equivalent exists.
  If it exists: use the SMRITI page.
  If it does not exist: create the SMRITI page first, THEN implement the feature.
  Never use /desk, /app, or /setup-wizard as a shortcut or workaround.

This rule applies to ALL development work, testing, verification, and
browser automation — including browser subagents used for UI testing.

### This Rule Cannot Be Overridden

No deadline, no shortcut, no "temporary" workaround justifies exposing
Frappe/ERPNext native UI to users or using it as a verification target.
If a SMRITI page doesn't exist for the needed verification:
  → Build the SMRITI page first (see Rule 7 checklist)
  → Then verify through that SMRITI page

---

# SMRITI Retail OS — AI Agent Architecture Constitution v1.0

Status: LOCKED
Authority: AITDL / PrathamOne
Applies To: All AI Agents, Developers, Contributors, Automation Systems

---

## RULE 1 — DO NOT REPLACE THE ARCHITECTURE

AI agents are prohibited from redesigning SMRITI Retail OS.

Agents may:
* Extend
* Improve
* Refactor
* Optimize

Agents may NOT:
* Replace architecture
* Introduce competing architectures
* Create parallel frameworks
* Ignore approved service layers

---

## RULE 2 — SERVICE-FIRST DESIGN (MANDATORY)

Frontend MUST NEVER directly manipulate database records.

Required flow:
UI → API → Service Layer → Business Logic → Database

Forbidden:
UI → Database
UI → DocType Insert

All business operations must pass through approved service controllers.

---

## RULE 3 — INVENTORY-FIRST OPERATIONS

SMRITI is an operational retail platform.
Inventory is the operational source of truth.
All stock-related calculations must originate from:
* Purchase
* GRN
* Landed Cost
* Stock Ledger

Never create separate stock valuation systems.
Never create duplicate inventory ledgers.

---

## RULE 4 — TALLY-FIRST ACCOUNTING STRATEGY

SMRITI is NOT a replacement for TallyPrime.
SMRITI owns:
* Inventory
* Purchase
* Sales
* PSV
* Pricing
* Intelligence
* AI

Tally owns:
* Books of Accounts
* Trial Balance
* Balance Sheet
* P&L
* Statutory Accounting

Agents must NOT create:
* General Ledger Engine
* Trial Balance Engine
* Balance Sheet Engine
* Financial Closing Engine
unless explicitly approved.

---

## RULE 5 — SINGLE SOURCE OF TRUTH

Every business concept must have exactly one owner.

Examples:
* Inventory Valuation: Inventory
* Coverage Days: Intelligence
* Demand Forecast: AI Hub
* Channel Stock: PSV

No duplicate ownership allowed.

---

## RULE 6 — PSV OWNERSHIP BOUNDARY

PSV = Party Stock Visibility
PSV owns:
* Distributor Stock
* Channel Stock
* Sell Through
* Coverage Days
* Inventory Aging
* Capital Locked
* Recovery Suggestions

PSV does NOT own:
* Warehouse Inventory
* Purchase Processing
* Accounting

---

## RULE 7 — INVENTORY VS PSV

Inventory: Company-owned stock
PSV: Channel/distributor stock

Agents must never merge these domains.

---

## RULE 8 — NO SHADOW DATABASES

Agents are prohibited from creating:
* Duplicate stock tables
* Duplicate customer masters
* Duplicate supplier masters
* Duplicate pricing masters

Existing masters must be extended, not replaced.

---

## RULE 9 — PRICING IS A SEPARATE DOMAIN

Pricing is NOT inventory.
Pricing owns:
* Price Lists
* Customer Pricing
* Promotions
* Schemes
* Price Revisions

Inventory must never maintain selling prices.

---

## RULE 10 — APPROVAL BEFORE AUTOMATION

Analytics may be automatic.
Business actions may NOT be automatic.

Allowed:
* Recommendations
* Suggestions
* Alerts

Forbidden without approval:
* Auto Purchase Orders
* Auto Transfers
* Auto Discounts
* Auto Price Changes

Human approval required.

---

## RULE 11 — FEATURE FLAGS REQUIRED

Future features must be hidden until activated.

Examples:
* Coverage Days
* Capital Locked
* AI Forecasting
* Recovery Suggestions

No unfinished features exposed to users.

---

## RULE 12 — BACKWARD COMPATIBILITY

Agents must preserve:
* Existing APIs
* Existing DocTypes
* Existing Workflows

Breaking changes require explicit approval.

---

## RULE 13 — AUDITABILITY

Every critical action must be traceable.

Required:
* User
* Timestamp
* Before Value
* After Value
* Reason

Examples:
* Price Revision
* Stock Adjustment
* Recovery Actions
* Configuration Changes

---

## RULE 14 — NO NEW PROJECTS RULE

Agents must prioritize:
1. Existing approved modules
2. Existing roadmap items
3. Existing pilot requirements

Agents may not introduce unrelated projects.

---

## RULE 15 — GOVERNANCE GATE

Before implementation:
Architecture Review → Gap Analysis → Approval → Implementation → Verification → Evidence Collection → Closure

Agents must never skip governance stages.

---

## FINAL PRINCIPLE

SMRITI Retail OS is:
Retail Operations + Inventory Intelligence + Party Stock Visibility + AI-assisted Decision Support

It is NOT:
* A Tally replacement
* A General ERP clone
* A Financial Accounting Platform

All future development must reinforce this identity.

---

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
