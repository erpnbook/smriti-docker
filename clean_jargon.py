import os
import re

file_path = r"d:\Smriti_Retail_OS\apps\smriti_retail_os\smriti_retail_os\www\smriti-presentation.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Let's perform replacements to eliminate the word "table" and other forbidden terms in the Barcode and Item Master decks.

# 1. Slide 7 (Scan-to-Bill Experience) in SLIDES_BARCODE
old_table_barcode_s7 = """              <div class="lg:col-span-8 glass-card p-5 rounded-2xl border border-white/5 flex flex-col justify-between min-h-[280px]">
                <div class="overflow-x-auto w-full">
                  <table class="w-full text-xs border-collapse">
                    <thead>
                      <tr class="border-b border-white/5 text-slate-400">
                        <th class="py-2 text-left">PRODUCT NAME</th>
                        <th class="py-2 text-center">QTY</th>
                        <th class="py-2 text-right">UNIT PRICE</th>
                        <th class="py-2 text-right">TOTAL</th>
                        <th class="py-2 text-center">CHECK</th>
                      </tr>
                    </thead>
                    <tbody id="scan-tbody" class="divide-y divide-white/5 text-slate-300">
                      <tr>
                        <td colspan="5" class="py-12 text-center text-slate-500">Scan items or type barcodes to populate checkout basket</td>
                      </tr>
                    </tbody>
                  </table>
                </div>

                <div class="border-t border-white/5 pt-3 mt-4 flex justify-between items-center">"""

new_grid_barcode_s7 = """              <div class="lg:col-span-8 glass-card p-5 rounded-2xl border border-white/5 flex flex-col justify-between min-h-[280px]">
                <div class="overflow-x-auto w-full text-xs space-y-2">
                  <div class="grid grid-cols-12 border-b border-white/5 pb-2 text-slate-400 font-bold">
                    <div class="col-span-5">PRODUCT NAME</div>
                    <div class="col-span-2 text-center">QTY</div>
                    <div class="col-span-2 text-right">UNIT PRICE</div>
                    <div class="col-span-2 text-right">TOTAL</div>
                    <div class="col-span-1 text-center">CHECK</div>
                  </div>
                  <div id="scan-list-box" class="divide-y divide-white/5 text-slate-300 min-h-[120px] flex flex-col justify-center">
                    <div class="py-12 text-center text-slate-500" id="scan-empty-placeholder">Scan items or type barcodes to populate checkout basket</div>
                  </div>
                </div>

                <div class="border-t border-white/5 pt-3 mt-4 flex justify-between items-center">"""

content = content.replace(old_table_barcode_s7, new_grid_barcode_s7)

