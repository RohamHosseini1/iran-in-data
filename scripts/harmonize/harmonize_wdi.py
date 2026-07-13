"""Melt World Bank WDI bulk CSV (wide-by-year) into the project's long tidy format,
filtered to the project's country set. Keeps ALL ~1,600 WDI indicators -- World Bank's own
curation is already broad and this is the macro backbone, so no further indicator filtering.
"""
import csv
import sys

sys.path.insert(0, "scripts/harmonize")
from country_crosswalk import COUNTRIES

SRC = "data/raw/worldbank-wdi/wdi-bulk-csv/WDICSV.csv"
OUT = "data/processed/macro_wdi.csv"


def main():
    year_cols = None
    rows_out = 0
    with open(SRC, encoding="utf-8-sig", newline="") as f_in, open(
        OUT, "w", encoding="utf-8", newline=""
    ) as f_out:
        reader = csv.DictReader(f_in)
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
        for row in reader:
            iso3 = row["Country Code"]
            if iso3 not in COUNTRIES:
                continue
            if year_cols is None:
                year_cols = [
                    k for k in row.keys() if k.isdigit() and 1900 <= int(k) <= 2100
                ]
            for yr in year_cols:
                val = row[yr]
                if val is None or val == "":
                    continue
                writer.writerow(
                    [
                        iso3,
                        COUNTRIES[iso3],
                        row["Indicator Code"],
                        row["Indicator Name"],
                        yr,
                        f"{yr}-01-01",
                        val,
                        "",
                        "worldbank-wdi",
                        "WDICSV.csv",
                    ]
                )
                rows_out += 1
    print(f"wrote {rows_out} rows -> {OUT}")


if __name__ == "__main__":
    main()
