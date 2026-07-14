import type { Locale } from "@/lib/i18n/config";

/**
 * Human-readable measure names for the common WDI-style variant labels,
 * replacing raw dataset phrasing like "GDP: linked series (current LCU)".
 * Terms follow standard Persian economic usage (per fa.wikipedia.org:
 * "تعدیل‌شده با تورم" for inflation-adjusted / real values).
 *
 * Unrecognized labels pass through untouched; a proper measure-level naming
 * pass across all 1,842 charts is tracked as its own translation task.
 */
const RULES: {
  pattern: RegExp;
  en: string;
  fa: string;
}[] = [
  {
    pattern: /constant\s+(\d{4}\s+)?(international\s+)?US?\$|constant.*U\.?S\.? dollars/i,
    en: "US dollars, adjusted for inflation",
    fa: "دلار آمریکا، تعدیل‌شده با تورم",
  },
  {
    pattern: /current\s+(international\s+)?US?\$|current.*U\.?S\.? dollars/i,
    en: "US dollars, not adjusted for inflation",
    fa: "دلار آمریکا، بدون تعدیل تورم",
  },
  {
    pattern: /constant\s+LCU/i,
    en: "Local currency, adjusted for inflation",
    fa: "پول ملی، تعدیل‌شده با تورم",
  },
  {
    pattern: /current\s+LCU/i,
    en: "Local currency, not adjusted for inflation",
    fa: "پول ملی، بدون تعدیل تورم",
  },
];

export function friendlyVariantLabel(rawLabel: string, locale: Locale): string {
  for (const rule of RULES) {
    if (rule.pattern.test(rawLabel)) return rule[locale];
  }
  return rawLabel;
}

/**
 * Default measure for a chart. For currency charts the black-market
 * (parallel) rate is the honest headline number, so it wins over the
 * official rate whenever present.
 */
export function pickDefaultVariant(
  variants: { code: string; label: string }[]
): string {
  const parallel = variants.find((v) =>
    /parallel|black[\s_-]?market|بازار\s*آزاد/i.test(`${v.code} ${v.label}`)
  );
  return (parallel ?? variants[0])?.code ?? "";
}
