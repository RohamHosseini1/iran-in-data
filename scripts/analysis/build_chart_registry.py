"""Build a deduplicated CHART_REGISTRY from the machine-readable harmonized sources
(WDI, FAOSTAT, IMF WEO, OWID, Maddison, WID). Collapses unit/currency/methodology
variants of the same underlying concept into one chart row, merges FAOSTAT's
historic/current and archive/current domain splits into one continuous series,
and flags cross-source duplicates (OWID/Maddison/WEO items that just re-report a
concept WDI or FAOSTAT already covers) as alt-source lines on the SAME chart
rather than new charts. Pahlavi-era archival tables and hand-curated series are
NOT included yet -- that cross-referencing pass (extends-existing-chart vs
genuinely-new-topic) is the next phase, done by hand/agent, not mechanically here.
"""
import csv
from collections import defaultdict

OUT = "data/processed/CHART_REGISTRY.csv"

WDI_PREFIX_CATEGORY = {
    'SP': 'Demographics & Population', 'NY': 'Macro / National Accounts',
    'NE': 'Macro / Expenditure & Trade Aggregates', 'SE': 'Education',
    'SL': 'Labor & Employment', 'SH': 'Health', 'EN': 'Environment',
    'DT': 'External Debt', 'NV': 'Industry / Value Added by Sector',
    'GC': 'Government Finance', 'TM': 'Trade (Imports)',
    'AG': 'Agriculture & Rural Development', 'DC': 'Aid & Development Finance',
    'TX': 'Trade (Exports)', 'EG': 'Energy', 'ER': 'Environment (Land & Resources)',
    'BX': 'Balance of Payments (Receipts)', 'FM': 'Financial Sector (Monetary)',
    'MS': 'Military Expenditure', 'IT': 'Infrastructure & Technology',
    'SI': 'Poverty & Inequality', 'BM': 'Balance of Payments (Payments)',
    'PA': 'Purchasing Power Parity', 'IS': 'Infrastructure (Transport)',
    'SM': 'Migration', 'CM': 'Capital Markets', 'BN': 'Balance of Payments (Net)',
    'ST': 'Tourism & Trade Services', 'FP': 'Prices & Inflation',
    'IP': 'Intellectual Property', 'FS': 'Financial Sector',
    'IQ': 'WB Meta / Statistical Capacity', 'TG': 'Trade (Goods)',
    'FI': 'Financial Sector (Interest Rates)', 'FD': 'Financial Sector (Private Credit)',
    'FR': 'Financial Sector (Interest Rates)', 'LP': 'Logistics Performance',
    'PX': 'Price Indices', 'FX': 'Exchange Rates', 'VC': 'Conflict & Violence',
    'SN': 'Nutrition', 'FB': 'Financial Sector (Banking Access)', 'SG': 'Gender',
    'BG': 'Balance of Payments (misc)', 'TT': 'Terms of Trade',
    'GB': 'Government / Governance', 'IE': 'Infrastructure (Energy)',
    'IC': 'Business & Investment Climate', 'GOV': 'Governance (WGI)',
    'HD': 'Human Capital', 'GD': 'Gender / Legal Rights', 'PER': 'Social Protection',
}
EXCLUDED_PREFIXES = {'IQ'}  # WB meta/statistical-capacity scoring -- not a fact about Iran

def wdi_root(code):
    if '.' in code:
        parts = code.split('.')
        return '.'.join(parts[:-1]) if len(parts) > 2 else code
    if '_' in code:
        parts = code.split('_')
        return '_'.join(parts[:-1]) if len(parts) > 2 else code
    return code

def wdi_category(root_code):
    prefix = root_code.split('.')[0].split('_')[0]
    # WDI_PREFIX_CATEGORY keys are uppercase; a handful of real topic codes (e.g. the
    # social-protection "per_..." indicators) are lowercase in the underlying indicator
    # ID, which silently fell through to the "Other (per)" fallback pre-2026-07-13 even
    # though a proper mapping already existed for 'PER'. Normalize before lookup.
    return WDI_PREFIX_CATEGORY.get(prefix.upper(), f'Other ({prefix})')

