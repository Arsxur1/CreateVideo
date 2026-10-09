import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { YAFHO, ease, useCanvas } from "./yafho/tokens";

export interface MythFactProps {
  myth: string;
  fact: string;
  /** e.g. "1 / 3" */
  counter?: string;
  areaTop?: number;
  /** "myth": ✗ mistake (struck) → ✓ right way; "qa": ? question → ✓ answer. */
  variant?: "myth" | "qa";
}

// Muted red for «ошибка» — 6.5:1 on white (text contrast ≥ 4.5:1), no neon.
export const WRONG = "#B42318";
export const WRONG_TINT = "#FBEAE8";
export const RIGHT_TINT = "#E3F3F1";
export const INFO_TINT = "#FCEFE6";
export const ASK_TINT = "#E8ECF2";

export type MarkKind = "ok" | "no" | "info" | "ask";
export const MARK_COLOR: Record<MarkKind, string> = { ok: YAFHO.teal, no: WRONG, info: YAFHO.orange, ask: YAFHO.navy };
export const MARK_TINT: Record<MarkKind, string> = { ok: RIGHT_TINT, no: WRONG_TINT, info: INFO_TINT, ask: ASK_TINT };

/** Round icon: ✓ ok, ✗ no, ! info, ? ask. */
export const Mark: React.FC<{ kind?: MarkKind; ok?: boolean; size: number }> = ({ kind, ok, size }) => {
  const k: MarkKind = kind ?? (ok ? "ok" : "no");
  return (
    <div
      style={{
        width: size,
        height: size,
        borderRadius: "50%",
        background: MARK_COLOR[k],
        flex: "none",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <svg width={size * 0.5} height={size * 0.5} viewBox="0 0 20 20">
        {k === "ok" && <path d="M3 10.5 L8 15.5 L17 4.5" stroke="#fff" strokeWidth={3.4} fill="none" strokeLinecap="round" strokeLinejoin="round" />}
        {k === "no" && <path d="M4 4 L16 16 M16 4 L4 16" stroke="#fff" strokeWidth={3.4} strokeLinecap="round" />}
        {k === "info" && (
          <>
            <path d="M10 3 L10 12" stroke="#fff" strokeWidth={3.4} strokeLinecap="round" />
            <circle cx={10} cy={16.5} r={1.9} fill="#fff" />
          </>
        )}
        {k === "ask" && (
          <>
            <path d="M6 7 C6 2.5 14 2.5 14 7 C14 10 10 10 10 13" stroke="#fff" strokeWidth={3.2} fill="none" strokeLinecap="round" />
            <circle cx={10} cy={17} r={1.9} fill="#fff" />
          </>
        )}
      </svg>
    </div>
  );
};

/**
 * Topic 07 «Мифы и ошибки»: ✗ the mistake (struck through) → ✓ the right way.
 * Two big cards in the upper part of the frame; titles stay free below.
 */
export const MythFact: React.FC<MythFactProps> = ({ myth, fact, counter, areaTop = 0.1, variant = "myth" }) => {
  const qa = variant === "qa";
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const { width, height } = useCanvas();
  const fs = Math.round(width * 0.062);
  const a = ease(frame, 0, 0.4 * fps);
  const strike = qa ? 0 : ease(frame, 0.7 * fps, 1.1 * fps);
  const b = ease(frame, 1.0 * fps, 1.4 * fps);
  const out = 1 - ease(frame, durationInFrames - 0.3 * fps, durationInFrames);
  const cardW = width * 0.88;

  const card = (ok: boolean, text: string, p: number, struck = 0) => (
    <div
      style={{
        width: cardW,
        boxSizing: "border-box",
        display: "flex",
        alignItems: "center",
        gap: fs * 0.55,
        padding: `${fs * 0.7}px ${fs * 0.7}px`,
        borderRadius: 36,
        background: ok ? RIGHT_TINT : qa ? ASK_TINT : WRONG_TINT,
        borderLeft: `${fs * 0.22}px solid ${ok ? YAFHO.teal : qa ? YAFHO.navy : WRONG}`,
        boxShadow: "0 16px 36px rgba(15,36,64,0.10)",
        opacity: p,
        transform: `translateY(${(1 - p) * 30}px)`,
      }}
    >
      <Mark kind={ok ? "ok" : qa ? "ask" : "no"} size={fs * 1.5} />
      <div style={{ position: "relative" }}>
        <div style={{ fontFamily: YAFHO.sans, fontWeight: 500, fontSize: fs * 0.5, color: ok ? YAFHO.tealText : qa ? YAFHO.navy : WRONG, marginBottom: fs * 0.1 }}>
          {qa ? (ok ? "Ответ" : "Вопрос") : ok ? "Правильно" : "Ошибка"}
        </div>
        <div style={{ position: "relative", fontFamily: YAFHO.sans, fontWeight: 800, fontSize: fs, lineHeight: 1.12, color: YAFHO.navy, whiteSpace: "pre-line" }}>
          {text}
          {!ok && !qa && (
            <div
              style={{
                position: "absolute",
                left: 0,
                top: "52%",
                height: fs * 0.1,
                width: `${struck * 100}%`,
                background: WRONG,
                borderRadius: 4,
              }}
            />
          )}
        </div>
      </div>
    </div>
  );

  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", paddingTop: height * areaTop * 0.5, paddingBottom: height * areaTop, opacity: out }}>
      {counter && (
        <div
          style={{
            fontFamily: YAFHO.mono,
            fontWeight: 700,
            fontSize: fs * 0.62,
            color: YAFHO.white,
            background: YAFHO.navy,
            borderRadius: 999,
            padding: `${fs * 0.15}px ${fs * 0.55}px`,
            marginBottom: fs * 0.6,
            opacity: a,
          }}
        >
          {counter}
        </div>
      )}
      {card(false, myth, a, strike)}
      <svg width={fs * 1.6} height={fs * 1.7} style={{ opacity: b, margin: `${fs * 0.2}px 0` }}>
        <line x1={fs * 0.8} y1={6} x2={fs * 0.8} y2={fs * 1.7 - 26} stroke={YAFHO.navy} strokeWidth={8} strokeLinecap="round" />
        <path d={`M ${fs * 0.8 - 22} ${fs * 1.7 - 34} L ${fs * 0.8} ${fs * 1.7 - 6} L ${fs * 0.8 + 22} ${fs * 1.7 - 34} Z`} fill={YAFHO.navy} />
      </svg>
      {card(true, fact, b)}
    </AbsoluteFill>
  );
};
