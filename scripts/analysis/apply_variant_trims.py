#!/usr/bin/env python3
"""
apply_variant_trims.py -- apply data/processed/quality_audit/variant_trim_proposals.csv.

Fixes charts whose DIMENSIONS were flattened into dozens/hundreds of "measures"
(owner: "I should not have ten different measures for one chart in most cases").

  trim  -> filter data.csv down to the agreed keep_variant_codes
  split -> a chart jamming 2+ distinct measures becomes one chart per measure
           (parent hidden, children materialized + registered)
  hide  -> appended to confirmed_hides.txt (applied by apply_culls.py)
  keep  -> no-op

Only variant_codes verified to exist in the chart's data.csv are used. Idempotent
for trims; splits skip children that already exist.
"""
import csv, json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG = os.path.join(ROOT, "data", "processed", "CHART_REGISTRY.csv")
CHARTS = os.path.join(ROOT, "data", "charts")
PROPS = os.path.join(ROOT, "data", "processed", "quality_audit", "variant_trim_proposals.csv")
HIDES = os.path.join(ROOT, "data", "processed", "quality_audit", "confirmed_hides.txt")
csv.field_size_limit(sys.maxsize)

# parent_chart_id -> [(child_id, EN title, FA title, predicate on variant_code)]
SPLITS = {
    "iran_disasters__registered_marriages_divorces_1991_2006": [
        ("iran_vital__registered_marriages_1991_2006", "Registered Marriages",
         "ازدواج‌های ثبت‌شده", lambda c: "marriage" in c),
        ("iran_vital__registered_divorces_1991_2006", "Registered Divorces",
         "طلاق‌های ثبت‌شده", lambda c: "divorce" in c),
    ],
    "iran_imidro__sales_export_by_group_2011_2015": [
        ("iran_imidro__sales_by_product_group_2011_2015", "IMIDRO Subsidiary Sales by Product Group",
         "فروش شرکت‌های ایمیدرو به تفکیک گروه محصول", lambda c: c.startswith("sales_")),
        ("iran_imidro__exports_by_product_group_2011_2015", "IMIDRO Subsidiary Exports by Product Group",
         "صادرات شرکت‌های ایمیدرو به تفکیک گروه محصول", lambda c: c.startswith("export_")),
    ],
    "iran_insurance__premium_loss_by_class_1383_1389": [
        ("iran_insurance__earned_premium_by_class_1383_1389", "Insurance Earned Premium by Class",
         "حق بیمه عایدشده به تفکیک رشته", lambda c: "earned_premium" in c),
        ("iran_insurance__incurred_loss_by_class_1383_1389", "Insurance Incurred Loss by Class",
         "خسارت واقع‌شده به تفکیک رشته", lambda c: "incurred_loss" in c),
    ],
    "iran_provincial__financial_markets_insurance_1397_1401": [
        ("iran_provincial__bank_loan_deposit_ratio_1397_1401", "Bank Loan-to-Deposit Ratio by Province",
         "نسبت تسهیلات به سپرده بانکی به تفکیک استان",
         lambda c: c.startswith("bank_loans_to_deposits_ratio_pct_")),
        ("iran_provincial__insurance_premium_per_capita_1397_1401", "Insurance Premium per Capita by Province",
         "حق بیمه سرانه به تفکیک استان",
         lambda c: c.startswith("insurance_premium_per_capita_")),
        ("iran_provincial__insurance_claims_paid_share_1397_1401", "Insurance Claims Paid Share by Province",
         "سهم خسارت پرداختی بیمه به تفکیک استان",
         lambda c: c.startswith("insurance_claims_paid_share_pct_")),
        ("iran_provincial__insurance_premium_written_share_1397_1401", "Insurance Premium Written Share by Province",
         "سهم حق بیمه صادرشده به تفکیک استان",
         lambda c: c.startswith("insurance_premium_written_share_pct_")),
    ],
    "iran_provincial__government_budget_execution_1397_1401": [
        ("iran_provincial__capital_expenditure_share_1397_1401",
         "Capital Expenditure Budget Execution Share by Province",
         "سهم اجرای بودجه عمرانی به تفکیک استان",
         lambda c: c.startswith("capital_expenditure_share_pct_")),
        ("iran_provincial__current_expenditure_share_1397_1401",
         "Current Expenditure Budget Execution Share by Province",
         "سهم اجرای بودجه جاری به تفکیک استان",
         lambda c: c.startswith("current_expenditure_share_pct_")),
    ],
    "iran_provincial__industry_workshops_1396_1400": [
        ("iran_provincial__industrial_production_value_share_1396_1400",
         "Industrial Production Value Share by Province",
         "سهم ارزش تولید صنعتی به تفکیک استان",
         lambda c: c.startswith("industrial_production_value_share_pct_")),
        ("iran_provincial__industrial_workshop_count_share_1396_1400",
         "Industrial Workshop Count Share by Province",
         "سهم تعداد کارگاه صنعتی به تفکیک استان",
         lambda c: c.startswith("industrial_workshop_count_share_pct_")),
    ],
    "pahlavi_hh__dairy_consumption_supply_1972_1977": [
        ("pahlavi_hh__dairy_consumption_by_type_1972_1977", "Dairy Product Consumption by Type",
         "مصرف فرآورده‌های لبنی به تفکیک نوع", lambda c: "consumption" in c),
        ("pahlavi_hh__milk_supply_by_source_1972_1977", "Milk Supply by Animal Source",
         "عرضه شیر به تفکیک منبع دامی", lambda c: "supply" in c),
    ],
}


