// Fonts a theme may name. Static imports so the bundler includes them;
// a font's files are only fetched when loadThemeFont() calls its loader.
// Keep this list in sync with TEMPLATE_FONTS in lib/themes.py.
import * as Anton from "@remotion/google-fonts/Anton";
import * as BricolageGrotesque from "@remotion/google-fonts/BricolageGrotesque";
import * as DMSerifDisplay from "@remotion/google-fonts/DMSerifDisplay";
import * as Fraunces from "@remotion/google-fonts/Fraunces";
import * as InstrumentSerif from "@remotion/google-fonts/InstrumentSerif";
import * as Manrope from "@remotion/google-fonts/Manrope";
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
