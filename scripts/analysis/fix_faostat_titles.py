#!/usr/bin/env python3
"""
fix_faostat_titles.py -- undo an over-strip.

The owner asked for the UNIT to be taken out of chart titles ("GDP (current US$)"
-> "GDP"). For FAOSTAT I wrongly took out the MEASURE as well, so
"Bananas, production (tonnes)" and "Bananas, imports and exports (1000 tonnes)"
both collapsed to "Bananas" -- four different charts ended up with the same name.
The collision guard missed it because those charts sit in four different categories
and it only checked within a category.

This restores the original FAOSTAT title and removes ONLY the trailing unit.
The WDI/archival titles are left alone: "GDP (current US$)" -> "GDP" was correct.

Persian titles are regenerated to match (subject + measure, no unit).
"""
import csv, json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG = os.path.join(ROOT, "data", "processed", "CHART_REGISTRY.csv")
PROPS = os.path.join(ROOT, "data", "processed", "quality_audit", "title_proposals.csv")
CHARTS = os.path.join(ROOT, "data", "charts")
csv.field_size_limit(sys.maxsize)

# a trailing parenthetical that is purely a UNIT (this is all the owner wanted gone)
UNIT_PAREN = re.compile(
    r"\s*\((?:tonnes?|1000 tonnes|t|kg|kg/ha|ha|hectares|head|1000 An|An|g/An|"
    r"No|1000 No|kg/capita/yr|kcal/capita/day|g/capita/day|LCU/tonne|USD/tonne|"
    r"SLC/tonne|1000 t)\)\s*$",
    re.I,
)

# Persian for each FAOSTAT measure family (subject + measure, no units)
FA_MEASURE = {
    "production": "تولید",
    "trade": "صادرات و واردات",
    "consumption": "مصرف سرانه",
    "price": "قیمت تولیدکننده",
}


def title_case_measure(t):
    """Normalise the measure clause's casing: '..., production' -> '..., Production'."""
    def up(m):
        return ", " + m.group(1)[0].upper() + m.group(1)[1:]
    return re.sub(r",\s*([a-z])", lambda m: ", " + m.group(1).upper(), t, count=0)


def main():
    old_title = {}
    for r in csv.DictReader(open(PROPS, encoding="utf-8")):
        old_title[r["chart_id"]] = r["old_title"]

    with open(REG, newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        fields = rd.fieldnames
        rows = list(rd)

    shutil.copy2(REG, REG + ".bak-faostat-titles")
    fixed = 0
    for r in rows:
        cid = r["chart_id"]
        if not cid.startswith("faostat__"):
            continue
        if r["status"] in ("merged", "hidden", "deleted") or r["merged_into"]:
            continue

        parts = cid.split("__")
        commodity = parts[1]
        angle = parts[2] if len(parts) > 2 else ""

        old = old_title.get(cid, "")
        if old:
            new = UNIT_PAREN.sub("", old).strip(" ,;")
        else:
            # chart appeared after the title pass (e.g. a recombined parent): build it
            label = {"production": "Production", "trade": "Imports and Exports",
                     "consumption": "Per-Capita Food Consumption",
                     "price": "Producer Price"}.get(angle, angle.title())
            new = f"{commodity}, {label}"
        # a bare commodity name means the measure is still missing -- put it back
        if new.strip().lower() == commodity.strip().lower():
            label = {"production": "Production", "trade": "Imports and Exports",
                     "consumption": "Per-Capita Food Consumption",
                     "price": "Producer Price"}.get(angle, angle.title())
            new = f"{commodity}, {label}"
        new = title_case_measure(new)

        if new and new != r["title"]:
            r["title"] = new
            fixed += 1

        # Persian: measure + commodity (the FA commodity name is whatever we had)
        fa_m = FA_MEASURE.get(angle)
        if fa_m:
            fa_commodity = (r.get("title_fa") or "").strip()
            # strip any measure phrase already glued on, keep the commodity noun
            for m in FA_MEASURE.values():
                fa_commodity = fa_commodity.replace(m, "").strip("،, ")
            if fa_commodity:
                r["title_fa"] = f"{fa_m} {fa_commodity}"

    with open(REG, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    # sync meta.json
    synced = 0
    for r in rows:
        cid = r["chart_id"]
        if not cid.startswith("faostat__"):
            continue
        mp = os.path.join(CHARTS, cid.replace("/", "_"), "meta.json")
        if not os.path.exists(mp):
            continue
        try:
            m = json.load(open(mp, encoding="utf-8"))
        except Exception:
            continue
        if m.get("title") != r["title"] or m.get("title_fa") != r["title_fa"]:
            m["title"] = r["title"]
            m["title_fa"] = r["title_fa"]
            json.dump(m, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            synced += 1

    print(f"FAOSTAT titles restored: {fixed} | meta.json synced: {synced}")

    # prove the collision is gone
    from collections import Counter
    live = [r for r in rows
            if r["status"] not in ("merged", "hidden", "deleted") and not r["merged_into"]]
    dupes = {t: n for t, n in Counter(r["title"] for r in live).items() if n > 1}
    print(f"live charts sharing a title with another chart: {len(dupes)}")
    for t, n in list(dupes.items())[:5]:
        print(f"   {n}x  {t}")


if __name__ == "__main__":
    main()
