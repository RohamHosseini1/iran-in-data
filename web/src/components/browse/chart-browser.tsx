"use client";

import * as React from "react";
import Link from "next/link";

import { toPersianDigits } from "@/lib/calendar";
import { normalizeSearchText } from "@/lib/i18n/normalize";
import type { SearchRecord } from "@/lib/data/types";
import type { Locale } from "@/lib/i18n/config";

const STRINGS = {
  en: {
    placeholder: "search --charts",
    category: "Category",
    source: "Source",
    from: "From year",
    to: "To year",
    all: "All",
    results: "records",
    of: "of",
    displaying: "Displaying",
    noResults: "No matching records.",
    clear: "Clear filters",
  },
  fa: {
    placeholder: "جستجوی نمودارها",
    category: "دسته",
    source: "منبع",
    from: "از سال",
    to: "تا سال",
    all: "همه",
    results: "رکورد",
    of: "از",
    displaying: "نمایش",
    noResults: "رکوردی یافت نشد.",
    clear: "حذف فیلترها",
  },
};

const PAGE_SIZE = 120;

interface ChartBrowserProps {
  locale: Locale;
  categories: { name: string; nameFa: string; count: number }[];
  initialCategory?: string;
}

export function ChartBrowser({
  locale,
  categories,
  initialCategory,
}: ChartBrowserProps) {
  const t = STRINGS[locale];
  const fa = locale === "fa";
  const [index, setIndex] = React.useState<
    (SearchRecord & { _hay: string })[] | null
  >(null);
  const [query, setQuery] = React.useState("");
  const [category, setCategory] = React.useState(initialCategory ?? "");
  const [source, setSource] = React.useState("");
  const [yearFrom, setYearFrom] = React.useState("");
  const [yearTo, setYearTo] = React.useState("");
  const [limit, setLimit] = React.useState(PAGE_SIZE);

  React.useEffect(() => {
    let cancelled = false;
    fetch("/api/search-index")
      .then((r) => r.json())
      .then((data: SearchRecord[]) => {
        if (cancelled) return;
        setIndex(
          data.map((r) => ({
            ...r,
            _hay: normalizeSearchText(`${r.t} ${r.tf} ${r.c} ${r.cf} ${r.id} ${r.s}`),
          }))
        );
      })
      .catch(() => {});
    return () => {
      cancelled = true;
    };
  }, []);

  const sources = React.useMemo(() => {
    if (!index) return [];
    const counts = new Map<string, number>();
    for (const r of index) counts.set(r.s, (counts.get(r.s) ?? 0) + 1);
    return [...counts.entries()].sort((a, b) => b[1] - a[1]);
  }, [index]);

  const resetPage = () => setLimit(PAGE_SIZE);

  const results = React.useMemo(() => {
    if (!index) return [];
    const tokens = normalizeSearchText(query.trim())
      .split(/\s+/)
      .filter(Boolean);
    const from = Number(yearFrom) || -Infinity;
    const to = Number(yearTo) || Infinity;
    return index.filter((r) => {
      if (category && r.c !== category) return false;
      if (source && r.s !== source) return false;
      if (Number.isFinite(from) || Number.isFinite(to)) {
        const y0 = Number(r.y0);
        const y1 = Number(r.y1);
        // Keep charts whose coverage overlaps the requested window.
        if (Number.isFinite(y1) && y1 < from) return false;
        if (Number.isFinite(y0) && y0 > to) return false;
      }
      if (!tokens.length) return true;
      return tokens.every((tok) => r._hay.includes(tok));
    });
  }, [index, query, category, source, yearFrom, yearTo]);

  const shown = results.slice(0, limit);
  const hasFilters = category || source || yearFrom || yearTo || query;

  return (
    <div>
      {/* Search first — the primary control gets the full row */}
      <div className="flex items-center gap-2 border border-border/70 bg-card/40 px-3 py-2.5 transition-colors focus-within:border-foreground/40">
        <span className="font-data text-muted-foreground" aria-hidden>
          &gt;
        </span>
        <input
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            resetPage();
          }}
          placeholder={t.placeholder}
          className="font-data w-full bg-transparent text-sm outline-none placeholder:text-muted-foreground/60"
        />
      </div>

      {/* Filters: label-over-control groups, clearly secondary */}
      <div className="mt-3 flex flex-wrap items-end gap-x-8 gap-y-3">
        <FilterGroup label={t.category}>
          <select
            value={category}
            onChange={(e) => {
              setCategory(e.target.value);
              resetPage();
            }}
            className="data-label max-w-52 border border-border/70 bg-card/40 px-2.5 py-2 outline-none"
          >
            <option value="">{t.all}</option>
            {categories.map((c) => (
              <option key={c.name} value={c.name}>
                {(fa ? c.nameFa : c.name) + ` (${c.count})`}
              </option>
            ))}
          </select>
        </FilterGroup>
        <FilterGroup label={t.source}>
          <select
            value={source}
            onChange={(e) => {
              setSource(e.target.value);
              resetPage();
            }}
            className="data-label max-w-44 border border-border/70 bg-card/40 px-2.5 py-2 outline-none"
          >
            <option value="">{t.all}</option>
            {sources.map(([s, n]) => (
              <option key={s} value={s}>
                {s} ({n})
              </option>
            ))}
          </select>
        </FilterGroup>
        <FilterGroup label={`${t.from} – ${t.to}`}>
          <div className="flex items-center gap-1.5" dir="ltr">
            <input
              value={yearFrom}
              onChange={(e) => {
                setYearFrom(e.target.value.replace(/[^0-9]/g, ""));
                resetPage();
              }}
              placeholder="1900"
              inputMode="numeric"
              className="font-data w-16 border border-border/70 bg-card/40 px-2 py-1.5 text-xs outline-none placeholder:text-muted-foreground/40"
            />
            <span className="text-muted-foreground">–</span>
            <input
              value={yearTo}
              onChange={(e) => {
                setYearTo(e.target.value.replace(/[^0-9]/g, ""));
                resetPage();
              }}
              placeholder="2026"
              inputMode="numeric"
              className="font-data w-16 border border-border/70 bg-card/40 px-2 py-1.5 text-xs outline-none placeholder:text-muted-foreground/40"
            />
          </div>
        </FilterGroup>
        {hasFilters ? (
          <button
            onClick={() => {
              setQuery("");
              setCategory("");
              setSource("");
              setYearFrom("");
              setYearTo("");
              resetPage();
            }}
            className="data-label border border-transparent px-2 py-2 text-muted-foreground transition-colors hover:text-foreground"
          >
            × {t.clear}
          </button>
        ) : null}
      </div>

      {/* Count line */}
      <p className="data-label mt-4">
        {index
          ? `${t.displaying} ${shown.length.toLocaleString("en-US")} ${t.of} ${results.length.toLocaleString("en-US")} ${t.results}`
          : "…"}
      </p>

      {/* Results */}
      <ul className="mt-2 divide-y divide-border/50 border border-border/60 bg-card/30">
        {shown.map((r) => (
          <li key={r.id}>
            <Link
              href={`/${locale}/charts/${encodeURIComponent(r.id)}`}
              className="group flex items-baseline gap-4 px-4 py-2.5 transition-colors hover:bg-muted/50"
            >
              <span className="min-w-0 flex-1 truncate text-sm group-hover:text-foreground">
                {fa ? r.tf : r.t}
              </span>
              <span className="data-label hidden shrink-0 sm:inline">
                {fa ? r.cf : r.c}
              </span>
              <span
                className="font-data shrink-0 text-[10px] text-muted-foreground"
                dir="ltr"
              >
                {fa
                  ? `${toPersianDigits(r.y0)}–${toPersianDigits(r.y1)}`
                  : `${r.y0}–${r.y1}`}
              </span>
            </Link>
          </li>
        ))}
        {index && results.length === 0 ? (
          <li className="data-label px-4 py-6 text-center">{t.noResults}</li>
        ) : null}
      </ul>

      {results.length > limit ? (
        <button
          onClick={() => setLimit((l) => l + PAGE_SIZE)}
          className="data-label mt-3 w-full border border-border/60 bg-card/40 py-2.5 transition-colors hover:bg-muted/50"
        >
          + {(results.length - limit).toLocaleString("en-US")}
        </button>
      ) : null}
    </div>
  );
}

function FilterGroup({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <div className="flex flex-col gap-1.5">
      <span className="data-label">{label}</span>
      {children}
    </div>
  );
}
