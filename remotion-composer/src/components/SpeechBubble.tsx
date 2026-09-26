import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/google-fonts/Gaegu";

const { fontFamily } = loadFont("normal", { weights: ["700"], subsets: ["latin"] });

export type BubbleVariant = "speech" | "thought";
export type TailSide = "bottom-left" | "bottom-right" | "none";

interface SpeechBubbleProps {
  text: string;
  /** Anchor position of the bubble centre, as % of the frame. */
  x?: number;
  y?: number;
  variant?: BubbleVariant;
  tail?: TailSide;
  fontSize?: number;
  maxWidth?: number;
  fill?: string;
  ink?: string;
}

/**
 * Hand-lettered comic bubble that pops in with an overshooting spring,
 * wobbles gently while held, and shrinks away in the last few frames.
 */
export const SpeechBubble: React.FC<SpeechBubbleProps> = ({
  text,
  x = 50,
  y = 25,
  variant = "speech",
  tail = "bottom-left",
  fontSize = 64,
  maxWidth = 900,
  fill = "#FFFDF6",
  ink = "#2B2118",
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const pop = spring({ frame, fps, config: { damping: 9, stiffness: 180, mass: 0.7 } });
  const exit = interpolate(frame, [durationInFrames - 6, durationInFrames], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const wobble = Math.sin(frame / 7) * 1.5;
  const scale = pop * exit;
  const tailLeft = tail === "bottom-left";
  const radius = variant === "thought" ? "48% 52% 46% 54% / 55% 48% 52% 45%" : 44;

  return (
    <div
      style={{
        position: "absolute",
        left: `${x}%`,
        top: `${y}%`,
        transform: `translate(-50%, -50%) scale(${scale}) rotate(${wobble}deg)`,
        transformOrigin: tailLeft ? "20% 100%" : "80% 100%",
      }}
    >
      <div
        style={{
          position: "relative",
          maxWidth,
          padding: variant === "thought" ? "34px 56px" : "22px 40px",
          background: fill,
          border: `6px solid ${ink}`,
          borderRadius: radius,
          boxShadow: "0 10px 30px rgba(0,0,0,0.25)",
          fontFamily,
          fontWeight: 700,
          fontSize,
          lineHeight: 1.05,
          color: ink,
          textAlign: "center",
          whiteSpace: "pre-wrap",
        }}
      >
        {text}
        {tail === "none" ? null : variant === "speech" ? (
          <div
            style={{
              position: "absolute",
              bottom: -34,
              [tailLeft ? "left" : "right"]: 48,
              width: 0,
              height: 0,
              borderLeft: "22px solid transparent",
              borderRight: "22px solid transparent",
              borderTop: `36px solid ${ink}`,
              transform: `skewX(${tailLeft ? 25 : -25}deg)`,
            }}
          />
        ) : (
          [0, 1].map((i) => (
            <div
              key={i}
              style={{
                position: "absolute",
                bottom: -30 - i * 34,
                [tailLeft ? "left" : "right"]: 40 - i * 26,
                width: 30 - i * 12,
                height: 30 - i * 12,
                borderRadius: "50%",
                background: fill,
                border: `5px solid ${ink}`,
              }}
            />
          ))
        )}
      </div>
    </div>
  );
};