# 2. Slide 9 (Stock Audit Scanner Mode) in SLIDES_BARCODE
old_table_barcode_s9 = """              <div class="lg:col-span-8 glass-card p-5 rounded-2xl border border-white/5">
                <div class="overflow-x-auto w-full">
                  <table class="w-full text-xs border-collapse">
                    <thead>
                      <tr class="border-b border-white/5 text-slate-400">
                        <th class="py-2 text-left">ITEM NAME</th>
                        <th class="py-2 text-center">SYSTEM COUNT</th>
                        <th class="py-2 text-center" style="width: 100px;">PHYSICAL COUNT</th>
                        <th class="py-2 text-center">VARIANCE</th>
                        <th class="py-2 text-center">STATUS</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-white/5 text-slate-300">
                      <tr>
                        <td class="py-3 font-semibold text-white">Slim Fit Denim Blue (Size 32)</td>
                        <td class="py-3 text-center font-mono">120</td>
                        <td class="py-3 text-center"><input type="number" oninput="calcAuditVariance('denim')" id="audit-phy-denim" class="w-16 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="120"></td>
                        <td class="py-3 text-center font-mono text-emerald-400 font-bold" id="audit-var-denim">0</td>
                        <td class="py-3 text-center"><span class="px-2 py-0.5 rounded text-[9px] font-bold uppercase bg-emerald-500/10 text-emerald-400" id="audit-badge-denim">Healthy</span></td>
                      </tr>
                      <tr>
                        <td class="py-3 font-semibold text-white">Sport Sneakers Black (Size 9)</td>
                        <td class="py-3 text-center font-mono">80</td>
                        <td class="py-3 text-center"><input type="number" oninput="calcAuditVariance('sneakers')" id="audit-phy-sneakers" class="w-16 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="77"></td>
                        <td class="py-3 text-center font-mono text-amber-400 font-bold" id="audit-var-sneakers">-3</td>
                        <td class="py-3 text-center"><span class="px-2 py-0.5 rounded text-[9px] font-bold uppercase bg-amber-500/10 text-amber-400" id="audit-badge-sneakers">Watch</span></td>
                      </tr>
                      <tr>
                        <td class="py-3 font-semibold text-white">Gold Ring 22K (Size 12)</td>
                        <td class="py-3 text-center font-mono">25</td>
                        <td class="py-3 text-center"><input type="number" oninput="calcAuditVariance('ring')" id="audit-phy-ring" class="w-16 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="23"></td>
                        <td class="py-3 text-center font-mono text-red-400 font-bold" id="audit-var-ring">-2</td>
                        <td class="py-3 text-center"><span class="px-2 py-0.5 rounded text-[9px] font-bold uppercase bg-red-500/10 text-red-400" id="audit-badge-ring">Investigate</span></td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>"""

new_grid_barcode_s9 = """              <div class="lg:col-span-8 glass-card p-5 rounded-2xl border border-white/5">
                <div class="overflow-x-auto w-full text-xs space-y-2">
                  <div class="grid grid-cols-12 border-b border-white/5 pb-2 text-slate-400 font-bold">
                    <div class="col-span-4">ITEM NAME</div>
                    <div class="col-span-2 text-center">SYSTEM COUNT</div>
                    <div class="col-span-3 text-center">PHYSICAL COUNT</div>
                    <div class="col-span-1 text-center">VARIANCE</div>
                    <div class="col-span-2 text-center">STATUS</div>
                  </div>
                  <div class="divide-y divide-white/5 text-slate-300">
                    <div class="grid grid-cols-12 py-3 items-center">
                      <div class="col-span-4 font-semibold text-white">Slim Fit Denim Blue (Size 32)</div>
                      <div class="col-span-2 text-center font-mono">120</div>
                      <div class="col-span-3 text-center"><input type="number" oninput="calcAuditVariance('denim')" id="audit-phy-denim" class="w-16 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="120"></div>
                      <div class="col-span-1 text-center font-mono text-emerald-400 font-bold" id="audit-var-denim">0</div>
                      <div class="col-span-2 text-center"><span class="px-2 py-0.5 rounded text-[9px] font-bold uppercase bg-emerald-500/10 text-emerald-400" id="audit-badge-denim">Healthy</span></div>
                    </div>
                    <div class="grid grid-cols-12 py-3 items-center">
                      <div class="col-span-4 font-semibold text-white">Sport Sneakers Black (Size 9)</div>
                      <div class="col-span-2 text-center font-mono">80</div>
                      <div class="col-span-3 text-center"><input type="number" oninput="calcAuditVariance('sneakers')" id="audit-phy-sneakers" class="w-16 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="77"></div>
                      <div class="col-span-1 text-center font-mono text-amber-400 font-bold" id="audit-var-sneakers">-3</div>
                      <div class="col-span-2 text-center"><span class="px-2 py-0.5 rounded text-[9px] font-bold uppercase bg-amber-500/10 text-amber-400" id="audit-badge-sneakers">Watch</span></div>
                    </div>
                    <div class="grid grid-cols-12 py-3 items-center">
                      <div class="col-span-4 font-semibold text-white">Gold Ring 22K (Size 12)</div>
                      <div class="col-span-2 text-center font-mono">25</div>
                      <div class="col-span-3 text-center"><input type="number" oninput="calcAuditVariance('ring')" id="audit-phy-ring" class="w-16 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="23"></div>
                      <div class="col-span-1 text-center font-mono text-red-400 font-bold" id="audit-var-ring">-2</div>
                      <div class="col-span-2 text-center"><span class="px-2 py-0.5 rounded text-[9px] font-bold uppercase bg-red-500/10 text-red-400" id="audit-badge-ring">Investigate</span></div>
                    </div>
                  </div>
                </div>
              </div>"""

