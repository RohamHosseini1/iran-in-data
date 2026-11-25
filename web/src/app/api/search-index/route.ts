import { NextResponse } from "next/server";

import { getSearchIndex } from "@/lib/data/catalog";

export const dynamic = "force-static";
export const revalidate = false;

export function GET() {
  return NextResponse.json(getSearchIndex(), {
    headers: {
      "cache-control": "public, max-age=3600, s-maxage=31536000",
    },
  });
}
