# Policy & Event Timeline

Curated, source-cited datasets of policy decisions, sanctions, political events, and economic
shocks — the layer meant to sit alongside every chart so a researcher can see *why* a series
moved when it did.

## Files

- `iran.csv` — primary focus (see file for current row count/date range; expanded separately from this round)
- `south-korea.csv` — 22 events, 1950–2020
- `turkey.csv` — 19 events, 1958–2023
- `saudi-arabia.csv` — 22 events, 1938–2020
- `venezuela.csv` — 32 events, 1943–2023
- `united-states.csv` — 35 events, 1913–2022
- `ussr-russia.csv` — 33 events, 1917–2022 (country code `SUN` pre-1991, `RUS` from the 1991 dissolution onward)
- `spain.csv` — 21 events, 1936–2013
- `portugal.csv` — 18 events, 1933–2015
- `greece.csv` — 24 events, 1936–2018
- `argentina.csv` — 37 events, 1930–2023 (serial currency-crisis comparator; includes the INDEC statistics-falsification scandal, 2007–2015)
- `global.csv` — 25 events — world-level shocks affecting multiple countries simultaneously (oil shocks, GFC, COVID, JCPOA, etc.)

## Schema

| column | notes |
|---|---|
| `date` | YYYY-MM-DD (or YYYY-MM/YYYY if only that precision is known) |
| `country` | ISO3, or `GLOBAL` for world-level events |
| `event_type` | one of: policy-proposed, policy-enacted, policy-repealed, sanction-imposed, sanction-lifted, political-event, economic-event, catastrophe, institutional-change |
| `title` | short headline |
| `description` | 1-3 sentences, factual |
| `economic_domains` | semicolon-separated: fx, inflation, oil, trade, housing, food, banking, fiscal, labor |
| `source_url` | the actual source consulted — every row must have one |
| `source_name` | human-readable source name |

## Curation rules (see `docs/bookkeeping.md` for full policy)

- Every fact is verified against a source before being written — nothing from memory alone.
- MEK/NCRI-affiliated outlets are never used as sources (see bookkeeping.md § Source reliability).
  During curation, `ncr-iran.org`, `iranfocus.com`, and `mojahedin.org` all surfaced in general
  search results and were explicitly excluded in favor of primary/official/mainstream-academic
  alternatives for the same facts.
- Preferred source hierarchy for Iran: primary government/legal texts > IMF/World Bank/OFAC/State
  Dept documents > declassified CIA assessments > Encyclopaedia Iranica/Britannica > mainstream
  press. Wikipedia is used only as a cross-check for well-established, uncontroversial dates, never
  as the sole citation for a contested claim.
- Contested/wide-ranging estimates (e.g. bonyad share of Iran's GDP) are NOT put in this timeline
  as point facts — they're documented separately as a range with all sources attributed
  (see `data/raw/iran-bonyad-estimates/`).
