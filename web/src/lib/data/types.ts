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
  /** 1–5 strength-of-association score from the correlation registry. */
  confidence: number;
  direction: string;
  relationship: string;
  lag: string;
  justification: string;
  caveats: string;
  description?: string;
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
