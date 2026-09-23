import React from "react";
import {
  AbsoluteFill,
  Audio,
  CalculateMetadataFunction,
  Easing,
  Img,
  interpolate,
  OffthreadVideo,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { loadThemeFont } from "./fonts";

// Review-reel template: a data-driven vertical reel. The look comes from the
// channel theme (props.theme), the edit comes from props.shots. Built by
// `python -m lib.review_kit`. See skills/creative/review-kit.md.

const FPS = 30;
const f = (seconds: number) => Math.round(seconds * FPS);

// ------------------------------------------------------------------ props

export type Theme = {
  palette: { background: string; text: string; muted: string; accent: string };
  fonts: { display: string; text: string };
  captions: {
    size: number;
    weight: number;
    top: number;
    left: number;
    right: number;
    scrim: boolean;
  };
  tags: { size: number };
  motion: { spring_damping: number; whip_frames: number; vignette: boolean };
  signature: {
    open: "aperture" | "fade" | "cut";
    close: "aperture" | "fade" | "cut";
  };
  intro: { cover_seconds: number };
};

type Media = {
  type: "video" | "still";
  src: string;
  at?: number; // source seconds (video)
  zoom?: [number, number];
  origin?: string;
  rate?: number;
  filter?: string;
  drift?: [number, number]; // px on x (still)
};

type Overlay =
  | {
      type: "tag";
      text: string;
      top?: number;
      at?: number;
      color?: "text" | "accent";
    }
  | { type: "bigword"; text: string; top?: number; size?: number; at?: number }
  | { type: "price"; text: string; top?: number; at?: number }
  | { type: "coverage"; box: [number, number, number, number]; at?: number }
  | {
      type: "controls";
      top?: number;
      rows: {
        step: string;
        label: string;
        icon: "moon" | "lamp" | "dim" | "dot";
        at: number;
        accent?: boolean;
      }[];
    }
  | {
      type: "ring";
      cx: number;
      cy: number;
      rx: number;
      ry: number;
      label: string;
      labelY: number;
      turn?: boolean;
      dark?: boolean;
      at?: number;
    }
  | {
      type: "verdict";
      line1: string;
      line2: string;
      icon: "check" | "pause";
      accent?: boolean;
      at?: number;
    }
  | { type: "checklist"; title: string; items: { text: string; at: number }[] }
  | { type: "scrim"; strength?: number };

export type Shot = {
  id: string;
  from: number;
  to: number;
  media: Media;
  enter?: "cut" | "whip" | "aperture";
  aperture?: { cx: number; cy: number };
  exit?: "cut" | "aperture" | "fade";
  overlays?: Overlay[];
};

type Caption = { text: string; start: number; end: number };
type Segment = { id: string; start: number; end: number };

export interface ReelProps {
  durationSeconds: number;
  theme: Theme;
  narration: string;
  music: string | null;
  musicVolume: number;
  musicDuckedVolume: number;
  timeline: Segment[];
  captions: Caption[];
  shots: Shot[];
  sfx: { name: string; at: number; volume: number }[];
  cover: { kicker: string; title: string; subtitle: string; image: string };
}

const ThemeContext = React.createContext<{
  theme: Theme;
  display: string;
  text: string;
} | null>(null);
const useTheme = () => {
  const ctx = React.useContext(ThemeContext);
  if (!ctx) throw new Error("ThemeContext missing");
  return ctx;
};

// ------------------------------------------------------------------ media

const Footage: React.FC<{ media: Media; frames: number }> = ({
  media,
  frames,
}) => {
  const frame = useCurrentFrame();
  const { theme } = useTheme();
  const zoom = media.zoom ?? [1, 1.06];
  const scale = interpolate(frame, [0, frames], zoom, {
    extrapolateRight: "clamp",
  });
  return (
    <AbsoluteFill
      style={{ overflow: "hidden", background: theme.palette.background }}
    >
      <OffthreadVideo
        src={staticFile(media.src)}
        trimBefore={Math.round((media.at ?? 0) * FPS)}
        playbackRate={media.rate ?? 1}
        muted
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${scale})`,
          transformOrigin: media.origin ?? "50% 50%",
          filter: media.filter,
        }}
      />
    </AbsoluteFill>
  );
};

const Still: React.FC<{ media: Media; frames: number }> = ({
  media,
  frames,
}) => {
  const frame = useCurrentFrame();
  const { theme } = useTheme();
  const zoom = media.zoom ?? [1, 1.08];
  const drift = media.drift ?? [0, 0];
  const t = interpolate(frame, [0, frames], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.sin),
  });
  const scale = zoom[0] + (zoom[1] - zoom[0]) * t;
  const x = drift[0] + (drift[1] - drift[0]) * t;
  return (
    <AbsoluteFill
      style={{ overflow: "hidden", background: theme.palette.background }}
    >
      <Img
        src={staticFile(media.src)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `translateX(${x}px) scale(${scale})`,
          transformOrigin: media.origin ?? "50% 50%",
          filter: media.filter,
        }}
      />
    </AbsoluteFill>
  );
};

const MediaLayer: React.FC<{ media: Media; frames: number }> = ({
  media,
  frames,
}) =>
  media.type === "video" ? (
    <Footage media={media} frames={frames} />
  ) : (
    <Still media={media} frames={frames} />
  );

const WhipIn: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();
  const { theme } = useTheme();
  const n = Math.max(1, theme.motion.whip_frames);
  const y = interpolate(frame, [0, n], [-160, 0], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const blur = interpolate(frame, [0, n], [18, 0], {
    extrapolateRight: "clamp",
  });
  return (
    <AbsoluteFill
      style={{ transform: `translateY(${y}px)`, filter: `blur(${blur}px)` }}
    >
      {children}
    </AbsoluteFill>
  );
};

// The light aperture: a circle of light that opens into a shot or closes it.
const Aperture: React.FC<{
  cx: number;
  cy: number;
  frames: number;
  mode: "open" | "close";
  children: React.ReactNode;
}> = ({ cx, cy, frames, mode, children }) => {
  const frame = useCurrentFrame();
  const { theme } = useTheme();
  const t = interpolate(frame, [0, frames], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });
  const r = mode === "open" ? 2400 * t : 2400 * (1 - t);
  const bloom =
    mode === "open"
      ? interpolate(frame, [0, frames * 0.5, frames * 1.4], [0, 0.55, 0], {
          extrapolateRight: "clamp",
        })
      : 0;
  return (
    <AbsoluteFill style={{ background: theme.palette.background }}>
      <AbsoluteFill style={{ clipPath: `circle(${r}px at ${cx}px ${cy}px)` }}>
        {children}
      </AbsoluteFill>
      <AbsoluteFill
        style={{
          background: `radial-gradient(circle at ${cx}px ${cy}px, rgba(255,250,235,${bloom}) 0%, rgba(255,250,235,0) 60%)`,
        }}
      />
    </AbsoluteFill>
  );
};

const FadeTail: React.FC<{
  frames: number;
  tail: number;
  toBlack?: boolean;
  children: React.ReactNode;
}> = ({ frames, tail, children }) => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [frames - tail - 4, frames - 4], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return <AbsoluteFill style={{ opacity: o }}>{children}</AbsoluteFill>;
};

const Vignette: React.FC = () => (
  <AbsoluteFill
    style={{
      background:
        "radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.45) 100%)",
    }}
  />
);

const hexToRgb = (hex: string) => {
  const n = parseInt(hex.slice(1), 16);
  return `${(n >> 16) & 255},${(n >> 8) & 255},${n & 255}`;
};

const TopScrim: React.FC<{ strength?: number }> = ({ strength = 0.78 }) => {
  const { theme } = useTheme();
  const bg = hexToRgb(theme.palette.background);
  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(180deg, rgba(${bg},${strength}) 0%, rgba(${bg},${strength * 0.85}) 45%, rgba(${bg},0) 70%)`,
      }}
    />
  );
};

