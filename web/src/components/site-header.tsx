import Link from "next/link";

import { ThemeToggle } from "@/components/theme-toggle";
import { LanguageToggle } from "@/components/language-toggle";
import { getDictionary } from "@/lib/i18n/dictionaries";
import type { Locale } from "@/lib/i18n/config";

export function SiteHeader({ locale }: { locale: Locale }) {
  const dict = getDictionary(locale);

  return (
    <header className="sticky top-0 z-40 border-b border-border/60 bg-background/85 backdrop-blur">
      <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4 sm:px-6">
        <Link
          href={`/${locale}`}
          className="text-sm font-medium tracking-tight"
        >
          {dict.siteName}
        </Link>
        <nav className="hidden items-center gap-6 text-sm text-muted-foreground sm:flex">
          <Link href={`/${locale}/charts`} className="hover:text-foreground">
            {dict.charts}
          </Link>
        </nav>
        <div className="flex items-center gap-2">
          <LanguageToggle locale={locale} />
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}
