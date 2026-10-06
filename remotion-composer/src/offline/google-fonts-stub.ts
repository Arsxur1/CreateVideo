// Stand-in for @remotion/google-fonts/* when REMOTION_OFFLINE_GOOGLE_FONTS=1
// (see remotion.config.ts). Nothing is fetched; the CSS family name is still
// returned so text falls back to the next font in each stack.
declare const __resourceQuery: string;

const family = (typeof __resourceQuery === "string" ? __resourceQuery : "").replace(/^\?/, "") || "sans-serif";

export const loadFont = () => ({
  fontFamily: family,
  fonts: {},
  unicodeRanges: {},
  waitUntilDone: () => Promise.resolve(undefined),
});

export const getInfo = () => ({ fontFamily: family, importName: family, version: "offline", url: "", unicodeRanges: {}, fonts: {} });
