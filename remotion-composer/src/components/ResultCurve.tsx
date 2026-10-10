import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { YAFHO, ease, useCanvas } from "./yafho/tokens";

export interface ResultMilestone {
  /** Month on the x axis where the label pins to the silicone curve. */
  at: number;
  label: string;
}

export interface ResultCurveProps {
  months?: number;
  milestones?: ResultMilestone[];
  withLabel?: string;
  withoutLabel?: string;
  axisLabel?: string;
  note?: string;
  areaTop?: number;
  areaBottom?: number;
}

const DEFAULT_MILESTONES: ResultMilestone[] = [
  { at: 0.6, label: "недели — первые изменения" },
  { at: 2, label: "1–3 мес — заметно" },
  { at: 4.6, label: "3–6 мес — ровнее" },
];

// Schematic only (no study data): visibility of the scar, 0 = invisible, 1 = very visible.
const withSilicone = (m: number) => 0.62 - 0.4 * (1 - Math.exp(-m / 2.2)) - 0.02 * m;
const withoutCare = (m: number) => 0.62 + 0.2 * (1 - Math.exp(-m / 1.4));

/**
 * Topic 05 «Результат»: when to expect what (product passport timings).
 * Teal «с силиконом» curve goes down, grey dashed «без ухода» does not;
 * milestone chips pop as the curve draws. Marked «схема» — not study data.
 */
