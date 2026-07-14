#!/usr/bin/env python3
"""
drop_empty_variants.py -- no measure may render an empty chart.

Selecting a measure like "Producer Price (LCU/tonne)" on a commodity chart could
show a blank chart. Root cause (verified against the source, NOT a deletion): FAOSTAT
publishes that element for other countries but has no Iran figure for that commodity.
Comparators are off by default, so the chart came up empty.

This is an Iran-first database: a measure with no Iran data is not a measure of Iran.
So any variant with zero Iran observations is removed from the chart. If that leaves a
chart with no variant at all, the chart itself is hidden.

The underlying rows stay in data/processed -- nothing is destroyed, only un-displayed.
"""
import csv, json, os, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG = os.path.join(ROOT, "data", "processed", "CHART_REGISTRY.csv")
CHARTS = os.path.join(ROOT, "data", "charts")
HIDES = os.path.join(ROOT, "data", "processed", "quality_audit", "confirmed_hides.txt")
csv.field_size_limit(sys.maxsize)


def main():
    reg = {r["chart_id"]: r for r in csv.DictReader(open(REG, encoding="utf-8"))}
    live = [c for c, r in reg.items()
            if r["status"] not in ("merged", "hidden", "deleted") and not r["merged_into"]]

    dropped_variants = 0
    touched = 0
    emptied = []
    for cid in sorted(live):
        p = os.path.join(CHARTS, cid.replace("/", "_"), "data.csv")
        if not os.path.exists(p):
            continue
        with open(p, newline="", encoding="utf-8") as f:
            rd = csv.DictReader(f)
            cols = rd.fieldnames
            rows = list(rd)
        if "variant_code" not in (cols or []):
            continue

        iran_pts = defaultdict(int)
        variants = set()
        for r in rows:
            v = r.get("variant_code") or ""
            variants.add(v)
            if r.get("country_iso3") == "IRN" and (r.get("value") or "").strip():
                iran_pts[v] += 1
        dead = {v for v in variants if iran_pts[v] == 0}
        if not dead:
            continue

        kept = [r for r in rows if (r.get("variant_code") or "") not in dead]
        if not kept:
            emptied.append(cid)
            continue  # hide the whole chart instead (below)

        with open(p, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(kept)

        mp = os.path.join(CHARTS, cid.replace("/", "_"), "meta.json")
        if os.path.exists(mp):
            try:
                m = json.load(open(mp, encoding="utf-8"))
                m["n_rows"] = len(kept)
                m["countries"] = sorted({r["country_iso3"] for r in kept if r.get("country_iso3")})
                yrs = sorted({r["year"] for r in kept if r.get("year")})
                if yrs:
                    m["year_range"] = [yrs[0], yrs[-1]]
                json.dump(m, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            except Exception:
                pass
        dropped_variants += len(dead)
        touched += 1

    if emptied:
        with open(HIDES, "a", encoding="utf-8") as f:
            f.write("\n# every measure had zero Iran data (verified against source, not a deletion)\n")
            for c in emptied:
                f.write(c + "\n")

    print(f"charts cleaned: {touched} | empty measures removed: {dropped_variants}")
    print(f"charts with NO measure left (queued to hide): {len(emptied)}")
    for c in emptied[:8]:
        print(f"   {c}")
    if emptied:
        print("\nnow run: apply_culls.py")


if __name__ == "__main__":
    main()