// ------------------------------------------------------------------ overlays

const useRise = (delay = 0, damping?: number) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { theme } = useTheme();
  return spring({
    frame: frame - delay,
    fps,
    config: {
      damping: damping ?? theme.motion.spring_damping,
      stiffness: 140,
      mass: 0.8,
    },
  });
};

const Tag: React.FC<{
  text: string;
  top?: number;
  delay?: number;
  color?: "text" | "accent";
}> = ({ text, top = 300, delay = 0, color = "text" }) => {
  const { theme, text: font } = useTheme();
  const p = useRise(delay);
  return (
    <div
      style={{
        position: "absolute",
        top,
        left: 72,
        display: "flex",
        flexDirection: "column",
        gap: 14,
        opacity: p,
        transform: `translateY(${(1 - p) * 24}px)`,
      }}
    >
      <div
        style={{
          width: interpolate(p, [0, 1], [0, 64]),
          height: 4,
          background: theme.palette.accent,
          borderRadius: 2,
        }}
      />
      <div
        style={{
          fontFamily: font,
          fontWeight: 800,
          fontSize: theme.tags.size,
          letterSpacing: 0.5,
          color: theme.palette[color],
          textShadow: "0 2px 18px rgba(0,0,0,0.75)",
        }}
      >
        {text}
      </div>
    </div>
  );
};

