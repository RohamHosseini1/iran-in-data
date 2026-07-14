export interface Citation {
  source_org: string;
  source_url: string;
  access_date: string;
  time_range: string;
  restored_note?: string;
}

export interface ChartIndexEntry {
  chart_id: string;
  title: string;
  title_fa: string;
  category: string;
  category_fa: string;
  description: string;
  year_range: [string, string];
  countries: string[];
  primary_source: string;
  citations: Citation[];
  data_path: string;
  row_count: number;
  status: "new" | "merged";
  merged_into: string | null;
  materialized: boolean;
}

export interface ChartMeta {
  chart_id: string;
  title: string;
  title_fa: string;
  category: string;
  category_fa: string;
  sources: string;
  n_rows: number;
  year_range: [string, string];
  countries: string[];
  citations: Citation[];
}

export interface DataRow {
  country_iso3: string;
  country_name: string;
  year: number;
  value: number;
  unit: string;
  variant_code: string;
  variant_label: string;
  source_dataset: string;
  original_period_label?: string;
}

/** Confidence-scored policy/event annotation joined to a chart. */
export interface ChartEventDetail {
  year: number;
  date: string;
  title: string;
  /**
   * TWO scores, deliberately separate. Collapsing them into one "confidence" is what
   * scored the White Revolution 1/5 against Iran's GDP: its causal channel is diffuse
   * (low attribution) but it is central to the story (high relevance).
   */
  relevance: number;
  attribution: number;
  direction: string;
  relationship: string;
  lag: string;
  lagFa: string;
  justification: string;
  justificationFa: string;
  caveats: string;
  caveatsFa: string;
  description?: string;
  /** Persian title/description from the timeline. The FA site must use these. */
  titleFa?: string;
  descriptionFa?: string;
  sourceUrl?: string;
  sourceName?: string;
}

/** Slim per-chart record shipped to the client for instant search. */
export interface SearchRecord {
  id: string;
  t: string; // title (en)
  tf: string; // title (fa)
  c: string; // category (en)
  cf: string; // category (fa)
  y0: string; // first year
  y1: string; // last year
  n: number; // country count
  s: string; // primary source
}

/** A law/regulation annotation. Persian-first: titleFa is the enacted original. */
export interface ChartLawDetail {
  lawId: string;
  year: number;
  titleFa: string;
  titleEn: string;
  summaryEn: string;
  summaryFa: string;
  /** Should a reader of this chart see this law at all? (drives display order) */
  relevance: number;
  /** Can we actually say it moved this line? (drives the causal claim) */
  attribution: number;
  relationship: string;
  direction: string;
  lag: string;
  lagFa: string;
  justification: string;
  justificationFa: string;
  caveats: string;
  caveatsFa: string;
  /** "specific" = this chart was named; "category" = swept in with its whole domain. */
  scope: "specific" | "category";
}

