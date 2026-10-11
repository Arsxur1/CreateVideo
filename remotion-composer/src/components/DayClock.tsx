import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { YAFHO, ease, useCanvas } from "./yafho/tokens";

export interface DayClockItem {
  /** Hour of day (may run past 24 for a span that crosses midnight, e.g. 21.5 → 31). */
  from: number;
  to?: number;
  label: string;
  /** wear: sheet A on the skin · wearB: sheet B · event: a moment (apply, rinse) */
  kind?: "wear" | "wearB" | "event";
}

export interface DayClockProps {
  items?: DayClockItem[];
  /** Where the hand starts (hour). */
  start?: number;
  /** Centre text once the day is done (default: the wear hours summed from `items`). */
  summary?: string;
  summaryNote?: string;
}

const DEFAULT_ITEMS: DayClockItem[] = [
  { from: 7, label: "наклеить", kind: "event" },
  { from: 7, to: 21, label: "день — под одеждой", kind: "wear" },
  { from: 21, label: "промыть, сменить", kind: "event" },
  { from: 22, to: 31, label: "ночь — вторая пластина", kind: "wearB" },
];  // 14 h + 9 h = 23 h — the top of the passport's 12–23 h a day

const fmtH = (h: number) => {
  // round to whole minutes first so 7.995 h reads 08:00, not 07:00
  const total = ((Math.round(h * 60) % 1440) + 1440) % 1440;
  const hh = Math.floor(total / 60);
  const mm = total % 60;
  return `${String(hh).padStart(2, "0")}:${String(mm).padStart(2, "0")}`;
};

const isSpan = (it: DayClockItem) => it.kind !== "event" && it.to !== undefined;

/**
 * Series 2 «День с пластиной»: 24 h dial. The hand runs one full day from
 * `start`; wear arcs fill as it passes (A teal, B lighter teal), orange dots
 * mark apply / rinse. Rows below name each part; the centre ends on the total.
 */
