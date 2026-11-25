import type { MetadataRoute } from "next";

export const dynamic = "force-static";
export const revalidate = false;

const BASE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "https://iranindata.org";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: { userAgent: "*", allow: "/" },
    sitemap: `${BASE_URL}/sitemap.xml`,
  };
}
