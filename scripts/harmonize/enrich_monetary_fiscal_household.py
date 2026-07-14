#!/usr/bin/env python3
"""
Harmonizes previously-downloaded-but-unprocessed Iran monetary/fiscal/household-consumption
raw sources into tidy long-format CSVs at
data/processed/iran_monetary_fiscal_household_enrich_series/.

Schema (per task brief): country_iso3, indicator_id, year, value, unit, source_dataset

Inputs (all already on disk from prior sessions, never harmonized):
  1. data/raw/imf-ifs-historical/iran-annual-series-extracted/data.csv
     -> money-supply/banking/national-accounts metrics only, 1937-1971
  2. data/raw/iran-data-portal/government-finance-tables/government_debt_to_central_bank_1978-2016_quarterly.xls
  3. data/raw/sci-amar/household-expenditure-detail-2001-2020/data.csv
  4. data/raw/iran-data-portal/government-finance-tables/gdp_by_final_expenditure_components_1991-2005.xlsx
"""
import csv
import os
import pandas as pd

ROOT = "/Users/rohamhosseini/Iran Economic database"
OUT = os.path.join(ROOT, "data/processed/iran_monetary_fiscal_household_enrich_series")


def write_tidy(rows, filename, fieldnames=("country_iso3", "indicator_id", "year", "value", "unit", "source_dataset")):
    path = os.path.join(OUT, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(fieldnames))
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"wrote {path} ({len(rows)} rows)")


# ---------------------------------------------------------------------------
# 1. IMF IFS historical -- money-supply/banking/national-accounts metrics only
# ---------------------------------------------------------------------------
IFS_KEEP = {
    "money_supply_currency", "money_supply_deposit_money", "money_supply_m1",
    "money_supply_total_m1", "quasi_money", "reserve_money",
    "monetary_survey_claims_on_government", "monetary_survey_claims_on_official_entities",
    "monetary_survey_claims_on_private_sector", "monetary_survey_domestic_credit_total",
    "monetary_survey_foreign_assets", "monetary_survey_total_assets",
    "central_bank_claims_on_government", "government_deposits_with_banks",
    "discount_rate", "bank_melli_domestic_credits", "bank_melli_foreign_assets",
    "bank_melli_fx_reserves", "bank_melli_gold_fx_total", "bank_melli_gold_reserves",
    "time_deposits", "short_term_assets_in_us",
    # fiscal / household-relevant national-accounts aggregates
    "government_consumption", "gross_domestic_product", "gross_national_expenditure_gnp",
    "national_income", "private_consumption_incl_stocks", "gross_fixed_capital_formation",
}


