---
title: POS FAQ
version: 1.0
last_updated: 2026-06-18
applies_to: SMRITI Retail OS v1.x
---

# Frequently Asked Questions — POS Operations

### Q1: Why can't I see products in the POS search or category lists?
**A**: Ensure the following product attributes are configured in the Item Master:
- **Disabled** must be set to `No`.
- **Is Sales Item** must be set to `Yes`.
- **Maintain Stock** must be set to `Yes`.
- The item must have an active price in the Selling Price List linked to the cashier's active POS Profile.
- The item must be linked to the company and warehouse designated in the profile.

### Q2: How do I refund a sale or process a return?
**A**:
1. Open the POS cart panel and select **Sales Return**.
2. Input the original invoice ID.
3. Select the items being returned, specify the return quantity, and confirm.
4. The register automatically processes stock receipt back into the warehouse and creates a draft Credit Note for manager approval.

### Q3: Can I print duplicate receipts for a past checkout transaction?
**A**: Yes. Navigate to the POS shift history panel or search for the submitted POS Invoice. Click the target invoice, open the Print View, and click **Print** to generate a duplicate receipt. SMRITI prints this receipt formatted under your default whitelabel brand layout.

### Q4: How do I handle cashier shift variances during register closure?
**A**: If the physical cash counted in the drawer does not match the system's expected balance:
- The cashier logs the actual closing amounts.
- If the difference exceeds the validation threshold (e.g. Rs. 500), the terminal locks.
- A Store Manager must verify the discrepancy and enter their numeric POS PIN to authorize the shift closure override.

### Q5: Can I recall a held bill on a different POS terminal?
**A**: By default, held bills (`custom_is_held = 1`) are locked to the cashier's active user ID and POS Profile to maintain register segregation. However, a Store Manager can override the user lock via the management console to load the draft cart onto another checkout terminal.
