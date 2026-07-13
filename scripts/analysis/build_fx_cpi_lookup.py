"""Build a single authoritative Iran FX-rate and CPI-index lookup table (JSON), used by
build_currency_variants.py to compute real/USD variants for every currency chart.

Per docs/bookkeeping.md "Currency & inflation-adjustment conventions" (corrected 2026-07-13 per
explicit user instruction): the OFFICIAL exchange rate is only used for the pre-1979 Pahlavi era.
For 1979-present (Islamic Republic era), the PARALLEL/BLACK-MARKET rate is used instead -- the
official multi-tier rates are not what an ordinary transaction actually costs.

UPDATE 2026-07-13 (later same day): the 1979-2010 gap is now CLOSED for 1979-2010 (real, dated,
directly-observed parallel/black-market data for every year) -- see
data/raw/iran-parallel-fx-1979-2010-research/manifest.json. Backbone source is Bahmani-Oskooee
(2005, Iranian Economic Review) Table 4, a complete MONTHLY black-market rial/USD series for
1979-2003 sourced to the World Currency Yearbook (Pick's) through mid-1989 and directly to the
Central Bank of Iran from mid-1989 onward; 2004-2010 is covered by annual anchors (mostly a
one-hop-removed Wikipedia transcription of CBI Annual Review 2013/14 figures, since cbi.ir and its
Wayback mirror were both inaccessible to this round). This supersedes an earlier, much thinner
concurrent-round interim fix (data/raw/iran-fx-secondary-compiled/wikipedia-iranprimer-cross-check/,
4 annual points for 1999-2002 only, plus a 2003-2010 fallback that used WDI's OFFICIAL rate on the
reasoning that the 2002 unification made official~=market for that window) -- that raw folder is
left untouched on disk per this project's no-delete rule, but its two loader functions are no
longer called here now that real parallel-rate figures (not an official-rate proxy) cover the same
2003-2010 window with a stronger citation trail.

UPDATE 2026-07-13 (later still): extended to build a matching FX/CPI lookup for the project's 16
comparator countries (KOR, TUR, SAU, VEN, USA, RUS, ARG, ESP, PRT, GRC, DEU, FRA, GBR, ITA, NLD,
SWE), one JSON file each (data/processed/fx_cpi_lookup_<iso3_lower>.json). The IRN-specific
functions/output above are UNCHANGED -- this is purely additive. Comparators use WDI's
PA.NUS.FCRF + FP.CPI.TOTL (same "constant US$" convention, no multi-tier/black-market complication)
for 14 of the 16 -- there is no equivalent documented black-market FX problem for South Korea,
Turkey, Saudi Arabia, USA, Russia, Spain, Portugal, Greece, Germany, France, UK, Italy, Netherlands,
or Sweden in this project's holdings. Two exceptions get the same "prefer a real, sourced parallel
rate over the official one" treatment Iran gets, because a genuine, well-documented divergence
exists and this project already has real data for it:
  - Venezuela: CADIVI/CENCOEX/DICOM multi-tier official rate vs. a black-market rate that reached
    ~100x official at points (2016 CENCOEX 10 vs black-market 1000 VEF/USD). Source: data/processed/
    iran_trade_institutions_fx_series/venezuela_parallel_fx_rate_milestones_2003_2020.csv.
  - Argentina: the "cepo cambiario" capital-control era (2011-2015, 2019-2024) produced a
    persistent official-vs-"blue" (informal cash) rate gap. Source: data/raw/argentinadatos/
    dolares-multi-rate-daily-2011-2026/dolares_2026-07-13.json (casa='blue'), not yet parsed into
    data/processed anywhere else in this project.
  Argentina also needed a CPI substitute since WDI's FP.CPI.TOTL has ZERO rows for ARG: built from
  IMF WEO's PCPI (actual-only, macro_imf_weo.csv) chained onto the independent Cavallo-Bertolotto
  academic CPI reconstruction (data/raw/argentina-inflation-reconstruction/) for the 1943-2017
  backbone, which also transparently covers the real, well-documented 2014-2015 INDEC-manipulation
  data blackout that leaves a hole in WEO's own actual-data series.
  Venezuela's WDI CPI is likewise very thin (2008-2016, 9 points, hyperinflation-era reporting
  collapse) so IMF WEO's PCPI (actual-only, continuous 1980-2025) is used as VEN's sole CPI source
  instead, rather than splicing two different bases.
See logs/downloads/currency-extension-comparators-archival.log for the full reconnaissance trail.
"""
import csv
import json
import math
import os
import statistics

