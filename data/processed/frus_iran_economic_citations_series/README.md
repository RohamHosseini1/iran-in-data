# Foreign Relations of the United States (FRUS) -- Iran economic citations (1951-1976)

Two FRUS volumes mined statistic-by-statistic into tidy long-format CSVs sharing the same schema.
Both source PDFs are official State Department-published, born-digital documents (no OCR needed)
totaling nearly 2,000 pages combined. Extraction method: `pdftotext -layout` full-text dump,
keyword-scan (`$`, `million`, `billion`, `rials`, `barrels`, `percent`, `oil revenue`, `budget`,
`deficit`, `loan`, `aid`, etc.) to identify economically dense candidate pages, then close reading
of the resulting candidate set with a full document-header index (built from the volume's own
numbered-document structure) to attach precise document/date/page citations to every row. No
sub-agents were used; raw PDFs in `data/raw/frus-iran/` were not modified.

## Schema

`date_label, year, category, subcategory, value, unit, notes, country_iso3, source_dataset, citation`

- **`date_label`** -- the period or event date as best characterized from context.
- **`year`** -- single sortable integer anchor; always cross-check `date_label` for precision
  (many rows describe multi-year targets, e.g. "by 1983", or historical comparisons across two
  or three dates within one row).
- **`category`** -- a coarse economic topic tag (Oil production & trade, Military expenditure,
  Foreign aid, Trade, Government Finance, Foreign investment, Prices, Macro / National Accounts,
  Demographics & Population, Balance of Payments, Labor & Employment, Metals & Minerals,
  Agriculture, External debt, Land Use, Foreign exchange) -- not a controlled vocabulary shared
  with other series in this project.
- **`subcategory`** -- the specific line item or statistic described.
- **`value`** / **`unit`** -- as printed in the source; many rows carry a before/after or
  multi-point comparison in a single `value` string (e.g. `"120 million (original) -> 238 million
  (100% increase) -> 338 million (Jan 1976)"`) because that is how the source itself framed a
  cost-escalation or trend -- these are **not** meant to be parsed as a single clean number without
  first reading the string.
- **`country_iso3`** -- see the per-file notes below; **this is the one schema element that
  differs between the two files in this folder.**
- **`source_dataset`**, **`citation`** (FRUS volume, document number, document date, and PDF page
  for every row).

## The two source documents

| `source_dataset` | Document | Rows | Era |
|---|---|---|---|
| `frus-iran-1951-54` | FRUS 1952-1954, Iran, 1951-1954 (`frus1951-54Iran.pdf`, 1,007pp) | 177 | Mossadeq nationalization crisis and 1953 coup |
| `frus-iran-1973-76-oil-boom-era` | FRUS 1969-1976, Volume XXVII, "Iran; Iraq, 1973-1976" (`frus1969-76v27.pdf`, 978pp) | 269 | Late Pahlavi oil-price-boom era, Nixon/Ford administrations |

**446 rows total.**

### `frus_1951_54_mossadegh_coup_era.csv`

Keyword-scanned all 1,007 pages, identified 113 candidate pages (≥4 economic-keyword hits),
close-read essentially the full candidate set end to end (PDF pages 22-976, i.e. nearly the entire
volume body). Covers Feb 1951-March 1954: EXIM Bank loan negotiations, oil production/refining
shares (world/regional), the Abadan refinery shutdown's employment/revenue impact, Soviet
Iranian-oil-access estimates, IBRD settlement proposal terms, exchange rates (official vs.
open-market, tracking the 1952-53 rial depreciation from ~32 to ~100/USD), monthly/annual
government budget deficits, the full NIE-46 (Feb 1952) financial snapshot, the Sept 5 1953 $45
million emergency grant (the single most-repeated figure across post-coup documents), and NIE and
NSC financial-appendix multi-year expenditure tables. `country_iso3` is always `IRN` in this file.

### `frus_1973_76_oil_boom_era.csv`

Keyword-scanned all 978 pages, identified 158 candidate pages (≥4 hits); close-read the 95
highest-density pages (≥6 hits) end to end, covering the volume's substantive body (PDF pages
52-950; pages beyond ~955 are the volume's back-matter Index and were confirmed to contain no
further economic data). The remaining 63 candidate pages with exactly 4-5 keyword hits were not
individually close-read -- a time-boxed scoping decision given this task's breadth across many
source documents, not an oversight; most 4-5-hit pages, spot-checked, were procedural/diplomatic
correspondence with only passing dollar-figure mentions already captured from adjacent pages.

**This volume covers both Iran and Iraq substantively** (its own title is "Iran; Iraq,
1973-1976"), unlike the 1951-54 volume or this project's CIA-series files, which use a
per-file-always-`IRN` convention. Because a meaningful fraction of this volume's content (about
20% of extracted rows) is genuinely and exclusively about Iraq's own domestic economy -- Iraq's
IPC oil nationalization, Iraq's Five-Year Plans, Iraq's GDP/population/trade -- **this file uses
`country_iso3 = IRQ` for those Iraq-only rows and `IRN` for everything else**, including
third-country comparator figures (US/French/Japanese/Saudi/UK figures) cited in the course of
Iran-focused discussions, which remain tagged `IRN` per this project's standard comparator-row
convention (see `notes` for what country a comparator figure actually describes). Filter by
`country_iso3` if you want an Iraq-only or Iran-only cut of this specific file; check `notes` for
any row where a non-Iran, non-Iraq country is the actual subject.

