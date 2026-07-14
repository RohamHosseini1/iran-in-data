/**
 * Calendar display transforms for ANNUAL data. Chart years are stored as
 * Gregorian integers; these are render-time label conversions only.
 *
 * For annual series the standard convention maps Gregorian year Y to the
 * Jalali year that begins in March of Y (Y − 621). The short-lived Imperial
 * calendar (introduced 1976, abandoned 1978) counts from Cyrus's accession:
 * Imperial = Jalali + 1180.
 */
export type CalendarSystem = "gregorian" | "jalali" | "imperial";

const PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹";

export function toPersianDigits(value: string | number): string {
  return String(value).replace(/[0-9]/g, (d) => PERSIAN_DIGITS[Number(d)]);
}

export function formatYearFor(
  calendar: CalendarSystem,
  { persianDigits = false }: { persianDigits?: boolean } = {}
): (year: number) => string {
  const digits = persianDigits ? toPersianDigits : String;
  switch (calendar) {
    case "jalali":
      return (y) => digits(y - 621);
    case "imperial":
      return (y) => digits(y + 559);
    default:
      return (y) => digits(y);
  }
}

export const calendarLabels: Record<
  CalendarSystem,
  { en: string; fa: string }
> = {
  gregorian: { en: "Gregorian", fa: "میلادی" },
  jalali: { en: "Solar Hejri", fa: "هجری خورشیدی" },
  imperial: { en: "Iranian Imperial", fa: "شاهنشاهی" },
};
