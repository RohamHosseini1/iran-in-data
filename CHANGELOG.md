# Changelog

Tracks changes that matter to anyone re-using or citing this data — new categories, methodology
changes, and data-quality fixes. Not a running commit log (see git history for that); see
`docs/bookkeeping.md` § "Versioning & changelog" for what belongs here.

## 2026-07-13

- **Project named and licensed.** Public name: "Iran in Data" (iranindata.org), compiled by Roham
  Hosseini. Dual-licensed: code under MIT, data compilation under CC BY 4.0.
- **Chart deduplication registry established** (`CHART_REGISTRY.csv`). Raw indicator counts across
  the machine-readable sources (WDI, FAOSTAT, IMF WEO, OWID, Maddison, WID) were heavily inflated by
  unit/currency variants and cross-source duplication; deduplicated to real distinct chart concepts.
- **Currency & inflation-adjustment methodology established**, then corrected twice:
  1. Base methodology: deflate in local currency to a 2015 base year using each country's own CPI,
     then convert to USD at the 2015 exchange rate (mirrors WDI's own "constant US$" convention).
  2. **Correction**: for Iran's Islamic Republic era (1979–present), official multi-tier exchange
     rates are not representative of what the public or private sector actually transacted at — the
     parallel/black-market rate is used instead, except 2003–2010 (a genuinely unified rate era) and
     the still-open pre-1999 stretch.
  3. Extended to all 17 project countries; Venezuela and Argentina also get a parallel-rate
     correction for their own documented divergence eras, following the same evidence-based logic
     as Iran rather than a blanket rule.
- **Citation-accuracy audit.** All fuzzy-matched archival citations were manually verified; found and
  fixed 15 wrong citations (country/topic mismatches) caused by two bugs in the matching script,
  which were fixed at the root rather than just patched per-row.
- **Timeline broadened** beyond deliberate policy decisions to include wars, revolutions, disasters,
  and global shocks (e.g. the 1941 Anglo-Soviet occupation, the 1917–18 famine and flu pandemic, the
  1990 Manjil-Rudbar earthquake) that can plausibly correlate with economic chart movements.
- **Public-good packaging added**: machine-readable catalog (`catalog/CHARTS_INDEX.json`), category
  index, `llms.txt` for AI-agent discoverability, and bulk-download zip packaging.
- Project moved into version control for the first time.
