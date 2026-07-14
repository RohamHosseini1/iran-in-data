#!/usr/bin/env python3
"""
scan_chart_quality.py -- objective data-quality scan of every live chart.

The project's whole premise is: a chart is a CLEAR MEASURE plotted over TIME for
Iran, with events overlaid. A chart earns its place only if Iran itself has a
real, multi-year, *varying* series in it. This script measures exactly that, per
chart, and emits a verdict so delete/merge/enrich decisions are grounded in data
rather than vibes.

For each chart under data/charts/<id>/ it inspects the IRN rows, grouped by
variant (measure). Output: data/processed/quality_audit/chart_quality_scan.csv
Read-only; writes one report CSV. Safe to re-run.
"""
import csv, json, os, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHARTS = os.path.join(ROOT, "data", "charts")
REGISTRY = os.path.join(ROOT, "data", "processed", "CHART_REGISTRY.csv")
OUT = os.path.join(ROOT, "data", "processed", "quality_audit", "chart_quality_scan.csv")

# tunables
MIN_POINTS = 8      # a real series needs at least this many non-zero Iran points
MIN_SPAN = 8        # ...spanning at least this many years
MIN_DISTINCT = 3    # ...with at least this much variation (not a flat line)
MANY_VARIANTS = 6   # more measures than this on one chart = clutter flag

csv.field_size_limit(sys.maxsize)


def fnum(s):
    if s is None:
        return None
    s = s.strip()
    if s == "" or s.lower() in ("na", "nan", "null", "none"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def load_registry():
    reg = {}
    with open(REGISTRY) as f:
        for r in csv.DictReader(f):
            reg[r["chart_id"]] = r
    return reg


def analyze(chart_id, path):
    data_csv = os.path.join(path, "data.csv")
    if not os.path.exists(data_csv):
        return None
    # group IRN values by variant
    by_var = defaultdict(list)         # variant_label -> list of (year, value)
    all_countries = set()
    with open(data_csv) as f:
        rd = csv.DictReader(f)
        cols = rd.fieldnames or []
        iso_col = "country_iso3" if "country_iso3" in cols else ("iso3" if "iso3" in cols else "country")
        var_col = "variant_label" if "variant_label" in cols else ("variant_code" if "variant_code" in cols else None)
        for row in rd:
            iso = row.get(iso_col, "")
            all_countries.add(iso)
            if iso != "IRN":
                continue
            v = fnum(row.get("value"))
            yr = fnum(row.get("year"))
            var = row.get(var_col, "") if var_col else "(single)"
            by_var[var].append((yr, v))

    variants = list(by_var.keys())
    n_variants = len(variants)

    # per-variant metrics, pick Iran's best variant
    best = None  # (n_nonzero, span, distinct, var, ymin, ymax, n_points)
    iran_total_points = 0
    for var, pts in by_var.items():
        nonnull = [(y, v) for (y, v) in pts if v is not None]
        iran_total_points += len(nonnull)
        nonzero = [(y, v) for (y, v) in nonnull if v != 0]
        years = [y for (y, v) in nonzero if y is not None]
        distinct = len({round(v, 6) for (y, v) in nonzero})
        span = (int(max(years)) - int(min(years)) + 1) if years else 0
        ymin = int(min(years)) if years else None
        ymax = int(max(years)) if years else None
        key = (len(nonzero), span, distinct)
        if best is None or key > best[0]:
            best = (key, var, ymin, ymax, len(nonnull), distinct, span, len(nonzero))

    if best is None:
        # Iran totally absent from this chart
        return dict(chart_id=chart_id, n_variants=n_variants, n_countries=len(all_countries),
                    iran_points=0, iran_nonzero=0, iran_span=0, iran_distinct=0,
                    iran_ymin="", iran_ymax="", best_variant="", flags="NO_IRAN", verdict="DEAD")

    (_, best_var, ymin, ymax, n_nonnull, distinct, span, n_nonzero) = best

    flags = []
    if iran_total_points == 0:
        flags.append("EMPTY")
    elif n_nonzero == 0:
        flags.append("ALL_ZERO")
    if 0 < n_nonzero < MIN_POINTS:
        flags.append("SPARSE")
    if 0 < span < MIN_SPAN:
        flags.append("SHORT")
    if n_nonzero > 0 and distinct < MIN_DISTINCT:
        flags.append("FLAT")
    if n_variants > MANY_VARIANTS:
        flags.append("MANY_VARIANTS")

    # verdict
    if iran_total_points == 0 or n_nonzero == 0:
        verdict = "DEAD"
    elif n_nonzero >= MIN_POINTS and span >= MIN_SPAN and distinct >= MIN_DISTINCT:
        verdict = "OK"
    else:
        verdict = "THIN"

    return dict(chart_id=chart_id, n_variants=n_variants, n_countries=len(all_countries),
                iran_points=iran_total_points, iran_nonzero=n_nonzero, iran_span=span,
                iran_distinct=distinct, iran_ymin=ymin or "", iran_ymax=ymax or "",
                best_variant=best_var, flags="|".join(flags), verdict=verdict)


def main():
    reg = load_registry()
    live_ids = {cid for cid, r in reg.items()
                if r["status"] not in ("merged", "hidden", "deleted", "proposed") and not r["merged_into"]}
    results = []
    for name in sorted(os.listdir(CHARTS)):
        p = os.path.join(CHARTS, name)
        if not os.path.isdir(p):
            continue
        r = reg.get(name)
        if name not in live_ids:
            continue
        a = analyze(name, p)
        if a is None:
            continue
        a["title"] = (r or {}).get("title", "")
        a["category"] = (r or {}).get("category", "")
        a["primary_source"] = (r or {}).get("primary_source", "")
        results.append(a)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cols = ["chart_id", "title", "category", "primary_source", "verdict", "flags",
            "n_variants", "n_countries", "iran_points", "iran_nonzero", "iran_span",
            "iran_distinct", "iran_ymin", "iran_ymax", "best_variant"]
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for a in results:
            w.writerow({k: a.get(k, "") for k in cols})

    # summary
    from collections import Counter
    vc = Counter(a["verdict"] for a in results)
    fc = Counter()
    for a in results:
        for fl in a["flags"].split("|"):
            if fl:
                fc[fl] += 1
    print(f"scanned {len(results)} live charts -> {OUT}")
    print("verdicts:", dict(vc))
    print("flags:", dict(fc.most_common()))
    # by source family
    fam = Counter()
    dead_fam = Counter()
    for a in results:
        f0 = a["primary_source"].split("-")[0]
        fam[f0] += 1
        if a["verdict"] == "DEAD":
            dead_fam[f0] += 1
    print("DEAD by source family:", dict(dead_fam.most_common(12)))


if __name__ == "__main__":
    main()