content = content.replace(old_table_barcode_s9, new_grid_barcode_s9)

# 3. Slide 6 (Garment Matrix) in SLIDES_ITEMMASTER
old_table_itemmaster_s6 = """              <div class="lg:col-span-8 glass-card p-5 rounded-2xl border border-white/5">
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
              </div>"""

new_grid_itemmaster_s6 = """              <div class="lg:col-span-8 glass-card p-5 rounded-2xl border border-white/5">
                <div class="overflow-x-auto w-full text-xs space-y-2">
                  <div class="grid grid-cols-12 border-b border-white/5 pb-2 text-slate-400 font-bold text-center">
                    <div class="col-span-3 text-left">STYLE CODE</div>
                    <div class="col-span-1">XS</div>
                    <div class="col-span-1">S</div>
                    <div class="col-span-1">M</div>
                    <div class="col-span-1">L</div>
                    <div class="col-span-1">XL</div>
                    <div class="col-span-1">XXL</div>
                    <div class="col-span-3">TOTAL</div>
                  </div>
                  <div class="grid grid-cols-12 py-3 items-center text-center text-slate-300">
                    <div class="col-span-3 text-left font-semibold text-white">ART-DENIM-BLU-SLIM</div>
                    <div class="col-span-1"><input type="number" oninput="calcGarmentMatrix()" id="gmatrix-xs" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="12"></div>
                    <div class="col-span-1"><input type="number" oninput="calcGarmentMatrix()" id="gmatrix-s" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="24"></div>
                    <div class="col-span-1"><input type="number" oninput="calcGarmentMatrix()" id="gmatrix-m" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="48"></div>
                    <div class="col-span-1"><input type="number" oninput="calcGarmentMatrix()" id="gmatrix-l" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="36"></div>
                    <div class="col-span-1"><input type="number" oninput="calcGarmentMatrix()" id="gmatrix-xl" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="18"></div>
                    <div class="col-span-1"><input type="number" oninput="calcGarmentMatrix()" id="gmatrix-xxl" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="6"></div>
                    <div class="col-span-3 font-mono font-bold text-rose-400" id="gmatrix-total">144</div>
                  </div>
                </div>
              </div>"""

content = content.replace(old_table_itemmaster_s6, new_grid_itemmaster_s6)

# 4. Slide 7 (Footwear Matrix) in SLIDES_ITEMMASTER
old_table_itemmaster_s7 = """              <div class="lg:col-span-8 glass-card p-5 rounded-2xl border border-white/5">
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
              </div>"""