def read_chart(cid):
    p = os.path.join(CHARTS, cid.replace("/", "_"), "data.csv")
    if not os.path.exists(p):
        return None, None
    with open(p, newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        return rd.fieldnames, list(rd)


def write_chart(cid, cols, rows, meta_base):
    folder = os.path.join(CHARTS, cid.replace("/", "_"))
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "data.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    yrs = sorted({r["year"] for r in rows if r.get("year")})
    meta = dict(meta_base)
    meta.update({"chart_id": cid, "n_rows": len(rows),
                 "year_range": [yrs[0], yrs[-1]] if yrs else None,
                 "countries": sorted({r["country_iso3"] for r in rows if r.get("country_iso3")})})
    json.dump(meta, open(os.path.join(folder, "meta.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    return yrs


def main():
    props = list(csv.DictReader(open(PROPS, encoding="utf-8")))
    with open(REG, newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        fields = rd.fieldnames
        regrows = list(rd)
    reg = {r["chart_id"]: r for r in regrows}
    shutil.copy2(REG, REG + ".bak-varianttrim")

    n_trim = n_split = n_hide = 0
    new_hides = []

    for p in props:
        cid, action = p["chart_id"], p["action"]
        if action == "keep":
            continue
        if action == "hide":
            new_hides.append(cid)
            n_hide += 1
            continue

        cols, rows = read_chart(cid)
        if not rows:
            print(f"  !! no data for {cid}")
            continue
        parent = reg.get(cid)
        if not parent:
            continue

        if action == "trim":
            keep = {c for c in p["keep_variant_codes"].split("|") if c}
            kept = [r for r in rows if r.get("variant_code") in keep]
            if not kept:
                print(f"  !! trim would empty {cid}, skipped")
                continue
            base = {"title": parent["title"], "title_fa": parent["title_fa"],
                    "category": parent["category"], "category_fa": parent["category_fa"],
                    "sources": parent["primary_source"],
                    "citations": json.loads(parent["citations_json"] or "[]")}
            write_chart(cid, cols, kept, base)
            before = len({r["variant_code"] for r in rows})
            after = len({r["variant_code"] for r in kept})
            print(f"  trim  {cid}: {before} -> {after} measures")
            n_trim += 1

        elif action == "split":
            children = SPLITS.get(cid)
            if not children:
                print(f"  !! no split spec for {cid}")
                continue
            keep = {c for c in p["keep_variant_codes"].split("|") if c}
            made = []
            for child_id, en, fa, pred in children:
                sub = [r for r in rows
                       if r.get("variant_code") in keep and pred(r["variant_code"])]
                if not sub:
                    print(f"     !! no rows for child {child_id}")
                    continue
                base = {"title": en, "title_fa": fa,
                        "category": parent["category"], "category_fa": parent["category_fa"],
                        "sources": parent["primary_source"],
                        "citations": json.loads(parent["citations_json"] or "[]")}
                yrs = write_chart(child_id, cols, sub, base)
                if child_id not in reg:
                    row = {k: "" for k in fields}
                    row.update({
                        "chart_id": child_id, "title": en, "title_fa": fa,
                        "category": parent["category"], "category_fa": parent["category_fa"],
                        "primary_source": parent["primary_source"],
                        "underlying_codes": parent["underlying_codes"],
                        "status": "new", "merged_into": "",
                        "time_range": f"{yrs[0]}-{yrs[-1]}" if yrs else "",
                        "citations_json": parent["citations_json"],
                        "notes": f"Split from {cid} by the 2026-07-14 variant-trim pass "
                                 f"(parent jammed multiple distinct measures into one chart).",
                    })
                    regrows.append(row)
                    reg[child_id] = row
                made.append(f"{child_id}({len({r['variant_code'] for r in sub})})")
            # hide the parent, pointing at the first child
            parent["status"] = "merged"
            parent["merged_into"] = children[0][0]
            parent["notes"] = (parent.get("notes", "") + " || 2026-07-14 variant-trim: split into "
                               + ", ".join(c[0] for c in children)).strip(" |")
            print(f"  split {cid} -> {', '.join(made)}")
            n_split += 1

    with open(REG, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(regrows)

    if new_hides:
        with open(HIDES, "a", encoding="utf-8") as f:
            f.write("\n# variant-trim pass: grab-bags of one-off facts, no measure over time\n")
            for h in new_hides:
                f.write(h + "\n")

    print(f"\ntrimmed {n_trim} | split {n_split} | queued-for-hide {n_hide}")
    print("now run: apply_culls.py, then build_catalog_index.py")


if __name__ == "__main__":
    main()