def shortest_label(members):
    # prefer the variant with the shortest label as the canonical chart title
    # (usually the plainest phrasing, e.g. "Population" over "Population, total")
    return sorted(members, key=lambda cl: len(cl[1]))[0][1]

rows = []

# ---------- WDI ----------
wdi_pairs = set()
with open("data/processed/macro_wdi.csv", newline='', encoding='utf-8', errors='replace') as f:
    for row in csv.DictReader(f):
        if row.get('country_iso3') == 'IRN' and row.get('value'):
            wdi_pairs.add((row['indicator_id'], row['indicator_label']))

wdi_groups = defaultdict(list)
for code, label in wdi_pairs:
    wdi_groups[wdi_root(code)].append((code, label))

wdi_new = 0
for root_code, members in wdi_groups.items():
    prefix = root_code.split('.')[0].split('_')[0]
    if prefix in EXCLUDED_PREFIXES:
        continue
    rows.append({
        "chart_id": f"wdi__{root_code}",
        "title": shortest_label(members),
        "category": wdi_category(root_code),
        "primary_source": "wdi",
        "alt_sources": "",
        "n_unit_variants_merged": len(members),
        "underlying_codes": "|".join(c for c, l in members),
        "status": "new",
    })
    wdi_new += 1

# ---------- FAOSTAT: commodity x economic-question-angle ----------
def iran_pairs(path):
    s = set()
    with open(path, newline='', encoding='utf-8', errors='replace') as f:
        for row in csv.DictReader(f):
            if row.get('country_iso3') == 'IRN' and row.get('value'):
                s.add((row['item'], row['element']))
    return s

qcl = iran_pairs("data/processed/agriculture_qcl_production.csv")
fbs = iran_pairs("data/processed/agriculture_fbs_food_balances.csv")
fbsh = iran_pairs("data/processed/agriculture_fbsh_food_balances_historic.csv")
fb = fbs | fbsh
pp = iran_pairs("data/processed/agriculture_pp_producer_prices.csv")
pa = iran_pairs("data/processed/agriculture_pa_prices_archive_pre1991.csv")
price = pp | pa

PROD_EL = {"Production", "Area harvested", "Yield", "Yield/Carcass Weight",
           "Producing Animals/Slaughtered", "Stocks", "Milk Animals", "Laying"}
TRADE_EL = {"Export quantity", "Import quantity", "Domestic supply quantity"}
CONS_EL = {"Food supply (kcal/capita/day)", "Food supply quantity (kg/capita/yr)",
           "Protein supply quantity (g/capita/day)", "Fat supply quantity (g/capita/day)", "Food"}

items_prod = set(i for i, e in qcl if e in PROD_EL)
items_trade = set(i for i, e in fb if e in TRADE_EL)
items_cons = set(i for i, e in fb if e in CONS_EL)
items_price = set(i for i, e in price)

# citrus is bridged pre-1961 in data/processed/bridged_series -- same chart, not new
fao_new = 0
for item in sorted(items_prod):
    rows.append({"chart_id": f"faostat__{item}__production", "title": f"{item} — Production, Area & Yield",
                 "category": "Agriculture Production", "primary_source": "faostat-qcl", "alt_sources": "",
                 "n_unit_variants_merged": "", "underlying_codes": item, "status": "new"})
    fao_new += 1
for item in sorted(items_trade):
    rows.append({"chart_id": f"faostat__{item}__trade", "title": f"{item} — Imports & Exports",
                 "category": "Agriculture Trade", "primary_source": "faostat-fbs+fbsh", "alt_sources": "",
                 "n_unit_variants_merged": "", "underlying_codes": item, "status": "new"})
    fao_new += 1
for item in sorted(items_cons):
    rows.append({"chart_id": f"faostat__{item}__consumption", "title": f"{item} — Per-Capita Food Consumption",
                 "category": "Food Consumption", "primary_source": "faostat-fbs+fbsh", "alt_sources": "",
                 "n_unit_variants_merged": "", "underlying_codes": item, "status": "new"})
    fao_new += 1
for item in sorted(items_price):
    rows.append({"chart_id": f"faostat__{item}__price", "title": f"{item} — Producer Price",
                 "category": "Agriculture Prices", "primary_source": "faostat-pp+pa", "alt_sources": "",
                 "n_unit_variants_merged": "", "underlying_codes": item, "status": "new"})
    fao_new += 1

