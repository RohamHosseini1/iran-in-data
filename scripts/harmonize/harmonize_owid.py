"""Concatenate OWID grapher CSVs (each: Entity,Code,Year,<metric>[,extra cols]) into the
project's long tidy format, filtered to the project's country set. Skips the two big
multi-indicator 'panel' files (owid-energy-data.csv, owid-co2-data.csv) -- those have a
different wide-by-indicator shape and are handled separately if/when needed.
"""
import csv
import glob
import sys

sys.path.insert(0, "scripts/harmonize")
from country_crosswalk import COUNTRIES

SRC_GLOB = "data/raw/owid/**/*.csv"
OUT = "data/processed/owid_indicators.csv"
SKIP_SUBSTR = ["-panel", "codebook"]


def main():
    files = [
        f
        for f in glob.glob(SRC_GLOB, recursive=True)
        if not any(s in f for s in SKIP_SUBSTR) and not f.endswith(".metadata.json")
    ]
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
        for fpath in sorted(files):
            indicator_id = fpath.split("/")[-1].removesuffix(".csv")
            try:
                with open(fpath, encoding="utf-8-sig", newline="") as f_in:
                    reader = csv.DictReader(f_in)
                    fieldnames = reader.fieldnames or []
                    if not {"Entity", "Code", "Year"}.issubset(fieldnames):
                        print(f"SKIP (unexpected columns): {fpath}")
                        continue
                    metric_cols = [
                        c for c in fieldnames if c not in ("Entity", "Code", "Year")
                    ]
                    for row in reader:
                        iso3 = row["Code"]
                        if iso3 not in COUNTRIES:
                            continue
                        for metric_col in metric_cols:
                            val = row.get(metric_col)
                            if val is None or val == "":
                                continue
                            # skip obviously non-numeric annotation columns
                            try:
                                float(val)
                            except ValueError:
                                continue
                            year = row["Year"]
                            writer.writerow(
                                [
                                    iso3,
                                    COUNTRIES[iso3],
                                    f"{indicator_id}__{metric_col}"
                                    if len(metric_cols) > 1
                                    else indicator_id,
                                    metric_col,
                                    year,
                                    f"{year}-01-01",
                                    val,
                                    "",
                                    "owid",
                                    fpath.split("data/raw/owid/")[-1],
                                ]
                            )
                            rows_out += 1
            except Exception as e:
                print(f"ERROR on {fpath}: {e}")
    print(f"wrote {rows_out} rows from {len(files)} OWID files -> {OUT}")


if __name__ == "__main__":
    main()
