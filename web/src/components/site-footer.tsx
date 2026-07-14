import Link from "next/link";

import { getDictionary } from "@/lib/i18n/dictionaries";
import type { Locale } from "@/lib/i18n/config";

/* TODO(owner): confirm the personal-website URL. */
const PERSONAL_SITE_URL = "https://rohamhosseini.com";

export function SiteFooter({ locale }: { locale: Locale }) {
  const dict = getDictionary(locale);

  return (
    <footer className="border-t border-border/60">
      <div className="mx-auto flex max-w-6xl flex-col gap-4 px-4 py-10 sm:px-6">
        <span className="text-sm font-medium">{dict.siteName}</span>
        <p className="max-w-2xl text-xs leading-relaxed text-muted-foreground">
          {dict.footerAbout}
        </p>
        <nav className="data-label flex flex-wrap items-center gap-x-6 gap-y-2">
          <Link
            href={`/${locale}/downloads`}
            className="transition-colors hover:text-foreground"
          >
            {dict.downloads}
          </Link>
          <Link
            href={`/${locale}/attributions`}
            className="transition-colors hover:text-foreground"
          >
            {dict.attributions}
          </Link>
          <a
            href={PERSONAL_SITE_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="transition-colors hover:text-foreground"
          >
            {dict.personalSite}
          </a>
        </nav>
      </div>
    </footer>
  );
}
