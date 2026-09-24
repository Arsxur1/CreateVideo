// Generic local webfont loader for Remotion.
//
// Why this exists: Remotion renders in headless Chromium, which only has a
// handful of system fonts. The pipeline hardcodes Latin fonts (Space Grotesk /
// Inter), so any non-Latin script (Devanagari, CJK, Arabic, etc.) silently
// renders blank — a serious, invisible failure.
//
// This helper injects an @font-face for a font file placed in `public/` so it
// is bundled and available to the headless renderer. Pair with a theme whose
// headingFont/bodyFont names the bundled family.

export interface LocalFont {
  /** Font-family name used in CSS (e.g. "Shobhika"). */
  family: string;
  /** Path relative to public/ (e.g. "/Shobhika.ttf"). */
  url: string;
  /** Format hint for the @font-face src. */
  format?: "truetype" | "opentype" | "woff2";
  /** Weight range, e.g. "400 700". */
  weight?: string;
}

export function localFontFaceCss(font: LocalFont): string {
  const format = font.format ?? "truetype";
  const weight = font.weight ?? "400 700";
  return `
    @font-face {
      font-family: '${font.family}';
      src: url('${font.url}') format('${format}');
      font-weight: ${weight};
      font-display: swap;
    }
  `;
}

/**
 * Inject one or more local @font-face rules into the document head.
 * Safe to call once per render (idempotent by family name).
 */
export function injectLocalFonts(fonts: LocalFont[]): void {
  if (typeof document === "undefined") return;
  for (const font of fonts) {
    const id = `local-font-${font.family}`;
    if (document.getElementById(id)) continue;
    const style = document.createElement("style");
    style.id = id;
    style.innerHTML = localFontFaceCss(font);
    document.head.appendChild(style);
  }
}
