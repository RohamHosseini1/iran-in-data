#!/usr/bin/env python3
"""
apply_titles.py -- apply the EN title changes from title_proposals.csv.

Updates CHART_REGISTRY.csv 'title' for every changed row, and syncs the same
'title' into that chart's data/charts/<id>/meta.json (used by the detail page's
schema.org markup and CSV downloads). Persian 'title_fa' is handled separately.

Backs up the registry. Idempotent (re-running is a no-op once applied).
"""
import csv, json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG = os.path.join(ROOT, "data", "processed", "CHART_REGISTRY.csv")
PROPS = os.path.join(ROOT, "data", "processed", "quality_audit", "title_proposals.csv")
CHARTS = os.path.join(ROOT, "data", "charts")
csv.field_size_limit(sys.maxsize)


def slug(cid):
    return cid.replace("/", "_")


def main():
    new_by_id = {r["chart_id"]: r["new_title"]
                 for r in csv.DictReader(open(PROPS)) if r["changed"] == "Y"}

    with open(REG) as f:
        rd = csv.DictReader(f)
        fields = rd.fieldnames
        rows = list(rd)

    shutil.copy2(REG, REG + ".bak-titles")
    reg_changed = 0
    for row in rows:
        nt = new_by_id.get(row["chart_id"])
        if nt and row["title"] != nt:
            row["title"] = nt
            reg_changed += 1

    with open(REG, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    meta_changed = 0
    for cid, nt in new_by_id.items():
        mp = os.path.join(CHARTS, slug(cid), "meta.json")
        if not os.path.exists(mp):
            continue
        try:
            m = json.load(open(mp))
        except Exception:
            continue
        if m.get("title") != nt:
            m["title"] = nt
            with open(mp, "w") as f:
                json.dump(m, f, ensure_ascii=False, indent=2)
            meta_changed += 1

    print(f"registry titles updated: {reg_changed} | meta.json titles synced: {meta_changed}")


if __name__ == "__main__":
    main()
