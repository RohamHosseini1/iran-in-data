"""Harmonize the 15 Pahlavi-era government-finance/banking archival tables (already
hand-extracted + visually verified to data/raw/pahlavi-era-primary-extraction/*/data.csv)
into tidy long-format CSVs under data/processed/pahlavi_government_finance_series/.

Schema (uniform across all output files):
  fiscal_year_label, year, category, subcategory, value, unit, notes, country_iso3, source_dataset

- fiscal_year_label: the period label exactly as printed in the source (e.g. "1958/59",
  "1957-06-20", "Sept1968-Aug1969", "budget_estimate_1970/71"). Never altered/reformatted
  beyond cosmetic underscore->slash or date-dash normalization.
- year: single integer for sorting/charting. Iran's fiscal year historically ran ~March 21
  to March 20; the World Bank's own dual-year notation "1958/59" is mapped to its LATER
  Western year (1959) throughout this project (matches the convention already used in
  data/processed/iran_data_portal_deep_series and bridged_series). For snapshot dates
  (e.g. 1957_06_20) the year is read directly off the date. For estimate/projection/budget
  columns, `year` is still populated (for chart placement) but `notes` always states the
  column is an estimate/projection/budget/draft, never an actual, so charting code can
  filter or style them distinctly.
- category/subcategory: preserves the source table's row hierarchy exactly.
- No value is ever fabricated, interpolated, or recalculated -- blanks pass through as blanks.

Never touches data/raw/ (immutable). Writes only to data/processed/.
"""
import csv
import os

RAW = "data/raw/pahlavi-era-primary-extraction"
OUT = "data/processed/pahlavi_government_finance_series"
FIELDNAMES = ["fiscal_year_label", "year", "category", "subcategory", "value", "unit",
              "notes", "country_iso3", "source_dataset"]


