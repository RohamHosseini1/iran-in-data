#!/usr/bin/env python3
"""
clean_titles.py -- take the MEASURE/UNIT out of chart titles.

Owner rule: the title is the SUBJECT ("GDP", "Ducks", "U.S. Dollar Exchange
Rate"), never the specific measure/unit ("GDP (current US$)", "Ducks, livestock
stocks (head)"). The measure lives in the in-chart variant toggle; the category
conveys production-vs-trade-vs-consumption.

  * FAOSTAT: title = the clean commodity name, taken from the chart_id
    (faostat__<commodity>__<measure>), which is authoritative and never carries
    a unit.
  * WDI + archival: strip a TRAILING pure-unit parenthetical (current US$, %,
    Mt CO2e, annual %, per capita, ...) but KEEP a definitional one (% of GDP,
    modeled estimate, by sex) -- removing those loses meaning.
  * A few hand overrides for the charts the owner named explicitly.

Writes proposals to data/processed/quality_audit/title_proposals.csv (EN only).
Review, then apply with apply_titles.py. Persian titles are handled separately.
"""
import csv, os, re, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG = os.path.join(ROOT, "data", "processed", "CHART_REGISTRY.csv")
OUT = os.path.join(ROOT, "data", "processed", "quality_audit", "title_proposals.csv")
csv.field_size_limit(sys.maxsize)

# Charts the owner named explicitly, or bespoke ones a rule can't clean.
OVERRIDES = {
    "fx__official_vs_parallel_gap_irn": "U.S. Dollar Exchange Rate",
}

TRAIL_PAREN = re.compile(r"\s*\(([^()]*)\)\s*$")

# Strip if the trailing parenthetical is a PURE unit/currency/index.
STRIP_TOKENS = (
    "us$", "international $", "lcu", "mt co2e", "sq. km", "gpi",
    "2015 = 100", "1=low to 5=high", "0-100", "kwh", "kg", "tonnes",
    "metric tons", "kt of", "current", "constant",
)
STRIP_EXACT = {"%", "annual %", "annual % growth", "% gross", "% net", "years",
               "number", "index", "ratio", "total"}
# Keep the parenthetical (it defines WHAT the measure is) if it contains these.
# (BoP/DOD are currency-framework tags conveyed by the category, so they are NOT
# kept -- "Current account balance (BoP, current US$)" -> "Current account balance".)
KEEP_SIGNALS = (" of ", "estimate", "female", "male", "cohort",
                "ppp", "per capita", "gross national income")


def strip_trailing_unit(title):
    m = TRAIL_PAREN.search(title)
    if not m:
        return title, False
    inner = m.group(1).strip()
    low = inner.lower()
    if any(s in low for s in KEEP_SIGNALS):
        return title, False
    strip = (low in STRIP_EXACT
             or any(t in low for t in STRIP_TOKENS)
             or low.startswith("per ")
             or low.startswith("% ") and " of " not in low)
    if strip:
        return title[: m.start()].rstrip(" ,;"), True
    return title, False


def main():
    with open(REG) as f:
        rows = list(csv.DictReader(f))
    live = [r for r in rows
            if r["status"] not in ("merged", "hidden", "deleted") and not r["merged_into"]]

    proposals = []
    for r in live:
        cid = r["chart_id"]
        src = r["primary_source"] or ""
        old = r["title"]
        rule = ""
        if cid in OVERRIDES:
            new, rule = OVERRIDES[cid], "override"
        elif src.startswith("faostat") or cid.startswith("faostat__"):
            new = cid.split("__")[1]
            rule = "faostat-commodity"
        else:
            new, changed = strip_trailing_unit(old)
            rule = "strip-unit" if changed else "keep"
        # never leave an empty or 1-char title
        if not new or len(new) < 2:
            new, rule = old, "keep(guard)"
        proposals.append(dict(chart_id=cid, primary_source=src, category=r["category"],
                              old_title=old, new_title=new,
                              changed="Y" if new != old else "", rule=rule))

    # collision guard: within a category, two different charts must not collapse
    # to the same title. If they do, revert both to their originals.
    bycat = defaultdict(lambda: defaultdict(list))
    for p in proposals:
        bycat[p["category"]][p["new_title"]].append(p)
    collisions = 0
    for cat, titles in bycat.items():
        for t, ps in titles.items():
            if len(ps) > 1:
                for p in ps:
                    if p["new_title"] != p["old_title"]:
                        p["new_title"] = p["old_title"]
                        p["changed"] = ""
                        p["rule"] = "keep(collision)"
                        collisions += 1

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cols = ["changed", "rule", "chart_id", "primary_source", "category", "old_title", "new_title"]
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for p in sorted(proposals, key=lambda x: (x["rule"], x["chart_id"])):
            w.writerow({k: p[k] for k in cols})

    from collections import Counter
    changed = [p for p in proposals if p["changed"]]
    print(f"{len(proposals)} live charts | {len(changed)} title changes | {collisions} collision-reverts -> {OUT}")
    print("by rule:", dict(Counter(p["rule"] for p in proposals)))
    print("\n--- sample changes ---")
    seen = set()
    for p in changed:
        key = p["rule"]
        if key in seen and list(map(lambda x: x[0], seen)).count(key) > 6:
            continue
        seen.add((key, p["chart_id"]))
    import random
    random.seed(3)
    for p in random.sample(changed, min(30, len(changed))):
        print(f"  [{p['rule']:12}] {p['old_title'][:52]:52} -> {p['new_title'][:32]}")


if __name__ == "__main__":
    main()
