import React from "react";
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { YAFHO, ease, useCanvas } from "./yafho/tokens";

export type SkinShape = "line" | "csection" | "burn" | "keloid" | "stria";
export type SkinStep = "effect" | "clean" | "measure" | "apply" | "wear" | "rinse" | "idle" | "compare";
export type ScarState = "fresh" | "hyper" | "soft";

export interface SkinSwatchProps {
  shape?: SkinShape;
  step?: SkinStep;
  /** Scar maturity window for effect / compare (0 = young scar, 1 = outcome after `months`). */
  progressFrom?: number;
  progressTo?: number;
  months?: number;
  /** effect: lift the sheet at the end to reveal the result. */
  reveal?: boolean;
  /** idle: the sheet lands on the scar. */
  land?: boolean;
  /** idle: which scar state is shown. */
  state?: ScarState;
  /** effect: the starting scar (hyper = red, raised — the most visible change). */
  from?: ScarState;
  areaTop?: number;
  areaBottom?: number;
  zoom?: number;
  note?: string;
  introFade?: boolean;
  leftLabel?: string;
  rightLabel?: string;
}

// Mirrors projects/yafho/make_skin.py: images are 1600 px square, 60 px per cm, scar centred.
const IMG_PX = 1600;
const IMG_PX_CM = 60;
const SHAPES: Record<SkinShape, { box: [number, number]; sheet: [number, number]; zoom: number }> = {
  line: { box: [0.6, 10], sheet: [4, 13], zoom: 1 },
  csection: { box: [12, 1.2], sheet: [15, 5], zoom: 1 },
  burn: { box: [7, 9], sheet: [10, 15], zoom: 0.95 },
  keloid: { box: [2.2, 1.5], sheet: [4, 4], zoom: 2.2 },
  stria: { box: [3.4, 9], sheet: [10, 15], zoom: 1 },
};

/** Quadratic curve from p0 via c to p1, cut at t (so an end marker sits on the drawn tip). */
function quadTo(p0: [number, number], c: [number, number], p1: [number, number], t: number): string {
  const k = Math.max(0.001, Math.min(1, t));
  const c1: [number, number] = [p0[0] + (c[0] - p0[0]) * k, p0[1] + (c[1] - p0[1]) * k];
  const b = (i: 0 | 1) => (1 - k) ** 2 * p0[i] + 2 * (1 - k) * k * c[i] + k ** 2 * p1[i];
  return `M ${p0[0]} ${p0[1]} Q ${c1[0]} ${c1[1]} ${b(0)} ${b(1)}`;
}

const src = (shape: SkinShape, state: ScarState) => staticFile(`yafho-skin/skin_${shape}_${state}.png`);

