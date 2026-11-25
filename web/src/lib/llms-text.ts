import { getCatalog, getChartEntry } from "@/lib/data/catalog";
import { locales } from "@/lib/i18n/config";

const BASE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000";

const FEATURED_IDS = [
  "wdi__NY.GDP.MKTP",
  "fx__official_vs_parallel_gap_irn",
  "wdi__FP.CPI.TOTL",
  "wdi__SP.POP",
  "weo__ppp_share_world_gdp",
  "iran_fx__usd_irr_parallel_rate_daily_2011_2026",
];

function chartPage(locale: string, chartId: string): string {
  return `${BASE_URL}/${locale}/charts/${encodeURIComponent(chartId)}`;
}

function chartCsv(chartId: string): string {
  return `${BASE_URL}/api/charts/${encodeURIComponent(chartId)}/csv`;
}

/** Short map for agents. Every URL here is meant to be fetched. */
export function llmsTxt(): string {
  const catalog = getCatalog();
  const featured = FEATURED_IDS.flatMap((id) => {
    const entry = getChartEntry(id);
    return entry ? [`- ${entry.title}: ${chartPage("en", id)}`] : [];
  });

  return [
    "# Iran in Data",
    "",
    "> An open, cited encyclopedia of Iran's economic and social history in charts.",
    "> Compiled by Roham Hosseini (https://rohamhosseini.com). Data compilation: CC BY 4.0.",
    "",
    "Fetch these URLs directly. robots.txt allows every user agent, and every chart page is in the sitemap.",
    "",
    "## Locales",
    "",
    `- English: ${BASE_URL}/en`,
    `- فارسی: ${BASE_URL}/fa`,
    "",
    "## Browse",
    "",
    `- Chart directory: ${BASE_URL}/en/charts`,
    `- فهرست نمودارها: ${BASE_URL}/fa/charts`,
    `- License and attribution: ${BASE_URL}/en/attributions`,
    `- Sitemap: ${BASE_URL}/sitemap.xml`,
    `- Every chart URL: ${BASE_URL}/llms-full.txt`,
    "",
    "## Datasets",
    "",
    `The catalog currently lists ${catalog.length.toLocaleString("en-US")} charts.`,
    "",
    `- Chart catalog (metadata, citations, year range, countries; no data rows): ${BASE_URL}/api/catalog`,
    `- Search index: ${BASE_URL}/api/search-index`,
    "- One chart's CSV: /api/charts/{chart_id}/csv",
    "- One chart's page: /{locale}/charts/{chart_id} for locale en or fa",
    "",
    "## Featured series",
    "",
    ...featured,
    "",
    "## Notes",
    "",
    "- Prefer the catalog, the search index, and the sitemap over guessing paths.",
    "- Attribute the original source in each chart's citations, and Roham Hosseini / Iran in Data (iranindata.org).",
    "- Upstream sources may carry their own terms. The CC BY 4.0 license covers this compilation.",
    "- Source repository, including the raw files: https://github.com/RohamHosseini1/iran-in-data",
    "",
  ].join("\n");
}

/** One URL per line for the pages, the CSV files, and the index endpoints. */
export function llmsFullTxt(): string {
  const catalog = getCatalog();
  const lines = [
    "# Iran in Data: full URL list",
    "",
    `${BASE_URL}/en`,
    `${BASE_URL}/fa`,
    `${BASE_URL}/en/charts`,
    `${BASE_URL}/fa/charts`,
    `${BASE_URL}/en/attributions`,
    `${BASE_URL}/fa/attributions`,
    `${BASE_URL}/api/catalog`,
    `${BASE_URL}/api/search-index`,
    `${BASE_URL}/sitemap.xml`,
    `${BASE_URL}/robots.txt`,
    `${BASE_URL}/llms.txt`,
    "",
  ];

  for (const entry of catalog) {
    for (const locale of locales) {
      lines.push(chartPage(locale, entry.chart_id));
    }
    lines.push(chartCsv(entry.chart_id));
  }
  lines.push("");
  return lines.join("\n");
}
