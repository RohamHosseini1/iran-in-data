/**
 * Persian names (fa.wikipedia.org conventions) for countries that appear as
 * comparators. Seed set covering the current comparator pool; the full
 * translation pass (task) extends this to every country in the archive.
 */
const COUNTRY_FA: Record<string, string> = {
  IRN: "ایران",
  ARG: "آرژانتین",
  DEU: "آلمان",
  ESP: "اسپانیا",
  FRA: "فرانسه",
  GBR: "بریتانیا",
  GRC: "یونان",
  ITA: "ایتالیا",
  KOR: "کره جنوبی",
  NLD: "هلند",
  PRT: "پرتغال",
  RUS: "روسیه",
  SAU: "عربستان سعودی",
  SWE: "سوئد",
  TUR: "ترکیه",
  USA: "ایالات متحده",
  VEN: "ونزوئلا",
  CHN: "چین",
  IND: "هند",
  JPN: "ژاپن",
  IRQ: "عراق",
  PAK: "پاکستان",
  AFG: "افغانستان",
  ARE: "امارات متحده عربی",
  QAT: "قطر",
  KWT: "کویت",
  EGY: "مصر",
  BRA: "برزیل",
  MEX: "مکزیک",
  IDN: "اندونزی",
  NGA: "نیجریه",
  DZA: "الجزایر",
  LBY: "لیبی",
  AZE: "جمهوری آذربایجان",
  ARM: "ارمنستان",
  TKM: "ترکمنستان",
};

export function countryNameFa(iso3: string, fallback: string): string {
  return COUNTRY_FA[iso3] ?? fallback;
}
