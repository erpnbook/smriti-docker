---
Document ID: "KB-028"
Title: "Volume 4 Troubleshooting Faq"
Owner: "Support Team"
Audience: "Support Engineer"
Module: "Core"
Version: "1.0.0"
Status: "Active"
Primary Document: "Yes"
Depends On: ""
Related Modules: ""
Last Updated: "2026-06-25"
Last Reviewed: "2026-06-25"
AI Generated: "Yes"
Reviewed By: "Jawahar R. Mallah"
---

## Revision History

| Version | Date | Author | Summary of Changes |
| --- | --- | --- | --- |
| 1.0.0 | 2026-06-25 | Jawahar R. Mallah | Reorganized & standardized |


---

## Author Profile

- **Author**: Jawahar R. Mallah
- **Designation**: Founder & Chief Architect
- **Organization**: AITDL – AI Technology & Development Lab
- **Professional Experience**: 20+ Years of Experience in Software Development, Retail Technology, Distribution Systems, POS Solutions, ERP Implementations, Business Process Automation, and Enterprise Application Design.

> "Always decision-ready."  
> — Jawahar R. Mallah  
> Founder & Chief Architect, AITDL
---

## Purchase Studio FAQs (v2.0.0)

**Q: Where is the new Purchase Center?**
Go to Sidebar → Purchase → Purchase Center, or navigate to `/smriti-purchase`.

**Q: My PO went to "Pending Approval" — who approves it?**
Your Store Manager or designated Purchase Approver. They will see the PO in Purchase Center → Purchase Orders → Pending Approval. They click Approve or Reject.

**Q: Can I skip GRN and create an invoice directly?**
Depends on your Invoice Policy setting. If policy = GRN Only, a GRN is mandatory. If Flexible, standalone invoices are allowed. Ask your administrator to check Purchase Settings.

**Q: The supplier is not appearing in the PO supplier search.**
The supplier may be disabled in ERPNext, or restricted by User Permissions. Contact your system administrator.

**Q: How do I reconcile purchase returns with GST?**
Use the Purchase Return Register report (Reports → Purchase Reports → Purchase Return Register). It shows CGST, SGST, and IGST amounts for each return separately.

**Q: Where do I see which POs have not been fully received yet?**
In the Purchase Order Summary report, check the Status column for "To Receive and Bill" entries. These have goods outstanding.

---

## UIE / TallyPrime FAQs (v2.0.0)

**Q: How do I connect SMRITI to TallyPrime?**
See the [UIE TallyPrime Setup Guide](./uie_tally_setup.md) for step-by-step instructions.

**Q: Does SMRITI replace TallyPrime?**
No. SMRITI owns Inventory, Purchase, Sales, and POS. TallyPrime owns the books of accounts (Trial Balance, P&L, Balance Sheet). UIE bridges the two.

**Q: What happens if TallyPrime is offline when an invoice is submitted?**
The sync entry goes into the Sync Queue with status "Queued". When TallyPrime comes back online, the queue processes automatically.

**Q: How do I check if a voucher was posted to Tally?**
Go to UIE Integration Center → Sync Queue. Filter by the invoice name. Status = "Completed" means it was posted successfully.