/** Translucent medical-silicone sheet seen from above (realistic light: 3D exception). */
const Sheet: React.FC<{
  cx: number;
  cy: number;
  w: number;
  h: number;
  ppc: number;
  lift?: number;
  peel?: number;
  opacity?: number;
  scale?: number;
  rotate?: number;
  sheen?: number;
  label?: string;
}> = ({ cx, cy, w, h, ppc, lift = 0, peel = 0, opacity = 1, scale = 1, rotate = 0, sheen = 0.3, label }) => {
  const s = scale * (1 + lift * 0.07);
  const sh = 3 + lift * 34 + peel * 20;
  return (
    <div
      style={{
        position: "absolute",
        left: cx - w / 2,
        top: cy - h / 2,
        width: w,
        height: h,
        opacity,
        transform: `translateY(${-lift * 40}px) scale(${s}) rotate(${rotate}deg) perspective(1800px) rotateX(${-peel * 52}deg)`,
        transformOrigin: "50% 100%",
        borderRadius: 0.55 * ppc,
        background: "rgba(252, 249, 246, 0.17)",
        border: "2px solid rgba(255,255,255,0.62)",
        boxShadow: `0 ${sh * 0.8}px ${sh * 1.6}px rgba(70,35,25,${0.2 + lift * 0.06}), inset 0 0 0 1px rgba(255,255,255,0.22), inset 0 3px 8px rgba(255,255,255,0.35)`,
        backdropFilter: "blur(1.4px) saturate(0.9) brightness(1.04)",
        WebkitBackdropFilter: "blur(1.4px) saturate(0.9) brightness(1.04)",
        overflow: "hidden",
      }}
    >
      {/* soft specular band — the sheet catches the window light */}
      <div
        style={{
          position: "absolute",
          inset: "-20%",
          background: `linear-gradient(118deg, transparent ${sheen * 100 - 14}%, rgba(255,255,255,0.26) ${sheen * 100}%, transparent ${sheen * 100 + 12}%)`,
        }}
      />
      {label && (
        <div
          style={{
            position: "absolute",
            right: 0.35 * ppc,
            top: 0.35 * ppc,
            minWidth: 0.9 * ppc,
            height: 0.9 * ppc,
            borderRadius: 999,
            background: YAFHO.navy,
            color: YAFHO.white,
            fontFamily: YAFHO.mono,
            fontWeight: 700,
            fontSize: 0.55 * ppc,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          {label}
        </div>
      )}
    </div>
  );
};

const Chip: React.FC<{ fs: number; children: React.ReactNode; dot?: string; style?: React.CSSProperties }> = ({ fs, children, dot, style }) => (
  <div
    style={{
      position: "absolute",
      display: "flex",
      alignItems: "center",
      gap: fs * 0.4,
      background: YAFHO.white,
      borderRadius: 999,
      padding: `${fs * 0.32}px ${fs * 0.72}px`,
      fontFamily: YAFHO.sans,
      fontWeight: 800,
      fontSize: fs,
      color: YAFHO.navy,
      boxShadow: "0 8px 20px rgba(15,36,64,0.12)",
      whiteSpace: "nowrap",
      ...style,
    }}
  >
    {dot && <span style={{ width: fs * 0.55, height: fs * 0.55, borderRadius: "50%", background: dot, flex: "none" }} />}
    {children}
  </div>
);

const MonthPill: React.FC<{ p: number; months: number; fs: number; width: number }> = ({ p, months, fs, width }) => (
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
    <span>{`${Math.round(p * months)} мес`}</span>
    <span style={{ width: width * 0.22, height: 8, borderRadius: 4, background: "rgba(255,255,255,0.25)", overflow: "hidden" }}>
      <span style={{ display: "block", height: "100%", width: `${p * 100}%`, background: YAFHO.teal }} />
    </span>
    <span style={{ opacity: 0.75 }}>{`${months} мес`}</span>
  </div>
);

/** Skin card: the scar photo-layers (fresh → target crossfade) plus whatever the step draws on top. */
const SkinCard: React.FC<{
  x: number;
  y: number;
  w: number;
  h: number;
  shape: SkinShape;
  zoom: number;
  target: ScarState;
  mix: number;
  base?: ScarState;
  children?: (geo: { cx: number; cy: number; ppc: number }) => React.ReactNode;
}> = ({ x, y, w, h, shape, zoom, target, mix, base = "fresh", children }) => {
  const scale = (Math.max(w, h) / IMG_PX) * Math.max(1, zoom); // never below cover
  const size = IMG_PX * scale;
  const ppc = IMG_PX_CM * scale;
  const cx = w / 2;
  const cy = h / 2;
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width: w,
        height: h,
        borderRadius: 36,
        overflow: "hidden",
        background: "#E0BEA6",
        boxShadow: "0 18px 40px rgba(15,36,64,0.16)",
      }}
    >
      <Img src={src(shape, base)} style={{ position: "absolute", left: cx - size / 2, top: cy - size / 2, width: size, height: size }} />
      {mix > 0.001 && target !== base && (
        <Img
          src={src(shape, target)}
          style={{ position: "absolute", left: cx - size / 2, top: cy - size / 2, width: size, height: size, opacity: mix }}
        />
      )}
      {children?.({ cx, cy, ppc })}
    </div>
  );
};

