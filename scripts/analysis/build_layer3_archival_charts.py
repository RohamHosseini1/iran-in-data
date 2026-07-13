"""Materialize Layer 3 (data/charts/<chart_id>/data.csv + meta.json) for the archival/
hand-curated chart_ids in CHART_REGISTRY.csv that build_layer3_charts.py deliberately skipped
(chart_ids NOT prefixed wdi__/weo__/owid__/faostat__/wid__, whose underlying_codes point at
heterogeneous data/processed/*_series/*.csv files instead of the uniform macro_wdi.csv-style
indexed files).

Originally covered the first ~213 such chart_ids (groups 0-22). Extended 2026-07-13 (groups 23-24)
to cover 56 more chart_ids added to the registry via newly-merged staging batches (the
us_primary_source_archives.csv staging file and several iran-institutional/modernization/
specialty-goods folders) -- same schema/conventions, same idempotent-per-chart_id design, just
two more narrative-citation-series source shapes (date_label/category/subcategory and
year/metric) that groups 0-22 hadn't needed a generic helper for yet.

Target schema (matches the 1,576 machine-readable charts exactly):
  data.csv columns: country_iso3, country_name, year, value, unit, variant_code, variant_label,
    source_dataset  [+ original_period_label when the source used a fiscal/Persian-calendar label
    distinct from the resolved Western year] [+ computed when USD-converted variant rows exist]
  meta.json fields: chart_id, title, category, sources, n_rows, year_range, countries, citations
    (citations copied directly from the registry row's citations_json -- already computed for
    ~98% of rows, per project convention; never re-derived here).

Never modifies data/raw/, data/processed/*_series/ originals, or CHART_REGISTRY.csv. Only writes
under data/charts/<chart_id>/. Designed to be safely re-run (idempotent overwrite per chart_id).

This required genuine per-file judgment (see docs/bookkeeping.md task brief) -- source schemas
vary hugely: some are already category/subcategory/value/unit long format (near-identical to the
target), some are wide (one row per entity, several numeric metric columns needing a melt), some
use Iranian dual-year or solar-Hijri year notation needing conversion (original label preserved
in `original_period_label`), and a few are pure narrative text with no numeric value at all
(value left blank, narrative preserved in a `notes` column) -- never fabricated, interpolated, or
dropped.
"""
import csv
import json
import os
import re
import sys

sys.path.insert(0, "scripts/harmonize")
from country_crosswalk import COUNTRIES  # noqa: E402

REGISTRY = "data/processed/CHART_REGISTRY.csv"
OUT_DIR = "data/charts"
PROC = "data/processed"
# Round 2 (2026-07-13, groups 23-24) writes to its own dated log per task instructions --
# log() appends every line immediately (not buffered to end-of-run), so this file is valid
# to inspect mid-run if the process is ever interrupted. The original groups 0-22 log lives
# at archival-layer3-materialization.log and is left alone.
LOG_PATH = "logs/downloads/archival-layer3-materialization-round2.log"

import datetime


def log(msg):
    line = f"{datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')} {msg}"
    print(line)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")


# ----------------------------------------------------------------------------
# generic helpers
# ----------------------------------------------------------------------------

def slugify(s):
    s = (s or "").strip().lower()
    s = re.sub(r"[^\w]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "value"


def dualyear_to_year(label):
    """'1958/59' -> 1959 ; '1962' -> 1962 ; 'proj_1970/71' -> 1971 (later Western year).
    Reused exactly from scripts/harmonize/harmonize_pahlavi_government_finance.py so the
    convention is identical project-wide."""
    if label is None:
        return ""
    label = str(label).strip()
    if not label:
        return ""
    core = label.split("_", 1)[-1] if label.startswith(("proj_", "first_6mo_")) else label
    if "/" in core:
        first = core.split("/")[0]
        suffix = core.split("/")[1]
        century_prefix = first[: -len(suffix)] if len(suffix) < len(first) else ""
        try:
            return int(century_prefix + suffix)
        except ValueError:
            return ""
    m = re.match(r"^-?\d{3,4}$", core)
    if m:
        try:
            return int(core)
        except ValueError:
            return ""
    return ""


def sh_to_gregorian(sh_year):
    """Solar-Hijri (Iranian) year -> approximate Gregorian year, per this project's own
    established convention (already used throughout iran_census_demographics_series and
    sci_yearbook_1399_series files, which pair solar_year with gregorian_year(_approx) columns
    computed as solar_year + 621 -- verified against those existing pairs, e.g. 1375->1996,
    1390->2011). Applied here only to sh-only files that lack a pre-computed Gregorian column."""
    try:
        return int(sh_year) + 621
    except (ValueError, TypeError):
        return ""


def extract_year_from_date(s):
    if not s:
        return ""
    m = re.search(r"(19|20)\d{2}", str(s))
    return int(m.group(0)) if m else ""


def leading_year(s):
    """'1982_high' -> 1982 ; '1975 (planned)' -> 1975 ; '2025-05' -> 2025 (a YYYY-MM period,
    not a genuine multi-year range) ; plain '2024' -> 2024. Returns '' if no leading 4-digit
    year is present."""
    if not s:
        return ""
    m = re.match(r"^(\d{4})(?:-\d{2}\b|[_\s(].*)?$", str(s).strip())
    return int(m.group(1)) if m else ""


def fiscal_range_to_later_year(s):
    """'2005-2006' (Iranian-fiscal-year-style Western-calendar range, hyphen variant of the
    documented '1963/64'-style dual-year notation) -> 2006 (later Western year, same convention
    as dualyear_to_year). Returns '' for anything else (including genuine multi-year
    ranges/averages, which must stay blank per project convention -- callers decide which case
    applies for their specific file)."""
    if not s:
        return ""
    m = re.match(r"^(\d{4})-(\d{4})$", str(s).strip())
    if not m:
        return ""
    y1, y2 = int(m.group(1)), int(m.group(2))
    return y2 if y2 == y1 + 1 else ""


def first_number(s):
    """Best-effort extraction of the first numeric token in a free-text string (e.g.
    'US$22.00 million' -> 22.00). Used only for a couple of narrative before/after tables where
    the source itself prints the number inline with prose -- not a fabrication, just parsing what
    the source already states."""
    if s is None:
        return None
    m = re.search(r"-?\d[\d,]*\.?\d*", str(s))
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", ""))
    except ValueError:
        return None


def load_csv(path):
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))


def load_registry():
    return {r["chart_id"]: r for r in load_csv(REGISTRY)}


REG = load_registry()
EXISTING = set(os.listdir(OUT_DIR))
STATS = {"built": 0, "skipped": 0, "rows_total": 0}
SKIPPED = []


def cname(iso3):
    return COUNTRIES.get(iso3, iso3)


BASE_FIELDS = ["country_iso3", "country_name", "year", "value", "unit",
               "variant_code", "variant_label", "source_dataset"]
OPTIONAL_ORDER = ["original_period_label", "computed", "notes"]


