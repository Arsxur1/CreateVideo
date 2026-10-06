import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { YAFHO, ease, useCanvas, useFadeSlide } from "./yafho/tokens";

export interface TimeCounterProps {
  labels?: string[];
  placement?: "top" | "bottom";
}

/**
 * Timeline chips over the result shot (H08): "2 нед → 1 мес → 3 мес → 6 мес".
 * Each chip turns navy in turn across the cut's duration.
 */
export const TimeCounter: React.FC<TimeCounterProps> = ({
  labels = ["2 нед", "1 мес", "3 мес", "6 мес"],
  placement = "top",
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const { width, height } = useCanvas();
  const { opacity, translateY } = useFadeSlide(frame);

  const n = labels.length;
  const start = Math.round(0.3 * fps);
  const span = durationInFrames * 0.8 - start;
  const step = span / n;
  const t = 0.3 * fps;
  const fontSize = 40;

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          ...(placement === "top" ? { top: height * 0.08 } : { bottom: height * 0.32 }),
          display: "flex",
          justifyContent: "center",
          opacity,
          transform: `translateY(${translateY}px)`,
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 12,
            background: YAFHO.white,
            borderRadius: 999,
            padding: 12,
            maxWidth: width * 0.94,
          }}
        >
          {labels.map((l, i) => {
            const on = ease(frame, start + i * step, start + i * step + t);
            const past = i < n - 1 ? ease(frame, start + (i + 1) * step, start + (i + 1) * step + t) : 0;
            const active = on > 0.5 && past < 0.5;
            const done = past >= 0.5;
            return (
              <div key={i} style={{ display: "flex", alignItems: "center", gap: 12 }}>
                {i > 0 && (
                  <div style={{ fontFamily: YAFHO.sans, fontWeight: 800, fontSize: fontSize * 0.8, color: done || active ? YAFHO.orange : "#B7BCC4" }}>
                    →
                  </div>
                )}
                <div
                  style={{
                    fontFamily: YAFHO.mono,
                    fontWeight: 700,
                    fontSize,
                    padding: "14px 22px",
                    borderRadius: 999,
                    background: active ? YAFHO.navy : "transparent",
                    color: active ? YAFHO.white : done ? YAFHO.navy : YAFHO.muted,
                    whiteSpace: "nowrap",
                  }}
                >
                  {l}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
