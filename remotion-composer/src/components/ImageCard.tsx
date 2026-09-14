import React from "react";
import { Img, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { resolveAsset } from "../lib/resolveAsset";

/**
 * Picture-in-picture still over talking-head footage (branded-reel). Renders inside the
 * overlay's Sequence + position box: frame 0 here is the pop-in's first frame. Spring in,
 * fade out over the last 0.2 s, framed and shadowed. Never full-frame — montage.md Rule 1.
 */
export interface ImageCardProps {
  src: string;
  holdSeconds: number;
  widthPercent?: number;               // of the 1080 canvas; 10–70, default 42
  anchor?: "left" | "right" | "center";
  borderColor?: string;
  canvasWidth?: number;
}

const POP_SPRING = { damping: 14, mass: 0.5, stiffness: 120 };

export const ImageCard: React.FC<ImageCardProps> = ({
  src, holdSeconds, widthPercent = 42, anchor = "right", borderColor, canvasWidth,
}) => {
  const frame = useCurrentFrame();
  const { fps, width: videoWidth } = useVideoConfig();
  const enter = spring({ frame, fps, config: POP_SPRING });
  const total = Math.round(holdSeconds * fps);
  const exit = interpolate(frame, [total - Math.round(0.2 * fps), total], [1, 0], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });
  // canvasWidth is an override for a non-standard composition; the composition's own
  // width (from useVideoConfig) is the correct default — 1080 was only ever right by
  // coincidence for the 1080x1920 talking-head composition.
  const effectiveCanvasWidth = canvasWidth ?? videoWidth;
  const clampedWidthPercent = Math.min(70, Math.max(10, widthPercent));
  const width = (clampedWidthPercent / 100) * effectiveCanvasWidth;
  const scale = 0.86 + enter * 0.14;
  const horizontal: React.CSSProperties =
    anchor === "left" ? { left: 0, transform: `scale(${scale})`, transformOrigin: "left top" }
    : anchor === "center" ? { left: "50%", transform: `translateX(-50%) scale(${scale})`, transformOrigin: "center top" }
    : { right: 0, transform: `scale(${scale})`, transformOrigin: "right top" };
  return (
    <div style={{
      position: "absolute", top: 0, width, opacity: exit,
      borderRadius: 24, overflow: "hidden", boxShadow: "0 24px 64px rgba(0,0,0,0.45)",
      border: borderColor ? `4px solid ${borderColor}` : undefined, ...horizontal,
    }}>
      <Img src={resolveAsset(src)} style={{ width: "100%", display: "block" }} />
    </div>
  );
};
