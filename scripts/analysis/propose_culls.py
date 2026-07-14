#!/usr/bin/env python3
"""
propose_culls.py -- identify charts to HIDE, per the owner's data-quality rules:

  * A chart must be a CLEAR MEASURE over TIME for Iran. Report-snapshot charts,
    event logs, single-document citation dumps, and comparator-only charts with
    no Iran series "simply should not exist".
  * Empty / all-zero Iran series tell the reader nothing.

Reads the quality scan + registry; writes proposals to
data/processed/quality_audit/cull_proposals.csv. Does NOT modify the registry --
review the proposals, then apply with apply_culls.py. Reversible either way
(hiding = status 'merged', data kept on disk).
"""
import csv, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG = os.path.join(ROOT, "data", "processed", "CHART_REGISTRY.csv")
SCAN = os.path.join(ROOT, "data", "processed", "quality_audit", "chart_quality_scan.csv")
OUT = os.path.join(ROOT, "data", "processed", "quality_audit", "cull_proposals.csv")
csv.field_size_limit(sys.maxsize)

# report-snapshot / event-log title signals (case-insensitive substring)
TOPICAL_TITLE = [
    "event log", "citations", "assessment timeline", "rescheduling",
    " agreement", "consultation history", "milestones", "narrative",
    "deal-flow pipeline", "concession", "joint ventures", "scenarios",
    "descriptive statistics",
]
# source families that are inherently single-document report snapshots, not measures
REPORT_SOURCES = ("cia", "frus")
# Iran-origin archival families: never auto-hide on DEAD alone (could be a bug or
# an enrichment target) -- send to REVIEW instead.
IRAN_ARCHIVAL = ("iran", "sci", "pahlavi", "iranica", "majlis", "cbi", "fao_giews")


def span_of(time_range):
    yrs = re.findall(r"(1[89]\d\d|20\d\d)", time_range or "")
    if len(yrs) >= 2:
        return int(yrs[-1]) - int(yrs[0])
    return None


def main():
    reg = {r["chart_id"]: r for r in csv.DictReader(open(REG))}
    scan = {r["chart_id"]: r for r in csv.DictReader(open(SCAN))}

    props = []
    for cid, r in reg.items():
        if r["status"] in ("merged", "hidden", "deleted") or r["merged_into"]:
            continue
        src = r["primary_source"] or ""
        fam = src.split("-")[0].split("/")[0]
        title = r["title"] or ""
        tl = title.lower()
        s = scan.get(cid, {})
        verdict = s.get("verdict", "")
        flags = s.get("flags", "")
        span = span_of(r.get("time_range", ""))

        action = None
        reason = None
        is_iran = fam in IRAN_ARCHIVAL or cid.startswith(("iran", "specialty", "pahlavi", "sci"))
        topical = any(k in tl for k in TOPICAL_TITLE)

        # AUTO-HIDE only the genuinely-safe categories. Never auto-hide an
        # Iran-origin chart on wording alone -- real measures (vehicle
        # production, PMI, tobacco workforce) carry "milestones"/"narrative"
        # in their titles too. Those go to REVIEW for a human call.
        if fam in REPORT_SOURCES:
            action, reason = "HIDE", f"report-snapshot source ({fam}); single-document dump, not a measure"
        elif "NO_IRAN" in flags and not is_iran:
            action, reason = "HIDE", "comparator-only, no Iran series (Iran-first rule)"
        elif verdict == "DEAD" and not is_iran:
            action, reason = "HIDE", f"empty/all-zero Iran series ({flags})"
        elif is_iran and (verdict == "DEAD" or "NO_IRAN" in flags):
            action, reason = "REVIEW", f"Iran-origin but no real series ({verdict}/{flags}) -- confirm hide vs enrich"
        elif is_iran and topical and verdict == "THIN":
            action, reason = "REVIEW", f"Iran-origin, topical wording + thin ({flags}) -- keep+clean, fold, or enrich?"
        elif topical and verdict in ("DEAD", "THIN"):
            action, reason = "REVIEW", f"topical wording + weak ({verdict}) -- check"

        if action:
            props.append(dict(chart_id=cid, action=action, reason=reason,
                              primary_source=src, category=r["category"],
                              verdict=verdict, flags=flags, time_range=r.get("time_range", ""),
                              title=title))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cols = ["action", "chart_id", "primary_source", "category", "verdict", "flags",
            "time_range", "reason", "title"]
    props.sort(key=lambda p: (p["action"], p["primary_source"]))
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for p in props:
            w.writerow({k: p.get(k, "") for k in cols})

    from collections import Counter
    ac = Counter(p["action"] for p in props)
    print(f"{len(props)} cull proposals -> {OUT}")
    print("actions:", dict(ac))
    hide_fam = Counter(p["primary_source"].split("-")[0].split("/")[0]
                       for p in props if p["action"] == "HIDE")
    print("HIDE by source family:", dict(hide_fam.most_common()))
    print("\n--- sample HIDE titles ---")
    n = 0
    for p in props:
        if p["action"] == "HIDE" and n < 25:
            print(f"  [{p['primary_source'][:14]:14}] {p['title'][:70]}")
            n += 1


if __name__ == "__main__":
    main()
