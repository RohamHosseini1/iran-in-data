"use client";

import * as React from "react";

const GLYPHS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

/**
 * Text that resolves from cipher noise into its final form, character by
 * character — the reference site's signature reveal, reframed as "the value
 * settling" rather than decryption. Re-runs whenever `text` changes.
 * Respects prefers-reduced-motion.
 */
export function ScrambleText({
  text,
  duration = 600,
  className,
  as: Tag = "span",
}: {
  text: string;
  duration?: number;
  className?: string;
  as?: React.ElementType;
}) {
  const [display, setDisplay] = React.useState(text);
  const frame = React.useRef<number | null>(null);

  React.useEffect(() => {
    if (
      typeof window !== "undefined" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches
    ) {
      setDisplay(text);
      return;
    }
    const start = performance.now();
    const tick = (now: number) => {
      const progress = Math.min(1, (now - start) / duration);
      const lockedCount = Math.floor(progress * text.length);
      let out = text.slice(0, lockedCount);
      for (let i = lockedCount; i < text.length; i++) {
        const ch = text[i];
        out += ch === " " ? " " : GLYPHS[(Math.random() * GLYPHS.length) | 0];
      }
      setDisplay(out);
      if (progress < 1) frame.current = requestAnimationFrame(tick);
    };
    frame.current = requestAnimationFrame(tick);
    return () => {
      if (frame.current) cancelAnimationFrame(frame.current);
    };
  }, [text, duration]);

  return <Tag className={className}>{display}</Tag>;
}
