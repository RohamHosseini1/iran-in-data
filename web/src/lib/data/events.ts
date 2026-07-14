import "server-only";

import fs from "node:fs";
import path from "node:path";

import type { ChartEventDetail } from "./types";

const DATA_ROOT = process.env.IRAN_DATA_ROOT ?? path.resolve(process.cwd(), "..");

interface CorrelationRow {
  chart_id: string;
  event_date: string;
  event_title: string;
  event_source_file: string;
  relationship_type: string;
  confidence: string;
  direction: string;
  lag_description: string;
  justification: string;
  caveats: string;
}

let correlationCache: CorrelationRow[] | null = null;
const timelineCache = new Map<string, Map<string, { description: string; url: string; source: string }>>();

function parseCsvRows(text: string): string[][] {
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
        } else inQuotes = false;
      } else field += ch;
    } else if (ch === '"') inQuotes = true;
    else if (ch === ",") {
      row.push(field);
      field = "";
    } else if (ch === "\n" || ch === "\r") {
      if (ch === "\r" && text[i + 1] === "\n") i++;
      row.push(field);
      field = "";
      if (row.length > 1 || row[0] !== "") rows.push(row);
      row = [];
    } else field += ch;
  }
  if (field !== "" || row.length > 0) {
    row.push(field);
    if (row.length > 1 || row[0] !== "") rows.push(row);
  }
  return rows;
}

function readCsvObjects(filePath: string): Record<string, string>[] {
  const [header, ...records] = parseCsvRows(fs.readFileSync(filePath, "utf-8"));
  return records.map((r) =>
    Object.fromEntries(header.map((h, i) => [h, r[i] ?? ""]))
  );
}

function getCorrelations(): CorrelationRow[] {
  if (!correlationCache) {
    const dir = path.join(DATA_ROOT, "data", "processed");
    correlationCache = fs
      .readdirSync(dir)
      .filter((f) => f.startsWith("policy_chart_correlations_") && f.endsWith(".csv"))
      .flatMap((f) => readCsvObjects(path.join(dir, f)) as unknown as CorrelationRow[]);
  }
  return correlationCache;
}

function getTimelineDetails(sourceFile: string) {
  if (!timelineCache.has(sourceFile)) {
    const map = new Map<string, { description: string; url: string; source: string }>();
    const full = path.join(DATA_ROOT, sourceFile);
    if (fs.existsSync(full)) {
      for (const row of readCsvObjects(full)) {
        map.set(`${row.date}|${row.title}`, {
          description: row.description ?? "",
          url: row.source_url ?? "",
          source: row.source_name ?? "",
        });
      }
    }
    timelineCache.set(sourceFile, map);
  }
  return timelineCache.get(sourceFile)!;
}

/** Confidence-scored policy/event annotations for one chart, oldest first. */
export function getChartEvents(chartId: string): ChartEventDetail[] {
  return getCorrelations()
    .filter((c) => c.chart_id === chartId)
    .map((c) => {
      const detail = getTimelineDetails(c.event_source_file).get(
        `${c.event_date}|${c.event_title}`
      );
      return {
        year: Number(c.event_date.slice(0, 4)),
        date: c.event_date,
        title: c.event_title,
        confidence: Number(c.confidence) || 0,
        direction: c.direction,
        relationship: c.relationship_type,
        lag: c.lag_description,
        justification: c.justification,
        caveats: c.caveats,
        description: detail?.description,
        sourceUrl: detail?.url,
        sourceName: detail?.source,
      };
    })
    .filter((e) => Number.isFinite(e.year))
    .sort((a, b) => a.year - b.year);
}
