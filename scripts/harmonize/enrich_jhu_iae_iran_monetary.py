#!/usr/bin/env python3
"""
Harmonizes the JHU IAE / Haver Analytics quarterly Iran central-bank monetary aggregates
(1998Q4-2016Q2) into data/processed/iran_monetary_fiscal_household_enrich_series/.

Source: data/raw/jhu-iae-haver-iran-monetary/cbi-balance-sheet-quarterly-1998-2016/
Schema: country_iso3, indicator_id, year, value, unit, source_dataset
"""
import csv
import os
import re
import pandas as pd

ROOT = "/Users/rohamhosseini/Iran Economic database"
SRC = os.path.join(ROOT, "data/raw/jhu-iae-haver-iran-monetary/cbi-balance-sheet-quarterly-1998-2016/"
                    "iran_central_bank_balance_sheet_1998q4_2016q2.xlsx")
OUT = os.path.join(ROOT, "data/processed/iran_monetary_fiscal_household_enrich_series",
                    "jhu_iae_haver_cbi_monetary_aggregates_quarterly_1998_2016.csv")


def slugify(desc: str) -> str:
    s = desc.split("(")[0].strip()  # drop the "(NSA, EOP, Bil.Rials)" suffix
    s = s.replace("Iran: Money Supply:", "").replace("Iran:", "").strip()
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_").lower()
    return s


def main():
    df = pd.read_excel(SRC, sheet_name="Iran monetary data", header=None)
    mnemonics = df.iloc[3]
    descs = df.iloc[4]
    sources = df.iloc[5]

    col_meta = {}
    seen_slugs = {}
    for j in range(1, df.shape[1]):
        mnem = mnemonics[j]
        desc = descs[j]
        if pd.isna(mnem) or pd.isna(desc):
            continue
        slug = slugify(str(desc))
        # disambiguate duplicate descriptions (source has 2 pairs of repeated labels
        # representing the same concept split by a different hierarchy grouping)
        if slug in seen_slugs:
            seen_slugs[slug] += 1
            slug = f"{slug}_v{seen_slugs[slug]}"
        else:
            seen_slugs[slug] = 1
        col_meta[j] = {
            "mnemonic": str(mnem).strip(),
            "desc": str(desc).strip(),
            "slug": slug,
            "lsource": str(sources[j]).strip() if not pd.isna(sources[j]) else "",
        }

    rows = []
    for i in range(8, len(df)):
        period = df.iloc[i, 0]
        if pd.isna(period):
            continue
        period = str(period).strip()
        if not re.match(r"^\d{4}-Q[1-4]$", period):
            continue
        for j, meta in col_meta.items():
            val = df.iloc[i, j]
            if pd.isna(val):
                continue
            rows.append({
                "country_iso3": "IRN",
                "indicator_id": f"jhu_iae_haver__{meta['slug']}",
                "year": period,
                "value": val,
                "unit": "billion_rials_nsa_eop",
                "source_dataset": (f"jhu-iae-haver-iran-monetary/cbi-balance-sheet-quarterly-1998-2016 "
                                    f"(haver_mnemonic={meta['mnemonic']}, "
                                    f"description={meta['desc']}, lsource={meta['lsource']})"),
            })

    rows.sort(key=lambda r: (r["indicator_id"], r["year"]))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["country_iso3", "indicator_id", "year", "value", "unit", "source_dataset"])
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"wrote {OUT} ({len(rows)} rows, {len(col_meta)} indicators)")
    for j, m in col_meta.items():
        print(" ", m["slug"], "<-", m["desc"])


if __name__ == "__main__":
    main()
