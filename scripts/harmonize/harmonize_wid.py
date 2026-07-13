"""Harmonize WID.world per-country CSVs (semicolon-delimited, 2-letter country codes) into the
project's long tidy format. Drops empty-value rows (WID ships the full variable grid per country
even where a cell was never estimated).
"""
import csv
import glob
import sys

sys.path.insert(0, "scripts/harmonize")
from country_crosswalk import COUNTRIES

# WID's 2-letter codes -> our ISO3 (only the ones we actually collected)
WID_TO_ISO3 = {
    "IR": "IRN", "KR": "KOR", "TR": "TUR", "SA": "SAU", "VE": "VEN",
    "US": "USA", "RU": "RUS", "SU": "SUN",  # USSR: WID has average income only (1950-), no share data
    "ES": "ESP", "PT": "PRT", "GR": "GRC", "DE": "DEU",
}

OUT = "data/processed/inequality_wid_world.csv"


def main():
    files = glob.glob("data/raw/wid-world/country-*/country-*_data_*.csv")
    rows_out = 0
    with open(OUT, "w", encoding="utf-8", newline="") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(
            ["country_iso3", "country_name", "year", "date", "percentile_group",
             "wid_variable_code", "value", "data_quality_score", "source_dataset"]
        )
        for fpath in sorted(files):
            with open(fpath, encoding="utf-8", errors="replace", newline="") as f_in:
                lines = f_in.readlines()
            # first line is a "Downloaded from wid.world on ..." banner, not a header
            reader = csv.DictReader(lines[1:], delimiter=";")
            for row in reader:
                wid_code = row.get("Country", "").strip()
                iso3 = WID_TO_ISO3.get(wid_code)
                if not iso3:
                    continue
                val = row.get("Value", "").strip()
                if not val:
                    continue
                year = row.get("Year", "").strip()
                writer.writerow(
                    [
                        iso3,
                        COUNTRIES.get(iso3, iso3),
                        year,
                        f"{year}-01-01" if year.lstrip("-").isdigit() else "",
                        row.get("Percentile", ""),
                        row.get("Variable", ""),
                        val,
                        row.get("DataQuality", ""),
                        "wid-world",
                    ]
                )
                rows_out += 1
    print(f"wrote {rows_out} rows from {len(files)} WID country files -> {OUT}")


if __name__ == "__main__":
    main()
