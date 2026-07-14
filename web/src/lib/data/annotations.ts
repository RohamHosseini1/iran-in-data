import "server-only";

import fs from "node:fs";
import path from "node:path";

import { readCsvObjects } from "./events";
import type { ChartLawDetail } from "./types";

const DATA_ROOT = process.env.IRAN_DATA_ROOT ?? path.resolve(process.cwd(), "..");

/**
 * Two annotation layers sit on top of a chart, and they are deliberately NOT merged:
 *
 *   events -> golden-orange markers   (see events.ts)
 *   laws   -> low-opacity GREY markers (here)
 *
 * Laws are PERSIAN-FIRST: the enacted Persian title is authoritative and is what the
 * Persian site shows verbatim; English shows a translation. A law does not need proven
 * causation to appear -- if it is genuinely related to the measure's field it is listed,
 * with an honest confidence and the mechanism spelled out.
 */

let lawCache: Map<string, ChartLawDetail[]> | null = null;

function buildLawIndex(): Map<string, ChartLawDetail[]> {
  const linksPath = path.join(DATA_ROOT, "data", "processed", "law_chart_links.csv");
  const index = new Map<string, ChartLawDetail[]>();
  if (!fs.existsSync(linksPath)) return index;

  // English titles/summaries land in a separate translation file; join if present.
  const trPath = path.join(DATA_ROOT, "data", "processed", "laws", "law_translations.csv");
  const tr = new Map<string, { en: string; summaryEn: string; summaryFa: string }>();
  if (fs.existsSync(trPath)) {
    for (const r of readCsvObjects(trPath)) {
      tr.set(r.law_id, {
        en: r.law_title_en ?? "",
        summaryEn: r.law_summary_en ?? "",
        summaryFa: r.law_summary_fa ?? "",
      });
    }
  }

  for (const r of readCsvObjects(linksPath)) {
    const year = Number(String(r.law_date).slice(0, 4));
    if (!Number.isFinite(year)) continue;
    const t = tr.get(r.law_id);
    const detail: ChartLawDetail = {
      lawId: r.law_id,
      year,
      titleFa: r.law_title_fa ?? "",
      titleEn: t?.en || r.law_title_en || "",
      summaryEn: t?.summaryEn || r.law_summary_en || "",
      summaryFa: t?.summaryFa || r.law_summary_fa || "",
      correlation: Number(r.correlation) || 0,
      expectedCausation: Number(r.expected_causation) || 0,
      relationship: r.relationship_type ?? "",
      direction: r.direction ?? "",
      lag: r.lag_en ?? "",
      lagFa: r.lag_fa ?? "",
      justification: r.justification_en ?? "",
      justificationFa: r.justification_fa ?? "",
      caveats: r.caveats_en ?? "",
      caveatsFa: r.caveats_fa ?? "",
      scope: (r.scope as ChartLawDetail["scope"]) ?? "category",
    };
    const list = index.get(r.chart_id);
    if (list) list.push(detail);
    else index.set(r.chart_id, [detail]);
  }

  // Chronological: every law is drawn, so the markers must read left-to-right and the
  // numbered log must line up with them. (Confidence-sorting made sense only while a
  // cap meant "which ones get drawn"; there is no cap now.)
  for (const list of index.values()) {
    list.sort(
      (a, b) =>
        a.year - b.year ||
        b.correlation - a.correlation ||
        a.titleEn.localeCompare(b.titleEn)
    );
  }
  return index;
}

/** Laws related to one chart, chronological. Every one is drawn and listed. */
export function getChartLaws(chartId: string): ChartLawDetail[] {
  if (!lawCache) lawCache = buildLawIndex();
  return lawCache.get(chartId) ?? [];
}

