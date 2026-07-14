/**
 * Search-text normalization for bilingual matching: folds Arabic-presentation
 * characters into their Persian forms, strips ZWNJ/tatweel, converts
 * Persian/Arabic-Indic digits to Latin, lowercases Latin.
 */
const CHAR_FOLD: Record<string, string> = {
  "ي": "ی", // ي → ی
  "ك": "ک", // ك → ک
  "ة": "ه", // ة → ه
  "أ": "ا", // أ → ا
  "إ": "ا", // إ → ا
  "‌": "", // ZWNJ
  "ـ": "", // tatweel
};

const PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹";
const ARABIC_DIGITS = "٠١٢٣٤٥٦٧٨٩";

export function normalizeSearchText(input: string): string {
  let out = "";
  for (const ch of input.toLowerCase()) {
    if (ch in CHAR_FOLD) {
      out += CHAR_FOLD[ch];
      continue;
    }
    const pIdx = PERSIAN_DIGITS.indexOf(ch);
    if (pIdx >= 0) {
      out += String(pIdx);
      continue;
    }
    const aIdx = ARABIC_DIGITS.indexOf(ch);
    if (aIdx >= 0) {
      out += String(aIdx);
      continue;
    }
    out += ch;
  }
  return out;
}
