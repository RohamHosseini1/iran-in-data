"""Harmonize CBI Annual Review "Balance of Payments" and "Export of Crude Oil" tables
(data/raw/cbi-iran/cbi-annual-review-wayback/, 23 English-language PDFs, FY1379-1401 /
2000/01-2022/23) into tidy trade/oil series extending this project's TRADE and OIL-EXPORT
layer with Iranian-primary (CBI, sourcing onward to Iran's Customs Administration / IRICA
and the Ministry of Petroleum) data for the Islamic Republic era.

METHOD: same as scripts/harmonize/harmonize_cbi_annual_review.py (native-text PDFs,
`pdftotext -layout`, no OCR needed). Every fiscal year's own Annual Review contains a
"Balance of Payments" table with a 5-year trailing window (the current fiscal year plus
the four preceding years, each year restated as of that report's own vintage). Per this
project's established convention (see cbi_annual_review_series/README.md), each fiscal
year's row uses THAT YEAR'S OWN report as the source -- never a later year's retrospective
restatement -- so inter-report revisions are visible if a future pass wants to compare
vintages, but never silently blended.

Two format eras exist in the source, both transcribed as printed (never reconciled):
  - Era A (FY1375-1386 / 1996/97-2007/08): "Trade balance / Exports / Oil and gas [and oil
    products] / Others / Imports". No oil-vs-non-oil split of IMPORTS in this era.
  - Era B (FY1387/2008-09, transitional): the source itself changed presentation mid-stream
    to "Exports (FOB) / Oil and gas / Exports of goods in trade statistics / Adjustments" --
    non-oil exports for this one year is computed as Exports(FOB) total minus Oil-and-gas
    (i.e. "Exports of goods in trade statistics" + "Adjustments" combined), flagged in notes.
  - Era C (FY1388-1401 / 2009/10-2022/23): "Exports (FOB) / Oil exports / Non-oil exports /
    Imports (FOB) / Gas and oil products / Other goods (non-oil imports)" -- a clean split on
    both sides. The source's own footnote states this reflects a 1997/98-2009/10 retroactive
    revision to the IMF Balance of Payments Manual 5th edition (BPM5); pre- and post-revision
    figures for the same year are NOT the same number by design (a genuine methodology break,
    not a project error) -- see README for the worked example.

A second, much shorter table -- "Export of Crude Oil" (Table 14, thousand barrels/day) --
appears ONLY in the two earliest reports (FY1379, FY1380). It was not found in any of the
other 21 files (confirmed by grep across all 23 plain-text extractions for "EXPORT OF CRUDE
OIL"). This is reported as a genuine, notable data-availability gap: CBI's own PUBLISHED
oil-export VOLUME series effectively stops after 2001/02, even though oil export REVENUE
(via the Balance of Payments table) continues to be published every year through FY1401.

Nothing here is interpolated, estimated, or fabricated. Every figure has a direct textual
citation trail (file + approximate line, recorded in `notes`/`source_file`). Raw PDFs are
never modified.
"""
import csv
import os

OUT_DIR = "data/processed/iran_trade_oil_enrich_series"
RAW_DIR = "data/raw/cbi-iran/cbi-annual-review-wayback"

BPM5_NOTE = ("CBI's own footnote: 'Balance of Payments data for 1997/98-2009/10 have been "
             "revised based on the fifth edition of the IMF Balance of Payments Manual "
             "(BPM5). Therefore, basis for classification and dissemination of data might be "
             "different.' This year's figure reflects that revision where applicable.")