const BigWord: React.FC<{
  text: string;
  top?: number;
  size?: number;
  delay?: number;
}> = ({ text, top = 760, size = 150, delay = 0 }) => {
  const { theme, display } = useTheme();
  const p = useRise(delay, 14);
  return (
    <div
      style={{
        position: "absolute",
        top,
        left: 0,
        right: 0,
        textAlign: "center",
        fontFamily: display,
        fontWeight: 800,
        fontSize: size,
        letterSpacing: -2,
        lineHeight: 1,
        color: theme.palette.text,
        opacity: Math.min(1, p * 1.4),
        transform: `scale(${0.86 + 0.14 * p})`,
        textShadow: "0 6px 40px rgba(0,0,0,0.8)",
      }}
    >
      {text}
    </div>
  );
};

const Price: React.FC<{ text: string; top?: number; delay?: number }> = ({
  text,
  top = 640,
  delay = 0,
}) => {
  const { theme, display } = useTheme();
  const p = useRise(delay, 11);
  return (
    <div
      style={{
        position: "absolute",
        top,
        left: 0,
        right: 0,
        textAlign: "center",
      }}
    >
      <div
        style={{
          fontFamily: display,
          fontWeight: 800,
          fontSize: 230,
          letterSpacing: -6,
          color: theme.palette.accent,
          lineHeight: 1,
          transform: `scale(${1.5 - 0.5 * p})`,
          opacity: Math.min(1, p * 2),
          textShadow: "0 10px 60px rgba(0,0,0,0.65)",
        }}
      >
        {text}
      </div>
    </div>
  );
};

const Coverage: React.FC<{
  box: [number, number, number, number];
  delay?: number;
}> = ({ box, delay = 0 }) => {
  const { theme } = useTheme();
  const p = useRise(delay + 6);
  const inset = interpolate(p, [0, 1], [40, 0]);
  const [x, y, w, h] = box;
  const arm = 70;
  const corner = (style: React.CSSProperties) => (
    <div
      style={{
        position: "absolute",
        width: arm,
        height: arm,
        borderColor: theme.palette.text,
        borderStyle: "solid",
        borderWidth: 0,
        opacity: p,
        ...style,
      }}
    />
  );
  return (
    <div
      style={{
        position: "absolute",
        left: x - inset,
        top: y - inset,
        width: w + inset * 2,
        height: h + inset * 2,
      }}
    >
      {corner({ left: 0, top: 0, borderLeftWidth: 5, borderTopWidth: 5 })}
      {corner({ right: 0, top: 0, borderRightWidth: 5, borderTopWidth: 5 })}
      {corner({ left: 0, bottom: 0, borderLeftWidth: 5, borderBottomWidth: 5 })}
      {corner({
        right: 0,
        bottom: 0,
        borderRightWidth: 5,
        borderBottomWidth: 5,
      })}
    </div>
  );
};

