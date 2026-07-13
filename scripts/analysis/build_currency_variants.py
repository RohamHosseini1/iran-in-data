"""Compute real (2015-base, inflation-adjusted) and nominal USD variants for every currency
chart, per docs/bookkeeping.md 'Currency & inflation-adjustment conventions'. Never overwrites
a recorded raw value -- only appends new variant rows/columns, always tagged computed=true
(or a `*_usd_nominal`/`*_usd_real_2015` column pair alongside the untouched original) with the
exact FX/CPI series used, so it's auditable.

UPDATE 2026-07-13: extended from Iran-only to all 17 countries in this project.
  - Part A (process_wdi) now loops every WDI chart row's own country_iso3 against that country's
    own FX/CPI lookup (data/processed/fx_cpi_lookup_<iso3>.json, built by build_fx_cpi_lookup.py's
    main_comparators()), instead of hardcoding IRN. 14 of the 16 comparators use WDI's official
    PA.NUS.FCRF/FP.CPI.TOTL outright; Venezuela and Argentina get a parallel/black-market-preferred
    rate for their documented divergence eras, mirroring Iran's own post-1979 treatment.
  - Part B (process_archival) gained several new rial-denominated Iran archival schemas beyond the
    original category/subcategory/value/unit pattern: revenue_rials/expenditure_rials pairs,
    bespoke single/multi rial-or-toman-named columns with non-"year" date columns (fiscal_year_ah,
    year_sh, period_start, a dual "1953/54" format, or no date column at all), and a dedicated
    pass for iran_insurance_series's many *_million_irr columns. Also fixes a latent bug in the
    original code: toman-denominated values (1 toman = 10 rials) were never scaled before being
    divided by the rial-per-USD FX rate -- harmless for the original 3 folders (no toman units
    there) but would have silently under-converted by 10x for the new toman-denominated files.
  Archival conversion remains Iran-only -- rial-denominated data is inherently Iran-specific in
  this project. See logs/downloads/currency-extension-comparators-archival.log for the full
  reconnaissance behind every folder/file added and every explicit exclusion decision.
"""
import csv
import json
import os

with open("data/processed/fx_cpi_lookup_irn.json", encoding="utf-8") as f:
    LOOKUP = json.load(f)
FX = {int(y): v for y, v in LOOKUP["fx_rate_rials_per_usd"].items()}
CPI = {int(y): v for y, v in LOOKUP["cpi_index_2015_base100"].items()}
BASE_YEAR = 2015


def real_usd_from_usd(nominal_usd, year, fx=FX, cpi=CPI):
    """Convert a nominal-USD value in `year` to real (2015-base) USD, per the documented
    'deflate in local currency first, then convert at base-year rate' methodology -- expanded
    algebraically so it also works starting from a USD value: LCU_y = usd*FX_y;
    real_LCU = LCU_y * CPI_2015/CPI_y; real_usd = real_LCU / FX_2015. `fx`/`cpi` default to Iran's
    own lookup for backward compatibility; Part A passes each row's own country's lookup."""
    if year not in fx or year not in cpi or BASE_YEAR not in fx or BASE_YEAR not in cpi:
        return None
    lcu_y = nominal_usd * fx[year]
    real_lcu = lcu_y * (cpi[BASE_YEAR] / cpi[year])
    return real_lcu / fx[BASE_YEAR]


def real_usd_from_lcu(nominal_lcu, year, fx=FX, cpi=CPI):
    if year not in fx or year not in cpi or BASE_YEAR not in fx or BASE_YEAR not in cpi:
        return None
    real_lcu = nominal_lcu * (cpi[BASE_YEAR] / cpi[year])
    return real_lcu / fx[BASE_YEAR]


def nominal_usd_from_lcu(nominal_lcu, year, fx=FX):
    if year not in fx:
        return None
    return nominal_lcu / fx[year]


# ============================================================================================
# Part A: WDI charts with a current-USD (.CD) variant but no constant-USD (.KD) -- ALL countries
# ============================================================================================
ALL_COUNTRIES = ["IRN", "KOR", "TUR", "SAU", "VEN", "USA", "RUS", "ARG", "ESP",
                  "PRT", "GRC", "DEU", "FRA", "GBR", "ITA", "NLD", "SWE"]


