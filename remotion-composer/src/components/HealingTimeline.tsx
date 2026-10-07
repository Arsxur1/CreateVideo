import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { YAFHO, ease, useCanvas, useFadeSlide } from "./yafho/tokens";

export interface HealingTimelineProps {
  /** Cursor position (0..1 along the bar) at the start and end of the overlay. */
  from?: number;
  to?: number;
  /** Light up the "Месяцы" segment as the window where the process can be steered. */
  highlightWindow?: boolean;
  /** Show 2 нед / 1 мес / 3 мес / 6 мес ticks (result scene). */
  ticks?: boolean;
  /** Rendered inside the 16:9 text panel instead of over the picture. */
  inPanel?: boolean;
  /** Move to the centre of the frame and grow — the "window" beat. */
  emphasis?: boolean;
}

// Stylised (not to scale): the long remodelling phase gets most of the bar.
export const HEALING_SEGMENTS = [
  { key: "days", label: "Дни", start: 0, end: 0.18 },
  { key: "weeks", label: "Недели", start: 0.18, end: 0.42 },
  { key: "months", label: "Месяцы", start: 0.42, end: 1 },
] as const;

const TICKS = [
  { at: 0.3, label: "2 нед" },
  { at: 0.47, label: "1 мес" },
  { at: 0.68, label: "3 мес" },
  { at: 0.95, label: "6 мес" },
];

/**
 * Persistent "healing timeline" — the story's spine: День 0 → Дни → Недели →
 * Месяцы. The cursor travels between scenes; the months segment lights up
 * orange as the window a silicone sheet can influence.
 */
export const HealingTimeline: React.FC<HealingTimelineProps> = ({
  from = 0,
  to = 0,
  highlightWindow = false,
  ticks = false,
  inPanel = false,
  emphasis = false,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const { width, height } = useCanvas();
  const { opacity, translateY } = useFadeSlide(frame);

  const move = ticks
    ? interpolate(frame, [0.3 * fps, durationInFrames - 0.5 * fps], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })
    : ease(frame, 0.2 * fps, 1.4 * fps);
  const cursor = from + (to - from) * move;
  const glow = highlightWindow ? ease(frame, 0.6 * fps, 1.4 * fps) : 0;

  const boxW = inPanel ? "100%" : width * 0.88;
  const fs = inPanel ? 30 : Math.round(width * 0.032);
  const barH = Math.max(8, fs * 0.28);

  const content = (
    <div
      style={{
        width: boxW,
        background: YAFHO.white,
        borderRadius: 24,
        padding: `${fs * 0.7}px ${fs * 0.9}px ${fs * (ticks ? 1.6 : 0.8)}px`,
        boxSizing: "border-box",
        opacity,
        transform: `translateY(${translateY}px)`,
      }}
    >
      {/* segment labels */}
      <div style={{ position: "relative", height: fs * 1.3 }}>
        {HEALING_SEGMENTS.map((s) => {
          const active = cursor >= s.start - 0.001 && (cursor < s.end || s.key === "months");
          const isWindow = s.key === "months" && glow > 0;
          return (
            <div
              key={s.key}
              style={{
                position: "absolute",
                left: `${s.start * 100}%`,
                width: `${(s.end - s.start) * 100}%`,
                textAlign: "center",
                fontFamily: YAFHO.sans,
                fontWeight: 800,
                fontSize: fs,
                color: active || isWindow ? YAFHO.navy : YAFHO.muted,
              }}
            >
              {s.label}
            </div>
          );
        })}
      </div>
      {/* bar */}
      <div style={{ position: "relative", height: barH * 3, marginTop: fs * 0.3 }}>
        {HEALING_SEGMENTS.map((s) => (
          <div
            key={s.key}
            style={{
              position: "absolute",
              left: `calc(${s.start * 100}% + 3px)`,
              width: `calc(${(s.end - s.start) * 100}% - 6px)`,
              top: barH,
              height: barH,
              borderRadius: barH,
              background: "#DDD4C8",
              overflow: "hidden",
            }}
          >
            <div
              style={{
                width: `${Math.max(0, Math.min(1, (cursor - s.start) / (s.end - s.start))) * 100}%`,
                height: "100%",
                background: s.key === "months" && glow > 0 ? YAFHO.orange : YAFHO.navy,
              }}
            />
          </div>
        ))}
        {/* window outline */}
        {glow > 0 && (
          <div
            style={{
              position: "absolute",
              left: `calc(${HEALING_SEGMENTS[2].start * 100}% - 4px)`,
              width: `calc(${(HEALING_SEGMENTS[2].end - HEALING_SEGMENTS[2].start) * 100}% + 8px)`,
              top: -fs * 1.6,
              height: barH * 3 + fs * 1.6,
              border: `4px solid ${YAFHO.orange}`,
              borderRadius: 16,
              opacity: glow,
              transform: `scale(${0.96 + 0.04 * glow})`,
            }}
          />
        )}
        {/* ticks */}
        {ticks &&
          TICKS.map((t) => {
            const passed = cursor >= t.at;
            return (
              <div key={t.label} style={{ position: "absolute", left: `${t.at * 100}%`, top: barH * 2.4, transform: "translateX(-50%)", textAlign: "center" }}>
                <div style={{ width: 3, height: barH, background: passed ? YAFHO.navy : "#B9B1A6", margin: "0 auto" }} />
                <div style={{ fontFamily: YAFHO.mono, fontWeight: 700, fontSize: fs * 0.72, color: passed ? YAFHO.navy : YAFHO.muted, whiteSpace: "nowrap" }}>
                  {t.label}
                </div>
              </div>
            );
          })}
        {/* cursor */}
        <div
          style={{
            position: "absolute",
            left: `${cursor * 100}%`,
            top: barH * 1.5,
            width: barH * 2.6,
            height: barH * 2.6,
            borderRadius: "50%",
            background: YAFHO.navy,
            border: `${Math.max(3, barH * 0.45)}px solid ${YAFHO.white}`,
            boxShadow: "0 0 0 2px rgba(15,36,64,0.25)",
            transform: "translate(-50%, -50%)",
          }}
        />
        {/* day 0 */}
        <div style={{ position: "absolute", left: 0, top: barH * 2.4, fontFamily: YAFHO.mono, fontWeight: 700, fontSize: fs * 0.62, color: YAFHO.muted, display: ticks ? "none" : "block" }}>
          День 0
        </div>
      </div>
    </div>
  );

  const emph = emphasis ? ease(frame, 0.2 * fps, 1.2 * fps) : 0;

  if (inPanel) {
    return <AbsoluteFill style={{ justifyContent: "flex-start", paddingTop: height * 0.12 }}>{content}</AbsoluteFill>;
  }
  return (
    <AbsoluteFill
      style={{
        alignItems: "center",
        paddingTop: height * (0.055 + 0.27 * emph),
        pointerEvents: "none",
      }}
    >
      <div style={{ transform: `scale(${1 + 0.1 * emph})`, transformOrigin: "50% 0" }}>{content}</div>
    </AbsoluteFill>
  );
};
