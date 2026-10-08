import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { CanvasContext, YAFHO, ease, useCanvas } from "./yafho/tokens";
import { SkinCrossSection3D } from "./SkinCrossSection3D";

export interface ScarCompareProps {
  /** Slice of the 0 → 6 month story shown by this cut (1 → 1 holds the end state). */
  progressFrom?: number;
  progressTo?: number;
  months?: number;
  leftLabel?: string;
  rightLabel?: string;
  note?: string;
  /** Fraction of the canvas height the two cards occupy (top part; the rest is for titles). */
  areaTop?: number;
  areaBottom?: number;
  /** Fade in from the background (off for a hook: frame 0 must already show the scene). */
  introFade?: boolean;
}

/**
 * The effect, side by side: the same young scar over ~6 months —
 * without care (ridge rises, collagen tangles) vs. with a silicone sheet
 * (scar flattens and pales, collagen aligns). Two 3D cards + month counter.
 */
export const ScarCompare: React.FC<ScarCompareProps> = ({
  progressFrom = 0,
  progressTo = 1,
  months = 6,
  leftLabel = "Без ухода",
  rightLabel = "С силиконом",
  note = "схема",
  areaTop = 0.035,
  areaBottom = 0.69,
  introFade = false,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const { width, height } = useCanvas();

  const p = progressFrom + (progressTo - progressFrom) * (frame / Math.max(1, durationInFrames - 1));
  const m = Math.round(p * months);
  const intro = introFade ? ease(frame, 0, 0.4 * fps) : 1;

  const gap = height * 0.05;
  const cardW = Math.round(width * 0.92);
  const cardH = Math.round((height * (areaBottom - areaTop) - gap) / 2);
  const left = (width - cardW) / 2;
  const fs = Math.round(width * 0.034);

  const Card: React.FC<{ top: number; label: string; swatch: string; phase: "untreated" | "treated"; showNote?: boolean }> = ({
    top,
    label,
    swatch,
    phase,
    showNote,
  }) => (
    <div
      style={{
        position: "absolute",
        left,
        top,
        width: cardW,
        height: cardH,
        borderRadius: 32,
        overflow: "hidden",
        background: YAFHO.offWhite,
        boxShadow: "0 18px 40px rgba(15,36,64,0.14)",
      }}
    >
      <CanvasContext.Provider value={{ width: cardW, height: cardH }}>
        <SkinCrossSection3D
          phase={phase}
          introFade={false}
          grade={false}
          centerY={0.56}
          fitFrac={0.94}
          progressFrom={progressFrom}
          progressTo={progressTo}
        />
      </CanvasContext.Provider>
      <div
        style={{
          position: "absolute",
          left: 24,
          top: 22,
          display: "flex",
          alignItems: "center",
          gap: 14,
          background: YAFHO.white,
          borderRadius: 999,
          padding: `${fs * 0.35}px ${fs * 0.75}px`,
          fontFamily: YAFHO.sans,
          fontWeight: 800,
          fontSize: fs,
          color: YAFHO.navy,
        }}
      >
        <span style={{ width: fs * 0.55, height: fs * 0.55, borderRadius: "50%", background: swatch }} />
        {label}
      </div>
      {showNote && (
        <div
          style={{
            position: "absolute",
            right: 24,
            bottom: 18,
            fontFamily: YAFHO.sans,
            fontWeight: 500,
            fontSize: fs * 0.55,
            color: YAFHO.muted,
            background: "rgba(255,255,255,0.85)",
            borderRadius: 10,
            padding: "4px 10px",
          }}
        >
          {note}
        </div>
      )}
    </div>
  );

  const topY = height * areaTop;
  const counterY = topY + cardH + gap / 2;

  return (
    <AbsoluteFill style={{ opacity: intro }}>
      <Card top={topY} label={leftLabel} swatch={YAFHO.orange} phase="untreated" />
      <Card top={topY + cardH + gap} label={rightLabel} swatch={YAFHO.teal} phase="treated" showNote />
      {/* month counter between the cards */}
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: counterY,
          transform: "translateY(-50%)",
          display: "flex",
          justifyContent: "center",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 18,
            background: YAFHO.navy,
            color: YAFHO.white,
            borderRadius: 999,
            padding: `${fs * 0.3}px ${fs * 0.8}px`,
            fontFamily: YAFHO.mono,
            fontWeight: 700,
            fontSize: fs * 1.05,
          }}
        >
          <span>{`${m} мес`}</span>
          <span style={{ width: width * 0.22, height: 8, borderRadius: 4, background: "rgba(255,255,255,0.25)", overflow: "hidden" }}>
            <span style={{ display: "block", height: "100%", width: `${interpolate(p, [0, 1], [0, 100])}%`, background: YAFHO.orange }} />
          </span>
          <span style={{ opacity: 0.75 }}>{`${months} мес`}</span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
