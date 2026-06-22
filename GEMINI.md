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

---

## Rule 9: No Desk Elements Policy (LOCKED — 2026-06-19)

### Policy Statement
Do NOT create, configure, expose, or link to any page, DocType, form, list view, report, or any other UI/UX element under `/desk/*`. All SMRITI user interface views and customer-facing features must reside on dedicated, standalone SMRITI www routes (e.g., `/smriti-*`, `/billing`, `/purchase`, etc.).

### Enforcement
1. **HTTP Routing**: Any incoming HTTP requests matching `/desk/*` must be blocked or redirected at the HTTP/boot-hook layer directly to the corresponding SMRITI standalone route or back to `/smriti`.
2. **File Structure**: Front-end assets must be stored in `www/` as standalone HTML/JS files, never inside standard Frappe `page/` directories that load inside `/desk`.
3. **No Desk Shortcuts**: PWA manifests, sidebar configs, workspaces, and user bookmarks must point to standalone routes and never to `/desk/*`.

---

## Rule 10: Explainable Metrics & Formula Transparency (Rule ID: DOC-01)

### Principle
Any field, report, dashboard metric, score, recommendation, prediction, KPI, alert, ranking, health score, forecast, or system-generated value displayed to a user must be accompanied by sufficient explanation for a non-technical business user to understand:
1. What the value means
2. How it was calculated
3. Which data contributed to it
4. What business action is recommended
5. What limitations or assumptions exist

### Mandatory Documentation Requirements
For every calculated field or report:
- **A. Business Meaning**: Why the metric exists and what it tracks.
- **B. Formula**: The exact mathematical expression.
- **C. Worked Example**: Arithmetic walk-through using real retail numbers.
- **D. Data Sources**: Source transaction tables or parameters.
- **E. Interpretation Guide**: Score bands (e.g., Critical, Monitor, Healthy).
- **F. Recommended Action**: Clear guidelines on what the user should do next based on the value.

### User Interface Transparency (ⓘ Explain Feature)
Whenever a computed KPI or prediction (e.g., `Confidence Score = 87%`) is displayed on a SMRITI UI/dashboard, the interface MUST provide an accessible **ⓘ Explain** button or modal rendering this transparency documentation with the live inputs populated.

### Enforcement
No KPI, Score, Forecast, Recommendation, or Dashboard Widget may be released to production unless the above details are fully documented.

---

## Rule 11: Formula Registry Policy (Rule ID: DOC-02)

### Policy Statement
Every mathematical or forecasting formula used inside SMRITI Retail OS must be centrally registered. No calculated dashboard metric, health score, or alert indicator may be deployed to production unless its formula is actively documented in the central Formula Registry.

### Registry Fields
Each registered formula must specify:
* Formula Name
* Formula Version
* Formula Expression
* Variables & Inputs
* Data Sources
* Effective Date / Last Modified Date
* Business Owner & Technical Owner

### Core Registered Formulas
The Formula Registry must include:
* Sales Velocity
* Weeks of Cover (WOC)
* Outlet Health Score
* Dead Stock Score
* Transfer Benefit Score
* Forecast Confidence
* Sell Through %
* Stock Accuracy %
* Inventory Turnover
* Variant Curve Health

---

## Rule 12: Author Attribution & Credibility Rule

### Mandatory Requirement
Every SMRITI User Manual, Training Guide, SOP, Operations Handbook, Architecture Guide, and Implementation Document must contain a structured Author Section at the beginning and the end.

### Author Profile
- **Author**: Jawahar R. Mallah
- **Designation**: Founder & Chief Architect
- **Organization**: AITDL – AI Technology & Development Lab
- **Professional Experience**: 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.

### Author Note
This manual is based on practical field experience gathered across retail operations, distribution management, inventory control, software architecture, business automation, and enterprise solution development. The objective is to make SMRITI Retail OS understandable and usable by both technical and non-technical users.

### Documentation Principle
The author believes that software should not only process data but also explain decisions. Every report, score, KPI, alert, recommendation, and prediction within SMRITI must be understandable by business users without requiring technical expertise.