const ControlIcon: React.FC<{
  kind: "moon" | "lamp" | "dim" | "dot";
  level: number;
}> = ({ kind, level }) => {
  const { theme } = useTheme();
  const { text, accent } = theme.palette;
  if (kind === "moon")
    return (
      <svg width="64" height="64" viewBox="0 0 64 64">
        <circle cx="32" cy="32" r="24" fill={text} />
        <circle
          cx="24"
          cy="26"
          r="5"
          fill={theme.palette.muted}
          opacity="0.5"
        />
        <circle
          cx="38"
          cy="38"
          r="7"
          fill={theme.palette.muted}
          opacity="0.5"
        />
      </svg>
    );
  if (kind === "lamp")
    return (
      <svg width="64" height="64" viewBox="0 0 64 64">
        <circle cx="32" cy="32" r="26" fill={accent} opacity="0.25" />
        <circle cx="32" cy="32" r="14" fill={accent} />
      </svg>
    );
  if (kind === "dim")
    return (
      <svg width="64" height="64" viewBox="0 0 64 64">
        <rect x="8" y="28" width="48" height="8" rx="4" fill="#3A3833" />
        <rect x="8" y="28" width={48 * level} height="8" rx="4" fill={text} />
        <circle cx={8 + 48 * level} cy="32" r="10" fill={text} />
      </svg>
    );
  return (
    <svg width="64" height="64" viewBox="0 0 64 64">
      <circle cx="32" cy="32" r="12" fill={text} />
    </svg>
  );
};

const Controls: React.FC<{
  rows: Extract<Overlay, { type: "controls" }>["rows"];
  top?: number;
}> = ({ rows, top = 380 }) => {
  const frame = useCurrentFrame();
  const { theme, text: font, display } = useTheme();
  const warmRow = rows.find((r) => r.icon === "lamp");
  const nextAfterWarm = warmRow
    ? rows.find((r) => r.at > warmRow.at)
    : undefined;
  const warmAt = warmRow ? f(warmRow.at) : -1;
  const warmEnd = nextAfterWarm ? f(nextAfterWarm.at) : warmAt + 90;
  const warm = warmRow
    ? interpolate(
        frame,
        [warmAt, warmAt + 12, warmEnd - 6, warmEnd + 6],
        [0, 0.32, 0.32, 0],
        { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
      )
    : 0;
  const dimRow = rows.find((r) => r.icon === "dim");
  const dimAt = dimRow ? f(dimRow.at) : 0;
  const level = interpolate(
    frame,
    [dimAt + 10, dimAt + 40, dimAt + 70],
    [0.3, 0.9, 0.55],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );
  return (
    <>
      <AbsoluteFill
        style={{
          background: `radial-gradient(circle at 50% 40%, rgba(${hexToRgb(theme.palette.accent)},${warm}) 0%, rgba(${hexToRgb(theme.palette.accent)},0) 70%)`,
        }}
      />
      <div
        style={{
          position: "absolute",
          top,
          left: 80,
          right: 80,
          display: "flex",
          flexDirection: "column",
          gap: 26,
        }}
      >
        {rows.map((row, i) => (
          <ControlRow key={i} delay={f(row.at)}>
            <ControlIcon kind={row.icon} level={level} />
            <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
              <div
                style={{
                  fontFamily: font,
                  fontWeight: 700,
                  fontSize: 34,
                  color: theme.palette.muted,
                  letterSpacing: 1,
                }}
              >
                {row.step}
              </div>
              <div
                style={{
                  fontFamily: display,
                  fontWeight: 800,
                  fontSize: 64,
                  color: row.accent ? theme.palette.accent : theme.palette.text,
                  letterSpacing: -1,
                }}
              >
                {row.label}
              </div>
            </div>
          </ControlRow>
        ))}
      </div>
    </>
  );
};

const ControlRow: React.FC<{ delay: number; children: React.ReactNode }> = ({
  delay,
  children,
}) => {
  const p = useRise(delay, 16);
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: 30,
        padding: "34px 40px",
        borderRadius: 28,
        background: "rgba(10,10,12,0.72)",
        border: "1.5px solid rgba(242,238,228,0.14)",
        opacity: p,
        transform: `translateX(${(1 - p) * -60}px)`,
      }}
    >
      {children}
    </div>
  );
};