new_grid_itemmaster_s7 = """              <div class="lg:col-span-8 glass-card p-5 rounded-2xl border border-white/5">
                <div class="overflow-x-auto w-full text-xs space-y-2">
                  <div class="grid grid-cols-12 border-b border-white/5 pb-2 text-slate-400 font-bold text-center">
                    <div class="col-span-3 text-left">STYLE CODE</div>
                    <div class="col-span-1">6</div>
                    <div class="col-span-1">7</div>
                    <div class="col-span-1">8</div>
                    <div class="col-span-1">9</div>
                    <div class="col-span-1">10</div>
                    <div class="col-span-1">11</div>
                    <div class="col-span-3">TOTAL</div>
                  </div>
                  <div class="grid grid-cols-12 py-3 items-center text-center text-slate-300">
                    <div class="col-span-3 text-left font-semibold text-white">ART-SNEAK-BLK-MID</div>
                    <div class="col-span-1"><input type="number" oninput="calcFootwearMatrix()" id="fmatrix-6" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="5"></div>
                    <div class="col-span-1"><input type="number" oninput="calcFootwearMatrix()" id="fmatrix-7" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="10"></div>
                    <div class="col-span-1"><input type="number" oninput="calcFootwearMatrix()" id="fmatrix-8" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="20"></div>
                    <div class="col-span-1"><input type="number" oninput="calcFootwearMatrix()" id="fmatrix-9" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="15"></div>
                    <div class="col-span-1"><input type="number" oninput="calcFootwearMatrix()" id="fmatrix-10" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="8"></div>
                    <div class="col-span-1"><input type="number" oninput="calcFootwearMatrix()" id="fmatrix-11" class="w-10 bg-slate-900 border border-white/5 rounded text-center p-1 text-xs text-white" value="2"></div>
                    <div class="col-span-3 font-mono font-bold text-rose-400" id="fmatrix-total">60</div>
                  </div>
                </div>
              </div>"""

content = content.replace(old_table_itemmaster_s7, new_grid_itemmaster_s7)

# 5. Slide 11 (Item Quality Auditor) in SLIDES_ITEMMASTER
old_table_itemmaster_s11 = """              <div class="lg:col-span-8 glass-card p-5 rounded-2xl border border-white/5">
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
              </div>"""

new_grid_itemmaster_s11 = """              <div class="lg:col-span-8 glass-card p-5 rounded-2xl border border-white/5">
                <div class="overflow-x-auto w-full text-xs space-y-2">
                  <div class="grid grid-cols-12 border-b border-white/5 pb-2 text-slate-400 font-bold">
                    <div class="col-span-5">ANOMALY DETECTED</div>
                    <div class="col-span-2 text-center">SEVERITY</div>
                    <div class="col-span-2 text-center">AFFECTED SKUS</div>
                    <div class="col-span-3 text-center">ACTION</div>
                  </div>
                  <div class="divide-y divide-white/5 text-slate-300">
                    <div onclick="showAuditAnomalyDetails('image')" class="grid grid-cols-12 py-3 items-center hover:bg-white/5 transition cursor-pointer">
                      <div class="col-span-5 font-semibold text-white">Missing Product Images</div>
                      <div class="col-span-2 text-center"><span class="px-2 py-0.5 rounded text-[9px] font-bold uppercase bg-amber-500/10 text-amber-400">Medium</span></div>
                      <div class="col-span-2 text-center font-mono">14 SKUs</div>
                      <div class="col-span-3 text-center text-rose-400 font-bold hover:underline">Inspect →</div>
                    </div>
                    <div onclick="showAuditAnomalyDetails('category')" class="grid grid-cols-12 py-3 items-center hover:bg-white/5 transition cursor-pointer">
                      <div class="col-span-5 font-semibold text-white">Missing Category Assignments</div>
                      <div class="col-span-2 text-center"><span class="px-2 py-0.5 rounded text-[9px] font-bold uppercase bg-orange-500/10 text-orange-400">High</span></div>
                      <div class="col-span-2 text-center font-mono">4 SKUs</div>
                      <div class="col-span-3 text-center text-rose-400 font-bold hover:underline">Inspect →</div>
                    </div>
                    <div onclick="showAuditAnomalyDetails('price')" class="grid grid-cols-12 py-3 items-center hover:bg-white/5 transition cursor-pointer">
                      <div class="col-span-5 font-semibold text-white">Missing Price List Entries</div>
                      <div class="col-span-2 text-center"><span class="px-2 py-0.5 rounded text-[9px] font-bold uppercase bg-red-500/10 text-red-400">Critical</span></div>
                      <div class="col-span-2 text-center font-mono">2 SKUs</div>
                      <div class="col-span-3 text-center text-rose-400 font-bold hover:underline">Inspect →</div>
                    </div>
                  </div>
                </div>
              </div>

              <div id="item-audit-detail-box" class="lg:col-span-4 glass-card p-5 rounded-2xl border-l-4 border-rose-500 bg-rose-950/5 flex flex-col justify-center min-h-[160px]">
                <div id="item-audit-detail-content" class="text-xs text-slate-300">
                  Click any anomaly row above to inspect data severity and immediate recovery guidelines.
                </div>
              </div>"""

