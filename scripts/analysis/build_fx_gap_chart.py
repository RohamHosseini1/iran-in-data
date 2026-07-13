"""Build the flagship 'Official vs. Parallel/Black-Market Exchange Rate' chart the project owner
explicitly asked for: both series side by side, plus the gap/premium between them over time, so the
chart itself tells the multi-tier-system story (divergence widening, narrowing, unification events).

This does NOT change the currency-display default used elsewhere (which correctly uses parallel-
market rates for post-1979 real/USD conversions) -- this chart's whole purpose is to show BOTH rates
together, official included, precisely so the reader can see the gap.
"""
import csv
import json
import os

OUT_DIR = "data/charts/fx__official_vs_parallel_gap_irn"
REGISTRY = "data/processed/CHART_REGISTRY.csv"
CHART_ID = "fx__official_vs_parallel_gap_irn"


def load_registry_row():
    """title/category/sources/citations come from CHART_REGISTRY.csv, never hardcoded here --
    a hardcoded copy in this script silently regressed the title (back to its pre-cleanup
    long form) and citations (dropped the IMF-IFS-historical entry, restored 2026-07-13 after
    a citation-accuracy-audit fix had been separately overwritten) the last time this ran,
    since main() always rewrote meta.json from these literals regardless of what the
    registry -- the single source of truth for these fields -- actually said."""
    with open(REGISTRY, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["chart_id"] == CHART_ID:
                return row
    raise SystemExit(f"{CHART_ID} not found in {REGISTRY}")


def load_official_all_years():
    """Official WDI rate wherever available (1960+), plus IFS 1937-1949, spanning the full period --
    this is deliberately the FULL official series, unlike fx_cpi_lookup_irn.json which only uses
    official rate for eras where it's also the real transactable rate."""
    rate = {}
    with open("data/processed/macro_wdi.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["country_iso3"] == "IRN" and row["indicator_id"] == "PA.NUS.FCRF" and row["value"]:
                rate[int(row["year"])] = float(row["value"])
    with open("data/raw/imf-ifs-historical/iran-annual-series-extracted/data.csv",
              newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["metric"] == "exchange_rate_official" and row["value"]:
                try:
                    y = int(row["year"])
                    if y not in rate:  # WDI wins on overlap, this only fills earlier years
                        rate[y] = float(row["value"])
                except ValueError:
                    pass
    return rate


def load_parallel_all_years():
    import statistics
    by_year = {}
    with open("data/processed/iran_trade_institutions_fx_series/usd_irr_parallel_rate_1979_2011.csv",
              newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                y = int(row["year"])
                v = float(row["rial_per_usd_parallel"])
            except ValueError:
                continue
            if row["frequency"] in ("monthly", "annual"):
                by_year.setdefault(y, []).append(v)
    with open("data/processed/iran_trade_institutions_fx_series/usd_irr_parallel_rate_daily_2011_2026.csv",
              newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                y = int(row["date_gregorian"].split("/")[0])
                v = float(row["close"])
            except (ValueError, IndexError):
                continue
            by_year.setdefault(y, []).append(v)
    return {y: statistics.mean(v) for y, v in by_year.items()}


def main():
    official = load_official_all_years()
    parallel = load_parallel_all_years()
    all_years = sorted(set(official) | set(parallel))

    rows = []
    for y in all_years:
        o, p = official.get(y), parallel.get(y)
        if o is not None:
            rows.append({"country_iso3": "IRN", "country_name": "Iran", "year": str(y),
                         "value": str(round(o, 4)), "unit": "rials per US$",
                         "variant_code": "OFFICIAL", "variant_label": "Official government rate",
                         "source_dataset": "wdi_ifs_official"})
        if p is not None:
            rows.append({"country_iso3": "IRN", "country_name": "Iran", "year": str(y),
                         "value": str(round(p, 4)), "unit": "rials per US$",
                         "variant_code": "PARALLEL", "variant_label": "Parallel/black-market rate",
                         "source_dataset": "bahmani_oskooee_tgju_wikipedia"})
        if o is not None and p is not None and o > 0:
            premium_pct = (p - o) / o * 100
            rows.append({"country_iso3": "IRN", "country_name": "Iran", "year": str(y),
                         "value": str(round(premium_pct, 2)), "unit": "% premium of parallel over official",
                         "variant_code": "PREMIUM_PCT", "variant_label": "Black-market premium (%)",
                         "source_dataset": "computed"})

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "data.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["country_iso3", "country_name", "year", "value", "unit",
                                           "variant_code", "variant_label", "source_dataset"])
        w.writeheader()
        w.writerows(rows)

    years_with_both = sorted(set(official) & set(parallel))
    reg = load_registry_row()
    try:
        citations = json.loads(reg["citations_json"]) if reg.get("citations_json") else []
    except json.JSONDecodeError:
        citations = []
    meta = {
        "chart_id": CHART_ID,
        "title": reg["title"],
        "category": reg["category"],
        "sources": reg["primary_source"],
        "n_rows": len(rows),
        "year_range": [str(all_years[0]), str(all_years[-1])],
        "countries": ["IRN"],
        "years_with_both_series_for_gap_calc": len(years_with_both),
        "notes": "Pre-1979 (Pahlavi era) the two series are expected to sit very close together "
                 "(no meaningful parallel market under the pre-revolution convertible economy) -- "
                 "watch for the gap opening sharply at the 1979 revolution, narrowing to ~0 during "
                 "the genuinely unified 2002-2010 window, then reopening from ~2010-2011 onward with "
                 "sanctions escalation. This chart exists specifically to make that story visible.",
        "citations": citations,
    }
    with open(os.path.join(OUT_DIR, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"Chart built: {OUT_DIR}")
    print(f"Years covered: {all_years[0]}-{all_years[-1]}, {len(rows)} rows")
    print(f"Years with BOTH official and parallel (gap computable): {len(years_with_both)}")


if __name__ == "__main__":
    main()
