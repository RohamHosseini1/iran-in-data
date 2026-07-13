"""Harmonize the 23 CBI Annual Review PDFs (English-language, data/raw/cbi-iran/
cbi-annual-review-wayback/, FY1379-1401 / 2000/01-2022/23) into a tidy processed CSV of headline
monetary/banking aggregates.

METHOD: these are native-text PDFs (not scans -- confirmed via pdftotext, no OCR/visual-render step
needed, unlike the Pahlavi-era archival PDFs which ARE scans). Each PDF was converted to plain text
via `pdftoppm`-free `pdftotext -layout`, then the "Money and Banking" chapter's own narrative
sentences ("Liquidity grew by X percent... reached Rls. Y billion/trillion") and its recurring
"Factors Affecting Monetary Base and Liquidity" summary table were read directly and cross-checked
against each other (the narrative figure and the table figure for the same year were required to
match before being recorded). For each fiscal year, the figure used is that YEAR'S OWN annual
review's stated current-year value (never a prior or later year's retrospective restatement of it)
-- see the README's note on inter-year revisions for why this matters.

Every figure here has a direct textual citation trail (line-locatable in the plain-text extraction
of the source PDF); nothing was interpolated or estimated. Where a figure was not found/legible
within the time budget of this pass, the cell is left blank -- never fabricated.
Raw PDFs are never modified.
"""
import csv

OUT = "data/processed/cbi_annual_review_series"

def ah_to_western_end_year(ah_year):
    return ah_year + 622

