import { AbsoluteFill, useCurrentFrame } from "remotion";
import { YAFHO, useCanvas, useFadeSlide } from "./yafho/tokens";

export interface ThesisTitleProps {
  text: string;
  /** "dark" = navy card + white text (over video), "light" = white card + navy text. */
  variant?: "dark" | "light";
  /** "panel" = bare left-aligned text for the 16:9 side panel. */
  placement?: "bottom" | "center" | "top" | "panel";
  fontSize?: number;
  /** Small source / footnote line under the title. */
  note?: string;
}

// "1 · Очистить" → step badge + text
const STEP_RE = /^(\d+)\s*·\s*(.+)$/;

/**
 * Large thesis title (≤ 6 words, ≥ 64px at 1080 wide) — the only copy channel
 * in no-voice brand videos. Fade + slide-up 0.4s, no bounce.
 */
export const ThesisTitle: React.FC<ThesisTitleProps> = ({
  text,
  variant = "dark",
  placement = "bottom",
  fontSize,
  note,
}) => {
  const frame = useCurrentFrame();
  const { width, height } = useCanvas();
  const { opacity, translateY } = useFadeSlide(frame);

  const step = text.match(STEP_RE);
  const body = step ? step[2] : text;

  if (placement === "panel") {
    const size = fontSize ?? 84;
    return (
      <AbsoluteFill style={{ justifyContent: "center" }}>
        <div style={{ opacity, transform: `translateY(${translateY}px)` }}>
          <div style={{ width: 96, height: 10, background: YAFHO.orange, borderRadius: 5, marginBottom: 40 }} />
          {step && (
            <div
              style={{
                fontFamily: YAFHO.mono,
                fontWeight: 700,
                fontSize: size * 0.6,
                color: YAFHO.navy,
                marginBottom: 16,
              }}
            >
              {`Шаг ${step[1]}`}
            </div>
          )}
          <div
            style={{
              fontFamily: YAFHO.sans,
              fontWeight: 800,
              fontSize: size,
              lineHeight: 1.1,
              color: YAFHO.navy,
              letterSpacing: "-0.01em",
              whiteSpace: "pre-line",
            }}
          >
            {body}
          </div>
          {note && (
            <div style={{ fontFamily: YAFHO.sans, fontWeight: 500, fontSize: 24, color: YAFHO.muted, marginTop: 24, lineHeight: 1.35 }}>{note}</div>
          )}
        </div>
      </AbsoluteFill>
    );
  }

  const size = fontSize ?? 76;
  const dark = variant === "dark";
  const tall = height / width > 1.6;
  const vertical: React.CSSProperties =
    placement === "center"
      ? { top: "50%", transform: `translateY(calc(-50% + ${translateY}px))` }
      : placement === "top"
        ? { top: height * 0.1, transform: `translateY(${translateY}px)` }
        : // keep clear of Reels/Shorts UI at the bottom of 9:16
          { bottom: height * (tall ? 0.17 : 0.07), transform: `translateY(${translateY}px)` };

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div
        style={{
          position: "absolute",
          left: width * 0.06,
          right: width * 0.06,
          display: "flex",
          justifyContent: "center",
          opacity,
          ...vertical,
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 28,
            background: dark ? YAFHO.navy : YAFHO.white,
            color: dark ? YAFHO.white : YAFHO.navy,
            borderRadius: 28,
            padding: "30px 44px",
            maxWidth: "100%",
          }}
        >
          {step && (
            <div
              style={{
                flex: "none",
                width: size * 1.15,
                height: size * 1.15,
                borderRadius: "50%",
                border: `6px solid ${YAFHO.orange}`,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontFamily: YAFHO.mono,
                fontWeight: 700,
                fontSize: size * 0.72,
              }}
            >
              {step[1]}
            </div>
          )}
          <div>
            <div
              style={{
                fontFamily: YAFHO.sans,
                fontWeight: 800,
                fontSize: size,
                lineHeight: 1.12,
                letterSpacing: "-0.01em",
                textAlign: step ? "left" : "center",
                whiteSpace: "pre-line",
              }}
            >
              {body}
            </div>
            {note && (
              <div
                style={{
                  fontFamily: YAFHO.sans,
                  fontWeight: 500,
                  fontSize: Math.round(size * 0.34),
                  lineHeight: 1.3,
                  marginTop: size * 0.25,
                  textAlign: "center",
                  color: dark ? "#C9D2DE" : YAFHO.muted,
                }}
              >
                {note}
              </div>
            )}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
