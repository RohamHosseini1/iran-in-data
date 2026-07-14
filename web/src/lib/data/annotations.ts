import "server-only";

import fs from "node:fs";
import path from "node:path";

import { readCsvObjects } from "./events";
import type { ChartLawDetail, EraBand } from "./types";

const DATA_ROOT = process.env.IRAN_DATA_ROOT ?? path.resolve(process.cwd(), "..");

/**
 * Two annotation layers sit on top of a chart, and they are deliberately NOT merged:
 *
 *   events -> golden-orange markers   (see events.ts)
 *   laws   -> low-opacity GREY markers (here)
 *   eras   -> shaded bands            (here)
 *
 * Laws are PERSIAN-FIRST: the enacted Persian title is authoritative and is what the
 * Persian site shows verbatim; English shows a translation. A law does not need proven
 * causation to appear -- if it is genuinely related to the measure's field it is listed,
 * with an honest confidence and the mechanism spelled out.
 */

let lawCache: Map<string, ChartLawDetail[]> | null = null;
let eraCache: EraBand[] | null = null;

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
      confidence: Number(r.confidence) || 0,
      relationship: r.relationship_type ?? "",
      direction: r.direction ?? "",
      lag: r.lag_description ?? "",
      justification: r.justification ?? "",
      caveats: r.caveats ?? "",
      scope: (r.scope as ChartLawDetail["scope"]) ?? "category",
    };
    const list = index.get(r.chart_id);
    if (list) list.push(detail);
    else index.set(r.chart_id, [detail]);
  }

  // strongest first (confidence, then a directly-named chart beats a category sweep)
  for (const list of index.values()) {
    list.sort(
      (a, b) =>
        b.confidence - a.confidence ||
        (a.scope === "specific" ? -1 : 1) - (b.scope === "specific" ? -1 : 1) ||
        a.year - b.year
    );
  }
  return index;
}

/**
 * Laws related to one chart, strongest first.
 * A broad law (a VAT act, a currency redenomination) legitimately attaches to many
 * charts, so the caller renders only the top few as markers and lists the remainder
 * below the chart -- nothing is dropped from the data.
 */
export function getChartLaws(chartId: string): ChartLawDetail[] {
  if (!lawCache) lawCache = buildLawIndex();
  return lawCache.get(chartId) ?? [];
}

/** Well-known periods (Revolution, war, sanctions eras) drawn as shaded bands. */
export function getEras(): EraBand[] {
  if (!eraCache) {
    const p = path.join(DATA_ROOT, "timeline", "eras.csv");
    eraCache = fs.existsSync(p)
      ? readCsvObjects(p).map((r) => ({
          eraId: r.era_id,
          country: r.country,
          startYear: Number(String(r.start_date).slice(0, 4)),
          endYear: Number(String(r.end_date).slice(0, 4)),
          title: r.title,
          titleFa: r.title_fa,
          description: r.description,
          descriptionFa: r.description_fa,
          kind: r.kind,
          sourceUrl: r.source_url,
          sourceName: r.source_name,
        })).filter((e) => Number.isFinite(e.startYear) && Number.isFinite(e.endYear))
      : [];
  }
  return eraCache;
}
