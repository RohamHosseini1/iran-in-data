# Iran media history series: cinema, press, and periodicals (1898–1988)

Hand-curated, citation-preserving extraction from two Encyclopaedia Iranica articles. Harmonized
2026-07-13 from `data/raw/iran-media-history/` (raw sources immutable, unchanged). Every row is a
number stated explicitly in the source article's prose, itself traceable to the Iran Statistical
Yearbook, UNESCO reports, or named film-industry scholarship (Naficy, Gaffary, Tahaminezhad).
Nothing was interpolated, estimated, or fabricated.

## Files

| File | Source raw folder | Coverage | What it covers |
|---|---|---|---|
| `cinema_theaters_and_attendance.csv` | `iranica-cinema-history` | 1932–1986 | Movie-house counts (national/Tehran), audience totals, seat counts |
| `film_production_and_industry.csv` | `iranica-cinema-history` | 1941–1982 | Films screened/produced/distributed by origin country, production-company spend, censorship (films inspected/banned/rejected) |
| `press_periodicals_series.csv` | `iranica-press-newspapers` | 1898–1988 | Daily/weekly/monthly newspaper and periodical counts, adult literacy rate by gender (1976) |

## Schema

`year, metric, value, unit, source, country_iso3` — one row per statistic. All rows are
`country_iso3 = IRN`.

## Key finding preserved in the data

Cinema tells a sharp "boom then bust" story entirely from official Iranian statistics: 142 movie
houses (1959) → 453 (1975, explosive Pahlavi-era growth) → 198 (1979, ~255 cinemas burned or
closed in the two years before the revolution) → a partial, smaller recovery to 247 theaters by
1986. Full-length film production similarly rose 25→80 films/year (1959–1971) before a 1979
censorship purge banned 1,800 of 2,000 films inspected that year. The press series shows the same
reversal in periodicals: 198 papers (1976) → 237 (1979–80, pre-university-closures) → 163 (1988).

## Caveats

- **Irregular snapshot years**, concentrated at whatever Statistical Yearbook editions (1976, 1981,
  1986, 1988) or scholarly tables (Gaffary 1973, Naficy 1979/1987) the source article cites — not a
  continuous annual series.
- **Retrieval method:** iranicaonline.org blocks curl/WebFetch (HTTP 403, Cloudflare); retrieved via
  an interactive browser tool, consistent with other iranicaonline.org sources in this project.
- **Unreconciled cross-reference, kept as printed, not corrected:** the cinema article's 1978 TV
  figure (2 million sets, 11M+ viewers, noted in `cinema-i-history.txt`) does not perfectly align in
  framing with the 1974 TV audience-reach figure (15 million) captured in the sibling
  `iran_telecom_communications_series/radio_tv_series.csv`.
- `press_periodicals_series.csv` is a topic-scoped extract of the SAME article used for
  `iran_telecom_communications_series` (postal/telegraph/telephone/radio/TV) — the article covers
  both post/telecom and press/newspapers in one piece. The full article text is stored once at
  `data/raw/iran-telecom-history/iranica-communications-in-persia/communications-in-persia.txt`
  (not duplicated under iran-media-history) — see
  `data/raw/iran-media-history/iranica-press-newspapers/SOURCE_NOTE.txt`.

## Sources

- Encyclopaedia Iranica, "CINEMA i. History of Cinema in Persia" (Farrokh Gaffary),
  https://www.iranicaonline.org/articles/cinema-i/ — manifest:
  `data/raw/iran-media-history/iranica-cinema-history/manifest.json`
- Encyclopaedia Iranica, "COMMUNICATIONS in Persia" (Sreberny-Mohammadi & Mohammadi), press/newspaper
  rows only — manifest: `data/raw/iran-media-history/iranica-press-newspapers/manifest.json`