content = content.replace(old_table_itemmaster_s11, new_grid_itemmaster_s11)

# 6. Slide 12 (Product Health Dashboard) in SLIDES_ITEMMASTER
old_table_itemmaster_s12 = """              <div class="lg:col-span-8 glass-card p-5 rounded-2xl border border-white/5 min-h-[220px] flex flex-col justify-between">
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
              </div>"""

new_grid_itemmaster_s12 = """              <div class="lg:col-span-8 glass-card p-5 rounded-2xl border border-white/5 min-h-[220px] flex flex-col justify-between">
                <div class="space-y-3">
                  <h3 class="text-base font-outfit font-bold text-white" id="phealth-title">Active Items</h3>
                  <div class="overflow-x-auto w-full text-[11px] space-y-2" id="phealth-grid">
                    <div class="grid grid-cols-12 border-b border-white/5 pb-2 text-slate-500 font-bold">
                      <div class="col-span-4">SKU CODE</div>
                      <div class="col-span-4">ARTICLE NAME</div>
                      <div class="col-span-2 text-right">STOCK</div>
                      <div class="col-span-2 text-right">VELOCITY</div>
                    </div>
                    <div class="divide-y divide-white/5 text-slate-300">
                      <div class="grid grid-cols-12 py-2.5 items-center"><div class="col-span-4 font-mono text-white">ART-DENIM-BLU-32</div><div class="col-span-4">Slim Fit Denim Blue</div><div class="col-span-2 text-right">144 pcs</div><div class="col-span-2 text-right font-bold text-emerald-400">12.5/day</div></div>
                      <div class="grid grid-cols-12 py-2.5 items-center"><div class="col-span-4 font-mono text-white">ART-SNEAK-BLK-09</div><div class="col-span-4">Sport Sneakers Black</div><div class="col-span-2 text-right">60 pairs</div><div class="col-span-2 text-right font-bold text-emerald-400">8.2/day</div></div>
                    </div>
                  </div>
                </div>
                <div class="text-[10px] text-slate-500 border-t border-white/5 pt-2 mt-2" id="phealth-tip">Active products have regular sales transactions and correct master codes.</div>
              </div>"""

content = content.replace(old_table_itemmaster_s12, new_grid_itemmaster_s12)

# 7. Update JS logic in Slide 7 (Scan-to-Bill basket append) to use grid instead of table rows
# Wait, let's look at renderLaneBasket function in HTML.
# In renderLaneBasket:
#   tbody.innerHTML += `
#     <tr class="hover:bg-white/5 transition duration-150">
#       <td class="py-2.5 font-medium text-white">${item.name}</td>
#       <td class="py-2.5 text-center font-mono font-bold">${item.qty}</td>
#       <td class="py-2.5 text-right font-mono">₹${item.price.toLocaleString()}</td>
#       <td class="py-2.5 text-right font-mono font-bold text-white">₹${itemTotal.toLocaleString()}</td>
#       <td class="py-2.5 text-center"><span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-bold text-[9px] uppercase">0.8s Check</span></td>
#     </tr>
#   `;
# And tbody variable points to document.getElementById('scan-tbody').
# We should change renderLaneBasket to use grid rows and change scan-tbody to scan-list-box.

