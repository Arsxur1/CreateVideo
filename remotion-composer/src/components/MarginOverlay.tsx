import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { YAFHO, coverMap, ease, useCanvas, useFadeSlide } from "./yafho/tokens";

export interface MarginOverlayProps {
  /** Scar bounding box in 1080x1920 source-video pixels. */
  scarBox?: { x: number; y: number; w: number; h: number };
  /** Sheet margin around the scar, in source pixels (≈ 1 cm in the shot). */
  marginPx?: number;
  label?: string;
}

/**
 * Orange "+1 cm" outline drawn over the application shot (H06): the dashed
 * scar box, the sheet outline around it and margin markers on each side.
 * Coordinates follow the video's objectFit: cover so 9:16, 4:5 and the split
 * 16:9 panel all stay registered to the footage.
 */
export const MarginOverlay: React.FC<MarginOverlayProps> = ({
  scarBox = { x: 470, y: 640, w: 140, h: 600 },
  marginPx = 80,
  label = "+1 см",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const canvas = useCanvas();
  const m = coverMap(canvas);
  const { opacity } = useFadeSlide(frame);

  const sx = m.x(scarBox.x), sy = m.y(scarBox.y);
  const sw = scarBox.w * m.scale, sh = scarBox.h * m.scale;
  const g = marginPx * m.scale;
  const ox = sx - g, oy = sy - g, ow = sw + 2 * g, oh = sh + 2 * g;
  const perim = 2 * (ow + oh);
  const draw = ease(frame, Math.round(0.2 * fps), Math.round(1.4 * fps));
  const tags = ease(frame, Math.round(1.2 * fps), Math.round(1.6 * fps));

  const Tag: React.FC<{ x: number; y: number }> = ({ x, y }) => (
    <g opacity={tags}>
      <rect x={x - 82} y={y - 34} width={164} height={68} rx={34} fill={YAFHO.white} />
      <text x={x} y={y + 13} textAnchor="middle" fontFamily={YAFHO.sans} fontWeight={800} fontSize={38} fill={YAFHO.navy}>
        {label}
      </text>
    </g>
  );

  return (
    <AbsoluteFill style={{ opacity, pointerEvents: "none" }}>
      <svg width={canvas.width} height={canvas.height}>
        <rect x={sx} y={sy} width={sw} height={sh} rx={10} fill="none" stroke={YAFHO.white} strokeWidth={4} strokeDasharray="14 12" />
        <rect
          x={ox}
          y={oy}
          width={ow}
          height={oh}
          rx={22}
          fill="none"
          stroke={YAFHO.orange}
          strokeWidth={8}
          strokeDasharray={perim}
          strokeDashoffset={perim * (1 - draw)}
        />
        {/* margin ticks: left, right, top */}
        <g stroke={YAFHO.orange} strokeWidth={6} strokeLinecap="round" opacity={tags}>
          <line x1={ox} y1={sy + sh / 2} x2={sx} y2={sy + sh / 2} />
          <line x1={sx + sw} y1={sy + sh / 2} x2={ox + ow} y2={sy + sh / 2} />
          <line x1={sx + sw / 2} y1={oy} x2={sx + sw / 2} y2={sy} />
        </g>
        <Tag x={ox - 100} y={sy + sh / 2} />
        <Tag x={ox + ow + 100} y={sy + sh / 2} />
      </svg>
    </AbsoluteFill>
  );
};
