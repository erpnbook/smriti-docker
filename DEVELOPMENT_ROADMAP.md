# Development Roadmap: SMRITI Retail OS

## 1. Top 20 Improvements Matrix
Ranked by business value and ROI.

| # | Improvement | Category | Impact | Effort | Risk | ROI |
|---|---|---|---|---|---|---|
| 1 | **Secure Secret Management** | Security | Critical | Low | Low | Infinite |
| 2 | **Standardize Schema to JSON** | Architecture | High | Med | Med | High |
| 3 | **Dedicated POS PIN Field** | Security | High | Low | Low | High |
| 4 | **Redis-Cached Stock Lookups** | Performance | High | Med | Low | High |
| 5 | **Replace JSON Blobs with Child Tables** | Architecture | Med | Low | Low | High |
| 6 | **Offline Resiliency (PWA/Service Workers)**| Reliability | High | High | Med | High |
| 7 | **Comprehensive API Unit Testing** | Stability | High | Med | Low | Med |
| 8 | **Async/Incremental Asset Sync** | Performance | Med | Med | Low | Med |
| 9 | **Remove Hardcoded Role Strings** | Architecture | Med | Low | Low | Med |
| 10 | **AI Inventory Predictor (ML Integration)** | Innovation | High | High | High | Med |
| 11 | **Smart Barcode Resolver (Fuzzy Search)** | UX | Med | Med | Low | Med |
| 12 | **JWT Authentication for Billing Terminal** | Security | High | High | Med | Med |
| 13 | **Automated Cloud Backups (S3/Azure)** | Reliability | Med | Med | Low | Med |
| 14 | **POS Audit Trail Expansion** | Governance | Med | Med | Low | Med |
| 15 | **Dark Mode / Dynamic Theming** | UX | Low | Low | Low | Low |
| 16 | **Biometric Manager Override** | Security | Med | High | Med | Low |
| 17 | **Developer CLI Tooling** | DX | Low | Low | Low | Med |
| 18 | **Multi-Currency Standardization** | Expansion | Low | Med | Low | Low |
| 19 | **Sales Invoice UI Event Logging** | Audit | Med | Low | Low | Med |
| 20 | **Frappe v16 Regression Testing** | Stability | Critical | Med | Low | N/A |

## 2. 12-Month Implementation Timeline

### Phase 1: Stabilization & Security (Months 1-3)
- **Month 1**: Migrate hardcoded passwords to environment variables. Implement dedicated hashed PIN field for managers.
- **Month 2**: Convert `setup.py` DocType definitions to standard Frappe JSON manifests. Add first wave of API unit tests.
- **Month 3**: Refactor `SMRITI Company Settings` to use proper child tables instead of JSON blobs.

### Phase 2: Performance & Reliability (Months 4-6)
- **Month 4**: Implement Redis-based caching for POS item/stock lookups to handle enterprise-scale datasets.
- **Month 5**: Optimize `sync_assets.py` to support incremental syncing (only copy changed files).
- **Month 6**: Launch PWA (Progressive Web App) support for the billing terminal to ensure basic functionality during network drops.

### Phase 3: Enterprise Features & Governance (Months 7-9)
- **Month 7**: Implement JWT-based authentication for the standalone billing terminal.
- **Month 8**: Expand Audit Trail to capture all UI-level transformations and manager override events.
- **Month 9**: Standardize multi-currency logic and tax overrides for global retail deployments.

### Phase 4: AI & Innovation (Months 10-12)
- **Month 10**: Integrate an AI Inventory Predictor to alert store managers of potential stock-outs.
- **Month 11**: Deploy the Smart Barcode Resolver for faster, error-tolerant scanning.
- **Month 12**: Complete full regression testing suite and prepare for the next major Frappe/ERPNext version.

## 3. Immediate "Quick Wins"
1. **Security Patch**: Move the DB password from `pwd.yml` to an `.env` file (Effort: < 1 hour).
2. **UX Fix**: Implement the 4-digit PIN override in `billing_api.py` (Effort: 1 day).
3. **Architecture Fix**: Run `bench export-fixtures` or manually create the JSON files for current custom DocTypes (Effort: 1 day).

## 4. Barcode Studio Quality Engineering Roadmap

To maintain strict alignment with the SMRITI Governance Framework and the AITDL constitution, the Barcode Studio roadmap is structured as a sequential quality engineering capability:

- **Phase 3A: Design Quality Intelligence (Completed)**: Configurable Quiet Zone expansions, Virtual HRT bounds validation, and Printability Score Engine (`SMRITI-PRN-SCORE-01`).
- **Phase 4: Operational Telemetry Intelligence (ACP-BARCODE-002A)**: Standalone scan telemetry collection pipeline, Scan Reliability Score (`SMRITI-SCAN-REL-01`), governance event IDs (`SCAN-EVT-001/002/003`), and 90-day retention cleanup.
- **Phase 5: Predictive Barcode Twin (ACP-BARCODE-002B)**: Downstream machine learning loops (PDT) correlating design-time layouts with real-world physical scan performance.

---
*Roadmap generated based on architectural audit of D:\Smriti_Retail_OS.*