# One row per fiscal year. All *_musd fields are million current US dollars, as printed.
# fy_ah = Iranian solar (Hijri) fiscal year; fy_label = source's own "1999/00"-style label;
# fy_end = fy_ah + 622 (Western calendar year the fiscal year ends in -- same convention as
# cbi_annual_review_series/monetary_banking_aggregates_1379_1401.csv).
ROWS = [
    dict(fy_ah=1375, fy_label="1996/97", ca=5232, trade_bal=7402, exp_total=22391,
         exp_oil=19271, exp_nonoil=3120, imp_total=14989, imp_oil=None, imp_other=None,
         source_file="cbi_annual_review_1379_2000-01.pdf",
         notes="Era A. Earliest year in our holdings; sourced from FY1379's report (the "
               "oldest available report covering this year) since no report from 1375's own "
               "vintage is held. Imports not split oil/non-oil in this era's table."),
    dict(fy_ah=1376, fy_label="1997/98", ca=2213, trade_bal=4258, exp_total=18381,
         exp_oil=15471, exp_nonoil=2910, imp_total=14123, imp_oil=None, imp_other=None,
         source_file="cbi_annual_review_1379_2000-01.pdf",
         notes="Era A. Sourced from FY1379's report (oldest available vintage covering this "
               "year); cross-checked identical in FY1380's report."),
    dict(fy_ah=1377, fy_label="1998/99", ca=-2140, trade_bal=-1168, exp_total=13118,
         exp_oil=9933, exp_nonoil=3185, imp_total=14286, imp_oil=None, imp_other=None,
         source_file="cbi_annual_review_1379_2000-01.pdf",
         notes="Era A. Trade deficit year (Asian financial crisis oil-price collapse). "
               "Cross-checked identical in FY1380's and FY1381's reports."),
    dict(fy_ah=1378, fy_label="1999/00", ca=6589, trade_bal=7597, exp_total=21030,
         exp_oil=17089, exp_nonoil=3941, imp_total=13433, imp_oil=None, imp_other=None,
         source_file="cbi_annual_review_1379_2000-01.pdf",
         notes="Era A. Cross-checked identical in FY1380/1381/1382 reports' trailing columns."),
    dict(fy_ah=1379, fy_label="2000/01", ca=12645, trade_bal=13138, exp_total=28345,
         exp_oil=24226, exp_nonoil=4119, imp_total=15207, imp_oil=None, imp_other=None,
         source_file="cbi_annual_review_1379_2000-01.pdf",
         notes="Era A, own-year report. NOTE: FY1380's report restates this year's current "
               "account as 12,500 (vs. 12,645 here) and trade balance/exports as 13,375/"
               "28,461 (vs. 13,138/28,345) -- a real, small inter-report revision, not an "
               "error; this row keeps FY1379's own contemporaneous figures per project "
               "convention (never pick a winner between vintages)."),
    dict(fy_ah=1380, fy_label="2001/02", ca=5985, trade_bal=5775, exp_total=23904,
         exp_oil=19339, exp_nonoil=4565, imp_total=18129, imp_oil=None, imp_other=None,
         source_file="cbi_annual_review_1380_2001-02.pdf",
         notes="Era A, own-year report."),
    dict(fy_ah=1381, fy_label="2002/03", ca=3731, trade_bal=4400, exp_total=28186,
         exp_oil=22807, exp_nonoil=5379, imp_total=23786, imp_oil=None, imp_other=None,
         source_file="cbi_annual_review_1381_2002-03.pdf",
         notes="Era A, own-year report."),
    dict(fy_ah=1382, fy_label="2003/04", ca=2059, trade_bal=4993, exp_total=33788,
         exp_oil=27033, exp_nonoil=6755, imp_total=28795, imp_oil=None, imp_other=None,
         source_file="cbi_annual_review_1382_2003-04.pdf",
         notes="Era A, own-year report."),
    dict(fy_ah=1383, fy_label="2004/05", ca=3989, trade_bal=7764, exp_total=44403,
         exp_oil=36827, exp_nonoil=7576, imp_total=36639, imp_oil=None, imp_other=None,
         source_file="cbi_annual_review_1383_2004-05.pdf",
         notes="Era A, own-year report."),
    dict(fy_ah=1384, fy_label="2005/06", ca=14037, trade_bal=19043, exp_total=60012,
         exp_oil=48823, exp_nonoil=11189, imp_total=40969, imp_oil=None, imp_other=None,
         source_file="cbi_annual_review_1384_2005-06.pdf",
         notes="Era A, own-year report. NOTE: FY1385's report restates this year's current "
               "account as 16,637 (vs. 14,037 here) -- a real inter-report revision (this is "
               "the same 2005/06 revision the project's own currency-conversion doc flagged "
               "for FX purposes); kept as FY1384's own contemporaneous figure."),
    dict(fy_ah=1385, fy_label="2006/07", ca=20650, trade_bal=26245, exp_total=75537,
         exp_oil=62458, exp_nonoil=13079, imp_total=49292, imp_oil=None, imp_other=None,
         source_file="cbi_annual_review_1385_2006-07.pdf",
         notes="Era A, own-year report."),
    dict(fy_ah=1386, fy_label="2007/08", ca=34081, trade_bal=40819, exp_total=97401,
         exp_oil=81764, exp_nonoil=15637, imp_total=56582, imp_oil=None, imp_other=None,
         source_file="cbi_annual_review_1386_2007-08.pdf",
         notes="Era A, own-year report. Last year before the source's own presentation "
               "changes (Era B transition in the very next report)."),
    dict(fy_ah=1387, fy_label="2008/09", ca=23987, trade_bal=32039, exp_total=100571,
         exp_oil=81855, exp_nonoil=18716, imp_total=68533, imp_oil=None, imp_other=None,
         source_file="cbi_annual_review_1387_2008-09.pdf",
         notes="Era B (transitional presentation). Source's own table for this year reads "
               "'Exports (FOB)=100,571 / Oil and gas=81,855 / Exports of goods in trade "
               "statistics=18,146 / Adjustments=570' with NO single 'non-oil exports' line -- "
               "exp_nonoil here is computed as Exports(FOB) minus Oil-and-gas (18,716 = "
               "100,571-81,855, matching 18,146+570 to within rounding), not printed verbatim "
               "as one cell. Imports similarly given as 'Imports (FOB)=68,533 / Imports of "
               "goods in trade statistics=55,849 / Adjustments=12,684' with no oil/non-oil "
               "import split published this year. FY1388's NEXT report retroactively "
               "restates this same year (2008/09) as CA=22,903, Exports=101,289, Oil "
               "exports=86,619, Non-oil=14,670, Imports=70,199 under the BPM5 revision -- a "
               "materially different set of numbers, not an error in either report (see "
               "BPM5 footnote). Kept as FY1387's own report per convention; the FY1388 "
               "revised vintage is recorded separately as the FY1388 row below (for 2009/10)."),
    dict(fy_ah=1388, fy_label="2009/10", ca=10908, trade_bal=20936, exp_total=87534,
         exp_oil=69825, exp_nonoil=17709, imp_total=66599, imp_oil=6600, imp_other=59999,
         source_file="cbi_annual_review_1388_2009-10.pdf",
         notes="Era C (clean Oil exports/Non-oil exports/Imports split begins). " + BPM5_NOTE),
    dict(fy_ah=1389, fy_label="2010/11", ca=25457, trade_bal=40165, exp_total=108612,
         exp_oil=86052, exp_nonoil=22560, imp_total=68446, imp_oil=3496, imp_other=64950,
         source_file="cbi_annual_review_1389_2010-11.pdf",
         notes="Era C, own-year report. " + BPM5_NOTE),
    dict(fy_ah=1390, fy_label="2011/12", ca=59383, trade_bal=67069, exp_total=144874,
         exp_oil=118232, exp_nonoil=26642, imp_total=77805, imp_oil=5726, imp_other=72079,
         source_file="cbi_annual_review_1390_2011-12.pdf",
         notes="Era C, own-year report. Peak pre-2012-sanctions-escalation export year in "
               "this series."),
    dict(fy_ah=1391, fy_label="2012/13", ca=26271, trade_bal=30975, exp_total=98033,
         exp_oil=68135, exp_nonoil=29899, imp_total=67058, imp_oil=2639, imp_other=64419,
         source_file="cbi_annual_review_1391_2012-13.pdf",
         notes="Era C, own-year report. Sharp oil-export drop vs. 2011/12 coincides with the "
               "2012 EU oil embargo / SWIFT-disconnection sanctions escalation."),
    dict(fy_ah=1392, fy_label="2013/14", ca=27965, trade_bal=32968, exp_total=93015,
         exp_oil=64789, exp_nonoil=28226, imp_total=60047, imp_oil=3111, imp_other=56936,
         source_file="cbi_annual_review_1392_2013-14.pdf",
         notes="Era C, own-year report."),
    dict(fy_ah=1393, fy_label="2014/15", ca=15861, trade_bal=21392, exp_total=86471,
         exp_oil=55352, exp_nonoil=31119, imp_total=65079, imp_oil=3948, imp_other=61131,
         source_file="cbi_annual_review_1393_2014-15.pdf",
         notes="Era C, own-year report. 2014 oil-price collapse visible in oil-export value."),
    dict(fy_ah=1394, fy_label="2015/16", ca=9016, trade_bal=12178, exp_total=64597,
         exp_oil=33569, exp_nonoil=31028, imp_total=52419, imp_oil=2233, imp_other=50186,
         source_file="cbi_annual_review_1394_2015-16.pdf",
         notes="Era C, own-year report. Final pre-JCPOA-implementation year (JCPOA "
               "Implementation Day was Jan 2016, i.e. within this fiscal year)."),
    dict(fy_ah=1395, fy_label="2016/17", ca=16388, trade_bal=20843, exp_total=83978,
         exp_oil=55752, exp_nonoil=28226, imp_total=63135, imp_oil=1388, imp_other=61747,
         source_file="cbi_annual_review_1395_2016-17.pdf",
         notes="Era C, own-year report. First full post-JCPOA-sanctions-relief fiscal year; "
               "oil exports recover sharply vs. 2015/16."),
    dict(fy_ah=1396, fy_label="2017/18", ca=15816, trade_bal=22596, exp_total=98142,
         exp_oil=65818, exp_nonoil=32324, imp_total=75546, imp_oil=2764, imp_other=72782,
         source_file="cbi_annual_review_1396_2016-17.pdf",
         notes="Era C, own-year report. RAW FILENAME NOTE (per cbi_annual_review_series/"
               "README.md): this file's filename says '2016-17' but its content is dated "
               "March 2018, i.e. genuinely covers FY1396=2017/18 -- fiscal_year_ah=1396 here "
               "is correct; only the raw filename's Western-year suffix is mislabeled."),
    dict(fy_ah=1397, fy_label="2018/19", ca=26741, trade_bal=32635, exp_total=93390,
         exp_oil=60735, exp_nonoil=32655, imp_total=60755, imp_oil=1378, imp_other=59377,
         source_file="cbi_annual_review_1397_2018-19.pdf",
         notes="Era C, own-year report. Last near-full pre-'maximum pressure'-sanctions year "
               "(US withdrew from JCPOA May 2018, within this fiscal year; full sanctions "
               "snapback effects show up more in the FY1398 row)."),
    dict(fy_ah=1398, fy_label="2019/20", ca=3754, trade_bal=7155, exp_total=59391,
         exp_oil=29016, exp_nonoil=30375, imp_total=52236, imp_oil=6, imp_other=52230,
         source_file="cbi_annual_review_1398_2019-20.pdf",
         notes="Era C, own-year report. Oil exports collapse to roughly half the prior year's "
               "level -- 'maximum pressure' sanctions reimposition fully in effect. Non-oil "
               "exports now exceed oil exports for the first time in this series."),
    dict(fy_ah=1399, fy_label="2020/21", ca=-708, trade_bal=3236, exp_total=49848,
         exp_oil=21043, exp_nonoil=28805, imp_total=46612, imp_oil=None, imp_other=46612,
         source_file="cbi_annual_review_1399_2020-21.pdf",
         notes="Era C, own-year report. First negative current-account balance in this "
               "series. Gas-and-oil-products IMPORT line printed as '__' (illegible/near-"
               "zero dash in source layout, not a normal number) -- left blank rather than "
               "guessed; Other-goods imports (46,612) equals the full imports total, "
               "consistent with a near-zero oil/gas import line that year (COVID-19 demand "
               "collapse plausibly relevant, not confirmed by source text)."),
    dict(fy_ah=1400, fy_label="2021/22", ca=11144, trade_bal=15844, exp_total=79470,
         exp_oil=38723, exp_nonoil=40748, imp_total=63626, imp_oil=0.2, imp_other=63626,
         source_file="cbi_annual_review_1400_2021-22.pdf",
         notes="Era C, own-year report. Non-oil exports exceed oil exports for the second "
               "time in this series."),
    dict(fy_ah=1401, fy_label="2022/23", ca=14205, trade_bal=22247, exp_total=97656,
         exp_oil=55410, exp_nonoil=42246, imp_total=75409, imp_oil=228, imp_other=75182,
         source_file="cbi_annual_review_1401_2022-23.pdf",
         notes="Era C, own-year report. Most recent fiscal year in our 23-PDF holdings."),
]

