#!/usr/bin/env python3
"""
materialize_comparator_lines.py -- add comparator-country lines to the Iranian-primary
charts, which until now showed Iran alone with nothing to compare against.

KEY DESIGN POINT: the comparator series is usually NOT in the same unit as the Iranian
one (Iran's money supply is in billion rials; the cross-country indicator is broad money
as % of GDP). Plotting those on one axis would be nonsense. So each comparator series is
added as its OWN MEASURE VARIANT, carrying its own unit and containing all countries
INCLUDING Iran measured the same way. Selecting that measure shows a coherent
cross-country comparison; the Iranian-primary measure stays untouched as the default.

Nothing is spliced or interpolated across a gap: where the comparator source covers
2012-2023 and Iran's own archival series covers 1954-1980, they stay as separate
measures rather than being falsely bridged.

Idempotent: re-running replaces previously-added comparator variants.
"""
import csv, json, os, re, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROC = os.path.join(ROOT, "data", "processed")
CHARTS = os.path.join(ROOT, "data", "charts")
STAGING = os.path.join(PROC, "chart_registry_staging")
csv.field_size_limit(sys.maxsize)

STAGING_FILES = ["comparator_mining_energy.csv", "comparator_monetary_prices.csv"]

# commodity keyword in the target chart_id -> USGS indicator substring
USGS_KEY = [
    ("aluminum", "aluminum"), ("barite", "barite"), ("cement", "cement"),
    ("chromite", "chromite"), ("coke", "coke"), ("copper", "copper"),
    ("crude_steel", "crude_steel"), ("gypsum", "gypsum"), ("iron_ore", "iron_ore"),
    ("lead", "lead"), ("manganese", "manganese"), ("pig_iron", "pig_iron"),
    ("salt", "salt"), ("zinc", "zinc"), ("gas_production", "natural_gas"),
]


def humanize(s):
    s = re.sub(r"^(mining|energy)__", "", s or "")
    s = s.replace("_", " ").strip()
    return (s[:1].upper() + s[1:]) if s else s


def pick_indicators(target, rows):
    """Which indicators in this comparator file belong on this chart."""
    inds = sorted({r["indicator_id"] for r in rows})
    if len(inds) == 1:
        return inds
    t = target.lower()
    # GFDD charts encode their indicator in the chart_id (gfdd__gfdd_di_01 -> GFDD.DI.01)
    m = re.match(r"gfdd__gfdd_([a-z]{2})_(\d+)", t)
    if m:
        want = f"GFDD.{m.group(1).upper()}.{m.group(2)}"
        return [i for i in inds if i.upper() == want]
    hits = []
    for key, needle in USGS_KEY:
        if key in t:
            hits += [i for i in inds if needle in i.lower()]
    return sorted(set(hits))


def main():
    touched = added = 0
    for sf in STAGING_FILES:
        p = os.path.join(STAGING, sf)
        if not os.path.exists(p):
            continue
        for s in csv.DictReader(open(p, encoding="utf-8")):
            if s.get("status") != "extends":
                continue
            target = s.get("extends_chart_id", "").strip()
            raw = s.get("underlying_codes", "").strip()
            if not target or not raw:
                continue
            # underlying_codes may carry the indicator inline and list several files:
            #   "path/x.csv (indicator_id=mining__zinc...)"  |  "a.csv;b.csv"
            want_ind = None
            m_ind = re.search(r"indicator_id=([^)\s;|]+)", raw)
            if m_ind:
                want_ind = m_ind.group(1)
            paths = []
            for part in re.split(r"[;|]", re.sub(r"\([^)]*\)", "", raw)):
                part = part.strip()
                if not part.endswith(".csv"):
                    continue
                for cand in (os.path.join(ROOT, part), os.path.join(PROC, part)):
                    if os.path.exists(cand):
                        paths.append(cand)
                        break
            if not paths:
                print(f"  !! missing comparator file: {raw[:70]}")
                continue

            cpath = os.path.join(CHARTS, target.replace("/", "_"), "data.csv")
            if not os.path.exists(cpath):
                print(f"  !! target chart not materialized: {target}")
                continue

            srows = []
            for sp in paths:
                srows += list(csv.DictReader(open(sp, encoding="utf-8")))
            if want_ind:
                inds = [want_ind]
            else:
                inds = pick_indicators(target, srows)
                if not inds and "insurance" in target:
                    # every indicator in the insurance file is an insurance-premium
                    # measure, so all of them belong on the insurance chart
                    inds = sorted({r["indicator_id"] for r in srows})
            if not inds:
                print(f"  !! no indicator matched for {target} in {raw[:60]}")
                continue

            with open(cpath, newline="", encoding="utf-8") as f:
                rd = csv.DictReader(f)
                cols = rd.fieldnames
                rows = [r for r in rd if r.get("variant_code") not in inds]  # idempotent

            n = 0
            for r in srows:
                if r["indicator_id"] not in inds or not (r.get("value") or "").strip():
                    continue
                row = {c: "" for c in cols}
                row.update({
                    "country_iso3": r["country_iso3"],
                    "country_name": r.get("country_name", r["country_iso3"]),
                    "year": r["year"],
                    "value": r["value"],
                    "unit": r.get("unit", ""),
                    "variant_code": r["indicator_id"],
                    "variant_label": r.get("indicator_label") or humanize(r["indicator_id"]),
                    "source_dataset": r.get("source_dataset", ""),
                })
                rows.append(row)
                n += 1
            if not n:
                continue

            with open(cpath, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=cols)
                w.writeheader()
                w.writerows(rows)

            mp = os.path.join(CHARTS, target.replace("/", "_"), "meta.json")
            if os.path.exists(mp):
                meta = json.load(open(mp, encoding="utf-8"))
                meta["countries"] = sorted({r["country_iso3"] for r in rows if r.get("country_iso3")})
                yrs = sorted({r["year"] for r in rows if r.get("year")})
                if yrs:
                    meta["year_range"] = [yrs[0], yrs[-1]]
                meta["n_rows"] = len(rows)
                json.dump(meta, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

            countries = len({r["country_iso3"] for r in rows if r.get("country_iso3")})
            print(f"  {target}: +{n} comparator rows ({len(inds)} measure(s)), now {countries} countries")
            touched += 1
            added += n

    print(f"\ncharts given comparator lines: {touched} | rows added: {added}")


if __name__ == "__main__":
    main()