export const ResultCurve: React.FC<ResultCurveProps> = ({
  months = 6,
  milestones = DEFAULT_MILESTONES,
  withLabel = "С силиконом",
  withoutLabel = "Без ухода",
  axisLabel = "заметность рубца",
  note = "схема по срокам из инструкции",
  areaTop = 0.035,
  areaBottom = 0.69,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const { width, height } = useCanvas();
  const t = frame / Math.max(1, durationInFrames - 1);
  const draw = ease(t, 0.08, 0.72);
  const fs0 = Math.round(width * 0.034);

  const cardW = Math.round(width * 0.92);
  const cardH = Math.round(height * (areaBottom - areaTop));
  // the milestone list must fit under the plot on short cards (Telegram 1:1); 9:16, 4:5, 16:9 unchanged
  const fs = Math.round(Math.min(fs0, cardH * 0.042));
  const left = (width - cardW) / 2;
  const top = height * areaTop;

  const padL = cardW * 0.1;
  const padR = cardW * 0.06;
  const padT = cardH * 0.2;
  const padB = cardH * 0.36; // room for the numbered milestone list
  const plotW = cardW - padL - padR;
  const plotH = cardH - padT - padB;
  const X = (m: number) => padL + (m / months) * plotW;
  const Y = (v: number) => padT + (1 - v) * plotH;

  const path = (f: (m: number) => number, upto: number) => {
    const n = 80;
    const pts: string[] = [];
    for (let i = 0; i <= n; i++) {
      const m = (i / n) * months * upto;
      pts.push(`${i === 0 ? "M" : "L"} ${X(m).toFixed(1)} ${Y(f(m)).toFixed(1)}`);
    }
    return pts.join(" ");
  };
  const head = months * draw;
  const ticks = [0, 1, 3, 6].filter((m) => m <= months);

  return (
    <AbsoluteFill>
      <div
        style={{
          position: "absolute",
          left,
          top,
          width: cardW,
          height: cardH,
          borderRadius: 36,
          background: YAFHO.white,
          boxShadow: "0 18px 40px rgba(15,36,64,0.12)",
          overflow: "hidden",
        }}
      >
        {/* legend */}
        <div style={{ position: "absolute", left: padL, top: cardH * 0.05, display: "flex", gap: fs * 0.8, flexWrap: "wrap" }}>
          {[
            { c: YAFHO.teal, l: withLabel, dash: false },
            { c: "#8A929E", l: withoutLabel, dash: true },
          ].map((it) => (
            <div key={it.l} style={{ display: "flex", alignItems: "center", gap: fs * 0.35, fontFamily: YAFHO.sans, fontWeight: 800, fontSize: fs, color: YAFHO.navy }}>
              <svg width={fs * 1.6} height={fs * 0.6}>
                <line x1={2} y1={fs * 0.3} x2={fs * 1.6 - 2} y2={fs * 0.3} stroke={it.c} strokeWidth={8} strokeLinecap="round" strokeDasharray={it.dash ? "10 9" : undefined} />
              </svg>
              {it.l}
            </div>
          ))}
        </div>
        <svg width={cardW} height={cardH} style={{ position: "absolute", left: 0, top: 0 }}>
          {/* axes */}
          <line x1={padL} y1={padT - 10} x2={padL} y2={padT + plotH} stroke={YAFHO.navy} strokeOpacity={0.35} strokeWidth={3} />
          <line x1={padL} y1={padT + plotH} x2={padL + plotW} y2={padT + plotH} stroke={YAFHO.navy} strokeOpacity={0.35} strokeWidth={3} />
          {ticks.map((m) => (
            <g key={m}>
              <line x1={X(m)} y1={padT} x2={X(m)} y2={padT + plotH} stroke={YAFHO.navy} strokeOpacity={0.08} strokeWidth={2} />
              <text
                x={X(m)}
                y={padT + plotH + fs * 1.3}
                textAnchor={m === 0 ? "start" : m === months ? "end" : "middle"}
                fontFamily={YAFHO.mono}
                fontWeight={700}
                fontSize={fs * 0.85}
                fill={YAFHO.navy}
              >
                {m === 0 ? "0" : `${m} мес`}
              </text>
            </g>
          ))}
          <text
            x={padL - fs * 0.6}
            y={padT + plotH / 2}
            transform={`rotate(-90 ${padL - fs * 0.6} ${padT + plotH / 2})`}
            textAnchor="middle"
            fontFamily={YAFHO.sans}
            fontWeight={500}
            fontSize={fs * 0.72}
            fill={YAFHO.muted}
          >
            {axisLabel}
          </text>
          {/* curves */}
          <path d={path(withoutCare, draw)} stroke="#8A929E" strokeWidth={8} fill="none" strokeLinecap="round" strokeDasharray="16 14" />
          <path d={path(withSilicone, draw)} stroke={YAFHO.teal} strokeWidth={10} fill="none" strokeLinecap="round" strokeLinejoin="round" />
          {draw > 0.01 && <circle cx={X(head)} cy={Y(withSilicone(head))} r={14} fill={YAFHO.teal} stroke={YAFHO.white} strokeWidth={5} />}
          {/* the gap between the outcomes */}
          {draw > 0.98 && (
            <g opacity={ease(t, 0.74, 0.82)}>
              <line
                x1={X(months) - 26}
                y1={Y(withoutCare(months)) + 18}
                x2={X(months) - 26}
                y2={Y(withSilicone(months)) - 20}
                stroke={YAFHO.orange}
                strokeWidth={7}
                markerEnd="url(#rc-a)"
              />
            </g>
          )}
          <defs>
            <marker id="rc-a" markerUnits="userSpaceOnUse" markerWidth="26" markerHeight="26" refX="20" refY="13" orient="auto">
              <path d="M0,0 L26,13 L0,26 Z" fill={YAFHO.orange} />
            </marker>
          </defs>
          {milestones.map((ms, i) => (
            <g key={ms.at} opacity={ease(head, ms.at, ms.at + 0.25)}>
              <circle cx={X(ms.at)} cy={Y(withSilicone(ms.at))} r={fs * 0.62} fill={YAFHO.white} stroke={YAFHO.teal} strokeWidth={5} />
              <text x={X(ms.at)} y={Y(withSilicone(ms.at)) + fs * 0.3} textAnchor="middle" fontFamily={YAFHO.mono} fontWeight={700} fontSize={fs * 0.8} fill={YAFHO.navy}>
                {i + 1}
              </text>
            </g>
          ))}
        </svg>
        <div style={{ position: "absolute", left: padL, right: padR, top: padT + plotH + fs * 2.3, display: "flex", flexDirection: "column", gap: fs * 0.45 }}>
          {milestones.map((ms, i) => {
            const o = ease(head, ms.at, ms.at + 0.35);
            return (
              <div
                key={ms.label}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: fs * 0.45,
                  opacity: o,
                  transform: `translateX(${(1 - o) * 24}px)`,
                  fontFamily: YAFHO.sans,
                  fontWeight: 800,
                  fontSize: fs * 1.05,
                  color: YAFHO.navy,
                }}
              >
                <span
                  style={{
                    width: fs * 1.3,
                    height: fs * 1.3,
                    borderRadius: "50%",
                    border: `5px solid ${YAFHO.teal}`,
                    boxSizing: "border-box",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontFamily: YAFHO.mono,
                    fontSize: fs * 0.8,
                    flex: "none",
                  }}
                >
                  {i + 1}
                </span>
                {ms.label}
              </div>
            );
          })}
        </div>
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
      </div>
    </AbsoluteFill>
  );
};
