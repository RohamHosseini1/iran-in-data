#!/usr/bin/env python3
"""
merge_timeline_events.py -- fold new events and Persian translations into timeline/*.csv.

The event layer was English-only, so the Persian site rendered English events. And it
was thin: only 64 of ~1,600 charts carried any event at all.

This does two things, idempotently:
  1. adds title_fa / description_fa columns to every timeline/*.csv and fills them
     from data/processed/quality_audit/timeline_translations.csv (keyed date+title);
  2. appends the new sourced events from timeline/new_events/*.csv (which already
     carry Persian), skipping any whose (date, title) already exists.

Safe to re-run: nothing is duplicated and an existing Persian value is never
overwritten with a blank.
"""
import csv, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TL = os.path.join(ROOT, "timeline")
NEW = os.path.join(TL, "new_events")
TRANS = os.path.join(ROOT, "data", "processed", "quality_audit", "timeline_translations.csv")
csv.field_size_limit(sys.maxsize)

COLS = ["date", "country", "event_type", "title", "title_fa", "description",
        "description_fa", "economic_domains", "source_url", "source_name"]


def load_translations():
    tr = {}
    if not os.path.exists(TRANS):
        return tr
    for r in csv.DictReader(open(TRANS, encoding="utf-8")):
        key = (r.get("source_file", ""), r.get("date", ""), r.get("title", ""))
        tr[key] = (r.get("title_fa", ""), r.get("description_fa", ""))
    return tr


def main():
    tr = load_translations()
    total_new = total_fa = 0

    for fn in sorted(os.listdir(TL)):
        if not fn.endswith(".csv") or fn == "eras.csv":
            continue
        path = os.path.join(TL, fn)
        rows = list(csv.DictReader(open(path, encoding="utf-8")))
        if not rows:
            continue
        seen = {(r["date"], r["title"]) for r in rows}

        # 1. Persian for existing rows
        n_fa = 0
        for r in rows:
            for c in COLS:
                r.setdefault(c, "")
            t = tr.get((fn, r["date"], r["title"]))
            if t:
                if t[0] and not r.get("title_fa"):
                    r["title_fa"] = t[0]
                    n_fa += 1
                if t[1] and not r.get("description_fa"):
                    r["description_fa"] = t[1]

        # 2. append new events for this country file
        newpath = os.path.join(NEW, fn)
        n_new = 0
        if os.path.exists(newpath):
            for r in csv.DictReader(open(newpath, encoding="utf-8")):
                key = (r.get("date", ""), r.get("title", ""))
                if not key[0] or key in seen:
                    continue
                seen.add(key)
                rows.append({c: r.get(c, "") for c in COLS})
                n_new += 1

        rows.sort(key=lambda r: r["date"])
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=COLS)
            w.writeheader()
            for r in rows:
                w.writerow({c: r.get(c, "") for c in COLS})
        total_new += n_new
        total_fa += n_fa
        if n_new or n_fa:
            print(f"  {fn}: +{n_new} new events, +{n_fa} Persian titles  ({len(rows)} rows)")

    # brand-new country files (e.g. iraq.csv -- Iraq is a comparator with no timeline)
    if os.path.isdir(NEW):
        for fn in sorted(os.listdir(NEW)):
            if not fn.endswith(".csv") or os.path.exists(os.path.join(TL, fn)):
                continue
            rows = list(csv.DictReader(open(os.path.join(NEW, fn), encoding="utf-8")))
            rows.sort(key=lambda r: r.get("date", ""))
            with open(os.path.join(TL, fn), "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=COLS)
                w.writeheader()
                for r in rows:
                    w.writerow({c: r.get(c, "") for c in COLS})
            total_new += len(rows)
            print(f"  {fn}: NEW FILE, {len(rows)} events")

    print(f"\ntotal: +{total_new} events, +{total_fa} Persian titles")


if __name__ == "__main__":
    main()
