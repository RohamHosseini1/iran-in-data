import type { MetadataRoute } from "next";

import { getCatalog } from "@/lib/data/catalog";
import { locales } from "@/lib/i18n/config";

const BASE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000";

export default function sitemap(): MetadataRoute.Sitemap {
  const entries: MetadataRoute.Sitemap = [];
  for (const locale of locales) {
    entries.push(
      { url: `${BASE_URL}/${locale}`, changeFrequency: "weekly", priority: 1 },
      {
        url: `${BASE_URL}/${locale}/charts`,
        changeFrequency: "weekly",
        priority: 0.9,
      }
    );
  }
  for (const e of getCatalog()) {
    for (const locale of locales) {
      entries.push({
        url: `${BASE_URL}/${locale}/charts/${encodeURIComponent(e.chart_id)}`,
        changeFrequency: "monthly",
        priority: 0.7,
      });
    }
  }
  return entries;
}