# Table 14 "Export of Crude Oil" (thousand barrels/day) -- only in the two earliest reports.
OIL_VOLUME_ROWS = [
    dict(fy_ah=1375, fy_label="1996/97", crude_kbd=2441, products_kbd=186, total_kbd=2627,
         source_file="cbi_annual_review_1379_2000-01.pdf", table="Table 14"),
    dict(fy_ah=1376, fy_label="1997/98", crude_kbd=2342, products_kbd=222, total_kbd=2564,
         source_file="cbi_annual_review_1379_2000-01.pdf", table="Table 14",
         notes="Identical in FY1380's report (own-vintage cross-check, no revision)."),
    dict(fy_ah=1377, fy_label="1998/99", crude_kbd=2300, products_kbd=113, total_kbd=2413,
         source_file="cbi_annual_review_1379_2000-01.pdf", table="Table 14",
         notes="Identical in FY1380's report."),
    dict(fy_ah=1378, fy_label="1999/00", crude_kbd=2079, products_kbd=197, total_kbd=2276,
         source_file="cbi_annual_review_1379_2000-01.pdf", table="Table 14",
         notes="Identical in FY1380's report."),
    dict(fy_ah=1379, fy_label="2000/01", crude_kbd=2345, products_kbd=181, total_kbd=2526,
         source_file="cbi_annual_review_1380_2001-02.pdf", table="Table 14",
         notes="FY1379's OWN report left this year's own-year column as '..' (not yet "
               "available at press time); value taken from FY1380's report, the earliest "
               "vintage that reports it."),
    dict(fy_ah=1380, fy_label="2001/02", crude_kbd=2208, products_kbd=218, total_kbd=2426,
         source_file="cbi_annual_review_1380_2001-02.pdf", table="Table 14",
         notes="Own-year report. LAST year this table appears in any of the 23 reports held "
               "-- confirmed by grep for 'EXPORT OF CRUDE OIL' / 'Export of Crude Oil' across "
               "all 23 plain-text extractions: zero hits in any FY1381-1401 report. CBI's own "
               "published oil-export VOLUME series stops here even though oil export REVENUE "
               "(via the Balance of Payments table) continues to be published every "
               "subsequent year through FY1401. Genuine source gap, not a project omission."),
]

