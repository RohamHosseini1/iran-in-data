"""Materialize Layer 3: one data.csv + meta.json per chart_id under data/charts/,
for the machine-readable-source portion of CHART_REGISTRY.csv (wdi__/faostat__/
weo__/owid__/wid__ chart_ids -- the original 1,577-row base, where underlying_codes
is precisely known). Archival/hand-curated chart_ids (pahlavi__, dams_of_iran_*,
etc.) are NOT handled here -- their underlying_codes point at heterogeneous
processed-series files that need per-file inspection, deferred to a follow-up pass.

Output schema per chart: country_iso3, country_name, year, value, unit,
source_dataset, variant_code, notes. Multiple unit/currency variants of a WDI
concept, or multiple elements of a FAOSTAT angle, all land in the same file as
distinct variant_code rows -- the frontend picks which variant to plot by default,
nothing is lost.
"""
import csv
import json
import os
from collections import defaultdict

REGISTRY = "data/processed/CHART_REGISTRY.csv"
OUT_DIR = "data/charts"

WDI_FILE = "data/processed/macro_wdi.csv"
WEO_FILE = "data/processed/macro_imf_weo.csv"
OWID_FILE = "data/processed/owid_indicators.csv"
WID_FILE = "data/processed/inequality_wid_world.csv"
FAOSTAT_FILES = {
    "qcl": "data/processed/agriculture_qcl_production.csv",
    "fbs": "data/processed/agriculture_fbs_food_balances.csv",
    "fbsh": "data/processed/agriculture_fbsh_food_balances_historic.csv",
    "pp": "data/processed/agriculture_pp_producer_prices.csv",
    "pa": "data/processed/agriculture_pa_prices_archive_pre1991.csv",
}
PROD_EL = {"Production", "Area harvested", "Yield", "Yield/Carcass Weight",
           "Producing Animals/Slaughtered", "Stocks", "Milk Animals", "Laying"}
TRADE_EL = {"Export quantity", "Import quantity", "Domestic supply quantity"}
CONS_EL = {"Food supply (kcal/capita/day)", "Food supply quantity (kg/capita/yr)",
           "Protein supply quantity (g/capita/day)", "Fat supply quantity (g/capita/day)", "Food"}


def slugify(cid):
    return cid.replace("/", "_")


def load_indexed(path, key_field):
    """index rows by key_field for fast repeated lookups"""
    idx = defaultdict(list)
    with open(path, newline='', encoding='utf-8', errors='replace') as f:
        for row in csv.DictReader(f):
            if row.get("value"):
                idx[row[key_field]].append(row)
    return idx


def write_chart(chart_id, title, category, rows, sources_note):
    folder = os.path.join(OUT_DIR, slugify(chart_id))
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "data.csv"), "w", newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=["country_iso3", "country_name", "year", "value",
                                           "unit", "variant_code", "variant_label", "source_dataset"])
        w.writeheader()
        for r in rows:
            w.writerow(r)
    years = sorted(set(r["year"] for r in rows if r["year"]))
    countries = sorted(set(r["country_iso3"] for r in rows))
    meta = {
        "chart_id": chart_id, "title": title, "category": category,
        "sources": sources_note, "n_rows": len(rows),
        "year_range": [years[0], years[-1]] if years else None,
        "countries": countries,
    }
    with open(os.path.join(folder, "meta.json"), "w", encoding='utf-8') as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    return len(rows)