def harmonize_ifs():
    src = os.path.join(ROOT, "data/raw/imf-ifs-historical/iran-annual-series-extracted/data.csv")
    rows = []
    with open(src, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            if row["metric"] not in IFS_KEEP:
                continue
            rows.append({
                "country_iso3": "IRN",
                "indicator_id": f"imf_ifs_hist__{row['metric']}",
                "year": row["year"],
                "value": row["value"],
                "unit": row["unit"],
                "source_dataset": f"imf-ifs-historical/iran-annual-series-extracted (source_issue={row['source_issue']})",
            })
    rows.sort(key=lambda x: (x["indicator_id"], int(x["year"])))
    write_tidy(rows, "money_supply_banking_national_accounts_imf_ifs_1937_1971.csv")
    return rows


# ---------------------------------------------------------------------------
# 2. Iran Data Portal -- government debt to central bank, quarterly 1978-2016
# ---------------------------------------------------------------------------
def harmonize_govt_debt_cbi():
    src = os.path.join(ROOT, "data/raw/iran-data-portal/government-finance-tables/"
                        "government_debt_to_central_bank_1978-2016_quarterly.xls")
    df = pd.read_excel(src, header=0)
    # columns: Year (Iranian Calendar), Quarter (Iranian Calendar), Year, Quarter,
    #   Government Debt to Central Bank (Total) - Billions of Rials,
    #   Government Debt to Central Bank (Excluding Government Corporations) -  Billions of Rials,
    #   Government Corporations Debt to Central Bank -  Billions of Rials
    cols = list(df.columns)
    col_map = {
        cols[0]: "fiscal_year_ah",
        cols[1]: "quarter_ah",
        cols[2]: "year_western",
        cols[3]: "quarter_western",
        cols[4]: "total",
        cols[5]: "excl_govt_corps",
        cols[6]: "govt_corps_only",
    }
    df = df.rename(columns=col_map)
    rows = []
    metric_map = {
        "total": "govt_debt_to_cbi_total",
        "excl_govt_corps": "govt_debt_to_cbi_excl_govt_corporations",
        "govt_corps_only": "govt_corporations_debt_to_cbi",
    }
    for _, r in df.iterrows():
        if pd.isna(r["fiscal_year_ah"]):
            continue
        try:
            fy_ah = int(r["fiscal_year_ah"])
            yr_western = int(r["year_western"])
        except (ValueError, TypeError):
            continue  # footer/source-note row, not data
        period = f"{fy_ah}{r['quarter_ah']}_{yr_western}{r['quarter_western']}"
        for col, mid in metric_map.items():
            val = r[col]
            if pd.isna(val):
                continue
            rows.append({
                "country_iso3": "IRN",
                "indicator_id": f"iran_data_portal__{mid}",
                "year": period,
                "value": val,
                "unit": "billion_rials",
                "source_dataset": "iran-data-portal/government-finance-tables/government_debt_to_central_bank_1978-2016_quarterly.xls",
            })
    write_tidy(rows, "government_debt_to_central_bank_quarterly_1978_2016.csv",
               fieldnames=("country_iso3", "indicator_id", "year", "value", "unit", "source_dataset"))
    return rows


# ---------------------------------------------------------------------------
# 3. SCI household expenditure detail, 2001-2020 (already tidy, just relabel)
# ---------------------------------------------------------------------------
def harmonize_household_expenditure():
    src = os.path.join(ROOT, "data/raw/sci-amar/household-expenditure-detail-2001-2020/data.csv")
    rows = []
    with open(src, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            indicator_id = f"sci_heis__{row['area']}_{row['metric']}"
            rows.append({
                "country_iso3": "IRN",
                "indicator_id": indicator_id,
                "year": row["gregorian_start_year"],
                "value": row["value_thousand_rials"],
                "unit": "thousand_rials_per_household_per_year",
                "source_dataset": (f"sci-amar/household-expenditure-detail-2001-2020 "
                                    f"(source_table={row['source_table']}, "
                                    f"iranian_solar_year={row['iranian_solar_year']})"),
            })
    write_tidy(rows, "household_expenditure_detail_urban_rural_2001_2020.csv")
    return rows


# ---------------------------------------------------------------------------
# 4. Iran Data Portal -- GDP by final expenditure component, 1991-2005
#    (captures household final consumption expenditure at national-accounts level)
# ---------------------------------------------------------------------------
def harmonize_gdp_expenditure():
    src = os.path.join(ROOT, "data/raw/iran-data-portal/government-finance-tables/"
                        "gdp_by_final_expenditure_components_1991-2005.xlsx")
    df = pd.read_excel(src, header=None)
    # row 3 (0-indexed) has "Description" + year headers like "1370 (1991)"
    header_row_idx = None
    for i in range(len(df)):
        if str(df.iloc[i, 0]).strip() == "Description":
            header_row_idx = i
            break
    assert header_row_idx is not None, "could not locate header row"
    year_cols = {}
    for j in range(1, df.shape[1]):
        cell = df.iloc[header_row_idx, j]
        if pd.isna(cell):
            continue
        s = str(cell)
        # format "1370 (1991)"
        if "(" in s and ")" in s:
            western = s.split("(")[1].split(")")[0].strip()
            if western.isdigit():
                year_cols[j] = western

    KEEP_LABELS = {
        "Private final consumption expenditures…": "private_final_consumption_expenditure",
        "Household final consumption expenditure": "household_final_consumption_expenditure",
        "Non-profit institutions serving households (NPISHs)": "npish_final_consumption_expenditure",
        "Government final consumption expenditure": "government_final_consumption_expenditure",
        "Gross fixed capital formation…": "gross_fixed_capital_formation",
    }

    rows = []
    for i in range(header_row_idx + 1, len(df)):
        label_raw = df.iloc[i, 0]
        if pd.isna(label_raw):
            continue
        label = str(label_raw).strip()
        if label not in KEEP_LABELS:
            continue
        indicator_id = f"iran_data_portal__gdp_expenditure_{KEEP_LABELS[label]}"
        for j, western_year in year_cols.items():
            val = df.iloc[i, j]
            if pd.isna(val):
                continue
            rows.append({
                "country_iso3": "IRN",
                "indicator_id": indicator_id,
                "year": western_year,
                "value": val,
                "unit": "billion_rials_current_prices",
                "source_dataset": "iran-data-portal/government-finance-tables/gdp_by_final_expenditure_components_1991-2005.xlsx",
            })
    write_tidy(rows, "gdp_by_final_expenditure_component_1991_2005.csv")
    return rows


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    r1 = harmonize_ifs()
    r2 = harmonize_govt_debt_cbi()
    r3 = harmonize_household_expenditure()
    r4 = harmonize_gdp_expenditure()
    print("TOTAL rows:", len(r1) + len(r2) + len(r3) + len(r4))
