#!/usr/bin/env python3
"""
apply_culls.py -- hide the charts proposed by propose_culls.py (action=HIDE) plus
the hand-confirmed extras in confirmed_hides.txt, minus keep_overrides.txt.

Hiding == registry status set to 'merged' with merged_into='' (the project's
"delete but keep the data" convention, rule 6 in apply_quality_audit.py). Fully
reversible: flip status back to 'new'. Data directories under data/charts/ are
never touched.

Idempotent: re-running only affects rows not already hidden. Backs up the
registry once per run.
"""
import csv, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG = os.path.join(ROOT, "data", "processed", "CHART_REGISTRY.csv")
QA = os.path.join(ROOT, "data", "processed", "quality_audit")
PROPS = os.path.join(QA, "cull_proposals.csv")
CONFIRMED = os.path.join(QA, "confirmed_hides.txt")
KEEP = os.path.join(QA, "keep_overrides.txt")
STAMP = "2026-07-14 data-quality cull"
csv.field_size_limit(sys.maxsize)


def read_id_file(path):
    ids = set()
    if not os.path.exists(path):
        return ids
    for line in open(path):
        line = line.strip()
        if line and not line.startswith("#"):
            ids.add(line)
    return ids


def main():
    hide = {r["chart_id"] for r in csv.DictReader(open(PROPS)) if r["action"] == "HIDE"}
    hide |= read_id_file(CONFIRMED)
    hide -= read_id_file(KEEP)

    with open(REG) as f:
        rd = csv.DictReader(f)
        fields = rd.fieldnames
        rows = list(rd)

    shutil.copy2(REG, REG + ".bak-cull")
    changed = 0
    missing = []
    for row in rows:
        if row["chart_id"] in hide:
            if row["status"] == "merged" and not row["merged_into"]:
                continue  # already hidden
            row["status"] = "merged"
            row["merged_into"] = ""
            note = row.get("notes", "") or ""
            sep = " || " if note else ""
            row["notes"] = f"{note}{sep}{STAMP}: hidden (not a measure-over-time / empty Iran series); data preserved on disk"
            changed += 1
    present = {r["chart_id"] for r in rows}
    missing = [h for h in hide if h not in present]

    with open(REG, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    print(f"requested hide: {len(hide)} | newly hidden: {changed} | already hidden or absent: {len(hide)-changed}")
    if missing:
        print(f"WARNING: {len(missing)} requested chart_ids not found in registry:")
        for m in missing:
            print("   ", m)
    live = sum(1 for r in rows if r["status"] not in ("merged", "hidden", "deleted") and not r["merged_into"])
    print(f"live charts remaining: {live}")


if __name__ == "__main__":
    main()
