# SMRITI Scale Risk Matrix

## 1. Scale Transition Risks

| Business Stage | Scale Risk | Impact | Priority |
|---|---|---|---|
| **1 - 10 Stores** | **Permission Collision** | Store Manager A modifies Store Manager B's users. | **P1** |
| **10 - 50 Stores** | **Worker Starvation** | Material Transfers delay POS checkout response time. | **P1** |
| **50 - 100 Stores** | **Database Lock Contention**| Simultaneous Day-Close updates on central Company DocType. | **P2** |
| **Franchise Model** | **Governance Leakage** | Franchisee gains access to Global System Settings via role exploit. | **P0** |

## 2. Technical Risk Breakdown

### 2.1 The "Shared Site" Single-Point-of-Failure (P0)
- **Risk**: A corruption in the single `frontend` site configuration or a failed migration on the monolithic database takes down **all** stores simultaneously.
- **CTO Verdict**: For a Retail OS, this is an unacceptable risk for 100+ stores.
- **Mitigation**: Move toward a multi-site orchestration where groups of 5-10 stores share a site/container pod.

### 2.2 Global State via `frappe.defaults` (P1)
- **Risk**: SMRITI uses `frappe.db.get_default("smriti_backup_settings")`. 
- **Impact**: In a multi-tenant franchise model, one franchisee changing their backup time changes it for everyone.
- **Mitigation**: Migrate all platform settings to the `SMRITI Company Settings` DocType.

### 2.3 Asset Sync Congestion (P2)
- **Risk**: Physical file copying in `sync_assets.py` scales linearly with the number of apps/assets.
- **Impact**: Container boot time increases from seconds to minutes as the app ecosystem grows.
- **Mitigation**: Use `rsync` with the `--update` flag instead of `shutil.copytree` to only sync changed files.

## 3. Strategic Redesign Phase-In
- **Phase 1 (Immediate)**: Secure the `reset_user_password` API to prevent Store Managers from escalating privileges.
- **Phase 2 (Before 20 Stores)**: Implement multi-site configuration for `backup_settings`.
- **Phase 3 (Enterprise)**: Move to a distributed worker architecture where critical POS APIs have dedicated Redis queues.

---
*Roadmap generated for SMRITI Retail OS CTO Review.*
