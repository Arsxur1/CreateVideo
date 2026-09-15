import { continueRender, delayRender } from "remotion";

import playfairItalicUrl from "../fonts/PlayfairDisplay-Italic-latin.woff2";
import playfairUrl from "../fonts/PlayfairDisplay-latin.woff2";
import spaceGroteskUrl from "../fonts/SpaceGrotesk-latin.woff2";

/**
 * Fonts bundled with the compositions instead of fetched from Google Fonts at
 * render time, so a render needs no network and a flaky connection cannot fail
 * it. The files are the exact latin woff2 files @remotion/google-fonts
 * requested (Space Grotesk v22, Playfair Display v40; SIL OFL 1.1, licences in
 * ../fonts), registered the same way: one FontFace per requested weight, same
 * family name, same unicode range — so glyphs render identically.
 */

const LATIN =
  "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD";

const loaded = new Set<string>();

const register = (family: string, url: string, style: "normal" | "italic", weights: string[]) => {
  if (typeof FontFace === "undefined") return family;
  for (const weight of weights) {
    const key = `${family}-${style}-${weight}`;
    if (loaded.has(key)) continue;
    loaded.add(key);
    const handle = delayRender(`Loading bundled font ${key}`);
    const face = new FontFace(family, `url(${url}) format('woff2')`, { weight, style, unicodeRange: LATIN });
    face
      .load()
      .then(() => {
        document.fonts.add(face);
        continueRender(handle);
      })
      .catch((err) => {
        // Never silently fall back to a system font: fail the render.
        throw new Error(`Bundled font ${key} failed to load: ${err}`);
      });
  }
  return family;
};

export const loadSpaceGrotesk = (weights: string[]) => ({ fontFamily: register("Space Grotesk", spaceGroteskUrl, "normal", weights) });
export const loadPlayfair = (style: "normal" | "italic", weights: string[]) => ({
  fontFamily: register("Playfair Display", style === "italic" ? playfairItalicUrl : playfairUrl, style, weights),
});