const Ring: React.FC<
  Extract<Overlay, { type: "ring" }> & { delay: number }
> = ({ cx, cy, rx, ry, label, labelY, turn, dark, delay }) => {
  const frame = useCurrentFrame();
  const { theme, display } = useTheme();
  const { accent, text, background } = theme.palette;
  const draw = interpolate(frame - delay, [0, 18], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const circumference =
    Math.PI * (3 * (rx + ry) - Math.sqrt((3 * rx + ry) * (rx + 3 * ry)));
  const spin = turn
    ? interpolate(frame - delay, [10, 70], [-40, 40], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
        easing: Easing.inOut(Easing.sin),
      })
    : 0;
  const p = useRise(delay + 8);
  return (
    <AbsoluteFill>
      <svg
        width="1080"
        height="1920"
        style={{ position: "absolute", inset: 0 }}
      >
        <ellipse
          cx={cx}
          cy={cy}
          rx={rx}
          ry={ry}
          fill="none"
          stroke={accent}
          strokeWidth={7}
          strokeDasharray={circumference}
          strokeDashoffset={circumference * (1 - draw)}
          style={{
            filter: `drop-shadow(0 0 12px rgba(${hexToRgb(accent)},0.7))`,
          }}
        />
        {turn && (
          <g transform={`rotate(${spin} ${cx} ${cy})`} opacity={p}>
            <path
              d={`M ${cx - rx * 0.7} ${cy - ry - 34} A ${rx} ${ry + 34} 0 0 1 ${cx + rx * 0.7} ${cy - ry - 34}`}
              fill="none"
              stroke={text}
              strokeWidth={6}
              strokeLinecap="round"
            />
            <path
              d={`M ${cx + rx * 0.7 - 26} ${cy - ry - 58} L ${cx + rx * 0.7 + 4} ${cy - ry - 34} L ${cx + rx * 0.7 - 30} ${cy - ry - 16}`}
              fill="none"
              stroke={text}
              strokeWidth={6}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </g>
        )}
      </svg>
      <div
        style={{
          position: "absolute",
          top: labelY,
          left: 0,
          right: 0,
          textAlign: "center",
          fontFamily: display,
          fontWeight: 800,
          fontSize: 76,
          color: dark ? background : text,
          opacity: p,
          transform: `translateY(${(1 - p) * 20}px)`,
          textShadow: dark ? "none" : "0 4px 30px rgba(0,0,0,0.85)",
        }}
      >
        {label}
      </div>
    </AbsoluteFill>
  );
};

const Check: React.FC<{ size?: number }> = ({ size = 56 }) => {
  const { theme } = useTheme();
  return (
    <svg width={size} height={size} viewBox="0 0 56 56">
      <circle cx="28" cy="28" r="26" fill={theme.palette.accent} />
      <path
        d="M16 29 L25 38 L41 19"
        fill="none"
        stroke={theme.palette.background}
        strokeWidth="6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
};

const PauseMark: React.FC = () => {
  const { theme } = useTheme();
  return (
    <svg width="84" height="84" viewBox="0 0 84 84">
      <circle
        cx="42"
        cy="42"
        r="40"
        fill="none"
        stroke={theme.palette.text}
        strokeWidth="4"
      />
      <rect
        x="28"
        y="24"
        width="9"
        height="36"
        rx="3"
        fill={theme.palette.text}
      />
      <rect
        x="47"
        y="24"
        width="9"
        height="36"
        rx="3"
        fill={theme.palette.text}
      />
    </svg>
  );
};

const Verdict: React.FC<{
  line1: string;
  line2: string;
  icon: "check" | "pause";
  accent?: boolean;
  delay: number;
}> = ({ line1, line2, icon, accent, delay }) => {
  const { theme, display, text: font } = useTheme();
  const a = useRise(delay);
  const b = useRise(delay + 10);
  return (
    <div style={{ position: "absolute", top: 330, left: 72, right: 72 }}>
      <div
        style={{
          fontFamily: font,
          fontWeight: 800,
          fontSize: 50,
          color: theme.palette.text,
          opacity: a,
          transform: `translateY(${(1 - a) * 20}px)`,
          textShadow: "0 2px 20px rgba(0,0,0,0.8)",
        }}
      >
        {line1}
      </div>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 22,
          marginTop: 14,
          opacity: b,
          transform: `translateY(${(1 - b) * 24}px)`,
        }}
      >
        {icon === "check" ? <Check size={86} /> : <PauseMark />}
        <div
          style={{
            fontFamily: display,
            fontWeight: 800,
            fontSize: 104,
            letterSpacing: -3,
            color: accent ? theme.palette.accent : theme.palette.text,
            lineHeight: 1,
            textShadow: "0 6px 40px rgba(0,0,0,0.8)",
          }}
        >
          {line2}
        </div>
      </div>
    </div>
  );
};

