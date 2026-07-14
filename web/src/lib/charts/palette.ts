/**
 * Chart color system: Iran is the vivid hero (glow, full opacity); every
 * comparator gets its own real hue but rendered at reduced opacity so Iran
 * always reads first. Red stays reserved for negative deltas/events.
 *
 * On the client the chrome colors are read live from the shadcn CSS variables
 * so charts always match the active Olive light/dark theme; these constants
 * back the server-rendered SVG (crawlers/no-JS) and the first paint.
 */
export const IRAN_COLOR = "#2140E3";
export const NEGATIVE_COLOR = "#E32128";
export const POSITIVE_COLOR = "oklch(0.596 0.145 163.225)";

/** Distinct hues for comparators; series render them at ~60% opacity. */
export const COMPARATOR_COLORS = [
  "#D97706", // amber
  "#0D9488", // teal
  "#9333EA", // violet
  "#DB2777", // pink
  "#65A30D", // lime
  "#EA580C", // orange
  "#0891B2", // cyan
  "#CA8A04", // gold
  "#C026D3", // fuchsia
  "#059669", // emerald
  "#E11D48", // rose
  "#7C3AED", // purple
  "#4D7C0F", // olive-green
  "#B45309", // bronze
  "#0369A1", // steel blue
  "#A21CAF", // magenta
] as const;

export const COMPARATOR_OPACITY = 0.55;

export interface ChartChrome {
  foreground: string;
  mutedForeground: string;
  border: string;
  background: string;
  tooltipBackground: string;
}

export const LIGHT_CHROME: ChartChrome = {
  foreground: "#262520",
  mutedForeground: "#8a8574",
  border: "#eae8e3",
  background: "#ffffff",
  tooltipBackground: "#ffffff",
};

export const DARK_CHROME: ChartChrome = {
  foreground: "#fbfaf8",
  mutedForeground: "#b1ada2",
  border: "rgba(255,255,255,0.10)",
  background: "#26251f",
  tooltipBackground: "#312f28",
};

/** Read the live shadcn variables so charts track the active theme exactly. */
export function readChromeFromCss(): ChartChrome {
  if (typeof window === "undefined") return LIGHT_CHROME;
  const style = getComputedStyle(document.documentElement);
  const v = (name: string, fallback: string) =>
    style.getPropertyValue(name).trim() || fallback;
  return {
    foreground: v("--foreground", LIGHT_CHROME.foreground),
    mutedForeground: v("--muted-foreground", LIGHT_CHROME.mutedForeground),
    border: v("--border", LIGHT_CHROME.border),
    background: v("--background", LIGHT_CHROME.background),
    tooltipBackground: v("--popover", LIGHT_CHROME.tooltipBackground),
  };
}
