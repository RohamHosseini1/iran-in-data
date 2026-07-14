"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { Button } from "@/components/ui/button";
import { locales, type Locale } from "@/lib/i18n/config";

/** Swaps the leading /en or /fa segment, preserving the rest of the path. */
function pathForLocale(pathname: string, locale: Locale) {
  const segments = pathname.split("/");
  segments[1] = locale;
  return segments.join("/") || "/";
}

export function LanguageToggle({ locale }: { locale: Locale }) {
  const pathname = usePathname();

  return (
    <div className="flex items-center gap-1">
      {locales.map((l) => (
        <Button
          key={l}
          nativeButton={false}
          render={<Link href={pathForLocale(pathname, l)} hrefLang={l} />}
          variant={l === locale ? "secondary" : "ghost"}
          size="sm"
          style={
            l === "fa"
              ? { fontFamily: "var(--font-yekan), ui-sans-serif, sans-serif" }
              : undefined
          }
        >
          {l === "en" ? "English" : "فارسی"}
        </Button>
      ))}
    </div>
  );
}