const Checklist: React.FC<{
  title: string;
  items: { text: string; at: number }[];
}> = ({ title, items }) => {
  const { theme, display, text: font } = useTheme();
  const head = useRise(0);
  return (
    <div
      style={{
        position: "absolute",
        top: 330,
        left: 72,
        display: "flex",
        flexDirection: "column",
        gap: 30,
      }}
    >
      <div
        style={{
          fontFamily: font,
          fontWeight: 800,
          fontSize: 44,
          color: theme.palette.accent,
          letterSpacing: 2,
          opacity: head,
        }}
      >
        {title}
      </div>
      {items.map((item, i) => (
        <ChecklistRow
          key={i}
          text={item.text}
          delay={f(item.at)}
          font={display}
          color={theme.palette.text}
        />
      ))}
    </div>
  );
};

const ChecklistRow: React.FC<{
  text: string;
  delay: number;
  font: string;
  color: string;
}> = ({ text, delay, font, color }) => {
  const p = useRise(delay);
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: 24,
        opacity: p,
        transform: `translateX(${(1 - p) * -50}px)`,
      }}
    >
      <Check size={70} />
      <div
        style={{
          fontFamily: font,
          fontWeight: 800,
          fontSize: 70,
          color,
          letterSpacing: -1,
          textShadow: "0 4px 30px rgba(0,0,0,0.9)",
        }}
      >
        {text}
      </div>
    </div>
  );
};

const OverlayView: React.FC<{ overlay: Overlay }> = ({ overlay: o }) => {
  const at = "at" in o && o.at ? f(o.at) : 0;
  switch (o.type) {
    case "tag":
      return (
        <Sequence from={at} layout="none">
          <Tag text={o.text} top={o.top} color={o.color} />
        </Sequence>
      );
    case "bigword":
      return <BigWord text={o.text} top={o.top} size={o.size} delay={at} />;
    case "price":
      return (
        <Sequence from={at} layout="none">
          <TopScrim strength={0.5} />
          <Price text={o.text} top={o.top} />
        </Sequence>
      );
    case "coverage":
      return <Coverage box={o.box} delay={at} />;
    case "controls":
      return <Controls rows={o.rows} top={o.top} />;
    case "ring":
      return (
        <Sequence from={at} layout="none">
          <Ring {...o} delay={0} />
        </Sequence>
      );
    case "verdict":
      return (
        <Verdict
          line1={o.line1}
          line2={o.line2}
          icon={o.icon}
          accent={o.accent}
          delay={at}
        />
      );
    case "checklist":
      return (
        <>
          <TopScrim />
          <Checklist title={o.title} items={o.items} />
        </>
      );
    case "scrim":
      return <TopScrim strength={o.strength} />;
  }
};

// ------------------------------------------------------------------ captions

