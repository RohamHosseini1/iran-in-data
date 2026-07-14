#!/usr/bin/env python3
"""
trim_fbs_variants.py -- de-clutter FAOSTAT food-consumption charts.

Each faostat__<commodity>__consumption chart bundled 5 near-duplicate measures
(Food total, kg/capita/yr, kcal/capita/day, protein supply, fat supply) -- the
"ten measures that all look the same / show nothing" the owner flagged. Keep the
two meaningful per-capita measures; drop the rest.

  KEEP: Food supply quantity (kg/capita/yr)  [default]
        Food supply (kcal/capita/day)
  DROP: Food (aggregate 1000 t), Protein supply quantity, Fat supply quantity

Guard: only trims a chart if a kept measure actually has data there (never empties
a chart). Data is preserved in data/processed; reversible by re-materializing.
"""
import csv, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHARTS = os.path.join(ROOT, "data", "charts")
csv.field_size_limit(sys.maxsize)

KEEP = {"Food supply quantity (kg/capita/yr)", "Food supply (kcal/capita/day)"}
DROP = {"Food", "Protein supply quantity (g/capita/day)", "Fat supply quantity (g/capita/day)"}


def main():
    trimmed = rows_dropped = skipped = 0
    for name in sorted(os.listdir(CHARTS)):
        if not (name.startswith("faostat__") and name.endswith("__consumption")):
            continue
        dpath = os.path.join(CHARTS, name, "data.csv")
        if not os.path.exists(dpath):
            continue
        with open(dpath, newline='', encoding='utf-8') as f:
            rd = csv.DictReader(f)
            cols = rd.fieldnames
            rows = list(rd)
        has_keep = any(r.get("variant_label") in KEEP and r.get("value") not in ("", "0", "0.000000")
                       for r in rows)
        if not has_keep:
            skipped += 1
            continue
        kept = [r for r in rows if r.get("variant_label") not in DROP]
        d = len(rows) - len(kept)
        if d == 0:
            continue
        with open(dpath, "w", newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for r in kept:
                w.writerow({k: r.get(k, "") for k in cols})
        mpath = os.path.join(CHARTS, name, "meta.json")
        if os.path.exists(mpath):
            try:
                m = json.load(open(mpath, encoding='utf-8'))
                m["n_rows"] = len(kept)
                m["countries"] = sorted(set(r["country_iso3"] for r in kept if r.get("country_iso3")))
                yrs = sorted(set(r["year"] for r in kept if r.get("year")))
                if yrs:
                    m["year_range"] = [yrs[0], yrs[-1]]
                json.dump(m, open(mpath, "w", encoding='utf-8'), indent=2, ensure_ascii=False)
            except Exception:
                pass
        trimmed += 1
        rows_dropped += d
    print(f"consumption charts trimmed: {trimmed} | rows dropped: {rows_dropped} | skipped (no per-capita data): {skipped}")


if __name__ == "__main__":
    main()
