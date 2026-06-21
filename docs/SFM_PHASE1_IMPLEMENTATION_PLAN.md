# SMRITI Sales Force Management (SFM) — Phase 1 Implementation Plan (v1.0.0)

---

### Author Profile (Start)
* **Author**: Jawahar R. Mallah
* **Designation**: Founder & Chief Architect
* **Organization**: AITDL – AI Technology & Development Lab
* **Professional Experience**: 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.

#### Author Note
This implementation manual is based on practical field experience gathered across retail operations, distribution management, inventory control, software architecture, business automation, and enterprise solution development. The objective is to make SMRITI Retail OS understandable and usable by both technical and non-technical users.

> "Light begins with learning."
> 
> — Jawahar R. Mallah
> Founder & Chief Architect, AITDL

---

## 1. Development Process & Tasks

### Step 1: DocType Declarations
Create the folder structure and schemas for the core DocTypes:
- `SMRITI Customer Ownership`
- `SMRITI Sales Target`
- `SMRITI SFM Settings`
- `SMRITI Attribution Rule` (Reserved placeholder)
- `SMRITI Attribution Event`
- `SMRITI Attribution Ledger`
- `SMRITI Sales KPI Snapshot`

Files to generate:
- JSON definition files under `smriti_retail_os/smriti_retail_os/doctype/`
- Python class controller files extending `Document`

### Step 2: Implementation of Service Layer
- Create `smriti_retail_os/sfm/service/attribution_service.py` with invoice submit and cancel hook handlers.
- Create `smriti_retail_os/sfm/service/target_service.py` for target vs achievement reporting logic.
- Register event hooks inside `smriti_retail_os/hooks.py` for `POS Invoice` and `Sales Invoice`.

### Step 3: API & Dashboard Interface
- Create whitelisted APIs in `smriti_retail_os/sfm/api/sfm_api.py`.
- Create WWW templates: `www/smriti-sfm.html`, `www/smriti-sfm.py`, and public static JS/CSS assets.

### Step 4: Verification Suite
- Write unit tests in `smriti_retail_os/tests/test_sfm_phase1.py` verifying full/split attribution, settings split overrides, timeline validations, and daily KPI snapshot generation.

---

## 2. Directory Structure

```text
smriti_retail_os/
├── hooks.py
├── sfm/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── sfm_api.py
│   └── service/
│       ├── __init__.py
│       ├── attribution_service.py
│       └── target_service.py
├── smriti_retail_os/
│   └── doctype/
│       ├── smriti_customer_ownership/
│       ├── smriti_sales_target/
│       ├── smriti_sfm_settings/
│       ├── smriti_attribution_rule/
│       ├── smriti_attribution_event/
│       ├── smriti_attribution_ledger/
│       └── smriti_sales_kpi_snapshot/
├── tests/
│   └── test_sfm_phase1.py
└── www/
    ├── smriti-sfm.html
    └── smriti-sfm.py
```

---

## 3. Database Migration & Provisioning

After the DocType JSON definitions are added to the codebase:
1. Run `bench migrate` to provision the database tables and update the schema.
2. The schema files will be picked up by the custom app installer automatically.
