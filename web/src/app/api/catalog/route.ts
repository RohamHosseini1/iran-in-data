import { NextResponse } from "next/server";

import { getCatalog } from "@/lib/data/catalog";

export const dynamic = "force-static";

/** Full machine-readable chart catalog (metadata + citations, no data rows). */
export function GET() {
  return NextResponse.json(getCatalog(), {
    headers: {
      "cache-control": "public, max-age=3600, stale-while-revalidate=86400",
    },
  });
}
