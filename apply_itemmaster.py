import os
import re

file_path = r"d:\Smriti_Retail_OS\apps\smriti_retail_os\smriti_retail_os\www\smriti-presentation.html"

if not os.path.exists(file_path):
    print("Error: smriti-presentation.html not found.")
    exit(1)

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

print("Original file length:", len(content))

# 1. Reorganize Selector HTML Screen
# We replace the flat grid of cards under <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 pt-4">...</div>
# Let's define the new grouped selector HTML:
grouped_selector_html = """        <!-- Mode Group Sections (SMRITI Experience Center Reorganization) -->
        <div class="space-y-8 pt-4">
          <!-- Business View Group -->
          <div class="space-y-3">
            <h2 class="text-lg font-outfit font-extrabold text-emerald-400 flex items-center gap-2 border-b border-white/5 pb-2">
              <span>💼</span> Business View
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <!-- Owner Deck -->
              <div class="glass-card p-6 rounded-2xl flex flex-col justify-between border-t-4 border-emerald-500 hover:scale-[1.02] transition cursor-pointer" onclick="selectDeck('owner')">
                <div>
                  <span class="text-xs text-emerald-400 font-bold uppercase tracking-wider block mb-2">15 Slides</span>
                  <h3 class="text-xl font-outfit font-bold text-white mb-2">Owner Presentation</h3>
                  <p class="text-slate-400 text-sm">Focuses on business problems, operational outcomes, margin protection, and return on investment. Free of technical jargon.</p>
                </div>
                <div class="mt-6 flex justify-between items-center">
                  <span class="text-xs text-emerald-400 font-bold">Start Business Deck →</span>
                  <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 text-[10px] font-bold uppercase">ROI Focused</span>
                </div>
              </div>

              <!-- Distributor Deck -->
              <div class="glass-card p-6 rounded-2xl flex flex-col justify-between border-t-4 border-amber-500 hover:scale-[1.02] transition cursor-pointer" onclick="selectDeck('distributor')">
                <div>
                  <span class="text-xs text-amber-400 font-bold uppercase tracking-wider block mb-2">15 Slides</span>
                  <h3 class="text-xl font-outfit font-bold text-white mb-2">Distributor Deck</h3>
                  <p class="text-slate-400 text-sm">Focuses on wholesale operations, logistics, collections aging, route optimization, and secondary sales network visibility.</p>
                </div>
                <div class="mt-6 flex justify-between items-center">
                  <span class="text-xs text-amber-400 font-bold">Start Wholesale Deck →</span>
                  <span class="px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 text-[10px] font-bold uppercase">Wholesale</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Operations View Group -->
          <div class="space-y-3">
            <h2 class="text-lg font-outfit font-extrabold text-blue-400 flex items-center gap-2 border-b border-white/5 pb-2">
              <span>⚙️</span> Operations View
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <!-- Manager Deck -->
              <div class="glass-card p-6 rounded-2xl flex flex-col justify-between border-t-4 border-blue-500 hover:scale-[1.02] transition cursor-pointer" onclick="selectDeck('manager')">
                <div>
                  <span class="text-xs text-blue-400 font-bold uppercase tracking-wider block mb-2">20 Slides</span>
                  <h3 class="text-xl font-outfit font-bold text-white mb-2">Manager Presentation</h3>
                  <p class="text-slate-400 text-sm">Focuses on store operations, cashier productivity trackers, stock auditing, shift registers, and daily stock management.</p>
                </div>
                <div class="mt-6 flex justify-between items-center">
                  <span class="text-xs text-blue-400 font-bold">Start Operations Deck →</span>
                  <span class="px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 text-[10px] font-bold uppercase">Store Ops</span>
                </div>
              </div>

              <!-- Label & Scan Studio Card -->
              <div class="glass-card p-6 rounded-2xl flex flex-col justify-between border-t-4 border-indigo-500 hover:scale-[1.02] transition cursor-pointer" onclick="selectDeck('barcode')">
                <div>
                  <span class="text-xs text-indigo-400 font-bold uppercase tracking-wider block mb-2">15 Slides</span>
                  <h3 class="text-xl font-outfit font-bold text-white mb-2">Label &amp; Scan Studio</h3>
                  <p class="text-slate-400 text-sm">Focuses on barcode workflows, label design, scanning productivity, warehouse operations, and audit accuracy.</p>
                </div>
                <div class="mt-6 flex justify-between items-center">
                  <span class="text-xs text-indigo-400 font-bold">Start Label &amp; Scan Deck →</span>
                  <span class="px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 text-[10px] font-bold uppercase">Operations</span>
                </div>
              </div>

              <!-- Item Master Studio Card -->
              <div class="glass-card p-6 rounded-2xl flex flex-col justify-between border-t-4 border-rose-500 hover:scale-[1.02] transition cursor-pointer" onclick="selectDeck('itemmaster')">
                <div>
                  <span class="text-xs text-rose-400 font-bold uppercase tracking-wider block mb-2">15 Slides</span>
                  <h3 class="text-xl font-outfit font-bold text-white mb-2">Item Master Studio</h3>
                  <p class="text-slate-400 text-sm">Focuses on product catalogs, dynamic variant generation, pricing governance, completeness metrics, and health audits.</p>
                </div>
                <div class="mt-6 flex justify-between items-center">
                  <span class="text-xs text-rose-400 font-bold">Start Catalog Deck →</span>
                  <span class="px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 text-[10px] font-bold uppercase">Foundation</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Technical View Group -->
          <div class="space-y-3">
            <h2 class="text-lg font-outfit font-extrabold text-purple-400 flex items-center gap-2 border-b border-white/5 pb-2">
              <span>🛡️</span> Technical View
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <!-- Technical Deck -->
              <div class="glass-card p-6 rounded-2xl flex flex-col justify-between border-t-4 border-purple-500 hover:scale-[1.02] transition cursor-pointer" onclick="selectDeck('tech')">
                <div>
                  <span class="text-xs text-purple-400 font-bold uppercase tracking-wider block mb-2">25 Slides</span>
                  <h3 class="text-xl font-outfit font-bold text-white mb-2">Technical Presentation</h3>
                  <p class="text-slate-400 text-sm">Focuses on SMRITI architecture, central ledger systems, secure transaction routing, audit telemetry, and scale limits.</p>
                </div>
                <div class="mt-6 flex justify-between items-center">
                  <span class="text-xs text-purple-400 font-bold">Start Architecture Deck →</span>
                  <span class="px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 text-[10px] font-bold uppercase">Architects</span>
                </div>
              </div>
            </div>
          </div>
        </div>"""

pattern_grid = r'<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 pt-4">.*?<!-- SMRITI Label & Scan Studio Card -->.*?</div>\s*</div>\s*</div>'
match_grid = re.search(pattern_grid, content, re.DOTALL)
if match_grid:
    print("Found selector grid block.")
    content = re.sub(pattern_grid, grouped_selector_html, content, flags=re.DOTALL, count=1)
else:
    print("Error: Selector grid block NOT found.")
    exit(1)

# 2. Add 6th navigation button in #demo-mode-bar
nav_bar_target = """    <button onclick="selectDeck('distributor')" id="btn-mode-distributor" class="px-4 py-1.5 rounded-full text-xs font-bold transition-all duration-300">Distributor View</button>
    <button onclick="selectDeck('barcode')" id="btn-mode-barcode" class="px-4 py-1.5 rounded-full text-xs font-bold transition-all duration-300">Label &amp; Scan Studio</button>"""

nav_bar_new = """    <button onclick="selectDeck('distributor')" id="btn-mode-distributor" class="px-4 py-1.5 rounded-full text-xs font-bold transition-all duration-300">Distributor View</button>
    <button onclick="selectDeck('barcode')" id="btn-mode-barcode" class="px-4 py-1.5 rounded-full text-xs font-bold transition-all duration-300">Label &amp; Scan Studio</button>
    <button onclick="selectDeck('itemmaster')" id="btn-mode-itemmaster" class="px-4 py-1.5 rounded-full text-xs font-bold transition-all duration-300">Item Master Studio</button>"""

if "btn-mode-itemmaster" not in content:
    content = content.replace(nav_bar_target, nav_bar_new)

# 3. Update selectDeck function variables and style resets
select_deck_vars_target = """      const btnDistributor = document.getElementById('btn-mode-distributor');
      const btnBarcode = document.getElementById('btn-mode-barcode');"""

select_deck_vars_new = """      const btnDistributor = document.getElementById('btn-mode-distributor');
      const btnBarcode = document.getElementById('btn-mode-barcode');
      const btnItemMaster = document.getElementById('btn-mode-itemmaster');"""

if "btnItemMaster =" not in content:
    content = content.replace(select_deck_vars_target, select_deck_vars_new)

select_deck_reset_target = """      // Reset styles
      [btnOwner, btnManager, btnTech, btnDistributor, btnBarcode].forEach(btn => {"""

select_deck_reset_new = """      // Reset styles
      [btnOwner, btnManager, btnTech, btnDistributor, btnBarcode, btnItemMaster].forEach(btn => {"""

content = content.replace(select_deck_reset_target, select_deck_reset_new)

# Update selectDeck deckType conditions
select_deck_cond_target = """      } else if (deckType === 'barcode') {
        currentDeck = SLIDES_BARCODE;
      }"""

select_deck_cond_new = """      } else if (deckType === 'barcode') {
        currentDeck = SLIDES_BARCODE;
      } else if (deckType === 'itemmaster') {
        currentDeck = SLIDES_ITEMMASTER;
      }"""

if "SLIDES_ITEMMASTER;" not in content:
    content = content.replace(select_deck_cond_target, select_deck_cond_new)

# Clean selectDeck styling blocks and add barcode + itemmaster styling
select_deck_distributor_styling_target = """      } else if (deckType === 'distributor') {
        accentColor = '#f59e0b'; // Amber
        btnDistributor.className = "px-4 py-1.5 rounded-full text-xs font-bold transition-all duration-300 bg-amber-500 text-white shadow-lg shadow-amber-500/20";
        logoBox.className = "w-8 h-8 rounded flex items-center justify-center shadow-lg transition-all duration-300 bg-amber-500 shadow-amber-500/20";

        const btnBarcode = document.getElementById('btn-mode-barcode');
      if (btnBarcode) {
        btnBarcode.className = "px-4 py-1.5 rounded-full text-xs font-bold transition-all duration-300 text-slate-400 hover:text-white bg-transparent";
      }
      // Hide What-If button
        document.getElementById('btn-whatif-hud').classList.remove('flex');
        document.getElementById('btn-whatif-hud').classList.add('hidden');
        document.getElementById('whatif-separator').classList.add('hidden');
      }"""