const Captions: React.FC<{ captions: Caption[] }> = ({ captions }) => {
  const frame = useCurrentFrame();
  const { theme, text: font } = useTheme();
  const t = frame / FPS;
  // Latest-starting caption wins, so a line never lingers into the next one.
  const current = [...captions]
    .reverse()
    .find((c) => t >= c.start - 0.05 && t < c.end + 0.05);
  const c = theme.captions;
  return (
    <AbsoluteFill>
      {c.scrim && (
        <AbsoluteFill
          style={{
            background:
              "linear-gradient(180deg, rgba(0,0,0,0) 62%, rgba(0,0,0,0.55) 78%, rgba(0,0,0,0.62) 100%)",
            opacity: current ? 1 : 0,
          }}
        />
      )}
      {current && (
        <CaptionLine key={current.start} caption={current} font={font} />
      )}
    </AbsoluteFill>
  );
};

const CaptionLine: React.FC<{ caption: Caption; font: string }> = ({
  caption,
  font,
}) => {
  const frame = useCurrentFrame();
  const { theme } = useTheme();
  const c = theme.captions;
  const p = interpolate(frame - f(caption.start), [0, 5], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.quad),
  });
  return (
    <div
      style={{
        position: "absolute",
        top: c.top,
        left: c.left,
        right: c.right,
        textAlign: "center",
        fontFamily: font,
        fontWeight: c.weight,
        fontSize: c.size,
        lineHeight: 1.22,
        color: theme.palette.text,
        opacity: p,
        transform: `translateY(${(1 - p) * 12}px)`,
        textShadow: "0 2px 4px rgba(0,0,0,0.9), 0 0 24px rgba(0,0,0,0.6)",
      }}
    >
      {caption.text}
    </div>
  );
};

// ------------------------------------------------------------------ audio

