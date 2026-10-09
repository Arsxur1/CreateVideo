import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { YAFHO, ease, useCanvas } from "./yafho/tokens";

export interface AudienceChipsProps {
  title?: string;
  chips: string[];
}

/** "Это про вас, если:" — recognisable situations pop in one by one (reach + relevance). */
export const AudienceChips: React.FC<AudienceChipsProps> = ({ title = "Это про вас, если:", chips }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const { width, height } = useCanvas();
  const fs = Math.round(width * 0.052);
  const out = 1 - ease(frame, durationInFrames - 0.4 * fps, durationInFrames);
  const t = ease(frame, 0, 0.4 * fps);
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: height * 0.22, opacity: out }}>
      <div
        style={{
          fontFamily: YAFHO.sans,
          fontWeight: 800,
          fontSize: fs * 1.15,
          color: YAFHO.navy,
          opacity: t,
          transform: `translateY(${(1 - t) * 24}px)`,
          marginBottom: fs * 0.9,
          whiteSpace: "pre-line",
          textAlign: "center",
          lineHeight: 1.15,
        }}
      >
        {title}
      </div>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: fs * 0.45 }}>
        {chips.map((c, i) => {
          const p = ease(frame, (0.35 + i * 0.32) * fps, (0.75 + i * 0.32) * fps);
          return (
            <div
              key={c}
              style={{
                display: "flex",
                alignItems: "center",
                gap: fs * 0.45,
                background: YAFHO.white,
                borderRadius: 999,
                padding: `${fs * 0.42}px ${fs * 0.9}px`,
                boxShadow: "0 10px 26px rgba(15,36,64,0.10)",
                fontFamily: YAFHO.sans,
                fontWeight: 800,
                fontSize: fs,
                color: YAFHO.navy,
                opacity: p,
                transform: `translateX(${(1 - p) * (i % 2 ? 60 : -60)}px)`,
              }}
            >
              <span style={{ width: fs * 0.42, height: fs * 0.42, borderRadius: "50%", background: YAFHO.orange, flex: "none" }} />
              {c}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