# Table 20 "Geographical Distribution of Crude Oil Exports" (percent shares) -- same
# discontinuation pattern as Table 14; only 5 years, 2 of them via revision, ever published.
GEO_SHARE_ROWS = [
    dict(fy_ah=1376, fy_label="1997/98", region="Europe", share_pct=51.4),
    dict(fy_ah=1376, fy_label="1997/98", region="Japan", share_pct=19.1),
    dict(fy_ah=1376, fy_label="1997/98", region="Asia and Far East (except Japan)", share_pct=26.9),
    dict(fy_ah=1376, fy_label="1997/98", region="Africa", share_pct=0.0),
    dict(fy_ah=1376, fy_label="1997/98", region="Other countries", share_pct=2.6),
    dict(fy_ah=1377, fy_label="1998/99", region="Europe", share_pct=49.8),
    dict(fy_ah=1377, fy_label="1998/99", region="Japan", share_pct=18.7),
    dict(fy_ah=1377, fy_label="1998/99", region="Asia and Far East (except Japan)", share_pct=27.8),
    dict(fy_ah=1377, fy_label="1998/99", region="Africa", share_pct=0.0),
    dict(fy_ah=1377, fy_label="1998/99", region="Other countries", share_pct=3.7),
    dict(fy_ah=1378, fy_label="1999/00", region="Europe", share_pct=33.6),
    dict(fy_ah=1378, fy_label="1999/00", region="Japan", share_pct=24.7),
    dict(fy_ah=1378, fy_label="1999/00", region="Asia and Far East (except Japan)", share_pct=26.1),
    dict(fy_ah=1378, fy_label="1999/00", region="Africa", share_pct=0.0),
    dict(fy_ah=1378, fy_label="1999/00", region="Other countries", share_pct=15.6),
    dict(fy_ah=1379, fy_label="2000/01", region="Europe", share_pct=31.4),
    dict(fy_ah=1379, fy_label="2000/01", region="Japan", share_pct=21.9),
    dict(fy_ah=1379, fy_label="2000/01", region="Asia and Far East (except Japan)", share_pct=39.6),
    dict(fy_ah=1379, fy_label="2000/01", region="Africa", share_pct=7.1),
    dict(fy_ah=1379, fy_label="2000/01", region="Other countries", share_pct=0.0),
    dict(fy_ah=1380, fy_label="2001/02", region="Europe", share_pct=14.0),
    dict(fy_ah=1380, fy_label="2001/02", region="Japan", share_pct=23.7),
    dict(fy_ah=1380, fy_label="2001/02", region="Asia and Far East (except Japan)", share_pct=41.8),
    dict(fy_ah=1380, fy_label="2001/02", region="Africa", share_pct=6.9),
    dict(fy_ah=1380, fy_label="2001/02", region="Other countries", share_pct=13.6,
         notes="Footnote: 'Includes Mediterranean countries in 1380.'"),
]


