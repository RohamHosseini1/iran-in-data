"""Melt the Maddison Project Database 2023 'Full data' sheet into the project's long tidy
format, filtered to the project's country set. Uniquely goes back to year 1 AD (sparse until
~1820, dense annually after) -- the deepest history of any source in this project.
"""
import csv
import sys

import pandas as pd

sys.path.insert(0, "scripts/harmonize")
from country_crosswalk import COUNTRIES

SRC = "data/raw/maddison-project/mpd-2023/mpd2023_web.xlsx"
OUT = "data/processed/macro_maddison.csv"

INDICATORS = {
    "gdppc": ("maddison.gdppc", "GDP per capita (2011 international $, PPP)"),
    "pop": ("maddison.pop", "Population (thousands)"),
}


def main():
    df = pd.read_excel(SRC, sheet_name="Full data")
    df = df[df["countrycode"].isin(COUNTRIES.keys())]

    rows_out = 0
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
                "source_dataset",
                "source_file",
            ]
        )
        for _, row in df.iterrows():
            iso3 = row["countrycode"]
            year = int(row["year"])
            for col, (indicator_id, label) in INDICATORS.items():
                val = row[col]
                if pd.isna(val):
                    continue
                writer.writerow(
                    [
                        iso3,
                        COUNTRIES[iso3],
                        indicator_id,
                        label,
                        year,
                        f"{year:04d}-01-01",
                        val,
                        "2011 international $" if col == "gdppc" else "thousands",
                        "maddison-project",
                        "mpd2023_web.xlsx",
                    ]
                )
                rows_out += 1
    print(f"wrote {rows_out} rows -> {OUT}")


if __name__ == "__main__":
    main()
