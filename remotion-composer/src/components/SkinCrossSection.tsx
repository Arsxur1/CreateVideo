import { AbsoluteFill, interpolate, interpolateColors, useCurrentFrame, useVideoConfig } from "remotion";
import { YAFHO, ease, useCanvas } from "./yafho/tokens";

export type SkinPhase = "scar" | "sealed" | "healed";

export interface SkinCrossSectionLabels {
  epidermis?: string;
  dermis?: string;
  collagen?: string;
  moisture?: string;
  signal?: string;
}

export interface SkinCrossSectionProps {
  /**
   * scar   — chaotic orange collagen, raised surface, fast signals, moisture escaping.
   * sealed — animates: sheet lowers → moisture film → signals slow → fibres align, surface flattens.
   * healed — end state: ordered fibres, flat surface, calm signals, no sheet.
   */
  phase?: SkinPhase;
  labels?: SkinCrossSectionLabels;
  /** Fade in at the start (turn off when continuing from a previous cross-section cut). */
  introFade?: boolean;
}

const DEFAULT_LABELS: SkinCrossSectionLabels = {
  epidermis: "эпидермис",
  dermis: "дерма",
  collagen: "коллаген",
  moisture: "влага ↑",
  signal: "сигнал ↓",
};

// Geometry in a 1000x1000 viewBox.
const SURFACE_Y = 300;
const EPI = 50;
const BUMP_X0 = 270;
const BUMP_X1 = 730;
const BUMP_H = 70;
const DERMIS_BOTTOM = 880;
const N_FIBRES = 22;
const SKIN_EPI = "#E8B79E";
const SKIN_EPI_SCAR = "#DC9A85";
const SKIN_DERMIS = "#F4DDCF";
const SKIN_FAT = "#F6EBD9";

