#!/usr/bin/env python3
"""
build_law_mapping_inputs.py -- prepare the two inputs the law->chart mapping fleet needs.

1. data/processed/laws/chart_index_for_mapping.tsv
   Every LIVE chart, compact: chart_id, title, category, year_range. This is what a
   mapping agent scans to decide which charts a policy could plausibly move.

2. data/processed/laws/laws_shortlist_typed.csv
   The economic shortlist, plus a document-TYPE tag, because type predicts importance:
     law            (قانون)            -- primary legislation: VAT, subsidy reform, privatization
     bylaw          (آيين‌نامه اجرايي) -- implementing regulation for one clause; usually derivative
     decree         (تصويب‌نامه)        -- cabinet decree
     court_ruling   (رأي / divan)      -- can still ANNUL an economic regulation, so kept
     amendment      (اصلاحيه)
     other
"""
import csv, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG = os.path.join(ROOT, "data", "processed", "CHART_REGISTRY.csv")
LAWS = os.path.join(ROOT, "data", "processed", "laws")
csv.field_size_limit(sys.maxsize)


def doc_type(title, folder):
    t = title.replace("‌", " ")
    if folder.startswith("Divan"):
        return "court_ruling"
    if re.search(r"اصلاحي?ه", t):
        return "amendment"
    if re.search(r"آي?ي?ن\s*نامه|آئين\s*نامه|آيين‌نامه", t):
        return "bylaw"
    if re.search(r"تصويب\s*نامه|تصويب‌نامه", t):
        return "decree"
    if re.search(r"^قانون|\bقانون\b", t):
        return "law"
    return "other"


def main():
    # 1. chart index
    rows = list(csv.DictReader(open(REG, encoding="utf-8")))
    live = [r for r in rows
            if r["status"] not in ("merged", "hidden", "deleted") and not r["merged_into"]]
    live.sort(key=lambda r: (r["category"], r["title"]))
    out1 = os.path.join(LAWS, "chart_index_for_mapping.tsv")
    with open(out1, "w", encoding="utf-8") as f:
        f.write("chart_id\ttitle\tcategory\tyear_range\n")
        for r in live:
            f.write(f"{r['chart_id']}\t{r['title']}\t{r['category']}\t{r.get('time_range','')}\n")
    print(f"chart index: {len(live)} live charts -> {out1}")

    # 2. typed law shortlist
    short = list(csv.DictReader(open(os.path.join(LAWS, "laws_economic_shortlist.csv"), encoding="utf-8")))
    cols = list(short[0].keys()) + ["doc_type"]
    out2 = os.path.join(LAWS, "laws_shortlist_typed.csv")
    from collections import Counter
    tc = Counter()
    with open(out2, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in short:
            r["doc_type"] = doc_type(r["title"], r["folder"])
            tc[r["doc_type"]] += 1
            w.writerow(r)
    print(f"typed shortlist: {len(short)} -> {out2}")
    print("by doc_type:", dict(tc.most_common()))

    # category summary, useful for broad laws that hit a whole domain
    cats = Counter(r["category"] for r in live)
    print(f"\nchart categories ({len(cats)}):")
    for c, n in cats.most_common(12):
        print(f"   {n:5d}  {c}")


if __name__ == "__main__":
    main()