### Quote
> "Light begins with learning."
> 
> — Jawahar R. Mallah
> Founder & Chief Architect, AITDL

### Required Manual Metadata
All manuals must contain:
1. Author Profile
2. Experience Summary
3. Documentation Version
4. Release Date
5. Intended Audience
6. Learning Objectives
7. Contact / Support Section
8. Revision History

This section must appear on the Cover Page, in the "About This Manual" section, and on the Final Acknowledgement Page.

---

## Rule 13: Explainability-First Development Rule (Rule ID: DOC-03)

### Policy Statement
No new module, report, KPI, dashboard card, AI recommendation, prediction, score, ranking, alert, or workflow may be released to production unless the following ten artifacts are completed and verified:
1. **Business Definition**
2. **Formula Definition**
3. **Worked Example**
4. **Data Source Mapping**
5. **Interpretation Guide**
6. **Recommended Action Guide**
7. **Formula Registry Entry**
8. **User Manual Chapter**
9. **Training Exercise**
10. **Audit Validation Test**

### Development Lifecycle
A SMRITI feature is not considered complete or ready for release until all five layers exist in the codebase:
$$\text{Design} \rightarrow \text{Formula Registry} \rightarrow \text{Implementation} \rightarrow \text{Documentation} \rightarrow \text{Training Workbook} \rightarrow \text{Release}$$
$$\text{Complete Feature} = \text{Code} + \text{Formula} + \text{Documentation} + \text{Training} + \text{Audit Validation}$$

---

## Rule 14: Digital Audit Trail for Recommendations (Rule ID: PDT-GOV-01)

### Policy Statement
Every purchase replenishment or network transfer recommendation generated by the Product Digital Twin (PDT) must be fully traceable and explainable. The system must save the exact snapshot of data inputs and parameters that produced the recommendation at the moment of execution.

### Audit Log Fields
For every recommendation, the following log fields are mandatory:
- **Recommendation ID** (Unique reference)
- **Generated By** (System/Module version)
- **Forecast Model & Version**
- **Reason Codes** (e.g. `STOCKOUT_RISK`, `EXCESS_COVER`, `POSITIVE_TRANSFER_BENEFIT`)
- **Input Variables** (Snapshot of Current Stock, Sales Velocity, and Lead Time)
- **Execution Timestamp**
- **Authorized User** (Auditor/Manager signature)
- **Execution Status** (Yes/No/Dismissed)

---

## Rule 15: Knowledge Layer & Business Dictionary (Rule ID: DOC-04)

### Policy Statement
SMRITI Retail OS must maintain a centralized, accessible Business Dictionary defining every key concept, metric, abbreviation, and parameter. 

### Dictionary Entry Schema
Every entry in the central SMRITI Business Dictionary must provide:
* **Definition**: Plain English and Hinglish meaning.
* **Mathematical Formula**: Clear math expression.
* **Worked Example**: Numerical walk-through.
* **Related Reports**: List of links to active reports.
* **Related Screens**: Links to SMRITI dashboard and master forms.
* **Frequently Asked Questions**: Common user inquiries.
* **Common Mistakes**: Explanations of user input errors and how to correct them.

### Priority Ranking for Implementation
SMRITI development modules and features will be implemented in the following order of priority:
1. **SMRITI Formula Registry** (DOC-02) — High Priority (5 Stars)
2. **ⓘ Explain Modal** (DOC-01) — High Priority (5 Stars)
3. **Business Dictionary** (DOC-04) — High Priority (5 Stars)
4. **Training Sandbox** — Medium Priority (4 Stars)
5. **Seasonality Engine** — Medium Priority (4 Stars)
6. **Advanced Forecast Models** — Low Priority (3 Stars)

---

## Rule 16: Documentation Before Deployment (Rule ID: DOC-05)