def _load_country_lookup(iso3):
    """Returns (fx_dict, cpi_dict) for a country, or (None, None) if no lookup file exists yet
    (e.g. build_fx_cpi_lookup.py's main_comparators() hasn't been run). IRN uses the module-level
    FX/CPI already loaded above (unchanged file/schema) rather than re-reading its own JSON under
    the comparators' generic key names."""
    if iso3 == "IRN":
        return FX, CPI
    path = f"data/processed/fx_cpi_lookup_{iso3.lower()}.json"
    if not os.path.exists(path):
        return None, None
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    fx = {int(y): v for y, v in d.get("fx_rate_lcu_per_usd", {}).items()}
    cpi = {int(y): v for y, v in d.get("cpi_index_2015_base100", {}).items()}
    return fx, cpi


COUNTRY_LOOKUPS = {}
for _c in ALL_COUNTRIES:
    _fx, _cpi = _load_country_lookup(_c)
    if _fx:
        COUNTRY_LOOKUPS[_c] = (_fx, _cpi)


def process_wdi():
    with open("data/processed/CHART_REGISTRY.csv", newline="", encoding="utf-8") as f:
        registry = list(csv.DictReader(f))

    targets = []
    for r in registry:
        if not r["chart_id"].startswith("wdi__"):
            continue
        codes = r["underlying_codes"].split("|")
        has_cd = any(c.endswith(".CD") for c in codes)
        has_kd = any(c.endswith(".KD") for c in codes)
        if has_cd and not has_kd:
            targets.append(r["chart_id"])

    print(f"WDI charts needing a computed real-USD variant: {len(targets)}")
    print(f"Countries with an FX/CPI lookup available: {sorted(COUNTRY_LOOKUPS)}")
    updated = 0
    countries_touched = set()
    for cid in targets:
        folder = cid.replace("/", "_")
        data_path = f"data/charts/{folder}/data.csv"
        meta_path = f"data/charts/{folder}/meta.json"
        if not os.path.exists(data_path):
            continue
        with open(data_path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
            fieldnames = list(rows[0].keys()) if rows else []
        if "computed" not in fieldnames:
            fieldnames = fieldnames + ["computed"]
        # idempotency: drop any previously-computed rows before recomputing, so re-running this
        # script (e.g. after the FX methodology correction, or after adding more countries) never
        # duplicates or leaves stale rows
        rows = [r for r in rows if not r.get("variant_code", "").endswith(".COMPUTED_REAL_2015USD")]

        new_rows = []
        for row in rows:
            iso3 = row.get("country_iso3")
            if iso3 not in COUNTRY_LOOKUPS:
                continue
            if not row.get("variant_code", "").endswith(".CD"):
                continue
            try:
                year = int(row["year"])
                val = float(row["value"])
            except (ValueError, TypeError):
                continue
            fx, cpi = COUNTRY_LOOKUPS[iso3]
            real = real_usd_from_usd(val, year, fx, cpi)
            if real is None:
                continue
            new_row = dict(row)
            new_row["value"] = str(round(real, 4))
            new_row["variant_code"] = row["variant_code"].replace(".CD", ".COMPUTED_REAL_2015USD")
            new_row["variant_label"] = (row.get("variant_label", "") + " (computed real, 2015 US$)").strip()
            new_row["unit"] = "constant 2015 US$ (computed)"
            new_row["computed"] = "true"
            new_rows.append(new_row)
            countries_touched.add(iso3)

        if not new_rows:
            continue
        for row in rows:
            row.setdefault("computed", "false")
        rows.extend(new_rows)
        with open(data_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)

        if os.path.exists(meta_path):
            with open(meta_path, encoding="utf-8") as f:
                meta = json.load(f)
            meta["currency_display"] = {
                "has_currency_toggle": True,
                "default_variant_suffix": ".COMPUTED_REAL_2015USD",
                "nominal_variant_suffix": ".CD",
                "note": "Real variant computed by this project (not WDI-native) using each "
                        "country's own FX rate + CPI, base year 2015. Iran: parallel/black-market "
                        "rate for 1979-present. Venezuela/Argentina: parallel/black-market rate for "
                        "their own documented official-vs-parallel divergence eras. All other "
                        "countries: WDI official PA.NUS.FCRF (no known equivalent divergence). See "
                        "docs/bookkeeping.md and data/processed/fx_cpi_lookup_<iso3>.json.",
            }
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2, ensure_ascii=False)
        updated += 1
    print(f"WDI charts updated with a computed real-USD variant: {updated}")
    print(f"Countries with at least one computed real-USD row written: {sorted(countries_touched)}")


