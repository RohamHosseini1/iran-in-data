/**
 * Unit display: the headline number must carry its unit inline, at the same
 * visual weight ("42.1%", "2.5B USD", «۲٫۵ میلیارد دلار آمریکا») — never buried
 * in a caption below. Raw unit strings in the data are heterogeneous, so this
 * pattern-matches the common families and falls back to a cleaned raw string.
 */

export interface InlineUnit {
  text: string;
  /** True for symbols that attach without a space ("%"). */
  tight?: boolean;
}

interface UnitRule {
  test: RegExp;
  en: InlineUnit;
  fa: InlineUnit;
}

const RULES: UnitRule[] = [
  { test: /rials? per US\$|IRR per USD/i, en: { text: "IRR / USD" }, fa: { text: "ریال به ازای دلار" } },
  { test: /IRR per coin/i, en: { text: "IRR / coin" }, fa: { text: "ریال به ازای سکه" } },
  { test: /billion rials/i, en: { text: "billion IRR" }, fa: { text: "میلیارد ریال" } },
  { test: /rial|IRR/i, en: { text: "IRR" }, fa: { text: "ریال" } },
  { test: /toman/i, en: { text: "toman" }, fa: { text: "تومان" } },
  // Percent outranks currency: "(annual %)" or "(% of GDP)" is a share even
  // when a dollar denomination is mentioned alongside.
  { test: /%|percent|درصد/i, en: { text: "%", tight: true }, fa: { text: "درصد" } },
  { test: /US\$|USD|dollar/i, en: { text: "USD" }, fa: { text: "دلار آمریکا" } },
  { test: /kcal\/cap\/d/i, en: { text: "kcal / day" }, fa: { text: "کیلوکالری در روز" } },
  { test: /g\/cap\/d/i, en: { text: "g / day" }, fa: { text: "گرم در روز" } },
  { test: /kg\/ha/i, en: { text: "kg / ha" }, fa: { text: "کیلوگرم بر هکتار" } },
  { test: /kg\/cap|^kg$|kilogram/i, en: { text: "kg" }, fa: { text: "کیلوگرم" } },
  { test: /^1000 t$|thousand (metric )?tons/i, en: { text: "kt" }, fa: { text: "هزار تن" } },
  { test: /^t$|metric tons?|tonnes?/i, en: { text: "t" }, fa: { text: "تن" } },
  { test: /^ha$|hectare/i, en: { text: "ha" }, fa: { text: "هکتار" } },
  { test: /barrel|BOE/i, en: { text: "bbl" }, fa: { text: "بشکه" } },
  { test: /persons?|people/i, en: { text: "people" }, fa: { text: "نفر" } },
  // Headline readings are always Iran's series: LCU means the rial.
  { test: /LCU|domestic currency|^SLC$/i, en: { text: "IRR" }, fa: { text: "ریال" } },
  { test: /=\s*100|index|PMI/i, en: { text: "index" }, fa: { text: "شاخص" } },
  { test: /years?$/i, en: { text: "years" }, fa: { text: "سال" } },
];

/** Short inline unit for headline numbers; null when there is no unit. */
export function unitInline(
  unit: string | undefined,
  locale: "en" | "fa"
): InlineUnit | null {
  const raw = (unit ?? "").trim();
  if (!raw) return null;
  for (const rule of RULES) {
    if (rule.test.test(raw)) return locale === "fa" ? rule.fa : rule.en;
  }
  // Fallback: the raw unit, minus pipeline parentheticals like "(computed)".
  const cleaned = raw.replace(/\((computed|estimated)\)/gi, "").trim();
  return cleaned ? { text: cleaned } : null;
}

/** Trailing parenthetical of a series label — where WDI-style labels carry
    the unit when the data's unit column is empty ("Inflation … (annual %)"). */
export function labelUnitText(label: string | undefined): string {
  const m = (label ?? "").match(/\(([^()]+)\)\s*$/);
  return m ? m[1].trim() : "";
}

/** Unit inferred from a series label's trailing parenthetical. Pattern rules
    only — no raw fallback, so an unrecognized parenthetical yields nothing
    rather than a repeated label fragment. */
export function unitFromLabel(
  label: string | undefined,
  locale: "en" | "fa"
): InlineUnit | null {
  const inner = labelUnitText(label);
  if (!inner) return null;
  for (const rule of RULES) {
    if (rule.test.test(inner)) return locale === "fa" ? rule.fa : rule.en;
  }
  return null;
}

const FA_NUM: Intl.NumberFormatOptions = { maximumFractionDigits: 2 };

/**
 * Persian headline-number format, mirroring formatReading(): full digits
 * below a billion (Persian digits + ٬ separators), scale words above:
 * 2.5e9 → «۲٫۵ میلیارد».
 */
export function formatReadingFa(value: number): string {
  const abs = Math.abs(value);
  if (abs >= 1e12)
    return (value / 1e12).toLocaleString("fa-IR", FA_NUM) + " تریلیون";
  if (abs >= 1e9)
    return (value / 1e9).toLocaleString("fa-IR", FA_NUM) + " میلیارد";
  if (abs >= 100) return Math.round(value).toLocaleString("fa-IR");
  return value.toLocaleString("fa-IR", FA_NUM);
}

/** Full-precision table-cell format: 4238190.5 → "4,238,190.5". */
export function formatFull(value: number): string {
  if (value !== 0 && Math.abs(value) < 1)
    return value.toLocaleString("en-US", { maximumSignificantDigits: 3 });
  return value.toLocaleString("en-US", { maximumFractionDigits: 2 });
}
