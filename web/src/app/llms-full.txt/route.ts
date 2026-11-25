import { llmsFullTxt } from "@/lib/llms-text";

export const dynamic = "force-static";
export const revalidate = false;

export function GET() {
  return new Response(llmsFullTxt(), {
    headers: {
      "content-type": "text/plain; charset=utf-8",
      "cache-control": "public, max-age=3600, s-maxage=31536000",
    },
  });
}