# ============================================================================================
# Part A2: WDI charts with a current-LCU (.CN) variant but WDI never published a matching
# current-USD (.CD) variant at all (mostly government-finance/fiscal aggregates, e.g.
# GC.REV.XGRT -- "Revenue, excluding grants" -- 25 such charts, added 2026-07-13, task #18).
# Part A above starts from WDI's own .CD row and computes a REAL variant from it; here there is
# no USD row to start from at all, so both a nominal-USD AND a real-USD variant are computed
# directly from the LCU value, reusing the same nominal_usd_from_lcu/real_usd_from_lcu helpers
# Part B already uses for Iran's rial-denominated archival series.
# ============================================================================================

def process_wdi_lcu_only():
    with open("data/processed/CHART_REGISTRY.csv", newline="", encoding="utf-8") as f:
        registry = list(csv.DictReader(f))

    targets = []
    for r in registry:
        if not r["chart_id"].startswith("wdi__"):
            continue
        codes = r["underlying_codes"].split("|")
        has_cd = any(c.endswith(".CD") for c in codes)
        has_cn = any(c.endswith(".CN") for c in codes)
        if has_cn and not has_cd:
            targets.append(r["chart_id"])

    print(f"WDI charts with LCU-only (no native .CD variant): {len(targets)}")
    updated = 0
    countries_touched = set()
    for cid in targets:
        folder = cid.replace("/", "_")
        data_path = f"data/charts/{folder}/data.csv"
        meta_path = f"data/charts/{folder}/meta.json"
        if not os.path.exists(data_path):
            continue
        with open(data_path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
            fieldnames = list(rows[0].keys()) if rows else []
        if "computed" not in fieldnames:
            fieldnames = fieldnames + ["computed"]
        # idempotency: drop any previously-computed rows before recomputing (same pattern as Part A)
        rows = [r for r in rows
                if not (r.get("variant_code", "").endswith(".COMPUTED_NOMINAL_USD")
                        or r.get("variant_code", "").endswith(".COMPUTED_REAL_2015USD"))]

        new_rows = []
        for row in rows:
            iso3 = row.get("country_iso3")
            if iso3 not in COUNTRY_LOOKUPS:
                continue
            if not row.get("variant_code", "").endswith(".CN"):
                continue
            try:
                year = int(row["year"])
                val = float(row["value"])
            except (ValueError, TypeError):
                continue
            fx, cpi = COUNTRY_LOOKUPS[iso3]
            nominal = nominal_usd_from_lcu(val, year, fx)
            real = real_usd_from_lcu(val, year, fx, cpi)
            base_code = row["variant_code"][:-3]  # strip ".CN"
            if nominal is not None:
                nrow = dict(row)
                nrow["value"] = str(round(nominal, 4))
                nrow["variant_code"] = base_code + ".COMPUTED_NOMINAL_USD"
                nrow["variant_label"] = (row.get("variant_label", "") + " (computed nominal, US$)").strip()
                nrow["unit"] = "current US$ (computed)"
                nrow["computed"] = "true"
                new_rows.append(nrow)
            if real is not None:
                rrow = dict(row)
                rrow["value"] = str(round(real, 4))
                rrow["variant_code"] = base_code + ".COMPUTED_REAL_2015USD"
                rrow["variant_label"] = (row.get("variant_label", "") + " (computed real, 2015 US$)").strip()
                rrow["unit"] = "constant 2015 US$ (computed)"
                rrow["computed"] = "true"
                new_rows.append(rrow)
            if nominal is not None or real is not None:
                countries_touched.add(iso3)

        if not new_rows:
            continue
        for row in rows:
            row.setdefault("computed", "false")
        rows.extend(new_rows)
        with open(data_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)

        if os.path.exists(meta_path):
            with open(meta_path, encoding="utf-8") as f:
                meta = json.load(f)
            meta["currency_display"] = {
                "has_currency_toggle": True,
                "default_variant_suffix": ".COMPUTED_REAL_2015USD",
                "nominal_variant_suffix": ".COMPUTED_NOMINAL_USD",
                "note": "WDI never published a current-USD variant of this indicator (LCU-only). "
                        "Both nominal and real (2015-base) USD variants are computed by this "
                        "project from the LCU value using each country's own FX rate + CPI. "
                        "Iran: parallel/black-market rate for 1979-present. Venezuela/Argentina: "
                        "parallel/black-market rate for their own documented divergence eras. All "
                        "other countries: WDI official PA.NUS.FCRF. See docs/bookkeeping.md and "
                        "data/processed/fx_cpi_lookup_<iso3>.json.",
            }
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2, ensure_ascii=False)
        updated += 1
    print(f"LCU-only WDI charts updated with computed nominal+real USD variants: {updated}")
    print(f"Countries with at least one computed row written: {sorted(countries_touched)}")


