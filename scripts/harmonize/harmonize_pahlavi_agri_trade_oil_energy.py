"""Harmonize 19 Pahlavi-era archival tables -- agriculture production/land-value,
foreign trade by commodity, ocean-trade tonnage, cost-of-living index, and the full
oil/gas/electric-power sector (World Bank 1960/1962/1971/1974 reports + US Bureau of
Mines Information Circular 8203, 1963) -- already hand-extracted and visually verified
to data/raw/pahlavi-era-primary-extraction/*/data.csv by earlier rounds of this
project, into tidy long-format CSVs.

Two output folders, same uniform schema as the existing
scripts/harmonize/harmonize_pahlavi_government_finance.py precedent (re-used
deliberately for consistency across all Pahlavi-extraction harmonization batches):

  data/processed/pahlavi_agriculture_trade_extensions/   (7 files)
  data/processed/pahlavi_oil_energy_series/               (12 files)

Schema (uniform across all 19 files):
  fiscal_year_label, year, category, subcategory, value, unit, notes, country_iso3, source_dataset

- fiscal_year_label: the period exactly as printed in the source ("1956/57", "1950/51",
  "1910-32" for an aggregated multi-year source row, "Sub-total (actuals)" for a printed
  subtotal row, etc.). Never reformatted beyond cosmetic underscore->slash normalization.
- year: single sortable integer. Dual-year fiscal labels ("1958/59") map to the LATER
  Western year (1959), matching the convention already established in
  pahlavi_government_finance_series/ and iran_data_portal_deep_series/. Aggregated
  multi-year source rows (e.g. "1910-32", "1952-54", "Sub-total (actuals)", grand TOTAL
  rows) get year="" (blank) since they are not a single point in time -- never guessed
  or midpoint-averaged.
- category/subcategory: preserves each source table's own row hierarchy.
- value: blank means the source cell was blank, "n.a.", or a dash -- never filled in.
- No value is ever recalculated, interpolated, fabricated, or unit-converted here.
  Citrus rows (Oranges & Tangerines, Other Citrus) from wb1960-agricultural-production
  are deliberately EXCLUDED from this batch's output -- already bridged in
  data/processed/bridged_series/citrus_production_iran_1950_2024.csv; re-including them
  here would create a duplicate series.

Never touches data/raw/ (immutable). Writes only to data/processed/.
"""
import csv
import os
import re

RAW = "data/raw/pahlavi-era-primary-extraction"
OUT_AGRI = "data/processed/pahlavi_agriculture_trade_extensions"
OUT_OIL = "data/processed/pahlavi_oil_energy_series"
FIELDNAMES = ["fiscal_year_label", "year", "category", "subcategory", "value", "unit",
              "notes", "country_iso3", "source_dataset"]