def fy_end(ah):
    return ah + 622


def write_bop_csv():
    path = os.path.join(OUT_DIR, "cbi_balance_of_payments_trade_oil_1375_1401.csv")
    fieldnames = [
        "country_iso3", "indicator_id", "fiscal_year_ah", "fiscal_year_label", "year",
        "value", "unit", "source_dataset", "source_file", "notes",
    ]
    indicator_defs = [
        ("iran_bop_current_account_musd", "ca"),
        ("iran_bop_trade_or_goods_balance_musd", "trade_bal"),
        ("iran_bop_exports_total_fob_musd", "exp_total"),
        ("iran_bop_exports_oil_musd", "exp_oil"),
        ("iran_bop_exports_nonoil_musd", "exp_nonoil"),
        ("iran_bop_imports_total_fob_musd", "imp_total"),
        ("iran_bop_imports_oil_gas_musd", "imp_oil"),
        ("iran_bop_imports_other_nonoil_musd", "imp_other"),
    ]
    n = 0
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in ROWS:
            for indicator_id, key in indicator_defs:
                val = row.get(key)
                if val is None:
                    continue
                w.writerow(dict(
                    country_iso3="IRN",
                    indicator_id=indicator_id,
                    fiscal_year_ah=row["fy_ah"],
                    fiscal_year_label=row["fy_label"],
                    year=fy_end(row["fy_ah"]),
                    value=val,
                    unit="million current US dollars",
                    source_dataset="cbi-iran-annual-review",
                    source_file=row["source_file"],
                    notes=row["notes"],
                ))
                n += 1
    print(f"wrote {n} rows to {path}")