# Replace all of that and insert barcode & itemmaster properly
select_deck_new_styling = """      } else if (deckType === 'distributor') {
        accentColor = '#f59e0b'; // Amber
        if (btnDistributor) btnDistributor.className = "px-4 py-1.5 rounded-full text-xs font-bold transition-all duration-300 bg-amber-500 text-white shadow-lg shadow-amber-500/20";
        logoBox.className = "w-8 h-8 rounded flex items-center justify-center shadow-lg transition-all duration-300 bg-amber-500 shadow-amber-500/20";

        // Hide What-If button
        document.getElementById('btn-whatif-hud').classList.remove('flex');
        document.getElementById('btn-whatif-hud').classList.add('hidden');
        document.getElementById('whatif-separator').classList.add('hidden');
      } else if (deckType === 'barcode') {
        accentColor = '#6366f1'; // Indigo
        if (btnBarcode) btnBarcode.className = "px-4 py-1.5 rounded-full text-xs font-bold transition-all duration-300 bg-indigo-500 text-white shadow-lg shadow-indigo-500/20";
        logoBox.className = "w-8 h-8 rounded flex items-center justify-center shadow-lg transition-all duration-300 bg-indigo-500 shadow-indigo-500/20";

        // Hide What-If button
        document.getElementById('btn-whatif-hud').classList.remove('flex');
        document.getElementById('btn-whatif-hud').classList.add('hidden');
        document.getElementById('whatif-separator').classList.add('hidden');
      } else if (deckType === 'itemmaster') {
        accentColor = '#f43f5e'; // Rose
        if (btnItemMaster) btnItemMaster.className = "px-4 py-1.5 rounded-full text-xs font-bold transition-all duration-300 bg-rose-500 text-white shadow-lg shadow-rose-500/20";
        logoBox.className = "w-8 h-8 rounded flex items-center justify-center shadow-lg transition-all duration-300 bg-rose-500 shadow-rose-500/20";

        // Hide What-If button
        document.getElementById('btn-whatif-hud').classList.remove('flex');
        document.getElementById('btn-whatif-hud').classList.add('hidden');
        document.getElementById('whatif-separator').classList.add('hidden');
      }"""

content = content.replace(select_deck_distributor_styling_target, select_deck_new_styling)

# Clean up other duplicate resets inside distributor/tech/manager selectDeck logic (if any)
# Let's search and replace other instances where btnBarcode reset is duplicated inside distributor etc.
# Wait, let's see. In selectDeck styling of 'tech' and 'manager', did the script also inject the resets?
# Yes! Let's check lines 3655 and 3668 in our previous print output:
#   } else if (deckType === 'manager') {
#     ...
#     const btnBarcode = document.getElementById('btn-mode-barcode');
#     if (btnBarcode) { btnBarcode.className = ... bg-transparent; }
#   }
# Let's clean those up as well.
# We will match the manager styling block:
manager_styling_target = """      } else if (deckType === 'manager') {
        accentColor = '#2563eb'; // Blue
        btnManager.className = "px-4 py-1.5 rounded-full text-xs font-bold transition-all duration-300 bg-blue-500 text-white shadow-lg shadow-blue-500/20";
        logoBox.className = "w-8 h-8 rounded flex items-center justify-center shadow-lg transition-all duration-300 bg-blue-500 shadow-blue-500/20";

        const btnBarcode = document.getElementById('btn-mode-barcode');
      if (btnBarcode) {
        btnBarcode.className = "px-4 py-1.5 rounded-full text-xs font-bold transition-all duration-300 text-slate-400 hover:text-white bg-transparent";
      }
      // Hide What-If button
        document.getElementById('btn-whatif-hud').classList.remove('flex');
        document.getElementById('btn-whatif-hud').classList.add('hidden');
        document.getElementById('whatif-separator').classList.add('hidden');"""

manager_styling_clean = """      } else if (deckType === 'manager') {
        accentColor = '#2563eb'; // Blue
        if (btnManager) btnManager.className = "px-4 py-1.5 rounded-full text-xs font-bold transition-all duration-300 bg-blue-500 text-white shadow-lg shadow-blue-500/20";
        logoBox.className = "w-8 h-8 rounded flex items-center justify-center shadow-lg transition-all duration-300 bg-blue-500 shadow-blue-500/20";

        // Hide What-If button
        document.getElementById('btn-whatif-hud').classList.remove('flex');
        document.getElementById('btn-whatif-hud').classList.add('hidden');
        document.getElementById('whatif-separator').classList.add('hidden');"""

content = content.replace(manager_styling_target, manager_styling_clean)

# Clean tech styling block
tech_styling_target = """      } else if (deckType === 'tech') {
        accentColor = '#8b5cf6'; // Purple
        btnTech.className = "px-4 py-1.5 rounded-full text-xs font-bold transition-all duration-300 bg-purple-500 text-white shadow-lg shadow-purple-500/20";
        logoBox.className = "w-8 h-8 rounded flex items-center justify-center shadow-lg transition-all duration-300 bg-purple-500 shadow-purple-500/20";

        const btnBarcode = document.getElementById('btn-mode-barcode');
      if (btnBarcode) {
        btnBarcode.className = "px-4 py-1.5 rounded-full text-xs font-bold transition-all duration-300 text-slate-400 hover:text-white bg-transparent";
      }
      // Hide What-If button
        document.getElementById('btn-whatif-hud').classList.remove('flex');
        document.getElementById('btn-whatif-hud').classList.add('hidden');
        document.getElementById('whatif-separator').classList.add('hidden');"""

tech_styling_clean = """      } else if (deckType === 'tech') {
        accentColor = '#8b5cf6'; // Purple
        if (btnTech) btnTech.className = "px-4 py-1.5 rounded-full text-xs font-bold transition-all duration-300 bg-purple-500 text-white shadow-lg shadow-purple-500/20";
        logoBox.className = "w-8 h-8 rounded flex items-center justify-center shadow-lg transition-all duration-300 bg-purple-500 shadow-purple-500/20";

        // Hide What-If button
        document.getElementById('btn-whatif-hud').classList.remove('flex');
        document.getElementById('btn-whatif-hud').classList.add('hidden');
        document.getElementById('whatif-separator').classList.add('hidden');"""

content = content.replace(tech_styling_target, tech_styling_clean)

# Clean up exitDeck resets and add both barcode + itemmaster resets
exit_deck_resets_target = """      const btnBarcode = document.getElementById('btn-mode-barcode');
      if (btnBarcode) {
        btnBarcode.className = "px-4 py-1.5 rounded-full text-xs font-bold transition-all duration-300 text-slate-400 hover:text-white bg-transparent";
      }
      // Hide What-If button"""

exit_deck_resets_new = """      const btnBarcode = document.getElementById('btn-mode-barcode');
      if (btnBarcode) {
        btnBarcode.className = "px-4 py-1.5 rounded-full text-xs font-bold transition-all duration-300 text-slate-400 hover:text-white bg-transparent";
      }
      const btnItemMaster = document.getElementById('btn-mode-itemmaster');
      if (btnItemMaster) {
        btnItemMaster.className = "px-4 py-1.5 rounded-full text-xs font-bold transition-all duration-300 text-slate-400 hover:text-white bg-transparent";
      }
      // Hide What-If button"""

content = content.replace(exit_deck_resets_target, exit_deck_resets_new)

# Update confidence meter conditions to add itemmaster
confidence_meter_cond_target = """      } else if (currentDeck === SLIDES_BARCODE) {
        if (slideIndex === 0) {
          status = "Studio Status: Active";
        } else if (slideIndex < 3) {
          status = "Challenges Identified";
        } else if (slideIndex < 6) {
          status = "Generation Configured";
        } else if (slideIndex < 9) {
          status = "Printing Simulator Ready";
        } else if (slideIndex < 11) {
          status = "Audit Variances Clear";
        } else if (slideIndex < 13) {
          status = "Productivity Secured";
        } else {
          status = "Scan Accuracy: 99.9%";
        }"""

confidence_meter_cond_new = """      } else if (currentDeck === SLIDES_ITEMMASTER) {
        if (slideIndex === 0) {
          status = "Catalog Risk: High";
        } else if (slideIndex < 14) {
          status = "Catalog Quality Improving";
        } else {
          status = "Catalog Confidence: 95%";
        }
      } else if (currentDeck === SLIDES_BARCODE) {
        if (slideIndex === 0) {
          status = "Studio Status: Active";
        } else if (slideIndex < 3) {
          status = "Challenges Identified";
        } else if (slideIndex < 6) {
          status = "Generation Configured";
        } else if (slideIndex < 9) {
          status = "Printing Simulator Ready";
        } else if (slideIndex < 11) {
          status = "Audit Variances Clear";
        } else if (slideIndex < 13) {
          status = "Productivity Secured";
        } else {
          status = "Scan Accuracy: 99.9%";
        }"""

content = content.replace(confidence_meter_cond_target, confidence_meter_cond_new)

