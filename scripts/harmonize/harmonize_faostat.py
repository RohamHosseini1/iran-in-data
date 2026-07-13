"""Filter FAOSTAT's normalized bulk CSVs (already long-format: Area,Item,Element,Year,
Unit,Value) down to the project's country set, standardizing Area names to ISO3. Keeps
ALL items/elements for our countries (not just chicken/citrus) -- FAOSTAT's own item
taxonomy is already granular and this preserves the full agricultural encyclopedia for our
country set. One output file per FAOSTAT domain, all sharing the same tidy schema.
"""
import csv
import sys

sys.path.insert(0, "scripts/harmonize")
from country_crosswalk import FAOSTAT_AREA_TO_ISO3, COUNTRIES

DOMAINS = {
    "qcl-production": (
        'data/raw/faostat/qcl-production/Production_Crops_Livestock_E_All_Data_(Normalized).csv',
        "data/processed/agriculture_qcl_production.csv",
    ),
    "fbs-food-balances": (
        'data/raw/faostat/fbs-food-balances/FoodBalanceSheets_E_All_Data_(Normalized).csv',
        "data/processed/agriculture_fbs_food_balances.csv",
    ),
    "fbsh-food-balances-historic": (
        'data/raw/faostat/fbsh-food-balances-historic/FoodBalanceSheetsHistoric_E_All_Data_(Normalized).csv',
        "data/processed/agriculture_fbsh_food_balances_historic.csv",
    ),
    "pp-producer-prices": (
        'data/raw/faostat/pp-producer-prices/Prices_E_All_Data_(Normalized).csv',
        "data/processed/agriculture_pp_producer_prices.csv",
    ),
    "pa-prices-archive": (
        'data/raw/faostat/pa-prices-archive/PricesArchive_E_All_Data_(Normalized).csv',
        "data/processed/agriculture_pa_prices_archive_pre1991.csv",
    ),
    "cp-consumer-price-indices": (
        'data/raw/faostat/cp-consumer-price-indices/ConsumerPriceIndices_E_All_Data_(Normalized).csv',
        "data/processed/food_cpi_faostat.csv",
    ),
}


def process_one(src_path, out_path, domain_slug):
    rows_out = 0
    skipped_areas = 0
    with open(src_path, encoding="utf-8", errors="replace", newline="") as f_in, open(
        out_path, "w", encoding="utf-8", newline=""
    ) as f_out:
        reader = csv.DictReader(f_in)
        writer = csv.writer(f_out)
        writer.writerow(
            [
                "country_iso3",
                "country_name",
                "item",
                "element",
                "indicator_id",
                "indicator_label",
                "year",
                "date",
                "value",
                "unit",
                "flag",
                "source_dataset",
                "source_file",
            ]
        )
        for row in reader:
            iso3 = FAOSTAT_AREA_TO_ISO3.get(row["Area"])
            if iso3 is None:
                continue
            val = row.get("Value")
            if val is None or val == "":
                continue
            year = row.get("Year")
            item = row["Item"]
            element = row["Element"]
            writer.writerow(
                [
                    iso3,
                    COUNTRIES[iso3],
                    item,
                    element,
                    f"faostat.{domain_slug}.{row.get('Item Code','')}.{row.get('Element Code','')}",
                    f"{item} — {element}",
                    year,
                    f"{year}-01-01" if str(year).isdigit() else "",
                    val,
                    row.get("Unit", ""),
                    row.get("Flag", ""),
                    f"faostat-{domain_slug}",
                    src_path.split("data/raw/")[-1],
                ]
            )
            rows_out += 1
    print(f"{domain_slug}: wrote {rows_out} rows -> {out_path}")


def main():
    for domain_slug, (src, out) in DOMAINS.items():
        try:
            process_one(src, out, domain_slug)
        except FileNotFoundError:
            print(f"{domain_slug}: SKIPPED, source file not found at {src}")


if __name__ == "__main__":
    main()