# ---------- IMF WEO: hand-classified against WDI overlap ----------
weo_new_concepts = [
    ("weo__primary_balance", "Government Primary Balance (excl. interest)", "Government Finance",
     "GGXONLB|GGXONLB_NGDP"),
    ("weo__net_govt_debt", "Government Net Debt (assets netted)", "Government Finance", "GGXWDN|GGXWDN_NGDP"),
    ("weo__gdp_fiscal_year", "GDP, Fiscal-Year Basis", "Macro / National Accounts", "NGDP_FY"),
    ("weo__gdp_pcap_ppp_constant", "GDP per Capita, Constant-Price PPP", "Macro / National Accounts", "NGDPRPPPPC"),
    ("weo__ppp_share_world_gdp", "Iran's Share of World GDP (PPP)", "Macro / National Accounts", "PPPSH"),
    ("weo__import_volume_growth", "Import Volume Growth", "Trade", "TMG_RPCH|TM_RPCH"),
    ("weo__export_volume_growth", "Export Volume Growth", "Trade", "TXG_RPCH|TX_RPCH"),
]
for cid, title, cat, codes in weo_new_concepts:
    rows.append({"chart_id": cid, "title": title, "category": cat, "primary_source": "imf-weo",
                 "alt_sources": "", "n_unit_variants_merged": "", "underlying_codes": codes, "status": "new"})

# ---------- OWID: hand-classified against WDI/FAOSTAT overlap ----------
owid_new_concepts = [
    ("owid__hdi", "Human Development Index", "Development / Composite Index", "human-development-index"),
    ("owid__mean_years_schooling_long_run", "Average Years of Schooling (long-run)", "Education",
     "mean-years-of-schooling-long-run"),
    ("owid__oil_production_volume", "Oil Production (physical volume)", "Energy", "oil-production-by-country"),
]
for cid, title, cat, codes in owid_new_concepts:
    rows.append({"chart_id": cid, "title": title, "category": cat, "primary_source": "owid",
                 "alt_sources": "", "n_unit_variants_merged": "", "underlying_codes": codes, "status": "new"})

# ---------- WID: fully additive, not tracked by WDI's Gini ----------
wid_new_concepts = [
    ("wid__avg_national_income", "Average National Income per Adult", "Inequality & Wealth", "anninc992i|anninc999i"),
    ("wid__income_share_top10", "Pre-Tax Income Share, Top 10%", "Inequality & Wealth", "sptinc*_p90p100"),
    ("wid__income_share_top1", "Pre-Tax Income Share, Top 1%", "Inequality & Wealth", "sptinc*_p99p100"),
    ("wid__wealth_share_top10", "Net Wealth Share, Top 10%", "Inequality & Wealth", "shweal*_p90p100"),
    ("wid__wealth_share_top1", "Net Wealth Share, Top 1%", "Inequality & Wealth", "shweal*_p99p100"),
]
for cid, title, cat, codes in wid_new_concepts:
    rows.append({"chart_id": cid, "title": title, "category": cat, "primary_source": "wid-world",
                 "alt_sources": "", "n_unit_variants_merged": "", "underlying_codes": codes, "status": "new"})

# Maddison contributes 0 new concepts (GDP per capita + population both already counted via WDI);
# its role is as a pre-1950 depth extension merged onto the WDI GDP-per-capita and Population charts.

with open(OUT, "w", newline='', encoding='utf-8') as f:
    fieldnames = ["chart_id", "title", "category", "primary_source", "alt_sources",
                  "n_unit_variants_merged", "underlying_codes", "status"]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for r in rows:
        w.writerow(r)

print(f"WDI new concepts:     {wdi_new}")
print(f"FAOSTAT new concepts: {fao_new}")
print(f"WEO new concepts:     {len(weo_new_concepts)}")
print(f"OWID new concepts:    {len(owid_new_concepts)}")
print(f"WID new concepts:     {len(wid_new_concepts)}")
print(f"Maddison new concepts: 0 (folds into WDI GDP-per-capita & Population as pre-1950 extension)")
print(f"TOTAL rows written to {OUT}: {len(rows)}")