# 4. Define SLIDES_ITEMMASTER array content
slides_itemmaster_def = """
    const SLIDES_ITEMMASTER = [
      {
        title: "Introduction",
        html: `
          <div class="max-w-4xl mx-auto text-center space-y-8">
            <div class="inline-flex items-center gap-3 px-4 py-2 rounded-full bg-rose-500/10 border border-rose-500/20 text-rose-400 font-bold text-sm tracking-wider uppercase mb-2">
              Retail Intelligence Platform
            </div>
            <h1 class="text-6xl md:text-7xl font-outfit font-extrabold text-white tracking-tight leading-none">
              SMRITI <span class="text-accent">Item Master Studio</span>
            </h1>
            <p class="text-2xl md:text-3xl font-light text-slate-300 italic">"The Foundation of Retail Intelligence"</p>
            <div class="h-[1px] w-48 bg-gradient-to-r from-transparent via-rose-500 to-transparent mx-auto"></div>
            <div class="pt-6 space-y-2">
              <p class="text-xs text-slate-500 uppercase tracking-widest font-bold">Powered by AITDL Network</p>
              <div class="glass-card max-w-md mx-auto p-4 rounded-xl border border-rose-500/20 bg-rose-950/5">
                <p class="text-sm font-bold text-white">Jawahar R. Mallah</p>
                <p class="text-xs text-slate-400">Founder &amp; Chief Architect, AITDL</p>
                <p class="text-[11px] text-slate-500 mt-1">20+ Years Experience in Software Development, Retail Technology, &amp; Enterprise Solution Design</p>
              </div>
              <p class="text-xs text-accent italic mt-2">"Light begins with learning."</p>
            </div>
          </div>
        `
      },
      {
        title: "Data Quality Objections",
        html: `
          <div class="max-w-6xl mx-auto space-y-4">
            <div class="text-center space-y-1">
              <span class="text-red-500 font-bold uppercase tracking-wider text-[10px]">Operational Objections</span>
              <h2 class="text-3xl font-outfit font-extrabold text-white">What Happens When Item Data Is Wrong?</h2>
              <p class="text-slate-400 text-xs max-w-xl mx-auto">Click any catalog issue to trace how SMRITI mitigates the operational impact.</p>
            </div>

            <div class="grid grid-cols-2 md:grid-cols-5 gap-3 pt-2">
              <button onclick="showItemObjectionDetails('size')" id="item-obj-tab-size" class="glass-card p-3 rounded-xl border border-white/5 hover:border-red-500/40 hover:scale-[1.02] transition cursor-pointer text-center space-y-1 flex flex-col justify-center min-h-[95px]">
                <span class="text-lg">📏</span>
                <span class="font-outfit font-bold text-xs text-white block">Wrong Size</span>
              </button>
              <button onclick="showItemObjectionDetails('price')" id="item-obj-tab-price" class="glass-card p-3 rounded-xl border border-white/5 hover:border-red-500/40 hover:scale-[1.02] transition cursor-pointer text-center space-y-1 flex flex-col justify-center min-h-[95px]">
                <span class="text-lg">💰</span>
                <span class="font-outfit font-bold text-xs text-white block">Wrong Price</span>
              </button>
              <button onclick="showItemObjectionDetails('category')" id="item-obj-tab-category" class="glass-card p-3 rounded-xl border border-white/5 hover:border-red-500/40 hover:scale-[1.02] transition cursor-pointer text-center space-y-1 flex flex-col justify-center min-h-[95px]">
                <span class="text-lg">📁</span>
                <span class="font-outfit font-bold text-xs text-white block">Wrong Category</span>
              </button>
              <button onclick="showItemObjectionDetails('image')" id="item-obj-tab-image" class="glass-card p-3 rounded-xl border border-white/5 hover:border-red-500/40 hover:scale-[1.02] transition cursor-pointer text-center space-y-1 flex flex-col justify-center min-h-[95px]">
                <span class="text-lg">🖼️</span>
                <span class="font-outfit font-bold text-xs text-white block">Missing Images</span>
              </button>
              <button onclick="showItemObjectionDetails('duplicate')" id="item-obj-tab-duplicate" class="glass-card p-3 rounded-xl border border-white/5 hover:border-red-500/40 hover:scale-[1.02] transition cursor-pointer text-center space-y-1 flex flex-col justify-center min-h-[95px]">
                <span class="text-lg">🚨</span>
                <span class="font-outfit font-bold text-xs text-white block">Duplicate SKUs</span>
              </button>
            </div>

            <div id="item-obj-detail-box" class="glass-card p-5 rounded-2xl border border-red-500/20 bg-red-950/5 min-h-[140px] flex flex-col justify-center">
              <div id="item-obj-detail-content" class="text-xs text-slate-300">
                Click one of the catalog issue cards above to trace its operational and business impacts.
              </div>
            </div>
          </div>
        `
      },
      {
        title: "Item Lifecycle Explorer",
        html: `
          <div class="max-w-6xl mx-auto space-y-4">
            <div class="text-center space-y-1">
              <span class="text-accent font-bold uppercase tracking-wider text-[10px]">Data Flow</span>
              <h2 class="text-3xl font-outfit font-extrabold text-white">Item Lifecycle Explorer</h2>
              <p class="text-slate-400 text-xs">Tracing how product records progress from creation to analytical reporting.</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-5 gap-4 pt-2">
              <div class="glass-card p-4 rounded-xl border border-white/5 flex flex-col items-center text-center space-y-2">
                <div class="w-10 h-10 rounded-full bg-rose-500/15 text-rose-400 flex items-center justify-center font-bold font-outfit text-sm">1</div>
                <span class="font-outfit font-bold text-xs text-white">Create</span>
                <p class="text-[10px] text-slate-400 leading-relaxed">Establish base article with core fields: style code, brand, and size grid.</p>
              </div>

              <div class="glass-card p-4 rounded-xl border border-white/5 flex flex-col items-center text-center space-y-2">
                <div class="w-10 h-10 rounded-full bg-rose-500/15 text-rose-400 flex items-center justify-center font-bold font-outfit text-sm">2</div>
                <span class="font-outfit font-bold text-xs text-white">Validate</span>
                <p class="text-[10px] text-slate-400 leading-relaxed">Auto-scan fields to verify mandatory entries, price ranges, and unique identifiers.</p>
              </div>

              <div class="glass-card p-4 rounded-xl border border-white/5 flex flex-col items-center text-center space-y-2">
                <div class="w-10 h-10 rounded-full bg-rose-500/15 text-rose-400 flex items-center justify-center font-bold font-outfit text-sm">3</div>
                <span class="font-outfit font-bold text-xs text-white">Approve</span>
                <p class="text-[10px] text-slate-400 leading-relaxed">Manager signs off price list and variants structure, publishing it to stores.</p>
              </div>

              <div class="glass-card p-4 rounded-xl border border-white/5 flex flex-col items-center text-center space-y-2">
                <div class="w-10 h-10 rounded-full bg-rose-500/15 text-rose-400 flex items-center justify-center font-bold font-outfit text-sm">4</div>
                <span class="font-outfit font-bold text-xs text-white">Sell</span>
                <p class="text-[10px] text-slate-400 leading-relaxed">POS registers synchronize the approved catalog for barcode scans.</p>
              </div>

              <div class="glass-card p-4 rounded-xl border border-white/5 flex flex-col items-center text-center space-y-2">
                <div class="w-10 h-10 rounded-full bg-rose-500/15 text-rose-400 flex items-center justify-center font-bold font-outfit text-sm">5</div>
                <span class="font-outfit font-bold text-xs text-white">Analyze</span>
                <p class="text-[10px] text-slate-400 leading-relaxed">System compiles metrics: sales velocity, inventory coverage, and health status.</p>
              </div>
            </div>
          </div>
        `
      },
      {
        title: "Product Intelligence Hub",
        html: `
          <div class="max-w-6xl mx-auto space-y-4">
            <div class="text-center space-y-1">
              <span class="text-accent font-bold uppercase tracking-wider text-[10px]">Data Classification</span>
              <h2 class="text-3xl font-outfit font-extrabold text-white">Product Intelligence Hub</h2>
              <p class="text-slate-400 text-xs">Establish rich data classification parameters to support advanced business intelligence reporting.</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 pt-2">
              <div class="glass-card p-4 rounded-xl border border-white/5 space-y-1.5">
                <span class="text-rose-400 font-bold text-xs">🏢 Brand</span>
                <p class="text-[10px] text-slate-400 leading-relaxed">Tracks master brand names and sub-brands, supporting multi-brand store sales analysis.</p>
              </div>
              <div class="glass-card p-4 rounded-xl border border-white/5 space-y-1.5">
                <span class="text-rose-400 font-bold text-xs">📦 Department</span>
                <p class="text-[10px] text-slate-400 leading-relaxed">High-level store divisions (e.g. Apparel, Footwear, Accessories) for macro budget allocations.</p>
              </div>
              <div class="glass-card p-4 rounded-xl border border-white/5 space-y-1.5">
                <span class="text-rose-400 font-bold text-xs">📁 Category</span>
                <p class="text-[10px] text-slate-400 leading-relaxed">Product classifications (e.g., Denim, Running Shoes) mapping directly to custom tax slabs.</p>
              </div>
              <div class="glass-card p-4 rounded-xl border border-white/5 space-y-1.5">
                <span class="text-rose-400 font-bold text-xs">🍂 Season</span>
                <p class="text-[10px] text-slate-400 leading-relaxed">Seasonal tracking (e.g. Summer 2026, Winter 2025) supporting inventory markdown strategies.</p>
              </div>
              <div class="glass-card p-4 rounded-xl border border-white/5 space-y-1.5">
                <span class="text-rose-400 font-bold text-xs">💎 Collection</span>
                <p class="text-[10px] text-slate-400 leading-relaxed">Special releases or premium lines (e.g. Athleisure, Festive) for targeted marketing analysis.</p>
              </div>
              <div class="glass-card p-4 rounded-xl border border-white/5 space-y-1.5">
                <span class="text-rose-400 font-bold text-xs">👫 Gender</span>
                <p class="text-[10px] text-slate-400 leading-relaxed">Customer profile segments (Mens, Womens, Unisex, Kids) to optimize marketing campaigns.</p>
              </div>
            </div>
          </div>
        `
      },
      {
        title: "Variant Generator",
        html: `
          <div class="max-w-6xl mx-auto space-y-4">
            <div class="text-center space-y-1">
              <span class="text-accent font-bold uppercase tracking-wider text-[10px]">Variant Builder</span>
              <h2 class="text-3xl font-outfit font-extrabold text-white">Dynamic Variant Generator</h2>
              <p class="text-slate-400 text-xs">Generate size-color variants dynamically. Toggle attribute parameters and watch SMRITI construct variants.</p>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 pt-2">
              <div class="lg:col-span-5 glass-card p-5 rounded-2xl border border-white/5 space-y-4 flex flex-col justify-between">
                <div class="space-y-3 text-xs text-slate-300">
                  <span class="panel-section-title text-rose-400 font-bold text-sm block">1. Select Attributes</span>
                  
                  <div class="space-y-1">
                    <span class="text-[10px] text-slate-500 uppercase font-bold block">Colors</span>
                    <div class="flex gap-3">
                      <label class="flex items-center gap-1.5"><input type="checkbox" checked id="v-col-blue" onchange="updateVariantCount()" class="accent-rose-500"> Blue</label>
                      <label class="flex items-center gap-1.5"><input type="checkbox" checked id="v-col-black" onchange="updateVariantCount()" class="accent-rose-500"> Black</label>
                      <label class="flex items-center gap-1.5"><input type="checkbox" id="v-col-grey" onchange="updateVariantCount()" class="accent-rose-500"> Grey</label>
                    </div>
                  </div>

                  <div class="space-y-1">
                    <span class="text-[10px] text-slate-500 uppercase font-bold block">Garment Sizes</span>
                    <div class="flex gap-3 flex-wrap">
                      <label class="flex items-center gap-1.5"><input type="checkbox" checked id="v-sz-xs" onchange="updateVariantCount()" class="accent-rose-500"> XS</label>
                      <label class="flex items-center gap-1.5"><input type="checkbox" checked id="v-sz-s" onchange="updateVariantCount()" class="accent-rose-500"> S</label>
                      <label class="flex items-center gap-1.5"><input type="checkbox" checked id="v-sz-m" onchange="updateVariantCount()" class="accent-rose-500"> M</label>
                      <label class="flex items-center gap-1.5"><input type="checkbox" checked id="v-sz-l" onchange="updateVariantCount()" class="accent-rose-500"> L</label>
                      <label class="flex items-center gap-1.5"><input type="checkbox" id="v-sz-xl" onchange="updateVariantCount()" class="accent-rose-500"> XL</label>
                      <label class="flex items-center gap-1.5"><input type="checkbox" id="v-sz-xxl" onchange="updateVariantCount()" class="accent-rose-500"> XXL</label>
                    </div>
                  </div>

                  <div class="space-y-1">
                    <span class="text-[10px] text-slate-500 uppercase font-bold block">Fits</span>
                    <div class="flex gap-3">
                      <label class="flex items-center gap-1.5"><input type="checkbox" checked id="v-fit-slim" onchange="updateVariantCount()" class="accent-rose-500"> Slim</label>
                      <label class="flex items-center gap-1.5"><input type="checkbox" id="v-fit-reg" onchange="updateVariantCount()" class="accent-rose-500"> Regular</label>
                    </div>
                  </div>
                </div>

                <div class="space-y-3">
                  <div class="bg-black/30 border border-white/5 rounded-lg p-3 text-center space-y-1">
                    <span class="text-[10px] text-slate-500 block uppercase font-bold">Planned Variant Count</span>
                    <span class="text-2xl font-outfit font-extrabold text-white" id="v-calc-count">8 Variants</span>
                  </div>
                  <button onclick="triggerVariantGeneration()" class="w-full py-2.5 rounded-lg bg-rose-500 hover:bg-rose-600 text-white font-bold text-xs uppercase transition shadow-lg shadow-rose-500/20">Generate Variants Grid</button>
                </div>
              </div>

              <div class="lg:col-span-7 glass-card p-5 rounded-2xl border border-white/5 flex flex-col justify-between min-h-[300px]">
                <div class="space-y-2">
                  <span class="panel-section-title text-indigo-400 font-bold text-sm block">Generated Variant SKU Grid</span>
                  <div class="max-h-[160px] overflow-y-auto w-full border border-white/5 rounded bg-black/20" id="v-list-container">
                    <div class="p-6 text-center text-slate-500 text-xs">Configure parameters and click Generate to build variant grid.</div>
                  </div>
                </div>

                <!-- ROI Time Comparison Widget -->
                <div class="border-t border-white/5 pt-3 mt-3 grid grid-cols-2 gap-4 text-center">
                  <div class="p-2.5 bg-red-950/20 border border-red-500/20 rounded-lg">
                    <span class="text-slate-400 text-[9px] uppercase font-bold block">Manual Creation (120 Variants)</span>
                    <span class="text-base font-bold text-red-400 font-mono">3.0 Hours</span>
                  </div>
                  <div class="p-2.5 bg-emerald-950/20 border border-emerald-500/20 rounded-lg">
                    <span class="text-slate-400 text-[9px] uppercase font-bold block">SMRITI Creation (120 Variants)</span>
                    <span class="text-base font-bold text-emerald-400 font-mono">30 Seconds</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        `
      },
      {
        title: "Garment Matrix",
        html: `
          <div class="max-w-6xl mx-auto space-y-4">
            <div class="text-center space-y-1">
              <span class="text-accent font-bold uppercase tracking-wider text-[10px]">Inventory Matrix</span>
              <h2 class="text-3xl font-outfit font-extrabold text-white">Garment Size Matrix</h2>
              <p class="text-slate-400 text-xs">Manage garment stocks across sizes. Change matrix counts to recalculate style sum total.</p>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 pt-2">
              <div class="lg:col-span-8 glass-card p-5 rounded-2xl border border-white/5">
                <div class="overflow-x-auto w-full">
                  <table class="w-full text-xs border-collapse">
                    <thead>
                      <tr class="border-b border-white/5 text-slate-400">
                        <th class="py-2 text-left">STYLE CODE</th>
                        <th class="py-2 text-center" style="width: 50px;">XS</th>
                        <th class="py-2 text-center" style="width: 50px;">S</th>
                        <th class="py-2 text-center" style="width: 50px;">M</th>
                        <th class="py-2 text-center" style="width: 50px;">L</th>
                        <th class="py-2 text-center" style="width: 50px;">XL</th>
                        <th class="py-2 text-center" style="width: 50px;">XXL</th>
                        <th class="py-2 text-center" style="width: 60px;">TOTAL</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-white/5 text-slate-300">
                      <tr>
                        <td class="py-3 font-semibold text-white">ART-DENIM-BLU-SLIM</td>
                        <td class="py-3 text-center"><input type="number" oninput="calcGarmentMatrix()" id="gmatrix-xs" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="12"></td>
                        <td class="py-3 text-center"><input type="number" oninput="calcGarmentMatrix()" id="gmatrix-s" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="24"></td>
                        <td class="py-3 text-center"><input type="number" oninput="calcGarmentMatrix()" id="gmatrix-m" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="48"></td>
                        <td class="py-3 text-center"><input type="number" oninput="calcGarmentMatrix()" id="gmatrix-l" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="36"></td>
                        <td class="py-3 text-center"><input type="number" oninput="calcGarmentMatrix()" id="gmatrix-xl" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="18"></td>
                        <td class="py-3 text-center"><input type="number" oninput="calcGarmentMatrix()" id="gmatrix-xxl" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="6"></td>
                        <td class="py-3 text-center font-mono font-bold text-rose-400" id="gmatrix-total">144</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <div class="lg:col-span-4 glass-card p-5 rounded-2xl border-l-4 border-rose-500 bg-rose-950/5 flex flex-col justify-center space-y-3">
                <span class="text-[9px] uppercase tracking-wider text-slate-400 font-bold block">Matrix Grid Control</span>
                <h4 class="font-outfit font-bold text-white text-sm">Size-wise Distribution Curve</h4>
                <p class="text-xs text-slate-300 leading-relaxed">Instead of managing 6 separate inventory lines, SMRITI lets you create and view sizes in a single matrix row. Auto-calculated columns ensure zero billing discrepancies.</p>
                <div class="text-[10px] text-emerald-400 font-semibold italic">"One row. Six variants. Accurate counts."</div>
              </div>
            </div>
          </div>
        `
      },
      {
        title: "Footwear Matrix",
        html: `
          <div class="max-w-6xl mx-auto space-y-4">
            <div class="text-center space-y-1">
              <span class="text-accent font-bold uppercase tracking-wider text-[10px]">Footwear Matrix</span>
              <h2 class="text-3xl font-outfit font-extrabold text-white">Footwear Size Matrix</h2>
              <p class="text-slate-400 text-xs">Manage footwear pairs across size options. Change matrix counts to recalculate aggregate stock.</p>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 pt-2">
              <div class="lg:col-span-8 glass-card p-5 rounded-2xl border border-white/5">
                <div class="overflow-x-auto w-full">
                  <table class="w-full text-xs border-collapse">
                    <thead>
                      <tr class="border-b border-white/5 text-slate-400">
                        <th class="py-2 text-left">STYLE CODE</th>
                        <th class="py-2 text-center" style="width: 50px;">6</th>
                        <th class="py-2 text-center" style="width: 50px;">7</th>
                        <th class="py-2 text-center" style="width: 50px;">8</th>
                        <th class="py-2 text-center" style="width: 50px;">9</th>
                        <th class="py-2 text-center" style="width: 50px;">10</th>
                        <th class="py-2 text-center" style="width: 50px;">11</th>
                        <th class="py-2 text-center" style="width: 60px;">TOTAL</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-white/5 text-slate-300">
                      <tr>
                        <td class="py-3 font-semibold text-white">ART-SNEAK-BLK-MID</td>
                        <td class="py-3 text-center"><input type="number" oninput="calcFootwearMatrix()" id="fmatrix-6" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="5"></td>
                        <td class="py-3 text-center"><input type="number" oninput="calcFootwearMatrix()" id="fmatrix-7" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="10"></td>
                        <td class="py-3 text-center"><input type="number" oninput="calcFootwearMatrix()" id="fmatrix-8" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="20"></td>
                        <td class="py-3 text-center"><input type="number" oninput="calcFootwearMatrix()" id="fmatrix-9" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="15"></td>
                        <td class="py-3 text-center"><input type="number" oninput="calcFootwearMatrix()" id="fmatrix-10" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="8"></td>
                        <td class="py-3 text-center"><input type="number" oninput="calcFootwearMatrix()" id="fmatrix-11" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="2"></td>
                        <td class="py-3 text-center font-mono font-bold text-rose-400" id="fmatrix-total">60</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <div class="lg:col-span-4 glass-card p-5 rounded-2xl border-l-4 border-rose-500 bg-rose-950/5 flex flex-col justify-center space-y-3">
                <span class="text-[9px] uppercase tracking-wider text-slate-400 font-bold block">Size Curve Analytics</span>
                <h4 class="font-outfit font-bold text-white text-sm">Shoe Size Distribution</h4>
                <p class="text-xs text-slate-300 leading-relaxed">Footwear sizing patterns require high visibility. SMRITI shows the shoe-size matrix in a single integrated view, reducing stock intake registration time by 75%.</p>
                <div class="text-[10px] text-emerald-400 font-semibold italic">"Size curves mapped to barcodes."</div>
              </div>
            </div>
          </div>
        `
      },
      {
        title: "Pricing Governance",
        html: `
          <div class="max-w-6xl mx-auto space-y-4">
            <div class="text-center space-y-1">
              <span class="text-accent font-bold uppercase tracking-wider text-[10px]">Margin Protection</span>
              <h2 class="text-3xl font-outfit font-extrabold text-white">Pricing Governance</h2>
              <p class="text-slate-400 text-xs">Enforce strict price list governance rules to prevent pricing disputes and cashier margin leakages.</p>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-4 gap-4 pt-2">
              <div class="glass-card p-4 rounded-xl border border-white/5 space-y-2">
                <span class="text-[9px] uppercase tracking-wider text-slate-500 font-bold block">MRP Matrix</span>
                <h4 class="font-outfit font-bold text-white text-sm">Maximum Retail Price</h4>
                <p class="text-xs text-slate-400 leading-relaxed">Establish base MRP limits for products. The printed barcode tags reflect the MRP to ensure regulatory compliance.</p>
              </div>

              <div class="glass-card p-4 rounded-xl border border-white/5 space-y-2">
                <span class="text-[9px] uppercase tracking-wider text-slate-500 font-bold block">Selling Price List</span>
                <h4 class="font-outfit font-bold text-white text-sm">Selling Price Governance</h4>
                <p class="text-xs text-slate-400 leading-relaxed">Governs the actual checkout lane price. Prevents cashiers from editing pricing fields manually unless supervisor overrides are authorized.</p>
              </div>

              <div class="glass-card p-4 rounded-xl border border-white/5 space-y-2">
                <span class="text-[9px] uppercase tracking-wider text-slate-500 font-bold block">Margin Guard</span>
                <h4 class="font-outfit font-bold text-white text-sm">Margin Protection Limits</h4>
                <p class="text-xs text-slate-400 leading-relaxed">Enforces minimum gross profit margin locks. If a discount scheme drops the margin below limits, SMRITI blocks the transaction.</p>
              </div>

              <div class="glass-card p-4 rounded-xl border border-white/5 space-y-2">
                <span class="text-[9px] uppercase tracking-wider text-slate-500 font-bold block">Promotional Pricing</span>
                <h4 class="font-outfit font-bold text-white text-sm">Scheme &amp; Offer Controls</h4>
                <p class="text-xs text-slate-400 leading-relaxed">Syncs campaign and scheme discounts automatically to checkouts, preventing cashier discounts fraud.</p>
              </div>
            </div>
          </div>
        `
      },
      {
        title: "Catalog Completeness Meter",
        html: `
          <div class="max-w-6xl mx-auto space-y-4">
            <div class="text-center space-y-1">
              <span class="text-accent font-bold uppercase tracking-wider text-[10px]">Data Quality</span>
              <h2 class="text-3xl font-outfit font-extrabold text-white">Catalog Completeness Meter</h2>
              <p class="text-slate-400 text-xs">Measure catalog content quality. Toggle checklist parameters to dynamically calculate Catalog Completeness Score.</p>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 pt-2">
              <div class="lg:col-span-5 glass-card p-5 rounded-2xl border border-white/5 space-y-3.5 flex flex-col justify-between">
                <div class="space-y-3">
                  <span class="panel-section-title text-rose-400 font-bold text-sm block">Data Elements Checklist</span>
                  <div class="space-y-2 text-xs text-slate-300">
                    <label class="flex items-center justify-between p-2 rounded bg-slate-950 border border-white/5">
                      <span>🖼️ Product Images Uploaded (100% complete)</span>
                      <input type="checkbox" checked id="comp-img" onchange="calcCompleteness()" class="accent-rose-500">
                    </label>
                    <label class="flex items-center justify-between p-2 rounded bg-slate-950 border border-white/5">
                      <span>📝 Detailed Descriptions (90% complete)</span>
                      <input type="checkbox" checked id="comp-desc" onchange="calcCompleteness()" class="accent-rose-500">
                    </label>
                    <label class="flex items-center justify-between p-2 rounded bg-slate-950 border border-white/5">
                      <span>📏 Size Grid Mappings (100% complete)</span>
                      <input type="checkbox" checked id="comp-size" onchange="calcCompleteness()" class="accent-rose-500">
                    </label>
                    <label class="flex items-center justify-between p-2 rounded bg-slate-950 border border-white/5">
                      <span>🏷️ Category &amp; Attribute Tags (55% complete)</span>
                      <input type="checkbox" id="comp-attr" onchange="calcCompleteness()" class="accent-rose-500">
                    </label>
                  </div>
                </div>
              </div>

              <div class="lg:col-span-7 glass-card p-5 rounded-2xl border border-white/5 flex flex-col justify-center items-center text-center space-y-4">
                <div class="text-[10px] text-slate-500 uppercase font-bold tracking-wider">Overall Catalog Quality Score</div>
                <div class="w-32 h-32 rounded-full border-8 border-rose-500/20 flex items-center justify-center relative bg-rose-950/5 shadow-lg shadow-rose-500/5 transition-all duration-300" id="comp-score-circle">
                  <span class="text-4xl font-outfit font-extrabold text-white" id="comp-score-text">86%</span>
                </div>
                <div class="space-y-1">
                  <span class="text-xs font-bold text-white" id="comp-badge-text">Catalog Status: Good</span>
                  <p class="text-[10px] text-slate-400 max-w-sm" id="comp-desc-text">Minimum operational quality met. Complete attribute mappings to maximize searchability and reporting accuracy.</p>
                </div>
              </div>
            </div>
          </div>
        `
      },
      {
        title: "Bulk Import Experience",
        html: `
          <div class="max-w-6xl mx-auto space-y-4">
            <div class="text-center space-y-1">
              <span class="text-accent font-bold uppercase tracking-wider text-[10px]">Data Loading</span>
              <h2 class="text-3xl font-outfit font-extrabold text-white">Bulk Import Experience</h2>
              <p class="text-slate-400 text-xs">Simulate importing catalog sheets with automatic validation checks and duplicate detection.</p>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 pt-2">
              <div class="glass-card p-5 rounded-2xl border-l-4 border-amber-500 bg-amber-950/5 space-y-2">
                <h4 class="font-outfit font-bold text-white text-sm">📋 Validation Checks</h4>
                <p class="text-xs text-slate-400 leading-relaxed">Auto-scans spreadsheet columns for missing sizes, invalid prices, or blank style codes, flagging rows in red before committing.</p>
              </div>

              <div class="glass-card p-5 rounded-2xl border-l-4 border-emerald-500 bg-emerald-950/5 space-y-2">
                <h4 class="font-outfit font-bold text-white text-sm">🛡️ Duplicate Detection</h4>
                <p class="text-xs text-slate-400 leading-relaxed">Compares incoming barcodes and styles against current records, preventing twin data rows from splitting sales history.</p>
              </div>

              <div class="glass-card p-5 rounded-2xl border-l-4 border-indigo-500 bg-indigo-950/5 space-y-2">
                <h4 class="font-outfit font-bold text-white text-sm">🔍 Data Quality Review</h4>
                <p class="text-xs text-slate-400 leading-relaxed">Enables managers to review a preview of clean rows vs failed rows, approving the import only when anomalies are resolved.</p>
              </div>
            </div>
          </div>
        `
      },
      {
        title: "Item Quality Auditor",
        html: `
          <div class="max-w-6xl mx-auto space-y-4">
            <div class="text-center space-y-1">
              <span class="text-accent font-bold uppercase tracking-wider text-[10px]">Data Quality Auditor</span>
              <h2 class="text-3xl font-outfit font-extrabold text-white">Item Quality Auditor</h2>
              <p class="text-slate-400 text-xs">Run automated item audits to inspect catalog anomalies. Click any alert trigger to review severity and correction steps.</p>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 pt-2">
              <div class="lg:col-span-8 glass-card p-5 rounded-2xl border border-white/5">
                <div class="overflow-x-auto w-full">
                  <table class="w-full text-xs border-collapse">
                    <thead>
                      <tr class="border-b border-white/5 text-slate-400">
                        <th class="py-2 text-left">ANOMALY DETECTED</th>
                        <th class="py-2 text-center">SEVERITY</th>
                        <th class="py-2 text-center">AFFECTED SKUS</th>
                        <th class="py-2 text-center">ACTION</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-white/5 text-slate-300">
                      <tr onclick="showAuditAnomalyDetails('image')" class="hover:bg-white/5 transition cursor-pointer">
                        <td class="py-3 font-semibold text-white">Missing Product Images</td>
                        <td class="py-3 text-center"><span class="px-2 py-0.5 rounded text-[9px] font-bold uppercase bg-amber-500/10 text-amber-400">Medium</span></td>
                        <td class="py-3 text-center font-mono">14 SKUs</td>
                        <td class="py-3 text-center text-rose-400 font-bold hover:underline">Inspect →</td>
                      </tr>
                      <tr onclick="showAuditAnomalyDetails('category')" class="hover:bg-white/5 transition cursor-pointer">
                        <td class="py-3 font-semibold text-white">Missing Category Assignments</td>
                        <td class="py-3 text-center"><span class="px-2 py-0.5 rounded text-[9px] font-bold uppercase bg-orange-500/10 text-orange-400">High</span></td>
                        <td class="py-3 text-center font-mono">4 SKUs</td>
                        <td class="py-3 text-center text-rose-400 font-bold hover:underline">Inspect →</td>
                      </tr>
                      <tr onclick="showAuditAnomalyDetails('price')" class="hover:bg-white/5 transition cursor-pointer">
                        <td class="py-3 font-semibold text-white">Missing Price List Entries</td>
                        <td class="py-3 text-center"><span class="px-2 py-0.5 rounded text-[9px] font-bold uppercase bg-red-500/10 text-red-400">Critical</span></td>
                        <td class="py-3 text-center font-mono">2 SKUs</td>
                        <td class="py-3 text-center text-rose-400 font-bold hover:underline">Inspect →</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <div id="item-audit-detail-box" class="lg:col-span-4 glass-card p-5 rounded-2xl border-l-4 border-rose-500 bg-rose-950/5 flex flex-col justify-center min-h-[160px]">
                <div id="item-audit-detail-content" class="text-xs text-slate-300">
                  Click any anomaly row on the table to inspect data severity and immediate recovery guidelines.
                </div>
              </div>
            </div>
          </div>
        `
      },
      {
        title: "Product Health Dashboard",
        html: `
          <div class="max-w-6xl mx-auto space-y-4">
            <div class="text-center space-y-1">
              <span class="text-accent font-bold uppercase tracking-wider text-[10px]">Product Health</span>
              <h2 class="text-3xl font-outfit font-extrabold text-white">Product Health Dashboard</h2>
              <p class="text-slate-400 text-xs">Monitor inventory health and catalog movement statuses. Click tabs to inspect SKU listings.</p>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 pt-2">
              <div class="lg:col-span-4 space-y-2.5">
                <button onclick="setProductHealthTab('active')" id="phealth-tab-active" class="w-full text-left p-3 rounded-lg border transition bg-accent text-white border-accent flex justify-between items-center" style="background-color: var(--accent); border-color: var(--accent);">
                  <span>🟢 Active (Healthy)</span><span>→</span>
                </button>
                <button onclick="setProductHealthTab('dormant')" id="phealth-tab-dormant" class="w-full text-left p-3 rounded-lg border transition bg-slate-900/40 border-white/5 text-slate-400 hover:text-white flex justify-between items-center">
                  <span>🟡 Dormant (Needs Attention)</span><span>→</span>
                </button>
                <button onclick="setProductHealthTab('slow')" id="phealth-tab-slow" class="w-full text-left p-3 rounded-lg border transition bg-slate-900/40 border-white/5 text-slate-400 hover:text-white flex justify-between items-center">
                  <span>🟠 Slow Moving (Action Rec.)</span><span>→</span>
                </button>
                <button onclick="setProductHealthTab('never')" id="phealth-tab-never" class="w-full text-left p-3 rounded-lg border transition bg-slate-900/40 border-white/5 text-slate-400 hover:text-white flex justify-between items-center">
                  <span>🔴 Never Sold (Investigate)</span><span>→</span>
                </button>
              </div>

              <div class="lg:col-span-8 glass-card p-5 rounded-2xl border border-white/5 min-h-[220px] flex flex-col justify-between">
                <div class="space-y-3">
                  <h3 class="text-base font-outfit font-bold text-white" id="phealth-title">Active Items</h3>
                  <div class="overflow-x-auto w-full">
                    <table class="w-full text-[11px] border-collapse" id="phealth-table">
                      <thead>
                        <tr class="border-b border-white/5 text-slate-500">
                          <th class="py-1.5 text-left">SKU CODE</th>
                          <th class="py-1.5 text-left">ARTICLE NAME</th>
                          <th class="py-1.5 text-right">STOCK</th>
                          <th class="py-1.5 text-right">VELOCITY</th>
                        </tr>
                      </thead>
                      <tbody class="divide-y divide-white/5 text-slate-300">
                        <tr>
                          <td class="py-1.5 font-mono text-white">ART-DENIM-BLU-32</td>
                          <td class="py-1.5">Slim Fit Denim Blue</td>
                          <td class="py-1.5 text-right">144 pcs</td>
                          <td class="py-1.5 text-right font-bold text-emerald-400">12.5 pcs/day</td>
                        </tr>
                        <tr>
                          <td class="py-1.5 font-mono text-white">ART-SNEAK-BLK-09</td>
                          <td class="py-1.5">Sport Sneakers Black</td>
                          <td class="py-1.5 text-right">60 pairs</td>
                          <td class="py-1.5 text-right font-bold text-emerald-400">8.2 pairs/day</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
                <div class="text-[10px] text-slate-500 border-t border-white/5 pt-2 mt-2" id="phealth-tip">Active products have regular sales transactions and correct master codes.</div>
              </div>
            </div>
          </div>
        `
      },
      {
        title: "Business Impact Calculator",
        html: `
          <div class="max-w-6xl mx-auto space-y-4">
            <div class="text-center space-y-1">
              <span class="text-accent font-bold uppercase tracking-wider text-[10px]">Return on Investment</span>
              <h2 class="text-3xl font-outfit font-extrabold text-white">Cost of Bad Data Calculator</h2>
              <p class="text-slate-400 text-xs">Evaluate annual profit leakages caused by incorrect size, price, or duplicate records in catalog.</p>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 pt-2">
              <div class="lg:col-span-5 glass-card p-5 rounded-2xl border border-white/5 space-y-4">
                <div class="panel-section-title text-rose-400 font-bold text-sm">Store &amp; Catalog Parameters</div>
                <div class="space-y-4">
                  <div class="space-y-1">
                    <div class="flex justify-between text-[11px] text-slate-400 font-bold">
                      <span>CATALOG SIZE (SKUS)</span>
                      <span id="roi-cat-size-val" class="text-white">1,500</span>
                    </div>
                    <input type="range" id="input-roi-cat-size" min="500" max="10000" step="500" value="1500" oninput="calcItemMasterRoi()" class="w-full accent-rose-500 bg-slate-900 border border-white/5 rounded-lg h-2">
                  </div>
                  <div class="space-y-1">
                    <div class="flex justify-between text-[11px] text-slate-400 font-bold">
                      <span>DATA ERROR RATE (%)</span>
                      <span id="roi-cat-err-val" class="text-white">4%</span>
                    </div>
                    <input type="range" id="input-roi-cat-err" min="1" max="15" step="1" value="4" oninput="calcItemMasterRoi()" class="w-full accent-rose-500 bg-slate-900 border border-white/5 rounded-lg h-2">
                  </div>
                  <div class="space-y-1">
                    <div class="flex justify-between text-[11px] text-slate-400 font-bold">
                      <span>MONTHLY TRANSACTIONS</span>
                      <span id="roi-cat-trans-val" class="text-white">5,000</span>
                    </div>
                    <input type="range" id="input-roi-cat-trans" min="1000" max="20000" step="1000" value="5000" oninput="calcItemMasterRoi()" class="w-full accent-rose-500 bg-slate-900 border border-white/5 rounded-lg h-2">
                  </div>
                </div>
              </div>

              <div class="lg:col-span-7 grid grid-cols-2 gap-4">
                <div class="glass-card p-4 rounded-xl border border-white/5 flex flex-col justify-center text-center">
                  <span class="text-slate-400 text-[10px] uppercase font-bold block">Annual Billing Errors</span>
                  <div class="text-2xl font-outfit font-extrabold text-rose-400 mt-1" id="roi-cat-billing-err">2,400 Items</div>
                  <span class="text-[9px] text-slate-500 mt-0.5 block">Estimated pricing discrepancies</span>
                </div>
                <div class="glass-card p-4 rounded-xl border border-white/5 flex flex-col justify-center text-center">
                  <span class="text-slate-400 text-[10px] uppercase font-bold block">Inventory Variance Risk</span>
                  <div class="text-2xl font-outfit font-extrabold text-rose-400 mt-1" id="roi-cat-inv-err">60 SKUs</div>
                  <span class="text-[9px] text-slate-500 mt-0.5 block">Split/Duplicate records risk</span>
                </div>
                <div class="glass-card p-4 rounded-xl border border-white/5 flex flex-col justify-center text-center col-span-2 bg-rose-950/10 border-rose-500/20">
                  <span class="text-slate-400 text-[10px] uppercase font-bold block">Estimated Revenue Leakage Risk</span>
                  <div class="text-3xl font-outfit font-extrabold text-emerald-400 mt-1" id="roi-cat-revenue-leak">₹1,20,000</div>
                  <span class="text-[9px] text-slate-400 mt-0.5 block">Yearly margin lost to wrong price checkouts and returns processing</span>
                </div>
              </div>
            </div>
          </div>
        `
      },
      {
        title: "Why Teams Choose Item Master Studio",
        html: `
          <div class="max-w-6xl mx-auto space-y-4">
            <div class="text-center space-y-1">
              <span class="text-accent font-bold uppercase tracking-wider text-[10px]">Business Outcomes</span>
              <h2 class="text-3xl font-outfit font-extrabold text-white">Why Teams Choose Item Master Studio</h2>
              <p class="text-slate-400 text-xs">The foundational engine that drives SMRITI Retail OS accuracy.</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 pt-2">
              <div class="glass-card p-5 rounded-2xl border border-white/5 space-y-2">
                <span class="text-rose-400 text-lg">📁</span>
                <h4 class="font-outfit font-bold text-white text-base">Cleaner Product Catalog</h4>
                <p class="text-xs text-slate-400 leading-relaxed">No duplicate entries, correct size matrices, and structured attribute categories.</p>
              </div>

              <div class="glass-card p-5 rounded-2xl border border-white/5 space-y-2">
                <span class="text-rose-400 text-lg">📊</span>
                <h4 class="font-outfit font-bold text-white text-base">Better Reporting Accuracy</h4>
                <p class="text-xs text-slate-400 leading-relaxed">Clear sales velocity metrics grouped by category, season, or customer gender profile.</p>
              </div>

              <div class="glass-card p-5 rounded-2xl border border-white/5 space-y-2">
                <span class="text-rose-400 text-lg">⚡</span>
                <h4 class="font-outfit font-bold text-white text-base">Faster Product Launches</h4>
                <p class="text-xs text-slate-400 leading-relaxed">Generate 120 size-color variants in 30 seconds rather than 3 hours of manual typing.</p>
              </div>

              <div class="glass-card p-5 rounded-2xl border border-white/5 space-y-2">
                <span class="text-rose-400 text-lg">🛡️</span>
                <h4 class="font-outfit font-bold text-white text-base">Perfect Inventory Control</h4>
                <p class="text-xs text-slate-400 leading-relaxed">Correct barcodes link stock ledger transactions to size curves, eliminating variances.</p>
              </div>

              <div class="glass-card p-5 rounded-2xl border border-white/5 space-y-2">
                <span class="text-rose-400 text-lg">🔮</span>
                <h4 class="font-outfit font-bold text-white text-base">Intelligent Forecasting</h4>
                <p class="text-xs text-slate-400 leading-relaxed">Complete data tags support accurate Weeks of Cover (WOC) models and replenishment signals.</p>
              </div>

              <div class="glass-card p-5 rounded-2xl border border-white/5 space-y-2 bg-rose-950/10 border-rose-500/20 flex flex-col justify-center">
                <span class="text-rose-400 text-lg">🏆</span>
                <h4 class="font-outfit font-bold text-white text-base">Foundation Completed</h4>
                <p class="text-xs text-slate-300 leading-relaxed font-medium">Accurate master data enables billing speed, printing precision, and warehouse control.</p>
              </div>
            </div>
          </div>
        `
      },
      {
        title: "Thank You",
        html: `
          <div class="max-w-4xl mx-auto text-center space-y-6">
            <h1 class="text-5xl font-outfit font-extrabold text-white">Thank <span class="text-accent">You</span></h1>
            <p class="text-base text-slate-300">Establish the perfect data foundation with SMRITI Item Master Studio.</p>
            
            <div class="glass-card max-w-lg mx-auto p-5 rounded-2xl border-accent space-y-4 text-xs">
              <div class="border-b border-white/5 pb-2 text-slate-400 font-bold uppercase tracking-wider">AITDL Founder Commitment</div>
              <div class="flex flex-col md:flex-row items-center gap-4 text-left">
                <div class="w-16 h-16 rounded-full bg-slate-900 border border-rose-500/30 flex items-center justify-center text-2xl">👨‍💼</div>
                <div class="space-y-1">
                  <p class="text-sm font-bold text-white">Jawahar R. Mallah</p>
                  <p class="text-[10px] text-slate-400">Founder &amp; Chief Architect, AITDL</p>
                  <p class="text-[10px] text-slate-500 leading-relaxed">"SMRITI is designed on a single tenet: software should explain its decisions. Every metric, health score, and forecast must be auditable by non-technical store owners."</p>
                </div>
              </div>
              <p class="text-[10px] text-accent font-bold italic mt-2">"Light begins with learning." — Jawahar R. Mallah</p>
            </div>
            
            <div class="pt-4 flex justify-center gap-4">
              <button onclick="goToSlide(0)" class="px-5 py-2.5 rounded-lg border border-rose-500 text-rose-400 hover:bg-rose-500 hover:text-white transition font-bold text-xs uppercase">Restart Presentation</button>
              <button onclick="exitDeck()" class="px-5 py-2.5 rounded-lg bg-rose-500 hover:bg-rose-600 text-white transition font-bold text-xs uppercase">Exit Suite</button>
            </div>
          </div>
        `
      }
    ];
"""

