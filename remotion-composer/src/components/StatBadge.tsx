import { AbsoluteFill } from "remotion";
import { useCurrentFrame } from "remotion";
import { YAFHO, useCanvas, useFadeSlide } from "./yafho/tokens";

export interface StatBadgeProps {
  value: string;
  label: string;
  /** Required: every study figure carries its source (TZ 0.1). */
  source: string;
  position?: "upper" | "middle" | "lower" | "top" | "hero";
  /** Inside the 16:9 text panel: sits under the title, full panel width. */
  inPanel?: boolean;
}

/** Brand stat card: big mono figure, short label, small source line. */
export const StatBadge: React.FC<StatBadgeProps> = ({ value, label, source, position = "upper", inPanel = false }) => {
  const frame = useCurrentFrame();
  const { width, height } = useCanvas();
  const { opacity, translateY } = useFadeSlide(frame, 6);
  const fs = inPanel ? 26 : Math.round(width * (position === "top" ? 0.026 : 0.03));
  if (position === "hero") {
    // The effect figure as the frame's headline.
    const hs = Math.round(width * 0.05);
    return (
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", paddingBottom: height * 0.12, pointerEvents: "none" }}>
        <div
          style={{
            width: width * 0.86,
            background: YAFHO.white,
            borderRadius: 36,
            borderTop: `${hs * 0.25}px solid ${YAFHO.teal}`,
            padding: `${hs * 0.9}px ${hs}px`,
            boxSizing: "border-box",
            boxShadow: "0 24px 60px rgba(15,36,64,0.18)",
            textAlign: "center",
            opacity,
            transform: `translateY(${translateY}px)`,
          }}
        >
          <div style={{ fontFamily: YAFHO.sans, fontWeight: 800, fontSize: hs * 2.3, lineHeight: 1, color: YAFHO.navy }}>{value}</div>
          <div style={{ fontFamily: YAFHO.sans, fontWeight: 800, fontSize: hs * 0.95, lineHeight: 1.2, color: YAFHO.navy, marginTop: hs * 0.5, whiteSpace: "pre-line" }}>
            {label}
          </div>
          <div style={{ fontFamily: YAFHO.sans, fontWeight: 500, fontSize: hs * 0.5, lineHeight: 1.35, color: YAFHO.muted, marginTop: hs * 0.6 }}>{source}</div>
        </div>
      </AbsoluteFill>
    );
  }
  if (inPanel) {
    return (
      <AbsoluteFill style={{ justifyContent: "flex-end", paddingBottom: height * 0.1, pointerEvents: "none" }}>
        <div
          style={{
            background: YAFHO.white,
            borderLeft: `${fs * 0.3}px solid ${YAFHO.orange}`,
            borderRadius: 16,
            padding: `${fs * 0.6}px ${fs * 0.8}px`,
            opacity,
            transform: `translateY(${translateY}px)`,
          }}
        >
          <div style={{ fontFamily: YAFHO.mono, fontWeight: 700, fontSize: fs * 2, lineHeight: 1, color: YAFHO.navy }}>{value}</div>
          <div style={{ fontFamily: YAFHO.sans, fontWeight: 800, fontSize: fs, color: YAFHO.navy, marginTop: fs * 0.3 }}>{label}</div>
          <div style={{ fontFamily: YAFHO.sans, fontWeight: 500, fontSize: fs * 0.7, color: YAFHO.muted, marginTop: fs * 0.4 }}>{source}</div>
        </div>
      </AbsoluteFill>
    );
  }
  return (
    <AbsoluteFill style={{ alignItems: position === "lower" ? "flex-start" : "flex-end", pointerEvents: "none" }}>
      <div
        style={{
          marginTop: height * (position === "top" ? 0.15 : position === "upper" ? 0.2 : position === "middle" ? 0.42 : 0.555),
          marginRight: width * 0.06,
          marginLeft: width * 0.06,
          width: width * (position === "top" ? 0.44 : 0.5),
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
