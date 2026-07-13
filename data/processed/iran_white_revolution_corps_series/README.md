# White Revolution corps series: Literacy, Health, and Extension/Development corps (1958–2003)

Hand-curated, citation-preserving extraction covering the three rural-mobilization "corps" of the
1963 White Revolution (Enqelab-e Sefid) — the Literacy Corps (Sepah-e Danesh), Health Corps (Sepah-e
Behdasht), and Extension and Development Corps (Sepah-e Tarvij va Abadani) — plus adjoining general
education/land-reform statistics. Harmonized 2026-07-13 from `data/raw/iran-white-revolution-corps/`
(raw sources immutable, unchanged) across four source folders: two Encyclopaedia Iranica articles, a
GFRAS (Global Forum for Rural Advisory Services) country page, and a Wikipedia raw-wikitext extract.
Nothing was interpolated, estimated, or fabricated — including explicitly-flagged **uncited/
"unverified"** figures, which are preserved as printed rather than dropped, per this project's
transparency-over-omission rule.

## Files

| File | Source raw folder | Coverage | What it covers |
|---|---|---|---|
| `literacy_corps_program_totals.csv` | `iranica-literacy-corps` | 1963–1979 (cumulative program totals) | Corpsmen/corpswomen counts, children/adults taught, corps pay rates |
| `literacy_illiteracy_rate.csv` | `iranica-literacy-corps` | 1958, 1966, 1979 | Illiteracy rate by sex (age 15+), factory-worker illiteracy |
| `health_expenditure_series.csv` | `iranica-behdari-health-system` | 1920–1978 | Government health expenditure vs. total government expenditure and oil revenue, immunization coverage |
| `extension_corps_stats.csv` | `gfras-extension-development-corps` | 1964–1965 (+2003 comparison) | EDC service-term structure, fertilizer-adoption figure attributed to EDC |
| `white_revolution_corps_stats.csv` | `wikipedia-white-revolution-corps-stats` | 1963–1978 | Health Corps treatment totals, agricultural production change, literacy rate, school enrollment by level, land-reform beneficiary families |

## Schema

Most files use `year, metric, value, unit, source, country_iso3`. Two deviate, preserving the
source's own framing rather than forcing a false single-year label:
- `literacy_corps_program_totals.csv` and `white_revolution_corps_stats.csv` use
  `period_start, period_end, metric, value, unit, source, country_iso3` (`white_revolution_corps_stats.csv`
  also carries a `corps` column) — because the underlying figures are **cumulative totals across the
  whole 1963–1979 program**, not single-year observations. Do not treat `period_start` as an annual
  data point.
- `literacy_illiteracy_rate.csv` adds a `sex` column (`male`/`female`/`total`).

All rows are `country_iso3 = IRN`.

## Caveats — read before charting

- **Two illiteracy-rate series in this folder do not reconcile with each other, and both are kept
  unreconciled per the no-fabrication rule:**
  - Iranica (`literacy_illiteracy_rate.csv`, sourced to UNESCO Statistical Yearbook 1966 + an
    uncited 1979 figure): illiteracy 67.2% male / 87.8% female (1966) → 44.2% male / 53.0% female (1979).
  - Wikipedia (`white_revolution_corps_stats.csv`): national literacy rate 26% (1963) → 42% (1978) —
    **explicitly marked "unverified"** in the source, with no inline citation in the Wikipedia article
    text itself.
- **Several rows in `white_revolution_corps_stats.csv` are flagged "unverified"** in their `source`
  text: the education-enrollment-by-level figures (kindergarten/elementary/secondary/college
  start/end), the 26%→42% literacy claim, and the 1.5-million-families land-reform figure all lack an
  inline citation in the current Wikipedia article. Preserved as-is for completeness, not treated as
  authoritative without independent corroboration.
- **`health_expenditure_series.csv` has an internal ambiguity, preserved not resolved:** the source
  gives both a "$0.5bn single-year (1974)" health-expenditure figure and a "$1.5bn→$116.5bn cumulative
  1948–74 growth" framing without reconciling the two — both rows are kept, flagged in their own notes.
- **`extension_corps_stats.csv`'s 2003 rows are explicitly modern-era**, not White-Revolution-era —
  kept only as a before/after scale comparison, flagged in the `source` text.
- **Iranica's own Tables 1–3 in the BEHDĀRĪ article (health worker/facility counts, health indicators
  1923–1978) are print-plate images, not machine-readable** — confirmed via DOM inspection (no
  `<table>` elements); could not be extracted. Flagged as a genuine gap, not fabricated around.
- **Retrieval method:** iranicaonline.org and g-fras.org content was retrieved via an interactive
  browser tool where curl/WebFetch returned HTTP 403 (Cloudflare); the Wikipedia file was retrieved
  via the raw wikitext API (`action=raw`) specifically to preserve inline `<ref>` citation markers.

## Sources

- Encyclopaedia Iranica, "LITERACY CORPS" (Farian Sabahi), https://www.iranicaonline.org/articles/literacy-corps-1/
- Encyclopaedia Iranica, "BEHDĀRĪ" (Mohammad Ali Faghih), https://www.iranicaonline.org/articles/behdari/
- GFRAS, Iran country page (world-wide extension study), https://www.g-fras.org/en/about-us/vision-mission/92-world-wide-extension-study/asia/southern-asia/292-iran.html
- Wikipedia, "White Revolution," https://en.wikipedia.org/wiki/White_Revolution (citing Encyclopedia.com
  "White Revolution (1961-1963)" and Britannica "White Revolution (Iran)")

Full manifests: `data/raw/iran-white-revolution-corps/*/manifest.json`.
