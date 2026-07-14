"use client";

import * as React from "react";

/**
 * localStorage-backed preference so choices like calendar system persist
 * across charts and visits. SSR-safe: first render uses the default, then
 * the stored value hydrates in.
 */
export function usePref<T>(
  key: string,
  defaultValue: T
): [T, (next: T) => void] {
  const storageKey = `iid:${key}`;
  const [value, setValue] = React.useState<T>(defaultValue);

  React.useEffect(() => {
    try {
      const raw = window.localStorage.getItem(storageKey);
      if (raw != null) setValue(JSON.parse(raw) as T);
    } catch {
      /* ignore */
    }
  }, [storageKey]);

  const update = React.useCallback(
    (next: T) => {
      setValue(next);
      try {
        window.localStorage.setItem(storageKey, JSON.stringify(next));
      } catch {
        /* ignore */
      }
    },
    [storageKey]
  );

  return [value, update];
}
