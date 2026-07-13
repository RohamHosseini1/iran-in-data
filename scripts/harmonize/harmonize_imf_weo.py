"""Melt the IMF WEO April 2026 'Countries' sheet (wide-by-year) into the project's long
tidy format, filtered to the project's country set. Includes IMF's 5-year-ahead forecast
columns -- kept and flagged via year (no separate 'is_forecast' column needed since IMF's
own LATEST_ACTUAL_ANNUAL_DATA column tells you the cutoff; recorded per-row).
"""
import csv
import re
import sys

import pandas as pd


def extract_year(val):
    """LATEST_ACTUAL_ANNUAL_DATA is usually a plain year but sometimes a fiscal-year
    string like 'FY2024/25' -- pull the first 4-digit year out of whatever it is."""
    m = re.search(r"\d{4}", str(val))
    return int(m.group()) if m else None

sys.path.insert(0, "scripts/harmonize")
from country_crosswalk import COUNTRIES

SRC = "data/raw/imf-weo/weo-entire-dataset-2026-april/WEOApr2026all.xlsx"
OUT = "data/processed/macro_imf_weo.csv"


def main():
    df = pd.read_excel(SRC, sheet_name="Countries")
    df = df[df["COUNTRY.ID"].isin(COUNTRIES.keys())]

    year_cols = [c for c in df.columns if isinstance(c, int)]

    id_cols = [
        "COUNTRY.ID",
        "INDICATOR.ID",
        "INDICATOR",
        "UNIT",
        "LATEST_ACTUAL_ANNUAL_DATA",
    ]
    long_df = df.melt(
        id_vars=id_cols, value_vars=year_cols, var_name="year", value_name="value"
    )
    long_df = long_df.dropna(subset=["value"])

    with open(OUT, "w", encoding="utf-8", newline="") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(
            [
                "country_iso3",
                "country_name",
                "indicator_id",
                "indicator_label",
                "year",
                "date",
                "value",
                "unit",
                "is_actual",
                "source_dataset",
                "source_file",
            ]
        )
        for _, row in long_df.iterrows():
            iso3 = row["COUNTRY.ID"]
            year = int(row["year"])
            latest_actual_year = extract_year(row["LATEST_ACTUAL_ANNUAL_DATA"])
            is_actual = (
                (year <= latest_actual_year) if latest_actual_year is not None else ""
            )
            writer.writerow(
                [
                    iso3,
                    COUNTRIES[iso3],
                    row["INDICATOR.ID"],
                    row["INDICATOR"],
                    year,
                    f"{year}-01-01",
                    row["value"],
                    row["UNIT"] if pd.notna(row["UNIT"]) else "",
                    is_actual,
                    "imf-weo",
                    "WEOApr2026all.xlsx",
                ]
            )
    print(f"wrote {len(long_df)} rows -> {OUT}")


if __name__ == "__main__":
    main()
