"""Merge new staging files into CHART_REGISTRY.csv, IN PLACE on top of whatever is
currently there -- never rebuilds from a frozen snapshot. This matters because several
agents make direct edits to CHART_REGISTRY.csv between merge runs (citations_json
fixes, underlying_codes path corrections) -- rebuilding from a pristine base would
silently wipe those out. (An earlier version of this script did rebuild from
CHART_REGISTRY_base.csv every time; that's why it once silently dropped the
citations_json column. Don't repeat that mistake.)

Tracks which staging files have already been merged in
data/processed/chart_registry_staging/.merged_files.json, so re-running only applies
NEW staging files -- re-applying an already-merged 'extends' row would double-append
its splice text onto the target row's alt_sources/notes.

status=new rows become new registry rows. status=extends rows are NOT appended as
duplicates -- they splice onto the referenced extends_chart_id row: alt_sources
gets the archival source appended, time_range gets noted, and the extension's own
notes get appended to that row's notes (never overwriting an existing note).
"""
import csv
import glob
import json
import os

REGISTRY = "data/processed/CHART_REGISTRY.csv"
STAGING_GLOB = "data/processed/chart_registry_staging/*.csv"
MERGED_LOG = "data/processed/chart_registry_staging/.merged_files.json"

FIELDS = ["chart_id", "title", "category", "primary_source", "alt_sources",
          "n_unit_variants_merged", "underlying_codes", "status",
          "extends_chart_id", "time_range", "notes", "citations_json"]


def load_current_registry():
    registry = {}
    order = []
    if not os.path.exists(REGISTRY):
        raise SystemExit(f"{REGISTRY} does not exist -- nothing to merge into. "
                          "If this is a true first run, seed it from CHART_REGISTRY_base.csv first.")
    with open(REGISTRY, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            for k in FIELDS:
                row.setdefault(k, "")
            registry[row["chart_id"]] = row
            order.append(row["chart_id"])
    return registry, order


def load_merged_log():
    if os.path.exists(MERGED_LOG):
        with open(MERGED_LOG, encoding='utf-8') as f:
            return set(json.load(f))
    return set()


def save_merged_log(merged):
    with open(MERGED_LOG, "w", encoding='utf-8') as f:
        json.dump(sorted(merged), f, indent=2)


def main():
    registry, order = load_current_registry()
    already_merged = load_merged_log()
    orphaned = []
    new_count = 0
    extends_count = 0
    all_staging_files = sorted(glob.glob(STAGING_GLOB))
    pending_files = [sf for sf in all_staging_files if sf not in already_merged]

    if not pending_files:
        print(f"No new staging files to merge ({len(all_staging_files)} total, all already merged).")
        print(f"Current TOTAL rows in {REGISTRY}: {len(order)}")
        return

    for sf in pending_files:
        with open(sf, newline='', encoding='utf-8', errors='replace') as f:
            for row in csv.DictReader(f):
                cid = row["chart_id"]
                status = row.get("status", "new").strip()

                if status == "extends":
                    target = row.get("extends_chart_id", "").strip()
                    if target and target in registry:
                        tgt = registry[target]
                        addition = f"{row.get('primary_source','')} ({row.get('time_range','')})"
                        tgt["alt_sources"] = (tgt["alt_sources"] + " | " + addition).strip(" |") \
                            if tgt["alt_sources"] else addition
                        extra_note = row.get("notes", "").strip()
                        if extra_note:
                            tgt["notes"] = (tgt["notes"] + " || " + extra_note).strip(" |") \
                                if tgt["notes"] else extra_note
                        extends_count += 1
                        continue
                    else:
                        orphaned.append((sf, cid, target))
                        # fall through -- treat as new so the data isn't silently dropped

                if cid in registry:
                    registry[cid]["notes"] = (registry[cid]["notes"] +
                                               f" || DUPLICATE chart_id also staged in {sf}, skipped").strip(" |")
                    continue

                for k in FIELDS:
                    row.setdefault(k, "")
                registry[cid] = row
                order.append(cid)
                new_count += 1

    with open(REGISTRY, "w", newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for cid in order:
            w.writerow({k: registry[cid].get(k, "") for k in FIELDS})

    already_merged.update(pending_files)
    save_merged_log(already_merged)

    print(f"Newly merged staging files: {len(pending_files)} -> {pending_files}")
    print(f"Already-merged staging files (skipped): {len(all_staging_files) - len(pending_files)}")
    print(f"New chart rows added: {new_count}")
    print(f"Extends-splices applied: {extends_count}")
    print(f"Orphaned extends_chart_id refs (fell back to new): {len(orphaned)}")
    for sf, cid, target in orphaned:
        print(f"  {sf}: {cid} -> missing target '{target}'")
    print(f"TOTAL rows in {REGISTRY}: {len(order)}")


if __name__ == "__main__":
    main()
