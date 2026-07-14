#!/usr/bin/env python3
"""
disambiguate_duplicate_measures.py -- stop the MEASURE dropdown showing the same
name twice.

287 FAOSTAT charts list a measure like "Domestic supply quantity" TWICE, because
FAO publishes the same element in two domains that are really two different
measurements:
    fbsh = Food Balance Sheets, HISTORIC methodology   (1961-2013)
    fbs  = Food Balance Sheets, CURRENT methodology    (2010-2023)
In their 2010-2013 overlap they DISAGREE materially (only 12.7% of Iran values
within 2%; p10 0.62, p90 2.11). So they must NOT be spliced into one line -- that
would silently pick a winner. Project rule: overlapping sources that disagree are
kept as separate LABELLED series, never adjudicated.

This appends the provenance qualifier to any variant_label that is shared by more
than one variant_code within a chart, so both stay visible and distinguishable.
Same treatment for the producer-price domains (pp / pa) and any other collision.

Pass --apply to write; default is a dry run.
"""
import csv, json, os, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG = os.path.join(ROOT, "data", "processed", "CHART_REGISTRY.csv")
CHARTS = os.path.join(ROOT, "data", "charts")
csv.field_size_limit(sys.maxsize)

DOMAIN = {
    "fbs":  "FAO current series",
    "fbsh": "FAO historic series",
    "pp":   "FAO current prices",
    "pa":   "FAO archive prices, pre-1991",
    "qcl":  "FAO production",
}
NOTE = ("FAO publishes this commodity's food-balance elements in two domains with "
        "different methodologies (historic 1961-2013 vs current 2010-2023); they "
        "disagree materially where they overlap, so both are kept as separate "
        "labelled series rather than spliced.")


def qualifier(code):
    dom = code.split(":", 1)[0] if ":" in code else ""
    return DOMAIN.get(dom, dom or code)


def main():
    apply = "--apply" in sys.argv
    with open(REG, newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        fields = rd.fieldnames
        regrows = list(rd)
    reg = {r["chart_id"]: r for r in regrows}
    live = [c for c, r in reg.items()
            if r["status"] not in ("merged", "hidden", "deleted") and not r["merged_into"]]

    n_charts = n_rows = 0
    preview = []
    for cid in sorted(live):
        p = os.path.join(CHARTS, cid.replace("/", "_"), "data.csv")
        if not os.path.exists(p):
            continue
        with open(p, newline="", encoding="utf-8") as f:
            rd = csv.DictReader(f)
            cols = rd.fieldnames
            rows = list(rd)
        if "variant_label" not in (cols or []):
            continue

        bylabel = defaultdict(set)
        for r in rows:
            bylabel[r.get("variant_label") or ""].add(r.get("variant_code") or "")
        dup = {l for l, codes in bylabel.items() if len(codes) > 1}
        if not dup:
            continue

        touched = 0
        for r in rows:
            lab = r.get("variant_label") or ""
            if lab in dup:
                q = qualifier(r.get("variant_code") or "")
                new = f"{lab} ({q})"
                if new != lab:
                    if len(preview) < 6:
                        preview.append((cid, lab, new))
                    r["variant_label"] = new
                    touched += 1
        if not touched:
            continue
        n_charts += 1
        n_rows += touched
        if apply:
            with open(p, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=cols)
                w.writeheader()
                w.writerows(rows)
            row = reg[cid]
            if NOTE[:40] not in (row.get("notes") or ""):
                row["notes"] = ((row.get("notes") or "") + " || " + NOTE).strip(" |")

    if apply:
        with open(REG, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(regrows)

    print(f"{'APPLIED' if apply else 'DRY RUN'}: disambiguated {n_rows} rows across {n_charts} charts")
    for cid, old, new in preview:
        print(f"   [{cid[:40]}] {old!r} -> {new!r}")
    if not apply:
        print("\nre-run with --apply to write")


if __name__ == "__main__":
    main()