/**
 * Top-down skin close-up with a healed scar and a silicone sheet — the
 * product's effect and the how-to steps, drawn in code (no Kling needed).
 *
 * step:
 *   effect  — sheet on, the scar turns softer, paler, flatter over `months`; sheet lifts to reveal
 *   compare — «без ухода» (scar thickens) vs «с силиконом» (scar softens), month counter
 *   clean   — pad wipes the skin, droplets disappear
 *   measure — orange outline grows from the scar to +1 cm on every side
 *   apply   — sheet lands and is smoothed flat
 *   wear    — 24 h dial fills to 23 h, then a sleeve covers the sheet
 *   rinse   — sheet A lifts and is rinsed, sheet B takes its place
 *   idle    — scar (any state), optional sheet landing
 */
export const SkinSwatch: React.FC<SkinSwatchProps> = ({
  shape = "line",
  step = "effect",
  progressFrom = 0,
  progressTo = 1,
  months = 6,
  reveal = true,
  land = false,
  state = "fresh",
  from = "fresh",
  areaTop = 0.035,
  areaBottom = 0.69,
  zoom,
  note = "схема",
  introFade = false,
  leftLabel = "Без ухода",
  rightLabel = "С силиконом",
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const { width, height } = useCanvas();
  const t = frame / Math.max(1, durationInFrames - 1);
  const T = (a: number, b: number) => ease(t, a, b);
  const intro = introFade ? ease(frame, 0, 0.4 * fps) : 1;
  const geo = SHAPES[shape];
  const z = zoom ?? geo.zoom;
  const fs = Math.round(width * 0.034);

  const cardW = Math.round(width * 0.92);
  const left = (width - cardW) / 2;
  const top = height * areaTop;
  const areaH = height * (areaBottom - areaTop);

  const noteEl = (
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
  );

  // ---------------------------------------------------------------- compare
  if (step === "compare") {
    const p = progressFrom + (progressTo - progressFrom) * t;
    const gap = height * 0.05;
    const wide = cardW / areaH > 0.95;
    const cw = wide ? Math.round((cardW - gap * 0.6) / 2) : cardW;
    const ch = wide ? Math.round(areaH - gap) : Math.round((areaH - gap) / 2);
    const z2 = zoom ?? geo.zoom;
    const second = wide ? { x: left + cw + gap * 0.6, y: top } : { x: left, y: top + ch + gap };
    return (
      <AbsoluteFill style={{ opacity: intro }}>
        <SkinCard x={left} y={top} w={cw} h={ch} shape={shape} zoom={z2} target="hyper" mix={p}>
          {() => (
            <Chip fs={fs} dot={YAFHO.orange} style={{ left: 24, top: 22 }}>
              {leftLabel}
            </Chip>
          )}
        </SkinCard>
        <SkinCard x={second.x} y={second.y} w={cw} h={ch} shape={shape} zoom={z2} target="soft" mix={p}>
          {({ cx, cy, ppc }) => (
            <>
              <Sheet cx={cx} cy={cy} w={geo.sheet[0] * ppc} h={geo.sheet[1] * ppc} ppc={ppc} sheen={0.25 + p * 0.3} />
              <Chip fs={fs} dot={YAFHO.teal} style={{ left: 24, top: 22 }}>
                {rightLabel}
              </Chip>
              {noteEl}
            </>
          )}
        </SkinCard>
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: wide ? top + ch + gap * 0.5 : top + ch + gap / 2,
            transform: "translateY(-50%)",
            display: "flex",
            justifyContent: "center",
          }}
        >
          <MonthPill p={p} months={months} fs={fs} width={width} />
        </div>
      </AbsoluteFill>
    );
  }

  // ---------------------------------------------------------------- single card steps
  let target: ScarState = state;
  let mix = 0;
  let base: ScarState = step === "idle" ? state : "fresh";
  if (step === "effect") {
    target = "soft";
    mix = progressFrom + (progressTo - progressFrom) * T(0.06, reveal ? 0.6 : 0.8);
    base = from;
  }

  return (
    <AbsoluteFill style={{ opacity: intro }}>
      <SkinCard x={left} y={top} w={cardW} h={Math.round(areaH)} shape={shape} zoom={z} target={target} mix={mix} base={base}>
        {({ cx, cy, ppc }) => {
          const sw = geo.sheet[0] * ppc;
          const shh = geo.sheet[1] * ppc;
          const bw = geo.box[0] * ppc;
          const bh = geo.box[1] * ppc;
          const cardH = Math.round(areaH);

          if (step === "effect") {
            const landP = land ? T(0, 0.12) : 1;
            const peel = reveal ? T(0.62, 0.78) : 0;
            const away = reveal ? T(0.75, 0.86) : 0;
            return (
              <>
                <Sheet
                  cx={cx}
                  cy={cy - away * cardH * 0.25}
                  w={sw}
                  h={shh}
                  ppc={ppc}
                  lift={1 - landP + peel * 0.6}
                  peel={peel}
                  opacity={(land ? T(0, 0.06) : 1) * (1 - away)}
                  sheen={0.2 + t * 0.5}
                />
                <div style={{ position: "absolute", left: 0, right: 0, top: 26, display: "flex", justifyContent: "center" }}>
                  <MonthPill p={mix} months={months} fs={fs} width={width} />
                </div>
                {noteEl}
              </>
            );
          }

          if (step === "clean") {
            const padP = T(0.08, 0.72);
            const padX = cx + interpolate(padP, [0, 1], [-0.75, 0.75]) * cardW;
            const padY = cy + Math.sin(padP * Math.PI * 3) * ppc * 1.2;
            const padR = 2.6 * ppc;
            const padOn = T(0.02, 0.1) * (1 - T(0.74, 0.84));
            const drops = Array.from({ length: 22 }, (_, i) => {
              const a = (i * 137.5 * Math.PI) / 180;
              const r = (1.2 + ((i * 53) % 37) / 37 * 4.2) * ppc;
              return { x: cx + Math.cos(a) * r * 1.1, y: cy + Math.sin(a) * r * 1.3, s: (0.12 + ((i * 29) % 11) / 11 * 0.22) * ppc };
            });
            return (
              <>
                {drops.map((d, i) => {
                  const gone = padOn > 0.01 && padX > d.x + padR * 0.2 ? 1 : 0;
                  const passed = interpolate(padX - d.x, [-padR, padR * 0.3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
                  const o = (1 - Math.max(gone, passed)) * T(0, 0.04);
                  return (
                    <div
                      key={i}
                      style={{
                        position: "absolute",
                        left: d.x - d.s,
                        top: d.y - d.s,
                        width: d.s * 2,
                        height: d.s * 2,
                        borderRadius: "50%",
                        opacity: o,
                        background: "rgba(255,255,255,0.22)",
                        border: "1.5px solid rgba(255,255,255,0.7)",
                        boxShadow: `${d.s * 0.25}px ${d.s * 0.35}px ${d.s * 0.5}px rgba(90,45,30,0.25), inset ${d.s * 0.3}px ${d.s * 0.3}px ${d.s * 0.4}px rgba(255,255,255,0.65)`,
                      }}
                    />
                  );
                })}
                {/* wipe direction */}
                <svg width={cardW} height={cardH} style={{ position: "absolute", left: 0, top: 0, opacity: padOn }}>
                  <defs>
                    <marker id="cl-ar" markerWidth="8" markerHeight="8" refX="5" refY="4" orient="auto">
                      <path d="M0,0 L8,4 L0,8 Z" fill={YAFHO.orange} />
                    </marker>
                  </defs>
                  <path
                    d={quadTo([cx - cardW * 0.36, cy - 4.8 * ppc], [cx, cy - 6.2 * ppc], [cx + cardW * 0.36, cy - 4.8 * ppc], padP)}
                    stroke={YAFHO.orange}
                    strokeWidth={8}
                    fill="none"
                    strokeLinecap="round"
                    markerEnd={padP > 0.05 ? "url(#cl-ar)" : undefined}
                  />
                </svg>
                <div
                  style={{
                    position: "absolute",
                    left: padX - padR,
                    top: padY - padR,
                    width: padR * 2,
                    height: padR * 2,
                    borderRadius: "50%",
                    opacity: padOn,
                    background: "#FBFBF9",
                    border: "1px solid rgba(0,0,0,0.05)",
                    boxShadow: "0 22px 40px rgba(70,35,25,0.28), inset 0 -6px 14px rgba(0,0,0,0.05)",
                    backgroundImage: "radial-gradient(rgba(0,0,0,0.05) 1.5px, transparent 2px)",
                    backgroundSize: "14px 14px",
                  }}
                />
              </>
            );
          }

          if (step === "measure" || step === "apply") {
            const grow = step === "measure" ? T(0.12, 0.5) : 1;
            const m = grow * ppc;
            const outlineO = step === "measure" ? T(0.05, 0.12) : 1 - T(0.35, 0.6);
            const labelsO = step === "measure" ? T(0.48, 0.6) : 0;
            const rx = cx - bw / 2 - m;
            const ry = cy - bh / 2 - m;
            const landP = step === "apply" ? T(0.08, 0.55) : 0;
            const ax = cx + bw / 2;
            const ay = cy - bh / 2;
            return (
              <>
                <svg width={cardW} height={cardH} style={{ position: "absolute", left: 0, top: 0 }}>
                  <defs>
                    <marker id="ms-a" markerUnits="userSpaceOnUse" markerWidth="22" markerHeight="22" refX="20" refY="11" orient="auto-start-reverse">
                      <path d="M0,0 L22,11 L0,22 Z" fill={YAFHO.orange} />
                    </marker>
                  </defs>
                  <rect
                    x={rx}
                    y={ry}
                    width={bw + 2 * m}
                    height={bh + 2 * m}
                    rx={Math.min(0.5 * ppc, (bw + 2 * m) / 2)}
                    fill="none"
                    stroke={YAFHO.orange}
                    strokeWidth={6}
                    strokeDasharray="20 12"
                    opacity={outlineO}
                  />
                  <g opacity={labelsO} stroke={YAFHO.orange} strokeWidth={6}>
                    <line x1={ax + 4} y1={cy} x2={ax + ppc - 2} y2={cy} markerStart="url(#ms-a)" markerEnd="url(#ms-a)" />
                    <line x1={cx} y1={ay - 4} x2={cx} y2={ay - ppc + 2} markerStart="url(#ms-a)" markerEnd="url(#ms-a)" />
                  </g>
                </svg>
                <Chip fs={fs * 1.15} style={{ left: ax + ppc + 18, top: cy - fs * 0.95, opacity: labelsO, color: YAFHO.orange }}>
                  +1 см
                </Chip>
                <Chip fs={fs * 1.15} style={{ left: cx + 22, top: ay - ppc - fs * 1.0, opacity: labelsO, color: YAFHO.orange }}>
                  +1 см
                </Chip>
                {step === "apply" && (
                  <>
                    <Sheet
                      cx={cx}
                      cy={cy - (1 - landP) * cardH * 0.18}
                      w={sw}
                      h={shh}
                      ppc={ppc}
                      lift={1 - landP}
                      opacity={T(0.02, 0.12)}
                      sheen={interpolate(T(0.58, 0.9), [0, 1], [0.05, 0.95])}
                    />
                    {/* smoothing strokes: press from the centre outwards */}
                    <svg width={cardW} height={cardH} style={{ position: "absolute", left: 0, top: 0, opacity: T(0.56, 0.62) * (1 - T(0.9, 0.98)) }}>
                      <defs>
                        <marker id="ap-a" markerWidth="8" markerHeight="8" refX="5" refY="4" orient="auto">
                          <path d="M0,0 L8,4 L0,8 Z" fill={YAFHO.teal} />
                        </marker>
                      </defs>
                      {[-1, 1].map((d) => {
                        const along = shh >= sw;
                        const len = (along ? shh : sw) * 0.36 * T(0.58, 0.85);
                        return (
                          <line
                            key={d}
                            x1={cx + (along ? 0 : d * 0.08 * sw)}
                            y1={cy + (along ? d * 0.08 * shh : 0)}
                            x2={cx + (along ? 0 : d * (0.08 * sw + len))}
                            y2={cy + (along ? d * (0.08 * shh + len) : 0)}
                            stroke={YAFHO.teal}
                            strokeWidth={8}
                            strokeLinecap="round"
                            markerEnd="url(#ap-a)"
                          />
                        );
                      })}
                    </svg>
                  </>
                )}
              </>
            );
          }

          if (step === "wear") {
            const hours = 23 * T(0.06, 0.5);
            const dial = cardW * 0.27;
            const sleeve = T(0.55, 0.78);
            const R = dial / 2 - 18;
            const arc = (h0: number, h1: number) => {
              const a0 = (h0 / 24) * 2 * Math.PI - Math.PI / 2;
              const a1 = (h1 / 24) * 2 * Math.PI - Math.PI / 2;
              const large = h1 - h0 > 12 ? 1 : 0;
              return `M ${dial / 2 + R * Math.cos(a0)} ${dial / 2 + R * Math.sin(a0)} A ${R} ${R} 0 ${large} 1 ${dial / 2 + R * Math.cos(a1)} ${dial / 2 + R * Math.sin(a1)}`;
            };
            const sheetBottom = cy + shh / 2;
            const sleeveBottom = interpolate(sleeve, [0, 1], [-cardH * 0.1, Math.min(cardH * 0.9, sheetBottom + 1.6 * ppc)]);
            return (
              <>
                <Sheet cx={cx} cy={cy} w={sw} h={shh} ppc={ppc} sheen={0.3 + t * 0.2} />
                {/* sleeve slides down over the sheet: invisible under clothes */}
                <div
                  style={{
                    position: "absolute",
                    left: -20,
                    right: -20,
                    top: -40,
                    height: Math.max(0, sleeveBottom + 40),
                    background: `repeating-linear-gradient(90deg, #DCD3C6 0px, #DCD3C6 7px, #CFC5B6 7px, #CFC5B6 11px)`,
                    boxShadow: "0 22px 30px rgba(60,30,18,0.32)",
                    borderBottom: `${ppc * 1.1}px solid #C6BBAB`,
                    borderRadius: "0 0 10px 10px",
                  }}
                />
                <div style={{ position: "absolute", right: 22, top: 22, width: dial, height: dial }}>
                  <svg width={dial} height={dial}>
                    <circle cx={dial / 2} cy={dial / 2} r={dial / 2} fill={YAFHO.white} />
                    <path d={arc(12, 23)} stroke={YAFHO.teal} strokeOpacity={0.28} strokeWidth={22} fill="none" />
                    {hours > 0.05 && <path d={arc(0, hours)} stroke={hours >= 12 ? YAFHO.teal : YAFHO.orange} strokeWidth={14} fill="none" strokeLinecap="round" />}
                    {Array.from({ length: 24 }, (_, i) => {
                      const a = (i / 24) * 2 * Math.PI - Math.PI / 2;
                      const r0 = R - (i % 6 === 0 ? 30 : 22);
                      return (
                        <line
                          key={i}
                          x1={dial / 2 + r0 * Math.cos(a)}
                          y1={dial / 2 + r0 * Math.sin(a)}
                          x2={dial / 2 + (R - 14) * Math.cos(a)}
                          y2={dial / 2 + (R - 14) * Math.sin(a)}
                          stroke={YAFHO.navy}
                          strokeOpacity={i % 6 === 0 ? 0.8 : 0.3}
                          strokeWidth={i % 6 === 0 ? 4 : 2}
                        />
                      );
                    })}
                  </svg>
                  <div
                    style={{
                      position: "absolute",
                      inset: 0,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontFamily: YAFHO.mono,
                      fontWeight: 700,
                      fontSize: dial * 0.2,
                      color: YAFHO.navy,
                    }}
                  >
                    {`${Math.round(hours)} ч`}
                  </div>
                </div>
              </>
            );
          }

          if (step === "rinse") {
            const peel = T(0.04, 0.26);
            const go = T(0.26, 0.44);
            const ax = interpolate(go, [0, 1], [cx, cardW - sw * 0.32 - 40]);
            const ay = interpolate(go, [0, 1], [cy, sw * 0.0 + shh * 0.3 + 30]);
            const landB = T(0.5, 0.82);
            const swap = T(0.6, 0.72) * (1 - T(0.93, 1));
            return (
              <>
                <Sheet
                  cx={cx - (1 - landB) * cardW * 0.25}
                  cy={cy - (1 - landB) * cardH * 0.15}
                  w={sw}
                  h={shh}
                  ppc={ppc}
                  lift={1 - landB}
                  opacity={T(0.48, 0.56)}
                  label="B"
                  sheen={0.4}
                />
                {/* rinse drops falling on sheet A */}
                {Array.from({ length: 9 }, (_, i) => {
                  const st = 0.42 + i * 0.03;
                  const f = T(st, st + 0.12);
                  const dx = ((i * 37) % 9 - 4) * sw * 0.05;
                  const o = f > 0 && f < 1 ? 1 : 0;
                  return (
                    <div
                      key={i}
                      style={{
                        position: "absolute",
                        left: ax + dx - 0.18 * ppc,
                        top: ay - 3 * ppc + f * 3 * ppc,
                        width: 0.36 * ppc,
                        height: 0.55 * ppc,
                        borderRadius: "50% 50% 50% 50% / 60% 60% 40% 40%",
                        background: "rgba(200,232,240,0.9)",
                        border: "1px solid rgba(255,255,255,0.9)",
                        opacity: o,
                      }}
                    />
                  );
                })}
                <Sheet
                  cx={ax}
                  cy={ay}
                  w={sw}
                  h={shh}
                  ppc={ppc}
                  lift={peel * (1 - go * 0.6)}
                  peel={peel * (1 - go)}
                  scale={1 - go * 0.55}
                  rotate={go * 8}
                  label="A"
                  sheen={0.6}
                />
                <svg width={cardW} height={cardH} style={{ position: "absolute", left: 0, top: 0, opacity: swap }}>
                  <defs>
                    <marker id="rs-a" markerWidth="8" markerHeight="8" refX="5" refY="4" orient="auto-start-reverse">
                      <path d="M0,0 L8,4 L0,8 Z" fill={YAFHO.orange} />
                    </marker>
                  </defs>
                  <path
                    d={`M ${cx + sw * 0.6} ${cy - shh * 0.1} Q ${cardW * 0.82} ${cy - shh * 0.1} ${cardW - sw * 0.32 - 40} ${shh * 0.3 + 30 + shh * 0.3}`}
                    stroke={YAFHO.orange}
                    strokeWidth={7}
                    fill="none"
                    strokeLinecap="round"
                    markerStart="url(#rs-a)"
                    markerEnd="url(#rs-a)"
                  />
                </svg>
              </>
            );
          }

          // idle
          const landP = land ? T(0.18, 0.6) : 0;
          return land ? (
            <Sheet
              cx={cx}
              cy={cy - (1 - landP) * cardH * 0.15}
              w={sw}
              h={shh}
              ppc={ppc}
              lift={1 - landP}
              opacity={T(0.12, 0.24)}
              sheen={0.2 + landP * 0.4}
            />
          ) : null;
        }}
      </SkinCard>
    </AbsoluteFill>
  );
};
