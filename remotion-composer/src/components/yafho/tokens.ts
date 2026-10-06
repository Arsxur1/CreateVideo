import { createContext, useContext, useEffect, useState } from "react";
import { Easing, continueRender, delayRender, interpolate, staticFile, useVideoConfig } from "remotion";

// Yafho SiliSkin brand tokens — mirrors styles/yafho-clinical.yaml.
// Fonts ship in public/fonts/yafho (OFL) so renders never depend on fonts.gstatic.com.
const CYRILLIC = "U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116";
const LATIN =
  "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD";
const SYMBOLS = "U+2190-2193, U+00D7, U+00B7, U+2013-2014";

const FACES: { family: string; file: string; weight: string; range: string }[] = [
  { family: "Yafho Onest", file: "onest-latin.woff2", weight: "100 900", range: LATIN },
  { family: "Yafho Onest", file: "onest-cyrillic.woff2", weight: "100 900", range: CYRILLIC },
  { family: "Yafho Onest", file: "onest-symbols-500.woff2", weight: "100 650", range: SYMBOLS },
  { family: "Yafho Onest", file: "onest-symbols-800.woff2", weight: "651 900", range: SYMBOLS },
  { family: "Yafho Mono", file: "jetbrainsmono-latin.woff2", weight: "100 900", range: LATIN },
  { family: "Yafho Mono", file: "jetbrainsmono-cyrillic.woff2", weight: "100 900", range: CYRILLIC },
];

// Inject @font-face rules once; the browser fetches the files natively.
if (typeof document !== "undefined" && !document.getElementById("yafho-fonts")) {
  const style = document.createElement("style");
  style.id = "yafho-fonts";
  style.textContent = FACES.map(
    (f) =>
      `@font-face{font-family:"${f.family}";src:url("${staticFile(`fonts/yafho/${f.file}`)}") format("woff2");` +
      `font-weight:${f.weight};unicode-range:${f.range};font-display:block;}`,
  ).join("\n");
  document.head.appendChild(style);
}

/** Hold the frame until the Yafho fonts are usable (falls back after 10s). */
export function useYafhoFonts(): void {
  const [handle] = useState(() => delayRender("Loading Yafho fonts"));
  useEffect(() => {
    let done = false;
    const finish = () => {
      if (!done) {
        done = true;
        continueRender(handle);
      }
    };
    const timer = setTimeout(finish, 10000);
    Promise.all([
      document.fonts.load('500 40px "Yafho Onest"', "Аа→"),
      document.fonts.load('800 40px "Yafho Onest"', "Аа→"),
      document.fonts.load('700 40px "Yafho Mono"', "А1"),
    ])
      .catch(() => undefined)
      .finally(() => {
        clearTimeout(timer);
        finish();
      });
  }, [handle]);
}

export const YAFHO = {
  navy: "#0F2440",
  orange: "#D4560F",
  teal: "#0D9488",
  offWhite: "#FBFAF7",
  beige: "#ECE6DD",
  muted: "#5B6472",
  white: "#FFFFFF",
  sans: `"Yafho Onest", system-ui, sans-serif`,
  mono: `"Yafho Mono", ui-monospace, monospace`,
} as const;

// Design canvas the Yafho components lay themselves out in. Normally the
// video frame; in the 16:9 "split" layout it is the 1080x1920 vertical panel.
export const CanvasContext = createContext<{ width: number; height: number } | null>(null);

export function useCanvas(): { width: number; height: number } {
  useYafhoFonts();
  const ctx = useContext(CanvasContext);
  const { width, height } = useVideoConfig();
  return ctx ?? { width, height };
}

/** 0→1 over [start, end] frames with ease-in-out, clamped. */
export function ease(frame: number, start: number, end: number): number {
  return interpolate(frame, [start, end], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.ease),
  });
}

/** Brand entrance/exit: fade + slide-up 0.4s, fade-out 0.4s, no bounce. */
export function useFadeSlide(frame: number, delayFrames = 0, exit = true) {
  const { fps, durationInFrames } = useVideoConfig();
  const t = Math.round(0.4 * fps);
  const inP = ease(frame, delayFrames, delayFrames + t);
  const outP = exit ? 1 - ease(frame, durationInFrames - t, durationInFrames) : 1;
  return { opacity: inP * outP, translateY: (1 - inP) * 24 };
}

/** Map a point from 1080x1920 source-video space into the canvas (objectFit: cover). */
export function coverMap(
  canvas: { width: number; height: number },
  source = { width: 1080, height: 1920 },
) {
  const s = Math.max(canvas.width / source.width, canvas.height / source.height);
  const ox = (canvas.width - source.width * s) / 2;
  const oy = (canvas.height - source.height * s) / 2;
  return {
    scale: s,
    x: (v: number) => ox + v * s,
    y: (v: number) => oy + v * s,
  };
}
