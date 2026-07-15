import type { Locale } from "./config";

export const dictionaries = {
  en: {
    siteName: "Iran in Data",
    tagline: "The open, cited encyclopedia of Iran's economy",
    heroDescription:
      "Every chart traces Iran's economic and social record, currency and trade, industry and agriculture, demographics and public finance. Sourced, cited, and free.",
    browseCharts: "Browse charts",
    searchPlaceholder: "Search charts, indicators, events…",
    exploreCharts: "Explore the charts",
    home: "Home",
    charts: "Charts",
    footerAbout:
      "Iran in Data is an independent, non-profit project by Roham Hosseini. To minimize political bias, every figure is drawn and cross-verified from diverse international sources wherever possible. I hope this encyclopedia serves your research or your personal curiosity about Iran's economy.",
    attributions: "License & Attribution",
    downloads: "Download the data",
    personalSite: "Roham Hosseini",
  },
  fa: {
    siteName: "داده‌های اقتصادی ایران",
    tagline: "روایتی از تاریخ اقتصادی ایران با آمار و ارقام",
    heroDescription:
      "هر نمودار روایتی از کارنامه اقتصادی و اجتماعی ایران است، ارز و تجارت، صنعت و کشاورزی، جمعیت و مالیه عمومی. مستند، با ذکر منبع و رایگان.",
    browseCharts: "مرور نمودارها",
    searchPlaceholder: "جستجوی نمودار، شاخص، رویداد…",
    exploreCharts: "کاوش در نمودارها",
    home: "خانه",
    charts: "نمودارها",
    footerAbout:
      "داده‌های اقتصادی ایران دانشنامه ایست مستقل و غیرانتفاعی به تألیف رهام حسینی. با هدف به حداقل رساندن سوگیری‌های سیاسی، تمامی آمار و ارقام تا حد امکان از منابع متنوع بین‌المللی تهیه و تأیید گشته است. امیدوارم این دانشنامه یاری‌رسان شما در امور تحقیقاتی یا کنجکاوی‌های اقتصادی شخصی باشد. پاینده ایران.",
    attributions: "مجوز و انتساب",
    downloads: "دریافت داده‌ها",
    personalSite: "رهام حسینی",
  },
} satisfies Record<Locale, Record<string, string>>;

export function getDictionary(locale: Locale) {
  return dictionaries[locale];
}