export const DayClock: React.FC<DayClockProps> = ({
  items = DEFAULT_ITEMS,
  start = 7,
  summary,
  summaryNote = "на коже в сутки",
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const { width, height } = useCanvas();
  const t = frame / Math.max(1, durationInFrames - 1);
  const fs = Math.round(width * 0.04);
  const intro = ease(frame, 0, 0.4 * fps);
  const run = ease(t, 0.06, 0.8);
  const now = start + 24 * run;
  const done = ease(t, 0.8, 0.88);
  const worn = items.filter(isSpan).reduce((acc, it) => acc + (it.to! - it.from), 0);
  const total = summary ?? `${Number.isInteger(worn) ? worn : worn.toFixed(1).replace(".", ",")} ч`;

  const D = Math.min(width * 0.7, height * 0.4);
  const R = D / 2 - 30;
  const cx = D / 2;
  const cy = D / 2;
  // text inside the dial scales with the dial (small on a square Telegram frame); 9:16 unchanged
  const df = Math.min(fs, D * 0.057);
  const ang = (h: number) => (h / 24) * 2 * Math.PI - Math.PI / 2;
  const pt = (h: number, r = R) => [cx + r * Math.cos(ang(h)), cy + r * Math.sin(ang(h))];
  const arc = (a: number, b: number, r = R) => {
    if (b - a < 0.01) return "";
    const [x0, y0] = pt(a, r);
    const [x1, y1] = pt(b, r);
    return `M ${x0} ${y0} A ${r} ${r} 0 ${b - a > 12 ? 1 : 0} 1 ${x1} ${y1}`;
  };
  // hours since start, so spans before `start` are read as the next day
  const rel = (h: number) => (h < start ? h + 24 : h);

  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: height * 0.05, opacity: intro }}>
      <div style={{ position: "relative", width: D, height: D }}>
        <svg width={D} height={D}>
          <circle cx={cx} cy={cy} r={D / 2} fill={YAFHO.white} />
          <circle cx={cx} cy={cy} r={R} fill="none" stroke={YAFHO.navy} strokeOpacity={0.08} strokeWidth={26} />
          {Array.from({ length: 24 }, (_, i) => {
            const [x0, y0] = pt(i, R - (i % 6 === 0 ? 46 : 36));
            const [x1, y1] = pt(i, R - 24);
            return <line key={i} x1={x0} y1={y0} x2={x1} y2={y1} stroke={YAFHO.navy} strokeOpacity={i % 6 === 0 ? 0.7 : 0.25} strokeWidth={i % 6 === 0 ? 4 : 2} />;
          })}
          {[0, 6, 12, 18].map((h) => {
            const [x, y] = pt(h, R - 74);
            return (
              <text key={h} x={x} y={y + df * 0.32} textAnchor="middle" fontFamily={YAFHO.mono} fontWeight={700} fontSize={df * 0.8} fill={YAFHO.navy} fillOpacity={0.6}>
                {h}
              </text>
            );
          })}
          {items
            .filter(isSpan)
            .map((it) => {
              const a = rel(it.from);
              const b = Math.min(rel(it.from) + (it.to! - it.from), now);
              return (
                <path
                  key={it.label}
                  d={arc(a, b)}
                  stroke={YAFHO.teal}
                  strokeOpacity={it.kind === "wearB" ? 0.55 : 1}
                  strokeWidth={26}
                  fill="none"
                  strokeLinecap="round"
                />
              );
            })}
          {items
            .filter((it) => it.kind === "event")
            .map((it) => {
              const passed = now >= rel(it.from) - 0.01;
              const [x, y] = pt(it.from);
              return <circle key={it.label} cx={x} cy={y} r={passed ? 20 : 0} fill={YAFHO.orange} stroke={YAFHO.white} strokeWidth={6} />;
            })}
          {/* hand */}
          {(() => {
            const [x, y] = pt(now, R - 40);
            return (
              <>
                <line x1={cx} y1={cy} x2={x} y2={y} stroke={YAFHO.navy} strokeWidth={8} strokeLinecap="round" opacity={1 - done} />
                <circle cx={cx} cy={cy} r={12} fill={YAFHO.navy} opacity={1 - done} />
              </>
            );
          })()}
        </svg>
        <div
          style={{
            position: "absolute",
            inset: 0,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            fontFamily: YAFHO.mono,
            fontWeight: 700,
            color: YAFHO.navy,
          }}
        >
          <div style={{ fontSize: df * 1.6, opacity: 1 - done, marginTop: D * 0.36, background: "rgba(255,255,255,0.9)", borderRadius: 12, padding: "0 10px" }}>{fmtH(now)}</div>
          <div style={{ position: "absolute", textAlign: "center", opacity: done }}>
            <div style={{ fontFamily: YAFHO.sans, fontWeight: 800, fontSize: df * 2.4, lineHeight: 1 }}>{total}</div>
            <div style={{ fontFamily: YAFHO.sans, fontWeight: 500, fontSize: df * 0.9, color: YAFHO.muted, marginTop: df * 0.3 }}>{summaryNote}</div>
          </div>
        </div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: fs * 0.5, marginTop: fs * 1.1, width: width * 0.86 }}>
        {items.map((it) => {
          const p = ease(now, rel(it.from), rel(it.from) + 0.9);
          const wear = isSpan(it);
          return (
            <div
              key={it.label}
              style={{
                display: "flex",
                alignItems: "center",
                gap: fs * 0.6,
                opacity: p,
                transform: `translateX(${(1 - p) * 30}px)`,
              }}
            >
              <span
                style={{
                  fontFamily: YAFHO.mono,
                  fontWeight: 700,
                  fontSize: fs * 1.05,
                  color: YAFHO.white,
                  // white text needs the text-safe shades (≥ 4.5:1)
                  background: wear ? YAFHO.tealText : YAFHO.orangeText,
                  borderRadius: 999,
                  padding: `${fs * 0.15}px ${fs * 0.55}px`,
                  minWidth: fs * 4.6,
                  textAlign: "center",
                  flex: "none",
                }}
              >
                {wear ? `${fmtH(it.from)}–${fmtH(it.to!)}`.replace(/:00/g, "") : fmtH(it.from)}
              </span>
              <span style={{ fontFamily: YAFHO.sans, fontWeight: 800, fontSize: fs * 1.25, color: YAFHO.navy }}>{it.label}</span>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
