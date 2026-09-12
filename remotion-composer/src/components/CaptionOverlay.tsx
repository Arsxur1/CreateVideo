import {
  AbsoluteFill,
  Sequence,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

// Word-level caption for TikTok-style highlight display
export interface WordCaption {
  word: string;
  startMs: number;
  endMs: number;
  // Force a page break after this word (e.g. sentence or scene boundaries).
  // Useful for CJK captions where pages should align with clause boundaries.
  pageBreakAfter?: boolean;
}

type CaptionOverlayProps = {
  words: WordCaption[];
  // How many words to show at once in a "page"
  wordsPerPage?: number;
  fontSize?: number;
  color?: string;
  highlightColor?: string;
  backgroundColor?: string;
  fontFamily?: string;
  // Separator rendered between words. Space-delimited languages want the
  // default " "; CJK languages (no inter-word spacing) should pass "".
  wordSeparator?: string;
};

interface CaptionPage {
  words: WordCaption[];
  startMs: number;
  endMs: number;
}

function buildPages(words: WordCaption[], wordsPerPage: number): CaptionPage[] {
  const pages: CaptionPage[] = [];
  let pageWords: WordCaption[] = [];
  const flush = () => {
    if (pageWords.length === 0) return;
    pages.push({
      words: pageWords,
      startMs: pageWords[0].startMs,
      endMs: pageWords[pageWords.length - 1].endMs,
    });
    pageWords = [];
  };
  for (const w of words) {
    pageWords.push(w);
    if (pageWords.length >= wordsPerPage || w.pageBreakAfter) flush();
  }
  flush();
  return pages;
}

const PageRenderer: React.FC<{
  page: CaptionPage;
  fontSize: number;
  color: string;
  highlightColor: string;
  backgroundColor: string;
  fontFamily: string;
  wordSeparator: string;
}> = ({ page, fontSize, color, highlightColor, backgroundColor, fontFamily, wordSeparator }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const currentMs = page.startMs + (frame / fps) * 1000;

  // Spring entrance
  const entrance = spring({
    frame,
    fps,
    config: { damping: 18, stiffness: 120 },
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: 64,
      }}
    >
      <div
        style={{
          backgroundColor,
          borderRadius: 14,
          padding: "16px 30px",
          maxWidth: "82%",
          textAlign: "center",
        }}
      >
        <span
          style={{
            fontSize,
            fontWeight: 700,
            fontFamily,
            lineHeight: 1.45,
            whiteSpace: "pre-wrap",
          }}
        >
          {page.words.map((w, i) => {
            // Cumulative reveal: a word only appears once its time has come.
            const appeared = w.startMs <= currentMs;
            if (!appeared) return null;
            const isActive = w.startMs <= currentMs && w.endMs > currentMs;
            // Per-word spring entrance keyed to its start time.
            const wordFrame = Math.max(
              0,
              Math.round(((currentMs - w.startMs) / 1000) * fps)
            );
            const entrance = spring({
              frame: wordFrame,
              fps,
              config: { damping: 16, stiffness: 160, mass: 0.7 },
              from: 0,
              to: 1,
            });
            return (
              <span
                key={`${w.startMs}-${i}`}
                style={{
                  display: "inline-block",
                  whiteSpace: "nowrap",
                  opacity: entrance,
                  transform: `translateY(${interpolate(entrance, [0, 1], [18, 0])}px) scale(${interpolate(entrance, [0, 1], [0.9, 1])})`,
                  color: isActive ? highlightColor : color,
                  textShadow: isActive
                    ? `0 0 22px ${highlightColor}66, 0 2px 4px rgba(0,0,0,0.5)`
                    : "0 2px 4px rgba(0,0,0,0.5)",
                }}
              >
                {w.word}{i < page.words.length - 1 ? wordSeparator : ""}
              </span>
            );
          })}
        </span>
      </div>
    </AbsoluteFill>
  );
};

export const CaptionOverlay: React.FC<CaptionOverlayProps> = ({
  words,
  wordsPerPage = 6,
  fontSize = 42,
  color = "#F8FAFC",
  highlightColor = "#22D3EE",
  backgroundColor = "rgba(15, 23, 42, 0.75)",
  fontFamily = "Baloo2, system-ui, sans-serif",
  wordSeparator = " ",
}) => {
  const { fps } = useVideoConfig();
  const pages = buildPages(words, wordsPerPage);

  return (
    <AbsoluteFill>
      {pages.map((page, i) => {
        const fromFrame = Math.round((page.startMs / 1000) * fps);
        const nextStart = pages[i + 1]?.startMs ?? page.endMs + 500;
        const duration = Math.max(
          1,
          Math.round(((nextStart - page.startMs) / 1000) * fps)
        );

        return (
          <Sequence key={i} from={fromFrame} durationInFrames={duration}>
            <PageRenderer
              page={page}
              fontSize={fontSize}
              color={color}
              highlightColor={highlightColor}
              backgroundColor={backgroundColor}
              fontFamily={fontFamily}
              wordSeparator={wordSeparator}
            />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
