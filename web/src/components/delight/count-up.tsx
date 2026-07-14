"use client";

import * as React from "react";

import { formatCompact, formatReading } from "@/lib/charts/line-option";
import { formatReadingFa } from "@/lib/charts/unit-format";

const FORMATTERS = {
  compact: formatCompact,
  reading: formatReading,
  integer: (n: number) => Math.round(n).toLocaleString("en-US"),
} as const;

function resolveFormatter(
  format: keyof typeof FORMATTERS,
  locale?: "en" | "fa"
): (n: number) => string {
  if (locale === "fa" && format === "reading") return formatReadingFa;
  if (locale === "fa" && format === "integer")
    return (n: number) => Math.round(n).toLocaleString("fa-IR");
  return FORMATTERS[format];
}

/**
 * Number that counts up to its value on first view — short and restrained
 * (<1s), per the design notes: responsive polish without implying live data.
 * `format` is a preset name so server components can pass it across the
 * RSC boundary; `locale: "fa"` switches to Persian digits and scale words.
 */
export function CountUp({
  value,
  format = "integer",
  locale,
  duration = 800,
  className,
}: {
  value: number;
  format?: keyof typeof FORMATTERS;
  locale?: "en" | "fa";
  duration?: number;
  className?: string;
}) {
  const fmt = resolveFormatter(format, locale);
  const [display, setDisplay] = React.useState(() => fmt(0));
  const ref = React.useRef<HTMLSpanElement>(null);
  const started = React.useRef(false);
  const shownValue = React.useRef(0);

  React.useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      shownValue.current = value;
      setDisplay(fmt(value));
      return;
    }
    let raf = 0;
    let settle: ReturnType<typeof setTimeout> | null = null;
    const run = (from: number, dur: number) => {
      const start = performance.now();
      const lo = Math.min(from, value);
      const hi = Math.max(from, value);
      const tick = (now: number) => {
        const t = Math.min(1, (now - start) / dur);
        const eased = 1 - Math.pow(1 - t, 3);
        const current = Math.min(hi, Math.max(lo, from + (value - from) * eased));
        shownValue.current = current;
        setDisplay(fmt(current));
        if (t < 1) raf = requestAnimationFrame(tick);
      };
      raf = requestAnimationFrame(tick);
    };
    // rAF and IntersectionObserver both stall in hidden tabs; guarantee the
    // final value lands regardless of whether the animation ever ran.
    settle = setTimeout(() => {
      shownValue.current = value;
      setDisplay(fmt(value));
    }, duration + 400);
    // After the first reveal, later value changes (e.g. switching measure)
    // re-count quickly from the currently shown number.
    if (started.current) {
      run(shownValue.current, 350);
      return () => {
        cancelAnimationFrame(raf);
        if (settle) clearTimeout(settle);
      };
    }
    const observer = new IntersectionObserver((entries) => {
      if (!entries[0].isIntersecting || started.current) return;
      started.current = true;
      // If the settle fallback already landed the value, don't rewind to 0.
      run(shownValue.current !== value ? shownValue.current : value, duration);
    });
    observer.observe(el);
    return () => {
      observer.disconnect();
      cancelAnimationFrame(raf);
      if (settle) clearTimeout(settle);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [value, duration]);

  return (
    <span ref={ref} className={className}>
      {display}
    </span>
  );
}
