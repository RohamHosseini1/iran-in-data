#!/usr/bin/env python3
"""
apply_roster.py -- apply the final comparator roster to materialized charts.

Final roster (owner decision 2026-07-14):
  IRN (hero) + TUR SAU IRQ VEN ARG RUS USA KOR ESP ITA
Dropped from display: DEU FRA GBR NLD PRT SWE GRC (kept in data/processed).

Surgical, per-chart edit of data/charts/<id>/data.csv:
  1. drop rows for dropped countries;
  2. for machine-source charts (wdi/weo/owid/faostat), append IRQ (Iraq) rows
     pulled from data/processed using the same underlying_codes logic as
     build_layer3_charts.py -- Iraq was just harmonized in.
meta.json's "countries" and "year_range" are recomputed; every other meta field
(title, title_fa, category_fa, citations, currency_display, ...) is preserved.

Idempotent: dropped countries stay dropped; IRQ isn't double-added.
"""
import csv, json, os, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REGISTRY = os.path.join(ROOT, "data", "processed", "CHART_REGISTRY.csv")
CHARTS = os.path.join(ROOT, "data", "charts")
csv.field_size_limit(sys.maxsize)

ROSTER = {"IRN", "TUR", "SAU", "IRQ", "VEN", "ARG", "RUS", "USA", "KOR", "ESP", "ITA"}
DROP = {"DEU", "FRA", "GBR", "NLD", "PRT", "SWE", "GRC"}

WDI_FILE = os.path.join(ROOT, "data", "processed", "macro_wdi.csv")
WEO_FILE = os.path.join(ROOT, "data", "processed", "macro_imf_weo.csv")
OWID_FILE = os.path.join(ROOT, "data", "processed", "owid_indicators.csv")
FAOSTAT_FILES = {
    "qcl": "agriculture_qcl_production.csv", "fbs": "agriculture_fbs_food_balances.csv",
    "fbsh": "agriculture_fbsh_food_balances_historic.csv",
    "pp": "agriculture_pp_producer_prices.csv", "pa": "agriculture_pa_prices_archive_pre1991.csv",
}
PROD_EL = {"Production", "Area harvested", "Yield", "Yield/Carcass Weight",
           "Producing Animals/Slaughtered", "Stocks", "Milk Animals", "Laying"}
TRADE_EL = {"Export quantity", "Import quantity", "Domestic supply quantity"}
CONS_EL = {"Food supply (kcal/capita/day)", "Food supply quantity (kg/capita/yr)",
           "Protein supply quantity (g/capita/day)", "Fat supply quantity (g/capita/day)", "Food"}


def slugify(cid):
    return cid.replace("/", "_")


def load_irq_indexed(path, key_field):
    idx = defaultdict(list)
    with open(path, newline='', encoding='utf-8', errors='replace') as f:
        for row in csv.DictReader(f):
            if row.get("value") and row.get("country_iso3") == "IRQ":
                idx[row[key_field]].append(row)
    return idx