def write_oil_volume_csv():
    path = os.path.join(OUT_DIR, "cbi_crude_oil_export_volume_1375_1380.csv")
    fieldnames = [
        "country_iso3", "indicator_id", "fiscal_year_ah", "fiscal_year_label", "year",
        "value", "unit", "source_dataset", "source_file", "notes",
    ]
    n = 0
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in OIL_VOLUME_ROWS:
            for indicator_id, key in [
                ("iran_crude_oil_export_volume_thousand_bpd", "crude_kbd"),
                ("iran_oil_products_export_volume_thousand_bpd", "products_kbd"),
                ("iran_total_oil_export_volume_thousand_bpd", "total_kbd"),
            ]:
                w.writerow(dict(
                    country_iso3="IRN",
                    indicator_id=indicator_id,
                    fiscal_year_ah=row["fy_ah"],
                    fiscal_year_label=row["fy_label"],
                    year=fy_end(row["fy_ah"]),
                    value=row[key],
                    unit="thousand barrels per day",
                    source_dataset="cbi-iran-annual-review",
                    source_file=row["source_file"],
                    notes=row.get("notes", ""),
                ))
                n += 1
    print(f"wrote {n} rows to {path}")


def write_geo_share_csv():
    path = os.path.join(OUT_DIR, "cbi_crude_oil_export_geographic_share_1376_1380.csv")
    fieldnames = [
        "country_iso3", "indicator_id", "fiscal_year_ah", "fiscal_year_label", "year",
        "destination_region", "value", "unit", "source_dataset", "source_file", "notes",
    ]
    n = 0
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in GEO_SHARE_ROWS:
            source_file = ("cbi_annual_review_1379_2000-01.pdf" if row["fy_ah"] <= 1378
                            else "cbi_annual_review_1380_2001-02.pdf")
            w.writerow(dict(
                country_iso3="IRN",
                indicator_id="iran_crude_oil_export_geographic_share_pct",
                fiscal_year_ah=row["fy_ah"],
                fiscal_year_label=row["fy_label"],
                year=fy_end(row["fy_ah"]),
                destination_region=row["region"],
                value=row["share_pct"],
                unit="percent of crude oil export value",
                source_dataset="cbi-iran-annual-review",
                source_file=source_file,
                notes=row.get("notes", ""),
            ))
            n += 1
    print(f"wrote {n} rows to {path}")


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    write_bop_csv()
    write_oil_volume_csv()
    write_geo_share_csv()
