import type { Metadata } from "next";
import { notFound } from "next/navigation";

import "../globals.css";
import { redditMono, switzer, yekanBakh } from "@/lib/fonts";
import { ThemeProvider } from "@/components/theme-provider";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { isLocale, locales, localeDirection, type Locale } from "@/lib/i18n/config";

export function generateStaticParams() {
  return locales.map((locale) => ({ locale }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  const fa = locale === "fa";
  const siteName = fa ? "ایران در داده‌ها" : "Iran in Data";
  return {
    title: { default: siteName, template: `%s · ${siteName}` },
    description: fa
      ? "روایتی از تاریخ اقتصادی ایران با آمار و ارقام"
      : "An open, cited encyclopedia of Iran's economic and social history in charts.",
  };
}

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  return (
    <html
      lang={locale}
      dir={localeDirection[locale]}
      className={`${yekanBakh.variable} ${switzer.variable} ${redditMono.variable} h-full antialiased`}
      suppressHydrationWarning
    >
      <body className="min-h-full flex flex-col bg-background text-foreground">
        <ThemeProvider
          attribute="class"
          defaultTheme="light"
          enableSystem={false}
          disableTransitionOnChange
        >
          <SiteHeader locale={locale as Locale} />
          <main className="flex-1">{children}</main>
          <SiteFooter locale={locale as Locale} />
        </ThemeProvider>
      </body>
    </html>
  );
}
