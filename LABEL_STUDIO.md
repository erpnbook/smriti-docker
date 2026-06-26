# SMRITI Label Studio v2.1 — Operator & Developer Manual

**SMRITI Label Studio v2.1** is a high-performance, real-time label printing and custom template designing module integrated directly into the SMRITI Retail OS platform. It enables store operators to generate barcodes, apparel tags, and box labels either dynamically from inventory transactions or manually via an optimized search worksheet.

---

## 1. Core Modules & Subsystems

### 1.1 Template Designer
Label Studio features a raw-code print layout editor that allows technical managers to build templates using **ZPL** (Zebra Programming Language) or **TSPL** (TSC Printer Language):
- **Dynamic Token Swaps**: Templates support curly-braced variables (e.g., `{barcode}`, `{mrp}`, `{size}`) that SMRITI replaces with actual item master attributes at print time.
- **Field Mappings**: Users can map custom ERP fields (e.g., Outsole, Gender, Purchase Class) directly to custom positions on the labels.
- **Size Validation**: The designer includes safety validations preventing template uploads exceeding **100 KB** to protect printer buffers.

### 1.2 Style / Article Search & Filters
To load print items into the worksheet, operators can query the database using standard retail dimensions:
- **Brand**: Filter by registered brand names.
- **Merchandise Category & Sub-Category**: Filter by product classifications (e.g., Footwear, Loafers).
- **Barcode Size**: Filter by specific attribute dimensions (e.g., Size 8, Size 9).
- **Style / Article Search Input**:
  Queries the database to match search strings against `item_code`, `item_name`, and barcodes using the `search_barcode_items` API.
  > [!NOTE]
  > If autocomplete is enabled in the deployed build, the input field supports suggestion-based selection, utilizing keyboard navigation (`Arrow Up`, `Arrow Down`, `Enter`, `Escape`) and a **300ms debounce** to automatically load selected items into the print worksheet.

### 1.3 Transaction-Based Label Loading
Instead of manual item lookups, operators can pull items directly from stock documents:
- **Purchase Receipt**: Load all items and receipt quantities directly from supplier deliveries.
- **Stock Entry**: Load items from material transfers, stock reconciliations, or production logs.
- **Recent Transactions Panel**: The UI displays the latest 15 transactions in a dropdown list for rapid selection.

### 1.4 Live Preview Simulator
Before sending jobs to physical devices, the visual simulator draws a dynamic representation of the label layout in the browser:
- Simulates multi-column layouts (such as the TSPL 106x55 3-up label featuring a full MRP tag, shoe tag, and box tag).
- Render simulations of standard sizes: `50x25`, `50x30`, `75x50`, and `100x50` ZPL labels.
- Dynamically updates the preview whenever size options, print quantities, or item selections are modified in the queue worksheet.

---

## 2. Printer Interface Options

SMRITI supports two printing protocols: USB (local) and LAN (network).

```
                  ┌──────────────────────┐
                  │ SMRITI Label Studio  │
                  └──────────┬───────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
   [Local USB Interface]          [Network LAN Interface]
   ┌───────────────────────┐      ┌─────────────────────────┐
   │ QZ Tray WebSocket     │      │ Raw TCP Socket (Port 9100)│
   │ (localhost:8182)      │      │ (Direct IP Streaming)   │
   └──────────┬────────────┘      └────────────┬────────────┘
              ▼                                ▼
   ┌───────────────────────┐      ┌─────────────────────────┐
   │ Local Thermal Printer │      │ Network Label Printer   │
   └───────────────────────┘      └─────────────────────────┘
```

### 2.1 USB / Local Printing (via QZ Tray)
SMRITI connects to local USB thermal label printers using the **QZ Tray WebSocket service**:
- **Connection Lifecycle**: On page load, `initQZ()` establishes a persistent connection to `localhost` over port `8182`. The UI displays a live status indicator (🟢 Connected / 🔴 Not Connected).
- **Signature Validation**: Bypasses browser security prompts by configuring a trust certificate promise, allowing silent raw commands to stream directly to USB ports.
- **Print Safety Confirmations**: Displays a modal alert before printing high-volume batches (e.g., > 100 labels) or when template metrics mismatch the target paper sizes.

### 2.2 LAN / Network Socket Printing
For industrial setups, SMRITI streams print codes directly to printers over the store network:
- **Raw Socket Stream**: Uses standard TCP sockets over port `9100` via the whitelisted `send_to_network_printer` API.
- **Connection Diagnostics**: Operators can trigger a test connection to ping the device IP and measure latency response benchmarks in milliseconds.

---

## 3. Print Run Analytics Dashboard

Every print run writes a JSON-formatted activity log to the database. The analytics dashboard compiles this data into actionable business intelligence:
- **KPI Metrics**: Total labels printed, successful jobs, failed print counts, and average run sizes.
- **Top Metrics**: Automatically identifies the most used templates and most active printers on the network.
- **History Audit Trail**: Shows the last 30 print runs with exact timestamps, target IPs, template names, and cashier IDs.

---

## 4. Template Reference Tokens

Custom raw print templates support the following placeholder tokens. SMRITI supports both ERP Variant-based and Flat Item Master workflows, and barcode/PRN printing does not require ERP Variant structures.

| Token | ERP Field Reference | Example Value |
|---|---|---|
| `{barcode}` | Item Barcode (primary child table) | `8901030987654` |
| `{item_code}` | **ERPNext Item Code** used for inventory identification. May differ from the resolved business Style/Article code. | `BBM-SPORTS-BLK-08` |
| `{style}` | **Intelligent Style Resolution Engine**<br><br>Returns the business Style/Article code using the configured resolution priority.<br>See <b>Resolution Note</b> below. | `BBM-SPORTS` |
| `{style_code}` | **Explicit Style Code / Article Number**<br><br>Returns the explicit Style Code / Article Number field exactly as stored in the Item Master without applying Style Resolution. | `BBM-SPORTS` |
| `{variant_template}` | **ERP Variant Template ID**<br><br>Returns the template item ID (<i>variant_of</i>) for variant items. | `BBM-SPORTS` |
| `{item_name}` | Item Name (truncated to 28 characters) | `BBM Sports Black` |
| `{brand}` | Brand | `Tattly Threads` |
| `{mrp}` | Maximum Retail Price (Integer value) | `1899` |
| `{size}` | Attribute: Size | `8` |
| `{color}` | Attribute: Color / Colour / Shade | `BLACK` |
| `{pkd_date}` | Generated print date (MM/YY format) | `06/26` |
| `{purchase_class}` | Custom Purchase Class (e.g. MFW, LFW) | `SPORTS` |

> **Resolution Note**
>
> `{style}` represents the business Style/Article identifier and is resolved dynamically using the configured priority. It is **not** guaranteed to be a substring of `{item_code}`. In flat Item Master workflows, Style may originate from an explicit Style Code field or Import Profile mapping. SKU parsing is used only as a legacy compatibility fallback.
>
> The complete resolution order for `{style}` is:
> 1. Parent Template Item Code (`variant_of`) for ERP Variant items.
> 2. Explicit Style Code / Article Number field.
> 3. Import Profile mapped Style field (bulk copy-paste imports).
> 4. Configured SKU parsing rule (legacy compatibility fallback).
>
> When both `{style}` and `{style_code}` are available, `{style}` returns the resolved business value while `{style_code}` always returns the original stored field value.
>
> Future versions of SMRITI may extend the Style Resolution Engine with additional configurable data sources without changing existing template syntax. Existing templates using `{style}` remain backward compatible.

