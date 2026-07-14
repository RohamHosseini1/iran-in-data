#!/usr/bin/env python3
"""
recombine_faostat_splits.py -- reverse the 2026-07-14 FAOSTAT production split.

A prior pass split each FAOSTAT production chart (which had Production / Area
harvested / Yield as unit-variants) into 3 separate single-measure charts, hiding
the multi-variant parent. That produced three identically-titled charts per
commodity and buried the measures the owner wants exposed as an in-chart toggle.

This restores the original model: ONE chart per commodity's production, with the
sub-measures (production, area, yield, ...) as toggleable variants. The parent
row is un-hidden; the single-measure children are hidden (merged into the parent).

Registry-only. data/charts is re-materialized separately (build_layer3_charts.py)
after this runs. Reversible; backs up the registry.
"""
import csv, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG = os.path.join(ROOT, "data", "processed", "CHART_REGISTRY.csv")
STAMP = "2026-07-14 recombine FAOSTAT production split"
csv.field_size_limit(sys.maxsize)


def main():
    with open(REG) as f:
        rd = csv.DictReader(f)
        fields = rd.fieldnames
        rows = list(rd)
    byid = {r["chart_id"]: r for r in rows}

    # split parents: hidden rows whose merged_into points at a "<stem>__production" child
    parents = [r for r in rows
               if r["status"] == "merged" and r["merged_into"].endswith("__production__production")]

    shutil.copy2(REG, REG + ".bak-recombine")
    unhidden = 0
    hidden_children = 0
    for p in parents:
        stem = p["chart_id"]                     # e.g. faostat__Wheat__production
        # un-hide the parent
        p["status"] = "new"
        p["merged_into"] = ""
        note = p.get("notes", "") or ""
        p["notes"] = f"{note} || {STAMP}: parent restored; sub-measures are variants".strip(" |")
        unhidden += 1
        # hide every currently-live child chart_id under this stem
        prefix = stem + "__"
        for cid, r in byid.items():
            if cid.startswith(prefix) and r["status"] == "new":
                r["status"] = "merged"
                r["merged_into"] = stem
                cnote = r.get("notes", "") or ""
                r["notes"] = f"{cnote} || {STAMP}: folded back into {stem} as a variant".strip(" |")
                hidden_children += 1

    with open(REG, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    live = sum(1 for r in rows if r["status"] not in ("merged", "hidden", "deleted") and not r["merged_into"])
    print(f"restored parents: {unhidden} | hidden single-measure children: {hidden_children}")
    print(f"live charts now: {live}")


if __name__ == "__main__":
    main()
