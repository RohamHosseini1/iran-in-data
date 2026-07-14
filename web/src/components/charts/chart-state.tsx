"use client";

import * as React from "react";

/**
 * Shared measure (variant) selection for one chart page, so the rail's
 * Latest_Reading follows the measure picked inside the visualizer.
 */
interface ChartState {
  variant: string;
  setVariant: (v: string) => void;
}

const ChartStateContext = React.createContext<ChartState | null>(null);

export function ChartStateProvider({
  initialVariant,
  children,
}: {
  initialVariant: string;
  children: React.ReactNode;
}) {
  const [variant, setVariant] = React.useState(initialVariant);
  const value = React.useMemo(() => ({ variant, setVariant }), [variant]);
  return (
    <ChartStateContext.Provider value={value}>
      {children}
    </ChartStateContext.Provider>
  );
}

/** Context-backed when a provider exists, local state otherwise. */
export function useChartVariant(
  fallback: string
): [string, (v: string) => void] {
  const ctx = React.useContext(ChartStateContext);
  const local = React.useState(fallback);
  return ctx ? [ctx.variant, ctx.setVariant] : local;
}
