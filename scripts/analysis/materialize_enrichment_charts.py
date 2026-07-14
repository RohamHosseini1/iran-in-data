#!/usr/bin/env python3
"""
materialize_enrichment_charts.py -- build data/charts/<id>/{data.csv,meta.json} for
the new Iranian-government-source enrichment charts.

The generic archival builder can't read these: the harmonized series come in three
shapes -- tidy long, wide (one column per metric), and tidy-with-compound-quarter
labels ("1357Q1_1978Q2"). Handled explicitly here, per chart, so nothing is guessed.

Emits the standard chart schema (+ original_period_label for sub-annual series,
which is the column the frontend parses for a real time axis). Applies clean
subject-only EN titles (owner rule: no measure/unit in a title) and Persian titles.
Idempotent.
"""
import csv, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG = os.path.join(ROOT, "data", "processed", "CHART_REGISTRY.csv")
CHARTS = os.path.join(ROOT, "data", "charts")
PROC = os.path.join(ROOT, "data", "processed")
csv.field_size_limit(sys.maxsize)

FIELDS = ["country_iso3", "country_name", "year", "value", "unit",
          "variant_code", "variant_label", "source_dataset", "original_period_label"]

# Per-chart build spec. mode: tidy | wide | tidy_quarter
SPECS = {
    "iran_energy__oil_product_domestic_consumption_cbi_1996_2017": dict(
        title="Oil Product Domestic Consumption", title_fa="مصرف داخلی فرآورده‌های نفتی",
        file="iran_industry_energy_enrich_series/oil_product_domestic_consumption_2000_2022.csv",
        mode="tidy"),
    "iran_energy__oil_product_production_by_refinery_sci_2001_2017": dict(
        title="Oil Product Production by Refinery", title_fa="تولید فرآورده‌های نفتی پالایشگاه‌ها",
        file="iran_industry_energy_enrich_series/oil_and_gas_production_sci_yearbook_2001_2017.csv",
        mode="tidy", prefix="oil_product_production_by_refinery"),
    "iran_monetary__government_debt_to_central_bank_1978_2016": dict(
        title="Government Debt to the Central Bank", title_fa="بدهی دولت به بانک مرکزی",
        file="iran_monetary_fiscal_household_enrich_series/government_debt_to_central_bank_quarterly_1978_2016.csv",
        mode="tidy_quarter"),
    "iran_household__heis_analysis_growth_poverty_gini_2023_2025": dict(
        title="Household Expenditure, Poverty and Inequality", title_fa="هزینه خانوار، فقر و نابرابری",
        file="iran_monetary_fiscal_household_enrich_series/heis_analysis_salehi_isfahani_2023_2025.csv",
        mode="tidy"),
    "iran_monetary__liquidity_m2_monetary_base_2000_2023": dict(
        title="Money Supply and Monetary Base", title_fa="نقدینگی و پایه پولی",
        file="cbi_annual_review_series/monetary_banking_aggregates_1379_1401.csv",
        mode="wide", year_col="fiscal_year_western_end",
        metrics=[("liquidity_m2_billion_rials", "Liquidity (M2)", "billion rials"),
                 ("monetary_base_billion_rials", "Monetary base", "billion rials"),
                 ("liquidity_m2_usd_real_2015", "Liquidity (M2), real 2015 US$", "million US$"),
                 ("monetary_base_usd_real_2015", "Monetary base, real 2015 US$", "million US$")]),
    "iranplanbudgetorg__annual_budget_law_totals": dict(
        title="Annual Budget Law Totals", title_fa="ارقام کل قانون بودجه سالانه",
        file="iran_plan_budget_org_series/annual_budget_law_totals_1371_1401.csv",
        mode="wide", year_col="fiscal_year_western_end",
        row_filter=("hierarchy_level", "Grand Total"),
        metrics=[("revenue_rials", "Revenue / resources", "rials"),
                 ("expenditure_rials", "Expenditure / uses", "rials"),
                 ("revenue_usd_real_2015", "Revenue, real 2015 US$", "US$"),
                 ("expenditure_usd_real_2015", "Expenditure, real 2015 US$", "US$")]),
}

GY = re.compile(r"((?:19|20)\d{2})(?:Q(\d))?")


def emit(iso, year, val, unit, code, label, sds, period=""):
    return {"country_iso3": iso or "IRN", "country_name": "Iran", "year": year,
            "value": val, "unit": unit, "variant_code": code, "variant_label": label,
            "source_dataset": sds, "original_period_label": period}


def build(cid, spec):
    src = os.path.join(PROC, spec["file"])
    if not os.path.exists(src):
        print(f"  !! missing source: {spec['file']}")
        return None
    rows = list(csv.DictReader(open(src, newline="", encoding="utf-8")))
    out = []

    if spec["mode"] in ("tidy", "tidy_quarter"):
        for s in rows:
            ind = s.get("indicator_id", "")
            if spec.get("prefix") and not ind.startswith(spec["prefix"]):
                continue
            val, yr = (s.get("value") or "").strip(), (s.get("year") or "").strip()
            if not val or not yr:
                continue
            period = ""
            if spec["mode"] == "tidy_quarter":
                m = GY.search(yr)
                if not m:
                    continue
                gy = m.group(1)
                period = f"{gy}Q{m.group(2)}" if m.group(2) else ""
                yr = gy
            label = ind.split("__")[-1].replace("_", " ") if ind else "value"
            out.append(emit(s.get("country_iso3"), yr, val, s.get("unit", ""),
                            ind or "value", label, s.get("source_dataset", ""), period))

    elif spec["mode"] == "wide":
        rf = spec.get("row_filter")
        for s in rows:
            if rf and (s.get(rf[0]) or "").strip() != rf[1]:
                continue
            yr = (s.get(spec["year_col"]) or "").strip()
            if not yr:
                continue
            for col, label, unit in spec["metrics"]:
                v = (s.get(col) or "").strip()
                if not v:
                    continue
                out.append(emit(s.get("country_iso3"), yr, v, unit, col, label,
                                s.get("source_file", "") or s.get("source_dataset", "")))
    return out


def main():
    with open(REG, newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        fields = rd.fieldnames
        rows = list(rd)

    built = 0
    for r in rows:
        cid = r["chart_id"]
        spec = SPECS.get(cid)
        if not spec:
            continue
        if r["status"] == "extends":
            r["status"] = "new"
        r["title"], r["title_fa"] = spec["title"], spec["title_fa"]

        out = build(cid, spec)
        if not out:
            print(f"  !! no rows for {cid}")
            continue

        folder = os.path.join(CHARTS, cid.replace("/", "_"))
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, "data.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            w.writerows(out)

        yrs = sorted({o["year"] for o in out})
        try:
            cits = json.loads(r["citations_json"]) if r["citations_json"] else []
        except Exception:
            cits = []
        meta = {"chart_id": cid, "title": spec["title"], "title_fa": spec["title_fa"],
                "category": r["category"], "category_fa": r["category_fa"],
                "sources": r["primary_source"], "n_rows": len(out),
                "year_range": [yrs[0], yrs[-1]],
                "countries": sorted({o["country_iso3"] for o in out}), "citations": cits}
        json.dump(meta, open(os.path.join(folder, "meta.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        r["time_range"] = f"{yrs[0]}-{yrs[-1]}"
        print(f"  built {cid}: {len(out)} rows, {yrs[0]}-{yrs[-1]}, "
              f"{len({o['variant_code'] for o in out})} measures")
        built += 1

    with open(REG, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"materialized {built}/{len(SPECS)} enrichment charts")


if __name__ == "__main__":
    main()
