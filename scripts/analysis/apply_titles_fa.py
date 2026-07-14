#!/usr/bin/env python3
"""
apply_titles_fa.py -- apply the Persian title cleanup (title_fa_proposals.csv).

Mirrors apply_titles.py for the FA side: the EN titles had the measure/unit
stripped, which left title_fa inconsistent. This writes the cleaned Persian
subject-only titles into CHART_REGISTRY.csv and each chart's meta.json.

Backs up the registry. Idempotent. Skips rows flagged needs_review.
"""
import csv, json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG = os.path.join(ROOT, "data", "processed", "CHART_REGISTRY.csv")
PROPS = os.path.join(ROOT, "data", "processed", "quality_audit", "title_fa_proposals.csv")
CHARTS = os.path.join(ROOT, "data", "charts")
csv.field_size_limit(sys.maxsize)


def main():
    new_by_id = {}
    for r in csv.DictReader(open(PROPS, encoding="utf-8")):
        nt = (r.get("new_title_fa") or "").strip()
        if not nt or "needs_review" in (r.get("note") or "").lower():
            continue
        new_by_id[r["chart_id"]] = nt

    with open(REG, encoding="utf-8") as f:
        rd = csv.DictReader(f)
        fields = rd.fieldnames
        rows = list(rd)

    shutil.copy2(REG, REG + ".bak-titles-fa")
    n = 0
    for row in rows:
        nt = new_by_id.get(row["chart_id"])
        if nt and row.get("title_fa") != nt:
            row["title_fa"] = nt
            n += 1
    with open(REG, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    m = 0
    for cid, nt in new_by_id.items():
        mp = os.path.join(CHARTS, cid.replace("/", "_"), "meta.json")
        if not os.path.exists(mp):
            continue
        try:
            meta = json.load(open(mp, encoding="utf-8"))
        except Exception:
            continue
        if meta.get("title_fa") != nt:
            meta["title_fa"] = nt
            json.dump(meta, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            m += 1
    print(f"registry title_fa updated: {n} | meta.json title_fa synced: {m}")


if __name__ == "__main__":
    main()