# Insert SLIDES_ITEMMASTER right before // Presentation HUD variables
hud_vars_line = "    // Presentation HUD variables"
if "const SLIDES_ITEMMASTER =" not in content:
    content = content.replace(hud_vars_line, slides_itemmaster_def + "\n\n" + hud_vars_line)

# 5. Append JS functions at the end of the script tag
itemmaster_js_funcs = """
    // Item Master Slide 2: Data Quality Objections
    function showItemObjectionDetails(issue) {
      const textEl = document.getElementById('item-obj-detail-content');
      const box = document.getElementById('item-obj-detail-box');
      if (!textEl || !box) return;
      box.classList.remove('hidden');

      const tabs = ['size', 'price', 'category', 'image', 'duplicate'];
      tabs.forEach(t => {
        const card = document.getElementById(`item-obj-tab-${t}`);
        if (card) {
          if (t === issue) {
            card.className = "glass-card p-3 rounded-xl border border-rose-500/80 bg-rose-950/20 scale-[1.02] transition cursor-pointer text-center space-y-1 flex flex-col justify-center min-h-[95px]";
          } else {
            card.className = "glass-card p-3 rounded-xl border border-white/5 hover:border-rose-500/40 hover:scale-[1.02] transition cursor-pointer text-center space-y-1 flex flex-col justify-center min-h-[95px]";
          }
        }
      });

      const details = {
        size: {
          title: "Catalog Issue: Wrong Size Mapping",
          impact: "Incorrect size labels on tags lead to wrong cashier billing, higher return rates, and stock count variances.",
          path: "Wrong Size Tag → Incorrect billing → Returns → Customer dissatisfaction.",
          mitigation: "SMRITI checks size variations against parent-style matrix curves before barcode creation."
        },
        price: {
          title: "Catalog Issue: Wrong Price Assigned",
          impact: "Cashiers bill items with wrong prices, leading to immediate profit leakage or customer pricing disputes at checkout lanes.",
          path: "Price typo in catalog → Wrong cashier checkout → Margin loss or customer dispute.",
          mitigation: "SMRITI enforces automated price validation checks, checking margins before approving price lists."
        },
        category: {
          title: "Catalog Issue: Wrong Category Classification",
          impact: "Inaccurate category assignment leads to distorted sales reports, corrupting stock planning models.",
          path: "Product misclassified → Distorted category reports → Bad purchase orders → Excess stock.",
          mitigation: "SMRITI requires department-to-category validation checks on saving new articles."
        },
        image: {
          title: "Catalog Issue: Missing Catalog Images",
          impact: "E-commerce channels and store sales displays cannot visual-match items, causing cashier scan errors.",
          path: "No photo in catalog → Cashier cannot visual-verify product → Wrong variant selected → Inventory mismatch.",
          mitigation: "SMRITI flags products missing images in the quality scorecard, prompting image uploads."
        },
        duplicate: {
          title: "Catalog Issue: Duplicate Product Entries",
          impact: "Duplicate items created for the same product split stock counts and histories, rendering reports useless.",
          path: "Twin product records → Split sales data → Distorted demand calculations → Bad business decisions.",
          mitigation: "SMRITI checks style codes and barcode fields dynamically to prevent duplicate registrations."
        }
      };

      const data = details[issue];
      if (data) {
        textEl.innerHTML = `
          <div class="space-y-3">
            <h4 class="font-outfit font-bold text-white text-sm border-b border-white/5 pb-1 flex items-center gap-2">
              <span class="text-rose-400">⚠️</span> ${data.title}
            </h4>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
              <div>
                <span class="text-rose-400 font-bold block">Business Impact:</span>
                <p class="text-slate-300 mt-0.5">${data.impact}</p>
              </div>
              <div>
                <span class="text-red-400 font-bold block">Operational Path:</span>
                <p class="text-slate-300 mt-0.5">${data.path}</p>
              </div>
              <div>
                <span class="text-emerald-400 font-bold block">SMRITI Mitigation:</span>
                <p class="text-slate-300 mt-0.5">${data.mitigation}</p>
              </div>
            </div>
          </div>
        `;
      }
    }

    // Item Master Slide 5: Preset Variant Generator JS
    function updateVariantCount() {
      const colors = ['blue', 'black', 'grey'].filter(c => document.getElementById(`v-col-${c}`).checked).length;
      const sizes = ['xs', 's', 'm', 'l', 'xl', 'xxl'].filter(s => document.getElementById(`v-sz-${s}`).checked).length;
      const fits = ['slim', 'reg'].filter(f => document.getElementById(`v-fit-${f}`).checked).length;
      
      const total = colors * sizes * fits;
      document.getElementById('v-calc-count').textContent = `${total} Variants`;
    }

    function triggerVariantGeneration() {
      const colors = ['blue', 'black', 'grey'].filter(c => document.getElementById(`v-col-${c}`).checked);
      const sizes = ['xs', 's', 'm', 'l', 'xl', 'xxl'].filter(s => document.getElementById(`v-sz-${s}`).checked);
      const fits = ['slim', 'reg'].filter(f => document.getElementById(`v-fit-${f}`).checked);
      const container = document.getElementById('v-list-container');
      if (!container) return;

      if (colors.length === 0 || sizes.length === 0 || fits.length === 0) {
        container.innerHTML = `<div class="p-6 text-center text-red-400 text-xs">Error: Select at least one color, size, and fit.</div>`;
        return;
      }

      let html = '<table class="w-full text-[10px] border-collapse"><thead class="border-b border-white/5 text-slate-500 bg-black/10"><tr><th class="p-2 text-left">SKU CODE</th><th class="p-2 text-left">COLOR</th><th class="p-2 text-left">SIZE</th><th class="p-2 text-left">FIT</th><th class="p-2 text-right">BARCODE</th></tr></thead><tbody class="divide-y divide-white/5 text-slate-300">';
      let codeBase = 890332211000;
      let count = 0;
      
      colors.forEach(col => {
        sizes.forEach(sz => {
          fits.forEach(fit => {
            count++;
            const sku = `ART-DENIM-${col.substring(0,3).toUpperCase()}-${sz.toUpperCase()}-${fit.substring(0,3).toUpperCase()}`;
            const barcode = codeBase + count;
            html += `<tr>
              <td class="p-2 font-mono font-bold text-white">${sku}</td>
              <td class="p-2 uppercase">${col}</td>
              <td class="p-2 uppercase">${sz}</td>
              <td class="p-2 uppercase">${fit}</td>
              <td class="p-2 text-right font-mono text-cyan-400">${barcode}</td>
            </tr>`;
          });
        });
      });
      html += '</tbody></table>';
      container.innerHTML = html;
    }

    // Item Master Slide 6: Garment Size Matrix
    function calcGarmentMatrix() {
      const xs = parseInt(document.getElementById('gmatrix-xs').value) || 0;
      const s = parseInt(document.getElementById('gmatrix-s').value) || 0;
      const m = parseInt(document.getElementById('gmatrix-m').value) || 0;
      const l = parseInt(document.getElementById('gmatrix-l').value) || 0;
      const xl = parseInt(document.getElementById('gmatrix-xl').value) || 0;
      const xxl = parseInt(document.getElementById('gmatrix-xxl').value) || 0;
      
      const total = xs + s + m + l + xl + xxl;
      document.getElementById('gmatrix-total').textContent = total;
    }

    // Item Master Slide 7: Footwear Size Matrix
    function calcFootwearMatrix() {
      const f6 = parseInt(document.getElementById('fmatrix-6').value) || 0;
      const f7 = parseInt(document.getElementById('fmatrix-7').value) || 0;
      const f8 = parseInt(document.getElementById('fmatrix-8').value) || 0;
      const f9 = parseInt(document.getElementById('fmatrix-9').value) || 0;
      const f10 = parseInt(document.getElementById('fmatrix-10').value) || 0;
      const f11 = parseInt(document.getElementById('fmatrix-11').value) || 0;
      
      const total = f6 + f7 + f8 + f9 + f10 + f11;
      document.getElementById('fmatrix-total').textContent = total;
    }

    // Item Master Slide 9: Catalog Completeness
    function calcCompleteness() {
      const img = document.getElementById('comp-img').checked ? 29 : 0;
      const desc = document.getElementById('comp-desc').checked ? 27 : 0;
      const size = document.getElementById('comp-size').checked ? 30 : 0;
      const attr = document.getElementById('comp-attr').checked ? 14 : 0;
      
      const total = img + desc + size + attr;
      document.getElementById('comp-score-text').textContent = `${total}%`;
      
      const scoreCircle = document.getElementById('comp-score-circle');
      const badgeText = document.getElementById('comp-badge-text');
      const descText = document.getElementById('comp-desc-text');
      
      if (total >= 90) {
        badgeText.textContent = "Catalog Status: Excellent";
        badgeText.className = "text-xs font-bold text-emerald-400";
        descText.textContent = "High-quality master catalog. Supports accurate inventory analytics and search classifications.";
        if (scoreCircle) scoreCircle.className = "w-32 h-32 rounded-full border-8 border-emerald-500/80 flex items-center justify-center relative bg-emerald-950/5 shadow-lg shadow-emerald-500/10 transition-all duration-300";
      } else if (total >= 70) {
        badgeText.textContent = "Catalog Status: Good";
        badgeText.className = "text-xs font-bold text-white";
        descText.textContent = "Minimum operational quality met. Complete attribute mappings to maximize searchability and reporting accuracy.";
        if (scoreCircle) scoreCircle.className = "w-32 h-32 rounded-full border-8 border-rose-500/40 flex items-center justify-center relative bg-rose-950/5 shadow-lg shadow-rose-500/5 transition-all duration-300";
      } else {
        badgeText.textContent = "Catalog Status: Critical Needs Attention";
        badgeText.className = "text-xs font-bold text-red-400";
        descText.textContent = "Low completeness. Missing fields may cause barcode printing halts and cashier lane classification errors.";
        if (scoreCircle) scoreCircle.className = "w-32 h-32 rounded-full border-8 border-red-500/80 flex items-center justify-center relative bg-red-950/5 shadow-lg shadow-red-500/10 transition-all duration-300";
      }
    }

    // Item Master Slide 11: Anomaly Details
    function showAuditAnomalyDetails(anomaly) {
      const textEl = document.getElementById('item-audit-detail-content');
      if (!textEl) return;

      const details = {
        image: {
          title: "Anomaly: Missing Product Images",
          severity: "Medium",
          impact: "Limits cashiers from visually matching products during scanning at POS checkout lanes.",
          recovery: "Export the list of 14 SKUs and upload JPEG file attachments to complete catalog profiles."
        },
        category: {
          title: "Anomaly: Missing Category Assignments",
          severity: "High",
          impact: "Skewed tax reports and inaccurate sales analytics for departments.",
          recovery: "Open bulk editing grid and select valid categories for the 4 affected style records."
        },
        price: {
          title: "Anomaly: Missing Price List Entries",
          severity: "Critical",
          impact: "Blocks cashiers from billing these items. Checkout scan will return zero value errors.",
          recovery: "Set selling prices in standard price list immediately to authorize billing."
        }
      };

      const data = details[anomaly];
      if (data) {
        textEl.innerHTML = `
          <div class="space-y-3">
            <h4 class="font-outfit font-bold text-white text-sm border-b border-white/5 pb-1">
              ${data.title}
            </h4>
            <div class="space-y-2 text-xs">
              <div><span class="text-rose-400 font-bold block">Severity Level:</span> <span class="text-white">${data.severity}</span></div>
              <div><span class="text-rose-400 font-bold block">Operational Risk:</span> <span class="text-slate-300">${data.impact}</span></div>
              <div><span class="text-emerald-400 font-bold block">Correction Steps:</span> <span class="text-slate-300">${data.recovery}</span></div>
            </div>
          </div>
        `;
      }
    }

    // Item Master Slide 12: Product Health Dashboard Tabs
    function setProductHealthTab(tab) {
      const tabs = ['active', 'dormant', 'slow', 'never'];
      tabs.forEach(t => {
        const btn = document.getElementById(`phealth-tab-${t}`);
        if (btn) {
          if (t === tab) {
            btn.className = "w-full text-left p-3 rounded-lg border transition bg-accent text-white border-accent flex justify-between items-center";
            btn.style.backgroundColor = 'var(--accent)';
            btn.style.borderColor = 'var(--accent)';
          } else {
            btn.className = "w-full text-left p-3 rounded-lg border transition bg-slate-900/40 border-white/5 text-slate-400 hover:text-white flex justify-between items-center";
            btn.style.backgroundColor = '';
            btn.style.borderColor = '';
          }
        }
      });

      const titleEl = document.getElementById('phealth-title');
      const tableEl = document.getElementById('phealth-table');
      const tipEl = document.getElementById('phealth-tip');
      if (!titleEl || !tableEl || !tipEl) return;

      const data = {
        active: {
          title: "Active (Healthy)",
          tip: "Active products have regular sales transactions and correct master codes.",
          rows: `
            <thead><tr class="border-b border-white/5 text-slate-500"><th class="py-1.5 text-left">SKU CODE</th><th class="py-1.5 text-left">ARTICLE NAME</th><th class="py-1.5 text-right">STOCK</th><th class="py-1.5 text-right">VELOCITY</th></tr></thead>
            <tbody class="divide-y divide-white/5 text-slate-300">
              <tr><td class="py-1.5 font-mono text-white">ART-DENIM-BLU-32</td><td class="py-1.5">Slim Fit Denim Blue</td><td class="py-1.5 text-right">144 pcs</td><td class="py-1.5 text-right font-bold text-emerald-400">12.5 pcs/day</td></tr>
              <tr><td class="py-1.5 font-mono text-white">ART-SNEAK-BLK-09</td><td class="py-1.5">Sport Sneakers Black</td><td class="py-1.5 text-right">60 pairs</td><td class="py-1.5 text-right font-bold text-emerald-400">8.2 pairs/day</td></tr>
            </tbody>
          `
        },
        dormant: {
          title: "Dormant (Needs Attention)",
          tip: "Dormant products have stock but zero transactions in the last 45+ days. Action: check price setups.",
          rows: `
            <thead><tr class="border-b border-white/5 text-slate-500"><th class="py-1.5 text-left">SKU CODE</th><th class="py-1.5 text-left">ARTICLE NAME</th><th class="py-1.5 text-right">STOCK</th><th class="py-1.5 text-right">DORMANT DAYS</th></tr></thead>
            <tbody class="divide-y divide-white/5 text-slate-300">
              <tr><td class="py-1.5 font-mono text-white">ART-GOLD-RING-12</td><td class="py-1.5">Gold Ring 22K</td><td class="py-1.5 text-right">8 pcs</td><td class="py-1.5 text-right font-bold text-amber-400">57 Days</td></tr>
              <tr><td class="py-1.5 font-mono text-white">ART-TEE-WHT-LARGE</td><td class="py-1.5">Casual Tee White</td><td class="py-1.5 text-right">45 pcs</td><td class="py-1.5 text-right font-bold text-amber-400">48 Days</td></tr>
            </tbody>
          `
        },
        slow: {
          title: "Slow Moving (Action Recommended)",
          tip: "Slow items have low velocity relative to inventory levels. Recommend promotional discount scheme.",
          rows: `
            <thead><tr class="border-b border-white/5 text-slate-500"><th class="py-1.5 text-left">SKU CODE</th><th class="py-1.5 text-left">ARTICLE NAME</th><th class="py-1.5 text-right">STOCK</th><th class="py-1.5 text-right">COVERAGE</th></tr></thead>
            <tbody class="divide-y divide-white/5 text-slate-300">
              <tr><td class="py-1.5 font-mono text-white">ART-JACKET-LEATHER</td><td class="py-1.5">Premium Leather Jacket</td><td class="py-1.5 text-right">30 pcs</td><td class="py-1.5 text-right font-bold text-orange-400">120 Days WOC</td></tr>
             </tbody>
          `
        },
        never: {
          title: "Never Sold (Investigate)",
          tip: "Never sold items have zero transactions since catalog creation. Check for barcode printing or price list issues.",
          rows: `
            <thead><tr class="border-b border-white/5 text-slate-500"><th class="py-1.5 text-left">SKU CODE</th><th class="py-1.5 text-left">ARTICLE NAME</th><th class="py-1.5 text-right">STOCK</th><th class="py-1.5 text-right">LOG DAYS</th></tr></thead>
            <tbody class="divide-y divide-white/5 text-slate-300">
              <tr><td class="py-1.5 font-mono text-white">ART-SOCKS-WOOL</td><td class="py-1.5">Woolen Winter Socks</td><td class="py-1.5 text-right">100 pairs</td><td class="py-1.5 text-right font-bold text-red-400">90 Days</td></tr>
            </tbody>
          `
        }
      };

      const current = data[tab];
      if (current) {
        titleEl.textContent = current.title;
        tableEl.innerHTML = current.rows;
        tipEl.textContent = current.tip;
      }
    }

    // Item Master Slide 13: Bad Data Calculator
    function calcItemMasterRoi() {
      const size = parseInt(document.getElementById('input-roi-cat-size').value) || 1500;
      const errRate = parseInt(document.getElementById('input-roi-cat-err').value) || 4;
      const trans = parseInt(document.getElementById('input-roi-cat-trans').value) || 5000;

      document.getElementById('roi-cat-size-val').textContent = size.toLocaleString();
      document.getElementById('roi-cat-err-val').textContent = `${errRate}%`;
      document.getElementById('roi-cat-trans-val').textContent = trans.toLocaleString();

      const billingErr = Math.round(trans * (errRate / 100) * 12);
      const invErr = Math.round(size * (errRate / 100));
      const revenueLeak = billingErr * 50;

      document.getElementById('roi-cat-billing-err').textContent = `${billingErr.toLocaleString()} Items`;
      document.getElementById('roi-cat-inv-err').textContent = `${invErr.toLocaleString()} SKUs`;
      document.getElementById('roi-cat-revenue-leak').textContent = `₹${revenueLeak.toLocaleString()}`;
    }
"""