def main():
    print("Indexing source files (one pass each, largest first)...")
    wdi_idx = load_indexed(WDI_FILE, "indicator_id")
    weo_idx = load_indexed(WEO_FILE, "indicator_id")
    owid_idx = load_indexed(OWID_FILE, "indicator_id")
    wid_idx = defaultdict(list)
    with open(WID_FILE, newline='', encoding='utf-8', errors='replace') as f:
        for row in csv.DictReader(f):
            if row.get("value"):
                wid_idx[(row["wid_variable_code"], row["percentile_group"])].append(row)

    fao_idx = {}
    for key, path in FAOSTAT_FILES.items():
        idx = defaultdict(list)
        with open(path, newline='', encoding='utf-8', errors='replace') as f:
            for row in csv.DictReader(f):
                if row.get("value"):
                    idx[(row["item"], row["element"])].append(row)
        fao_idx[key] = idx

    built = 0
    skipped_archival = 0
    empty = 0

    with open(REGISTRY, newline='', encoding='utf-8') as f:
        registry_rows = list(csv.DictReader(f))

    for reg in registry_rows:
        cid = reg["chart_id"]
        rows = []

        if cid.startswith("wdi__"):
            codes = reg["underlying_codes"].split("|")
            for code in codes:
                for r in wdi_idx.get(code, []):
                    rows.append({"country_iso3": r["country_iso3"], "country_name": r["country_name"],
                                 "year": r["year"], "value": r["value"], "unit": r.get("unit", ""),
                                 "variant_code": code, "variant_label": r.get("indicator_label", ""),
                                 "source_dataset": "wdi"})

        elif cid.startswith("weo__"):
            codes = reg["underlying_codes"].split("|")
            for code in codes:
                for r in weo_idx.get(code, []):
                    rows.append({"country_iso3": r["country_iso3"], "country_name": r["country_name"],
                                 "year": r["year"], "value": r["value"], "unit": r.get("unit", ""),
                                 "variant_code": code, "variant_label": r.get("indicator_label", ""),
                                 "source_dataset": "imf-weo"})

        elif cid.startswith("owid__"):
            code = reg["underlying_codes"]
            for r in owid_idx.get(code, []):
                rows.append({"country_iso3": r["country_iso3"], "country_name": r["country_name"],
                             "year": r["year"], "value": r["value"], "unit": r.get("unit", ""),
                             "variant_code": code, "variant_label": r.get("indicator_label", ""),
                             "source_dataset": "owid"})

        elif cid.startswith("wid__"):
            # underlying_codes like "sptinc992j|sptinc999j_p90p100" style patterns from the build script;
            # match any wid key whose variable code is a prefix match and percentile matches if given
            spec = reg["underlying_codes"]
            for (varcode, pct), recs in wid_idx.items():
                if any(varcode.startswith(part.split("*")[0].split("_p")[0]) for part in spec.split("|")):
                    if "p90p100" in spec and pct != "p90p100":
                        continue
                    if "p99p100" in spec and pct != "p99p100":
                        continue
                    for r in recs:
                        rows.append({"country_iso3": r["country_iso3"], "country_name": r["country_name"],
                                     "year": r["year"], "value": r["value"], "unit": "",
                                     "variant_code": varcode, "variant_label": pct,
                                     "source_dataset": "wid-world"})

        elif cid.startswith("faostat__"):
            parts = cid.split("__")
            item, angle = parts[1], parts[2]
            domains = {"production": ["qcl"], "trade": ["fbs", "fbsh"],
                       "consumption": ["fbs", "fbsh"], "price": ["pp", "pa"]}.get(angle, [])
            el_set = {"production": PROD_EL, "trade": TRADE_EL, "consumption": CONS_EL,
                      "price": None}.get(angle)
            for dom in domains:
                idx = fao_idx[dom]
                for (it, el), recs in idx.items():
                    if it != item:
                        continue
                    if el_set is not None and el not in el_set:
                        continue
                    for r in recs:
                        rows.append({"country_iso3": r["country_iso3"], "country_name": r["country_name"],
                                     "year": r["year"], "value": r["value"], "unit": r.get("unit", ""),
                                     "variant_code": f"{dom}:{el}", "variant_label": el,
                                     "source_dataset": f"faostat-{dom}"})
        else:
            skipped_archival += 1
            continue

        if not rows:
            empty += 1
            continue

        write_chart(cid, reg["title"], reg["category"], rows, reg["primary_source"])
        built += 1

    print(f"Charts materialized: {built}")
    print(f"Archival/hand-curated chart_ids skipped (need a separate pass): {skipped_archival}")
    print(f"Registry rows with zero matched data (check): {empty}")


if __name__ == "__main__":
    main()