# ============================================================================================
# Part B: archival Iran-rial series (Iran-only -- rial-denominated data is inherently Iran-
# specific in this project). Two sub-patterns: (1) folders sharing a generic value/unit/year
# column pattern, handled by process_archival(); (2) bespoke schemas, handled by
# process_custom_jobs() and process_insurance_series().
# ============================================================================================
RIAL_MARKERS = ["rial", "rls", "toman"]
# Unit strings that describe an EXCHANGE RATE (e.g. "rials/USD"), not a monetary stock/flow value.
# Dividing a rate by another rate is meaningless -- these are deliberately left unconverted.
RATE_UNIT_MARKERS = ["/usd", "/us$", "per usd", "per us$"]


def _unit_is_rial(unit):
    u = (unit or "").lower()
    return any(m in u for m in RIAL_MARKERS)


def _unit_is_rate_not_value(unit):
    u = (unit or "").lower()
    return any(m in u for m in RATE_UNIT_MARKERS)


def _to_rial_equivalent(value, unit):
    """1 toman = 10 rials. Scales a toman-denominated value up to its rial equivalent before FX
    conversion, since Iran's own FX/CPI lookup is rial-per-USD. Values already stated in rials
    (or any unit not mentioning toman) pass through unchanged. Bookkeeping.md's own words: 'Getting
    this wrong silently produces a value off by exactly 10x' -- the ORIGINAL version of this
    function (this file, pre-2026-07-13 extension) didn't do this scaling at all; harmless then
    because none of the 3 original archival folders had toman-denominated rows, but several of the
    newly-added ones do (e.g. majlis ministry_level_appropriations_1301.csv, entirely in tomans)."""
    u = (unit or "").lower()
    if "toman" in u and "rial" not in u:
        return value * 10.0
    return value


def _convert_lcu_value(val, year, unit):
    """Shared Iran rial/toman -> nominal & real USD conversion core, used by every archival
    schema handler below. Returns (nominal_usd_or_None, real_usd_or_None, note_str). Caller is
    expected to have already checked _unit_is_rial(unit) before calling (this function does not
    re-check that, only the rate-vs-value distinction, so it can also be reused for a fixed,
    already-known-rial unit literal like "rials"/"tomans"/"rls"/"irr")."""
    if _unit_is_rate_not_value(unit):
        return None, None, f"unit '{unit}' is an exchange rate, not a monetary value -- not converted"
    rial_val = _to_rial_equivalent(val, unit)
    nominal_usd = nominal_usd_from_lcu(rial_val, year)
    real_usd = real_usd_from_lcu(rial_val, year)
    if nominal_usd is None:
        return None, None, f"no FX rate for {year} (known gap), not converted"
    scale_note = ""
    u = (unit or "").lower()
    if "toman" in u and "rial" not in u:
        scale_note = " (toman->rial x10 applied before conversion)"
    return (round(nominal_usd, 4), round(real_usd, 4) if real_usd is not None else None,
            f"computed via IRN official/parallel FX rate + CPI, base year 2015 "
            f"(FX_{year}={FX.get(year)}, rebased CPI_{year}={CPI.get(year)}){scale_note}")


