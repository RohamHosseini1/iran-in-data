#!/usr/bin/env python3
"""
build_law_chart_links.py -- turn the law->chart mapping workflow's output into the
annotation layer the frontend renders.

This is the SECOND annotation layer, parallel to (not merged with) the existing
event layer:
  * events -> golden-orange markers  (data/processed/policy_chart_correlations_*.csv)
  * laws   -> low-opacity GREY markers (this file)

Owner's model for laws: a law does NOT need proven causation to appear. If it is
genuinely related to the measure's field, it goes on the timeline with an honest
confidence and a plain description: "on this date this law passed, it did X, it
could plausibly affect this measure because Y" -- plus a caveat. Weak links are
recorded AS weak, never omitted and never dressed up as causal.

Laws are PERSIAN-FIRST: the enacted Persian title is authoritative and is what the
Persian site shows verbatim; the English site shows a translation.

Input : data/processed/laws/law_mappings_raw.json  (workflow output: correlations[])
        data/processed/laws/laws_shortlist_typed.csv (law_id -> Persian title, date)
        data/processed/CHART_REGISTRY.csv            (category -> chart_ids)
Output: data/processed/law_chart_links.csv
"""
import csv, json, os, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LAWS = os.path.join(ROOT, "data", "processed", "laws")
RAW = os.path.join(LAWS, "law_mappings_raw.json")
REG = os.path.join(ROOT, "data", "processed", "CHART_REGISTRY.csv")
OUT = os.path.join(ROOT, "data", "processed", "law_chart_links.csv")
csv.field_size_limit(sys.maxsize)

FIELDS = ["link_id", "chart_id", "law_id", "law_date",
          "law_title_fa", "law_title_en", "law_summary_en", "law_summary_fa",
          "relationship_type", "confidence", "direction", "lag_description",
          "justification", "caveats", "scope", "source_path"]


def main():
    if not os.path.exists(RAW):
        raise SystemExit(f"missing {RAW} -- write the workflow's correlations there first")
    corr = json.load(open(RAW, encoding="utf-8"))
    if isinstance(corr, dict):
        corr = corr.get("correlations", [])

    laws = {r["law_id"]: r for r in csv.DictReader(open(
        os.path.join(LAWS, "laws_shortlist_typed.csv"), encoding="utf-8"))}

    reg = list(csv.DictReader(open(REG, encoding="utf-8")))
    live = [r for r in reg
            if r["status"] not in ("merged", "hidden", "deleted") and not r["merged_into"]]
    live_ids = {r["chart_id"] for r in live}
    by_cat = defaultdict(list)
    for r in live:
        by_cat[r["category"]].append(r["chart_id"])

    # The scraped corpus contains the SAME law text under several file ids (e.g. the
    # Direct Taxation Law appears twice). Collapse them to one canonical law_id so a
    # chart doesn't show the same law twice.
    import re as _re

    def norm_title(t):
        t = _re.sub(r"\s+", " ", t or "").strip()
        return t.replace("ي", "ی").replace("ك", "ک")

    canon = {}
    ident = {}
    for lid, l in laws.items():
        key = (norm_title(l.get("title")), l.get("gregorian_year", ""))
        if key not in ident:
            ident[key] = lid
        canon[lid] = ident[key]

    rows = []
    seen = set()
    dropped_bad_chart = 0
    dropped_bad_cat = 0
    n = 0
    for c in corr:
        law_id = canon.get(c.get("law_id", ""), c.get("law_id", ""))
        law = laws.get(law_id, {})
        # the Persian title from our own index is authoritative, not the agent's echo
        title_fa = law.get("title") or c.get("law_title", "")
        date = law.get("jalali_date", "")
        gyear = law.get("gregorian_year", "") or c.get("law_date", "")

        targets = []
        for cid in (c.get("chart_ids") or []):
            if cid in live_ids:
                targets.append((cid, "specific"))
            else:
                dropped_bad_chart += 1
        for cat in (c.get("categories") or []):
            if cat in by_cat:
                for cid in by_cat[cat]:
                    targets.append((cid, "category"))
            else:
                dropped_bad_cat += 1

        for cid, scope in targets:
            key = (cid, law_id)
            if key in seen:
                continue
            seen.add(key)
            n += 1
            rows.append({
                "link_id": f"law_{n:06d}",
                "chart_id": cid,
                "law_id": law_id,
                "law_date": gyear,
                "law_title_fa": title_fa,
                "law_title_en": "",      # filled by the translation pass
                "law_summary_en": "",    # filled by the translation pass
                "law_summary_fa": "",
                "relationship_type": c.get("relationship_type", ""),
                "confidence": c.get("confidence", ""),
                "direction": c.get("direction", ""),
                "lag_description": c.get("lag_description", ""),
                "justification": c.get("justification", ""),
                "caveats": c.get("caveats", ""),
                "scope": scope,
                "source_path": law.get("path", ""),
            })

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    from collections import Counter
    print(f"law->chart links: {len(rows)}  -> {OUT}")
    print(f"  distinct laws: {len({r['law_id'] for r in rows})}")
    print(f"  distinct charts annotated: {len({r['chart_id'] for r in rows})}")
    print(f"  by relationship: {dict(Counter(r['relationship_type'] for r in rows))}")
    print(f"  by confidence:   {dict(sorted(Counter(r['confidence'] for r in rows).items()))}")
    print(f"  by scope:        {dict(Counter(r['scope'] for r in rows))}")
    if dropped_bad_chart or dropped_bad_cat:
        print(f"  dropped invented refs: {dropped_bad_chart} chart_ids, {dropped_bad_cat} categories")
    # density check: how crowded does the busiest chart get?
    per = Counter(r["chart_id"] for r in rows)
    if per:
        top = per.most_common(5)
        print("  busiest charts (law count):")
        for cid, k in top:
            print(f"     {k:5d}  {cid}")


if __name__ == "__main__":
    main()
