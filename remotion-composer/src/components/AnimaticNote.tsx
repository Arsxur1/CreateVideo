import { AbsoluteFill } from "remotion";
import { YAFHO, useCanvas } from "./yafho/tokens";

export interface AnimaticNoteProps {
  /** e.g. "#3 · 0:10–0:15 · 3D" */
  label: string;
  /** Voice-over line for this shot. */
  text?: string;
}

/** Draft-only strip for animatics: shot number/timing and the voice-over line. */
export const AnimaticNote: React.FC<AnimaticNoteProps> = ({ label, text }) => {
  const { width, height } = useCanvas();
  const fs = Math.round(width * 0.024);
  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: height * 0.025, pointerEvents: "none" }}>
      <div
        style={{
          width: width * 0.92,
          background: "rgba(255,255,255,0.94)",
          border: `2px dashed ${YAFHO.muted}`,
          borderRadius: 16,
          padding: `${fs * 0.5}px ${fs * 0.8}px`,
          boxSizing: "border-box",
          fontFamily: YAFHO.sans,
          fontSize: fs,
          lineHeight: 1.3,
          color: YAFHO.navy,
        }}
      >
        <span style={{ fontFamily: YAFHO.mono, fontWeight: 700, color: YAFHO.muted }}>{label}</span>
        {text && <span style={{ fontWeight: 500 }}>{`  ГЗК: «${text}»`}</span>}
      </div>
    </AbsoluteFill>
  );
};
