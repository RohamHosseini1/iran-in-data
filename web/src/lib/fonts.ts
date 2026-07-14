import { Reddit_Mono } from "next/font/google";
import localFont from "next/font/local";

/**
 * Type system mirrors the Overwatch reference exactly:
 * - Latin UI/prose: Switzer (the reference's own typeface, owner-provided).
 * - Persian: Yekan Bakh (owner-licensed); Persian has no mono companion, so
 *   in fa mode Yekan Bakh covers everything including data labels.
 * - Numerals/IDs/badges (Latin only): Reddit Mono, the reference's mono.
 */
export const yekanBakh = localFont({
  src: [
    { path: "../assets/fonts/yekan-bakh/YekanBakh-Light.woff2", weight: "300" },
    { path: "../assets/fonts/yekan-bakh/YekanBakh-Regular.woff2", weight: "400" },
    { path: "../assets/fonts/yekan-bakh/YekanBakh-SemiBold.woff2", weight: "600" },
    { path: "../assets/fonts/yekan-bakh/YekanBakh-Bold.woff2", weight: "700" },
    { path: "../assets/fonts/yekan-bakh/YekanBakh-Black.woff2", weight: "900" },
  ],
  variable: "--font-yekan",
  display: "swap",
});

export const switzer = localFont({
  src: [
    { path: "../assets/fonts/switzer/Switzer-Light.otf", weight: "300" },
    { path: "../assets/fonts/switzer/Switzer-Regular.otf", weight: "400" },
    { path: "../assets/fonts/switzer/Switzer-Medium.otf", weight: "500" },
    { path: "../assets/fonts/switzer/Switzer-Semibold.otf", weight: "600" },
    { path: "../assets/fonts/switzer/Switzer-Bold.otf", weight: "700" },
    { path: "../assets/fonts/switzer/Switzer-Black.otf", weight: "900" },
  ],
  variable: "--font-switzer",
  display: "swap",
});

export const redditMono = Reddit_Mono({
  subsets: ["latin"],
  variable: "--font-reddit-mono",
  display: "swap",
});