const Soundtrack: React.FC<ReelProps> = ({
  narration,
  music,
  musicVolume,
  musicDuckedVolume,
  timeline,
  durationSeconds,
  sfx,
}) => {
  const total = f(durationSeconds);
  const musicLevel = (frame: number) => {
    const t = frame / FPS;
    const speaking = timeline.some(
      (s) => t > s.start - 0.25 && t < s.end + 0.2,
    );
    const fadeIn = interpolate(frame, [0, 12], [0, 1], {
      extrapolateRight: "clamp",
    });
    const fadeOut = interpolate(frame, [total - 40, total], [1, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
    return (speaking ? musicDuckedVolume : musicVolume) * fadeIn * fadeOut;
  };
  return (
    <>
      <Audio src={staticFile(narration)} />
      {music && <Audio src={staticFile(music)} volume={musicLevel} />}
      {sfx.map((s, i) => (
        <Sequence key={i} from={f(s.at)} durationInFrames={f(2)} layout="none">
          <Audio
            src={staticFile(`audio/sfx/${s.name}.wav`)}
            volume={s.volume}
          />
        </Sequence>
      ))}
    </>
  );
};

// ------------------------------------------------------------------ shots

const ShotView: React.FC<{ shot: Shot; frames: number; isLast: boolean }> = ({
  shot,
  frames,
}) => {
  const { theme } = useTheme();
  let body: React.ReactNode = <MediaLayer media={shot.media} frames={frames} />;
  if (shot.enter === "whip") body = <WhipIn>{body}</WhipIn>;
  if (shot.enter === "aperture" && shot.aperture) {
    body = (
      <Aperture
        cx={shot.aperture.cx}
        cy={shot.aperture.cy}
        frames={20}
        mode="open"
      >
        {body}
      </Aperture>
    );
  }
  const overlays = (
    <>
      {theme.motion.vignette && <Vignette />}
      {(shot.overlays ?? []).map((o, i) => (
        <OverlayView key={i} overlay={o} />
      ))}
    </>
  );
  if (shot.exit === "aperture") {
    const close = 24;
    const media = <MediaLayer media={shot.media} frames={frames} />;
    return (
      <>
        <Sequence from={0} durationInFrames={frames - close} layout="none">
          <AbsoluteFill>{body}</AbsoluteFill>
        </Sequence>
        <Sequence from={frames - close} layout="none">
          <Aperture cx={540} cy={860} frames={close} mode="close">
            {media}
          </Aperture>
        </Sequence>
        <FadeTail frames={frames} tail={20}>
          {overlays}
        </FadeTail>
      </>
    );
  }
  if (shot.exit === "fade") {
    return (
      <FadeTail frames={frames} tail={18}>
        {body}
        {overlays}
      </FadeTail>
    );
  }
  return (
    <>
      {body}
      {overlays}
    </>
  );
};

// ------------------------------------------------------------------ cover

const CoverCard: React.FC<{ cover: ReelProps["cover"] }> = ({ cover }) => {
  const { theme, display, text: font } = useTheme();
  const bg = hexToRgb(theme.palette.background);
  return (
    <AbsoluteFill style={{ background: theme.palette.background }}>
      {cover.image && (
        <Img
          src={staticFile(cover.image)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            transform: "scale(1.12)",
            transformOrigin: "52% 30%",
          }}
        />
      )}
      <AbsoluteFill
        style={{
          background: `linear-gradient(180deg, rgba(${bg},0) 35%, rgba(${bg},0.85) 72%, rgba(${bg},0.95) 100%)`,
        }}
      />
      <div style={{ position: "absolute", left: 80, right: 80, top: 1180 }}>
        <div
          style={{
            width: 90,
            height: 6,
            background: theme.palette.accent,
            borderRadius: 3,
            marginBottom: 30,
          }}
        />
        <div
          style={{
            fontFamily: display,
            fontWeight: 800,
            fontSize: 180,
            lineHeight: 0.95,
            letterSpacing: -6,
            color: theme.palette.accent,
          }}
        >
          {cover.kicker}
        </div>
        <div
          style={{
            fontFamily: display,
            fontWeight: 800,
            fontSize: 104,
            lineHeight: 1.0,
            letterSpacing: -3,
            color: theme.palette.text,
            marginTop: 10,
          }}
        >
          {cover.title}
        </div>
        <div
          style={{
            fontFamily: font,
            fontWeight: 700,
            fontSize: 48,
            color: theme.palette.muted,
            marginTop: 24,
          }}
        >
          {cover.subtitle}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const ThemeScope: React.FC<{ theme: Theme; children: React.ReactNode }> = ({
  theme,
  children,
}) => {
  const value = React.useMemo(
    () => ({
      theme,
      display: loadThemeFont(theme.fonts.display),
      text: loadThemeFont(theme.fonts.text),
    }),
    [theme],
  );
  return (
    <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
  );
};

export const Reel: React.FC<ReelProps> = (props) => {
  const coverFrames = f(props.theme.intro?.cover_seconds ?? 0);
  return (
    <ThemeScope theme={props.theme}>
      <AbsoluteFill style={{ background: props.theme.palette.background }}>
        {coverFrames > 0 && (
          <Sequence from={0} durationInFrames={coverFrames}>
            <CoverCard cover={props.cover} />
          </Sequence>
        )}
        <Sequence from={coverFrames}>
          {props.shots.map((shot, i) => {
            const start = f(shot.from);
            const frames = f(shot.to) - start;
            return (
              <Sequence key={shot.id} from={start} durationInFrames={frames}>
                <ShotView
                  shot={shot}
                  frames={frames}
                  isLast={i === props.shots.length - 1}
                />
              </Sequence>
            );
          })}
          <Captions captions={props.captions} />
          <Soundtrack {...props} />
        </Sequence>
      </AbsoluteFill>
    </ThemeScope>
  );
};

export const Cover: React.FC<ReelProps> = (props) => (
  <ThemeScope theme={props.theme}>
    <CoverCard cover={props.cover} />
  </ThemeScope>
);

export const calculateMetadata: CalculateMetadataFunction<ReelProps> = async ({
  props,
}) => ({
  durationInFrames: f(
    (props.durationSeconds ?? 60) + (props.theme?.intro?.cover_seconds ?? 0),
  ),
  fps: FPS,
  width: 1080,
  height: 1920,
});
