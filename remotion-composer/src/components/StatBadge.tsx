import { AbsoluteFill } from "remotion";
import { useCurrentFrame } from "remotion";
import { YAFHO, useCanvas, useFadeSlide } from "./yafho/tokens";

export interface StatBadgeProps {
  value: string;
  label: string;
  /** Required: every study figure carries its source (TZ 0.1). */
  source: string;
  position?: "upper" | "middle" | "lower";
}

/** Brand stat card: big mono figure, short label, small source line. */
export const StatBadge: React.FC<StatBadgeProps> = ({ value, label, source, position = "upper" }) => {
  const frame = useCurrentFrame();
  const { width, height } = useCanvas();
  const { opacity, translateY } = useFadeSlide(frame, 6);
  const fs = Math.round(width * 0.03);
  return (
    <AbsoluteFill style={{ alignItems: position === "lower" ? "flex-start" : "flex-end", pointerEvents: "none" }}>
      <div
        style={{
          marginTop: height * (position === "upper" ? 0.2 : position === "middle" ? 0.42 : 0.555),
          marginRight: width * 0.06,
          marginLeft: width * 0.06,
          width: width * 0.5,
          background: YAFHO.white,
          borderLeft: `${fs * 0.3}px solid ${YAFHO.orange}`,
          borderRadius: 20,
          padding: `${fs * 0.7}px ${fs * 0.9}px`,
          boxSizing: "border-box",
          opacity,
          transform: `translateY(${translateY}px)`,
        }}
      >
        <div style={{ fontFamily: YAFHO.mono, fontWeight: 700, fontSize: fs * 2.4, lineHeight: 1, color: YAFHO.navy }}>{value}</div>
        <div style={{ fontFamily: YAFHO.sans, fontWeight: 800, fontSize: fs, lineHeight: 1.2, color: YAFHO.navy, marginTop: fs * 0.4 }}>{label}</div>
        <div style={{ fontFamily: YAFHO.sans, fontWeight: 500, fontSize: fs * 0.62, lineHeight: 1.3, color: YAFHO.muted, marginTop: fs * 0.5 }}>{source}</div>
      </div>
    </AbsoluteFill>
  );
};