def write_chart(chart_id, rows):
    """rows: list of dicts with at least the BASE_FIELDS keys (year/value may be '').
    Drops rows with no chart_id in the registry (should never happen -- caller bug if so)."""
    if chart_id not in REG:
        log(f"ERROR chart_id not in registry, skipping: {chart_id}")
        return 0
    reg = REG[chart_id]
    rows = [r for r in rows if r is not None]
    if not rows:
        log(f"SKIP {chart_id}: zero rows produced")
        SKIPPED.append((chart_id, "zero rows produced"))
        STATS["skipped"] += 1
        return 0
    folder = os.path.join(OUT_DIR, chart_id.replace("/", "_"))
    os.makedirs(folder, exist_ok=True)
    used_optional = [c for c in OPTIONAL_ORDER if any(r.get(c) not in (None, "") for r in rows)]
    fieldnames = BASE_FIELDS + used_optional
    with open(os.path.join(folder, "data.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})
    years = sorted({str(r["year"]) for r in rows if r.get("year") not in (None, "")},
                    key=lambda y: (len(y), y))
    countries = sorted({r["country_iso3"] for r in rows if r.get("country_iso3")})
    citations = []
    if reg.get("citations_json"):
        try:
            citations = json.loads(reg["citations_json"])
        except json.JSONDecodeError:
            citations = []
    meta = {
        "chart_id": chart_id,
        "title": reg["title"],
        "category": reg["category"],
        "sources": reg["primary_source"],
        "n_rows": len(rows),
        "year_range": [years[0], years[-1]] if years else None,
        "countries": countries,
        "citations": citations,
    }
    with open(os.path.join(folder, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    STATS["built"] += 1
    STATS["rows_total"] += len(rows)
    log(f"OK {chart_id}: {len(rows)} rows -> {folder}")
    return len(rows)


def base_row(country_iso3, year, value, unit, variant_code, variant_label, source_dataset,
             original_period_label=None, computed=None, notes=None, country_name=None):
    r = {
        "country_iso3": country_iso3,
        "country_name": country_name if country_name is not None else cname(country_iso3),
        "year": year if year not in (None,) else "",
        "value": value if value is not None else "",
        "unit": unit or "",
        "variant_code": variant_code,
        "variant_label": variant_label,
        "source_dataset": source_dataset or "",
    }
    if original_period_label:
        r["original_period_label"] = original_period_label
    if computed is not None:
        r["computed"] = "true" if computed else "false"
    if notes:
        r["notes"] = notes
    return r


# ----------------------------------------------------------------------------
# family helper: category/subcategory/value/unit rows (pahlavi WB/USBM-table schema),
# optionally carrying fiscal_year_label + value_usd_nominal/value_usd_real_2015
# ----------------------------------------------------------------------------

def rows_from_catsub(records, source_dataset_override=None, category_filter=None,
                      country_iso3="IRN"):
    out = []
    for r in records:
        if category_filter and not category_filter(r):
            continue
        cat = (r.get("category") or "").strip()
        sub = (r.get("subcategory") or "").strip()
        label = f"{cat} — {sub}" if sub else cat
        vcode = slugify(label)
        sd = source_dataset_override or r.get("source_dataset", "")
        ciso = r.get("country_iso3") or country_iso3
        yr = r.get("year", "")
        fyl = r.get("fiscal_year_label", "")
        has_usd = bool(r.get("value_usd_nominal") or r.get("value_usd_real_2015"))
        b = base_row(ciso, yr, r.get("value", ""), r.get("unit", ""), vcode, label, sd,
                     original_period_label=fyl if fyl and fyl != yr else None,
                     computed=False if has_usd else None)
        out.append(b)
        if r.get("value_usd_nominal"):
            out.append(base_row(ciso, yr, r["value_usd_nominal"], "current US$ (computed)",
                                 vcode + ".USD_NOMINAL", label + " (computed, nominal US$)", sd,
                                 original_period_label=fyl if fyl and fyl != yr else None,
                                 computed=True,
                                 notes=r.get("currency_conversion_note", "")))
        if r.get("value_usd_real_2015"):
            out.append(base_row(ciso, yr, r["value_usd_real_2015"], "constant 2015 US$ (computed)",
                                 vcode + ".USD_REAL_2015", label + " (computed, real 2015 US$)", sd,
                                 original_period_label=fyl if fyl and fyl != yr else None,
                                 computed=True,
                                 notes=r.get("currency_conversion_note", "")))
    return out


def rows_from_long(records, year_field, value_field, unit_field=None, label_fields=(),
                    source_dataset="", country_field="country_iso3", default_country="IRN",
                    year_transform=None, static_year=None, notes_field=None,
                    variant_code_suffix=""):
    """Generic 'already mostly long format' loader: one numeric value per row, label built
    from label_fields, year resolved from year_field (optionally transformed)."""
    out = []
    for r in records:
        val = r.get(value_field, "")
        if val in (None, ""):
            continue
        if static_year is not None:
            yr = static_year
        elif year_transform:
            yr = year_transform(r)
        else:
            yr = r.get(year_field, "")
        label_parts = [str(r[f]).strip() for f in label_fields if r.get(f)]
        label = " — ".join(label_parts) if label_parts else value_field
        vcode = slugify(label) + variant_code_suffix
        ciso = r.get(country_field) or default_country
        out.append(base_row(ciso, yr, val, r.get(unit_field, "") if unit_field else "",
                             vcode, label, source_dataset,
                             notes=r.get(notes_field, "") if notes_field else None))
    return out


def melt_wide(records, id_fields, value_fields, year_field=None, static_year=None,
              unit_map=None, source_dataset="", country_field="country_iso3",
              default_country="IRN", year_transform=None, notes_field=None):
    """One row per entity with several numeric metric columns -> one output row per
    (entity, metric) pair, skipping blanks. `value_fields` may be a list of column names or a
    dict {column_name: unit_string}."""
    if isinstance(value_fields, dict):
        vf_units = value_fields
    else:
        vf_units = {vf: (unit_map or {}).get(vf, "") for vf in value_fields}
    out = []
    for r in records:
        if static_year is not None:
            yr = static_year
        elif year_transform:
            yr = year_transform(r)
        else:
            yr = r.get(year_field, "") if year_field else ""
        id_label = " — ".join(str(r[f]).strip() for f in id_fields if r.get(f))
        ciso = r.get(country_field) or default_country
        for vf, unit in vf_units.items():
            val = r.get(vf, "")
            if val in (None, ""):
                continue
            label = f"{id_label} — {vf}" if id_label else vf
            vcode = slugify(label)
            out.append(base_row(ciso, yr, val, unit, vcode, label, source_dataset,
                                 notes=r.get(notes_field, "") if notes_field else None))
    return out


def expand_pipe_filter(spec, prefix):
    parts = [p.strip() for p in spec.split("|")]
    out = []
    for p in parts:
        out.append(p if p.startswith(prefix) else prefix + p)
    return out


log("=" * 70)
log("Starting archival Layer 3 materialization run")
missing = sorted(cid for cid in REG if cid.replace("/", "_") not in EXISTING)
log(f"Registry rows without a data/charts/ folder: {len(missing)}")
CASE_COLLISION_RESOLVED = {"faostat__Cereals, other__trade", "faostat__Cereals, other__consumption"}
missing = [cid for cid in missing if cid not in CASE_COLLISION_RESOLVED]
log(f"After excluding already-resolved case-collision duplicates: {len(missing)} to build")

# ============================================================================
# GROUP 0: three stray machine-readable-source chart_ids (wdi__/faostat__/owid__ prefix)
# added to the registry after build_layer3_charts.py's last run -- same pipeline, reused here.
# ============================================================================

def group0_machine_strays():
    # NOTE: "faostat__Cereals, other__{trade,consumption}" (lowercase "other") is a genuine
    # separate CHART_REGISTRY.csv row, but collides case-insensitively on disk with the
    # pre-existing "faostat__Cereals, Other__{trade,consumption}" (capital "Other") chart from
    # the original 1,576-chart build -- and FAOSTAT's own FBS file spells the item "Cereals,
    # other" while FBSH spells it "Cereals, Other", so the two registry rows were each written to
    # match one file's casing. Resolved once (2026-07-13) by merging both item-string casings
    # (both FBS and FBSH domains) into the pre-existing capital-"Other" folder so no data from
    # either registry row is lost; meta.json there carries a `notes_on_case_collision` field
    # documenting this. Do not re-attempt the lowercase path here -- it would silently re-collide.
    pass

    if "owid__hdi" in missing:
        owid = load_csv(os.path.join(PROC, "owid_indicators.csv"))
        rows = []
        for r in owid:
            if not r.get("indicator_id", "").startswith("human-development-index"):
                continue
            if not r.get("value"):
                continue
            rows.append(base_row(r["country_iso3"], r["year"], r["value"], r.get("unit", ""),
                                  r["indicator_id"], r.get("indicator_label", "Human Development Index"),
                                  "owid"))
            rows[-1]["country_name"] = r.get("country_name", cname(r["country_iso3"]))
        write_chart("owid__hdi", rows)


group0_machine_strays()

# ============================================================================
# GROUP 1: pahlavi__ World Bank / USBM archival tables -- category/subcategory/value/unit schema,
# matched by exact source_dataset id (== underlying_codes for this group).
# ============================================================================

PAHLAVI_DIRS = [
    "pahlavi_agriculture_trade_extensions",
    "pahlavi_oil_energy_series",
    "pahlavi_government_finance_series",
]


def load_catsub_index():
    """source_dataset value -> list of rows, scanned across all pahlavi_* archival folders."""
    idx = {}
    file_of = {}
    for d in PAHLAVI_DIRS:
        folder = os.path.join(PROC, d)
        if not os.path.isdir(folder):
            continue
        for fn in sorted(os.listdir(folder)):
            if not fn.endswith(".csv"):
                continue
            path = os.path.join(folder, fn)
            recs = load_csv(path)
            if not recs or "source_dataset" not in recs[0]:
                continue
            for r in recs:
                sd = r.get("source_dataset", "")
                idx.setdefault(sd, []).append(r)
                file_of.setdefault(sd, path)
    return idx, file_of


CATSUB_IDX, CATSUB_FILE = load_catsub_index()

# 1:1 source_dataset -> chart_id (whole table becomes the chart)
PAHLAVI_1TO1 = [
    "wb1962-agriculturetable1-crop-land-production-value",
    "wb1962-agriculturetable2-livestock-production-value",
    "wb1960-table16-exports-by-commodities",
    "wb1960-table17-imports-by-commodities",
    "wb1962-transporttable7-ocean-trade",
    "wb1960-table1-oil-revenues",
    "wb1971-table9-oil-exports-and-revenues",
    "wb1971-table8.8-domestic-consumption-of-oil-products",
    "wb1960-table2-petroleum-statistics",
    "wb1971-table8.9-production-and-consumption-of-gas",
    "wb1974-table15.3-electric-power-generation-by-plant-and-use",
    "wb1974-table15.2-power-generating-capacity",
    "usbm1963-aioc-profits-royalties-1910-1951",
    "usbm1963-consortium-disbursements-1954-1962",
    "usbm1963-oil-industry-employment-1939-1960",
    "usbm1963-oil-industry-personnel-by-category-1955-1961",
    "usbm1963-oil-revenue-distribution-1957-1959",
]


def group1_pahlavi_1to1():
    for r in load_csv(REGISTRY):
        cid = r["chart_id"]
        if cid not in missing:
            continue
        uc = r["underlying_codes"]
        if uc in PAHLAVI_1TO1:
            recs = CATSUB_IDX.get(uc, [])
            write_chart(cid, rows_from_catsub(recs))


group1_pahlavi_1to1()

# the 7 crop categories from wb1960-table5-agricultural-production sharing one source table
AG_PRODUCTION_CATEGORY = {
    "pahlavi__other_grains_production_1950_1958": "Other grains",
    "pahlavi__vegetables_melons_production_1950_1958": "Vegetables & melons",
    "pahlavi__fresh_fruits_noncitrus_production_1950_1958": "Fresh fruits (non-citrus) & berries",
    "pahlavi__dried_apricots_production_1950_1958": "Dried Apricots",
    "pahlavi__raisins_production_1950_1958": "Raisins",
    "pahlavi__other_dried_fruits_production_1950_1958": "Other Dried Fruits",
    "pahlavi__animal_fats_production_1950_1958": "Animal Fats",
}


def group1b_ag_production_split():
    recs = CATSUB_IDX.get("wb1960-table5-agricultural-production", [])
    for cid, cat in AG_PRODUCTION_CATEGORY.items():
        if cid not in missing:
            continue
        write_chart(cid, rows_from_catsub(recs, category_filter=lambda r, c=cat: r.get("category") == c))


group1b_ag_production_split()

# ============================================================================
# GROUP 2: pahlavi__ government-finance series -- same category/subcategory schema, but each
# chart_id maps 1:1 to its own file under pahlavi_government_finance_series/ (underlying_codes
# gives "filename.csv|source_dataset_id").
# ============================================================================

PAHLAVI_GOVFIN_FILES = [
    "bank_deposits_private_sector_1963_70.csv",
    "banking_statistics_private_sector_1957_59.csv",
    "century_indicators_1900_2006.csv",
    "fiscal_system_narrative_indicators_1921_79.csv",
    "monetary_aggregates_movements_1963_73.csv",
    "monetary_survey_1963_70.csv",
    "money_quasi_money_changes_1965_71.csv",
    "money_supply_changes_1957_59.csv",
]


def _repair_known_csv_corruption(recs, fn):
    """One row in fiscal_system_narrative_indicators_1921_79.csv has an unescaped comma inside
    its `category` text ('...(planned, not fully disbursed)') that silently shifted every
    subsequent column by one -- a known bug class documented in docs/bookkeeping.md ('CSV-writing
    discipline'). Never touching the source file itself (forbidden); this reconstructs the one
    affected row for OUR output only, re-assembling the numbers that ARE present in the source
    (32, percent) rather than dropping or fabricating them. Original raw fields kept in notes for
    auditability. No-op for every other file/row."""
    if fn != "fiscal_system_narrative_indicators_1921_79.csv":
        return recs
    for r in recs:
        if r.get("category", "").rstrip().endswith("(planned") and r.get("value", "").strip() == "not fully disbursed)":
            raw = dict(r)
            r["category"] = "First Seven-Year Plan World Bank loan share (planned, not fully disbursed)"
            r["subcategory"] = ""
            r["value"] = r.get("unit", "")  # the shifted value landed in the unit slot ('32')
            r["unit"] = "percent"
            r["notes"] = (f"[reconstructed from a comma-corrupted source row -- original raw fields: "
                           f"category={raw.get('category')!r}, value={raw.get('value')!r}, "
                           f"unit={raw.get('unit')!r}, notes={raw.get('notes')!r}]")
    return recs


def group2_pahlavi_govfin():
    folder = os.path.join(PROC, "pahlavi_government_finance_series")
    for fn in PAHLAVI_GOVFIN_FILES:
        path = os.path.join(folder, fn)
        if not os.path.exists(path):
            log(f"WARN missing expected file {path}")
            continue
        recs = load_csv(path)
        recs = _repair_known_csv_corruption(recs, fn)
        sd = recs[0]["source_dataset"] if recs else ""
        # find the chart_id in registry whose underlying_codes references this filename
        for r in load_csv(REGISTRY):
            cid = r["chart_id"]
            if cid not in missing:
                continue
            if fn in r["underlying_codes"]:
                write_chart(cid, rows_from_catsub(recs))


group2_pahlavi_govfin()

log(f"After groups 0-2: built={STATS['built']} skipped={STATS['skipped']} rows={STATS['rows_total']}")

# ============================================================================
# GROUP 3: pahlavi_hh__ household-consumption series -- 6 files, 1:1, bespoke small schemas.
# ============================================================================

def group3_pahlavi_hh():
    d = os.path.join(PROC, "pahlavi_household_consumption_series")

    if "pahlavi_hh__expenditure_shares_by_category_1965_1971" in missing:
        recs = load_csv(os.path.join(d, "expenditure_composition_shares_1965_1971.csv"))
        rows = rows_from_long(recs, "year", "value", unit_field="unit",
                               label_fields=("area", "metric"),
                               source_dataset="wb1974-cep-table9.2-expenditure-composition-shares")
        write_chart("pahlavi_hh__expenditure_shares_by_category_1965_1971", rows)

    if "pahlavi_hh__expenditure_levels_rials_1965_1971" in missing:
        recs = load_csv(os.path.join(d, "expenditure_levels_rials_1965_1971.csv"))
        rows = rows_from_long(recs, "year", "value", unit_field="unit",
                               label_fields=("area", "metric"),
                               source_dataset="wb1974-cep-table9.1-expenditure-levels",
                               notes_field="notes")
        write_chart("pahlavi_hh__expenditure_levels_rials_1965_1971", rows)

    if "pahlavi_hh__expenditure_distribution_by_bracket_1971" in missing:
        recs = load_csv(os.path.join(d, "expenditure_distribution_by_bracket_1971.csv"))
        rows = []
        for r in recs:
            for vf, unit in [("pct_households", "percent of households"),
                              ("cumulative_pct", "cumulative percent")]:
                if not r.get(vf):
                    continue
                label = f"{r['monthly_expenditure_bracket_rials']} — {r['group']} — {vf}"
                rows.append(base_row("IRN", r.get("year", ""), r[vf], unit, slugify(label), label,
                                      "wb1974-cep-table9.3-expenditure-distribution-by-bracket"))
        write_chart("pahlavi_hh__expenditure_distribution_by_bracket_1971", rows)

    if "pahlavi_hh__dairy_consumption_supply_1972_1977" in missing:
        recs = load_csv(os.path.join(d, "dairy_consumption_supply_1972_1977.csv"))
        rows = []
        for r in recs:
            for vf, unit in [("product_000tons_or_000head", "'000 tons or '000 head"),
                              ("fat_equivalent_tons", "fat-equivalent tons"),
                              ("pct_of_total", "percent of total")]:
                if not r.get(vf):
                    continue
                label = f"{r['category']} — {r['item']} — {vf}"
                rows.append(base_row(r.get("country_iso3", "IRN"), r.get("year", ""), r[vf], unit,
                                      slugify(label), label,
                                      "wb1974-cep-statistical-appendix-dairy-consumption-supply",
                                      notes=r.get("note", "")))
        write_chart("pahlavi_hh__dairy_consumption_supply_1972_1977", rows)

    if "pahlavi_hh__food_demand_actual_projected_1972_1982" in missing:
        recs = load_csv(os.path.join(d, "food_demand_actual_and_projected_1972_1982.csv"))
        rows = []
        for r in recs:
            for vf in ("rural_000tons", "urban_000tons", "total_000tons"):
                if not r.get(vf):
                    continue
                label = f"{r['commodity']} — {vf}"
                rows.append(base_row(r.get("country_iso3", "IRN"), leading_year(r.get("period", "")), r[vf],
                                      "'000 tons", slugify(label), label,
                                      "wb1974-cep-statistical-appendix-food-demand",
                                      original_period_label=r.get("period", ""), notes=r.get("note", "")))
        write_chart("pahlavi_hh__food_demand_actual_projected_1972_1982", rows)

    if "pahlavi_hh__nonfood_consumption_index_1955_1958" in missing:
        recs = load_csv(os.path.join(d, "per_capita_consumption_index_1955_1958.csv"))
        keep = {"tobacco", "textiles", "cement", "electricity", "kerosene", "agricultural_products"}
        rows = []
        for r in recs:
            if r.get("item") not in keep:
                continue
            label = r["item"]
            yr = dualyear_to_year(r.get("solar_year", ""))
            rows.append(base_row(r.get("country_iso3", "IRN"), yr, r.get("index_value", ""),
                                  r.get("unit", ""), slugify(label), label,
                                  "wb1960-table7-per-capita-consumption-index",
                                  original_period_label=r.get("solar_year", ""),
                                  notes=r.get("notes", "")))
        write_chart("pahlavi_hh__nonfood_consumption_index_1955_1958", rows)


group3_pahlavi_hh()

# ============================================================================
# GROUP 4: majlis__, banking_hist__, gfdd__ -- small, mostly-direct mappings.
# ============================================================================

def group4_majlis_banking_gfdd():
    d = os.path.join(PROC, "majlis_budget_law_series")

    if "majlis__supplementary_budget_additions" in missing:
        recs = load_csv(os.path.join(d, "supplementary_budget_additions.csv"))
        rows = []
        for r in recs:
            yr = dualyear_to_year(r.get("fiscal_year_ah", ""))
            label = r.get("item", "")
            rows.append(base_row(r.get("country_iso3", "IRN"), yr, r.get("amount_rials", ""),
                                  "rials", slugify(label), label, "majlis-historical-budget-laws",
                                  original_period_label=r.get("fiscal_year_ah", ""),
                                  notes=r.get("notes", "")))
        write_chart("majlis__supplementary_budget_additions", rows)

    if "majlis__forex_budget_law_1364" in missing:
        recs = load_csv(os.path.join(d, "forex_budget_law_1364.csv"))
        rows = []
        for r in recs:
            yr = dualyear_to_year(r.get("fiscal_year_ah", ""))
            label = r.get("item", "")
            rows.append(base_row(r.get("country_iso3", "IRN"), yr, r.get("amount", ""),
                                  r.get("unit", ""), slugify(label), label,
                                  "majlis-historical-budget-laws",
                                  original_period_label=r.get("fiscal_year_ah", ""),
                                  notes=r.get("notes", "")))
        write_chart("majlis__forex_budget_law_1364", rows)

    dbank = os.path.join(PROC, "iran_banking_history_series")

    if "banking_hist__nationalization_1979_events" in missing:
        recs = load_csv(os.path.join(dbank, "nationalization_1979_consolidation_events.csv"))
        rows = []
        for r in recs:
            yr = extract_year_from_date(r.get("event_date", ""))
            label = r.get("event_type", "")
            rows.append(base_row("IRN", yr, "", "", slugify(label), label,
                                  "iranica-banking-history+contemporaneous-press",
                                  original_period_label=r.get("event_date", ""),
                                  notes=f"{r.get('description','')} [entities: {r.get('entity_names','')}] "
                                        f"[source: {r.get('source','')}]"))
        write_chart("banking_hist__nationalization_1979_events", rows)

    if "banking_hist__private_bank_reentry_2000_2025" in missing:
        recs = load_csv(os.path.join(dbank, "private_bank_reentry_2000_2025.csv"))
        rows = []
        for r in recs:
            label = r.get("bank_name", "")
            ey = r.get("establishment_year", "")
            yr = int(ey) if re.match(r"^\d{4}$", ey or "") else ""
            rows.append(base_row("IRN", yr, "", "", slugify(label), label,
                                  "iran-banking-history",
                                  original_period_label=ey if yr == "" and ey else None,
                                  notes=f"{r.get('persian_name_transliteration','')}; license/ops date "
                                        f"{r.get('license_operations_date','')}; {r.get('notes','')} "
                                        f"[source: {r.get('source','')}]"))
        write_chart("banking_hist__private_bank_reentry_2000_2025", rows)

    if any(cid.startswith("gfdd__") for cid in missing):
        recs = load_csv(os.path.join(dbank, "worldbank_gfdd_banking_depth_1960_2016.csv"))
        by_ind = {}
        for r in recs:
            by_ind.setdefault(r["indicator_id"], []).append(r)
        for r in load_csv(REGISTRY):
            cid = r["chart_id"]
            if cid not in missing or not cid.startswith("gfdd__"):
                continue
            code = r["underlying_codes"].split("|")[-1]
            rows = []
            for rec in by_ind.get(code, []):
                rows.append(base_row(rec["country_iso3"], rec["year"], rec["value"], rec.get("unit", ""),
                                      code, rec.get("indicator_label", code), "worldbank-gfdd-via-fred"))
            write_chart(cid, rows)


group4_majlis_banking_gfdd()

# ============================================================================
# GROUP 5: Iran dams/water-infrastructure archival tables (5 chart_ids, several wide/mixed files).
# ============================================================================

def group5_dams():
    d = os.path.join(PROC, "iran_dams_water_infrastructure_series")

    if "dams_of_iran_technical_economic_specs_1971" in missing:
        recs = load_csv(os.path.join(d, "major_dams_specifications_1971.csv"))
        value_fields = ["height_from_foundation_m", "reservoir_capacity_million_m3",
                         "regulated_annual_capacity_million_m3",
                         "area_under_cultivation_final_phase_1000ha",
                         "cost_of_dam_million_rials", "cost_of_irrigation_million_rials"]
        rows = []
        for r in recs:
            id_label = " — ".join(str(r[f]).strip() for f in
                                   ["category", "dam_name", "common_or_modern_name", "river"] if r.get(f))
            yos = r.get("year_operation_started", "")
            yr = leading_year(yos)
            opl = yos if (yos and not yos.isdigit()) else None
            for vf in value_fields:
                if not r.get(vf):
                    continue
                label = f"{id_label} — {vf}"
                rows.append(base_row("IRN", yr, r[vf], "", slugify(label), label,
                                      "wb1975water-major-dams-specifications-1971",
                                      original_period_label=opl, notes=r.get("notes", "")))
        write_chart("dams_of_iran_technical_economic_specs_1971", rows)

    if "diversion_dams_of_iran_specifications_1937_1967" in missing:
        recs = load_csv(os.path.join(d, "diversion_dams_specifications_1937_1967.csv"))
        value_fields = ["overall_length_at_crest_m", "height_from_foundation_m",
                         "area_under_cultivation_ha"]
        rows = melt_wide(recs, ["dam_name", "location"], value_fields,
                          year_transform=lambda r: r.get("utilization_date", ""),
                          source_dataset="wb1975water-diversion-dams-specifications")
        write_chart("diversion_dams_of_iran_specifications_1937_1967", rows)

    if "iran_reservoir_water_control_forecast_by_zone" in missing:
        recs = load_csv(os.path.join(d, "reservoir_water_control_forecast_4th_5th_plan.csv"))
        value_fields = [k for k in recs[0].keys() if k != "zone"] if recs else []
        rows = melt_wide(recs, ["zone"], value_fields, static_year="",
                          unit_map={vf: "million m3" for vf in value_fields},
                          source_dataset="wb1975water-reservoir-water-control-forecast-by-zone")
        for r in rows:
            r["original_period_label"] = "4th-5th Development Plan forecast (no single year; plan-period aggregate)"
        write_chart("iran_reservoir_water_control_forecast_by_zone", rows)

    if "dez_dam_project_economics_1960" in missing:
        rows = []
        params = load_csv(os.path.join(d, "dez_dam_key_parameters_1960_appraisal.csv"))
        for r in params:
            label = r.get("parameter", "")
            rows.append(base_row("IRN", 1960, r.get("value", ""), r.get("unit", ""), slugify(label),
                                  label, "wb1960dez-project-key-parameters", notes=r.get("notes", "")))
        cost = load_csv(os.path.join(d, "dez_dam_cost_estimate_by_component_1960.csv"))
        cost_fields = ["foreign_currency_million_rials", "local_currency_million_rials",
                       "total_million_rials", "total_million_usd"]
        rows += melt_wide(cost, ["section", "line_item"], cost_fields, static_year=1960,
                           unit_map={"foreign_currency_million_rials": "million rials",
                                     "local_currency_million_rials": "million rials",
                                     "total_million_rials": "million rials",
                                     "total_million_usd": "million USD"},
                           source_dataset="wb1960dez-project-cost-estimate-by-component",
                           notes_field="notes")
        write_chart("dez_dam_project_economics_1960", rows)

    if "ghazvin_project_economics_appraisal_vs_actual_1967_1978" in missing:
        rows = []
        appraisal = load_csv(os.path.join(d, "ghazvin_project_appraisal_cost_parameters_1967.csv"))
        appraisal_fields = ["local_currency_usd_million", "foreign_exchange_usd_million", "total_usd_million"]
        rows += melt_wide(appraisal, ["category", "item"], appraisal_fields, static_year=1967,
                           unit_map={f: "million USD" for f in appraisal_fields},
                           source_dataset="wb1967ghazvin-project-cost-and-parameters",
                           notes_field="notes")
        audit = load_csv(os.path.join(d, "ghazvin_project_completion_audit_1978.csv"))
        for r in audit:
            for vf in ("original_plan", "actual_or_revised"):
                text = r.get(vf, "")
                if not text:
                    continue
                num = first_number(text)
                label = f"{r['metric']} — {vf}"
                rows.append(base_row("IRN", 1978, num if num is not None else "", "", slugify(label),
                                      label, "wb1978ghazvin-project-completion-audit",
                                      notes=f"{text} | {r.get('notes','')}"))
        write_chart("ghazvin_project_economics_appraisal_vs_actual_1967_1978", rows)


group5_dams()

log(f"After groups 3-5: built={STATS['built']} skipped={STATS['skipped']} rows={STATS['rows_total']}")

# ============================================================================
# GROUP 6: Iran mining (USGS Minerals Yearbook Iran series, IMIDRO, and Pahlavi-era industrial
# production) -- commodity-filtered charts sharing 2 source files, plus a few one-off IMIDRO ones.
# ============================================================================

def usgs_commodity_rows(recs, pred):
    rows = []
    for r in recs:
        if not pred(r.get("commodity", "")):
            continue
        label = r["commodity"]
        rows.append(base_row("IRN", r.get("year", ""), r.get("value", ""), r.get("unit", ""),
                              slugify(label), label,
                              f"usgs-minerals-yearbook:{r.get('source_yearbook_edition','')}",
                              notes=f"flag={r.get('flag','')}" if r.get("flag") else None))
    return rows


def pahlavi_industry_commodity_rows(recs, pred):
    rows = []
    for r in recs:
        if not pred(r.get("commodity", "")):
            continue
        label = r["commodity"]
        yr = dualyear_to_year(r.get("fiscal_year", ""))
        rows.append(base_row("IRN", yr, r.get("value", ""), r.get("unit", ""), slugify(label), label,
                              "wb1960-industrial-production-1954-1959",
                              original_period_label=r.get("fiscal_year", "")))
    return rows


def group6_mining():
    dm = os.path.join(PROC, "iran_mining_series")
    dpi = os.path.join(PROC, "pahlavi_industry_series")
    usgs = load_csv(os.path.join(dm, "usgs_iran_mineral_production_1961_1980.csv"))
    pahlavi_ind = load_csv(os.path.join(dpi, "industrial_production_1954_1959.csv"))

    EXACT = {
        "iran_chromite_production_1961_1980": "Chromite (gross weight)",
        "iran_pig_iron_production_1973_1980": "Pig iron",
        "iran_crude_steel_production_1973_1980": "Steel, crude",
        "iran_barite_production_1961_1980": "Barite",
        "iran_gypsum_production_1968_1980": "Gypsum",
        "iran_salt_production_1961_1980": "Salt (rock)",
        "iran_coal_production_1961_1980": "Coal",
        "iran_coke_production_1961_1980": "Coke",
    }
    for cid, commodity in EXACT.items():
        if cid in missing:
            write_chart(cid, usgs_commodity_rows(usgs, lambda c, x=commodity: c == x))

    CONTAINS = {
        "iran_copper_production_by_stage_1961_1980": "copper",
        "iran_iron_ore_production_1961_1980": "iron ore",
        "iran_aluminum_production_1973_1980": "aluminum",
        "iran_lead_production_by_stage_1961_1980": "lead",
        "iran_manganese_ore_production_1961_1980": "manganese",
        "iran_zinc_production_1961_1980": "zinc",
        "iran_sulfur_production_1961_1980": "sulfur",
    }
    for cid, needle in CONTAINS.items():
        if cid in missing:
            write_chart(cid, usgs_commodity_rows(usgs, lambda c, n=needle: n in c.lower()))

    if "iran_cement_production_1954_1980" in missing:
        rows = pahlavi_industry_commodity_rows(pahlavi_ind, lambda c: c == "Cement")
        rows += usgs_commodity_rows(usgs, lambda c: c == "Cement, hydraulic")
        write_chart("iran_cement_production_1954_1980", rows)

    if "iran_processed_tea_output_pahlavi_era" in missing:
        write_chart("iran_processed_tea_output_pahlavi_era",
                    pahlavi_industry_commodity_rows(pahlavi_ind, lambda c: c == "Tea"))

    if "iran_processed_sugar_output_pahlavi_era" in missing:
        write_chart("iran_processed_sugar_output_pahlavi_era",
                    pahlavi_industry_commodity_rows(pahlavi_ind, lambda c: c == "Sugar"))

    if "iran_textile_cloth_output_by_fiber_1954_1959" in missing:
        fibers = {"Cotton cloth", "Woolen cloth", "Jute cloth", "Silk cloth"}
        write_chart("iran_textile_cloth_output_by_fiber_1954_1959",
                    pahlavi_industry_commodity_rows(pahlavi_ind, lambda c: c in fibers))

    if "iran_cigarette_production_1954_1959" in missing:
        write_chart("iran_cigarette_production_1954_1959",
                    pahlavi_industry_commodity_rows(pahlavi_ind, lambda c: c == "Cigarettes"))

    if "iran_misc_light_manufacturing_output_1954_1959" in missing:
        misc = {"Matches", "Soap", "Rubber shoes", "Glass", "Soft drinks"}
        write_chart("iran_misc_light_manufacturing_output_1954_1959",
                    pahlavi_industry_commodity_rows(pahlavi_ind, lambda c: c in misc))

    if "iran_sar_cheshmeh_copper_project_narrative_1965_2022" in missing:
        narrative = load_csv(os.path.join(dm, "usgs_iran_commodity_narrative_highlights_1965_1980.csv"))
        rows = []
        for r in narrative:
            blob = (r.get("topic", "") + " " + r.get("narrative_summary", "")).lower()
            if "sar cheshmeh" not in blob:
                continue
            label = r["topic"]
            rows.append(base_row("IRN", r.get("report_year_context", ""), "", "", slugify(label), label,
                                  f"usgs-minerals-yearbook:{r.get('source_yearbook_edition','')}",
                                  notes=r.get("narrative_summary", "")))
        snap = load_csv(os.path.join(dm, "imidro_sarcheshmeh_monthly_production_snapshot_2021_22.csv"))
        value_fields = ["month_value_current", "month_value_prior", "ytd_value_current", "ytd_value_prior"]
        pct_fields = ["month_pct_change", "ytd_pct_change"]
        for r in snap:
            unit = r.get("unit", "")
            for vf in value_fields:
                if not r.get(vf):
                    continue
                label = f"{r['product_stage']} — {r['site']} — {vf}"
                rows.append(base_row("IRN", "", r[vf], unit, slugify(label), label,
                                      "imidro-iran:annual-report-2021-22-extraction",
                                      original_period_label="2021/22 (monthly bulletin, exact month not captured)",
                                      notes=r.get("notes", "")))
            for vf in pct_fields:
                if not r.get(vf):
                    continue
                label = f"{r['product_stage']} — {r['site']} — {vf}"
                rows.append(base_row("IRN", "", r[vf], "percent", slugify(label), label,
                                      "imidro-iran:annual-report-2021-22-extraction",
                                      original_period_label="2021/22 (monthly bulletin, exact month not captured)"))
        write_chart("iran_sar_cheshmeh_copper_project_narrative_1965_2022", rows)

    if "iran_new_mineral_reserves_valuation_2014_2021" in missing:
        recs = load_csv(os.path.join(dm, "imidro_new_mineral_reserves_value_2014_2021.csv"))
        value_fields = {"new_reserves_quantity": None, "unit_price_usd": "USD",
                         "price_percentage": "percent", "total_value_usd": "USD"}
        rows = []
        for r in recs:
            for vf, unit in value_fields.items():
                if not r.get(vf):
                    continue
                u = unit if unit else r.get("unit", "")
                label = f"{r['mineral']} — {vf}"
                rows.append(base_row("IRN", "", r[vf], u, slugify(label), label,
                                      "imidro-iran:annual-report-2021-22-extraction",
                                      original_period_label="2014-2021 (cumulative new reserves period)"))
        write_chart("iran_new_mineral_reserves_valuation_2014_2021", rows)

    if "iran_mining_capacity_growth_since_2002" in missing:
        recs = load_csv(os.path.join(dm, "imidro_capacity_growth_since_2002.csv"))
        rows = []
        for r in recs:
            label = r["metric"]
            unit = r.get("unit", "")
            rows.append(base_row("IRN", dualyear_to_year("2002/03"), r.get("value_at_imidro_founding_2002_03", ""),
                                  unit, slugify(label) + ".founding_2002_03", label + " (at IMIDRO founding)",
                                  "imidro-iran:annual-report-2021-22-extraction",
                                  original_period_label="2002/03"))
            rows.append(base_row("IRN", dualyear_to_year("2021/22"), r.get("value_2021_22", ""),
                                  unit, slugify(label) + ".fy2021_22", label + " (FY2021/22)",
                                  "imidro-iran:annual-report-2021-22-extraction",
                                  original_period_label="2021/22"))
        write_chart("iran_mining_capacity_growth_since_2002", rows)

    if "iran_imidro__production_performance_2011_2015" in missing:
        recs = load_csv(os.path.join(dm, "imidro_production_performance_2011_2015.csv"))
        rows = []
        for r in recs:
            label = f"{r['product']} — {r['metric_type']}"
            rows.append(base_row("IRN", dualyear_to_year(r.get("fiscal_year_iranian", "")),
                                  r.get("value_thousand_tons", ""), "thousand tons", slugify(label), label,
                                  f"imidro-iran:{r.get('source_report','')}",
                                  original_period_label=r.get("fiscal_year_iranian", "")))
        write_chart("iran_imidro__production_performance_2011_2015", rows)

    if "iran_imidro__sales_export_by_group_2011_2015" in missing:
        recs = load_csv(os.path.join(dm, "imidro_sales_export_by_group_2011_2015.csv"))
        rows = []
        for r in recs:
            label_q = f"{r['metric']} — {r['group']} — quantity"
            fy = r.get("fiscal_year_iranian", "")
            if r.get("quantity_thousand_tons"):
                rows.append(base_row("IRN", dualyear_to_year(fy), r["quantity_thousand_tons"],
                                      "thousand tons", slugify(label_q), label_q,
                                      f"imidro-iran:{r.get('source_report','')}", original_period_label=fy))
            if r.get("value"):
                label_v = f"{r['metric']} — {r['group']} — value"
                rows.append(base_row("IRN", dualyear_to_year(fy), r["value"], r.get("value_unit", ""),
                                      slugify(label_v), label_v, f"imidro-iran:{r.get('source_report','')}",
                                      original_period_label=fy))
        write_chart("iran_imidro__sales_export_by_group_2011_2015", rows)


group6_mining()

log(f"After group 6: built={STATS['built']} skipped={STATS['skipped']} rows={STATS['rows_total']}")

# ============================================================================
# GROUP 7: remaining pahlavi_industry_series / automotive-textile singles.
# ============================================================================

def group7_industry_singles():
    dpi = os.path.join(PROC, "pahlavi_industry_series")

    if "iran_industry_import_dependence_1970" in missing:
        recs = load_csv(os.path.join(dpi, "industry_import_dependence_1970.csv"))
        rows = []
        for r in recs:
            label = f"{r['category']} — {r['product']}"
            note = r.get("notes", "")
            if r.get("footnote_b_planned_project_under_construction"):
                note = (note + " " if note else "") + \
                    f"[{r['footnote_b_planned_project_under_construction']}]"
            rows.append(base_row("IRN", 1970, r.get("share_of_imported_inputs_in_sales_value_pct", ""),
                                  "percent", slugify(label), label, "wb1970-industry-import-dependence",
                                  notes=note))
        write_chart("iran_industry_import_dependence_1970", rows)

    if "iran_isfahan_steel_mill_idro_capital_goods_narrative_1972" in missing:
        recs = load_csv(os.path.join(dpi, "isfahan_steel_idro_capital_goods_1972.csv"))
        rows = []
        for r in recs:
            label = f"{r['topic']} — {r['item']}"
            rows.append(base_row("IRN", 1972, "", "", slugify(label), label,
                                  "wb1972industrial-isfahan-steel-and-idro-capital-goods",
                                  notes=r.get("detail", "")))
        write_chart("iran_isfahan_steel_mill_idro_capital_goods_narrative_1972", rows)

    if "iran_gasoline_consumption_1955_1972" in missing:
        rows = []
        g1 = load_csv(os.path.join(dpi, "gasoline_consumption_1955_1962.csv"))
        for r in g1:
            yr = dualyear_to_year(r.get("year", ""))
            rows.append(base_row("IRN", yr, r.get("gasoline_consumption_million_liters", ""),
                                  "million liters", "gasoline_consumption", "Gasoline consumption",
                                  "wb1962-gasoline-consumption-1955-1962",
                                  original_period_label=r.get("year", ""), notes=r.get("note", "")))
        g2 = load_csv(os.path.join(dpi, "vehicle_registration_gasoline_1962_1972.csv"))
        for r in g2:
            if r.get("metric") != "gasoline_consumption":
                continue
            rows.append(base_row("IRN", r.get("year", ""), r.get("value", ""), r.get("unit", ""),
                                  "gasoline_consumption", "Gasoline consumption",
                                  "pahlavi-era-primary-extraction:vehicle-registration-gasoline-1962-1972",
                                  notes=r.get("note", "")))
        write_chart("iran_gasoline_consumption_1955_1972", rows)

    if "iran_railways_income_expense_1953_1961" in missing:
        recs = load_csv(os.path.join(dpi, "railways_income_expense_1953_1961.csv"))
        value_fields = ["gross_revenues_million_rls", "working_expenses_million_rls",
                         "balance_before_depreciation_million_rls"]
        rows = []
        for r in recs:
            opl = r.get("year", "")
            yr = dualyear_to_year(opl)
            for vf in value_fields:
                if not r.get(vf):
                    continue
                label = vf.replace("_million_rls", "").replace("_", " ")
                rows.append(base_row("IRN", yr, r[vf], "million rials", slugify(label), label,
                                      "wb1962-railways-income-expense-1953-1961",
                                      original_period_label=opl))
        write_chart("iran_railways_income_expense_1953_1961", rows)

    if "iran_vehicle_registration_by_type_1955_1972" in missing:
        rows = []
        v1 = load_csv(os.path.join(dpi, "road_vehicle_registration_1955_56_vs_1960_61.csv"))
        for r in v1:
            for period, vf in [("1955/56", "registered_1955_56"), ("1960/61", "registered_1960_61")]:
                if not r.get(vf):
                    continue
                label = r["vehicle_type"]
                rows.append(base_row("IRN", dualyear_to_year(period), r[vf], "count", slugify(label),
                                      label, "wb1962-road-vehicle-registration-1955-1961",
                                      original_period_label=period))
        v2 = load_csv(os.path.join(dpi, "vehicle_registration_gasoline_1962_1972.csv"))
        for r in v2:
            if r.get("metric") == "gasoline_consumption":
                continue
            label = r["metric"].replace("_", " ")
            rows.append(base_row("IRN", r.get("year", ""), r.get("value", ""), r.get("unit", ""),
                                  slugify(label), label,
                                  "pahlavi-era-primary-extraction:vehicle-registration-gasoline-1962-1972",
                                  notes=r.get("note", "")))
        write_chart("iran_vehicle_registration_by_type_1955_1972", rows)

    dat = os.path.join(PROC, "iran_automotive_textile_series")

    if "iran_automotive_national_vehicle_production_1970_2018" in missing:
        recs = load_csv(os.path.join(dat, "automotive_paykan_national_production_1967_2018.csv"))
        rows = []
        for r in recs:
            if not r.get("national_vehicle_production_units"):
                continue
            rows.append(base_row("IRN", r.get("year", ""), r["national_vehicle_production_units"],
                                  "vehicles/year", "national_vehicle_production", "National vehicle production",
                                  "iran-automotive-industry:khodro-paykan-production-history",
                                  notes=f"{r.get('notes','')} [source: {r.get('source','')}]"))
        write_chart("iran_automotive_national_vehicle_production_1970_2018", rows)

    if "iran_textile_sector_capacity_employment_1923_2002" in missing:
        recs = load_csv(os.path.join(dat, "textile_sector_pahlavi_to_2002.csv"))
        rows = []
        for r in recs:
            if not r.get("value"):
                continue
            label = r["metric"]
            rows.append(base_row("IRN", extract_year_from_date(r.get("year", "")), r["value"],
                                  r.get("unit", ""), slugify(label), label,
                                  "iran-textile-industry:pahlavi-era-textile-sector-overview",
                                  original_period_label=r.get("year", ""), notes=r.get("notes", "")))
        write_chart("iran_textile_sector_capacity_employment_1923_2002", rows)


group7_industry_singles()

log(f"After group 7: built={STATS['built']} skipped={STATS['skipped']} rows={STATS['rows_total']}")

# ============================================================================
# GROUP 8: iran_insurance__ (Bimeh Markazi Iran) -- 6 files, all year_sh + several numeric metric
# columns ("edition" = which BMI annual-report edition the row was extracted from).
# ============================================================================

def group8_insurance():
    d = os.path.join(PROC, "iran_insurance_series")

    def sh_year(r):
        return sh_to_gregorian(r.get("year_sh", ""))

    jobs = [
        ("iran_insurance__market_earned_premium_incurred_loss_1379_1391",
         "market_earned_premium_incurred_loss_1379_1391.csv", [],
         ["earned_premium_million_irr", "incurred_loss_million_irr", "loss_ratio_pct"]),
        ("iran_insurance__market_direct_premium_1379_1384",
         "market_direct_premium_1379_1384.csv", [],
         ["direct_premium_million_irr", "growth_rate_pct"]),
        ("iran_insurance__premium_loss_by_class_1383_1389",
         "market_premium_loss_by_insurance_class.csv", ["class_label"],
         ["earned_premium_million_irr", "incurred_loss_million_irr", "loss_ratio_pct"]),
        ("iran_insurance__sales_network_1382_1391",
         "sales_network_by_year.csv", [],
         ["number_of_companies", "number_of_branches", "number_of_brokers", "number_of_agents",
          "number_of_life_insurance_agents", "number_of_loss_adjusters", "number_of_policies",
          "number_of_claims"]),
        ("iran_insurance__companies_by_ownership_1385_1391",
         "companies_by_ownership_type.csv", [],
         ["state_owned_companies", "private_companies", "state_owned_employees", "private_employees",
          "number_of_branches", "number_of_agents", "number_of_life_insurance_agents",
          "number_of_brokers", "number_of_loss_adjusters"]),
        ("iran_insurance__bmi_own_financial_highlights_1386_1391",
         "bmi_own_financial_highlights.csv", [],
         ["gross_premium_million_irr", "retained_premium_million_irr", "retained_pct_of_gross",
          "earned_premium_million_irr", "incurred_loss_million_irr", "incurred_loss_pct_of_earned",
          "net_claim_million_irr", "net_claim_pct_of_retained", "investment_and_other_income_million_irr",
          "general_expenses_million_irr", "general_expenses_pct_of_retained", "profit_loss_million_irr",
          "total_assets_million_irr", "shareholders_equity_million_irr", "technical_reserve_million_irr",
          "unexpired_risks_million_irr", "outstanding_loss_million_irr", "catastrophic_risk_reserve_million_irr"]),
    ]
    for cid, fn, id_fields, value_fields in jobs:
        if cid not in missing:
            continue
        recs = load_csv(os.path.join(d, fn))
        # (not using melt_wide directly here so each row can carry its own original_period_label
        # and edition-specific source_dataset)
        out = []
        for r in recs:
            yr = sh_year(r)
            id_label = " — ".join(str(r[f]).strip() for f in id_fields if r.get(f))
            for vf in value_fields:
                if not r.get(vf):
                    continue
                label = f"{id_label} — {vf}" if id_label else vf
                out.append(base_row("IRN", yr, r[vf], "", slugify(label), label,
                                     f"bimeh-markazi-iran:{r.get('edition','')}",
                                     original_period_label=r.get("year_sh", "")))
        write_chart(cid, out)


group8_insurance()

# ============================================================================
# GROUP 9: iran_provincial__ (SCI provincial standing indicators, jaygah series) -- 6 files,
# already long format (province,indicator,year_sh,value,unit[,...]).
# ============================================================================

def group9_provincial():
    d = os.path.join(PROC, "iran_provincial_indicators_series")
    jobs = [
        ("iran_provincial__gdp_per_capita_excl_oil_1393_1397",
         "gdp_per_capita_excl_oil_by_province_1393_1397.csv", "metric", None),
        ("iran_provincial__government_budget_execution_1397_1401",
         "government_budget_execution_share_by_province.csv", "indicator", "unit"),
        ("iran_provincial__financial_markets_insurance_1397_1401",
         "financial_markets_insurance_by_province.csv", "indicator", "unit"),
        ("iran_provincial__industry_workshops_1396_1400",
         "industry_workshops_by_province.csv", "indicator", "unit"),
        ("iran_provincial__mining_production_value_1397_1401",
         "mining_production_value_share_by_province.csv", "indicator", "unit"),
        ("iran_provincial__foreign_investment_1398_1400",
         "foreign_investment_by_province.csv", "indicator", "unit"),
    ]
    for cid, fn, ind_field, unit_field in jobs:
        if cid not in missing:
            continue
        recs = load_csv(os.path.join(d, fn))
        rows = []
        for r in recs:
            if not r.get("value"):
                continue
            label = f"{r[ind_field]} — {r['province']}"
            unit = r.get(unit_field, "") if unit_field else ""
            val = r["value"]
            # a handful of rows in this SCI source use Persian-style slash-decimal notation
            # (e.g. "100/00" meaning 100.00, not a fraction/date) -- normalize to a parseable
            # decimal point; same numeric magnitude, not a fabrication.
            if re.match(r"^-?\d+/\d+$", val):
                val = val.replace("/", ".")
            rows.append(base_row("IRN", sh_to_gregorian(r.get("year_sh", "")), val, unit,
                                  slugify(label), label,
                                  f"sci-provincial-standing-indicators:{r.get('edition','jaygah')}",
                                  original_period_label=r.get("year_sh", "")))
        write_chart(cid, rows)


group9_provincial()

# ============================================================================
# GROUP 10: iran_energy__ (Iran Data Portal energy series) -- 4 files, year_sh + Persian labels.
# ============================================================================

def group10_energy():
    d = os.path.join(PROC, "iran_energy_data_portal_series")

    if "iran_energy__national_balance_1386_1394" in missing:
        recs = load_csv(os.path.join(d, "national_energy_balance_1386_1394.csv"))
        rows = []
        for r in recs:
            if not r.get("value_million_boe"):
                continue
            label = f"{r['row_category']} — {r['fuel_type']}"
            rows.append(base_row("IRN", sh_to_gregorian(r.get("year_sh", "")), r["value_million_boe"],
                                  "million BOE", slugify(label), label, "iran-data-portal",
                                  original_period_label=r.get("year_sh", ""), notes=r.get("note", "")))
        write_chart("iran_energy__national_balance_1386_1394", rows)

    if "iran_energy__natural_gas_consumption_1370_1385" in missing:
        recs = load_csv(os.path.join(d, "natural_gas_consumption_1370_1385.csv"))
        rows = []
        for r in recs:
            label = r["category_fa"]
            rows.append(base_row("IRN", sh_to_gregorian(r.get("year_sh", "")), r.get("value_mln_cu_m", ""),
                                  "million cubic meters", slugify(label), label, "iran-data-portal",
                                  original_period_label=r.get("year_sh", "")))
        write_chart("iran_energy__natural_gas_consumption_1370_1385", rows)

    if "iran_energy__oil_products_imports_1370_1385" in missing:
        recs = load_csv(os.path.join(d, "oil_products_imports_1370_1385.csv"))
        rows = []
        for r in recs:
            label = r["product_fa"]
            rows.append(base_row("IRN", sh_to_gregorian(r.get("year_sh", "")), r.get("value_mln_liters", ""),
                                  "million liters", slugify(label), label, "iran-data-portal",
                                  original_period_label=r.get("year_sh", ""), notes=r.get("note", "")))
        write_chart("iran_energy__oil_products_imports_1370_1385", rows)

    if "iran_energy__npc_petrochemical_production_1375_1385" in missing:
        recs = load_csv(os.path.join(d, "npc_petrochemical_production_1375_1385.csv"))
        rows = []
        for r in recs:
            label = r["category_fa"]
            rows.append(base_row("IRN", sh_to_gregorian(r.get("year_sh", "")), r.get("value_1000_tons", ""),
                                  "1000 tons", slugify(label), label, "iran-data-portal",
                                  original_period_label=r.get("year_sh", ""), notes=r.get("note", "")))
        write_chart("iran_energy__npc_petrochemical_production_1375_1385", rows)


group10_energy()

# ============================================================================
# GROUP 11: iran_ports__ tariff schedules (3 files, all a fixed-year-2024 snapshot).
# ============================================================================

def group11_ports():
    d = os.path.join(PROC, "iran_ports_tariff_series")

    if "iran_ports__thc_container_handling_2024" in missing:
        recs = load_csv(os.path.join(d, "thc_container_handling_charges_2024.csv"))
        rows = []
        for r in recs:
            label = f"{r['container_size']} — {r['cargo_status']}"
            rows.append(base_row("IRN", 2024, r.get("terminal_handling_charge", ""), r.get("unit", ""),
                                  slugify(label), label, "iran-ports-maritime-org:thc-tariff-2024"))
        write_chart("iran_ports__thc_container_handling_2024", rows)

    if "iran_ports__ship_port_dues_2024" in missing:
        recs = load_csv(os.path.join(d, "ship_port_dues_2024.csv"))
        rows = []
        for r in recs:
            label = f"{r['tariff_item']} — {r['ship_type']}"
            rows.append(base_row("IRN", 2024, r.get("rate", ""), r.get("unit", ""), slugify(label),
                                  label, "iran-ports-maritime-org:port-dues-tariff-2024"))
        write_chart("iran_ports__ship_port_dues_2024", rows)

    if "iran_ports__container_storage_charges_2024" in missing:
        recs = load_csv(os.path.join(d, "container_storage_charges_2024.csv"))
        rows = []
        for r in recs:
            label = f"{r['container_size']} — {r['status']} — days {r['storage_period_days']}"
            rows.append(base_row("IRN", 2024, r.get("charge_rial", ""), "rial", slugify(label), label,
                                  "iran-ports-maritime-org:storage-tariff-2024"))
        write_chart("iran_ports__container_storage_charges_2024", rows)


group11_ports()

log(f"After groups 8-11: built={STATS['built']} skipped={STATS['skipped']} rows={STATS['rows_total']}")

# ============================================================================
# GROUP 12: iranplanbudgetorg__ (Five-Year Development Plan targets, split 3 ways by category).
# ============================================================================

def group12_plan_budget():
    d = os.path.join(PROC, "iran_plan_budget_org_series")
    recs = load_csv(os.path.join(d, "five_year_plan_targets.csv"))
    SPLIT = {
        "iranplanbudgetorg__five_year_plan_gdp_growth_targets": {"macro"},
        "iranplanbudgetorg__five_year_plan_sectoral_growth_targets": {"sectoral_value_added", "sectoral_employment"},
        "iranplanbudgetorg__five_year_plan_investment_ceilings": {"investment", "credit", "spending"},
    }
    value_fields = ["base_value", "interim_value", "final_value", "avg_annual_growth_pct"]
    for cid, cats in SPLIT.items():
        if cid not in missing:
            continue
        rows = []
        for r in recs:
            if r.get("category") not in cats:
                continue
            for vf in value_fields:
                if not r.get(vf):
                    continue
                label = f"Plan {r['plan_number']} — {r['indicator']} — {vf}"
                note = r.get("notes", "")
                extra = f"[{r.get('value_type','')}, source: {r.get('source_file','')} {r.get('source_page','')}]"
                rows.append(base_row("IRN", "", r[vf], r.get("unit", ""), slugify(label), label,
                                      "iran-plan-budget-org:five-year-plan-law-texts",
                                      original_period_label=r.get("plan_years_ce", ""),
                                      notes=(note + " " + extra).strip()))
        write_chart(cid, rows)


group12_plan_budget()

# ============================================================================
# GROUP 13: iran_pmi__, iran_bizenv__, iran_mimt__, iran_unido_cip__ (ICCIMA / MIMT industry data).
# ============================================================================

def group13_pmi_industry():
    dp = os.path.join(PROC, "iran_iccima_pmi_series")

    if "iran_pmi__whole_economy_fy1403" in missing or "iran_pmi__sectoral_fy1403" in missing:
        recs = load_csv(os.path.join(dp, "pmi_yearbook_fy1403_by_sector.csv"))
        for cid, pred in [("iran_pmi__whole_economy_fy1403", lambda st: "Whole Economy" in st),
                           ("iran_pmi__sectoral_fy1403", lambda st: "Whole Economy" not in st)]:
            if cid not in missing:
                continue
            rows = []
            for r in recs:
                if not pred(r.get("sector_table", "")):
                    continue
                sector = re.sub(r"^\s*3-\d+-?\s*", "", r["sector_table"]).strip()
                yr = extract_year_from_date(r.get("month_western", ""))
                label = sector
                rows.append(base_row("IRN", yr, r.get("value", ""), "PMI index", slugify(label), label,
                                      "iccima-iran:pmi-yearbook-fy1403",
                                      original_period_label=f"{r.get('month_fa','')} ({r.get('month_western','')})"))
            write_chart(cid, rows)

    if "iran_bizenv__national_index_1398_1404" in missing:
        recs = load_csv(os.path.join(dp, "business_environment_national_index.csv"))
        rows = []
        for r in recs:
            yr = sh_to_gregorian(r.get("period_sh", ""))
            label = "National Business Environment Index"
            rows.append(base_row("IRN", yr, r.get("national_business_environment_index", ""), "index",
                                  slugify(label), label, "iccima-iran:business-environment-index",
                                  original_period_label=r.get("period_sh", ""),
                                  notes=f"frequency={r.get('frequency','')}"))
        write_chart("iran_bizenv__national_index_1398_1404", rows)

    dmimt = os.path.join(PROC, "iran_industry_ministry_series")

    if "iran_mimt__daily_bulletin_panel_1399" in missing:
        recs = load_csv(os.path.join(dmimt, "mimt_daily_bulletin_panel_1399.csv"))
        value_fields = [k for k in recs[0].keys() if k not in ("date_sh", "date_western", "source_report_id")] if recs else []
        rows = []
        for r in recs:
            yr = extract_year_from_date(r.get("date_western", ""))
            for vf in value_fields:
                if r.get(vf) in (None, ""):
                    continue
                label = vf.replace("_", " ")
                rows.append(base_row("IRN", yr, r[vf], "", slugify(label), label,
                                      f"mimt-iran:daily-bulletin-{r.get('source_report_id','')}",
                                      original_period_label=r.get("date_sh", "")))
        write_chart("iran_mimt__daily_bulletin_panel_1399", rows)

    if "iran_unido_cip__iran_subindicators_2010_2014" in missing:
        recs = load_csv(os.path.join(dmimt, "unido_cip_iran_subindicators_2010_2014.csv"))
        rows = []
        for r in recs:
            label = r["indicator"]
            rows.append(base_row("IRN", r.get("year", ""), r.get("value", ""), "", slugify(label), label,
                                  "mimt-iran:unido-cip"))
        write_chart("iran_unido_cip__iran_subindicators_2010_2014", rows)

    if "iran_unido_cip__regional_comparison_2010_2014" in missing:
        recs = load_csv(os.path.join(dmimt, "unido_cip_regional_comparison_2010_2014.csv"))
        NAME_TO_ISO3 = {
            "Bahrain": "BHR", "Egypt": "EGY", "Iran": "IRN", "Israel": "ISR", "Kazakhstan": "KAZ",
            "Kuwait": "KWT", "Oman": "OMN", "Qatar": "QAT", "Saudi Arabia": "SAU", "Turkey": "TUR",
            "United Arab Emirates": "ARE",
        }
        rows = []
        for r in recs:
            iso3 = NAME_TO_ISO3.get(r.get("country_common_name", ""), "")
            if not iso3:
                continue
            for vf, unit in [("cip_rank", "rank"), ("cip_score", "index")]:
                if not r.get(vf):
                    continue
                label = f"CIP {vf}"
                row = base_row(iso3, r.get("year", ""), r[vf], unit, slugify(label), label, "mimt-iran:unido-cip")
                row["country_name"] = r.get("country_common_name", cname(iso3))
                rows.append(row)
        write_chart("iran_unido_cip__regional_comparison_2010_2014", rows)


group13_pmi_industry()

# ============================================================================
# GROUP 14: iran_sci1399__ (SCI Iran Statistical Yearbook 1399) -- 5 files.
# ============================================================================

def group14_sci1399():
    d = os.path.join(PROC, "sci_yearbook_1399_series")

    if "iran_sci1399__labor_force_indicators_1380_1399" in missing:
        recs = load_csv(os.path.join(d, "labor_force_indicators_1380_1399.csv"))
        value_fields = ["economic_participation_rate_pct", "unemployment_rate_pct",
                         "unemployment_rate_15_24_pct", "unemployment_rate_15_29_pct",
                         "underemployment_share_pct", "employment_share_agriculture_pct",
                         "employment_share_manufacturing_pct", "employment_share_services_pct"]
        rows = []
        for r in recs:
            for vf in value_fields:
                if not r.get(vf):
                    continue
                label = f"{r['area']} — {r['sex']} — {vf}"
                rows.append(base_row("IRN", r.get("gregorian_year_approx", ""), r[vf], "percent",
                                      slugify(label), label, "sci-amar:statistical-yearbook-1399",
                                      original_period_label=r.get("solar_year", ""),
                                      notes=r.get("notes", "")))
        write_chart("iran_sci1399__labor_force_indicators_1380_1399", rows)

    if "iran_sci1399__government_budget_summary_1385_1400" in missing:
        recs = load_csv(os.path.join(d, "government_budget_summary_1385_1400.csv"))
        rows = []
        for r in recs:
            label = r["budget_line"]
            rows.append(base_row("IRN", r.get("gregorian_year_approx", ""), r.get("value_bln_rials", ""),
                                  "billion rials", slugify(label), label,
                                  "sci-amar:statistical-yearbook-1399",
                                  original_period_label=r.get("solar_year", ""), notes=r.get("notes", "")))
        write_chart("iran_sci1399__government_budget_summary_1385_1400", rows)

    if "iran_sci1399__cpi_by_coicop_group_1390_1399" in missing:
        recs = load_csv(os.path.join(d, "cpi_by_group_1390_1399.csv"))
        value_fields = ["cpi_index_1395_100", "pct_change_1399_vs_1398", "weight_pct_of_1395_basket"]
        units = {"cpi_index_1395_100": "index, 1395=100", "pct_change_1399_vs_1398": "percent",
                 "weight_pct_of_1395_basket": "percent of 1395 basket"}
        rows = []
        for r in recs:
            for vf in value_fields:
                if not r.get(vf):
                    continue
                label = f"{r['group']} — {vf}"
                rows.append(base_row("IRN", r.get("gregorian_year_approx", ""), r[vf], units[vf],
                                      slugify(label), label, "sci-amar:statistical-yearbook-1399",
                                      original_period_label=r.get("solar_year", "")))
        write_chart("iran_sci1399__cpi_by_coicop_group_1390_1399", rows)

    for cid, fn in [("iran_sci1399__gdp_value_added_by_sector_1390_1397", "gdp_value_added_by_sector_1390_1397.csv"),
                    ("iran_sci1399__gdp_by_expenditure_component_1390_1397", "gdp_by_expenditure_1390_1397.csv")]:
        if cid not in missing:
            continue
        recs = load_csv(os.path.join(d, fn))
        rows = []
        for r in recs:
            label = f"{r['line_item']} — {r['price_basis']}"
            rows.append(base_row("IRN", r.get("gregorian_year_approx", ""), r.get("value_bln_rials", ""),
                                  "billion rials", slugify(label), label,
                                  "sci-amar:statistical-yearbook-1399",
                                  original_period_label=r.get("solar_year", ""), notes=r.get("notes", "")))
        write_chart(cid, rows)


group14_sci1399()

log(f"After groups 12-14: built={STATS['built']} skipped={STATS['skipped']} rows={STATS['rows_total']}")

# ============================================================================
# GROUP 15: iran_census1996__ -- SCI 1996 (1375) census "Selected Findings" tables, 6 files, all
# wide (one row per entity + several numeric columns), solar_year+gregorian_year already paired.
# ============================================================================

def group15_census1996():
    d = os.path.join(PROC, "iran_census_demographics_series")

    def yr(r):
        return r.get("gregorian_year", "") or sh_to_gregorian(r.get("solar_year", ""))

    if "iran_census1996__admin_units_by_province" in missing:
        recs = load_csv(os.path.join(d, "census1996_admin_units_by_province.csv"))
        vf = ["num_shahrestan", "num_bakhsh", "num_shahr", "num_dehestan", "num_populated_abadi"]
        rows = []
        for r in recs:
            for f in vf:
                if not r.get(f):
                    continue
                label = f"{r['province']} — {f}"
                rows.append(base_row("IRN", yr(r), r[f], "count", slugify(label), label,
                                      r.get("source", "sci-1375-1996-census-selected-findings"),
                                      original_period_label=r.get("solar_year", ""), notes=r.get("notes", "")))
        write_chart("iran_census1996__admin_units_by_province", rows)

    if "iran_census1996__population_by_sex_residence" in missing:
        recs = load_csv(os.path.join(d, "census1996_population_by_sex_residence.csv"))
        vf = ["total_population", "urban_resident", "rural_resident", "non_resident"]
        rows = []
        for r in recs:
            for f in vf:
                if not r.get(f):
                    continue
                label = f"{r['sex']} — {f}"
                rows.append(base_row("IRN", yr(r), r[f], "persons", slugify(label), label,
                                      r.get("source", "sci-1375-1996-census-selected-findings"),
                                      original_period_label=r.get("solar_year", ""), notes=r.get("notes", "")))
        write_chart("iran_census1996__population_by_sex_residence", rows)

    if "iran_census1996__population_by_age_group" in missing:
        recs = load_csv(os.path.join(d, "census1996_population_by_age_group.csv"))
        vf = ["population", "pct_of_total", "male", "female", "sex_ratio_male_per_100_female"]
        units = {"population": "persons", "pct_of_total": "percent", "male": "persons",
                 "female": "persons", "sex_ratio_male_per_100_female": "males per 100 females"}
        rows = []
        for r in recs:
            for f in vf:
                if not r.get(f):
                    continue
                label = f"{r['age_group']} — {f}"
                rows.append(base_row("IRN", yr(r), r[f], units[f], slugify(label), label,
                                      r.get("source", "sci-1375-1996-census-selected-findings"),
                                      original_period_label=r.get("solar_year", ""), notes=r.get("notes", "")))
        write_chart("iran_census1996__population_by_age_group", rows)

    if "iran_census1996__literacy_by_age_group" in missing:
        recs = load_csv(os.path.join(d, "census1996_literacy_by_age_group.csv"))
        vf = ["literacy_rate_pct_female", "literacy_rate_pct_male", "literacy_rate_pct_national_both_sexes"]
        rows = []
        for r in recs:
            for f in vf:
                if not r.get(f):
                    continue
                label = f"{r['age_group']} — {r['area']} — {f}"
                rows.append(base_row("IRN", yr(r), r[f], "percent", slugify(label), label,
                                      r.get("source", "sci-1375-1996-census-selected-findings"),
                                      original_period_label=r.get("solar_year", "")))
        write_chart("iran_census1996__literacy_by_age_group", rows)

    if "iran_census1996__school_enrollment_by_age_group" in missing:
        recs = load_csv(os.path.join(d, "census1996_school_enrollment_by_age_group.csv"))
        vf = ["in_education_pct_female", "in_education_pct_male", "in_education_pct_national_both_sexes"]
        rows = []
        for r in recs:
            for f in vf:
                if not r.get(f):
                    continue
                label = f"{r['age_group']} — {r['area']} — {f}"
                rows.append(base_row("IRN", yr(r), r[f], "percent", slugify(label), label,
                                      r.get("source", "sci-1375-1996-census-selected-findings"),
                                      original_period_label=r.get("solar_year", "")))
        write_chart("iran_census1996__school_enrollment_by_age_group", rows)

    if "iran_census1996__activity_status_by_residence_sex" in missing:
        recs = load_csv(os.path.join(d, "census1996_activity_status_by_residence_sex.csv"))
        vf = ["pct_non_resident_female", "pct_non_resident_male", "pct_rural_female", "pct_rural_male",
              "pct_urban_female", "pct_urban_male", "pct_national"]
        rows = []
        for r in recs:
            for f in vf:
                if not r.get(f):
                    continue
                label = f"{r['activity_status']} — {f}"
                rows.append(base_row("IRN", yr(r), r[f], "percent", slugify(label), label,
                                      r.get("source", "sci-1375-1996-census-selected-findings"),
                                      original_period_label=r.get("solar_year", ""), notes=r.get("notes", "")))
        write_chart("iran_census1996__activity_status_by_residence_sex", rows)


group15_census1996()

log(f"After group 15: built={STATS['built']} skipped={STATS['skipped']} rows={STATS['rows_total']}")

# ============================================================================
# GROUP 16: iran_census__ -- Iranica narrative demography, WB-archives citations, and the
# 2011/2016 census "table"-structured files (already long: table/province/area/year/metric/value).
# ============================================================================

def narrative_year(period_str):
    """Best-effort single year from a free-text period like '1868 (Jan-Mar)', '1956-1966',
    'c.1900', 'mid-1960s' -- returns '' (genuine ambiguity) when no confident single year exists,
    per project convention of leaving year blank rather than guessing."""
    if not period_str:
        return ""
    m = re.match(r"^(\d{4})\b", period_str.strip())
    if m and "-" not in period_str.split()[0][4:5]:
        # single leading 4-digit year not immediately followed by a range dash
        rest = period_str.strip()[4:]
        if not rest.startswith("-"):
            return int(m.group(1))
    return ""


def group16_census_narrative():
    d = os.path.join(PROC, "iran_census_demographics_series")

    if "iran_census__premodern_local_counts_1868_1884" in missing:
        recs = load_csv(os.path.join(d, "iranica_census_demography_narrative_1868_1998.csv"))
        prefixes = ("1868", "1883-84", "1874")
        rows = []
        for r in recs:
            if not str(r.get("year_or_period", "")).startswith(prefixes):
                continue
            label = r["metric"]
            rows.append(base_row(r.get("country_iso3", "IRN"), narrative_year(r["year_or_period"]),
                                  r.get("value", ""), r.get("unit", ""), slugify(label), label,
                                  "iranica-online:census-i-in-iran",
                                  original_period_label=r["year_or_period"], notes=r.get("cited_source", "")))
        write_chart("iran_census__premodern_local_counts_1868_1884", rows)

    KEYWORD_CHARTS = [
        ("iran_census__fertility_family_planning_1956_1991",
         ["fertility rate", "children born", "birth-control pill", "abortion", "family planning",
          "family-planning", "contracept"]),
        ("iran_census__marriage_migration_patterns_1956_1991",
         ["marriage", "married", "migrant", "migration", "exile"]),
        ("iran_census__nomadic_population_1900_1990s", ["nomadic"]),
    ]
    if any(cid in missing for cid, _ in KEYWORD_CHARTS):
        recs = load_csv(os.path.join(d, "iranica_census_demography_narrative_1868_1998.csv"))
        for cid, keywords in KEYWORD_CHARTS:
            if cid not in missing:
                continue
            rows = []
            for r in recs:
                blob = r.get("metric", "").lower()
                if not any(k in blob for k in keywords):
                    continue
                label = r["metric"]
                rows.append(base_row(r.get("country_iso3", "IRN"), narrative_year(r.get("year_or_period", "")),
                                      r.get("value", ""), r.get("unit", ""), slugify(label), label,
                                      "iranica-online:census-i-in-iran",
                                      original_period_label=r.get("year_or_period", ""),
                                      notes=r.get("cited_source", "")))
            write_chart(cid, rows)

    if ("iran_census__wb_archives_reproduction_family_size_1966_1982" in missing
            or "iran_census__tehran_city_population_growth_1956_1972" in missing):
        recs = load_csv(os.path.join(d, "wb_archives_population_demographic_citations_1956_1982.csv"))
        if "iran_census__wb_archives_reproduction_family_size_1966_1982" in missing:
            keywords = ["reproduction rate", "completed family size", "life expectancy"]
            rows = []
            for r in recs:
                blob = r.get("metric", "").lower()
                if not any(k in blob for k in keywords):
                    continue
                label = r["metric"]
                rows.append(base_row(r.get("country_iso3", "IRN"), narrative_year(r.get("year_or_period", "")),
                                      r.get("value", ""), r.get("unit", ""), slugify(label), label,
                                      "world-bank-archives-iran:cep-vol3-population-employment-family-planning",
                                      original_period_label=r.get("year_or_period", ""),
                                      notes=r.get("cited_source", "")))
            write_chart("iran_census__wb_archives_reproduction_family_size_1966_1982", rows)

        if "iran_census__tehran_city_population_growth_1956_1972" in missing:
            rows = []
            for r in recs:
                if "tehran" not in r.get("metric", "").lower():
                    continue
                label = r["metric"]
                rows.append(base_row(r.get("country_iso3", "IRN"), narrative_year(r.get("year_or_period", "")),
                                      r.get("value", ""), r.get("unit", ""), slugify(label), label,
                                      "world-bank-archives-iran:cep-vol3-population-employment-family-planning",
                                      original_period_label=r.get("year_or_period", ""),
                                      notes=r.get("cited_source", "")))
            write_chart("iran_census__tehran_city_population_growth_1956_1972", rows)

    TABLE_2011 = {
        "iran_census__urban_rural_household_indicators_2011": "Table 2 - Population Indicators by Urban/Rural",
        "iran_census__population_by_religion_2011": "Table 3 - Population by Religion",
        "iran_census__sex_ratio_by_province_2011": "Table 14 - Sex Ratio by Province",
        "iran_census__household_size_by_province_2011": "Table 18 - Average Household Size by Province",
    }
    if any(cid in missing for cid in TABLE_2011):
        recs = load_csv(os.path.join(d, "national_and_provincial_summary_2011_census.csv"))
        for cid, table in TABLE_2011.items():
            if cid not in missing:
                continue
            rows = []
            for r in recs:
                if r.get("table") != table:
                    continue
                label = f"{r['metric']} — {r['province']}" if r.get("province") else r["metric"]
                rows.append(base_row(r.get("country_iso3", "IRN"), r.get("year", ""), r.get("value", ""),
                                      r.get("unit", ""), slugify(label), label, r.get("source", "sci-iran-census"),
                                      notes=r.get("area", "") if r.get("area") not in ("total", "") else None))
            write_chart(cid, rows)

    if "iran_census__population_by_nationality_citizenship_2006_2016" in missing:
        recs2011 = load_csv(os.path.join(d, "national_and_provincial_summary_2011_census.csv"))
        recs2016 = load_csv(os.path.join(d, "national_summary_2016_census.csv"))
        rows = []
        for r in recs2011:
            if r.get("table") != "Table 4 - Population by Citizenship":
                continue
            label = f"{r['metric']} — {r['province']}" if r.get("province") else r["metric"]
            rows.append(base_row(r.get("country_iso3", "IRN"), r.get("year", ""), r.get("value", ""),
                                  r.get("unit", ""), slugify(label), label, r.get("source", "sci-iran-census")))
        for r in recs2016:
            if r.get("table") != "Population by nationality, 2006-2016":
                continue
            label = r["metric"]
            rows.append(base_row(r.get("country_iso3", "IRN"), r.get("year", ""), r.get("value", ""),
                                  r.get("unit", ""), slugify(label), label, r.get("source", "sci-iran-census")))
        write_chart("iran_census__population_by_nationality_citizenship_2006_2016", rows)

    if "iran_census__housing_tenure_type_2006_2016" in missing:
        recs2011 = load_csv(os.path.join(d, "national_and_provincial_summary_2011_census.csv"))
        recs2016 = load_csv(os.path.join(d, "national_summary_2016_census.csv"))
        rows = []
        for r in recs2011:
            if r.get("table") != "Table 6 - Housing Tenure Type":
                continue
            label = f"{r['metric']} — {r['province']}" if r.get("province") else r["metric"]
            rows.append(base_row(r.get("country_iso3", "IRN"), r.get("year", ""), r.get("value", ""),
                                  r.get("unit", ""), slugify(label), label, r.get("source", "sci-iran-census")))
        for r in recs2016:
            if r.get("table") != "Household tenure type, 2006-2016":
                continue
            label = r["metric"]
            rows.append(base_row(r.get("country_iso3", "IRN"), r.get("year", ""), r.get("value", ""),
                                  r.get("unit", ""), slugify(label), label, r.get("source", "sci-iran-census")))
        write_chart("iran_census__housing_tenure_type_2006_2016", rows)

    TABLE_2016 = {
        "iran_census__household_development_by_residence_1976_2016": ["Household development by residence 1976-2016"],
        "iran_census__mean_median_age_by_residence_2006_2016": ["Mean age of population by residence, 2006-2016",
                                                                  "Median age of population by residence, 2006-2016"],
        "iran_census__marital_status_2006_2016": ["Population aged 10+ by marital status, 2006-2016"],
    }
    if any(cid in missing for cid in TABLE_2016):
        recs = load_csv(os.path.join(d, "national_summary_2016_census.csv"))
        for cid, tables in TABLE_2016.items():
            if cid not in missing:
                continue
            rows = []
            for r in recs:
                if r.get("table") not in tables:
                    continue
                label = f"{r['metric']} — {r['area']}" if r.get("area") not in ("", "total") else r["metric"]
                rows.append(base_row(r.get("country_iso3", "IRN"), r.get("year", ""), r.get("value", ""),
                                      r.get("unit", ""), slugify(label), label, r.get("source", "sci-iran-census")))
            write_chart(cid, rows)


group16_census_narrative()

log(f"After group 16: built={STATS['built']} skipped={STATS['skipped']} rows={STATS['rows_total']}")

# ============================================================================
# GROUP 17: iran_unctad_maritime__ (4), iran_opec__ (4), iran_giews__ (2) -- already near-target
# long format (country_iso3,metric/line_item,year,value,unit,source,notes).
# ============================================================================

def group17_unctad_opec_giews():
    dm = os.path.join(PROC, "unctad_maritime_series")
    JOBS = [
        ("iran_unctad_maritime__facts_snapshot_2024", "iran_maritime_snapshot_2024.csv", "metric", "value", "unit"),
        ("iran_unctad_maritime__merchandise_trade_2005_2024", "iran_merchandise_trade_2005_2024.csv",
         "line_item", "value_millions_usd", None),
        ("iran_unctad_maritime__transport_services_trade_2005_2024", "iran_transport_services_trade_2005_2024.csv",
         "line_item", "value", None),
        ("iran_unctad_maritime__national_fleet_by_type_2005_2024", "iran_national_fleet_by_type_2005_2024.csv",
         "ship_type", "carrying_capacity_thousand_dwt", None),
    ]
    for cid, fn, label_field, value_field, unit_field in JOBS:
        if cid not in missing:
            continue
        recs = load_csv(os.path.join(dm, fn))
        rows = []
        for r in recs:
            if not r.get(value_field):
                continue
            label = r[label_field]
            unit = r.get(unit_field, "") if unit_field else (
                "thousand DWT" if "fleet" in fn else "millions USD" if "trade" in fn else "")
            rows.append(base_row(r.get("country_iso3", "IRN"), r.get("year", ""), r[value_field], unit,
                                  slugify(label), label, r.get("source", "unctad-maritime"),
                                  notes=r.get("notes", "")))
        write_chart(cid, rows)

    do = os.path.join(PROC, "opec_asb_2025_series")
    OPEC_JOBS = [
        ("iran_opec__facts_snapshot_2024", "iran_opec_facts_2024_snapshot.csv"),
        ("iran_opec__macro_aggregates_2020_2024", "iran_opec_macro_2020_2024.csv"),
        ("iran_opec__natural_gas_2020_2024", "iran_opec_natural_gas_2020_2024.csv"),
        ("iran_opec__heavy_crude_spot_price_2020_2024", "iran_heavy_crude_spot_price_2020_2024.csv"),
    ]
    for cid, fn in OPEC_JOBS:
        if cid not in missing:
            continue
        recs = load_csv(os.path.join(do, fn))
        rows = []
        for r in recs:
            label = r["metric"]
            rows.append(base_row(r.get("country_iso3", "IRN"), r.get("year", ""), r.get("value", ""),
                                  r.get("unit", ""), slugify(label), label,
                                  r.get("source", "opec-asb-2025"), notes=r.get("notes", "")))
        write_chart(cid, rows)

    dg = os.path.join(PROC, "fao_giews_iran_series")

    if "iran_giews__cereal_import_requirements_2010_2027" in missing:
        recs = load_csv(os.path.join(dg, "cereal_import_requirements_2010_2027.csv"))
        rows = []
        for r in recs:
            for vf in ("total_cereal_mt", "maize_mt", "wheat_mt", "barley_mt", "rice_mt"):
                if not r.get(vf):
                    continue
                label = vf.replace("_mt", "").replace("_", " ")
                rows.append(base_row(r.get("country_iso3", "IRN"), "", r[vf], "million metric tons",
                                      slugify(label), label, "fao-giews:iran-country-briefs",
                                      original_period_label=r.get("marketing_year_apr_mar", ""),
                                      notes=f"{r.get('notes','')} [as of {r.get('brief_reference_date','')}, "
                                            f"{r.get('source','')}]"))
        write_chart("iran_giews__cereal_import_requirements_2010_2027", rows)

    if "iran_giews__wheat_guaranteed_purchase_price_2013_2026" in missing:
        recs = load_csv(os.path.join(dg, "wheat_guaranteed_purchase_price_2013_2026.csv"))
        rows = []
        for r in recs:
            for vf, label in [("common_wheat_price", "Common wheat guaranteed purchase price"),
                               ("durum_wheat_price", "Durum wheat guaranteed purchase price")]:
                if not r.get(vf):
                    continue
                rows.append(base_row(r.get("country_iso3", "IRN"), r.get("crop_year", ""), r[vf],
                                      r.get("unit", ""), slugify(label), label,
                                      "fao-giews:iran-country-briefs",
                                      notes=f"{r.get('notes_and_brief_reference_date','')} "
                                            f"[source: {r.get('source','')}]"))
        write_chart("iran_giews__wheat_guaranteed_purchase_price_2013_2026", rows)


group17_unctad_opec_giews()

log(f"After group 17: built={STATS['built']} skipped={STATS['skipped']} rows={STATS['rows_total']}")

# ============================================================================
# GROUP 18: ussr_russia__ / ussr_us__ historical series (CIA Soviet-economy assessments +
# Narodnoe Khozyaistvo yearbooks + Imperial Russia statistical yearbook). country = RUS/SUN
# throughout per country_crosswalk's SUN=USSR convention; USA rows where the file is a direct
# US-USSR comparison keep country_iso3=USA for those specific rows.
# ============================================================================

def group18_ussr():
    d = os.path.join(PROC, "ussr_russia_historical_series")

    if "ussr_russia_cia_gnp_by_sector_1950_1987" in missing:
        recs = load_csv(os.path.join(d, "cia_soviet_gnp_by_sector_1950_1987.csv"))
        rows = []
        for r in recs:
            label = r["sector_of_origin"]
            rows.append(base_row("SUN", r.get("year", ""), r.get("billion_1982_rubles_factor_cost", ""),
                                  "billion 1982 rubles, factor cost", slugify(label), label,
                                  "ussr-russia-historical:cia-soviet-economy-assessments"))
        write_chart("ussr_russia_cia_gnp_by_sector_1950_1987", rows)

    if "ussr_russia_cia_gnp_by_end_use_1950_1987" in missing:
        recs = load_csv(os.path.join(d, "cia_soviet_gnp_by_end_use_1950_1987.csv"))
        rows = []
        for r in recs:
            label = r["end_use_category"]
            rows.append(base_row("SUN", r.get("year", ""), r.get("billion_1982_rubles_factor_cost", ""),
                                  "billion 1982 rubles, factor cost", slugify(label), label,
                                  "ussr-russia-historical:cia-soviet-economy-assessments"))
        write_chart("ussr_russia_cia_gnp_by_end_use_1950_1987", rows)

    if "ussr_russia_cia_consumption_population_1950_1987" in missing:
        recs = load_csv(os.path.join(d, "cia_soviet_consumption_population_1950_1987.csv"))
        rows = []
        for r in recs:
            label = r["indicator"]
            rows.append(base_row("SUN", r.get("year", ""), r.get("value", ""), "", slugify(label), label,
                                  "ussr-russia-historical:cia-soviet-economy-assessments"))
        write_chart("ussr_russia_cia_consumption_population_1950_1987", rows)

    if "ussr_russia_cia_gnp_growth_defense_narrative" in missing:
        recs = load_csv(os.path.join(d, "cia_soviet_gnp_growth_and_defense_narrative.csv"))
        rows = []
        for r in recs:
            label = r["indicator"]
            yr = narrative_year(r.get("period_or_year", ""))
            rows.append(base_row("SUN", yr, r.get("value", ""), "", slugify(label), label,
                                  f"ussr-russia-historical:cia-soviet-economy-assessments:{r.get('source_pdf','')}",
                                  original_period_label=r.get("period_or_year", ""),
                                  notes=f"{r.get('notes','')} [{r.get('source_page_or_location','')}]"))
        write_chart("ussr_russia_cia_gnp_growth_defense_narrative", rows)

    if "ussr_us_gnp_pct_comparison_1960_1983" in missing:
        recs = load_csv(os.path.join(d, "cia_soviet_gnp_pct_of_us_gnp_1960_1983.csv"))
        rows = []
        for r in recs:
            label = "Soviet GNP as % of US GNP"
            rows.append(base_row("SUN", r.get("year", ""), r.get("soviet_gnp_pct_of_us_gnp", ""), "percent",
                                  slugify(label), label, "ussr-russia-historical:cia-soviet-economy-assessments",
                                  notes=r.get("notes", "")))
        write_chart("ussr_us_gnp_pct_comparison_1960_1983", rows)

    for cid, fn, unit in [
        ("ussr_us_gnp_ruble_valuation_1960_1981", "cia_soviet_us_gnp_ruble_valuation_1960_1981.csv", None),
        ("ussr_us_defense_spending_ruble_valuation_1960_1981",
         "cia_soviet_us_defense_spending_ruble_valuation_1960_1981.csv", None),
    ]:
        if cid not in missing:
            continue
        recs = load_csv(os.path.join(d, fn))
        rows = []
        for r in recs:
            iso3 = "SUN" if r.get("series", "").strip().upper() == "USSR" else "USA"
            label = "GNP" if "gnp" in fn else "Defense spending"
            u = unit or r.get("notes", "")
            rows.append(base_row(iso3, r.get("year", ""), r.get("value", ""), u, slugify(label), label,
                                  "ussr-russia-historical:cia-soviet-economy-assessments"))
        write_chart(cid, rows)

    NARKHOZ_SIMPLE = [
        ("ussr_russia_narkhoz_grain_harvest_index_1950_1956", "narkhoz_grain_harvest_index_1950_1956.csv",
         "crop", "gross_harvest_index_1950_100", "index, 1950=100"),
        ("ussr_russia_narkhoz_livestock_products_index_1950_1956", "narkhoz_livestock_products_index_1950_1956.csv",
         "product", "output_index_1950_100", "index, 1950=100"),
    ]
    for cid, fn, label_field, value_field, unit in NARKHOZ_SIMPLE:
        if cid not in missing:
            continue
        recs = load_csv(os.path.join(d, fn))
        rows = []
        for r in recs:
            label = r[label_field]
            rows.append(base_row("SUN", r.get("year", ""), r.get(value_field, ""), unit, slugify(label),
                                  label, "ussr-russia-historical:narodnoe-khozyaistvo-yearbooks"))
        write_chart(cid, rows)

    if "ussr_russia_narkhoz_national_economy_index_1913_1989" in missing:
        recs = load_csv(os.path.join(d, "narkhoz_national_economy_index_1913_1989.csv"))
        rows = []
        for r in recs:
            label = f"{r['indicator']} ({r['index_base']})"
            yr = narrative_year(r.get("year_or_period", ""))
            rows.append(base_row("SUN", yr, r.get("value", ""), r.get("index_base", ""), slugify(label), label,
                                  f"ussr-russia-historical:narodnoe-khozyaistvo-yearbooks:{r.get('edition_and_source_page','')}",
                                  original_period_label=r.get("year_or_period", "")))
        write_chart("ussr_russia_narkhoz_national_economy_index_1913_1989", rows)

    if "ussr_russia_narkhoz_population_1913_1956" in missing:
        recs = load_csv(os.path.join(d, "narkhoz_population_1913_1956.csv"))
        vf = ["total_population_millions", "urban_population_millions", "rural_population_millions",
              "urban_pct_of_total", "rural_pct_of_total"]
        rows = []
        for r in recs:
            for f in vf:
                if not r.get(f):
                    continue
                label = f"{r['year_label']} — {f}"
                unit = "percent" if "pct" in f else "millions"
                rows.append(base_row("SUN", narrative_year(r.get("year_label", "")), r[f], unit, slugify(label),
                                      label, "ussr-russia-historical:narodnoe-khozyaistvo-yearbooks",
                                      original_period_label=r.get("year_label", "")))
        write_chart("ussr_russia_narkhoz_population_1913_1956", rows)

    if "ussr_russia_narkhoz_livestock_headcount_1916_1956" in missing:
        recs = load_csv(os.path.join(d, "narkhoz_livestock_headcount_1916_1956.csv"))
        vf = ["cattle_million_head", "of_which_cows_million_head", "pigs_million_head",
              "sheep_and_goats_million_head"]
        rows = []
        for r in recs:
            for f in vf:
                if not r.get(f):
                    continue
                label = f"{r['date_label']} — {f}"
                rows.append(base_row("SUN", narrative_year(r.get("date_label", "")), r[f], "million head",
                                      slugify(label), label, "ussr-russia-historical:narodnoe-khozyaistvo-yearbooks",
                                      original_period_label=r.get("date_label", "")))
        write_chart("ussr_russia_narkhoz_livestock_headcount_1916_1956", rows)

    if "ussr_russia_narkhoz_1932_five_year_plan_farm_machinery" in missing:
        recs = load_csv(os.path.join(d, "narkhoz_1932_five_year_plan_farm_machinery.csv"))
        rows = []
        for r in recs:
            label = r["machine_type"]
            try:
                yr = int(float(r["year"]))
            except (ValueError, TypeError):
                yr = ""
            rows.append(base_row("SUN", yr, r.get("value", ""), r.get("unit", ""), slugify(label), label,
                                  "ussr-russia-historical:narodnoe-khozyaistvo-yearbooks",
                                  original_period_label=r.get("year", ""), notes=r.get("notes", "")))
        write_chart("ussr_russia_narkhoz_1932_five_year_plan_farm_machinery", rows)

    if "ussr_russia_imperial_population_by_region_1858_1910" in missing:
        recs = load_csv(os.path.join(d, "imperial_russia_population_by_region_1858_1910.csv"))
        rows = []
        for r in recs:
            label = r["region"]
            rows.append(base_row("RUS", narrative_year(r.get("date", "")), r.get("population_thousands", ""),
                                  "thousands", slugify(label), label,
                                  "ussr-russia-historical:imperial-russia-statistical-yearbook",
                                  original_period_label=r.get("date", "")))
        write_chart("ussr_russia_imperial_population_by_region_1858_1910", rows)

    HIST_NAME_TO_ISO3 = {
        "Russia": "RUS", "United States": "USA", "Germany": "DEU", "England": "GBR", "France": "FRA",
        "Italy": "ITA", "Belgium": "BEL", "Netherlands": "NLD", "Denmark": "DNK", "Norway": "NOR",
        "Romania": "ROU", "Sweden": "SWE", "Bulgaria": "BGR", "Switzerland": "CHE", "Japan": "JPN",
        "Spain": "ESP", "Portugal": "PRT", "Greece": "GRC", "Turkey": "TUR",
        # no modern successor state maps cleanly -- left without an iso3 code, not fabricated
        "Austria-Hungary": "",
    }

    if "ussr_russia_imperial_international_population_comparison" in missing:
        recs = load_csv(os.path.join(d, "imperial_russia_international_population_comparison.csv"))
        rows = []
        for r in recs:
            full_label = r["country_and_census_year"]
            base_name = re.sub(r"\s*\(.*\)\s*$", "", full_label).strip()
            iso3 = HIST_NAME_TO_ISO3.get(base_name, "")
            display_name = base_name if base_name == "Russia (Empire average)" else \
                (f"{base_name} (Empire, historical)" if base_name == "Russia" else base_name)
            rows.append(base_row(iso3, "", r.get("population_thousands", ""), "thousands", slugify(full_label),
                                  full_label, "ussr-russia-historical:imperial-russia-statistical-yearbook",
                                  original_period_label=r.get("comparison_group", ""), country_name=display_name))
        write_chart("ussr_russia_imperial_international_population_comparison", rows)

    if "ussr_russia_imperial_population_density_comparison" in missing:
        recs = load_csv(os.path.join(d, "imperial_russia_population_density_comparison.csv"))
        rows = []
        for r in recs:
            country = r["country"]
            base_name = re.sub(r"\s*\(.*\)\s*$", "", country).strip()
            iso3 = HIST_NAME_TO_ISO3.get(base_name, "")
            label = "Population density"
            rows.append(base_row(iso3, r.get("year", ""), r.get("persons_per_sq_verst", ""),
                                  "persons per sq. verst", slugify(label), label,
                                  "ussr-russia-historical:imperial-russia-statistical-yearbook",
                                  country_name=country))
        write_chart("ussr_russia_imperial_population_density_comparison", rows)

    if "ussr_russia_imperial_foreign_trade_1897_1908" in missing:
        recs = load_csv(os.path.join(d, "imperial_russia_foreign_trade_1897_1908.csv"))
        rows = []
        for r in recs:
            label = r["flow"]
            yv = r.get("year", "")
            yr = int(yv) if re.match(r"^\d{4}$", yv or "") else ""
            rows.append(base_row("RUS", yr, r.get("value_rubles", ""), "rubles",
                                  slugify(label), label, "ussr-russia-historical:imperial-russia-statistical-yearbook",
                                  original_period_label=yv if yr == "" else None, notes=r.get("notes", "")))
        write_chart("ussr_russia_imperial_foreign_trade_1897_1908", rows)


group18_ussr()

log(f"After group 18: built={STATS['built']} skipped={STATS['skipped']} rows={STATS['rows_total']}")

# ============================================================================
# GROUP 19: comparator-country archival series (maritime, mining/USGS, Portugal, Spain, Saudi,
# Venezuela) -- long-format files filtered by country_iso3 or source_table.
# ============================================================================

def group19_comparators():
    if "maritime_comparator__unctad_maritime_key_figures_2024" in missing:
        recs = load_csv(os.path.join(PROC, "unctad_maritime_comparators_series",
                                      "unctad_maritime_comparators_2024.csv"))
        rows = []
        for r in recs:
            if not r.get("value"):
                continue
            label = r.get("metric_label") or r.get("metric", "")
            rows.append(base_row(r["country_iso3"], r.get("year", ""), r["value"], r.get("unit", ""),
                                  slugify(label), label, "unctad-maritime:comparator-country-profiles",
                                  country_name=r.get("country_name", cname(r["country_iso3"])),
                                  notes=f"raw: {r.get('value_raw_text','')}" if r.get("estimate_flag") else None))
        write_chart("maritime_comparator__unctad_maritime_key_figures_2024", rows)

    dmin = os.path.join(PROC, "usgs_minerals_comparators_series")
    MINING_COMP = {
        "mining_comparator__arg_usgs_mineral_production": "ARG",
        "mining_comparator__tur_usgs_mineral_production": "TUR",
        "mining_comparator__sau_usgs_mineral_production": "SAU",
        "mining_comparator__rus_usgs_mineral_production": "RUS",
        "mining_comparator__usa_usgs_mineral_production": "USA",
    }
    if any(cid in missing for cid in MINING_COMP):
        recs = load_csv(os.path.join(dmin, "usgs_minerals_comparators_2014_2023.csv"))
        for cid, iso3 in MINING_COMP.items():
            if cid not in missing:
                continue
            rows = []
            for r in recs:
                if r.get("country_iso3") != iso3 or not r.get("value"):
                    continue
                label = r["commodity"]
                rows.append(base_row(iso3, r.get("year", ""), r["value"], r.get("unit", ""), slugify(label),
                                      label, f"usgs-minerals-yearbook:{r.get('source_yearbook_edition','')}",
                                      notes=f"flag={r.get('flag','')}" if r.get("flag") else None))
            write_chart(cid, rows)

    dp = os.path.join(PROC, "portugal_historical_series")
    PORTUGAL_INE = {
        "portugal_comparator__population_employment_1941_2020": ["Q1.1", "Q1.2", "Q1.11"],
        "portugal_comparator__investment_fbcf_1953_2020": ["Q2.1"],
        "portugal_comparator__gdp_national_accounts_1953_2020": ["Q3.1", "Q3.6.1"],
        "portugal_comparator__cpi_1948_2020": ["Q4.1", "Q4.2"],
        "portugal_comparator__monetary_aggregates_1947_2020": ["Q5.1", "Q5.2"],
        "portugal_comparator__government_finance_debt_1947_2020": ["Q6.1", "Q6.3"],
        "portugal_comparator__balance_of_payments_1948_2020": ["Q7.3"],
    }
    if any(cid in missing for cid in PORTUGAL_INE):
        recs = load_csv(os.path.join(dp, "ine_slep2020_headline_series.csv"))
        for cid, tables in PORTUGAL_INE.items():
            if cid not in missing:
                continue
            rows = []
            for r in recs:
                if r.get("source_table") not in tables or not r.get("value"):
                    continue
                label = r["indicator"]
                rows.append(base_row("PRT", r.get("year", ""), r["value"], r.get("unit", ""), slugify(label),
                                      label, f"ine-portugal:slep2020:{r.get('source_table','')}",
                                      notes=r.get("table_title", "")))
            write_chart(cid, rows)

    if "portugal_comparator__central_bank_balance_sheet_1947_1976" in missing:
        recs = load_csv(os.path.join(dp, "banco_portugal_balance_sheet_1947_1976.csv"))
        rows = []
        for r in recs:
            if not r.get("value_million_escudos"):
                continue
            label = f"{r['section']} — {r['item']}"
            rows.append(base_row("PRT", r.get("year", ""), r["value_million_escudos"], "million escudos",
                                  slugify(label), label, "banco-portugal:series-longas-pos-guerra",
                                  original_period_label=r.get("period", "")))
        write_chart("portugal_comparator__central_bank_balance_sheet_1947_1976", rows)

    dsp = os.path.join(PROC, "spain_historical_series")
    SPAIN = {
        "spain_comparator__gdp_long_run_1850_2000": ["Cuadro 17.6", "Cuadro 17.7", "Cuadro 17.8"],
        "spain_comparator__price_indices_1800_2000": ["Cuadro 16.19", "Cuadro 16.20"],
    }
    if any(cid in missing for cid in SPAIN):
        recs = load_csv(os.path.join(dsp, "carreras_tafunell_gdp_cpi_1800_2000.csv"))
        for cid, tables in SPAIN.items():
            if cid not in missing:
                continue
            rows = []
            for r in recs:
                if r.get("source_table") not in tables or not r.get("value"):
                    continue
                label = r["series"]
                rows.append(base_row("ESP", r.get("year", ""), r["value"], "", slugify(label), label,
                                      f"banco-espana-historical:carreras-tafunell:{r.get('source_table','')}",
                                      notes=r.get("table_title", "")))
            write_chart(cid, rows)

    dsa = os.path.join(PROC, "saudi_gastat_series")

    if "saudi_comparator__national_accounts_aggregates_2018_2024" in missing:
        recs = load_csv(os.path.join(dsa, "gastat_national_accounts_2018_2024.csv"))
        rows = []
        for r in recs:
            if r.get("source_table") != "Table 8" or not r.get("value"):
                continue
            label = r["indicator"]
            rows.append(base_row("SAU", r.get("year", ""), r["value"], r.get("unit", ""), slugify(label), label,
                                  "gastat-saudi:national-accounts:Table 8", notes=r.get("table_title", "")))
        write_chart("saudi_comparator__national_accounts_aggregates_2018_2024", rows)

    if "saudi_comparator__gdp_by_sector_and_investment_2018_2024" in missing:
        recs = load_csv(os.path.join(dsa, "gastat_national_accounts_2018_2024.csv"))
        tables = expand_pipe_filter("1|5|6|12", "Table ")
        rows = []
        for r in recs:
            if r.get("source_table") not in tables or not r.get("value"):
                continue
            label = f"{r['table_title']} — {r['indicator']}"
            rows.append(base_row("SAU", r.get("year", ""), r["value"], r.get("unit", ""), slugify(label), label,
                                  f"gastat-saudi:national-accounts:{r.get('source_table','')}"))
        write_chart("saudi_comparator__gdp_by_sector_and_investment_2018_2024", rows)

    if "saudi_comparator__cpi_2024_2026" in missing:
        recs = load_csv(os.path.join(dsa, "gastat_cpi_series.csv"))
        rows = []
        for r in recs:
            if not r.get("value"):
                continue
            label = f"{r['series_type']} — {r['section']} — {r['metric']}"
            rows.append(base_row("SAU", leading_year(r.get("period", "")), r["value"],
                                  "index" if "index" in r.get("metric", "") else "",
                                  slugify(label), label, "gastat-saudi:cpi-series",
                                  original_period_label=r.get("period", ""), notes=r.get("base_period", "")))
        write_chart("saudi_comparator__cpi_2024_2026", rows)

    dve = os.path.join(PROC, "venezuela_ovf_series")

    if "venezuela_comparator__ovf_macro_aggregates_2012_2024" in missing:
        recs = load_csv(os.path.join(dve, "ovf_macro_indicators_2012_2024.csv"))
        rows = []
        for r in recs:
            if r.get("source_table") != "Cuadro 9" or not r.get("value"):
                continue
            label = f"{r['section']} — {r['variable']}"
            rows.append(base_row("VEN", r.get("year", ""), r["value"], r.get("unit", ""), slugify(label), label,
                                  "ovf-venezuela:Cuadro 9"))
        write_chart("venezuela_comparator__ovf_macro_aggregates_2012_2024", rows)

    if "venezuela_comparator__ovf_global_context_gdp_inflation_2021_2024" in missing:
        recs = load_csv(os.path.join(dve, "ovf_macro_indicators_2012_2024.csv"))
        rows = []
        for r in recs:
            if r.get("source_table") not in ("Cuadro 1", "Cuadro 2") or not r.get("value"):
                continue
            label = f"{r['section']} — {r['variable']}"
            rows.append(base_row("VEN", r.get("year", ""), r["value"], r.get("unit", ""), slugify(label), label,
                                  f"ovf-venezuela:imf-via-ovf:{r.get('source_table','')}"))
        write_chart("venezuela_comparator__ovf_global_context_gdp_inflation_2021_2024", rows)


group19_comparators()

log(f"After group 19: built={STATS['built']} skipped={STATS['skipped']} rows={STATS['rows_total']}")

# ============================================================================
# GROUP 20: iran_disasters__ (NOAA earthquakes, Iran Data Portal social-statistics tables).
# ============================================================================

def group20_disasters():
    d = os.path.join(PROC, "iran_disasters_regional_series")

    if "iran_disasters__significant_earthquakes_1956_2023" in missing:
        recs = load_csv(os.path.join(d, "significant_earthquakes_1956_2023.csv"))
        value_fields = ["eqMagnitude", "deaths", "injuries", "housesDestroyed", "damageMillionsDollars"]
        units = {"eqMagnitude": "magnitude", "deaths": "persons", "injuries": "persons",
                 "housesDestroyed": "houses", "damageMillionsDollars": "million USD"}
        rows = []
        for r in recs:
            loc = r.get("locationName", "").strip()
            for vf in value_fields:
                if not r.get(vf):
                    continue
                label = f"{loc} — {vf}"
                date_label = f"{r.get('year','')}-{r.get('month','')}-{r.get('day','')}"
                rows.append(base_row("IRN", r.get("year", ""), r[vf], units[vf], slugify(label), label,
                                      r.get("source", "noaa-ncei-significant-earthquake-database"),
                                      original_period_label=date_label))
        write_chart("iran_disasters__significant_earthquakes_1956_2023", rows)

    if "iran_disasters__gold_price_divorce_rate_descriptive_stats_1980_2014" in missing:
        recs = load_csv(os.path.join(d, "gold_price_divorce_rate_study.csv"))
        rows = []
        for r in recs:
            label = r["metric"]
            rows.append(base_row(r.get("country_iso3", "IRN"), "", r.get("value", ""), r.get("unit", ""),
                                  slugify(label), label, r.get("source", "farzanegan-gholipour-2018"),
                                  original_period_label=r.get("period", ""), notes=r.get("notes", "")))
        write_chart("iran_disasters__gold_price_divorce_rate_descriptive_stats_1980_2014", rows)

    if "iran_disasters__mean_age_at_first_marriage_1966_2006" in missing:
        recs = load_csv(os.path.join(d, "mean_age_at_first_marriage_1966_2006.csv"))
        rows = []
        for r in recs:
            label = f"{r['area']} — {r['sex']}"
            rows.append(base_row(r.get("country_iso3", "IRN"), r.get("year", ""),
                                  r.get("mean_age_at_first_marriage", ""), "years", slugify(label), label,
                                  r.get("source", "iran-data-portal")))
        write_chart("iran_disasters__mean_age_at_first_marriage_1966_2006", rows)

    if "iran_disasters__registered_marriages_divorces_1991_2006" in missing:
        recs = load_csv(os.path.join(d, "registered_marriages_divorces_1991_2006.csv"))
        rows = []
        for r in recs:
            label = f"{r['metric']} — {r['province']}"
            rows.append(base_row(r.get("country_iso3", "IRN"), r.get("year", ""), r.get("value", ""), "count",
                                  slugify(label), label, r.get("source", "iran-data-portal")))
        write_chart("iran_disasters__registered_marriages_divorces_1991_2006", rows)

    if "iran_disasters__registered_births_by_sex_1991_2006" in missing:
        recs = load_csv(os.path.join(d, "registered_births_by_sex_1991_2006.csv"))
        rows = []
        for r in recs:
            label = f"{r['sex']} — {r['province']}"
            rows.append(base_row(r.get("country_iso3", "IRN"), r.get("year", ""), r.get("value", ""), "count",
                                  slugify(label), label, r.get("source", "iran-data-portal")))
        write_chart("iran_disasters__registered_births_by_sex_1991_2006", rows)

    if "iran_disasters__employed_by_occupation_gender_2005_2013" in missing:
        recs = load_csv(os.path.join(d, "labor_force_by_occupation_and_gender_2005_2013.csv"))
        rows = []
        for r in recs:
            label = f"{r['occupation']} — {r['sex']} — {r['area']}"
            yr = fiscal_range_to_later_year(r.get("year_western", ""))
            rows.append(base_row(r.get("country_iso3", "IRN"), yr, r.get("value", ""),
                                  r.get("unit", ""), slugify(label), label, r.get("source", "iran-data-portal"),
                                  original_period_label=f"{r.get('year_iranian','')} ({r.get('year_western','')})"))
        write_chart("iran_disasters__employed_by_occupation_gender_2005_2013", rows)

    if "iran_disasters__ssi_pensioners_amounts_paid_1991_2006" in missing:
        recs = load_csv(os.path.join(d, "ssi_pensioners_and_amounts_paid_1991_2006.csv"))
        rows = []
        for r in recs:
            for vf, unit in [("number", "persons"), ("amount_million_rials", "million rials")]:
                if not r.get(vf):
                    continue
                label = f"{r['category']} — {vf}"
                rows.append(base_row(r.get("country_iso3", "IRN"), r.get("year", ""), r[vf], unit,
                                      slugify(label), label, r.get("source", "iran-data-portal")))
        write_chart("iran_disasters__ssi_pensioners_amounts_paid_1991_2006", rows)


group20_disasters()

# ============================================================================
# GROUP 21: iran_institutions__, iran_fx__ (non-daily), iran_migration__, iran_trade__ singles.
# ============================================================================

def group21_institutions_fx_trade():
    d = os.path.join(PROC, "iran_trade_institutions_fx_series")

    if "iran_institutions__opec_quota_policy_history_1960_2025" in missing:
        recs = load_csv(os.path.join(d, "opec_quota_policy_history_1960_2025.csv"))
        rows = []
        for r in recs:
            label = r["event"]
            rows.append(base_row(r.get("country_iso3", "IRN"), r.get("year", ""), r.get("figure_value", ""),
                                  r.get("unit", ""), slugify(label), label, r.get("source_name", "iran-opec-membership"),
                                  original_period_label=r.get("date", ""), notes=r.get("description", "")))
        write_chart("iran_institutions__opec_quota_policy_history_1960_2025", rows)

    if "iran_institutions__wto_gatt_accession_timeline_1995_2026" in missing:
        recs = load_csv(os.path.join(d, "wto_gatt_accession_timeline_1995_2026.csv"))
        rows = []
        for r in recs:
            label = r["event"]
            rows.append(base_row(r.get("country_iso3", "IRN"), r.get("year", ""), "", "", slugify(label), label,
                                  r.get("source_name", "iran-wto-gatt-accession"),
                                  original_period_label=r.get("date", ""), notes=r.get("description", "")))
        write_chart("iran_institutions__wto_gatt_accession_timeline_1995_2026", rows)

    if "iran_institutions__imf_article_iv_consultation_history_2002_2025" in missing:
        recs = load_csv(os.path.join(d, "imf_article_iv_consultation_history_2002_2025.csv"))
        rows = []
        for r in recs:
            label = r["event_type"]
            cy = r.get("consultation_year", "")
            yr = int(cy) if re.match(r"^\d{4}$", cy or "") else ""
            rows.append(base_row(r.get("country_iso3", "IRN"), yr, "", "",
                                  slugify(label), label, r.get("source_name", "imf-article-iv-iran"),
                                  original_period_label=f"{cy} ({r.get('mission_or_conclusion_date', '')})",
                                  notes=r.get("headline_findings", "")))
        write_chart("iran_institutions__imf_article_iv_consultation_history_2002_2025", rows)

    if "iran_fx__mazarei_1995_parallel_fx_market_1978_1990" in missing:
        recs = load_csv(os.path.join(d, "mazarei_1995_parallel_fx_market_1978_1990.csv"))
        rows = []
        for r in recs:
            label = f"{r['series']} — {r['statistic']}"
            rows.append(base_row(r.get("country_iso3", "IRN"), "", r.get("value", ""), r.get("unit", ""),
                                  slugify(label), label, "imf-mazarei-1995",
                                  original_period_label="1978-1990 (parallel-market study period)",
                                  notes=r.get("notes", "")))
        write_chart("iran_fx__mazarei_1995_parallel_fx_market_1978_1990", rows)

    if "iran_migration__knomad_remittances_diaspora_2000_2023" in missing:
        recs = load_csv(os.path.join(d, "knomad_remittances_migration_2000_2023.csv"))
        rows = []
        for r in recs:
            label = f"{r['series']} — {r['counterpart_country']}"
            rows.append(base_row(r.get("country_iso3", "IRN"), r.get("year", ""), r.get("value", ""),
                                  r.get("unit", ""), slugify(label), label, "worldbank-knomad",
                                  notes=r.get("notes", "")))
        write_chart("iran_migration__knomad_remittances_diaspora_2000_2023", rows)

    if "iran_trade__handicraft_export_institutional_history" in missing:
        recs = load_csv(os.path.join(d, "handicraft_export_and_institutional_history.csv"))
        rows = []
        for r in recs:
            label = r["category"]
            yr = narrative_year(r.get("period", ""))
            rows.append(base_row(r.get("country_iso3", "IRN"), yr, r.get("figure_value", ""), r.get("unit", ""),
                                  slugify(label), label, r.get("source_name", "tehran-times"),
                                  original_period_label=r.get("period", ""), notes=r.get("description", "")))
        write_chart("iran_trade__handicraft_export_institutional_history", rows)

    if "iran_trade__cites_caviar_quota_trade_timeline_1998_2006" in missing:
        recs = load_csv(os.path.join(d, "cites_caviar_quota_trade_timeline_1998_2006.csv"))
        rows = []
        for r in recs:
            label = f"{r['scope']} — {r['figure_type']}"
            yr = narrative_year(r.get("year", ""))
            rows.append(base_row(r.get("country_iso3", "IRN"), yr, r.get("value_kg", ""), "kg",
                                  slugify(label), label, r.get("source_name", "cites-caviar"),
                                  original_period_label=r.get("year", ""), notes=r.get("description", "")))
        write_chart("iran_trade__cites_caviar_quota_trade_timeline_1998_2006", rows)


group21_institutions_fx_trade()

log(f"After groups 20-21: built={STATS['built']} skipped={STATS['skipped']} rows={STATS['rows_total']}")

# ============================================================================
# GROUP 22: daily-frequency series -- TGJU Iran FX/gold (3) and BCRA Argentina (5) + Venezuela
# parallel-FX milestones (1). Daily OHLC files melt into open/low/high/close/change variants,
# each row keeping the exact date in original_period_label (year alone would collapse ~365
# distinct daily observations per year into one, which is not the target -- multiple rows per
# country+year+variant, disambiguated by original_period_label, preserves full fidelity).
# ============================================================================

def group22_daily_fx():
    d = os.path.join(PROC, "iran_trade_institutions_fx_series")
    OHLC = ["open", "low", "high", "close"]
    CHANGE = ["change_abs", "change_pct"]

    def ohlc_rows(recs, base_label, unit, source_dataset):
        rows = []
        for r in recs:
            yr = extract_year_from_date(r.get("date_gregorian", ""))
            for vf in OHLC:
                if not r.get(vf):
                    continue
                label = f"{base_label} — {vf}"
                rows.append(base_row("IRN", yr, r[vf], unit, slugify(label), label, source_dataset,
                                      original_period_label=r.get("date_gregorian", "")))
            for vf in CHANGE:
                if not r.get(vf):
                    continue
                u = unit if vf == "change_abs" else "percent"
                label = f"{base_label} — {vf}"
                rows.append(base_row("IRN", yr, r[vf], u, slugify(label), label, source_dataset,
                                      original_period_label=r.get("date_gregorian", "")))
        return rows

    if "iran_fx__usd_irr_parallel_rate_daily_2011_2026" in missing:
        recs = load_csv(os.path.join(d, "usd_irr_parallel_rate_daily_2011_2026.csv"))
        write_chart("iran_fx__usd_irr_parallel_rate_daily_2011_2026",
                    ohlc_rows(recs, "USD/IRR parallel-market rate", "IRR per USD", "tgju:price_dollar_rl"))

    if "iran_fx__gold_coin_bahar_azadi_price_daily_2013_2026" in missing:
        recs = load_csv(os.path.join(d, "gold_coin_bahar_azadi_price_daily_2013_2026.csv"))
        write_chart("iran_fx__gold_coin_bahar_azadi_price_daily_2013_2026",
                    ohlc_rows(recs, "Bahar Azadi gold coin price", "IRR per coin", "tgju:sekeb"))

    if "iran_fx__gold_coin_emami_price_daily_2010_2026" in missing:
        recs = load_csv(os.path.join(d, "gold_coin_emami_price_daily_2010_2026.csv"))
        write_chart("iran_fx__gold_coin_emami_price_daily_2010_2026",
                    ohlc_rows(recs, "Emami gold coin price", "IRR per coin", "tgju:sekee"))

    ARG = [
        ("fx_comparator__argentina_fx_retail_rate_daily", "argentina_fx_retail_rate_daily.csv"),
        ("fx_comparator__argentina_fx_wholesale_reference_rate_daily", "argentina_fx_wholesale_reference_rate_daily.csv"),
        ("fx_comparator__argentina_international_reserves_daily", "argentina_international_reserves_daily.csv"),
        ("fx_comparator__argentina_badlar_interest_rate_daily", "argentina_badlar_interest_rate_daily.csv"),
        ("fx_comparator__argentina_monetary_policy_rate_daily", "argentina_monetary_policy_rate_daily.csv"),
    ]
    for cid, fn in ARG:
        if cid not in missing:
            continue
        recs = load_csv(os.path.join(d, fn))
        rows = []
        for r in recs:
            if not r.get("value"):
                continue
            label = r.get("metric", fn)
            yr = extract_year_from_date(r.get("date", ""))
            rows.append(base_row(r.get("country_iso3", "ARG"), yr, r["value"], r.get("unit", ""),
                                  slugify(label), label, "bcra-argentina:statistics-api",
                                  original_period_label=r.get("date", "")))
        write_chart(cid, rows)

    if "fx_comparator__venezuela_parallel_fx_milestones_2003_2020" in missing:
        recs = load_csv(os.path.join(d, "venezuela_parallel_fx_rate_milestones_2003_2020.csv"))
        rows = []
        for r in recs:
            for vf in ("rate_low", "rate_high"):
                if not r.get(vf):
                    continue
                label = f"{r['rate_type']} — {vf}"
                rows.append(base_row(r.get("country_iso3", "VEN"), extract_year_from_date(r.get("date", "")),
                                      r[vf], r.get("unit", ""), slugify(label), label,
                                      r.get("source", "venezuela-parallel-fx-history"),
                                      original_period_label=r.get("date", ""), notes=r.get("notes", "")))
        write_chart("fx_comparator__venezuela_parallel_fx_milestones_2003_2020", rows)


group22_daily_fx()

log(f"After group 22: built={STATS['built']} skipped={STATS['skipped']} rows={STATS['rows_total']}")

# ============================================================================
# GROUP 23 (round 2, 2026-07-13): US/IMF primary-source narrative-citation archives --
# FRUS 1951-54 & 1973-76, CIA war-era (1974-1988) + NIS-33 (1973 survey), USAID Point Four
# RAC secondary-research reports, IMF Article IV 2015/2018. All 6 source files share one
# schema: date_label,year,category,subcategory,value,unit,notes,country_iso3,
# source_dataset,citation [+ value_usd_nominal,value_usd_real_2015,currency_conversion_note
# on the IMF file] -- structurally the pahlavi category/subcategory schema (see
# rows_from_catsub above) but keyed on date_label (not fiscal_year_label) and carrying a
# per-row `citation` (exact document/page) that pahlavi's single-document tables didn't
# need, since these files mix many distinct source documents under one source_dataset tag.
# The registry's own underlying_codes strings for this batch use a
# "path|source_dataset=X & category in {A,B,C} (n1+n2+... = N rows)" mini-DSL; rather than
# writing a string parser for a one-off 34-chart_id batch, the same filter is expressed
# directly as composable predicates (cat_eq/cat_in/src_eq/all_of) -- verified below to
# reproduce the registry's own stated row counts exactly for every one of the 34 chart_ids.
# ============================================================================

def cat_eq(c):
    return lambda r: (r.get("category") or "").strip() == c


def cat_in(cats):
    s = set(cats)
    return lambda r: (r.get("category") or "").strip() in s


def src_eq(sd):
    return lambda r: (r.get("source_dataset") or "").strip() == sd


def all_of(*preds):
    return lambda r: all(p(r) for p in preds)


def rows_from_citation_series(records, source_dataset_override=None, row_filter=None,
                               country_iso3="IRN", include_citation=True):
    out = []
    for r in records:
        if row_filter and not row_filter(r):
            continue
        cat = (r.get("category") or "").strip()
        sub = (r.get("subcategory") or "").strip()
        label = f"{cat} — {sub}" if sub else cat
        vcode = slugify(label)
        sd = source_dataset_override or r.get("source_dataset", "")
        ciso = r.get("country_iso3") or country_iso3
        # the FRUS 1973-76 file tags some rows country_iso3=IRQ (Iraq context around
        # Iran-focused discussions, per that folder's own convention) -- country_crosswalk's
        # COUNTRIES dict only covers this project's 18 tracked comparators (Iraq isn't one),
        # so name it explicitly here rather than let cname() fall back to the bare code.
        cname_override = "Iraq" if ciso == "IRQ" else None
        yr = r.get("year", "")
        dl = r.get("date_label", "")
        has_usd = bool(r.get("value_usd_nominal") or r.get("value_usd_real_2015"))
        note_parts = []
        if r.get("notes"):
            note_parts.append(r["notes"])
        if not has_usd and r.get("currency_conversion_note"):
            note_parts.append(f"[{r['currency_conversion_note']}]")
        if include_citation and r.get("citation"):
            note_parts.append(f"[cite: {r['citation']}]")
        notes = " ".join(note_parts) if note_parts else None
        out.append(base_row(ciso, yr, r.get("value", ""), r.get("unit", ""), vcode, label, sd,
                             original_period_label=dl if dl and dl != yr else None,
                             computed=False if has_usd else None,
                             notes=notes, country_name=cname_override))
        if r.get("value_usd_nominal"):
            out.append(base_row(ciso, yr, r["value_usd_nominal"], "current US$ (computed)",
                                 vcode + ".USD_NOMINAL", label + " (computed, nominal US$)", sd,
                                 original_period_label=dl if dl and dl != yr else None,
                                 computed=True, notes=r.get("currency_conversion_note", ""),
                                 country_name=cname_override))
        if r.get("value_usd_real_2015"):
            out.append(base_row(ciso, yr, r["value_usd_real_2015"], "constant 2015 US$ (computed)",
                                 vcode + ".USD_REAL_2015", label + " (computed, real 2015 US$)", sd,
                                 original_period_label=dl if dl and dl != yr else None,
                                 computed=True, notes=r.get("currency_conversion_note", ""),
                                 country_name=cname_override))
    return out


def group23_us_primary_source_archives():
    dfrus = os.path.join(PROC, "frus_iran_economic_citations_series")
    frus1951 = load_csv(os.path.join(dfrus, "frus_1951_54_mossadegh_coup_era.csv"))
    frus1973 = load_csv(os.path.join(dfrus, "frus_1973_76_oil_boom_era.csv"))
    dcia = os.path.join(PROC, "cia_iran_economy_series")
    cia_war = load_csv(os.path.join(dcia, "cia_iran_iraq_economic_assessments_1974_1988.csv"))
    cia_nis33 = load_csv(os.path.join(dcia, "cia_nis33_iran_economy_survey_1973.csv"))
    usaid = load_csv(os.path.join(PROC, "usaid_point_four_series",
                                   "usaid_point_four_rac_research_reports.csv"))
    imf = load_csv(os.path.join(PROC, "imf_article_iv_iran_series",
                                 "imf_article_iv_iran_2015_2018.csv"))

    # --- FRUS 1951-54 (Mossadegh/coup era) ---
    if "frus__1951_54_foreign_aid_exim_loan_negotiations" in missing:
        write_chart("frus__1951_54_foreign_aid_exim_loan_negotiations",
                    rows_from_citation_series(frus1951, row_filter=cat_eq("Foreign aid")))
    if "frus__1951_54_oil_production_trade_abadan_crisis" in missing:
        write_chart("frus__1951_54_oil_production_trade_abadan_crisis",
                    rows_from_citation_series(frus1951, row_filter=cat_eq("Oil production & trade")))
    if "frus__1951_54_misc_smaller_categories" in missing:
        write_chart("frus__1951_54_misc_smaller_categories",
                    rows_from_citation_series(frus1951, row_filter=cat_in(
                        ["Prices", "Trade", "Money supply", "Agriculture", "Demographics",
                         "Covert operations financing", "External debt", "External assets",
                         "Employment"])))

    # --- FRUS 1973-76 (oil boom era) ---
    if "frus__1973_76_arms_deals_cost_escalation" in missing:
        write_chart("frus__1973_76_arms_deals_cost_escalation",
                    rows_from_citation_series(frus1973, row_filter=cat_eq("Military expenditure")))
    if "frus__1973_76_oil_price_shock_production_revenue" in missing:
        write_chart("frus__1973_76_oil_price_shock_production_revenue",
                    rows_from_citation_series(frus1973, row_filter=cat_eq("Oil production & trade")))
    if "frus__1973_76_government_finance_oil_dependence" in missing:
        write_chart("frus__1973_76_government_finance_oil_dependence",
                    rows_from_citation_series(frus1973, row_filter=cat_eq("Government Finance")))
    if "frus__1973_76_outbound_foreign_aid" in missing:
        write_chart("frus__1973_76_outbound_foreign_aid",
                    rows_from_citation_series(frus1973, row_filter=cat_eq("Foreign aid")))
    if "frus__1973_76_western_oil_import_cost_impact" in missing:
        write_chart("frus__1973_76_western_oil_import_cost_impact",
                    rows_from_citation_series(frus1973, row_filter=cat_eq("Balance of Payments")))
    if "frus__1973_76_foreign_investment_deal_pipeline" in missing:
        write_chart("frus__1973_76_foreign_investment_deal_pipeline",
                    rows_from_citation_series(frus1973, row_filter=cat_eq("Foreign investment")))
    if "frus__1973_76_trade_targets_historical_comparison" in missing:
        write_chart("frus__1973_76_trade_targets_historical_comparison",
                    rows_from_citation_series(frus1973, row_filter=cat_eq("Trade")))
    if "frus__1973_76_gnp_targets_comparator_growth" in missing:
        write_chart("frus__1973_76_gnp_targets_comparator_growth",
                    rows_from_citation_series(frus1973, row_filter=cat_eq("Macro / National Accounts")))
    if "frus__1973_76_inflation_and_import_prices" in missing:
        write_chart("frus__1973_76_inflation_and_import_prices",
                    rows_from_citation_series(frus1973, row_filter=cat_eq("Prices")))
    if "frus__1973_76_demographics_population" in missing:
        write_chart("frus__1973_76_demographics_population",
                    rows_from_citation_series(frus1973, row_filter=cat_eq("Demographics & Population")))
    if "frus__1973_76_misc_smaller_categories" in missing:
        write_chart("frus__1973_76_misc_smaller_categories",
                    rows_from_citation_series(frus1973, row_filter=cat_in(
                        ["Manufacturing", "Agriculture", "Metals & Minerals", "Labor & Employment",
                         "External debt", "Land Use", "Foreign exchange"])))

    # --- CIA war-era (1974-1988): shah-economy-overview, iran-iraq-economic-balance-1986,
    # war-weary-economies-1988 (split 3 ways), gloomy-economic-prospects-1987 (split 4 ways) ---
    if "cia_econ__shah_economy_overview_1974" in missing:
        write_chart("cia_econ__shah_economy_overview_1974",
                    rows_from_citation_series(cia_war, row_filter=src_eq("cia-shah-economy-overview-1974")))
    if "cia_econ__iran_iraq_economic_balance_1986" in missing:
        write_chart("cia_econ__iran_iraq_economic_balance_1986",
                    rows_from_citation_series(cia_war, row_filter=src_eq("cia-iran-iraq-economic-balance-1986")))
    if "cia_econ__war_weary_demographic_macro_comparison_1988" in missing:
        write_chart("cia_econ__war_weary_demographic_macro_comparison_1988",
                    rows_from_citation_series(cia_war, row_filter=all_of(
                        src_eq("cia-iran-iraq-war-weary-economies-1988"),
                        cat_in(["Demographics", "Demographics & Population", "Health",
                                "Social Protection", "Macro / National Accounts"]))))
    if "cia_econ__war_weary_external_sector_comparison_1988" in missing:
        write_chart("cia_econ__war_weary_external_sector_comparison_1988",
                    rows_from_citation_series(cia_war, row_filter=all_of(
                        src_eq("cia-iran-iraq-war-weary-economies-1988"),
                        cat_in(["External debt", "Foreign exchange", "Foreign aid", "Trade",
                                "Oil production & trade", "Balance of Payments (Net)",
                                "Balance of Payments (misc)"]))))
    if "cia_econ__war_weary_military_infra_govt_finance_1988" in missing:
        write_chart("cia_econ__war_weary_military_infra_govt_finance_1988",
                    rows_from_citation_series(cia_war, row_filter=all_of(
                        src_eq("cia-iran-iraq-war-weary-economies-1988"),
                        cat_in(["Military expenditure", "Infrastructure (Transport)",
                                "Infrastructure & Technology", "Energy", "Government finance",
                                "Labor & Employment", "Prices"]))))
    if "cia_econ__gloomy_prospects_current_account_scenarios_1987" in missing:
        write_chart("cia_econ__gloomy_prospects_current_account_scenarios_1987",
                    rows_from_citation_series(cia_war, row_filter=all_of(
                        src_eq("cia-iran-iraq-gloomy-economic-prospects-1987"),
                        cat_in(["Balance of Payments (Net)", "Balance of Payments (misc)"]))))
    if "cia_econ__gloomy_prospects_trade_oil_1987" in missing:
        write_chart("cia_econ__gloomy_prospects_trade_oil_1987",
                    rows_from_citation_series(cia_war, row_filter=all_of(
                        src_eq("cia-iran-iraq-gloomy-economic-prospects-1987"),
                        cat_in(["Trade", "Oil production & trade"]))))
    if "cia_econ__gloomy_prospects_iraq_debt_rescheduling_1987" in missing:
        write_chart("cia_econ__gloomy_prospects_iraq_debt_rescheduling_1987",
                    rows_from_citation_series(cia_war, row_filter=all_of(
                        src_eq("cia-iran-iraq-gloomy-economic-prospects-1987"),
                        cat_eq("External debt"))))
    if "cia_econ__gloomy_prospects_misc_1987" in missing:
        write_chart("cia_econ__gloomy_prospects_misc_1987",
                    rows_from_citation_series(cia_war, row_filter=all_of(
                        src_eq("cia-iran-iraq-gloomy-economic-prospects-1987"),
                        cat_in(["Foreign aid", "Foreign exchange", "Military expenditure", "Prices",
                                "Demographics & Population", "Labor & Employment",
                                "Infrastructure & Technology", "Macro / National Accounts"]))))

    # --- CIA NIS-33 (1973 economy survey) ---
    if "nis33__land_use_irrigation_demographics" in missing:
        write_chart("nis33__land_use_irrigation_demographics",
                    rows_from_citation_series(cia_nis33, row_filter=cat_in(
                        ["Land Use", "Demographics & Population"])))
    if "nis33__crop_livestock_production_opium" in missing:
        write_chart("nis33__crop_livestock_production_opium",
                    rows_from_citation_series(cia_nis33, row_filter=cat_eq("Agriculture")))
    if "nis33__oil_production_export_destination" in missing:
        # Full 'Oil production & trade' category (183 rows). The sibling
        # nis33__petroleum_revenue_series_1959_71 chart (out of this task's 56-chart scope,
        # status=extends in the registry) actually draws from the separate 'Government
        # Finance' category's 'Revenue from the petroleum sector' / 'Figure 28' subcategories
        # (verified directly against the file), NOT from 'Oil production & trade' as the
        # staging script's own underlying_codes comment guessed -- so there is no real overlap
        # to subtract here despite that comment; using the full category is correct and drops
        # nothing that actually belongs to the other chart.
        write_chart("nis33__oil_production_export_destination",
                    rows_from_citation_series(cia_nis33, row_filter=cat_eq("Oil production & trade")))
    if "nis33__manufactured_goods_output" in missing:
        write_chart("nis33__manufactured_goods_output",
                    rows_from_citation_series(cia_nis33, row_filter=cat_eq("Manufacturing")))
    if "nis33__trade_by_commodity_and_partner" in missing:
        write_chart("nis33__trade_by_commodity_and_partner",
                    rows_from_citation_series(cia_nis33, row_filter=cat_eq("Trade")))
    if "nis33__external_debt_investment_fx" in missing:
        write_chart("nis33__external_debt_investment_fx",
                    rows_from_citation_series(cia_nis33, row_filter=cat_in(
                        ["External debt", "Foreign investment", "Foreign exchange"])))
    if "nis33__macro_national_accounts" in missing:
        write_chart("nis33__macro_national_accounts",
                    rows_from_citation_series(cia_nis33, row_filter=cat_eq("Macro / National Accounts")))

    # --- USAID Point Four RAC secondary-research reports (2 academic sources, filtered by
    # author surname in the row's own `citation` field -- this file has no separate per-
    # author source_dataset tag, both rows share source_dataset=usaid-point-four-rac-
    # research-reports) ---
    if "usaid_pt4__ford_foundation_harvard_advisory_group" in missing:
        write_chart("usaid_pt4__ford_foundation_harvard_advisory_group",
                    rows_from_citation_series(usaid, row_filter=lambda r: "Brew" in r.get("citation", "")))
    if "usaid_pt4__motheral_report_land_reform" in missing:
        write_chart("usaid_pt4__motheral_report_land_reform",
                    rows_from_citation_series(usaid, row_filter=lambda r: "Roush" in r.get("citation", "")))

    # --- IMF Article IV 2015/2018 (only 2 of the staging script's 10 rows are in this
    # task's 56-chart scope; the other 8 are status=extends, out of scope) ---
    if "imf_a4__foreign_exchange_2015_2018" in missing:
        write_chart("imf_a4__foreign_exchange_2015_2018",
                    rows_from_citation_series(imf, row_filter=cat_eq("Foreign exchange")))
    if "imf_a4__oil_production_trade_2015_2018" in missing:
        write_chart("imf_a4__oil_production_trade_2015_2018",
                    rows_from_citation_series(imf, row_filter=cat_eq("Oil production & trade")))


group23_us_primary_source_archives()
log(f"After group 23: built={STATS['built']} skipped={STATS['skipped']} rows={STATS['rows_total']}")

# ============================================================================
# GROUP 24 (round 2, 2026-07-13): Iran institutional/modernization/culture archival --
# aviation history, pre-1979 foreign concessions, Iran Data Portal employment/housing deep
# series, media history (cinema/film/press), telecom history (post/telegraph/radio-TV),
# White Revolution corps, World Bank poverty & equity, and specialty goods (carpets,
# caviar, tobacco, Trans-Iranian Railway financing -- incl. the flagship carpet-export
# chart). Most source files share one narrow schema: year,metric,value,unit,source,
# [notes,]country_iso3[,value_usd_nominal,value_usd_real_2015,currency_conversion_note] --
# a handful (radio/TV has a `medium` prefix column; the two White Revolution corps files use
# period_start/period_end instead of a single year; automotive JVs, the D'Arcy concession,
# and the two Iran Data Portal wide-employment files, plus WB poverty and housing, are
# bespoke enough to write directly rather than force through the generic helper).
# ============================================================================

def rows_from_metric_series(records, source_dataset, country_iso3="IRN",
                             year_field="year", label_field="metric", label_prefix_field=None,
                             notes_field="notes", source_field="source"):
    """Generic loader for the year/metric/value/unit/source[/notes]/country_iso3[/USD-variant]
    schema shared by the aviation, media-history, telecom-history, White-Revolution-extension,
    and specialty-goods archival files. The row's own free-text `source` citation is folded
    into notes as `[source: ...]` (mirrors the convention already used in group4's banking-
    history rows) since these folders don't carry a separate short source_dataset slug column
    of their own -- source_dataset here is the fixed project-level slug from the registry's
    primary_source field, passed in by the caller."""
    out = []
    for r in records:
        label = r.get(label_field, "")
        if label_prefix_field and r.get(label_prefix_field):
            label = f"{r[label_prefix_field]} — {label}"
        vcode = slugify(label)
        ciso = r.get("country_iso3") or country_iso3
        yr = r.get(year_field, "")
        has_usd = bool(r.get("value_usd_nominal") or r.get("value_usd_real_2015"))
        note_parts = []
        if notes_field and r.get(notes_field):
            note_parts.append(r[notes_field])
        if not has_usd and r.get("currency_conversion_note"):
            note_parts.append(f"[{r['currency_conversion_note']}]")
        if source_field and r.get(source_field):
            note_parts.append(f"[source: {r[source_field]}]")
        notes = " ".join(note_parts) if note_parts else None
        out.append(base_row(ciso, yr, r.get("value", ""), r.get("unit", ""), vcode, label,
                             source_dataset, notes=notes, computed=False if has_usd else None))
        if r.get("value_usd_nominal"):
            out.append(base_row(ciso, yr, r["value_usd_nominal"], "current US$ (computed)",
                                 vcode + ".USD_NOMINAL", label + " (computed, nominal US$)",
                                 source_dataset, computed=True,
                                 notes=r.get("currency_conversion_note", "")))
        if r.get("value_usd_real_2015"):
            out.append(base_row(ciso, yr, r["value_usd_real_2015"], "constant 2015 US$ (computed)",
                                 vcode + ".USD_REAL_2015", label + " (computed, real 2015 US$)",
                                 source_dataset, computed=True,
                                 notes=r.get("currency_conversion_note", "")))
    return out


def group24_institutional_modernization_specialty():
    if "iran_aviation__events_fleet_workforce_1952_1988" in missing:
        recs = load_csv(os.path.join(PROC, "iran_aviation_history_series", "aviation_events_and_fleet.csv"))
        write_chart("iran_aviation__events_fleet_workforce_1952_1988",
                    rows_from_metric_series(recs, "iran-aviation-history:iranica-aviation-history"))

    # --- pre-1979 foreign concessions ---
    d_conc = os.path.join(PROC, "iran_foreign_concessions_series")

    if "iran_concessions__darcy_oil_1901_terms" in missing:
        recs = load_csv(os.path.join(d_conc, "darcy_oil_concession_1901_terms.csv"))
        sd = "iran-foreign-concessions-pre1979:darcy-concession-1901-terms"
        rows = []
        for r in recs:
            term = r.get("term", "")
            label = term.replace("_", " ")
            # single 1901 contract's terms (not a time series, per the registry's own
            # framing) except the 6 "successor_agreement_1933_..." rows, which describe the
            # 1933 renegotiation explicitly named in the term itself -- grounded in the
            # source's own field name, not guessed.
            yr = 1933 if "1933" in term else 1901
            has_usd = bool(r.get("value_usd_nominal") or r.get("value_usd_real_2015"))
            note_parts = []
            if r.get("notes"):
                note_parts.append(r["notes"])
            if not has_usd and r.get("currency_conversion_note"):
                note_parts.append(f"[{r['currency_conversion_note']}]")
            rows.append(base_row("IRN", yr, r.get("value", ""), r.get("unit", ""), slugify(label), label, sd,
                                  notes=" ".join(note_parts) if note_parts else None,
                                  computed=False if has_usd else None))
            if r.get("value_usd_nominal"):
                rows.append(base_row("IRN", yr, r["value_usd_nominal"], "current US$ (computed)",
                                      slugify(label) + ".USD_NOMINAL", label + " (computed, nominal US$)", sd,
                                      computed=True, notes=r.get("currency_conversion_note", "")))
            if r.get("value_usd_real_2015"):
                rows.append(base_row("IRN", yr, r["value_usd_real_2015"], "constant 2015 US$ (computed)",
                                      slugify(label) + ".USD_REAL_2015", label + " (computed, real 2015 US$)", sd,
                                      computed=True, notes=r.get("currency_conversion_note", "")))
        write_chart("iran_concessions__darcy_oil_1901_terms", rows)

    if "iran_concessions__automotive_joint_ventures_1956_1979" in missing:
        recs = load_csv(os.path.join(d_conc, "automotive_joint_ventures_1956_1979.csv"))
        rows = []
        for r in recs:
            label = r.get("venture_name", "")
            sy = r.get("start_year", "")
            yr = leading_year(sy)
            note = (f"Foreign partner: {r.get('foreign_partner','')} ({r.get('foreign_partner_country','')}); "
                    f"Iranian partner: {r.get('iranian_partner','')}; ends/status: "
                    f"{r.get('end_year_or_status','')}; {r.get('notes','')} [source: {r.get('source','')}]")
            rows.append(base_row("IRN", yr, "", "", slugify(label), label,
                                  "iran-foreign-concessions-pre1979:automotive-joint-ventures-1956-1979",
                                  original_period_label=sy if sy and str(yr) != sy else None,
                                  notes=note))
        write_chart("iran_concessions__automotive_joint_ventures_1956_1979", rows)

    # --- Iran Data Portal deep series (employment + housing) ---
    d_idp = os.path.join(PROC, "iran_data_portal_deep_series")

    if "iran_data_portal__employment_by_gender_1966_2011" in missing:
        recs = load_csv(os.path.join(d_idp, "employment_by_gender_1966_2011.csv"))
        value_fields = {"employed_male": "persons", "employed_female": "persons",
                         "employed_total": "persons", "female_share_pct": "percent"}
        rows = []
        for r in recs:
            yr = fiscal_range_to_later_year(r.get("year_western", "")) or leading_year(r.get("year_western", ""))
            for vf, unit in value_fields.items():
                if r.get(vf) in (None, ""):
                    continue
                label = vf.replace("_", " ")
                rows.append(base_row("IRN", yr, r[vf], unit, slugify(label), label, "iran-data-portal",
                                      original_period_label=r.get("year_iranian", "")))
        write_chart("iran_data_portal__employment_by_gender_1966_2011", rows)

    if "iran_data_portal__employment_by_sector_1956_2011" in missing:
        recs = load_csv(os.path.join(d_idp, "employment_by_sector_1956_2011.csv"))
        SECTOR_FIELDS = ["agriculture", "oil", "mining", "industry", "water_electricity_gas",
                          "construction", "transport_storage", "communication",
                          "trade_hotels_restaurants", "services_financial", "services_real_estate",
                          "services_public_social", "uncategorized", "total"]
        rows = []
        for r in recs:
            yr = fiscal_range_to_later_year(r.get("year_western", "")) or leading_year(r.get("year_western", ""))
            for vf in SECTOR_FIELDS:
                if r.get(vf) in (None, ""):
                    continue
                label = "Total employment (all sectors)" if vf == "total" else vf.replace("_", " ").title()
                rows.append(base_row("IRN", yr, r[vf], "persons", slugify(label), label, "iran-data-portal",
                                      original_period_label=r.get("year_iranian", "")))
        write_chart("iran_data_portal__employment_by_sector_1956_2011", rows)

    if "iran_data_portal__housing_units_by_household_size_1966_2006" in missing:
        recs = load_csv(os.path.join(d_idp, "housing_units_by_household_census_1966_2006.csv"))
        FIELD_LABELS = {"total_housing_units": "Total housing units",
                         "1_household": "Housing units with 1 resident household",
                         "2_households": "Housing units with 2 resident households",
                         "3_households": "Housing units with 3 resident households",
                         "4plus_households": "Housing units with 4+ resident households"}
        rows = []
        for r in recs:
            lbl_raw = r.get("census_year_label", "").strip()
            m = re.search(r"\((\d{4})\)", lbl_raw)
            yr = int(m.group(1)) if m else ""
            for vf, label in FIELD_LABELS.items():
                if not r.get(vf):
                    continue
                rows.append(base_row("IRN", yr, r[vf], "housing units", slugify(label), label,
                                      "iran-data-portal", original_period_label=lbl_raw))
        write_chart("iran_data_portal__housing_units_by_household_size_1966_2006", rows)

    # --- media history ---
    d_media = os.path.join(PROC, "iran_media_history_series")

    if "iran_media__cinema_theaters_attendance_1932_1986" in missing:
        recs = load_csv(os.path.join(d_media, "cinema_theaters_and_attendance.csv"))
        write_chart("iran_media__cinema_theaters_attendance_1932_1986",
                    rows_from_metric_series(recs, "iran-media-history:iranica-cinema-history"))
    if "iran_media__film_production_industry_1941_1982" in missing:
        recs = load_csv(os.path.join(d_media, "film_production_and_industry.csv"))
        write_chart("iran_media__film_production_industry_1941_1982",
                    rows_from_metric_series(recs, "iran-media-history:iranica-cinema-history"))
    if "iran_media__press_periodicals_1898_1988" in missing:
        recs = load_csv(os.path.join(d_media, "press_periodicals_series.csv"))
        write_chart("iran_media__press_periodicals_1898_1988",
                    rows_from_metric_series(recs, "iran-media-history:iranica-press-newspapers"))

    # --- telecom history ---
    d_tel = os.path.join(PROC, "iran_telecom_communications_series")

    if "iran_telecom__postal_service_1913_1989" in missing:
        recs = load_csv(os.path.join(d_tel, "postal_service_series.csv"))
        write_chart("iran_telecom__postal_service_1913_1989",
                    rows_from_metric_series(recs, "iran-telecom-history:iranica-communications-in-persia"))
    if "iran_telecom__telegraph_offices_1914_1989" in missing:
        recs = load_csv(os.path.join(d_tel, "telegraph_offices.csv"))
        write_chart("iran_telecom__telegraph_offices_1914_1989",
                    rows_from_metric_series(recs, "iran-telecom-history:iranica-communications-in-persia"))
    if "iran_telecom__radio_tv_ownership_1940_1989" in missing:
        recs = load_csv(os.path.join(d_tel, "radio_tv_series.csv"))
        write_chart("iran_telecom__radio_tv_ownership_1940_1989",
                    rows_from_metric_series(recs, "iran-telecom-history:iranica-communications-in-persia",
                                             label_prefix_field="medium"))

    # --- White Revolution corps ---
    d_wr = os.path.join(PROC, "iran_white_revolution_corps_series")

    if "white_revolution__extension_corps_stats_1964_1965" in missing:
        recs = load_csv(os.path.join(d_wr, "extension_corps_stats.csv"))
        write_chart("white_revolution__extension_corps_stats_1964_1965",
                    rows_from_metric_series(recs, "iran-white-revolution-corps:gfras-extension-development-corps"))

    if "white_revolution__literacy_corps_program_totals_1963_1979" in missing:
        recs = load_csv(os.path.join(d_wr, "literacy_corps_program_totals.csv"))
        sd = "iran-white-revolution-corps:iranica-literacy-corps"
        rows = []
        for r in recs:
            label = r.get("metric", "").replace("_", " ")
            ps, pe = r.get("period_start", ""), r.get("period_end", "")
            yr = ps
            opl = f"{ps}-{pe}" if pe and pe != ps else None
            has_usd = bool(r.get("value_usd_nominal") or r.get("value_usd_real_2015"))
            note_parts = []
            if r.get("notes"):
                note_parts.append(r["notes"])
            if not has_usd and r.get("currency_conversion_note"):
                note_parts.append(f"[{r['currency_conversion_note']}]")
            if r.get("source"):
                note_parts.append(f"[source: {r['source']}]")
            rows.append(base_row("IRN", yr, r.get("value", ""), r.get("unit", ""), slugify(label), label, sd,
                                  original_period_label=opl, computed=False if has_usd else None,
                                  notes=" ".join(note_parts) if note_parts else None))
            if r.get("value_usd_nominal"):
                rows.append(base_row("IRN", yr, r["value_usd_nominal"], "current US$ (computed)",
                                      slugify(label) + ".USD_NOMINAL", label + " (computed, nominal US$)", sd,
                                      original_period_label=opl, computed=True,
                                      notes=r.get("currency_conversion_note", "")))
            if r.get("value_usd_real_2015"):
                rows.append(base_row("IRN", yr, r["value_usd_real_2015"], "constant 2015 US$ (computed)",
                                      slugify(label) + ".USD_REAL_2015", label + " (computed, real 2015 US$)", sd,
                                      original_period_label=opl, computed=True,
                                      notes=r.get("currency_conversion_note", "")))
        write_chart("white_revolution__literacy_corps_program_totals_1963_1979", rows)

    if "white_revolution__corps_stats_bundle_1963_1978" in missing:
        recs = load_csv(os.path.join(d_wr, "white_revolution_corps_stats.csv"))
        sd = "iran-white-revolution-corps:wikipedia-white-revolution-corps-stats"
        rows = []
        for r in recs:
            label = f"{r.get('corps','')} — {r.get('metric','').replace('_',' ')}"
            ps, pe = r.get("period_start", ""), r.get("period_end", "")
            yr = ps
            opl = f"{ps}-{pe}" if pe and pe != ps else None
            rows.append(base_row("IRN", yr, r.get("value", ""), r.get("unit", ""), slugify(label), label, sd,
                                  original_period_label=opl, notes=f"[source: {r.get('source','')}]"))
        write_chart("white_revolution__corps_stats_bundle_1963_1978", rows)

    # --- World Bank poverty & equity ---
    if "wb_poverty__iran_poverty_rate_by_region_2011_2020" in missing:
        recs = load_csv(os.path.join(PROC, "worldbank_poverty_equity", "iran_poverty_rate_by_region_2011_2020.csv"))
        sd = "worldbank-poverty-equity-iran-poverty-assessment-2023"
        rows = []
        for r in recs:
            region = r.get("region", "")
            for yr_field, yr in [("poverty_rate_2011_percent", 2011), ("poverty_rate_2020_percent", 2020)]:
                if not r.get(yr_field):
                    continue
                label = f"{region} — poverty rate"
                rows.append(base_row("IRN", yr, r[yr_field], "percent", slugify(label), label, sd))
            if r.get("percentage_point_change"):
                label = f"{region} — poverty rate change, 2011-2020"
                rows.append(base_row("IRN", "", r["percentage_point_change"], "percentage points",
                                      slugify(label), label, sd, original_period_label="2011-2020"))
        write_chart("wb_poverty__iran_poverty_rate_by_region_2011_2020", rows)

    # --- specialty goods: carpets (the flagship chart), caviar, tobacco, railway financing ---
    d_sg = os.path.join(PROC, "specialty_goods_series")

    if "specialty_goods__carpet_export_value_1960_2024" in missing:
        # two source files (state-monopoly era 1960-1988, post-liberalization 1994-2024)
        # concatenated into one chart per the registry's own underlying_codes
        # ("...1960_1988.csv|...post1990.csv") -- same chart concept (carpet export value),
        # same metric-series schema in both files, just a 6-year sourcing gap (1989-1993)
        # between them that is a genuine, not fabricated, data gap.
        rows = rows_from_metric_series(load_csv(os.path.join(d_sg, "carpet_exports_1960_1988.csv")),
                                        "iran-carpet-exports")
        rows += rows_from_metric_series(load_csv(os.path.join(d_sg, "carpet_exports_post1990.csv")),
                                         "iran-carpet-exports")
        write_chart("specialty_goods__carpet_export_value_1960_2024", rows)

    if "specialty_goods__caviar_shilat_production_2013_2024" in missing:
        recs = load_csv(os.path.join(d_sg, "caviar_shilat_production_2013_2024.csv"))
        write_chart("specialty_goods__caviar_shilat_production_2013_2024",
                    rows_from_metric_series(recs, "iran-caviar-exports:ifo-caviar-production-export-compiled"))

    if "specialty_goods__caviar_sturgeon_aquaculture_2010_2018" in missing:
        recs = load_csv(os.path.join(d_sg, "caviar_sturgeon_aquaculture_eumofa_2010_2018.csv"))
        write_chart("specialty_goods__caviar_sturgeon_aquaculture_2010_2018",
                    rows_from_metric_series(recs, "iran-caviar-exports:eumofa-caviar-market-report-2021"))

    if "specialty_goods__tobacco_monopoly_1890_1995" in missing:
        recs = load_csv(os.path.join(d_sg, "tobacco_monopoly_1890_1995.csv"))
        write_chart("specialty_goods__tobacco_monopoly_1890_1995",
                    rows_from_metric_series(
                        recs, "iran-tobacco-monopoly:iranica-tobacco-monopoly-narrative-series-1890-1995"))

    if "specialty_goods__tobacco_post_privatization_2018" in missing:
        recs = load_csv(os.path.join(d_sg, "tobacco_post_privatization_2018.csv"))
        write_chart("specialty_goods__tobacco_post_privatization_2018",
                    rows_from_metric_series(recs, "iran-tobacco-monopoly:tobacco-market-post-privatization-2018"))

    if "specialty_goods__trans_iranian_railway_financing_1938_39" in missing:
        recs = load_csv(os.path.join(d_sg, "trans_iranian_railway_financing_context.csv"))
        write_chart("specialty_goods__trans_iranian_railway_financing_1938_39",
                    rows_from_metric_series(recs, "iran-sugar-tea-history:trans-iranian-railway-financing-context"))


group24_institutional_modernization_specialty()
log(f"After group 24: built={STATS['built']} skipped={STATS['skipped']} rows={STATS['rows_total']}")

# ============================================================================
# METADATA SYNC: every group*() function above is gated on `if cid not in missing: continue`,
# so a chart_id that already has a data/charts/ folder never gets write_chart() called for it
# again even if CHART_REGISTRY.csv's title/category/primary_source/citations_json later changed
# for that row -- despite this module's own docstring claiming "safely re-run (idempotent
# overwrite per chart_id)". Found 2026-07-13 when a title-cleanup pass edited 51 registry rows
# and re-running this script reported built=0, silently leaving the old titles in meta.json.
# Re-deriving data.csv for an existing chart_id would mean re-invoking that one chart's specific
# group function, which isn't safe to do generically here -- so this pass only re-syncs the four
# registry-derived meta.json fields (title, category, sources, citations), never data.csv or the
# rows-derived fields (n_rows/year_range/countries), for every already-built chart_id.
# ============================================================================


def sync_existing_metadata():
    synced = 0
    for cid, reg in REG.items():
        if cid in missing or cid in CASE_COLLISION_RESOLVED:
            continue
        folder = os.path.join(OUT_DIR, cid.replace("/", "_"))
        meta_path = os.path.join(folder, "meta.json")
        if not os.path.isfile(meta_path):
            continue
        with open(meta_path, encoding="utf-8") as f:
            meta = json.load(f)
        citations = []
        if reg.get("citations_json"):
            try:
                citations = json.loads(reg["citations_json"])
            except json.JSONDecodeError:
                citations = []
        new_fields = {
            "title": reg["title"],
            "category": reg["category"],
            "sources": reg["primary_source"],
            "citations": citations,
        }
        if any(meta.get(k) != v for k, v in new_fields.items()):
            meta.update(new_fields)
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2, ensure_ascii=False)
                f.write("\n")
            synced += 1
    log(f"Metadata sync: refreshed title/category/sources/citations for {synced} already-built chart_ids")


sync_existing_metadata()

log("=" * 70)
log(f"FINAL: built={STATS['built']} skipped={STATS['skipped']} total_rows={STATS['rows_total']}")
if SKIPPED:
    log(f"Skipped chart_ids: {SKIPPED}")
still_missing = sorted(cid for cid in REG if cid.replace('/', '_') not in set(os.listdir(OUT_DIR))
                        and cid not in CASE_COLLISION_RESOLVED)
log(f"Registry rows still without a data/charts/ folder after this run: {len(still_missing)}")
if still_missing:
    log(f"  {still_missing}")
