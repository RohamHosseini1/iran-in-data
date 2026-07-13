# USAID / Point Four era -- Rockefeller Archive Center research reports (1948-1963)

Two short Rockefeller Archive Center (RAC) "Research Reports" -- born-digital PDFs, extracted via
`pdftotext -layout` (no OCR needed) -- mined for every dated, cited economic statistic embedded in
their prose. **15 rows total.**

## Important caveat: these are secondary sources, not primary documents

Unlike the rest of `data/raw/`'s primary-source folders (FRUS volumes, declassified CIA reports,
NIS 33), these two RAC publications are **contemporary (2017/2025) academic research reports** by
PhD students (Gregory Brew, Georgetown; Jack Roush, LSE) summarizing their own archival research
at the RAC. They cite primary sources (State Department cables, Ford Foundation grant files,
FRUS volumes, oral histories) but are not primary documents themselves. They were included in this
task's assigned folder list (`data/raw/usaid-point-four-iran/`) specifically as representative
secondary-literature coverage of the US Point Four technical-assistance program and Ford
Foundation/Harvard Advisory Group activity in 1950s-60s Iran -- a topic not otherwise covered by
this project's primary-source holdings. Per each raw folder's own `manifest.json` notes, both are
explicitly logged as "secondary historical research report[s]... not itself a primary government
document."

**This folder is thin by design, not by extraction failure.** Both reports are short (8pp and
13pp) narrative political/institutional histories of the Ford Foundation's Harvard Advisory Group
and the 1957 Motheral land-reform report, respectively -- they are not statistical yearbooks or
data-dense diplomatic cables, so most of their content is qualitative analysis with only
occasional dated dollar or headcount figures embedded in the prose. Every such figure that exists
in either document has been extracted below; nothing further was omitted.

## Schema

`date_label, year, category, subcategory, value, unit, notes, country_iso3, source_dataset, citation`

Same schema as this project's other primary-source extraction CSVs. `country_iso3` is always
`IRN`. `citation` gives the RAC report's author/title/year and the printed page number the figure
appeared on.

## The two source documents

| Document | Rows | Raw file |
|---|---|---|
| Gregory Brew, "Economic Expertise and Rural Improvement in Iran, 1948-1963" (2017) | 8 | `data/raw/usaid-point-four-iran/economic-expertise-rural-improvement/29283.pdf` |
| Jack Roush, "The Motheral Report and Land Reform in Iran, 1952-1963" (2025) | 7 | `data/raw/usaid-point-four-iran/motheral-report-land-reform/45044.pdf` |

## What's in it

- **Brew (2017)**, on the Ford Foundation's Harvard Advisory Group (HAG) and the Plan
  Organization's Economic Bureau: the oil consortium's revenue growth from $33 million (1955) to
  $338 million (1960) that funded the Second Seven Year Plan; the Plan's original $930 million /
  70 billion-rial budget, later raised to $1.1 billion / 84 billion rials; the Ford Foundation's
  $1.2 million three-year grant funding the HAG team (1957-onward); the August 1958
  Hansen/Farmanfarmaian projection that Iranian state spending would exceed revenues by $933
  million by September 1962; the observation that after "several years and $505 million" (by
  1959) it was difficult to measure what the Plan Organization had achieved; and the Third Plan's
  (from September 1962) targeted 6%/year average GNP growth rate.
- **Roush (2025)**, on the 1957 Motheral Report and its influence on the 1961 Amini and 1963 White
  Revolution land reforms: the claim (cited to Daniel Craig, 1978) that up to 60% of Iran's
  population lived and worked as tenant farmers into the early 1960s; the Shah's 1951 firman
  redistributing 2,100 villages from his own landholdings; the 1952 Point Four-linked program's
  limited initial scope (3,000 of an estimated 50,000 villages); Motheral's proposed 1958-1962
  five-year timeline to redistribute land in over 15,000 villages (roughly one-third of the
  country's villages); the 1958 founding of the Industrial Development Bank of Iran (later
  IMDBI) and the 1958-1960 establishment of the Central Bank of Iran; and the Shah's own June
  1963 framing of the White Revolution as "emancipating fifteen million Iranians."

## Caveats

- Several rows have a blank or non-numeric `value` (e.g. "institutional founding (no dollar figure
  printed)", "qualitative (no dollar figure printed)") where the source describes an event
  precisely dated but without an accompanying dollar or count figure -- these rows exist to record
  *that* the source discusses the event with a citation, not to imply a missing number that should
  be filled in later.
- The 1955-1960 oil-revenue figure ($33M -> $338M) and the "up to 60%" tenant-farmer figure are
  both themselves citations *within* the RAC report to other scholarly works (Gasiorowski 1991;
  Heiss 1994; Craig 1978) -- this project is one citation-hop removed from those original sources.
  If a primary or more authoritative figure for either statistic is later found elsewhere in this
  project's holdings, that source should be preferred over this one.
- No rows from this folder should be treated as having the same evidentiary weight as the FRUS,
  CIA, or NIS-33 primary-source series elsewhere in this project -- flag this folder's
  `source_dataset` (`usaid-point-four-rac-research-reports`) distinctly in any downstream
  source-reliability tagging.