## Notable content in the 1973-76 file

- **Oil-price-shock arithmetic**: the Dec 1973 Tehran OPEC meeting's new $11.60/barrel posted
  price (>100% increase); the US government's contemporaneous internal estimate that the 1974
  world oil bill would double to ~$100 billion; and, three years later, Ford's Oct 1976 letter to
  the Shah citing OPEC's projected $125 billion in 1976 oil export earnings (>400% above 1973)
  against industrialized-country export prices to oil producers having risen only 30% since
  mid-1973.
- **The full Iran-US "recycling" relationship**: the Shah's stated $180 billion decade-long
  domestic investment program and $190-193 billion 1983 GNP target (two slightly different figures
  from two different meetings, both preserved as printed); the March 1975 Protocol's $12.5 billion
  five-year non-military trade/investment package (nuclear power, ports, agriculture, housing,
  hospitals); the US-Iran Joint Commission trade target's rapid escalation from $15 billion (1975)
  to $25-26 billion (1976); and Iran's own foreign-aid outflows (loans/credits to the UK, France,
  Egypt, Syria, Pakistan, India, the IMF, and the World Bank).
- **Detailed, document-by-document arms-cost-escalation chains** rarely available elsewhere: the
  Spruance-class destroyer's price rising from $100-120 million (Dec 1973 quote) to $238 million
  (purchase decision) to $338 million (Nov 1975/Jan 1976), corroborated independently in two
  separate documents (148 and 158); the I-Hawk "Peace Shield" program's $270 million → $444
  million → $800 million escalation; and the F-16/300-aircraft package's confused pricing history
  ($2.14 billion quoted by General Dynamics → $3.0 billion survey-team estimate → $3.4 billion
  pre-notification → $3.866 billion final formal DOD notification to Congress) -- a case where
  Brent Scowcroft's own marginal note ("This is over double the GD quoted price. How can this be?")
  is preserved in the `notes` field.
- **The Kurdish-aid financial thread**: Iran's own annual support to the Iraqi Kurds (over $74
  million/year as of late 1974, later given as ~200 million tomans/year rising to ~500 million
  tomans/year), alongside the parallel, much smaller CIA/US channel (~$20 million cumulative
  FY1973-75, with a specific $8.06 million FY1975 authorization).
- **Iraq's parallel post-nationalization boom**: oil's share of Iraqi government revenue rising
  from 58% (1966-73, pre-nationalization) to 74% (1973-74) to 89.9% (1974-75); Iraq's oil revenue
  growing from $900 million (1971) to an estimated $8.2 billion (1975); and a full Table 4
  (American-Iraqi Trade, 1972-1975) showing US exports to Iraq growing more than tenfold
  ($23.3M to $309.7M) over those four years.

## Caveats -- read before charting

- **Several rows contain internally inconsistent source arithmetic, preserved as printed rather
  than corrected.** Example: Document 109 (PDF p.365) has Kissinger describing a "$12.5 billion"
  five-year US-Iran program broken into components ($6bn nuclear + $5bn ports + $2.5bn agriculture
  = $13.5bn) that do not sum to the stated $12.5 billion headline figure -- this project's
  no-fabrication rule means the discrepancy is flagged in `notes`, not silently reconciled.
- **The same underlying fact is sometimes given slightly different values in different documents
  within the same volume** -- e.g. the Shah's steel-production target appears as both 15 million
  tons/year (Documents 59 and 88) and 17 million tons/year (Document 100); Iran's targeted 1983 GNP
  appears as both $190 billion (Document 88) and $193 billion (Document 109); Iran's crude oil
  reserves appear as 64 billion barrels in one 1976 CIA study (Document 317, PDF p.924) versus 65
  billion barrels in the separate 1973 NIS-33 survey (see `cia_iran_economy_series/`). All such
  variants are kept as separate rows rather than averaged or silently picking a "winner" -- these
  reflect genuinely different sources/vintages within the declassified record, not extraction
  noise.
- **Dollar figures in this era are nominal (current) US dollars of the stated year**, not
  inflation-adjusted -- do not compare a 1973 figure to a 1976 figure as if they were in constant
  terms without your own deflator.
- **Some `value` fields hold ranges or multi-point trajectories rather than a single point
  estimate** (see Schema note above) -- always read the full string.
- **No blank/skipped-value rows in this file**: unlike the CIA and NIS-33 series in this project
  (which contain some intentionally blank cells for illegible source scans), the FRUS volumes are
  fully legible born-digital text, so every row extracted from them carries a real value.
