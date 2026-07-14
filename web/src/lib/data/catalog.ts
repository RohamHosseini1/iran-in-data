import "server-only";

import fs from "node:fs";
import path from "node:path";

import type {
  ChartIndexEntry,
  ChartMeta,
  DataRow,
  SearchRecord,
} from "./types";

/**
 * The app lives in web/ inside the data repo; chart data sits one level up
 * in data/charts and catalog/. All reads happen at build time (full static
 * generation), so nothing outside web/ needs to be bundled for runtime.
 */
const DATA_ROOT = process.env.IRAN_DATA_ROOT ?? path.resolve(process.cwd(), "..");

let catalogCache: ChartIndexEntry[] | null = null;

export function getCatalog(): ChartIndexEntry[] {
  if (!catalogCache) {
    const raw = fs.readFileSync(
      path.join(DATA_ROOT, "catalog", "CHARTS_INDEX.json"),
      "utf-8"
    );
    const all = JSON.parse(raw) as ChartIndexEntry[];
    catalogCache = all.filter((e) => e.materialized && e.status !== "merged");
  }
  return catalogCache;
}

export function getChartEntry(chartId: string): ChartIndexEntry | undefined {
  return getCatalog().find((e) => e.chart_id === chartId);
}

export function getChartMeta(chartId: string): ChartMeta {
  const raw = fs.readFileSync(
    path.join(DATA_ROOT, "data", "charts", chartId, "meta.json"),
    "utf-8"
  );
  return JSON.parse(raw) as ChartMeta;
}

export function getChartData(chartId: string): DataRow[] {
  const raw = fs.readFileSync(
    path.join(DATA_ROOT, "data", "charts", chartId, "data.csv"),
    "utf-8"
  );
  return parseCsv(raw);
}

export function getCategories(): { name: string; nameFa: string; count: number }[] {
  const seen = new Map<string, { name: string; nameFa: string; count: number }>();
  for (const e of getCatalog()) {
    const existing = seen.get(e.category);
    if (existing) existing.count += 1;
    else seen.set(e.category, { name: e.category, nameFa: e.category_fa, count: 1 });
  }
  return [...seen.values()].sort((a, b) => b.count - a.count);
}

export function getSearchIndex(): SearchRecord[] {
  return getCatalog().map((e) => ({
    id: e.chart_id,
    t: e.title,
    tf: e.title_fa,
    c: e.category,
    cf: e.category_fa,
    y0: e.year_range?.[0] ?? "",
    y1: e.year_range?.[1] ?? "",
    n: e.countries?.length ?? 0,
    s: e.primary_source,
  }));
}

/** Minimal RFC-4180 CSV parser (quoted fields, embedded commas/newlines). */
function parseCsvRaw(text: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let field = "";
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (inQuotes) {
      if (ch === '"') {
        if (text[i + 1] === '"') {
          field += '"';
          i++;
        } else {
          inQuotes = false;
        }
      } else {
        field += ch;
      }
    } else if (ch === '"') {
      inQuotes = true;
    } else if (ch === ",") {
      row.push(field);
      field = "";
    } else if (ch === "\n" || ch === "\r") {
      if (ch === "\r" && text[i + 1] === "\n") i++;
      row.push(field);
      field = "";
      if (row.length > 1 || row[0] !== "") rows.push(row);
      row = [];
    } else {
      field += ch;
    }
  }
  if (field !== "" || row.length > 0) {
    row.push(field);
    if (row.length > 1 || row[0] !== "") rows.push(row);
  }
  return rows;
}

function parseCsv(text: string): DataRow[] {
  const [header, ...records] = parseCsvRaw(text);
  const col = (name: string) => header.indexOf(name);
  const iIso = col("country_iso3");
  const iName = col("country_name");
  const iYear = col("year");
  const iValue = col("value");
  const iUnit = col("unit");
  const iVCode = col("variant_code");
  const iVLabel = col("variant_label");
  const iSource = col("source_dataset");
  const iPeriod = col("original_period_label");

  const rows: DataRow[] = [];
  for (const r of records) {
    const year = Number(r[iYear]);
    const value = Number(r[iValue]);
    if (!Number.isFinite(year) || !Number.isFinite(value)) continue;
    rows.push({
      country_iso3: r[iIso],
      country_name: r[iName],
      year,
      value,
      unit: iUnit >= 0 ? r[iUnit] : "",
      variant_code: iVCode >= 0 ? r[iVCode] : "",
      variant_label: iVLabel >= 0 ? r[iVLabel] : "",
      source_dataset: iSource >= 0 ? r[iSource] : "",
      original_period_label: iPeriod >= 0 ? r[iPeriod] : undefined,
    });
  }
  return rows;
}