# ---- B1: generic value/unit/year folders ----
ARCHIVAL_FOLDERS = [
    "data/processed/pahlavi_government_finance_series",
    "data/processed/pahlavi_agriculture_trade_extensions",
    "data/processed/pahlavi_oil_energy_series",
    # Added 2026-07-13: same value/unit/year column shape, confirmed via a full data/processed
    # rial-marker scan to contain real rial/toman-unit rows (see reconnaissance log).
    "data/processed/imf_article_iv_iran_series",
    "data/processed/usaid_point_four_series",
    "data/processed/iran_aviation_history_series",
    "data/processed/iran_white_revolution_corps_series",
    "data/processed/specialty_goods_series",
    "data/processed/iran_disasters_regional_series",
]


def process_archival():
    total_converted_rows = 0
    files_touched = 0
    for folder in ARCHIVAL_FOLDERS:
        if not os.path.isdir(folder):
            continue
        for fname in sorted(os.listdir(folder)):
            if not fname.endswith(".csv"):
                continue
            path = os.path.join(folder, fname)
            with open(path, newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            # Files without all three of unit/value/year are skipped here by design -- e.g.
            # gold_price_divorce_rate_study.csv (iran_disasters_regional_series) has a "period"
            # range ("1980-2014") instead of a single "year" column, so it's intentionally left
            # out of this generic pass rather than guessing a representative year for a
            # multi-decade descriptive statistic.
            if not rows or "unit" not in rows[0] or "value" not in rows[0] or "year" not in rows[0]:
                continue
            fieldnames = list(rows[0].keys())
            if "value_usd_nominal" not in fieldnames:
                fieldnames += ["value_usd_nominal", "value_usd_real_2015", "currency_conversion_note"]

            changed = False
            for row in rows:
                unit = row.get("unit") or ""
                if not _unit_is_rial(unit):
                    row.setdefault("value_usd_nominal", "")
                    row.setdefault("value_usd_real_2015", "")
                    row.setdefault("currency_conversion_note", "")
                    continue
                try:
                    year = int(row["year"])
                    val = float(row["value"])
                except (ValueError, TypeError):
                    row["value_usd_nominal"] = ""
                    row["value_usd_real_2015"] = ""
                    row["currency_conversion_note"] = "unparseable year/value, not converted"
                    continue
                nominal_usd, real_usd, note = _convert_lcu_value(val, year, unit)
                row["value_usd_nominal"] = "" if nominal_usd is None else str(nominal_usd)
                row["value_usd_real_2015"] = "" if real_usd is None else str(real_usd)
                row["currency_conversion_note"] = note
                changed = True

            if changed:
                with open(path, "w", newline="", encoding="utf-8") as f:
                    w = csv.DictWriter(f, fieldnames=fieldnames)
                    w.writeheader()
                    w.writerows(rows)
                files_touched += 1
                total_converted_rows += sum(1 for r in rows if r.get("value_usd_nominal"))

    print(f"Archival files touched (generic value/unit/year schema): {files_touched}")
    print(f"Archival rows converted to USD nominal+real (generic schema): {total_converted_rows}")
    return files_touched, total_converted_rows


# ---- B2: bespoke schemas -- explicit rial-named column(s), various year sources ----
def _year_from_col(col):
    def fn(row):
        try:
            return int(row[col])
        except (KeyError, ValueError, TypeError):
            return None
    return fn


def _year_from_fiscal_ah_plus622(row, col="fiscal_year_ah"):
    """AH solar fiscal year -> approx Gregorian fiscal-YEAR-END, i.e. +622. Matches the convention
    this project's OWN sibling file (national_budget_totals_by_fiscal_year.csv) already uses for
    its explicit fiscal_year_ah -> fiscal_year_western_end column (verified: 1341+622=1963,
    matching that file's own printed value)."""
    try:
        return int(row[col]) + 622
    except (KeyError, ValueError, TypeError):
        return None


def _year_from_date_col_prefix(col):
    def fn(row):
        try:
            return int(str(row[col])[:4])
        except (KeyError, ValueError, TypeError):
            return None
    return fn


def _year_from_slash_year(col):
    """Parses a dual-year fiscal label like '1953/54' by taking the leading (Gregorian-numbered)
    year. Used for pahlavi_industry_series/railways_income_expense_1953_1961.csv, the only file
    found using this specific format (the original 3 pahlavi archival folders don't use it)."""
    def fn(row):
        try:
            return int(str(row[col]).split("/")[0])
        except (KeyError, ValueError, TypeError, IndexError):
            return None
    return fn


def _year_constant(y):
    return lambda row: y


def _year_from_year_op_started(row):
    raw = (row.get("year_operation_started") or "").strip()
    if not raw:
        return None
    digits = "".join(ch for ch in raw.split("(")[0] if ch.isdigit())
    return int(digits) if digits else None


CUSTOM_JOBS = [
    {
        # fiscal_year_ah/ministry/article/item/amount/unit -- e.g. bookkeeping.md's own named
        # example schema. All observed rows are toman-denominated; year predates IFS FX coverage
        # (1937+) so every row is expected to land as an honest "no FX rate" gap, not a silent
        # zero-conversion -- kept in the job list anyway so that gap is documented in the file
        # itself, not just in this script's comments.
        "path": "data/processed/majlis_budget_law_series/ministry_level_appropriations_1301.csv",
        "year_fn": _year_from_fiscal_ah_plus622,
        "columns": [("amount", "unit_col", "amount")],
    },
    {
        "path": "data/processed/majlis_budget_law_series/supplementary_budget_additions.csv",
        "year_fn": _year_from_col("fiscal_year_western_end"),
        "columns": [("amount_rials", "rials", "amount")],
    },
    {
        # bookkeeping.md's other named example schema: revenue_rials/expenditure_rials.
        "path": "data/processed/majlis_budget_law_series/national_budget_totals_by_fiscal_year.csv",
        "year_fn": _year_from_col("fiscal_year_western_end"),
        "columns": [("revenue_rials", "rials", "revenue"), ("expenditure_rials", "rials", "expenditure")],
    },
    {
        "path": "data/processed/iran_plan_budget_org_series/annual_budget_law_totals_1371_1401.csv",
        "year_fn": _year_from_col("fiscal_year_western_end"),
        "columns": [("revenue_rials", "rials", "revenue"), ("expenditure_rials", "rials", "expenditure")],
    },
    {
        "path": "data/processed/cbi_annual_review_series/monetary_banking_aggregates_1379_1401.csv",
        "year_fn": _year_from_col("fiscal_year_western_end"),
        "columns": [("liquidity_m2_billion_rials", "rials", "liquidity_m2"),
                    ("monetary_base_billion_rials", "rials", "monetary_base")],
    },
    {
        # No year column at all in the source (year is only in the filename/report title). The
        # file already has 3 rows of a PRE-EXISTING, primary-sourced total_million_usd column
        # (real historical USD estimates from the source document itself) -- deliberately NOT
        # touched; these new columns use an unambiguous "_computed" name so they're never
        # confused with that primary-sourced figure.
        "path": "data/processed/iran_dams_water_infrastructure_series/dez_dam_cost_estimate_by_component_1960.csv",
        "year_fn": _year_constant(1960),
        "columns": [("total_million_rials", "rials", "total_computed")],
        "note_suffix": " [year 1960 taken from filename/report date, no per-row year column in "
                        "source; pre-existing total_million_usd column, where present, is a "
                        "primary-sourced figure from the original document and is left untouched]",
    },
    {
        "path": "data/processed/iran_dams_water_infrastructure_series/major_dams_specifications_1971.csv",
        "year_fn": _year_from_year_op_started,
        "columns": [("cost_of_dam_million_rials", "rials", "cost_of_dam"),
                    ("cost_of_irrigation_million_rials", "rials", "cost_of_irrigation")],
        "note_suffix": " [year = this dam's own year_operation_started, not the 1971 survey/report "
                        "year; blank for dams still under study/construction with no start year yet]",
    },
    {
        "path": "data/processed/iran_ports_tariff_series/container_storage_charges_2024.csv",
        "year_fn": _year_constant(2024),
        "columns": [("charge_rial", "rials", "charge")],
    },
    {
        "path": "data/processed/iran_industry_ministry_series/mimt_daily_bulletin_panel_1399.csv",
        "year_fn": _year_from_date_col_prefix("date_western"),
        "columns": [("stad_esystem_transactions_value_million_toman", "tomans",
                     "stad_esystem_transactions_value")],
    },
    {
        # Single toman-denominated row (1901) among many non-monetary "term" rows (dates, areas,
        # percentages, qualitative text) -- the unit_col gate below skips all the non-rial ones.
        # Expected to land as an honest "no FX rate" gap (1901 predates IFS FX coverage, 1937+).
        "path": "data/processed/iran_foreign_concessions_series/darcy_oil_concession_1901_terms.csv",
        "year_fn": _year_constant(1901),
        "columns": [("value", "unit_col", "value")],
    },
    {
        "path": "data/processed/pahlavi_industry_series/railways_income_expense_1953_1961.csv",
        "year_fn": _year_from_slash_year("year"),
        "columns": [("gross_revenues_million_rls", "rls", "gross_revenues"),
                    ("working_expenses_million_rls", "rls", "working_expenses"),
                    ("balance_before_depreciation_million_rls", "rls", "balance_before_depreciation")],
    },
    {
        # period_start/period_end range, not a single "year" column -- uses period_start as the
        # reference year (documented in note_suffix). Most rows are non-monetary (persons taught)
        # or already USD-denominated ("US_dollars" unit) -- the unit_col gate skips those; one row
        # ("300-400" toman, a range string) will also correctly fall through as unparseable.
        "path": "data/processed/iran_white_revolution_corps_series/literacy_corps_program_totals.csv",
        "year_fn": _year_from_col("period_start"),
        "columns": [("value", "unit_col", "value")],
        "note_suffix": " [year = period_start; rate may have applied through period_end too -- "
                        "exact within-range year not resolvable from source]",
    },
]


def _resolve_unit(row, unit_spec):
    return row.get("unit") or "" if unit_spec == "unit_col" else unit_spec


def process_custom_jobs():
    files_touched = 0
    rows_converted = 0
    for job in CUSTOM_JOBS:
        path = job["path"]
        if not os.path.exists(path):
            print(f"  [skip, not found] {path}")
            continue
        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        if not rows:
            continue
        fieldnames = list(rows[0].keys())
        for value_col, unit_spec, out_prefix in job["columns"]:
            for suffix in ("_usd_nominal", "_usd_real_2015"):
                c = f"{out_prefix}{suffix}"
                if c not in fieldnames:
                    fieldnames.append(c)
        if "currency_conversion_note" not in fieldnames:
            fieldnames.append("currency_conversion_note")

        file_had_conversion = False
        for row in rows:
            year = job["year_fn"](row)
            note_parts = []
            for value_col, unit_spec, out_prefix in job["columns"]:
                nom_col, real_col = f"{out_prefix}_usd_nominal", f"{out_prefix}_usd_real_2015"
                raw = row.get(value_col)
                if raw is None or str(raw).strip() == "":
                    row[nom_col] = ""
                    row[real_col] = ""
                    continue
                unit = _resolve_unit(row, unit_spec)
                if not _unit_is_rial(unit):
                    # e.g. a non-toman/rial row sharing a unit_col-driven file with real rial rows
                    row[nom_col] = ""
                    row[real_col] = ""
                    continue
                try:
                    val = float(raw)
                except (ValueError, TypeError):
                    row[nom_col] = ""
                    row[real_col] = ""
                    note_parts.append(f"{value_col}: unparseable value, not converted")
                    continue
                if year is None:
                    row[nom_col] = ""
                    row[real_col] = ""
                    note_parts.append(f"{value_col}: no year available for this row, not converted")
                    continue
                nominal_usd, real_usd, note = _convert_lcu_value(val, year, unit)
                row[nom_col] = "" if nominal_usd is None else str(nominal_usd)
                row[real_col] = "" if real_usd is None else str(real_usd)
                note_parts.append(f"{value_col}: {note}")
                if nominal_usd is not None:
                    file_had_conversion = True
                    rows_converted += 1
            if note_parts:
                row["currency_conversion_note"] = "; ".join(note_parts) + job.get("note_suffix", "")
            else:
                row.setdefault("currency_conversion_note", "")

        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)
        files_touched += 1
        if not file_had_conversion:
            print(f"  [written, 0 rows converted -- documented gap] {path}")

    print(f"Custom-schema archival files processed: {files_touched}")
    print(f"Custom-schema archival rows with at least one value converted: {rows_converted}")
    return files_touched, rows_converted