def read_raw(dataset_dir, filename="data.csv"):
    path = os.path.join(RAW, dataset_dir, filename)
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_out(out_dir, filename, rows):
    path = os.path.join(out_dir, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writeheader()
        for r in rows:
            full = {k: r.get(k, "") for k in FIELDNAMES}
            full["country_iso3"] = "IRN"
            w.writerow(full)
    print(f"  wrote {out_dir}/{filename}: {len(rows)} rows")


def dualyear_to_year(label):
    """'1958/59' -> 1959 ; '1962' -> 1962 ; '1958_59' -> 1959 ; range/aggregate labels -> ''."""
    label = label.strip()
    core = label.replace("_", "/") if re.match(r"^\d{4}_\d{2,4}$", label) else label
    if "/" in core:
        first, suffix = core.split("/", 1)
        if not suffix.isdigit() or not first.isdigit():
            return ""
        century_prefix = first[:-len(suffix)] if len(suffix) < len(first) else ""
        try:
            return int(century_prefix + suffix)
        except ValueError:
            return ""
    if re.fullmatch(r"\d{4}", core):
        return int(core)
    return ""  # multi-year aggregate ranges, subtotal/total labels, etc.


n_written = 0

# =====================================================================
# FOLDER 1: pahlavi_agriculture_trade_extensions
# =====================================================================

# ---------- 1. Agricultural production, 1950-1958 ----------
print("1. agricultural_production_1950_1958.csv")
raw = read_raw("wb1960-agricultural-production-1950-1958")
year_cols = ["1950", "1951", "1952", "1953", "1954", "1955", "1956", "1957", "1958"]
EXCLUDE_CITRUS = {"Oranges & Tangerines", "Other Citrus"}
rows = []
for r in raw:
    if r["commodity"] in EXCLUDE_CITRUS:
        continue  # already bridged in data/processed/bridged_series/citrus_production_iran_1950_2024.csv
    for yc in year_cols:
        rows.append({
            "fiscal_year_label": yc, "year": int(yc),
            "category": r["commodity"], "subcategory": "Production",
            "value": r.get(yc, ""), "unit": r["unit"],
            "notes": "", "source_dataset": "wb1960-table5-agricultural-production",
        })
write_out(OUT_AGRI, "agricultural_production_1950_1958.csv", rows)
n_written += 1

# ---------- 2. Crop land, production & gross value, 1960 ----------
print("2. crop_land_production_value_1960.csv")
raw = read_raw("wb1962-crop-land-production-value-1960")
metric_cols = [
    ("area_1000_ha", "Area Harvested", "1000 ha"),
    ("production_1000_metric_tons", "Production", "1000 metric tons"),
    ("value_rls_million", "Gross Value", "Rls million"),
]
rows = []
for r in raw:
    for col, subcat, unit in metric_cols:
        rows.append({
            "fiscal_year_label": "1960", "year": 1960,
            "category": r["commodity"], "subcategory": subcat,
            "value": r.get(col, ""), "unit": unit,
            "notes": "", "source_dataset": "wb1962-agriculturetable1-crop-land-production-value",
        })
write_out(OUT_AGRI, "crop_land_production_value_1960.csv", rows)
n_written += 1

# ---------- 3. Livestock production & gross value, 1960 ----------
print("3. livestock_production_value_1960.csv")
raw = read_raw("wb1962-livestock-production-value-1960")
rows = []
for r in raw:
    if r.get("quantity"):
        rows.append({
            "fiscal_year_label": "1960", "year": 1960,
            "category": r["commodity"], "subcategory": "Quantity",
            "value": r["quantity"], "unit": r.get("quantity_unit", ""),
            "notes": "", "source_dataset": "wb1962-agriculturetable2-livestock-production-value",
        })
    if r.get("value_rls_million"):
        rows.append({
            "fiscal_year_label": "1960", "year": 1960,
            "category": r["commodity"], "subcategory": "Gross Value",
            "value": r["value_rls_million"], "unit": "Rls million",
            "notes": "", "source_dataset": "wb1962-agriculturetable2-livestock-production-value",
        })
write_out(OUT_AGRI, "livestock_production_value_1960.csv", rows)
n_written += 1

# ---------- 4. Exports by commodity, 1956/57-1958/59 ----------
print("4. exports_by_commodity_1956_59.csv")
raw = read_raw("wb1960-exports-by-commodities-1956-1959")
fy_pairs = [("value_1956_57", "pct_1956_57", "1956/57"), ("value_1957_58", "pct_1957_58", "1957/58"),
            ("value_1958_59", "pct_1958_59", "1958/59")]
rows = []
for r in raw:
    for vcol, pcol, label in fy_pairs:
        rows.append({
            "fiscal_year_label": label, "year": dualyear_to_year(label),
            "category": r["commodity"], "subcategory": "Export Value",
            "value": r.get(vcol, ""), "unit": r["value_unit"],
            "notes": "Oil/petroleum exports excluded from this table (reported separately) -- see pahlavi_oil_energy_series/",
            "source_dataset": "wb1960-table16-exports-by-commodities",
        })
        rows.append({
            "fiscal_year_label": label, "year": dualyear_to_year(label),
            "category": r["commodity"], "subcategory": "Share of Total Exports",
            "value": r.get(pcol, ""), "unit": "percent",
            "notes": "", "source_dataset": "wb1960-table16-exports-by-commodities",
        })
write_out(OUT_AGRI, "exports_by_commodity_1956_59.csv", rows)
n_written += 1

# ---------- 5. Imports by commodity, 1956/57-1958/59 ----------
print("5. imports_by_commodity_1956_59.csv")
raw = read_raw("wb1960-imports-by-commodities-1956-1959")
rows = []
for r in raw:
    for vcol, pcol, label in fy_pairs:
        rows.append({
            "fiscal_year_label": label, "year": dualyear_to_year(label),
            "category": r["commodity"], "subcategory": "Import Value",
            "value": r.get(vcol, ""), "unit": r["value_unit"],
            "notes": "", "source_dataset": "wb1960-table17-imports-by-commodities",
        })
        rows.append({
            "fiscal_year_label": label, "year": dualyear_to_year(label),
            "category": r["commodity"], "subcategory": "Share of Total Imports",
            "value": r.get(pcol, ""), "unit": "percent",
            "notes": "", "source_dataset": "wb1960-table17-imports-by-commodities",
        })
write_out(OUT_AGRI, "imports_by_commodity_1956_59.csv", rows)
n_written += 1

# ---------- 6. Ocean trade tonnage (excl. petroleum), 1950/51-1959/60 ----------
print("6. ocean_trade_tonnage_1950_60.csv")
raw = read_raw("wb1962-ocean-trade-1950-1960")
rows = []
for r in raw:
    label = r["year"]
    for col, subcat in [("exports_1000_metric_tons", "Exports"), ("imports_1000_metric_tons", "Imports"),
                         ("total_1000_metric_tons", "Total")]:
        rows.append({
            "fiscal_year_label": label, "year": dualyear_to_year(label),
            "category": "Ocean Trade Tonnage (Excl. Petroleum Products)", "subcategory": subcat,
            "value": r.get(col, ""), "unit": "1000 metric tons",
            "notes": "", "source_dataset": "wb1962-transporttable7-ocean-trade",
        })
write_out(OUT_AGRI, "ocean_trade_tonnage_1950_60.csv", rows)
n_written += 1

# ---------- 7. Cost of living index, 1955-1959 ----------
print("7. cost_of_living_index_1955_59.csv")
raw = read_raw("wb1960-cost-of-living-index-1955-1959")
period_cols = [("dec_1956", "Dec 1956", 1956), ("dec_1957", "Dec 1957", 1957),
               ("dec_1958", "Dec 1958", 1958), ("sept_1959", "Sept 1959", 1959)]
rows = []
for r in raw:
    rows.append({
        "fiscal_year_label": "(fixed basket weight)", "year": "",
        "category": r["category"], "subcategory": "Weight in Index Basket",
        "value": r["weight_pct"], "unit": "percent of total basket",
        "notes": "", "source_dataset": "wb1960-table9-cost-of-living-index",
    })
    for col, label, yr in period_cols:
        val = r.get(col, "")
        note = ""
        if r["category"] == "Total" and col == "sept_1959":
            note = "Printed in source as '137 (provisional)' -- 'provisional' flag preserved, numeric value used as-is"
            val = "137"
        rows.append({
            "fiscal_year_label": label, "year": yr,
            "category": r["category"], "subcategory": "Cost of Living Index (Dec 1955=100)",
            "value": val, "unit": "index, Dec 1955=100",
            "notes": note, "source_dataset": "wb1960-table9-cost-of-living-index",
        })
write_out(OUT_AGRI, "cost_of_living_index_1955_59.csv", rows)
n_written += 1

# =====================================================================
# FOLDER 2: pahlavi_oil_energy_series
# =====================================================================

# ---------- 8. Oil revenues by allocation, 1955/56-1962/63 ----------
print("8. oil_revenues_by_allocation_1955_63.csv")
raw = read_raw("wb1960-oil-revenues-1955-1963")
alloc_cols = [("total", "Total"), ("budget", "Budget"), ("nioc", "NIOC"),
              ("plan_organization", "Plan Organization"), ("bpc", "B.P.C.")]
rows = []
for r in raw:
    label = r["period"]
    yr = dualyear_to_year(label)
    type_tag = f" [{r['type']}]" if r["type"] not in ("actual",) else ""
    for col, subcat in alloc_cols:
        rows.append({
            "fiscal_year_label": label, "year": yr,
            "category": "Oil Revenue by Allocation (Accrual Basis)", "subcategory": subcat,
            "value": r.get(col, ""), "unit": r["unit"],
            "notes": (r.get("notes", "") + type_tag).strip(),
            "source_dataset": "wb1960-table1-oil-revenues",
        })
write_out(OUT_OIL, "oil_revenues_by_allocation_1955_63.csv", rows)
n_written += 1

# ---------- 9. Oil exports & revenues (by company), 1963/64-1970/71 ----------
print("9. oil_exports_revenues_by_company_1963_71.csv")
raw = read_raw("wb1971-oil-exports-and-revenues-1963-1971")
SERIES_MAP = {
    "exports_total": ("Oil Exports (Volume)", "Total"),
    "exports_crude": ("Oil Exports (Volume)", "Crude"),
    "exports_products": ("Oil Exports (Volume)", "Products"),
    "revenues_total": ("Oil Revenue by Paying Company", "Total"),
    "revenues_consortium": ("Oil Revenue by Paying Company", "Consortium"),
    "revenues_nioc": ("Oil Revenue by Paying Company", "NIOC"),
    "revenues_other_companies": ("Oil Revenue by Paying Company", "Other Companies"),
    "avg_revenue_per_ton_total": ("Average Oil Revenue per Ton Exported", "Total"),
    "avg_revenue_per_ton_consortium": ("Average Oil Revenue per Ton Exported", "Consortium"),
    "avg_revenue_per_ton_other_companies": ("Average Oil Revenue per Ton Exported", "Other Companies"),
}
year_cols_9 = ["1963_64", "1964_65", "1965_66", "1966_67", "1967_68", "1968_69", "1969_70", "1970_71_estimate"]
rows = []
for r in raw:
    cat, subcat = SERIES_MAP[r["series"]]
    for yc in year_cols_9:
        is_est = yc.endswith("_estimate")
        base = yc.replace("_estimate", "")
        label = base.replace("_", "/") + (" (preliminary estimate)" if is_est else "")
        rows.append({
            "fiscal_year_label": label, "year": dualyear_to_year(base),
            "category": cat, "subcategory": subcat,
            "value": r.get(yc, ""), "unit": r["unit"],
            "notes": "Preliminary estimate, not final actual" if is_est else "",
            "source_dataset": "wb1971-table9-oil-exports-and-revenues",
        })
write_out(OUT_OIL, "oil_exports_revenues_by_company_1963_71.csv", rows)
n_written += 1

# ---------- 10. Domestic oil consumption by product, 1964-1969 ----------
print("10. domestic_oil_consumption_by_product_1964_69.csv")
raw = read_raw("wb1971-domestic-oil-consumption-1964-1969")
PRODUCT_LABEL = {
    "fuel_oil": "Fuel Oil", "gas_oil": "Gas Oil", "kerosene": "Kerosene", "gasoline": "Gasoline",
    "other_products_incl_liquid_gas": "Other Products (incl. Liquid Gas)", "total_consumption": "Total",
}
rows = []
for r in raw:
    rows.append({
        "fiscal_year_label": r["year"], "year": int(r["year"]),
        "category": "Domestic Consumption of Oil Products", "subcategory": PRODUCT_LABEL[r["product"]],
        "value": r["value_thousand_mtons"], "unit": "1000 metric tons",
        "notes": "1965 kerosene value (2,216) is a genuine printed anomaly vs 1964 (1,188) and 1966 (1,266), double-checked against the source image, not a transcription artifact" if (r["year"] == "1965" and r["product"] == "kerosene") else "",
        "source_dataset": "wb1971-table8.8-domestic-consumption-of-oil-products",
    })
write_out(OUT_OIL, "domestic_oil_consumption_by_product_1964_69.csv", rows)
n_written += 1

# ---------- 11. Petroleum statistics, 1956-1958 ----------
print("11. petroleum_statistics_1956_58.csv")
raw = read_raw("wb1960-petroleum-statistics-1956-1958")
year_cols_11 = ["1956", "1957", "1958"]
rows = []
for r in raw:
    for yc in year_cols_11:
        note = ""
        if r["category"] == "Production":
            note = ("This 'Production' row (physical volume, million m3) covers the same broad concept as "
                     "the already-registered owid__oil_production_volume chart (OWID's Iran oil-production "
                     "series already runs continuously from 1900) -- OVERLAPPING years, not a gap, so this "
                     "should be treated as an ALTERNATE/cross-check source line for 1956-1958, never averaged "
                     "or silently reconciled with OWID's figure.")
        rows.append({
            "fiscal_year_label": yc, "year": int(yc),
            "category": r["category"], "subcategory": r["subcategory"],
            "value": r.get(yc, ""), "unit": r["unit"],
            "notes": note, "source_dataset": "wb1960-table2-petroleum-statistics",
        })
write_out(OUT_OIL, "petroleum_statistics_1956_58.csv", rows)
n_written += 1

# ---------- 12. Natural gas production & consumption, 1965-1969 ----------
print("12. gas_production_consumption_1965_69.csv")
raw = read_raw("wb1971-gas-production-consumption-1965-1969")
rows = []
for r in raw:
    rows.append({
        "fiscal_year_label": r["year"], "year": int(r["year"]),
        "category": "Natural Gas Production & Consumption", "subcategory": f"{r['entity']} — {r['metric']}",
        "value": r["value_million_cubic_meters"], "unit": "million cubic meters",
        "notes": "", "source_dataset": "wb1971-table8.9-production-and-consumption-of-gas",
    })
write_out(OUT_OIL, "gas_production_consumption_1965_69.csv", rows)
n_written += 1

# ---------- 13. Electric power generation by plant and use, 1968-1972 ----------
print("13. electric_power_generation_by_use_1968_72.csv")
raw = read_raw("wb1974-electric-power-generation-by-use-1968-1972")
rows = []
for r in raw:
    rows.append({
        "fiscal_year_label": r["year"], "year": int(r["year"]),
        "category": "Electric Power Generation by Use", "subcategory": f"{r['company_or_aggregate']} — {r['use_category']}",
        "value": r["value"], "unit": r["unit"],
        "notes": r.get("note", ""), "source_dataset": "wb1974-table15.3-electric-power-generation-by-plant-and-use",
    })
write_out(OUT_OIL, "electric_power_generation_by_use_1968_72.csv", rows)
n_written += 1

# ---------- 14. Power generating capacity by prime mover, 1970-1971 ----------
print("14. power_generating_capacity_1970_71.csv")
raw = read_raw("wb1974-power-generating-capacity-1970-1971")
mover_cols = [("total_kw", "Total"), ("diesel_kw", "Diesel"), ("steam_kw", "Steam"),
              ("gas_kw", "Gas"), ("water_kw", "Water (Hydro)")]
rows = []
for r in raw:
    for col, subcat in mover_cols:
        rows.append({
            "fiscal_year_label": r["year"], "year": int(r["year"]),
            "category": r["region_or_dam"], "subcategory": subcat,
            "value": r.get(col, ""), "unit": "kW (installed capacity)",
            "notes": "", "source_dataset": "wb1974-table15.2-power-generating-capacity",
        })
write_out(OUT_OIL, "power_generating_capacity_1970_71.csv", rows)
n_written += 1

# ---------- 15. AIOC profits, UK taxes & Iran royalties, 1910-1951 ----------
print("15. aioc_profits_uk_taxes_iran_royalties_1910_51.csv")
raw = read_raw("usbm1963-aioc-profits-royalties-1910-1951", "aioc_profits_uk_taxes_iran_royalties_1910_1951.csv")
metric_cols_15 = [("net_profit_gbp_thousand", "Net Profit"), ("uk_taxes_gbp_thousand", "UK Taxes"),
                   ("royalty_payments_to_iran_gbp_thousand", "Royalty Payments to Iran")]
rows = []
for r in raw:
    label = r["year"]
    yr = dualyear_to_year(label) if re.fullmatch(r"\d{4}", label) else ""
    for col, subcat in metric_cols_15:
        rows.append({
            "fiscal_year_label": label, "year": yr,
            "category": "AIOC Profits, UK Tax & Iran Royalty Payments", "subcategory": subcat,
            "value": r.get(col, ""), "unit": "GBP thousand",
            "notes": r.get("notes", ""), "source_dataset": "usbm1963-aioc-profits-royalties-1910-1951",
        })
write_out(OUT_OIL, "aioc_profits_uk_taxes_iran_royalties_1910_51.csv", rows)
n_written += 1

# ---------- 16. Consortium disbursements, 1954-1962 (incl. wages) ----------
print("16. consortium_disbursements_1954_62.csv")
raw = read_raw("usbm1963-consortium-disbursements-1954-1962", "consortium_disbursements_1954_1962.csv")
rows = []
for r in raw:
    label = r["year"]
    yr = dualyear_to_year(label) if re.fullmatch(r"\d{4}", label) else ""
    rows.append({
        "fiscal_year_label": label, "year": yr,
        "category": r["category"], "subcategory": r.get("subcategory", ""),
        "value": r.get("value", ""), "unit": r["unit"],
        "notes": r.get("notes", ""), "source_dataset": "usbm1963-consortium-disbursements-1954-1962",
    })
write_out(OUT_OIL, "consortium_disbursements_1954_62.csv", rows)
n_written += 1

# ---------- 17. Oil industry employment by nationality, 1939-1960 ----------
print("17. oil_industry_employment_by_nationality_1939_60.csv")
raw = read_raw("usbm1963-oil-industry-employment-1939-1960", "oil_industry_employment_by_nationality_1939_1960.csv")
nat_cols = [("iranian", "Iranian"), ("non_iranian", "Non-Iranian"), ("not_specified", "Not Specified"),
            ("total", "Total")]
rows = []
for r in raw:
    label = r["year"]
    yr = dualyear_to_year(label) if re.fullmatch(r"\d{4}", label) else ""
    for col, subcat in nat_cols:
        val = r.get(col, "")
        if val == "":
            continue  # e.g. the 1950 and 1952-54 rows are entirely blank -- skip rather than write empty rows
        rows.append({
            "fiscal_year_label": label, "year": yr,
            "category": "Oil Industry Employment by Nationality", "subcategory": subcat,
            "value": val, "unit": "count (persons employed)",
            "notes": r.get("notes", ""), "source_dataset": "usbm1963-oil-industry-employment-1939-1960",
        })
write_out(OUT_OIL, "oil_industry_employment_by_nationality_1939_60.csv", rows)
n_written += 1

# ---------- 18. Oil industry personnel by company & category, 1955-1961 ----------
print("18. oil_industry_personnel_by_company_category_1955_61.csv")
raw = read_raw("usbm1963-oil-industry-personnel-by-category-1955-1961", "oil_industry_personnel_by_company_category_1955_1961.csv")
rows = []
for r in raw:
    label = r["year"]
    yr = dualyear_to_year(label) if re.fullmatch(r"\d{4}", label) else ""
    rows.append({
        "fiscal_year_label": label, "year": yr,
        "category": r["company"], "subcategory": r["category"],
        "value": r.get("value", ""), "unit": "count (persons employed)",
        "notes": r.get("notes", ""), "source_dataset": "usbm1963-oil-industry-personnel-by-category-1955-1961",
    })
write_out(OUT_OIL, "oil_industry_personnel_by_company_category_1955_61.csv", rows)
n_written += 1

# ---------- 19. Oil revenue distribution by recipient, 1957-1959 ----------
print("19. oil_revenue_distribution_1957_59.csv")
raw = read_raw("usbm1963-oil-revenue-distribution-1957-1959", "oil_revenue_distribution_1957_1959.csv")
rows = []
for r in raw:
    rows.append({
        "fiscal_year_label": r["year"], "year": int(r["year"]),
        "category": "Oil Revenue Distribution by Recipient", "subcategory": r["recipient"],
        "value": r["share_percent"], "unit": "percent",
        "notes": r.get("notes", ""), "source_dataset": "usbm1963-oil-revenue-distribution-1957-1959",
    })
write_out(OUT_OIL, "oil_revenue_distribution_1957_59.csv", rows)
n_written += 1

print(f"\nTOTAL files written: {n_written}")