function mulberry32(seed: number) {
  return () => {
    seed |= 0;
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

type Pt = [number, number];
type Fibre = [Pt, Pt, Pt, Pt];

const rnd = mulberry32(20261006);
const CHAOTIC: Fibre[] = Array.from({ length: N_FIBRES }, () => {
  const cx = 340 + rnd() * 320;
  const cy = 430 + rnd() * 370;
  const a = rnd() * Math.PI;
  const len = 150 + rnd() * 110;
  const dx = Math.cos(a), dy = Math.sin(a);
  const px = -dy, py = dx;
  const k1 = (rnd() - 0.5) * 150;
  const k2 = (rnd() - 0.5) * 150;
  const p0: Pt = [cx - (dx * len) / 2, cy - (dy * len) / 2];
  return [
    p0,
    [p0[0] + (dx * len) / 3 + px * k1, p0[1] + (dy * len) / 3 + py * k1],
    [p0[0] + (dx * 2 * len) / 3 + px * k2, p0[1] + (dy * 2 * len) / 3 + py * k2],
    [cx + (dx * len) / 2, cy + (dy * len) / 2],
  ];
});
const ALIGNED: Fibre[] = Array.from({ length: N_FIBRES }, (_, i) => {
  const row = i % 11;
  const col = Math.floor(i / 11);
  const y = 420 + row * 38;
  const x0 = 290 + col * 215;
  return [
    [x0, y],
    [x0 + 65, y - 9],
    [x0 + 135, y + 9],
    [x0 + 200, y],
  ];
});
const CELLS: Pt[] = [
  [390, 560],
  [600, 500],
  [520, 700],
  [660, 780],
  [420, 810],
];
const FAT = Array.from({ length: 16 }, (_, i) => ({
  x: 40 + i * 62 + (i % 2) * 18,
  y: DERMIS_BOTTOM + 45 + (i % 3) * 22,
  r: 26 + (i % 4) * 4,
}));

function bump(x: number): number {
  if (x <= BUMP_X0 || x >= BUMP_X1) return 0;
  return 0.5 * (1 - Math.cos((2 * Math.PI * (x - BUMP_X0)) / (BUMP_X1 - BUMP_X0)));
}

function surfacePoints(h: number, offset = 0): Pt[] {
  const pts: Pt[] = [];
  for (let i = 0; i <= 100; i++) {
    const x = i * 10;
    pts.push([x, SURFACE_Y - h * bump(x) + offset]);
  }
  return pts;
}

const toPath = (pts: Pt[]) => pts.map((p, i) => `${i ? "L" : "M"}${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(" ");

const Label: React.FC<{
  x: number;
  y: number;
  text: string;
  swatch: string;
  anchor?: "start" | "end";
  opacity?: number;
  leader?: Pt;
}> = ({ x, y, text, swatch, anchor = "end", opacity = 1, leader }) => {
  const fs = 34;
  const w = text.length * fs * 0.64 + 74;
  const left = anchor === "end" ? x - w : x;
  return (
    <g opacity={opacity}>
      {leader && (
        <line
          x1={anchor === "end" ? left : left + w}
          y1={y}
          x2={leader[0]}
          y2={leader[1]}
          stroke={YAFHO.navy}
          strokeWidth={2.5}
        />
      )}
      <rect x={left} y={y - 30} width={w} height={60} rx={30} fill={YAFHO.white} stroke={YAFHO.navy} strokeOpacity={0.15} />
      <circle cx={left + 30} cy={y} r={10} fill={swatch} />
      <text x={left + 50} y={y + 12} fontSize={fs} fontFamily={YAFHO.sans} fontWeight={800} fill={YAFHO.navy}>
        {text}
      </text>
    </g>
  );
};

/**
 * Animated skin cross-section explaining how a silicone sheet works:
 * occlusion → moisture held → fibroblast signalling slows → collagen settles.
 * Lays out in the top ~60% of the canvas so a ThesisTitle fits below.
 */
export const SkinCrossSection: React.FC<SkinCrossSectionProps> = ({
  phase = "scar",
  labels,
  introFade = true,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const { width, height } = useCanvas();
  const L = { ...DEFAULT_LABELS, ...labels };
  const D = durationInFrames;

  // Phase timelines (0..1)
  let plate = 0, film = 0, slow = 0, align = 0;
  if (phase === "sealed") {
    plate = ease(frame, D * 0.02, D * 0.2);
    film = ease(frame, D * 0.18, D * 0.38);
    slow = ease(frame, D * 0.32, D * 0.6);
    align = ease(frame, D * 0.45, D * 0.92);
  } else if (phase === "healed") {
    slow = 1;
    align = 1;
  }

  const h = BUMP_H * (1 - align);
  const top = surfacePoints(h);
  const epiBottom = surfacePoints(h, EPI);
  const crest = SURFACE_Y - h;

  // Sheet rests on the crest of the scar and follows it down as it flattens.
  const plateH = 24;
  const filmGap = 14 * film;
  const plateRestY = crest - plateH - filmGap;
  const plateY = interpolate(plate, [0, 1], [-80, plateRestY]);

  // Fibroblast pulses: integrate frequency so slowing never jumps phase.
  const freqAt = (f: number) => {
    const s = phase === "sealed" ? ease(f, D * 0.32, D * 0.6) : slow;
    return interpolate(s, [0, 1], [1.6, 0.35]);
  };
  let cycles = 0;
  for (let f = 0; f < frame; f++) cycles += freqAt(f) / fps;

  const drift = (i: number, k: number) => Math.sin(frame / fps * 0.9 + i * 1.7 + k) * 5 * (1 - align);
  const fibres = CHAOTIC.map((c, i) =>
    c.map((p, j) => [
      interpolate(align, [0, 1], [p[0], ALIGNED[i][j][0]]) + drift(i, j),
      interpolate(align, [0, 1], [p[1], ALIGNED[i][j][1]]) + drift(i, j + 2) - h * 0.35 * (1 - align),
    ]) as Fibre,
  );

  const epiColor = interpolateColors(align, [0, 1], [SKIN_EPI_SCAR, SKIN_EPI]);
  const evaporation = phase === "scar" ? 1 : phase === "sealed" ? 1 - plate : 0;
  const intro = introFade ? ease(frame, 0, Math.round(0.4 * fps)) : 1;
  const zoom = 1 + 0.03 * (frame / D);

  // Box: top 6%..64% of the canvas, square, centred.
  const boxTop = height * 0.06;
  const boxH = height * 0.58;
  const size = Math.min(width * 0.96, boxH);

  const epiPath = `${toPath(top)} ${toPath([...epiBottom].reverse()).replace("M", "L")} Z`;
  const dermisPath = `${toPath(epiBottom)} L1000,${DERMIS_BOTTOM} L0,${DERMIS_BOTTOM} Z`;

  return (
    <AbsoluteFill style={{ background: YAFHO.offWhite, opacity: intro }}>
      <svg
        viewBox="0 0 1000 1000"
        width={size}
        height={size}
        style={{
          position: "absolute",
          left: (width - size) / 2,
          top: boxTop + (boxH - size) / 2,
          transform: `scale(${zoom})`,
          overflow: "visible",
        }}
      >
        <defs>
          <clipPath id="skin-clip">
            <rect x={0} y={0} width={1000} height={1000} rx={36} />
          </clipPath>
        </defs>
        <g clipPath="url(#skin-clip)">
          <rect x={0} y={0} width={1000} height={1000} fill={YAFHO.beige} />
          {/* hypodermis */}
          <rect x={0} y={DERMIS_BOTTOM} width={1000} height={1000 - DERMIS_BOTTOM} fill={SKIN_FAT} />
          {FAT.map((c, i) => (
            <circle key={i} cx={c.x} cy={c.y} r={c.r} fill="none" stroke="#E4D2B4" strokeWidth={3} />
          ))}
          {/* dermis + scar tissue zone */}
          <path d={dermisPath} fill={SKIN_DERMIS} />
          <ellipse cx={500} cy={620} rx={250} ry={240} fill="#EFC9B8" opacity={1 - align * 0.85} />
          {/* normal (ordered) dermis fibres outside the scar */}
          {Array.from({ length: 11 }, (_, r) => (
            <g key={r} stroke="#DDB9A4" strokeWidth={5} strokeLinecap="round" fill="none">
              <path d={`M30,${420 + r * 38} q60,-9 120,0 t110,0`} />
              <path d={`M740,${420 + r * 38} q60,-9 120,0 t110,0`} />
            </g>
          ))}
          {/* collagen */}
          {fibres.map((f, i) => (
            <path
              key={i}
              d={`M${f[0][0]},${f[0][1]} C${f[1][0]},${f[1][1]} ${f[2][0]},${f[2][1]} ${f[3][0]},${f[3][1]}`}
              stroke={YAFHO.orange}
              strokeWidth={8}
              strokeLinecap="round"
              fill="none"
            />
          ))}
          {/* fibroblasts + signalling pulses */}
          {CELLS.map(([cx, cy], i) => {
            const ph = (cycles + i * 0.37) % 1;
            return (
              <g key={i}>
                <circle cx={cx} cy={cy} r={18 + ph * 62} fill="none" stroke={YAFHO.navy} strokeWidth={3} opacity={(1 - ph) * 0.55} />
                <ellipse cx={cx} cy={cy} rx={20} ry={12} fill={YAFHO.navy} />
                <circle cx={cx + 3} cy={cy} r={5} fill={YAFHO.offWhite} />
              </g>
            );
          })}
          {/* epidermis */}
          <path d={epiPath} fill={epiColor} />
          {/* moisture held in the upper skin */}
          {Array.from({ length: 9 }, (_, i) => (
            <circle
              key={i}
              cx={300 + i * 50}
              cy={SURFACE_Y - h * bump(300 + i * 50) + 16 + (i % 3) * 9}
              r={7}
              fill={YAFHO.teal}
              opacity={film * (i % 2 ? 0.9 : 0.6)}
            />
          ))}
          {/* moisture escaping without a sheet */}
          {Array.from({ length: 7 }, (_, i) => {
            const x = 300 + i * 68;
            const t = ((frame / fps) * 0.55 + i * 0.23) % 1;
            const y0 = SURFACE_Y - h * bump(x) - 12;
            return (
              <circle key={i} cx={x + Math.sin(t * 6 + i) * 8} cy={y0 - t * 170} r={8 - t * 3} fill={YAFHO.teal} opacity={(1 - t) * 0.75 * evaporation} />
            );
          })}
          {/* moisture film under the sheet */}
          {film > 0 && (
            <path
              d={`M240,${plateY + plateH} L760,${plateY + plateH} ${toPath(top.slice(24, 77).reverse()).replace("M", "L")} Z`}
              fill={YAFHO.teal}
              opacity={0.35 * film}
            />
          )}
          {/* silicone sheet */}
          {plate > 0 && (
            <rect x={230} y={plateY} width={540} height={plateH} rx={10} fill="#E3F1F0" stroke={YAFHO.navy} strokeOpacity={0.45} strokeWidth={3} />
          )}
        </g>

        {/* labels */}
        <Label x={36} y={SURFACE_Y + 25} text={L.epidermis!} swatch={SKIN_EPI_SCAR} anchor="start" />
        <Label x={36} y={640} text={L.dermis!} swatch={SKIN_DERMIS} anchor="start" />
        <Label x={964} y={360 + 30} text={L.collagen!} swatch={YAFHO.orange} leader={[fibres[3][3][0], fibres[3][3][1]]} />
        {phase !== "scar" && (
          <>
            <Label x={964} y={150} text={L.moisture!} swatch={YAFHO.teal} opacity={film} />
            <Label x={964} y={960} text={L.signal!} swatch={YAFHO.navy} opacity={slow} />
          </>
        )}
      </svg>
    </AbsoluteFill>
  );
};