# Append JS functions at the end of the script block (before </script> at the bottom)
# To be completely safe and avoid replacing the wrong </script> tags, we replace the last unique block.
# Let's match from the end of showBarcodeFailureDetails details block:
end_pattern = """      const data = details[cardId];
      if (data) {
        textEl.innerHTML = `
          <div class="space-y-3">
            <h4 class="font-outfit font-bold text-white text-sm border-b border-white/5 pb-1 flex items-center gap-2">
              <span class="text-amber-400">❓</span> ${data.title}
            </h4>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
              <div>
                <span class="text-amber-400 font-bold block">1. Operational Detection:</span>
                <p class="text-slate-300 mt-0.5">${data.detect}</p>
              </div>
              <div>
                <span class="text-emerald-400 font-bold block">2. In-Lane Correction:</span>
                <p class="text-slate-300 mt-0.5">${data.correct}</p>
              </div>
              <div>
                <span class="text-emerald-400 font-bold block">3. System Recovery:</span>
                <p class="text-slate-300 mt-0.5">${data.recover}</p>
              </div>
            </div>
          </div>
        `;
      }
    }"""

if "calcItemMasterRoi" not in content:
    content = content.replace(end_pattern, end_pattern + "\n" + itemmaster_js_funcs)

print("Cleaned / Updated file length:", len(content))

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("[SUCCESS] apply_itemmaster.py completed successfully. HTML updated.")
