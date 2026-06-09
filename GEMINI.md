# SMRITI RETAIL OS — ARCHITECTURE DIRECTIVE (LOCKED)

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