### Policy Statement
No feature, module, report, API, dashboard widget, KPI, prediction engine, recommendation engine, workflow, or integration may be marked as Production Ready or merged to the release branch unless the following ten documentation artifacts exist, are approved, and are checked into the repository:
1. **Functional Specification** (SOP and business flow)
2. **Technical Architecture** (Design layout, database mapping)
3. **Formula Registry Entries** (Rule DOC-02)
4. **User Manual Chapter** (Volume 1-3 alignment)
5. **Administrator Guide** (Security and setup settings)
6. **Training Exercise** (Workbook Scenario in Volume 5)
7. **API Documentation** (Endpoints, parameters, JSON payload)
8. **Test Cases** (Functional validation checks)
9. **Walkthrough Document** (Step-by-step verification)
10. **Release Notes** (Changelog description)

### Release Gate Workflow
$$\text{Development Complete} \rightarrow \text{Documentation Review} \rightarrow \text{Training Validation} \rightarrow \text{Audit Validation} \rightarrow \text{Production Approval}$$
Any feature lacking complete documentation is considered Incomplete and blocked from production deployment, regardless of code completeness.

### Core Principle
> "If it is not documented, it is not deployable."

### Rule ID: KGF-DOC-05 — Documentation Registry Requirement
All SMRITI documentation assets, user manuals, about pages, and governance files must be registered centrally through the `DOCUMENT_REGISTRY` in `help_api.py`. Hardcoding document routes or rendering files that bypass the registry's role-based metadata check is strictly prohibited.

---

## Rule 17: SMRITI Knowledge Operating System (Rule ID: SKOS-CORE-01 - LOCKED)

### Policy Statement
SMRITI Retail OS must maintain a centralized, schema-agnostic relational graph layer managed by the **SMRITI Knowledge Operating System (SKOS)** platform service. All explainability assets, formulas, business terms, reports, SOPs, processes, training materials, AI knowledge objects, and future metadata entities must be registered through `KAR-01` and linked through `KGR-01`.

Direct hardcoded relationships between knowledge assets are prohibited.

### Protected Standards
1. **KAR-01 (Knowledge Asset Registry)**: A polymorphic reference index mapping asset URIs (e.g. `smriti:formula:INV-002`) to physical DocType records using auto-generated UUID primary keys.
2. **KGR-01 (Knowledge Graph Relations)**: A generic relational matrix mapping asset-to-asset connection edges, governed by weight parameters, visibility permissions, and multi-tenant scopes.
3. **UAF-01 (Universal Attribute Framework)**: An extensible Entity-Attribute-Value (EAV) mapping schema allowing store owners to define scoped and reportable attributes without code migrations.

---

## Rule 18: Presentation & Template Metadata Safety Rule (Rule ID: TEMPLATE-01 - LOCKED — 2026-06-23)

### Purpose
Prevent developer metadata, debugging artifacts, implementation notes, and source comments from appearing in customer-facing experiences.

### Requirements
1. HTML templates must use only HTML comment syntax (`<!-- comment -->`).
2. JavaScript block comments (`/* comment */`) are prohibited outside script tags.
3. Customer-facing templates and rendered pages must not expose:
   * `@file:`
   * `@author:`
   * `@license:`
   * `Copyright`
   * `TODO`
   * `FIXME`
   * `DEBUG`
   * `console.log`
   * `alert`
4. All releases must pass:
   * `validate_html_templates.py`
   * `test_raw_templates_no_js_comments`
   * `test_rendered_pages_no_leaked_comments`
5. Any exposure of metadata, source annotations, or debugging artifacts in rendered output is a release-blocking defect.

### Classification
Presentation Integrity
Brand Governance
Experience Center Protection

### Severity
Critical

---

## SMRITI Knowledge Governance Framework (KGF)
Rules 13, 14, 15, 16, and 17 collectively constitute the **SMRITI Knowledge Governance Framework (KGF)**. The KGF is a core architectural pillar of SMRITI Retail OS, ensuring that:
- **Every number** displayed is explainable in plain business terms.
- **Every recommendation** generated is traceable with an immutable digital audit trail.
- **Every metric** is defined clearly in a centralized Business Dictionary.
- **Every release** is fully documented, verified, and accompanied by practical onboarding training materials.
- **Every operational asset** is dynamically linked and traversable through the centralized SMRITI Knowledge Operating System graph.
