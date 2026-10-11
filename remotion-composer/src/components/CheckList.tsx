import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { YAFHO, ease, useCanvas } from "./yafho/tokens";
import { MARK_COLOR, MARK_TINT, Mark } from "./MythFact";
import type { MarkKind } from "./MythFact";

export interface CheckListItem {
  text: string;
  /** ok ✓ · no ✗ · info ! (e.g. «к врачу») */
  kind?: MarkKind;
}

export interface CheckListProps {
  title?: string;
  items: CheckListItem[];
  /** Small line under the list (e.g. a caveat). */
  note?: string;
  /** Seconds between items appearing. */
  stagger?: number;
}

/**
 * Series 2 «Когда начинать» / «Когда нельзя»: a header and big ✓ / ✗ / ! rows
 * popping in one by one, centred in the upper part of the frame.
 */
export const CheckList: React.FC<CheckListProps> = ({ title, items, note, stagger = 0.45 }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const { width, height } = useCanvas();
  const fs = Math.round(width * 0.056);
  const out = 1 - ease(frame, durationInFrames - 1 - 0.4 * fps, durationInFrames - 1); // last frame fully faded
  const head = ease(frame, 0, 0.4 * fps);
  const last = 0.35 + items.length * stagger;

  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", paddingBottom: height * 0.12, opacity: out }}>
      {title && (
        <div
          style={{
            fontFamily: YAFHO.sans,
            fontWeight: 800,
            fontSize: fs * 1.12,
            color: YAFHO.navy,
            marginBottom: fs * 0.7,
            opacity: head,
            transform: `translateY(${(1 - head) * 24}px)`,
            textAlign: "center",
            whiteSpace: "pre-line",
          }}
        >
          {title}
        </div>
      )}
      <div style={{ display: "flex", flexDirection: "column", gap: fs * 0.38, width: width * 0.86 }}>
        {items.map((it, i) => {
          const k: MarkKind = it.kind ?? "ok";
          const p = ease(frame, (0.35 + i * stagger) * fps, (0.75 + i * stagger) * fps);
          return (
            <div
              key={it.text}
              style={{
                display: "flex",
                alignItems: "center",
                gap: fs * 0.5,
                background: MARK_TINT[k],
                borderLeft: `${fs * 0.2}px solid ${MARK_COLOR[k]}`,
                borderRadius: 28,
                padding: `${fs * 0.42}px ${fs * 0.6}px`,
                boxShadow: "0 12px 28px rgba(15,36,64,0.08)",
                opacity: p,
                transform: `translateX(${(1 - p) * 50}px)`,
              }}
            >
              <Mark kind={k} size={fs * 1.15} />
              <div style={{ fontFamily: YAFHO.sans, fontWeight: 800, fontSize: fs, lineHeight: 1.12, color: YAFHO.navy, whiteSpace: "pre-line" }}>
                {it.text}
              </div>
            </div>
          );
        })}
      </div>
      {note && (
        <div
          style={{
            marginTop: fs * 0.6,
            fontFamily: YAFHO.sans,
            fontWeight: 500,
            fontSize: fs * 0.55,
            color: YAFHO.muted,
            opacity: ease(frame, last * fps, (last + 0.4) * fps),
            textAlign: "center",
          }}
        >
          {note}
        </div>
      )}
    </AbsoluteFill>
  );
};
