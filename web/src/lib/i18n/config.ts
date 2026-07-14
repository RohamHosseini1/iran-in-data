export const locales = ["en", "fa"] as const;

export type Locale = (typeof locales)[number];

export const defaultLocale: Locale = "en";

export const localeDirection: Record<Locale, "ltr" | "rtl"> = {
  en: "ltr",
  fa: "rtl",
};

export const localeLabel: Record<Locale, string> = {
  en: "English",
  fa: "فارسی",
};

export function isLocale(value: string): value is Locale {
  return (locales as readonly string[]).includes(value);
}
