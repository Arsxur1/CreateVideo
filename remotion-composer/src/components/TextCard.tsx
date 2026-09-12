import { AbsoluteFill, spring, useCurrentFrame, useVideoConfig, interpolate } from "remotion";

interface TextCardProps {
  text: string;
  fontSize?: number;
  color?: string;
  backgroundColor?: string;
  fontFamily?: string;
}

export const TextCard: React.FC<TextCardProps> = ({
  text,
  fontSize = 56,
  color = "#FFFFFF",
  backgroundColor = "#1F2937",
  fontFamily = "Baloo2, system-ui, sans-serif",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const words = text.split(/\s+/).filter(Boolean);
  const wordsPerLine = 3;

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        background: backgroundColor,
        padding: "6% 8%",
      }}
    >
      <div
        style={{
          fontSize,
          color,
          fontFamily,
          fontWeight: 700,
          textAlign: "center",
          maxWidth: "82%",
          lineHeight: 1.45,
        }}
      >
        {words.map((w, i) => {
          const delay = i * 5;
          const entrance = spring({
            frame: frame - delay,
            fps,
            config: { damping: 18, stiffness: 140, mass: 0.8 },
            from: 0,
            to: 1,
          });
          const lineBreak = (i + 1) % wordsPerLine === 0 ? <br /> : " ";
          return (
            <span key={i}>
              <span
                style={{
                  display: "inline-block",
                  whiteSpace: "nowrap",
                  opacity: entrance,
                  transform: `translateY(${interpolate(entrance, [0, 1], [16, 0])}px) scale(${interpolate(entrance, [0, 1], [0.92, 1])})`,
                }}
              >
                {w}
              </span>
              {lineBreak}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
