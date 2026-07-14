#!/usr/bin/env python3
"""
build_event_chart_links.py -- expand the event->chart mapping workflow's output into
the correlation file the frontend already reads.

The event layer was an MVP: only 64 of ~1,600 charts carried any event. This writes
the mapped events into the SAME schema/filename pattern the frontend globs
(data/processed/policy_chart_correlations_*.csv), so it lights up with no frontend
change.

Broad events (an oil shock, the Revolution) attach by CATEGORY and get expanded here
into every chart in that category; targeted events name exact chart_ids. Every
chart_id is validated against the live registry, so an invented one cannot slip in.
Existing (chart_id, event) pairs from the earlier hand-curated pass are NOT
duplicated -- those stay authoritative.

Input : data/processed/laws/event_mappings_raw.json
Output: data/processed/policy_chart_correlations_mapped.csv
"""
import csv, glob, json, os, sys
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROC = os.path.join(ROOT, "data", "processed")
RAW = os.path.join(PROC, "laws", "event_mappings_raw.json")
REG = os.path.join(PROC, "CHART_REGISTRY.csv")
OUT = os.path.join(PROC, "policy_chart_correlations_mapped.csv")
csv.field_size_limit(sys.maxsize)

FIELDS = ["correlation_id", "chart_id", "chart_title", "event_date", "event_title",
          "event_source_file", "relationship_type", "confidence", "direction",
          "lag_description", "justification", "caveats"]


def main():
    corr = json.load(open(RAW, encoding="utf-8"))
    if isinstance(corr, dict):
        corr = corr.get("correlations", [])

    reg = list(csv.DictReader(open(REG, encoding="utf-8")))
    live = [r for r in reg
            if r["status"] not in ("merged", "hidden", "deleted") and not r["merged_into"]]
    title = {r["chart_id"]: r["title"] for r in live}
    by_cat = defaultdict(list)
    for r in live:
        by_cat[r["category"]].append(r["chart_id"])

    # pairs already covered by the earlier hand-curated correlation files
    existing = set()
    for f in glob.glob(os.path.join(PROC, "policy_chart_correlations_*.csv")):
        if os.path.basename(f) == os.path.basename(OUT):
            continue
        for r in csv.DictReader(open(f, encoding="utf-8")):
            existing.add((r["chart_id"], r["event_date"], r["event_title"]))

    rows = []
    seen = set()
    bad_chart = bad_cat = 0
    for c in corr:
        date = c.get("event_date", "")
        etitle = c.get("event_title", "")
        src = c.get("event_source_file", "")
        if not date or not etitle:
            continue

        targets = []
        for cid in (c.get("chart_ids") or []):
            if cid in title:
                targets.append(cid)
            else:
                bad_chart += 1
        for cat in (c.get("categories") or []):
            if cat in by_cat:
                targets.extend(by_cat[cat])
            else:
                bad_cat += 1

        for cid in targets:
            key = (cid, date, etitle)
            if key in seen or key in existing:
                continue
            seen.add(key)
            rows.append({
                "correlation_id": f"evm_{len(rows) + 1:06d}",
                "chart_id": cid,
                "chart_title": title.get(cid, ""),
                "event_date": date,
                "event_title": etitle,
                "event_source_file": src,
                "relationship_type": c.get("relationship_type", ""),
                "confidence": c.get("confidence", ""),
                "direction": c.get("direction", ""),
                "lag_description": c.get("lag_description", ""),
                "justification": c.get("justification", ""),
                "caveats": c.get("caveats", ""),
            })

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    charts = {r["chart_id"] for r in rows} | {e[0] for e in existing}
    print(f"new event->chart links: {len(rows)} -> {OUT}")
    print(f"  distinct events mapped: {len({(r['event_date'], r['event_title']) for r in rows})}")
    print(f"  charts with events now: {len(charts)} (was {len({e[0] for e in existing})})")
    print(f"  by relationship: {dict(Counter(r['relationship_type'] for r in rows))}")
    print(f"  by confidence:   {dict(sorted(Counter(r['confidence'] for r in rows).items()))}")
    if bad_chart or bad_cat:
        print(f"  dropped invented refs: {bad_chart} chart_ids, {bad_cat} categories")
    per = Counter(r["chart_id"] for r in rows)
    if per:
        print("  busiest charts (event count):")
        for cid, k in per.most_common(4):
            print(f"     {k:4d}  {cid}")


if __name__ == "__main__":
    main()