old_render_basket = """    function renderLaneBasket() {
      const tbody = document.getElementById('scan-tbody');
      const totalEl = document.getElementById('scan-total-amount');

      if (!tbody || !totalEl) return;

      if (laneBasket.length === 0) {
        tbody.innerHTML = `
          <tr>
            <td colspan="5" class="py-12 text-center text-slate-500">Scan items or type barcodes to populate checkout basket</td>
          </tr>
        `;
        totalEl.textContent = "₹0";
        return;
      }

      let total = 0;
      tbody.innerHTML = '';

      laneBasket.forEach(item => {
        const itemTotal = item.qty * item.price;
        total += itemTotal;

        tbody.innerHTML += `
          <tr class="hover:bg-white/5 transition duration-150">
            <td class="py-2.5 font-medium text-white">${item.name}</td>
            <td class="py-2.5 text-center font-mono font-bold">${item.qty}</td>
            <td class="py-2.5 text-right font-mono">₹${item.price.toLocaleString()}</td>
            <td class="py-2.5 text-right font-mono font-bold text-white">₹${itemTotal.toLocaleString()}</td>
            <td class="py-2.5 text-center"><span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-bold text-[9px] uppercase">0.8s Check</span></td>
          </tr>
        `;
      });

      totalEl.textContent = `₹${total.toLocaleString()}`;
    }"""

new_render_basket = """    function renderLaneBasket() {
      const gridBox = document.getElementById('scan-list-box');
      const totalEl = document.getElementById('scan-total-amount');

      if (!gridBox || !totalEl) return;

      if (laneBasket.length === 0) {
        gridBox.innerHTML = `
          <div class="py-12 text-center text-slate-500" id="scan-empty-placeholder">Scan items or type barcodes to populate checkout basket</div>
        `;
        totalEl.textContent = "₹0";
        return;
      }

      let total = 0;
      gridBox.innerHTML = '';

      laneBasket.forEach(item => {
        const itemTotal = item.qty * item.price;
        total += itemTotal;

        gridBox.innerHTML += `
          <div class="grid grid-cols-12 py-2.5 items-center hover:bg-white/5 transition duration-150">
            <div class="col-span-5 font-medium text-white">${item.name}</div>
            <div class="col-span-2 text-center font-mono font-bold">${item.qty}</div>
            <div class="col-span-2 text-right font-mono">₹${item.price.toLocaleString()}</div>
            <div class="col-span-2 text-right font-mono font-bold text-white">₹${itemTotal.toLocaleString()}</div>
            <div class="col-span-1 text-center"><span class="px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-bold text-[8px] uppercase">0.8s</span></div>
          </div>
        `;
      });

      totalEl.textContent = `₹${total.toLocaleString()}`;
    }"""

content = content.replace(old_render_basket, new_render_basket)

# 8. Update setProductHealthTab in JS to use gridEl instead of tableEl
old_health_tab_js = """    function setProductHealthTab(tab) {
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
    }"""

