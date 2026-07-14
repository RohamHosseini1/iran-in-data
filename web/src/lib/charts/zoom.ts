/**
 * Wheel-zoom window maths, kept pure so it can be reasoned about and tested.
 *
 * ECharts' own inside-dataZoom applies a coarse step per wheel tick, so one trackpad
 * flick jumped from a decade to a single year, and a snap-to-year timer then yanked
 * the window again after the gesture settled. Both are gone; interactive-chart.tsx
 * eases the live window toward the target this returns.
 */

/** Wheel delta -> zoom. Small: one trackpad flick should be a nudge, not a jump. */
export const ZOOM_SENSITIVITY = 0.0022;

export interface ZoomInput {
  /** Window we are zooming from, in axis units (years, or epoch ms). */
  win: [number, number];
  /** Hard bounds: the extent of the DATA. The window may never exceed this. */
  bounds: [number, number];
  /** Raw wheel deltaY. Negative = zoom in. */
  delta: number;
  /** Axis value under the cursor; it stays put as the window scales around it. */
  anchor: number;
  /** Narrowest allowed window (3 years, or 7 days in time mode). */
  minSpan: number;
}

/**
 * The window a wheel gesture should ease toward.
 *
 * Guarantees, in order:
 *   - never wider than `bounds` (so zooming out stops exactly at the first and last
 *     observation and never reveals empty gutter),
 *   - never narrower than `minSpan`,
 *   - never straying outside `bounds`,
 *   - the anchor stays under the cursor whenever the clamps allow it.
 */
export function nextZoomWindow({
  win,
  bounds,
  delta,
  anchor,
  minSpan,
}: ZoomInput): [number, number] {
  const full = bounds[1] - bounds[0];
  const a = Math.min(Math.max(anchor, win[0]), win[1]);
  const factor = Math.exp(delta * ZOOM_SENSITIVITY);

  const rawStart = a - (a - win[0]) * factor;
  const rawEnd = a + (win[1] - a) * factor;
  const rawSpan = rawEnd - rawStart;

  const span = Math.min(Math.max(rawSpan, minSpan), full);

  // Re-derive around the anchor at the clamped span, preserving where in the window
  // the cursor sat, so clamping the span does not also slide the view sideways.
  const frac = rawSpan > 0 ? (a - rawStart) / rawSpan : 0.5;
  let start = a - frac * span;
  let end = start + span;

  if (start < bounds[0]) {
    start = bounds[0];
    end = start + span;
  }
  if (end > bounds[1]) {
    end = bounds[1];
    start = end - span;
  }
  return [start, end];
}