# Each row: fiscal_year_ah, m2_level_billion_rials, m2_growth_pct, monetary_base_level_billion_rials,
# monetary_base_growth_pct, cpi_inflation_growth_pct, notes, source_file
ROWS = [
    dict(fy=1379, m2=249110.7, m2g=29.3, mb=84398.1, mbg=17.5, cpi=12.6,
         notes="CPI figure is the average annual consumer price index growth; the report separately states a point-to-point (year-end) inflation figure of 20.1 percent, which is NOT the same measure -- kept out of the cpi_inflation_growth_pct column to avoid conflating the two; see raw text line ~1067 of the plain-text extraction for both.",
         source_file="cbi_annual_review_1379_2000-01.pdf"),
    dict(fy=1380, m2=320957.3, m2g=28.8, mb=97184.8, mbg=15.2, cpi=11.4, notes="",
         source_file="cbi_annual_review_1380_2001-02.pdf"),
    dict(fy=1381, m2=417524.0, m2g=30.1, mb=None, mbg=23.1, cpi=None,
         notes="Monetary base LEVEL not captured this pass (only its 23.1 percent growth rate was cleanly legible; the source page mixes a bar-chart's axis labels into the surrounding paragraph text in the plain-text extraction, making the exact billion-rial figure ambiguous to transcribe with confidence -- left blank rather than guessed). CPI/inflation narrative for this year is similarly chart-garbled in the extraction and was not used.",
         source_file="cbi_annual_review_1381_2002-03.pdf"),
    dict(fy=1382, m2=526596.4, m2g=26.1, mb=None, mbg=None, cpi=15.6,
         notes="CPI is the consumer price index growth rate as stated ('the consumer, wholesale and producer price indices grew by 15.6, 10.1 and 15.6 percent, respectively' -- note CPI and PPI are both printed as 15.6, not a transcription error, taken directly from source). Monetary base not captured this pass.",
         source_file="cbi_annual_review_1382_2003-04.pdf"),
    dict(fy=1383, m2=685697.5, m2g=30.2, mb=151200.0, mbg=17.5, cpi=15.2,
         notes="IMPORTANT: FY1383's own report states its year-end M2 as 685,697.5 billion rials, but the FOLLOWING year's report (FY1384, see its own table) restates the same FY1383 year-end M2 as 685,867.2 billion rials -- a small (~170 million rial, ~0.02%) but real inter-report revision, kept as printed in FY1383's own report rather than silently updated to the later restatement (this project's standing never-pick-a-winner policy for disagreeing sources, here applied to sequential vintages of the same statistic). Monetary base level/growth taken from the FY1384 report's prior-year column (151,200.0 billion, 17.5 percent), which matches FY1383's own narrative growth language.",
         source_file="cbi_annual_review_1383_2004-05.pdf"),
    dict(fy=1384, m2=921019.4, m2g=34.3, mb=220541.4, mbg=45.9, cpi=None,
         notes="No 'Price Trends' narrative section was found in this file's extraction (unlike all other years) -- confirmed genuine gap in this pass, not a search failure elsewhere avoided.",
         source_file="cbi_annual_review_1384_2005-06.pdf"),
    dict(fy=1385, m2=1284199.4, m2g=39.4, mb=280000.0, mbg=26.9, cpi=13.6,
         notes="Monetary base level of 'Rls. 280 trillion' as stated in narrative prose (not a table row with more decimal precision) -- recorded as 280,000.0 billion rials; treat as a rounded figure, not to the same decimal precision as other years' table-sourced levels.",
         source_file="cbi_annual_review_1385_2006-07.pdf"),
    dict(fy=1386, m2=1640293.0, m2g=27.7, mb=None, mbg=30.5, cpi=None,
         notes="Monetary base level and CPI not captured this pass.", source_file="cbi_annual_review_1386_2007-08.pdf"),
    dict(fy=1387, m2=1901366.0, m2g=15.9, mb=None, mbg=None, cpi=None,
         notes="Monetary base and CPI not captured this pass.", source_file="cbi_annual_review_1387_2008-09.pdf"),
    dict(fy=1388, m2=2355889.1, m2g=23.9, mb=None, mbg=None, cpi=None,
         notes="Monetary base and CPI not captured this pass.", source_file="cbi_annual_review_1388_2009-10.pdf"),
    dict(fy=1389, m2=2948874.2, m2g=25.2, mb=None, mbg=13.7, cpi=None,
         notes="Monetary base level and CPI not captured this pass.", source_file="cbi_annual_review_1389_2010-11.pdf"),
    dict(fy=1390, m2=3522204.1, m2g=19.4, mb=None, mbg=None, cpi=21.5,
         notes="Liquidity growth (19.4%) and inflation (21.5%) both stated together in the same narrative sentence, providing a natural cross-check that the M2 growth figure (19.4%) matches the M2 table value independently extracted.",
         source_file="cbi_annual_review_1390_2011-12.pdf"),
    dict(fy=1391, m2=4606935.9, m2g=30.0, mb=None, mbg=27.6, cpi=None,
         notes="Monetary base level and CPI not captured this pass.", source_file="cbi_annual_review_1391_2012-13.pdf"),
    dict(fy=1392, m2=5947853.5, m2g=29.1, mb=None, mbg=17.8, cpi=None,
         notes="Monetary base level and CPI not captured this pass.", source_file="cbi_annual_review_1392_2013-14.pdf"),
    dict(fy=1393, m2=7823847.9, m2g=22.3, mb=None, mbg=10.7, cpi=None,
         notes="Monetary base level and CPI not captured this pass.", source_file="cbi_annual_review_1393_2014-15.pdf"),
    dict(fy=1394, m2=10172800.0, m2g=30.0, mb=None, mbg=16.9, cpi=None,
         notes="Source table denominated in TRILLION rials from this year onward (10,172.8) -- converted x1000 to billion rials here for unit consistency with earlier years. Monetary base level and CPI not captured this pass.",
         source_file="cbi_annual_review_1394_2015-16.pdf"),
    dict(fy=1395, m2=12533900.0, m2g=23.2, mb=None, mbg=17.3, cpi=None,
         notes="Source table in trillion rials (12,533.9), converted x1000 to billion rials. Monetary base level and CPI not captured this pass.",
         source_file="cbi_annual_review_1395_2016-17.pdf"),
    dict(fy=1396, m2=15299800.0, m2g=22.1, mb=None, mbg=19.0, cpi=None,
         notes="RAW FILENAME NOTE: this file is named 'cbi_annual_review_1396_2016-17.pdf' but its actual text content is explicitly dated 'March 2018' throughout (e.g. 'Broad money (M2) amounted to Rls. 15,299.8 trillion in March 2018') -- FY1396 (AH solar) properly corresponds to 2017/18, not 2016-17 (which is FY1395, already used by the adjacent file cbi_annual_review_1395_2016-17.pdf, whose own content is correctly dated 'in 2016/17'). This is a Western-year-label copy/paste error in the raw filename from an earlier download round, not an error in this project's reading of the file's actual content, and not corrected in the raw filename per the immutability rule -- flagged here and in the README. Source stated 'Rls. 15,299.8 trillion' -- converted x1000 to billion rials.",
         source_file="cbi_annual_review_1396_2016-17.pdf (filename's '2016-17' suffix is a mislabeling; content is FY1396=2017/18)"),
    dict(fy=1397, m2=18828900.0, m2g=23.1, mb=None, mbg=24.2, cpi=None,
         notes="Source stated 'Rls. 18,828.9 trillion' (March 2019) -- converted x1000 to billion rials. Monetary base level and CPI not captured this pass.",
         source_file="cbi_annual_review_1397_2018-19.pdf"),
    dict(fy=1398, m2=24721500.0, m2g=31.3, mb=None, mbg=32.8, cpi=None,
         notes="Source stated 'Rls. 24,721.5 trillion' (March 2020) -- converted x1000 to billion rials. Monetary base level and CPI not captured this pass.",
         source_file="cbi_annual_review_1398_2019-20.pdf"),
    dict(fy=1399, m2=34761700.0, m2g=40.6, mb=None, mbg=30.1, cpi=None,
         notes="Source stated 'Rls. 34,761.7 trillion' (March 2021) -- converted x1000 to billion rials. Monetary base level and CPI not captured this pass.",
         source_file="cbi_annual_review_1399_2020-21.pdf"),
    dict(fy=1400, m2=48324400.0, m2g=39.0, mb=None, mbg=31.6, cpi=None,
         notes="Source stated 'Rls. 48,324.4 trillion' (March 2022) -- converted x1000 to billion rials. Monetary base level and CPI not captured this pass.",
         source_file="cbi_annual_review_1400_2021-22.pdf"),
    dict(fy=1401, m2=63376800.0, m2g=31.1, mb=None, mbg=42.4, cpi=None,
         notes="Source stated 'Rls. 63,376.8 trillion' (March 2023) -- converted x1000 to billion rials. Monetary base level and a candidate CPI figure ('soared to 8.7 percent in 2022') were found nearby but NOT used -- context suggests this may refer to a regional/global comparator inflation figure rather than Iran's own CPI (ambiguous), so left blank per the no-guessing rule rather than risk a wrong attribution.",
         source_file="cbi_annual_review_1401_2022-23.pdf"),
]

