---
title: Knowledge Governance Framework (KGF)
version: 1.0
last_updated: 2026-06-19
applies_to: SMRITI Retail OS v2.2.0
---

# SMRITI Knowledge Governance Framework (KGF)

SMRITI Retail OS is designed not only to process retail transactions and run forecasting models but also to explain its decisions clearly to business users. The **Knowledge Governance Framework (KGF)** is the central compliance and transparency layer of SMRITI that ensures every dashboard metric, score, recommendation, and prediction is explainable, documented, and traceable.

The KGF consists of three primary components that form an integrated audit chain:
1. **Central Formula Registry** (DOC-02)
2. **Universal Explain Modal** (DOC-01/03)
3. **Business Dictionary** (DOC-04)

---

## 🗺️ KGF Integration Chain

When a user clicks on an **ⓘ Explain** button next to any KPI or recommendation on a SMRITI dashboard, the system executes the following flow:

```
[Dashboard KPI / Metric]
         │
         ▼ (Triggers smritiExplain(formula_id))
[Universal Explain Modal]
         │
         ├─► [Worked Example & Formula Expression (No eval() used)]
         │
         ├─► [📘 Read Manual / 🎓 Training Lesson (Coming Soon wrapper)]
         │
         └─► [📖 Dictionary Entry]
                      │
                      ▼ (Loads /smriti-dictionary?term=ID)
              [Business Dictionary Drawer]
                      │
                      ├─► [Hinglish Explanation, FAQs, Mistakes]
                      └─► [Related Terms & Related Formulas]
```

---

## 🔒 Core Governance Directives

The SMRITI Constitution enforces strict rules regarding mathematical computations and business intelligence displays:

*   **Rule DOC-01 (Explainable Metrics & Formula Transparency)**: Any computed dashboard metric, forecast, or score must provide the user with a Worked Example, Data Sources, and Recommended Actions.
*   **Rule DOC-02 (Formula Registry Policy)**: Every formula must be centrally registered. No calculated dashboard metric or indicator may be deployed unless its formula is registered.
*   **Rule DOC-03 (Explainability-First Development Rule)**: No new feature or recommendation engine may go live without completing the ten required explainability artifacts.
*   **Rule DOC-04 (Business Dictionary)**: The platform must maintain a central, searchable glossary of retail operational terms with Hinglish translations.
*   **Rule 12 (Author Attribution & Credibility)**: Every guide, handbook, and governance document must support transparency and explain the business rationale clearly.

---

## Support & Helpdesk
For questions or support, please contact the SMRITI Helpdesk at **support@aitdl.com**.
