// Fonts a theme may name. Static imports so the bundler includes them;
// a font's files are only fetched when loadThemeFont() calls its loader.
// Keep this list in sync with TEMPLATE_FONTS in lib/themes.py.
import * as Anton from "@remotion/google-fonts/Anton";
import * as BricolageGrotesque from "@remotion/google-fonts/BricolageGrotesque";
import * as DMSerifDisplay from "@remotion/google-fonts/DMSerifDisplay";
import * as Fraunces from "@remotion/google-fonts/Fraunces";
import * as InstrumentSerif from "@remotion/google-fonts/InstrumentSerif";
import * as Manrope from "@remotion/google-fonts/Manrope";
import * as NotoSansDevanagari from "@remotion/google-fonts/NotoSansDevanagari";
import * as NotoSansTamil from "@remotion/google-fonts/NotoSansTamil";
import * as Outfit from "@remotion/google-fonts/Outfit";
import * as PlusJakartaSans from "@remotion/google-fonts/PlusJakartaSans";
import * as Sora from "@remotion/google-fonts/Sora";
import * as SpaceGrotesk from "@remotion/google-fonts/SpaceGrotesk";
import * as Syne from "@remotion/google-fonts/Syne";
import * as Unbounded from "@remotion/google-fonts/Unbounded";

type FontModule = {
  loadFont: (style?: any, options?: any) => { fontFamily: string };
};

const FONTS: Record<string, FontModule> = {
  Anton,
  BricolageGrotesque,
  DMSerifDisplay,
  Fraunces,
  InstrumentSerif,
  Manrope,
  Outfit,
  PlusJakartaSans,
  Sora,
  SpaceGrotesk,
  Syne,
  Unbounded,
};

const loaded = new Map<string, string>();

export const loadThemeFont = (name: string): string => {
  const cached = loaded.get(name);
  if (cached) return cached;
  const mod = FONTS[name] ?? FONTS.Manrope;
  // Latin only: captions are English. Bold weights where the font has them;
  // single-weight display fonts (Anton, serif faces) fall back to their default.
  let fontFamily: string;
  try {
    fontFamily = mod.loadFont("normal", { subsets: ["latin"], weights: ["600", "700", "800"] }).fontFamily;
  } catch {
    fontFamily = mod.loadFont("normal", { subsets: ["latin"] }).fontFamily;
  }
  loaded.set(name, fontFamily);
  return fontFamily;
};

// Script fallbacks: headless Chromium has no Tamil or Devanagari glyphs, so
// that text renders blank unless a font with those glyphs is registered.
// A theme opts in with fonts.scripts (e.g. ["tamil"]); each script's font is
// appended to every font-family chain, so Latin text keeps the theme font.
const SCRIPT_FONTS: Record<string, { mod: FontModule; subset: string }> = {
  tamil: { mod: NotoSansTamil, subset: "tamil" },
  devanagari: { mod: NotoSansDevanagari, subset: "devanagari" },
};

export const loadScriptFallbacks = (scripts: string[] = []): string[] =>
  scripts
    .filter((script) => SCRIPT_FONTS[script])
    .map((script) => {
      const cacheKey = `script:${script}`;
      const cached = loaded.get(cacheKey);
      if (cached) return cached;
      const { mod, subset } = SCRIPT_FONTS[script];
      const { fontFamily } = mod.loadFont("normal", { subsets: [subset], weights: ["400", "600", "700", "800"] });
      loaded.set(cacheKey, fontFamily);
      return fontFamily;
    });