def main():
    print("Indexing IRQ rows from processed sources...")
    wdi_idx = load_irq_indexed(WDI_FILE, "indicator_id")
    weo_idx = load_irq_indexed(WEO_FILE, "indicator_id")
    owid_idx = load_irq_indexed(OWID_FILE, "indicator_id")
    fao_idx = {}
    for key, fn in FAOSTAT_FILES.items():
        idx = defaultdict(list)
        with open(os.path.join(ROOT, "data", "processed", fn), newline='', encoding='utf-8', errors='replace') as f:
            for row in csv.DictReader(f):
                if row.get("value") and row.get("country_iso3") == "IRQ":
                    idx[(row["item"], row["element"])].append(row)
        fao_idx[key] = idx

    reg = {r["chart_id"]: r for r in csv.DictReader(open(REGISTRY, encoding='utf-8'))}

    def irq_rows_for(cid):
        r0 = reg.get(cid)
        out = []
        if cid.startswith("wdi__"):
            for code in r0["underlying_codes"].split("|"):
                for r in wdi_idx.get(code, []):
                    out.append((r, code, r.get("indicator_label", ""), "wdi", r.get("unit", "")))
        elif cid.startswith("weo__"):
            for code in r0["underlying_codes"].split("|"):
                for r in weo_idx.get(code, []):
                    out.append((r, code, r.get("indicator_label", ""), "imf-weo", r.get("unit", "")))
        elif cid.startswith("owid__"):
            code = r0["underlying_codes"]
            for r in owid_idx.get(code, []):
                out.append((r, code, r.get("indicator_label", ""), "owid", r.get("unit", "")))
        elif cid.startswith("faostat__"):
            parts = cid.split("__")
            item, angle = parts[1], parts[2]
            domains = {"production": ["qcl"], "trade": ["fbs", "fbsh"],
                       "consumption": ["fbs", "fbsh"], "price": ["pp", "pa"]}.get(angle, [])
            el_set = {"production": PROD_EL, "trade": TRADE_EL, "consumption": CONS_EL,
                      "price": None}.get(angle)
            for dom in domains:
                for (it, el), recs in fao_idx[dom].items():
                    if it != item or (el_set is not None and el not in el_set):
                        continue
                    for r in recs:
                        out.append((r, f"{dom}:{el}", el, f"faostat-{dom}", r.get("unit", "")))
        return out

    FIELDS = ["country_iso3", "country_name", "year", "value", "unit",
              "variant_code", "variant_label", "source_dataset"]
    dropped_rows = added_irq = touched = 0
    for name in sorted(os.listdir(CHARTS)):
        folder = os.path.join(CHARTS, name)
        dpath = os.path.join(folder, "data.csv")
        if not os.path.isdir(folder) or not os.path.exists(dpath):
            continue
        with open(dpath, newline='', encoding='utf-8') as f:
            rd = csv.DictReader(f)
            cols = rd.fieldnames
            rows = list(rd)
        n0 = len(rows)
        rows = [r for r in rows if r.get("country_iso3") not in DROP]
        d = n0 - len(rows)

        cid = None  # recover chart_id from meta (folder name is slugified)
        mpath = os.path.join(folder, "meta.json")
        meta = None
        if os.path.exists(mpath):
            try:
                meta = json.load(open(mpath, encoding='utf-8'))
                cid = meta.get("chart_id")
            except Exception:
                meta = None
        cid = cid or name

        a = 0
        has_irq = any(r.get("country_iso3") == "IRQ" for r in rows)
        if not has_irq and (cid.startswith(("wdi__", "weo__", "owid__", "faostat__"))):
            for (r, vcode, vlabel, sds, unit) in irq_rows_for(cid):
                rows.append({"country_iso3": "IRQ", "country_name": "Iraq", "year": r["year"],
                             "value": r["value"], "unit": unit, "variant_code": vcode,
                             "variant_label": vlabel, "source_dataset": sds})
                a += 1

        if d == 0 and a == 0:
            continue
        # write data.csv (preserve original column order)
        with open(dpath, "w", newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for r in rows:
                w.writerow({k: r.get(k, "") for k in cols})
        # update meta countries + year_range only
        if meta is not None:
            meta["countries"] = sorted(set(r["country_iso3"] for r in rows if r.get("country_iso3")))
            yrs = sorted(set(r["year"] for r in rows if r.get("year")))
            if yrs:
                meta["year_range"] = [yrs[0], yrs[-1]]
            meta["n_rows"] = len(rows)
            with open(mpath, "w", encoding='utf-8') as f:
                json.dump(meta, f, indent=2, ensure_ascii=False)
        dropped_rows += d
        added_irq += a
        touched += 1

    print(f"charts touched: {touched} | dropped-country rows removed: {dropped_rows} | IRQ rows added: {added_irq}")


if __name__ == "__main__":
    main()