# ---- B3: iran_insurance_series -- dynamic *_million_irr column detection, year_sh+622 ----
INSURANCE_FOLDER = "data/processed/iran_insurance_series"


def process_insurance_series():
    files_touched = 0
    rows_converted = 0
    if not os.path.isdir(INSURANCE_FOLDER):
        return 0, 0
    for fname in sorted(os.listdir(INSURANCE_FOLDER)):
        if not fname.endswith(".csv"):
            continue
        path = os.path.join(INSURANCE_FOLDER, fname)
        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        if not rows or "year_sh" not in rows[0]:
            continue
        irr_cols = [c for c in rows[0].keys() if c.endswith("_million_irr")]
        if not irr_cols:
            continue  # e.g. companies_by_ownership_type.csv, sales_network_by_year.csv (counts only)
        fieldnames = list(rows[0].keys())
        for c in irr_cols:
            prefix = c[: -len("_million_irr")]
            for suffix in ("_usd_nominal", "_usd_real_2015"):
                nc = f"{prefix}{suffix}"
                if nc not in fieldnames:
                    fieldnames.append(nc)
        if "currency_conversion_note" not in fieldnames:
            fieldnames.append("currency_conversion_note")

        file_had_conversion = False
        for row in rows:
            year = _year_from_fiscal_ah_plus622(row, col="year_sh")
            any_value = False
            for c in irr_cols:
                prefix = c[: -len("_million_irr")]
                nom_col, real_col = f"{prefix}_usd_nominal", f"{prefix}_usd_real_2015"
                raw = row.get(c)
                if raw is None or str(raw).strip() == "" or year is None:
                    row[nom_col] = ""
                    row[real_col] = ""
                    continue
                try:
                    val = float(raw)
                except ValueError:
                    row[nom_col] = ""
                    row[real_col] = ""
                    continue
                nominal_usd, real_usd, _note = _convert_lcu_value(val, year, "irr")
                row[nom_col] = "" if nominal_usd is None else str(nominal_usd)
                row[real_col] = "" if real_usd is None else str(real_usd)
                if nominal_usd is not None:
                    any_value = True
            if year is None:
                row["currency_conversion_note"] = "year_sh missing/unparseable, not converted"
            else:
                row["currency_conversion_note"] = (
                    f"computed via IRN official/parallel FX rate + CPI, base year 2015; year = "
                    f"year_sh({row.get('year_sh')})+622 (approx Gregorian fiscal-year-end, "
                    f"consistent with cbi_annual_review_series' own fiscal_year_western_end "
                    f"convention); FX_{year}={FX.get(year)}, rebased CPI_{year}={CPI.get(year)}"
                )
            if any_value:
                file_had_conversion = True
                rows_converted += 1
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)
        files_touched += 1
        if not file_had_conversion:
            print(f"  [written, 0 rows converted -- documented gap] {path}")

    print(f"Insurance-series files processed: {files_touched}")
    print(f"Insurance-series rows with at least one value converted: {rows_converted}")
    return files_touched, rows_converted


if __name__ == "__main__":
    process_wdi()
    process_wdi_lcu_only()
    gen_files, gen_rows = process_archival()
    custom_files, custom_rows = process_custom_jobs()
    ins_files, ins_rows = process_insurance_series()
    print(f"TOTAL archival files touched: {gen_files + custom_files + ins_files}")
    print(f"TOTAL archival rows converted: {gen_rows + custom_rows + ins_rows}")