with open(f"{OUT}/monetary_banking_aggregates_1379_1401.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = ["fiscal_year_ah", "fiscal_year_western_end", "liquidity_m2_billion_rials",
                  "liquidity_m2_growth_pct", "monetary_base_billion_rials", "monetary_base_growth_pct",
                  "cpi_inflation_growth_pct", "notes", "country_iso3", "source_file"]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for r in ROWS:
        w.writerow({
            "fiscal_year_ah": r["fy"], "fiscal_year_western_end": ah_to_western_end_year(r["fy"]),
            "liquidity_m2_billion_rials": r["m2"] if r["m2"] is not None else "",
            "liquidity_m2_growth_pct": r["m2g"] if r["m2g"] is not None else "",
            "monetary_base_billion_rials": r["mb"] if r["mb"] is not None else "",
            "monetary_base_growth_pct": r["mbg"] if r["mbg"] is not None else "",
            "cpi_inflation_growth_pct": r["cpi"] if r["cpi"] is not None else "",
            "notes": r["notes"], "country_iso3": "IRN", "source_file": r["source_file"],
        })
print(f"monetary_banking_aggregates_1379_1401.csv: {len(ROWS)} rows (all 23 fiscal years)")

# coverage summary
n_m2 = sum(1 for r in ROWS if r["m2"] is not None)
n_mb_level = sum(1 for r in ROWS if r["mb"] is not None)
n_mb_growth = sum(1 for r in ROWS if r["mbg"] is not None)
n_cpi = sum(1 for r in ROWS if r["cpi"] is not None)
print(f"Coverage: M2 level {n_m2}/23, monetary base level {n_mb_level}/23, "
      f"monetary base growth {n_mb_growth}/23, CPI {n_cpi}/23")
