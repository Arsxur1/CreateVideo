import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { YAFHO, ease, useCanvas } from "./yafho/tokens";

export type SizeZone = "face" | "arm" | "abdomen" | "burn";

export interface SizeGuideItem {
  /** Sheet size in cm, e.g. [4, 13]. */
  cm: [number, number];
  zone: SizeZone;
  label: string;
}

export interface SizeGuideProps {
  items?: SizeGuideItem[];
}

const DEFAULT_ITEMS: SizeGuideItem[] = [
  { cm: [4, 4], zone: "face", label: "лицо, мелкий" },
  { cm: [4, 13], zone: "arm", label: "рука" },
  { cm: [5, 15], zone: "abdomen", label: "живот" },
  { cm: [10, 15], zone: "burn", label: "ожог" },
];

const SKIN = "#E2C4B0";
const UNIT = 12; // svg units per cm (cell viewBox 300x300)

// Silhouette + where the sheet lands (centre, rotation) per zone.
const ZONES: Record<SizeZone, { d: string; at: [number, number]; rot: number }> = {
  face: {
    d: "M150,40 C215,40 240,95 236,150 C232,210 195,250 150,250 C105,250 68,210 64,150 C60,95 85,40 150,40 Z M118,245 L182,245 L190,300 L110,300 Z",
    at: [195, 170],
    rot: 0,
  },
  arm: {
    d: "M20,230 L210,90 C230,75 262,80 274,100 C286,120 280,146 260,158 L62,288 C44,300 20,296 10,278 C0,262 4,242 20,230 Z",
    at: [140, 190],
    rot: -36,
  },
  abdomen: {
    d: "M70,20 L230,20 C240,90 262,150 262,215 C262,262 240,300 240,300 L60,300 C60,300 38,262 38,215 C38,150 60,90 70,20 Z",
    at: [150, 235],
    rot: 90,
  },
  burn: {
    d: "M20,120 C40,70 90,52 120,48 L180,48 C210,52 260,70 280,120 L292,300 L8,300 Z",
    at: [150, 185],
    rot: 0,
  },
};

/**
 * Size picker (topic 06): four sheets drop onto zone silhouettes, staggered,
 * each with its size in mono and the zone in Onest.
 */
export const SizeGuide: React.FC<SizeGuideProps> = ({ items = DEFAULT_ITEMS }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { width, height } = useCanvas();

  const gridTop = height * 0.07;
  const gridH = height * 0.6;
  const cols = 2;
  const rows = Math.ceil(items.length / cols);
  const gap = 28;
  const cellW = (width * 0.9 - gap) / cols;
  const cellH = (gridH - gap * (rows - 1)) / rows;

  return (
    <AbsoluteFill>
      {items.map((it, i) => {
        const col = i % cols;
        const row = Math.floor(i / cols);
        const appear = ease(frame, i * 0.25 * fps, i * 0.25 * fps + 0.4 * fps);
        const drop = ease(frame, (0.5 + i * 0.5) * fps, (0.9 + i * 0.5) * fps);
        const z = ZONES[it.zone];
        const [w, h] = it.cm;
        const svgSize = Math.min(cellW, cellH - 130);
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: width * 0.05 + col * (cellW + gap),
              top: gridTop + row * (cellH + gap),
              width: cellW,
              height: cellH,
              background: YAFHO.white,
              borderRadius: 32,
              opacity: appear,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "space-between",
              padding: "18px 0 22px",
              boxSizing: "border-box",
            }}
          >
            <svg viewBox="0 0 300 300" width={svgSize} height={svgSize}>
              <path d={z.d} fill={SKIN} />
              <g
                transform={`translate(${z.at[0]}, ${interpolate(drop, [0, 1], [z.at[1] - 160, z.at[1]])}) rotate(${z.rot})`}
                opacity={drop}
              >
                <rect
                  x={(-w * UNIT) / 2}
                  y={(-h * UNIT) / 2}
                  width={w * UNIT}
                  height={h * UNIT}
                  rx={8}
                  fill="#EAF5F4"
                  fillOpacity={0.85}
                  stroke={YAFHO.teal}
                  strokeWidth={4}
                />
              </g>
            </svg>
            <div style={{ textAlign: "center", opacity: drop }}>
              <div style={{ fontFamily: YAFHO.mono, fontWeight: 700, fontSize: 52, color: YAFHO.navy }}>
                {`${w}×${h} см`}
              </div>
              <div style={{ fontFamily: YAFHO.sans, fontWeight: 500, fontSize: 36, color: YAFHO.muted }}>{it.label}</div>
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