def read_raw(dataset_dir):
    path = os.path.join(RAW, dataset_dir, "data.csv")
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_out(filename, rows):
    path = os.path.join(OUT, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writeheader()
        for r in rows:
            full = {k: r.get(k, "") for k in FIELDNAMES}
            full["country_iso3"] = "IRN"
            w.writerow(full)
    print(f"  wrote {filename}: {len(rows)} rows")


def dualyear_to_year(label):
    """'1958/59' -> 1959 ; '1962' -> 1962 ; 'proj_1970/71' -> 1971 (later Western year)."""
    core = label.split("_", 1)[-1] if label.startswith(("proj_", "first_6mo_")) else label
    if "/" in core:
        first = core.split("/")[0]
        suffix = core.split("/")[1]
        century_prefix = first[:-len(suffix)] if len(suffix) < len(first) else ""
        try:
            return int(century_prefix + suffix)
        except ValueError:
            return ""
    try:
        return int(core)
    except ValueError:
        return ""


def snapshot_to_year(label):
    # '1957_06_20' -> 1957
    return int(label.split("_")[0])


n_written = 0

# ---------- 1. Actual budget revenues 1958/59 ----------
print("1. actual_budget_revenues_1958_59.csv")
raw = read_raw("wb1960-actual-budget-revenues-1958-1959")
rows = []
for r in raw:
    rows.append({
        "fiscal_year_label": "1958/59", "year": 1959,
        "category": r["group"], "subcategory": r["line_item"],
        "value": r["1958/59"], "unit": r["unit"],
        "notes": "", "source_dataset": "wb1960-table12-actual-budget-revenues",
    })
write_out("actual_budget_revenues_1958_59.csv", rows)
n_written += 1

# ---------- 2. Actual treasury expenditures 1958/59 ----------
print("2. actual_treasury_expenditures_1958_59.csv")
raw = read_raw("wb1960-actual-treasury-expenditures-1958-1959")
rows = []
for r in raw:
    rows.append({
        "fiscal_year_label": "1958/59", "year": 1959,
        "category": r["category"], "subcategory": "",
        "value": r["1958/59"], "unit": r["unit"],
        "notes": "", "source_dataset": "wb1960-table11-actual-treasury-expenditures",
    })
write_out("actual_treasury_expenditures_1958_59.csv", rows)
n_written += 1

# ---------- 3. Budgeted vs actual expenditures 1955/56-1959/60 ----------
print("3. budgeted_vs_actual_expenditures_1955_60.csv")
raw = read_raw("wb1960-budgeted-expenditures-1955-1960")
year_cols = ["1955/56", "1956/57", "1957/58", "1958/59", "1959/60"]
rows = []
for r in raw:
    row_type = "Actual" if r["category"] == "Actual expenditure" else (
        "Budgeted total" if r["category"] == "Total budgeted expenditure" else "Budgeted (by ministry/category)")
    for yc in year_cols:
        val = r.get(yc, "")
        if val == "" and r["category"] == "Actual expenditure" and yc == "1959/60":
            note = "1959/60 actual not yet available (blank in source)"
        else:
            note = r.get("notes", "")
        rows.append({
            "fiscal_year_label": yc, "year": dualyear_to_year(yc),
            "category": r["category"], "subcategory": row_type,
            "value": val, "unit": r["unit"],
            "notes": note, "source_dataset": "wb1960-table10-budgeted-expenditures",
        })
write_out("budgeted_vs_actual_expenditures_1955_60.csv", rows)
n_written += 1

# ---------- 4. Banking statistics, private sector, 1957-1959 (June 20 snapshots) ----------
print("4. banking_statistics_private_sector_1957_59.csv")
raw = read_raw("wb1960-banking-statistics-private-sector-1957-1959")
date_cols = ["1957_06_20", "1958_06_20", "1959_06_20"]
rows = []
for r in raw:
    for dc in date_cols:
        label = dc.replace("_", "-")
        rows.append({
            "fiscal_year_label": label, "year": snapshot_to_year(dc),
            "category": r["section"], "subcategory": r["line_item"],
            "value": r.get(dc, ""), "unit": r["unit"],
            "notes": r.get("notes", ""), "source_dataset": "wb1960-table14-banking-statistics-private-sector",
        })
write_out("banking_statistics_private_sector_1957_59.csv", rows)
n_written += 1

# ---------- 5. Bank deposits, private sector, 1963/64-1969/70 ----------
print("5. bank_deposits_private_sector_1963_70.csv")
raw = read_raw("wb1971-bank-deposits-private-sector-1963-1970")
fy_cols = ["1963/64", "1964/65", "1965/66", "1966/67", "1967/68", "1968/69", "1969/70"]
rolling_cols = ["Sept1968-Aug1969", "Sept1969-Aug1970"]
rows = []
for r in raw:
    for fc in fy_cols:
        rows.append({
            "fiscal_year_label": fc, "year": dualyear_to_year(fc),
            "category": r["category"], "subcategory": "",
            "value": r.get(fc, ""), "unit": r["unit"],
            "notes": "", "source_dataset": "wb1971-table6.5-bank-deposits-private-sector",
        })
    for rc in rolling_cols:
        end_year = 1969 if "Aug1969" in rc else 1970
        rows.append({
            "fiscal_year_label": rc, "year": end_year,
            "category": r["category"], "subcategory": "",
            "value": r.get(rc, ""), "unit": r["unit"],
            "notes": "Rolling 12-month period (Sept-Aug), not aligned to the Iranian fiscal year -- do not chart interleaved with the FY columns without labeling.",
            "source_dataset": "wb1971-table6.5-bank-deposits-private-sector",
        })
write_out("bank_deposits_private_sector_1963_70.csv", rows)
n_written += 1

# ---------- 6. Money supply changes 1957-1959 (semi-annual snapshots) ----------
print("6. money_supply_changes_1957_59.csv")
raw = read_raw("wb1960-changes-in-money-supply-1957-1959")
date_cols = ["1957_06_20", "1957_12_20", "1958_06_20", "1958_12_20", "1959_06_20"]
rows = []
for r in raw:
    for dc in date_cols:
        rows.append({
            "fiscal_year_label": dc.replace("_", "-"), "year": snapshot_to_year(dc),
            "category": r["line_item"], "subcategory": "",
            "value": r.get(dc, ""), "unit": r["unit"],
            "notes": r.get("notes", ""), "source_dataset": "wb1960-table8-changes-in-money-supply",
        })
write_out("money_supply_changes_1957_59.csv", rows)
n_written += 1

# ---------- 7. Money & quasi-money changes 1964/65-1970/71 ----------
print("7. money_quasi_money_changes_1965_71.csv")
raw = read_raw("wb1971-changes-money-quasi-money-1965-1971")
fy_cols = ["1964/65", "1965/66", "1966/67", "1967/68", "1968/69", "1969/70"]
rows = []
for r in raw:
    for fc in fy_cols:
        rows.append({
            "fiscal_year_label": fc, "year": dualyear_to_year(fc),
            "category": r["category"], "subcategory": r.get("subcategory", ""),
            "value": r.get(fc, ""), "unit": "billion rials (year-over-year change, flow not level)",
            "notes": "", "source_dataset": "wb1971-table6.2-changes-money-quasi-money",
        })
    proj = r.get("proj_1970/71", "")
    if proj != "":
        rows.append({
            "fiscal_year_label": "proj_1970/71", "year": 1971,
            "category": r["category"], "subcategory": r.get("subcategory", ""),
            "value": proj, "unit": "billion rials (year-over-year change, flow not level)",
            "notes": "PROJECTION, not an actual -- report's own forward estimate for FY1970/71.",
            "source_dataset": "wb1971-table6.2-changes-money-quasi-money",
        })
    for half_col, half_label, half_year in [("first_6mo_1969/70", "first_6mo_1969/70", 1970),
                                              ("first_6mo_1970/71", "first_6mo_1970/71", 1971)]:
        v = r.get(half_col, "")
        if v != "":
            rows.append({
                "fiscal_year_label": half_label, "year": half_year,
                "category": r["category"], "subcategory": r.get("subcategory", ""),
                "value": v, "unit": "billion rials (year-over-year change, flow not level)",
                "notes": "First 6 months of the fiscal year only, not a full-year figure -- do not chart alongside full-FY columns without labeling.",
                "source_dataset": "wb1971-table6.2-changes-money-quasi-money",
            })
write_out("money_quasi_money_changes_1965_71.csv", rows)
n_written += 1

# ---------- 8. Monetary survey 1963/64-1969/70 ----------
print("8. monetary_survey_1963_70.csv")
raw = read_raw("wb1971-monetary-survey-1963-1970")
fy_cols = ["1963/64", "1964/65", "1965/66", "1966/67", "1967/68", "1968/69", "1969/70"]
rows = []
for r in raw:
    for fc in fy_cols:
        v = r.get(fc, "")
        if v == "":
            continue
        rows.append({
            "fiscal_year_label": fc, "year": dualyear_to_year(fc),
            "category": r["category"], "subcategory": r.get("subcategory", ""),
            "value": v, "unit": "billion rials (year-end stock level; 1 US$ = 75.7 rials per report)",
            "notes": "", "source_dataset": "wb1971-table6.1-monetary-survey",
        })
write_out("monetary_survey_1963_70.csv", rows)
n_written += 1

# ---------- 9. Monetary aggregates movements 1963-1973 ----------
print("9. monetary_aggregates_movements_1963_73.csv")
raw = read_raw("wb1974-movements-monetary-aggregates-1963-1973")
year_cols = [str(y) for y in range(1963, 1974)]
rows = []
for r in raw:
    for yc in year_cols:
        v = r.get(yc, "")
        if v == "":
            continue
        rows.append({
            "fiscal_year_label": yc, "year": int(yc),
            "category": r["category"], "subcategory": r.get("subcategory", ""),
            "value": v, "unit": "billion rials (year-over-year change during FY ended March 20, flow not level)",
            "notes": "", "source_dataset": "wb1974-table7.1-movements-monetary-aggregates",
        })
write_out("monetary_aggregates_movements_1963_73.csv", rows)
n_written += 1

# ---------- 10. Government revenue summary 1962/63-1971/72 ----------
print("10. government_revenue_summary_1962_72.csv")
raw = read_raw("wb1971-government-revenue-summary-1962-1972")
fy_cols = ["1962/63", "1963/64", "1964/65", "1965/66", "1966/67", "1967/68", "1968/69", "1969/70"]
special_cols = [("budget_estimate_1970/71", 1971, "BUDGET ESTIMATE for FY1970/71 (not the revised estimate, not an actual)."),
                 ("revised_estimate_1970/71", 1971, "REVISED ESTIMATE for FY1970/71 (mid-year revision, not the original budget estimate, not a final actual)."),
                 ("draft_budget_1971/72", 1972, "DRAFT BUDGET for FY1971/72, not yet enacted at time of report -- not an actual or even a passed budget.")]
rows = []
for r in raw:
    for fc in fy_cols:
        v = r.get(fc, "")
        if v == "":
            continue
        rows.append({
            "fiscal_year_label": fc, "year": dualyear_to_year(fc),
            "category": r["category"], "subcategory": "",
            "value": v, "unit": "billion rials (1 US$ = 75.7 rials per report)",
            "notes": "", "source_dataset": "wb1971-table5.2-government-revenue-summary",
        })
    for col, yr, note in special_cols:
        v = r.get(col, "")
        if v == "":
            continue
        rows.append({
            "fiscal_year_label": col, "year": yr,
            "category": r["category"], "subcategory": "",
            "value": v, "unit": "billion rials (1 US$ = 75.7 rials per report)",
            "notes": note, "source_dataset": "wb1971-table5.2-government-revenue-summary",
        })
write_out("government_revenue_summary_1962_72.csv", rows)
n_written += 1

# ---------- 11. Ordinary budget central govt expenditure 1962/63-1971/72 ----------
print("11. ordinary_budget_expenditure_1962_72.csv")
raw = read_raw("wb1971-ordinary-budget-central-govt-expenditure-1962-1972")
fy_cols = ["1962/63", "1963/64", "1964/65", "1965/66", "1966/67", "1967/68", "1968/69", "1969/70"]
special_cols = [("budget_estimate_1970/71", 1971, "BUDGET ESTIMATE for FY1970/71, not an actual."),
                 ("revised_estimate_1970/71", 1971, "REVISED ESTIMATE for FY1970/71 (mid-year revision), not a final actual."),
                 ("draft_budget_1971/72", 1972, "DRAFT BUDGET for FY1971/72, not yet enacted at time of report.")]
rows = []
for r in raw:
    for fc in fy_cols:
        v = r.get(fc, "")
        if v == "" or v == "n.a.":
            continue
        rows.append({
            "fiscal_year_label": fc, "year": dualyear_to_year(fc),
            "category": r["category"], "subcategory": r.get("subcategory", ""),
            "value": v, "unit": "billion rials (1 US$ = 75.7 rials per report)",
            "notes": "", "source_dataset": "wb1971-table5.1-ordinary-budget-expenditure",
        })
    for col, yr, note in special_cols:
        v = r.get(col, "")
        if v == "" or v == "n.a.":
            continue
        rows.append({
            "fiscal_year_label": col, "year": yr,
            "category": r["category"], "subcategory": r.get("subcategory", ""),
            "value": v, "unit": "billion rials (1 US$ = 75.7 rials per report)",
            "notes": note, "source_dataset": "wb1971-table5.1-ordinary-budget-expenditure",
        })
write_out("ordinary_budget_expenditure_1962_72.csv", rows)
n_written += 1

# ---------- 12. Central govt operations summary 1962-1973 ----------
print("12. central_govt_operations_summary_1962_73.csv")
raw = read_raw("wb1974-summary-central-govt-operations-1962-1973")
year_cols = [str(y) for y in range(1962, 1972)]
special_cols = [("preliminary_actuals_1972", 1972, "PRELIMINARY ACTUALS for 1972 -- not yet final at time of report."),
                 ("budget_estimates_1973", 1973, "BUDGET ESTIMATE for 1973, not an actual.")]
rows = []
for r in raw:
    for yc in year_cols:
        v = r.get(yc, "")
        if v == "" or v == "n.a.":
            continue
        rows.append({
            "fiscal_year_label": yc, "year": int(yc),
            "category": r["category"], "subcategory": r.get("subcategory", ""),
            "value": v, "unit": "billion rials",
            "notes": "", "source_dataset": "wb1974-table6.1-central-govt-operations-summary",
        })
    for col, yr, note in special_cols:
        v = r.get(col, "")
        if v == "" or v == "n.a.":
            continue
        rows.append({
            "fiscal_year_label": col, "year": yr,
            "category": r["category"], "subcategory": r.get("subcategory", ""),
            "value": v, "unit": "billion rials",
            "notes": note, "source_dataset": "wb1974-table6.1-central-govt-operations-summary",
        })
write_out("central_govt_operations_summary_1962_73.csv", rows)
n_written += 1

# ---------- 13. Balance of payments summary 1963/64-1969/70 ----------
print("13. balance_of_payments_summary_1963_70.csv")
raw = read_raw("wb1971-balance-of-payments-summary-1963-1970")
fy_cols = ["1963_4", "1964_5", "1965_6", "1966_7", "1967_8", "1968_9", "1969_70"]
fy_labels = {"1963_4": "1963/64", "1964_5": "1964/65", "1965_6": "1965/66", "1966_7": "1966/67",
             "1967_8": "1967/68", "1968_9": "1968/69", "1969_70": "1969/70"}
fy_years = {"1963_4": 1964, "1964_5": 1965, "1965_6": 1966, "1966_7": 1967,
            "1967_8": 1968, "1968_9": 1969, "1969_70": 1970}
rows = []
for r in raw:
    for fc in fy_cols:
        v = r.get(fc, "")
        if v == "":
            continue
        label = fy_labels[fc]
        year = fy_years[fc]
        rows.append({
            "fiscal_year_label": label, "year": year,
            "category": r["series"], "subcategory": "",
            "value": v, "unit": r["unit"],
            "notes": r.get("notes", ""), "source_dataset": "wb1971-appendix1-balance-of-payments-summary",
        })
    cagr = r.get("cagr_pct_7yr", "")
    if cagr != "":
        rows.append({
            "fiscal_year_label": "7yr_CAGR_1963_64_to_1969_70", "year": "",
            "category": r["series"], "subcategory": "7-year compound annual growth rate",
            "value": cagr, "unit": "percent (7-year CAGR)",
            "notes": r.get("notes", ""), "source_dataset": "wb1971-appendix1-balance-of-payments-summary",
        })
write_out("balance_of_payments_summary_1963_70.csv", rows)
n_written += 1

# ---------- 14. Fiscal system narrative indicators 1921-1979 ----------
print("14. fiscal_system_narrative_indicators_1921_79.csv")
raw = read_raw("iranica-fiscal-system-narrative-series-1921-1979")
rows = []
for r in raw:
    period = r["year_or_period"]
    # try to extract a single sortable year: take the first 4-digit number found
    import re
    m = re.search(r"(1[89]\d{2})", period)
    year = int(m.group(1)) if m else ""
    rows.append({
        "fiscal_year_label": period, "year": year,
        "category": r["metric"], "subcategory": "",
        "value": r["value"], "unit": r["unit"],
        "notes": f"Cited source (per Encyclopaedia Iranica article): {r['cited_source']}",
        "source_dataset": "iranica-fiscal-system-narrative-1921-1979",
    })
write_out("fiscal_system_narrative_indicators_1921_79.csv", rows)
n_written += 1

# ---------- 15. Century indicators 1900 vs 2006 (Esfahani-Pesaran) ----------
print("15. century_indicators_1900_2006.csv")
raw = read_raw("esfahani-pesaran-2008-century-indicators-1900-2006")
rows = []
for r in raw:
    v1900 = r.get("1900_rough_estimate", "")
    if v1900 != "":
        rows.append({
            "fiscal_year_label": "1900 (rough estimate)", "year": 1900,
            "category": r["indicator"], "subcategory": "",
            "value": v1900.lstrip("~") if isinstance(v1900, str) else v1900,
            "unit": r["unit"],
            "notes": "Source table presents this as a rough century-baseline estimate, not a precisely dated observation" + (" (value printed with leading '~' or uncertainty marker in source)" if isinstance(v1900, str) and ("~" in v1900 or "?" in v1900 or "<" in v1900) else ""),
            "source_dataset": "esfahani-pesaran-2008-century-indicators",
        })
    v2006 = r.get("2006", "")
    if v2006 != "":
        rows.append({
            "fiscal_year_label": "2006", "year": 2006,
            "category": r["indicator"], "subcategory": "",
            "value": v2006, "unit": r["unit"],
            "notes": "", "source_dataset": "esfahani-pesaran-2008-century-indicators",
        })
write_out("century_indicators_1900_2006.csv", rows)
n_written += 1

print(f"\nTOTAL files written: {n_written}")
