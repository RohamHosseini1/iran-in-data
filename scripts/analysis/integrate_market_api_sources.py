#!/usr/bin/env python3
"""
integrate_market_api_sources.py -- add the navasan daily series to the FX and
gold-coin charts as an INDEPENDENT SECOND SOURCE (owner rule: same measure =>
multi-source on the existing chart, never a new chart).

navasan was cross-validated against the existing TGJU series on ~2,000 overlapping
days (median ratio 1.0002) -- they agree, so this is corroboration + coverage, not
a contested estimate. Both are kept as separately-labelled variants so the reader
can see two independent providers agreeing; TGJU stays the default.

Also appends the navasan citation to each chart. Idempotent (drops any previously
inserted navasan rows before re-adding).
"""
import csv, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHARTS = os.path.join(ROOT, "data", "charts")
SERIES = os.path.join(ROOT, "data", "processed", "iran_api_market_series")
REG = os.path.join(ROOT, "data", "processed", "CHART_REGISTRY.csv")
csv.field_size_limit(sys.maxsize)

CITATION = {
    "source_org": "Navasan (nosan.tech) currency & gold API",
    "source_url": "http://api.navasan.tech/ohlcSearch/ (API key redacted)",
    "access_date": "2026-07-14",
    "time_range": "2019-2026",
}

# chart_id -> (series file, indicator_id in that file, new variant_code, variant_label)
JOBS = [
    ("fx__official_vs_parallel_gap_irn",
     "usd_irr_navasan_brsapi_cbi_2026.csv", "usd_irr_parallel_rate",
     "PARALLEL_NAVASAN", "Parallel rate (Navasan, independent source)"),
    ("iran_fx__gold_coin_bahar_azadi_price_daily_2013_2026",
     "gold_coin_bahar_azadi_navasan_brsapi_2026.csv", "gold_coin_bahar_azadi_price",
     "BAHAR_NAVASAN", "Bahar Azadi price (Navasan, independent source)"),
    ("iran_fx__gold_coin_emami_price_daily_2010_2026",
     "gold_coin_emami_navasan_brsapi_2026.csv", "gold_coin_emami_price",
     "EMAMI_NAVASAN", "Emami price (Navasan, independent source)"),
]


def main():
    reg = {r["chart_id"]: r for r in csv.DictReader(open(REG, encoding="utf-8"))}
    with open(REG, newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        fields = rd.fieldnames
        regrows = list(rd)

    for cid, fn, ind, vcode, vlabel in JOBS:
        cpath = os.path.join(CHARTS, cid, "data.csv")
        spath = os.path.join(SERIES, fn)
        if not (os.path.exists(cpath) and os.path.exists(spath)):
            print(f"  !! skip {cid} (missing chart or series)")
            continue

        with open(cpath, newline="", encoding="utf-8") as f:
            rd = csv.DictReader(f)
            cols = rd.fieldnames
            rows = [r for r in rd if r.get("variant_code") != vcode]  # idempotent
        before = len(rows)

        added = 0
        seen = set()
        for s in csv.DictReader(open(spath, newline="", encoding="utf-8")):
            if s.get("indicator_id") != ind:
                continue
            # prefer the daily ohlcSearch close rows; skip the single /latest/ snapshot dupes
            date = (s.get("date") or "").strip()
            val = (s.get("value") or "").strip()
            if not date or not val or date in seen:
                continue
            seen.add(date)
            year = date[:4]
            # match the existing TGJU period-label format on these charts (YYYY/MM/DD)
            date = date.replace("-", "/")
            row = {c: "" for c in cols}
            row.update({
                "country_iso3": "IRN", "country_name": "Iran", "year": year,
                "value": val, "unit": s.get("unit", ""),
                "variant_code": vcode, "variant_label": vlabel,
                "source_dataset": "navasan-api",
            })
            if "original_period_label" in cols:
                row["original_period_label"] = date
            rows.append(row)
            added += 1

        with open(cpath, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)

        # citation + meta
        mp = os.path.join(CHARTS, cid, "meta.json")
        if os.path.exists(mp):
            meta = json.load(open(mp, encoding="utf-8"))
            cits = meta.get("citations") or []
            if not any(c.get("source_org", "").startswith("Navasan") for c in cits):
                cits.append(CITATION)
            meta["citations"] = cits
            meta["n_rows"] = len(rows)
            json.dump(meta, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

        for r in regrows:
            if r["chart_id"] == cid:
                try:
                    cj = json.loads(r["citations_json"]) if r["citations_json"] else []
                except Exception:
                    cj = []
                if not any(c.get("source_org", "").startswith("Navasan") for c in cj):
                    cj.append(CITATION)
                    r["citations_json"] = json.dumps(cj, ensure_ascii=False)
                alt = r.get("alt_sources") or ""
                if "navasan" not in alt:
                    r["alt_sources"] = (alt + "|navasan-api").strip("|")

        print(f"  {cid}: +{added} navasan rows (chart {before} -> {len(rows)})")

    with open(REG, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(regrows)
    print("done")


if __name__ == "__main__":
    main()
