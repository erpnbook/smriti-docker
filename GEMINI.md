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