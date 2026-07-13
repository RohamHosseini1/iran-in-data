"""Harmonize banking-history/FDI-concessions raw folders into
data/processed/iran_banking_history_series/ and data/processed/iran_foreign_concessions_series/.
Sources are already clean, well-structured CSVs (event logs / long-format indicator series) --
this script's job is (a) round WDI/FRED floating-point noise in the GFDD file, (b) pass every
other file through csv.DictReader/csv.DictWriter for guaranteed correct quoting per this project's
CSV-writing rule, (c) rename into the processed/ folder with clear filenames. No values altered
beyond float rounding (documented). Never touches data/raw/.
"""
import csv

# Two raw files in this batch have a pre-existing CSV-quoting defect (unescaped comma inside an
# unquoted field -- the exact bug class flagged in docs/bookkeeping.md's CSV-writing-discipline
# rule, apparently written by an earlier agent before that rule was in force). Per project policy
# ("raw data is immutable, fixes happen in data/processed/"), data/raw/ is left untouched and the
# split fields are rejoined here, with no numeric/textual content altered -- only column alignment.
KNOWN_SPLIT_FIELD_FIXES = {
    "data/raw/iran-banking-history/nationalization-1979-consolidation/data.csv": {
        # row (0-indexed data row 12, "1982 post_consolidation_state..."): entity_names field
        # "9 banks / 6,581 branches" was split into 2 columns by its internal comma.
        12: {"merge_cols": (3, 4), "into_field": "entity_names"},
    },
    "data/raw/iran-foreign-concessions-pre1979/automotive-joint-ventures-1956-1979/data.csv": {
        # row (0-indexed data row 1, "Iran National / Peykan-Rootes licence"): foreign_partner
        # field "Rootes Group (UK; became Chrysler UK 1967, then Talbot/Peugeot 1978)" was split.
        1: {"merge_cols": (1, 2), "into_field": "foreign_partner"},
    },
}


def read_with_known_fixes(src):
    fixes = KNOWN_SPLIT_FIELD_FIXES.get(src, {})
    with open(src, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        raw_rows = list(reader)
    rows = []
    for i, raw in enumerate(raw_rows):
        fix = fixes.get(i)
        if fix and len(raw) == len(header) + 1:
            c1, c2 = fix["merge_cols"]
            merged = raw[:c1] + [raw[c1] + "," + raw[c2]] + raw[c2 + 1:]
            raw = merged
            print(f"  [fixed split-field defect] {src} data-row {i}: rejoined columns {c1}+{c2} into '{fix['into_field']}'")
        rows.append(dict(zip(header, raw)))
    return header, rows


def copy_through(src, dst, round_cols=None):
    fieldnames, rows = read_with_known_fixes(src)
    if round_cols:
        for r in rows:
            for c in round_cols:
                if r.get(c):
                    try:
                        r[c] = round(float(r[c]), 4)
                    except ValueError:
                        pass
    with open(dst, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"  wrote {dst}: {len(rows)} rows")

BH = "data/processed/iran_banking_history_series"
FC = "data/processed/iran_foreign_concessions_series"

copy_through(
    "data/raw/worldbank-gfdd/iran-banking-sector-depth-1960-2016/data.csv",
    f"{BH}/worldbank_gfdd_banking_depth_1960_2016.csv",
    round_cols=["value"],
)
copy_through(
    "data/raw/iran-banking-history/branch-network-timeseries/data.csv",
    f"{BH}/branch_network_timeseries_1919_2016.csv",
)
copy_through(
    "data/raw/iran-banking-history/nationalization-1979-consolidation/data.csv",
    f"{BH}/nationalization_1979_consolidation_events.csv",
)
copy_through(
    "data/raw/iran-banking-history/private-bank-reentry-2000-2015/data.csv",
    f"{BH}/private_bank_reentry_2000_2025.csv",
)
copy_through(
    "data/raw/iran-foreign-concessions-pre1979/darcy-concession-1901-terms/data.csv",
    f"{FC}/darcy_oil_concession_1901_terms.csv",
)
copy_through(
    "data/raw/iran-foreign-concessions-pre1979/automotive-joint-ventures-1956-1979/data.csv",
    f"{FC}/automotive_joint_ventures_1956_1979.csv",
)
print("done")