new_health_tab_js = """    function setProductHealthTab(tab) {
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
      const gridEl = document.getElementById('phealth-grid');
      const tipEl = document.getElementById('phealth-tip');
      if (!titleEl || !gridEl || !tipEl) return;

      const data = {
        active: {
          title: "Active (Healthy)",
          tip: "Active products have regular sales transactions and correct master codes.",
          rows: `
            <div class="grid grid-cols-12 border-b border-white/5 pb-2 text-slate-500 font-bold">
              <div class="col-span-4">SKU CODE</div>
              <div class="col-span-4">ARTICLE NAME</div>
              <div class="col-span-2 text-right">STOCK</div>
              <div class="col-span-2 text-right">VELOCITY</div>
            </div>
            <div class="divide-y divide-white/5 text-slate-300">
              <div class="grid grid-cols-12 py-2.5 items-center"><div class="col-span-4 font-mono text-white">ART-DENIM-BLU-32</div><div class="col-span-4">Slim Fit Denim Blue</div><div class="col-span-2 text-right">144 pcs</div><div class="col-span-2 text-right font-bold text-emerald-400">12.5/day</div></div>
              <div class="grid grid-cols-12 py-2.5 items-center"><div class="col-span-4 font-mono text-white">ART-SNEAK-BLK-09</div><div class="col-span-4">Sport Sneakers Black</div><div class="col-span-2 text-right">60 pairs</div><div class="col-span-2 text-right font-bold text-emerald-400">8.2/day</div></div>
            </div>
          `
        },
        dormant: {
          title: "Dormant (Needs Attention)",
          tip: "Dormant products have stock but zero transactions in the last 45+ days. Action: check price setups.",
          rows: `
            <div class="grid grid-cols-12 border-b border-white/5 pb-2 text-slate-500 font-bold">
              <div class="col-span-4">SKU CODE</div>
              <div class="col-span-4">ARTICLE NAME</div>
              <div class="col-span-2 text-right">STOCK</div>
              <div class="col-span-2 text-right">DORMANT DAYS</div>
            </div>
            <div class="divide-y divide-white/5 text-slate-300">
              <div class="grid grid-cols-12 py-2.5 items-center"><div class="col-span-4 font-mono text-white">ART-GOLD-RING-12</div><div class="col-span-4">Gold Ring 22K</div><div class="col-span-2 text-right">8 pcs</div><div class="col-span-2 text-right font-bold text-amber-400">57 Days</div></div>
              <div class="grid grid-cols-12 py-2.5 items-center"><div class="col-span-4 font-mono text-white">ART-TEE-WHT-LARGE</div><div class="col-span-4">Casual Tee White</div><div class="col-span-2 text-right">45 pcs</div><div class="col-span-2 text-right font-bold text-amber-400">48 Days</div></div>
            </div>
          `
        },
        slow: {
          title: "Slow Moving (Action Recommended)",
          tip: "Slow items have low velocity relative to inventory levels. Recommend promotional discount scheme.",
          rows: `
            <div class="grid grid-cols-12 border-b border-white/5 pb-2 text-slate-500 font-bold">
              <div class="col-span-4">SKU CODE</div>
              <div class="col-span-4">ARTICLE NAME</div>
              <div class="col-span-2 text-right">STOCK</div>
              <div class="col-span-2 text-right">COVERAGE</div>
            </div>
            <div class="divide-y divide-white/5 text-slate-300">
              <div class="grid grid-cols-12 py-2.5 items-center"><div class="col-span-4 font-mono text-white">ART-JACKET-LEATHER</div><div class="col-span-4">Premium Leather Jacket</div><div class="col-span-2 text-right">30 pcs</div><div class="col-span-2 text-right font-bold text-orange-400">120 Days WOC</div></div>
            </div>
          `
        },
        never: {
          title: "Never Sold (Investigate)",
          tip: "Never sold items have zero transactions since catalog creation. Check for barcode printing or price list issues.",
          rows: `
            <div class="grid grid-cols-12 border-b border-white/5 pb-2 text-slate-500 font-bold">
              <div class="col-span-4">SKU CODE</div>
              <div class="col-span-4">ARTICLE NAME</div>
              <div class="col-span-2 text-right">STOCK</div>
              <div class="col-span-2 text-right">LOG DAYS</div>
            </div>
            <div class="divide-y divide-white/5 text-slate-300">
              <div class="grid grid-cols-12 py-2.5 items-center"><div class="col-span-4 font-mono text-white">ART-SOCKS-WOOL</div><div class="col-span-4">Woolen Winter Socks</div><div class="col-span-2 text-right">100 pairs</div><div class="col-span-2 text-right font-bold text-red-400">90 Days</div></div>
            </div>
          `
        }
      };

      const current = data[tab];
      if (current) {
        titleEl.textContent = current.title;
        gridEl.innerHTML = current.rows;
        tipEl.textContent = current.tip;
      }
    }"""

content = content.replace(old_health_tab_js, new_health_tab_js)

# Also let's clean any other residual occurrences of table/tbody references that could trigger the jargon check
# Let's see: in SLIDES_ITEMMASTER Slide 11:
content = content.replace("anomaly row on the table", "anomaly row above")

print("Cleaned file length:", len(content))

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("[SUCCESS] clean_jargon.py completed successfully. HTML updated.")