OUT = "data/processed/fx_cpi_lookup_irn.json"


def _round_sig(x, sig=8):
    """Round to `sig` significant figures rather than a fixed decimal count. A plain round(x, 4)
    silently collapses to 0.0 for a series like Argentina's rebased CPI index (72 years of
    cumulative hyperinflation before its 2015 base year compresses early-year index values well
    below 1e-4), which would then divide-by-zero downstream in build_currency_variants.py. Only
    used for the comparator-country CPI index (see build_comparator below); Iran's own CPI index
    doesn't hit this edge case (checked -- its smallest, 1937, is 0.0032) so its main() above is
    left untouched."""
    if x == 0:
        return 0.0
    d = sig - int(math.floor(math.log10(abs(x)))) - 1
    return round(x, d)


def load_wdi_fx_pre1979():
    fx = {}
    with open("data/processed/macro_wdi.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["country_iso3"] == "IRN" and row["indicator_id"] == "PA.NUS.FCRF" and row["value"]:
                year = int(row["year"])
                if year < 1979:
                    fx[year] = float(row["value"])
    return fx


def load_ifs_fx():
    fx = {}
    with open("data/raw/imf-ifs-historical/iran-annual-series-extracted/data.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["metric"] == "exchange_rate_official" and row["value"]:
                try:
                    year = int(row["year"])
                    if year < 1979:
                        fx[year] = float(row["value"])
                except ValueError:
                    pass
    return fx


def load_parallel_fx_annual():
    """Annualize the 2011-2026 daily TGJU parallel-rate series (mean of daily closes per year)."""
    by_year = {}
    with open("data/processed/iran_trade_institutions_fx_series/usd_irr_parallel_rate_daily_2011_2026.csv",
              newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                year = int(row["date_gregorian"].split("/")[0])
                close = float(row["close"])
            except (ValueError, IndexError):
                continue
            by_year.setdefault(year, []).append(close)
    return {y: statistics.mean(vals) for y, vals in by_year.items() if vals}


def load_parallel_fx_1979_2010():
    """1979-2010 parallel/black-market rate, from data/raw/iran-parallel-fx-1979-2010-research/
    (backbone: Bahmani-Oskooee 2005 Table 4, a complete monthly series 1979-2003 sourced to the
    World Currency Yearbook/Pick's through mid-1989 and directly to the Central Bank of Iran from
    mid-1989 onward; 2004-2010 covered by annual anchors, mostly a one-hop-removed Wikipedia
    transcription of CBI Annual Review 2013/14 figures -- see that folder's manifest.json for full
    per-figure citations). Monthly years are annualized (mean of the months present that year, same
    convention as load_parallel_fx_annual's TGJU annualization); years with only annual/point rows
    use the 'annual'-frequency row directly. 2011 is deliberately excluded here even though present
    in the source file -- TGJU's own daily series (load_parallel_fx_annual) already covers 2011
    (from Nov 26) and takes precedence as the more granular source at that seam.
    """
    by_year_monthly = {}
    annual_direct = {}
    with open("data/processed/iran_trade_institutions_fx_series/usd_irr_parallel_rate_1979_2011.csv",
              newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                year = int(row["year"])
            except ValueError:
                continue
            if year < 1979 or year > 2010:
                continue
            try:
                value = float(row["rial_per_usd_parallel"])
            except ValueError:
                continue
            if row["frequency"] == "monthly":
                by_year_monthly.setdefault(year, []).append(value)
            elif row["frequency"] == "annual":
                annual_direct.setdefault(year, []).append(value)
            # point_observation rows are cross-validation anchors only, not fed into the lookup,
            # to avoid double-counting against a same-year monthly or annual figure.
    out = {y: statistics.mean(vals) for y, vals in by_year_monthly.items() if vals}
    for y, vals in annual_direct.items():
        if y not in out:  # monthly coverage (1979-2003) always wins if present
            out[y] = statistics.mean(vals)
    return out


def load_wdi_cpi():
    cpi = {}
    with open("data/processed/macro_wdi.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["country_iso3"] == "IRN" and row["indicator_id"] == "FP.CPI.TOTL" and row["value"]:
                cpi[int(row["year"])] = float(row["value"])
    return cpi


def load_pre1960_inflation_rates():
    rates = {}
    with open("data/processed/iran_data_portal_deep_series/inflation_rate_1937_2014.csv",
              newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            year = int(row["year_western"].split("-")[-1])
            try:
                rates[year] = float(row["inflation_rate_pct"])
            except ValueError:
                pass
    return rates


def main():
    ifs_fx = load_ifs_fx()               # 1937-1949, official (Pahlavi era)
    wdi_fx_pre1979 = load_wdi_fx_pre1979()  # 1960-1978, official (Pahlavi era)
    parallel_fx_1979_2010 = load_parallel_fx_1979_2010()  # 1979-2010, black-market (IRI era)
    parallel_fx = load_parallel_fx_annual()  # 2011-2026, black-market (IRI era, TGJU)
    wdi_cpi = load_wdi_cpi()
    pre1960_rates = load_pre1960_inflation_rates()

    # ---- FX rate lookup ----
    # Pre-1979: official rate (Pahlavi era, official ~= market, no sanctions/capital controls).
    # 1979-2010: parallel/black-market rate -- Bahmani-Oskooee (2005) Table 4 monthly series
    #            (1979-2003, annualized) + annual anchors (2004-2010). See
    #            data/raw/iran-parallel-fx-1979-2010-research/manifest.json for full per-year
    #            citations and confidence notes. Includes the 2003-2010 window even though official
    #            and parallel rates were genuinely unified/converged then (confirmed by this same
    #            source) -- recorded as an observed parallel figure, not an official-rate stand-in.
    # 2011-2026: parallel/black-market rate (annual mean of TGJU daily closes) -- divergence resumed.
    fx_lookup = {}
    fx_lookup.update(ifs_fx)
    fx_lookup.update(wdi_fx_pre1979)
    fx_source = {y: "official (Pahlavi era, official ~= market)" for y in fx_lookup}
    for y, v in parallel_fx_1979_2010.items():
        fx_lookup[y] = v
        fx_source[y] = "parallel/black-market (Bahmani-Oskooee 2005 Table 4, annualized, + annual anchors)"
    for y, v in parallel_fx.items():
        fx_lookup[y] = v
        fx_source[y] = "parallel/black-market (TGJU annual mean)"

    gap_years = [y for y in range(1950, 1960) if y not in fx_lookup]
    iri_gap_years = [y for y in range(1979, 2011) if y not in fx_lookup]

    # ---- CPI index, rebased so 2015 = 100, chained back to 1937 (unchanged -- CPI/inflation
    # measurement itself isn't an "official vs black-market" question, only the FX conversion is) ----
    if 2015 not in wdi_cpi:
        raise SystemExit("WDI CPI has no 2015 value -- cannot rebase, aborting")
    rebase_factor = 100.0 / wdi_cpi[2015]
    cpi_index = {y: v * rebase_factor for y, v in wdi_cpi.items()}
    for y in range(1959, 1936, -1):
        rate_at_next_year = pre1960_rates.get(y + 1)
        if rate_at_next_year is None or (y + 1) not in cpi_index:
            break
        cpi_index[y] = cpi_index[y + 1] / (1 + rate_at_next_year / 100.0)

    out = {
        "methodology": "See docs/bookkeeping.md 'Currency & inflation-adjustment conventions'. "
                        "Base year 2015=100 for CPI index. FX rate = rials per US$. Pre-1979: "
                        "official rate (Pahlavi era, official ~= market). 1979-2010: parallel/"
                        "black-market rate -- Bahmani-Oskooee (2005) Table 4 monthly series "
                        "(1979-2003) + annual anchors (2004-2010), see "
                        "data/raw/iran-parallel-fx-1979-2010-research/manifest.json. 2011-present: "
                        "parallel/black-market rate (TGJU daily). Never uses the official multi-tier "
                        "rate for any period after 1979, even when official and parallel happened to "
                        "converge (e.g. 2003-2010) -- the recorded figure is always an observed "
                        "parallel/market rate, not an official-rate stand-in.",
        "fx_rate_rials_per_usd": {str(y): fx_lookup[y] for y in sorted(fx_lookup)},
        "fx_rate_source_by_year": {str(y): fx_source[y] for y in sorted(fx_source)},
        "fx_gap_years_pahlavi_era_not_fabricated": gap_years,
        "fx_gap_years_iri_era_not_fabricated": iri_gap_years,
        "cpi_index_2015_base100": {str(y): round(cpi_index[y], 4) for y in sorted(cpi_index)},
        "cpi_pre1960_note": "1937-1959 values are BACK-CHAINED from WDI's 2015-based index using "
                             "Bank Melli/CBI YoY inflation rates, not a directly measured continuous "
                             "index. Treat with wider uncertainty than the WDI-native 1960+ segment.",
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    print(f"FX rate years covered: {sorted(fx_lookup.keys())[0]}-{sorted(fx_lookup.keys())[-1]}, "
          f"{len(fx_lookup)} years with real data")
    print(f"Pahlavi-era FX gap (1950-1959, not fabricated): {gap_years}")
    print(f"IRI-era FX gap remaining (1979-2010, not fabricated -- {len(iri_gap_years)} years): "
          f"{iri_gap_years}")
    print(f"CPI index years: {sorted(cpi_index.keys())[0]}-{sorted(cpi_index.keys())[-1]}")
    print(f"Wrote {OUT}")


# ============================================================================================
# Comparator countries (16). See module docstring "UPDATE 2026-07-13 (later still)" for the
# methodology summary and logs/downloads/currency-extension-comparators-archival.log for the
# full reconnaissance trail behind each source choice below.
# ============================================================================================
COMPARATOR_COUNTRIES = [
    "KOR", "TUR", "SAU", "VEN", "USA", "RUS", "ARG", "ESP",
    "PRT", "GRC", "DEU", "FRA", "GBR", "ITA", "NLD", "SWE",
]
# Countries with a real, documented official-vs-parallel FX divergence in this project's holdings
# (same "prefer the parallel rate" principle Iran gets). All other comparators use WDI's official
# PA.NUS.FCRF outright -- no known equivalent black-market problem for them in this project.
PARALLEL_FX_COUNTRIES = {"VEN", "ARG"}
# Countries where WDI's FP.CPI.TOTL is missing or too thin to use as the CPI source.
CPI_SUBSTITUTE_COUNTRIES = {"ARG", "VEN"}

# Eurozone comparators: WDI's PA.NUS.FCRF is NOT retroactively restated across the Euro changeover
# (confirmed by inspection -- e.g. DEU's own series jumps from ~1.76 Deutsche-Mark-per-USD in 1998
# to ~0.94 EUR-per-USD in 1999 with no rescale, unlike VEN/RUS's redenominations which WDI DOES
# restate continuously). Left as-is, this project's base-year-ratio deflation formula
# (FX[year]/FX[2015]) would silently divide a pre-Euro-national-currency figure by a Euro figure
# as if they were the same unit -- not a data gap, a real correctness bug. Fixed here by rescaling
# every pre-Euro year into EUR-equivalent terms using the EU's own official, permanently fixed
# (irrevocable, EU Council Regulation) national-currency-per-EUR conversion rates -- these are
# exact historical facts, not an estimate or a judgment call, so this is not "inventing" a rate the
# way an interpolation would be. CPI needs no equivalent fix: FP.CPI.TOTL is a pure chain-linked
# index, confirmed continuous across each changeover (no jump) by inspection.
EURO_LEGACY_CONVERSION = {
    # iso3: (first year WDI reports in EUR, national-currency-units per 1 EUR, national currency name)
    "DEU": (1999, 1.95583, "Deutsche Mark"),
    "FRA": (1999, 6.55957, "French Franc"),
    "ITA": (1999, 1936.27, "Italian Lira"),
    "ESP": (1999, 166.386, "Spanish Peseta"),
    "PRT": (1999, 200.482, "Portuguese Escudo"),
    "NLD": (1999, 2.20371, "Dutch Guilder"),
    "GRC": (2001, 340.750, "Greek Drachma"),  # Greece joined the euro two years after the first wave
}

ARG_CB_CSV = ("data/raw/argentina-inflation-reconstruction/"
              "cavallo-bertolotto-inflation-1943-2016/Argentina_inflation_inflacionverdadera_2022-09-01.csv")
ARG_BLUE_JSON = "data/raw/argentinadatos/dolares-multi-rate-daily-2011-2026/dolares_2026-07-13.json"
VEN_PARALLEL_CSV = ("data/processed/iran_trade_institutions_fx_series/"
                     "venezuela_parallel_fx_rate_milestones_2003_2020.csv")


def load_wdi_fx_official_generic(iso3):
    fx = {}
    with open("data/processed/macro_wdi.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["country_iso3"] == iso3 and row["indicator_id"] == "PA.NUS.FCRF" and row["value"]:
                fx[int(row["year"])] = float(row["value"])
    return fx


def load_wdi_cpi_generic(iso3):
    cpi = {}
    with open("data/processed/macro_wdi.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["country_iso3"] == iso3 and row["indicator_id"] == "FP.CPI.TOTL" and row["value"]:
                cpi[int(row["year"])] = float(row["value"])
    return cpi


def load_weo_pcpi_actual(iso3):
    """IMF WEO PCPI (Consumer Price Index, period average), ACTUAL values only (is_actual=='True'
    -- excludes WEO's own forward projections, which are not real observed data)."""
    cpi = {}
    with open("data/processed/macro_imf_weo.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if (row["country_iso3"] == iso3 and row["indicator_id"] == "PCPI"
                    and row["value"] and row.get("is_actual") == "True"):
                cpi[int(row["year"])] = float(row["value"])
    return cpi


def load_argentina_cb_index_annual():
    """Cavallo & Bertolotto's independent academic CPI reconstruction (monthly index, 1943m1-
    2018m11 -- see data/raw/argentina-inflation-reconstruction/.../manifest.json). Annualized as
    the mean of the 12 monthly values for each FULL calendar year present (2018 is dropped here --
    only 11 months on file -- so the backbone this function returns is clean 1943-2017)."""
    by_year = {}
    with open(ARG_CB_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                year = int(row["date"].split("m")[0])
                idx = float(row["index"])
            except (ValueError, IndexError, KeyError):
                continue
            by_year.setdefault(year, []).append(idx)
    return {y: statistics.mean(vals) for y, vals in by_year.items() if len(vals) == 12}


def build_argentina_cpi():
    """Backbone 1943-2017 from Cavallo-Bertolotto (rebased to this project's own 2015=100 using
    CB's own 2015 annual average), then chain IMF WEO's actual annual growth rates forward for
    2018-2025 off the 2017 seam (both series have a real 2017 value). This mirrors the same
    "back-chain a supplementary source's growth rate onto the anchored 2015 base" technique
    fx_cpi_lookup_irn.json's own pre-1960 CPI construction already uses (see
    load_pre1960_inflation_rates / main() above) -- not a new methodology, the same one applied to
    a different gap. WEO is continuous 2016-2025 (only its 2014/2015 rows are missing, both before
    the 2018 chain-start), so no further gap-jumping logic is needed for this segment."""
    cb = load_argentina_cb_index_annual()
    weo = load_weo_pcpi_actual("ARG")
    if 2015 not in cb:
        raise SystemExit("Argentina Cavallo-Bertolotto series has no full 2015 -- cannot rebase, aborting")
    rebase = 100.0 / cb[2015]
    cpi_index = {y: v * rebase for y, v in cb.items()}
    cpi_source = {y: "Cavallo-Bertolotto academic CPI reconstruction (annualized), rebased 2015=100"
                  for y in cpi_index}
    prev = cpi_index.get(2017)
    if prev is not None and 2017 in weo:
        y = 2018
        while y in weo and (y - 1) in weo:
            prev = prev * (weo[y] / weo[y - 1])
            cpi_index[y] = prev
            cpi_source[y] = ("IMF WEO PCPI actual annual growth rate, chained onto the "
                              "Cavallo-Bertolotto 2015-based backbone at the 2017 seam")
            y += 1
    return cpi_index, cpi_source


def load_argentina_blue_fx_annual():
    """Argentina's 'blue' (informal/cash black-market) USD rate, daily 2011-01-03 to 2026-07-12,
    from the ArgentinaDatos API dump (data/raw/argentinadatos/.../manifest.json). Mid of
    compra/venta (buy/sell), annualized as the mean of daily mids per year -- same convention as
    Iran's TGJU annualization (load_parallel_fx_annual above), including that the final year on
    file may be a partial year."""
    with open(ARG_BLUE_JSON, encoding="utf-8") as f:
        data = json.load(f)
    by_year = {}
    for d in data:
        if d.get("casa") != "blue":
            continue
        try:
            mid = (float(d["compra"]) + float(d["venta"])) / 2.0
            year = int(d["fecha"][:4])
        except (KeyError, ValueError, TypeError):
            continue
        by_year.setdefault(year, []).append(mid)
    return {y: statistics.mean(vals) for y, vals in by_year.items() if vals}


def load_venezuela_parallel_fx_annual():
    """Venezuela black-market USD rate from dated milestone snapshots (NOT a systematic daily/
    monthly series -- see venezuela_parallel_fx_rate_milestones_2003_2020.csv's own notes column).
    Only rows whose rate_type contains 'black_market' are used (official_fixed/official_DICOM/
    official_SIMADI/official_CENCOEX/official_SICAD_I rows are the OFFICIAL side, deliberately
    excluded here -- WDI's own PA.NUS.FCRF already covers the official rate). All values are
    normalized to VEF-equivalent units (WDI's VEN series is itself already continuously restated
    across the 2008 VEB->VEF redenomination, confirmed by inspection -- no jump at 2008 in WDI's
    own numbers) so a single 2015-anchored ratio chain stays valid: rows stated in VES (after the
    2018-08-20 VEF->VES redenomination) are multiplied by 100,000 (1 VES = 100,000 VEF) back onto
    the VEF-equivalent scale. When multiple snapshots fall in the same year, the year's value is
    the mean of that year's snapshot midpoints (rate_low+rate_high)/2 -- a crude annual proxy given
    real intra-year (often hyperinflationary) volatility that a handful of point observations
    cannot capture, flagged as such in the output notes, not presented as a true annual average."""
    by_year = {}
    with open(VEN_PARALLEL_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if "black_market" not in row["rate_type"]:
                continue
            try:
                year = int(row["date"][:4])
                mid = (float(row["rate_low"]) + float(row["rate_high"])) / 2.0
            except (ValueError, KeyError):
                continue
            unit = row.get("unit", "")
            if unit == "VES_per_USD":
                mid *= 100_000.0
            elif unit != "VEF_per_USD":
                continue  # VEB_per_USD or any other unit: not expected among black_market rows, skip rather than guess
            by_year.setdefault(year, []).append(mid)
    return {y: statistics.mean(vals) for y, vals in by_year.items() if vals}


def build_comparator(iso3):
    fx = load_wdi_fx_official_generic(iso3)
    fx_source = {y: "official (WDI PA.NUS.FCRF, period average)" for y in fx}
    parallel_note = ""
    euro_note = ""

    if iso3 in EURO_LEGACY_CONVERSION:
        euro_year, conv_rate, currency_name = EURO_LEGACY_CONVERSION[iso3]
        rescaled_years = []
        for y in list(fx):
            if y < euro_year:
                fx[y] = fx[y] / conv_rate
                fx_source[y] = (f"official (WDI PA.NUS.FCRF, originally {currency_name} per US$, "
                                 f"rescaled to EUR-equivalent via the fixed EU conversion rate "
                                 f"1 EUR = {conv_rate} {currency_name})")
                rescaled_years.append(y)
        if rescaled_years:
            euro_note = (f" Pre-{euro_year} years ({min(rescaled_years)}-{max(rescaled_years)}) were "
                         f"reported by WDI in {currency_name} (not retroactively restated to EUR by "
                         f"WDI itself, confirmed by inspection) -- rescaled here to EUR-equivalent "
                         f"using the EU's permanently fixed conversion rate (1 EUR = {conv_rate} "
                         f"{currency_name}) so the whole series stays ratio-consistent with the "
                         f"EUR-denominated 2015 base year. This is an exact official conversion "
                         f"factor, not an estimate.")

    if iso3 == "VEN":
        parallel = load_venezuela_parallel_fx_annual()
        for y, v in parallel.items():
            fx[y] = v
            fx_source[y] = ("parallel/black-market (dated milestone snapshots, annualized mean, "
                             "VEF-equivalent) -- overrides WDI official per the documented CADIVI/"
                             "CENCOEX/DICOM multi-tier vs. black-market divergence")
        parallel_note = (" Parallel/black-market rate used for 2012-2020 (years with a real "
                          "black_market-labeled observation in venezuela_parallel_fx_rate_"
                          "milestones_2003_2020.csv) per the same 'prefer parallel over official' "
                          "principle Iran's post-1979 rate uses -- CADIVI/CENCOEX/DICOM official "
                          "rates were, at points, ~1/100th of the real black-market rate. 2003-2011 "
                          "and 2021-present remain WDI-official / blank respectively (no sourced "
                          "black-market figure available for those sub-windows in this project). "
                          "NOTE ON MAGNITUDE: 2018-2020 figures look implausibly large (billions of "
                          "'VEF per USD') because they are deliberately kept in pre-Aug-2018 "
                          "VEF-equivalent terms (the source's VES-denominated rows are multiplied "
                          "by 100,000, the official 1-VES=100,000-VEF redenomination factor) so "
                          "that the FX[year]/FX[2015] ratio this project's deflation formula relies "
                          "on stays dimensionally valid against the (pre-redenomination) 2015 base "
                          "year -- not a data error, and not how these rates were actually quoted "
                          "at the time.")
    elif iso3 == "ARG":
        parallel = load_argentina_blue_fx_annual()
        for y, v in parallel.items():
            fx[y] = v
            fx_source[y] = ("parallel/informal ('blue') rate (ArgentinaDatos, daily mid of compra/"
                             "venta, annualized) -- overrides WDI official per the documented "
                             "2011-2015 / 2019-2024 'cepo cambiario' capital-control era")
        parallel_note = (" Parallel/'blue' rate used for 2011-2026 (ArgentinaDatos daily series) "
                          "per the same principle -- Argentina's capital-control eras produced a "
                          "persistent, well-documented official/blue gap. Pre-2011 divergence also "
                          "occurred historically (1989 hyperinflation, 2001-02 convertibility "
                          "collapse) but no sourced parallel-rate data for those episodes exists in "
                          "this project -- left as WDI official, not fabricated.")

    if iso3 in CPI_SUBSTITUTE_COUNTRIES:
        if iso3 == "ARG":
            cpi_index, cpi_source = build_argentina_cpi()
            cpi_note = ("WDI's FP.CPI.TOTL has ZERO rows for Argentina -- CPI built instead from "
                         "the Cavallo-Bertolotto academic reconstruction (1943-2017 backbone) "
                         "chained onto IMF WEO PCPI actual growth rates (2018-2025). See "
                         "build_argentina_cpi() docstring.")
        else:  # VEN
            weo = load_weo_pcpi_actual("VEN")
            if 2015 not in weo:
                raise SystemExit("Venezuela WEO PCPI has no 2015 value -- cannot rebase, aborting")
            rebase = 100.0 / weo[2015]
            cpi_index = {y: v * rebase for y, v in weo.items()}
            cpi_source = {y: "IMF WEO PCPI actual, rebased 2015=100" for y in cpi_index}
            cpi_note = ("WDI's FP.CPI.TOTL is only 2008-2016 (9 points) for Venezuela -- hyperinflation-"
                         "era reporting collapse. Used IMF WEO's PCPI (actual only, continuous "
                         "1980-2025) instead as a single coherent source rather than splicing two "
                         "different index bases.")
    else:
        wdi_cpi = load_wdi_cpi_generic(iso3)
        if 2015 not in wdi_cpi:
            cpi_index, cpi_source, cpi_note = {}, {}, (
                "WDI FP.CPI.TOTL has no 2015 value for this country -- real/USD variants cannot be "
                "computed (base-year rebase impossible); FX-only lookup written, CPI left empty.")
        else:
            rebase = 100.0 / wdi_cpi[2015]
            cpi_index = {y: v * rebase for y, v in wdi_cpi.items()}
            cpi_source = {y: "WDI FP.CPI.TOTL, rebased 2015=100" for y in cpi_index}
            cpi_note = "WDI FP.CPI.TOTL (2015=100 rebase), no known gaps beyond WDI's own native coverage."

    fx_years = sorted(fx)
    gap_note = ""
    if fx_years:
        full_span = set(range(fx_years[0], fx_years[-1] + 1))
        missing = sorted(full_span - set(fx_years))
        if missing:
            gap_note = f" FX gap years within {fx_years[0]}-{fx_years[-1]} (not fabricated): {missing}."

    out = {
        "country_iso3": iso3,
        "methodology": ("See docs/bookkeeping.md 'Currency & inflation-adjustment conventions', "
                         "point 6 (comparator countries). Base year 2015=100 for CPI index. FX "
                         "rate = local currency units (LCU) per US$, WDI PA.NUS.FCRF (period "
                         "average) unless noted." + euro_note + parallel_note + gap_note),
        "fx_rate_lcu_per_usd": {str(y): fx[y] for y in sorted(fx)},
        "fx_rate_source_by_year": {str(y): fx_source[y] for y in sorted(fx_source)},
        "cpi_index_2015_base100": {str(y): _round_sig(cpi_index[y]) for y in sorted(cpi_index)},
        "cpi_source_note": cpi_note,
    }
    out_path = f"data/processed/fx_cpi_lookup_{iso3.lower()}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    fx_range = f"{fx_years[0]}-{fx_years[-1]}" if fx_years else "NONE"
    cpi_years = sorted(cpi_index)
    cpi_range = f"{cpi_years[0]}-{cpi_years[-1]}" if cpi_years else "NONE"
    print(f"{iso3}: FX {fx_range} (n={len(fx_years)}), CPI {cpi_range} (n={len(cpi_years)}) -> {out_path}")


def main_comparators():
    for iso3 in COMPARATOR_COUNTRIES:
        build_comparator(iso3)


if __name__ == "__main__":
    main()
    main_comparators()
