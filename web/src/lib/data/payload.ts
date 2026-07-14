import type { DataRow } from "./types";

/**
 * Sub-year (daily/monthly/quarterly) observations, aligned to a shared time
 * axis (epoch ms). Present only when the source rows carry period labels
 * finer than the year, e.g. the daily parallel-FX series.
 */
export interface SubYearSeries {
  /** Epoch ms per observation, ascending. */
  times: number[];
  /** Source period labels aligned to `times` (e.g. "2011/11/26"). */
  labels: string[];
  values: Record<string, Record<string, (number | null)[]>>;
}

/**
 * Compact, serializable form of a chart's dataset for client hydration:
 * value arrays are aligned to the shared `years` axis so the payload stays
 * a fraction of the raw row list's size.
 */
export interface ChartPayload {
  years: number[];
  variants: { code: string; label: string; unit: string }[];
  countries: { iso: string; name: string }[];
  values: Record<string, Record<string, (number | null)[]>>;
  subYear?: SubYearSeries;
}

/**
 * Parse an original_period_label into epoch ms, but only if it is finer than
 * annual. Accepts 2011/11/26, 2011-11-26, 2011-11, 2011M11, 2011Q3. Returns
 * null for plain years and anything unparseable (incl. labels whose year
 * disagrees with the row's Gregorian year, e.g. Jalali-labelled periods).
 */
function parsePeriodMs(label: string, rowYear: number): number | null {
  const s = label.trim();
  let m = s.match(/^(\d{4})[/\-.](\d{1,2})(?:[/\-.](\d{1,2}))?$/);
  let y: number, mo: number, d: number;
  if (m) {
    y = Number(m[1]);
    mo = Number(m[2]);
    d = m[3] ? Number(m[3]) : 15;
  } else if ((m = s.match(/^(\d{4})M(\d{1,2})$/i))) {
    y = Number(m[1]);
    mo = Number(m[2]);
    d = 15;
  } else if ((m = s.match(/^(\d{4})Q([1-4])$/i))) {
    y = Number(m[1]);
    mo = (Number(m[2]) - 1) * 3 + 2;
    d = 15;
  } else {
    return null;
  }
  if (mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  if (Math.abs(y - rowYear) > 1) return null; // non-Gregorian label; distrust
  // Anchor at noon UTC so the local calendar date matches the source label
  // in every viewer timezone within ±11h.
  return Date.UTC(y, mo - 1, d, 12);
}

export function buildChartPayload(rows: DataRow[]): ChartPayload {
  const years = [...new Set(rows.map((r) => r.year))].sort((a, b) => a - b);
  const yearIndex = new Map(years.map((y, i) => [y, i]));

  const variants = new Map<string, { code: string; label: string; unit: string }>();
  const countries = new Map<string, string>();
  const values: Record<string, Record<string, (number | null)[]>> = {};

  for (const r of rows) {
    if (!variants.has(r.variant_code)) {
      variants.set(r.variant_code, {
        code: r.variant_code,
        label: r.variant_label || r.variant_code || "value",
        unit: r.unit,
      });
    }
    if (!countries.has(r.country_iso3)) {
      countries.set(r.country_iso3, r.country_name);
    }
    const byCountry = (values[r.variant_code] ??= {});
    const arr = (byCountry[r.country_iso3] ??= new Array(years.length).fill(null));
    arr[yearIndex.get(r.year)!] = r.value;
  }

  return {
    years,
    variants: [...variants.values()],
    countries: [...countries.entries()]
      .map(([iso, name]) => ({ iso, name }))
      .sort((a, b) => (a.iso === "IRN" ? -1 : b.iso === "IRN" ? 1 : a.name.localeCompare(b.name))),
    values,
    subYear: buildSubYear(rows, years.length),
  };
}

function buildSubYear(rows: DataRow[], yearCount: number): SubYearSeries | undefined {
  const parsed: { ms: number; label: string; row: DataRow }[] = [];
  for (const r of rows) {
    if (!r.original_period_label) continue;
    const ms = parsePeriodMs(r.original_period_label, r.year);
    if (ms != null) parsed.push({ ms, label: r.original_period_label.trim(), row: r });
  }
  // Only a real sub-year series if labels parse for most rows AND the time
  // axis is meaningfully finer than annual.
  if (!parsed.length || parsed.length < rows.length * 0.8) return undefined;
  const distinct = new Map<number, string>();
  for (const p of parsed) if (!distinct.has(p.ms)) distinct.set(p.ms, p.label);
  if (distinct.size < yearCount * 2) return undefined;

  const times = [...distinct.keys()].sort((a, b) => a - b);
  const labels = times.map((t) => distinct.get(t)!);
  const timeIndex = new Map(times.map((t, i) => [t, i]));

  const values: Record<string, Record<string, (number | null)[]>> = {};
  for (const p of parsed) {
    const byCountry = (values[p.row.variant_code] ??= {});
    const arr = (byCountry[p.row.country_iso3] ??= new Array(times.length).fill(null));
    arr[timeIndex.get(p.ms)!] = p.row.value;
  }
  return { times, labels, values };
}
