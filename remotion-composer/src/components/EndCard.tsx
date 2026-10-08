import { AbsoluteFill, Img, useCurrentFrame, useVideoConfig } from "remotion";
import { YAFHO, ease, useCanvas } from "./yafho/tokens";

export interface EndCardProps {
  /** Resolved logo URL; when absent the wordmark is set in Onest. */
  logoSrc?: string;
  brand?: string;
  tagline?: string;
  handle?: string;
  /** QR module matrix (rows of 0/1), quiet zone excluded. */
  qr?: number[][];
  qrCaption?: string;
  /** Call to action above the handle. */
  cta?: string;
}

/**
 * Navy end card: logo or wordmark, @handle and an Instagram QR.
 * Elements fade/slide in one after another (0.4s each), no bounce.
 */
export const EndCard: React.FC<EndCardProps> = ({
  logoSrc,
  brand = "Yafho-Silicare",
  tagline,
  handle = "@sil.icare",
  qr,
  qrCaption = "instagram.com/sil.icare",
  cta,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { height } = useCanvas();
  const t = Math.round(0.4 * fps);
  const step = (i: number) => {
    const p = ease(frame, i * 0.25 * fps, i * 0.25 * fps + t);
    return { opacity: p, transform: `translateY(${(1 - p) * 24}px)` };
  };

  const compact = height < 1500;
  const qrSize = compact ? 300 : 360;
  // "Yafho-Silicare" / "Yafho SiliSkin": first part bold, separator kept
  const m = brand.match(/^(\S+?)([- ])(.+)$/);
  const first = m ? m[1] : brand;
  const rest = m ? `${m[2]}${m[3]}` : "";

  return (
    <AbsoluteFill
      style={{
        background: YAFHO.navy,
        alignItems: "center",
        justifyContent: "center",
        gap: compact ? 40 : 64,
        fontFamily: YAFHO.sans,
        color: YAFHO.white,
        textAlign: "center",
      }}
    >
      <div style={step(0)}>
        {logoSrc ? (
          <Img src={logoSrc} style={{ height: compact ? 120 : 150, objectFit: "contain" }} />
        ) : (
          <div style={{ fontSize: 104, lineHeight: 1, letterSpacing: "-0.02em" }}>
            <span style={{ fontWeight: 800 }}>{first}</span>
            {rest && <span style={{ fontWeight: 500 }}>{rest}</span>}
          </div>
        )}
        <div style={{ width: 120, height: 8, borderRadius: 4, background: YAFHO.orange, margin: "36px auto 0" }} />
        {tagline && <div style={{ fontWeight: 500, fontSize: 40, marginTop: 28, color: "#D7DEE8" }}>{tagline}</div>}
      </div>

      {qr && qr.length > 0 && (
        <div style={{ ...step(1), display: "flex", flexDirection: "column", alignItems: "center", gap: 20 }}>
          <div style={{ background: YAFHO.white, borderRadius: 28, padding: 28 }}>
            <svg width={qrSize} height={qrSize} viewBox={`0 0 ${qr.length} ${qr.length}`} shapeRendering="crispEdges">
              {qr.flatMap((row, y) =>
                row.map((v, x) => (v ? <rect key={`${x}-${y}`} x={x} y={y} width={1} height={1} fill={YAFHO.navy} /> : null)),
              )}
            </svg>
          </div>
          <div style={{ fontFamily: YAFHO.mono, fontWeight: 600, fontSize: 30, color: "#D7DEE8" }}>{qrCaption}</div>
        </div>
      )}

      {cta && (
        <div style={{ ...step(2), fontWeight: 800, fontSize: compact ? 60 : 72, lineHeight: 1.12, whiteSpace: "pre-line", maxWidth: "88%" }}>
          {cta}
        </div>
      )}
      <div style={{ ...step(cta ? 3 : 2), fontWeight: 800, fontSize: cta ? 64 : 88, letterSpacing: "-0.01em", color: cta ? "#D7DEE8" : YAFHO.white }}>
        {handle}
      </div>
    </AbsoluteFill>
  );
};
