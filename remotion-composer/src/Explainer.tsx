import {
  AbsoluteFill,
  Audio,
  Img,
  OffthreadVideo,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/SpaceGrotesk";

// Resolve asset path — handle URLs, absolute paths (Windows/Unix), and public/ relative paths
function resolveAsset(src: string): string {
  if (src.startsWith("http://") || src.startsWith("https://") || src.startsWith("data:")) {
    return src;
  }
  // Strip any file:// prefix
  const clean = src.replace(/^file:\/\/\/?/, "");
  // Absolute paths (Unix: /foo, Windows: C:\foo or C:/foo) — convert to file:// URI
  // staticFile() only accepts relative paths within public/, so absolute paths must bypass it
  if (clean.startsWith("/") || /^[A-Za-z]:[\\/]/.test(clean)) {
    return `file:///${clean.replace(/\\/g, "/")}`;
  }
  return staticFile(clean);
}
import { TextCard } from "./components/TextCard";
import { StatCard } from "./components/StatCard";
import { CalloutBox } from "./components/CalloutBox";
import { ComparisonCard } from "./components/ComparisonCard";
import { BarChart } from "./components/charts/BarChart";
import { LineChart } from "./components/charts/LineChart";
import { PieChart } from "./components/charts/PieChart";
import { KPIGrid } from "./components/charts/KPIGrid";
import { ProgressBar } from "./components/ProgressBar";
import { CaptionOverlay, WordCaption } from "./components/CaptionOverlay";
import { SectionTitle } from "./components/SectionTitle";
import { StatReveal } from "./components/StatReveal";
import { HeroTitle } from "./components/HeroTitle";
import { AnimeScene } from "./components/AnimeScene";
import type { CameraMotion } from "./components/AnimeScene";
import { TerminalScene } from "./components/TerminalScene";
import type { TerminalStep } from "./components/TerminalScene";
import { ScreenshotScene } from "./components/ScreenshotScene";
import type { ScreenshotStep } from "./components/ScreenshotScene";
import { ProviderChip } from "./components/ProviderChip";
import { ThesisTitle } from "./components/ThesisTitle";
import { SkinCrossSection } from "./components/SkinCrossSection";
import { SkinCrossSection3D } from "./components/SkinCrossSection3D";
import { ScarCompare } from "./components/ScarCompare";
import type { SkinPhase, SkinCrossSectionLabels } from "./components/SkinCrossSection";
import { MarginOverlay } from "./components/MarginOverlay";
import { TimeCounter } from "./components/TimeCounter";
import { SizeGuide } from "./components/SizeGuide";
import { SkinSwatch } from "./components/SkinSwatch";
import { ResultCurve } from "./components/ResultCurve";
import type { ResultMilestone } from "./components/ResultCurve";
import { MythFact } from "./components/MythFact";
import { CheckList } from "./components/CheckList";
import type { CheckListItem } from "./components/CheckList";
import { DayClock } from "./components/DayClock";
import type { DayClockItem } from "./components/DayClock";
import { PatchHero3D } from "./components/PatchHero3D";
import type { ScarState, SkinShape, SkinStep } from "./components/SkinSwatch";
import type { SizeGuideItem } from "./components/SizeGuide";
import { EndCard } from "./components/EndCard";
import { HealingTimeline } from "./components/HealingTimeline";
import { AnimaticNote } from "./components/AnimaticNote";
import { StatBadge } from "./components/StatBadge";
import { AudienceChips } from "./components/AudienceChips";
import { CanvasContext } from "./components/yafho/tokens";
import type { ParticleType } from "./components/ParticleOverlay";
import { resolveTheme, type ThemeConfig, DEFAULT_THEME } from "./Root";

// Load Space Grotesk font for cinematic typography
const { fontFamily } = loadFont("normal", {
  weights: ["400", "700"],
  subsets: ["latin"],
});

// ---------------------------------------------------------------------------
// Animated Background — Gradient Mesh + Floating Orbs
// ---------------------------------------------------------------------------

// Parse hex color to RGB components
function hexToRgb(hex: string): { r: number; g: number; b: number } {
  const clean = hex.replace("#", "");
  const bigint = parseInt(clean.length === 3
    ? clean.split("").map(c => c + c).join("")
    : clean, 16);
  return { r: (bigint >> 16) & 255, g: (bigint >> 8) & 255, b: bigint & 255 };
}

// Detect if a color is "light" (for choosing grid/overlay treatment)
function isLightColor(hex: string): boolean {
  const { r, g, b } = hexToRgb(hex);
  return (r * 299 + g * 587 + b * 114) / 1000 > 128;
}

// Darken/lighten a color by mixing toward black or white
function shiftColor(hex: string, amount: number): string {
  const { r, g, b } = hexToRgb(hex);
  const clamp = (v: number) => Math.max(0, Math.min(255, Math.round(v)));
  if (amount < 0) {
    // Darken
    const f = 1 + amount;
    return `rgb(${clamp(r * f)}, ${clamp(g * f)}, ${clamp(b * f)})`;
  }
  // Lighten
  return `rgb(${clamp(r + (255 - r) * amount)}, ${clamp(g + (255 - g) * amount)}, ${clamp(b + (255 - b) * amount)})`;
}

const AnimatedBackground: React.FC<{ theme: ThemeConfig }> = ({ theme }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const bg = theme.backgroundColor;
  const primary = theme.primaryColor;
  const accent = theme.accentColor;
  const surface = theme.surfaceColor;
  const light = isLightColor(bg);

  // Slow-moving gradient angles
  const angle1 = 135 + Math.sin(frame / (fps * 8)) * 30;

  // Build gradient from theme colors instead of hardcoded dark blue
  const { r: bgR, g: bgG, b: bgB } = hexToRgb(bg);
  const { r: priR, g: priG, b: priB } = hexToRgb(primary);
  const { r: accR, g: accG, b: accB } = hexToRgb(accent);

  const gradient = `
    radial-gradient(ellipse at ${30 + Math.sin(frame / (fps * 10)) * 20}% ${40 + Math.cos(frame / (fps * 8)) * 20}%,
      rgba(${priR}, ${priG}, ${priB}, 0.15) 0%, transparent 60%),
    radial-gradient(ellipse at ${70 + Math.cos(frame / (fps * 7)) * 20}% ${60 + Math.sin(frame / (fps * 9)) * 25}%,
      rgba(${accR}, ${accG}, ${accB}, 0.1) 0%, transparent 55%),
    linear-gradient(${angle1}deg, ${bg} 0%, ${shiftColor(bg, light ? -0.05 : 0.05)} 40%, ${surface} 70%, ${bg} 100%)
  `;

  // Floating orbs — derived from theme chart colors with low opacity
  const orbColors = theme.chartColors.slice(0, 5);
  const orbOpacity = light ? 0.06 : 0.08;
  const orbs = [
    { x: 20, y: 30, size: 300, color: orbColors[0] || primary, speedX: 7, speedY: 11 },
    { x: 70, y: 60, size: 250, color: orbColors[1] || accent, speedX: 9, speedY: 8 },
    { x: 40, y: 80, size: 200, color: orbColors[2] || primary, speedX: 13, speedY: 6 },
    { x: 80, y: 20, size: 350, color: orbColors[3] || accent, speedX: 11, speedY: 14 },
    { x: 10, y: 70, size: 180, color: orbColors[4] || primary, speedX: 8, speedY: 10 },
  ];

  // Grid and overlay colors adapt to light vs dark backgrounds
  const gridColor = light ? "rgba(0,0,0,0.03)" : "rgba(255,255,255,0.02)";
  const fadeColor = light
    ? `rgba(${bgR},${bgG},${bgB},0.2)`
    : `rgba(${bgR},${bgG},${bgB},0.4)`;

  return (
    <AbsoluteFill style={{ background: gradient }}>
      {/* Floating glow orbs */}
      {orbs.map((orb, i) => {
        const ox = orb.x + Math.sin(frame / (fps * orb.speedX)) * 15;
        const oy = orb.y + Math.cos(frame / (fps * orb.speedY)) * 12;
        const { r, g, b } = hexToRgb(orb.color);
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: `${ox}%`,
              top: `${oy}%`,
              width: orb.size,
              height: orb.size,
              borderRadius: "50%",
              background: `rgba(${r}, ${g}, ${b}, ${orbOpacity})`,
              filter: `blur(${orb.size * 0.4}px)`,
              transform: "translate(-50%, -50%)",
              willChange: "transform",
            }}
          />
        );
      })}

      {/* Subtle grid overlay */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: `
            linear-gradient(${gridColor} 1px, transparent 1px),
            linear-gradient(90deg, ${gridColor} 1px, transparent 1px)
          `,
          backgroundSize: "60px 60px",
          opacity: 0.5 + Math.sin(frame / (fps * 20)) * 0.2,
        }}
      />

      {/* Top gradient fade for depth */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: "30%",
          background: `linear-gradient(to bottom, ${fadeColor}, transparent)`,
        }}
      />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
// Types — aligned with edit_decisions artifact schema
// ---------------------------------------------------------------------------

interface Cut {
  id: string;
  source: string;
  in_seconds: number;
  out_seconds: number;
  layer?: string;
  type?: string;
  // Component-specific props
  text?: string;
  stat?: string;
  subtitle?: string;
  callout_type?: "info" | "warning" | "tip" | "quote";
  title?: string;
  // Video source trim — seek to this point in the source before playback.
  // Defaults to 0 (play from beginning). Use this instead of in_seconds for source trimming.
  source_in_seconds?: number;
  // Comparison props
  leftLabel?: string;
  rightLabel?: string;
  leftValue?: string;
  rightValue?: string;
  // Chart props
  chartData?: any[];
  chartSeries?: any[];
  chartColors?: string[];
  chartAnimation?: string;
  donut?: boolean;
  centerLabel?: string;
  centerValue?: string;
  showGrid?: boolean;
  showValues?: boolean;
  showLegend?: boolean;
  showMarkers?: boolean;
  xLabel?: string;
  yLabel?: string;
  columns?: 2 | 3 | 4;
  // Progress bar props
  progress?: number;
  progressLabel?: string;
  progressColor?: string;
  progressAnimation?: string;
  progressSegments?: any[];
  // Hero title props (when used as scene, not overlay)
  heroSubtitle?: string;
  // Styling overrides
  backgroundColor?: string;
  backgroundImage?: string; // AI-generated or stock image rendered behind the component
  backgroundVideo?: string; // Video clip rendered behind the component (takes priority over backgroundImage)
  backgroundVideoStart?: number; // Seek position in seconds for background video (default 0)
  backgroundOverlay?: number; // Opacity of dark overlay on backgroundImage/backgroundVideo (0-1, default 0.55)
  color?: string;
  accentColor?: string;
  fontSize?: number;
  // Animation & transitions
  animation?: string;
  transition_in?: string;
  transition_out?: string;
  transform?: {
    animation?: string;
    scale?: number;
    position?: string | { x: number; y: number };
  };
  // Anime scene props (type: "anime_scene")
  images?: string[];
  particles?: ParticleType;
  particleColor?: string;
  particleCount?: number;
  particleIntensity?: number;
  vignette?: boolean;
  lightingFrom?: string;
  lightingTo?: string;
  // Terminal scene props (type: "terminal_scene")
  steps?: TerminalStep[];
  terminalTitle?: string;
  prompt?: string;
  // Screenshot scene props (type: "screenshot_scene")
  screenshotSteps?: ScreenshotStep[];
  screenshotSize?: { width: number; height: number };
  cursorStartAt?: [number, number];
  // Skin cross-section (type: "skin_cross_section")
  phase?: SkinPhase;
  crossLabels?: SkinCrossSectionLabels;
  introFade?: boolean;
  focusX?: number;
  centerY?: number;
  fitFrac?: number;
  // scar_compare / skin_cross_section_3d progress window
  progressFrom?: number;
  progressTo?: number;
  /** "Dive" exit: push in, soften and fade out over the last N seconds of the cut. */
  exitZoom?: number;
  /** Video playback speed (e.g. stretch a 5 s Kling clip over a 7.5 s slot). */
  playbackRate?: number;
  // Size guide (type: "size_guide")
  sizeItems?: SizeGuideItem[];
  // Skin close-up with sheet (type: "skin_demo")
  skinShape?: SkinShape;
  skinStep?: SkinStep;
  skinState?: ScarState;
  skinFrom?: ScarState;
  months?: number;
  reveal?: boolean;
  land?: boolean;
  soften?: boolean;
  zoom?: number;
  /** skin_demo / result_curve / scar_compare: vertical band the cards occupy (fractions of the canvas). */
  areaTop?: number;
  areaBottom?: number;
  // Result timing curve (type: "result_curve")
  milestones?: ResultMilestone[];
  // Myth → fact card (type: "myth_fact")
  myth?: string;
  fact?: string;
  counter?: string;
  mythVariant?: "myth" | "qa";
  // Check list (type: "check_list") — header from `title`
  checkItems?: CheckListItem[];
  checkNote?: string;
  // 24 h dial (type: "day_clock")
  clockItems?: DayClockItem[];
  clockStart?: number;
  clockSummary?: string;
  clockSummaryNote?: string;
  // 3D sheet (type: "patch_3d"); end_card takes patch3d
  motion?: "flex" | "spin";
  size?: number;
  patch3d?: boolean;
  // End card (type: "end_card")
  logoSrc?: string;
  brand?: string;
  tagline?: string;
  handle?: string;
  qr?: number[][];
  qrCaption?: string;
  cta?: string;
}

interface Overlay {
  type:
    | "section_title"
    | "stat_reveal"
    | "hero_title"
    | "provider_chip"
    | "thesis"
    | "margin_overlay"
    | "time_counter"
    | "healing_timeline"
    | "animatic_note"
    | "stat_badge"
    | "audience_chips";
  in_seconds: number;
  out_seconds: number;
  text?: string;
  subtitle?: string;
  accentColor?: string;
  position?: string;
  // provider_chip
  providers?: string[];
  cycleSeconds?: number;
  label?: string;
  // thesis
  variant?: "dark" | "light";
  fontSize?: number;
  // margin_overlay
  scarBox?: { x: number; y: number; w: number; h: number };
  marginPx?: number;
  // time_counter
  labels?: string[];
  // healing_timeline
  from?: number;
  to?: number;
  highlightWindow?: boolean;
  ticks?: boolean;
  emphasis?: boolean;
  // audience_chips
  chips?: string[];
  // stat_badge
  value?: string;
  source?: string;
  /** Only render in these layouts (default: all). */
  layouts?: ("full" | "split")[];
}

interface AudioLayer {
  src: string;
  volume?: number;
}

interface AudioConfig {
  narration?: AudioLayer;
  music?: AudioLayer & {
    fadeInSeconds?: number;
    fadeOutSeconds?: number;
    /** Start playback from this offset in seconds (skip quiet intros).
     *  Use the audio_energy tool to find the optimal offset. */
    offsetSeconds?: number;
    /** Loop the music if it's shorter than the video duration. */
    loop?: boolean;
  };
}

export interface ExplainerProps {
  [key: string]: unknown;
  /**
   * "full"  — scenes fill the frame (default).
   * "split" — 16:9 frame: scenes play in a 9:16 panel on the left (or centre),
   *           thesis overlays move to a text panel on the right.
   */
  layout?: "full" | "split";
  splitPanel?: "left" | "center";
  /** Exact composition length; otherwise last cut end + 1s. */
  durationSeconds?: number;
  width?: number;
  height?: number;
  /** Brand backdrop behind every scene that does not paint its own background. */
  backdrop?: { image?: string; color?: string };
  cuts: Cut[];
  overlays?: Overlay[];
  captions?: WordCaption[];
  audio?: AudioConfig;
}

// ---------------------------------------------------------------------------
// Image Extensions
// ---------------------------------------------------------------------------

const IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"];
const VIDEO_EXTENSIONS = [".mp4", ".mov", ".webm", ".avi", ".mkv"];

function isImage(source: string): boolean {
  const lower = source.toLowerCase();
  return IMAGE_EXTENSIONS.some((ext) => lower.endsWith(ext));
}

function isVideo(source: string): boolean {
  const lower = source.toLowerCase();
  return VIDEO_EXTENSIONS.some((ext) => lower.endsWith(ext));
}

// ---------------------------------------------------------------------------
// Cinematic vignette overlay
// ---------------------------------------------------------------------------

const Vignette: React.FC = () => (
  <AbsoluteFill
    style={{
      background:
        "radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.6) 100%)",
      pointerEvents: "none",
    }}
  />
);

// ---------------------------------------------------------------------------
// Enhanced Image Scene — spring physics, parallax, variety
// ---------------------------------------------------------------------------

const ImageScene: React.FC<{ src: string; animation?: string; flat?: boolean; introFade?: boolean }> = ({
  src,
  animation,
  flat = false,
  introFade = true,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  if (flat) {
    // Brand-flat treatment: 0.4s fade-in, gentle push-in, no vignette or dimming.
    const fade = introFade ? interpolate(frame, [0, 0.4 * fps], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 1;
    const push = interpolate(frame, [0, durationInFrames], [1, animation === "static" ? 1 : animation === "gentle" ? 1.025 : 1.06], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
    return (
      <AbsoluteFill style={{ overflow: "hidden" }}>
        <Img src={resolveAsset(src)} style={{ width: "100%", height: "100%", objectFit: "cover", opacity: fade, transform: `scale(${push})` }} />
      </AbsoluteFill>
    );
  }

  // Smooth spring fade-in
  const fadeIn = spring({ frame, fps, config: { damping: 18, stiffness: 80 } });

  // Fade-out for crossfade effect
  const fadeOutStart = durationInFrames - 8;
  const fadeOut = interpolate(frame, [fadeOutStart, durationInFrames], [1, 0.3], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  let scale = 1;
  let translateX = 0;
  let translateY = 0;
  const anim = animation || "zoom-in";

  // Progress with easing — smoother than linear
  const progress = interpolate(frame, [0, durationInFrames], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  if (anim === "zoom-in") {
    scale = 1 + progress * 0.18;
  } else if (anim === "zoom-out") {
    scale = 1.18 - progress * 0.18;
  } else if (anim === "pan-left") {
    translateX = interpolate(progress, [0, 1], [40, -40]);
    scale = 1.15;
  } else if (anim === "pan-right") {
    translateX = interpolate(progress, [0, 1], [-40, 40]);
    scale = 1.15;
  } else if (anim === "ken-burns" || anim === "ken-burns-slow-zoom") {
    // Cinematic Ken Burns: gentle zoom + diagonal drift
    scale = 1 + progress * 0.22;
    translateX = interpolate(progress, [0, 1], [0, -25]);
    translateY = interpolate(progress, [0, 1], [0, -15]);
  } else if (anim === "parallax") {
    // Subtle parallax — foreground moves faster
    translateY = interpolate(progress, [0, 1], [15, -15]);
    scale = 1.1;
  }
  // "static" or "none" → just display

  return (
    <AbsoluteFill style={{ overflow: "hidden", background: "#0F172A" }}>
      <Img
        src={resolveAsset(src)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          opacity: fadeIn * fadeOut,
          transform: `scale(${scale}) translate(${translateX}px, ${translateY}px)`,
          willChange: "transform, opacity",
        }}
      />
      <Vignette />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
// Enhanced Video Scene
// ---------------------------------------------------------------------------

const VideoScene: React.FC<{ src: string; startFrom?: number; flat?: boolean; playbackRate?: number }> = ({
  src,
  startFrom = 0,
  flat = false,
  playbackRate = 1,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  if (flat) {
    // Brand-flat treatment: 0.4s linear fade-in, no vignette, no dimming tail.
    const fade = interpolate(frame, [0, 0.4 * fps], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
    return (
      <AbsoluteFill style={{ background: "transparent" }}>
        <OffthreadVideo
          src={resolveAsset(src)}
          startFrom={Math.round(startFrom * fps)}
          style={{ width: "100%", height: "100%", objectFit: "cover", opacity: fade }}
          playbackRate={playbackRate}
          muted
        />
      </AbsoluteFill>
    );
  }

  const fadeIn = spring({ frame, fps, config: { damping: 20 } });
  const fadeOutStart = durationInFrames - 8;
  const fadeOut = interpolate(frame, [fadeOutStart, durationInFrames], [1, 0.3], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ background: "#0F172A" }}>
      <OffthreadVideo
        src={resolveAsset(src)}
        startFrom={Math.round(startFrom * fps)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          opacity: fadeIn * fadeOut,
        }}
        muted
      />
      <Vignette />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
// Scene renderer — maps cut type / source to the right component
// ---------------------------------------------------------------------------

// Background image layer — renders an AI-generated/stock image behind data components
const BackgroundImageLayer: React.FC<{
  src: string;
  overlayOpacity?: number;
  children: React.ReactNode;
}> = ({ src, overlayOpacity = 0.55, children }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Subtle ken-burns on the background
  const progress = interpolate(frame, [0, durationInFrames], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const bgScale = 1 + progress * 0.08;

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      {/* Background image with subtle zoom */}
      <Img
        src={resolveAsset(src)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${bgScale})`,
          willChange: "transform",
        }}
      />
      {/* Dark overlay for readability */}
      <AbsoluteFill
        style={{
          background: `rgba(15, 23, 42, ${overlayOpacity})`,
        }}
      />
      {/* Component content on top */}
      {children}
    </AbsoluteFill>
  );
};

// Background video layer — plays a looping video behind component content with dark overlay
const BackgroundVideoLayer: React.FC<{
  src: string;
  startFrom?: number;
  overlayOpacity?: number;
  children: React.ReactNode;
}> = ({ src, startFrom = 0, overlayOpacity = 0.55, children }) => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      {/* Background video */}
      <OffthreadVideo
        src={resolveAsset(src)}
        startFrom={Math.round(startFrom * fps)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
        }}
        muted
      />
      {/* Dark overlay for readability */}
      <AbsoluteFill
        style={{
          background: `rgba(15, 23, 42, ${overlayOpacity})`,
        }}
      />
      {/* Component content on top */}
      {children}
    </AbsoluteFill>
  );
};

const SceneRenderer: React.FC<{ cut: Cut; theme: ThemeConfig }> = ({ cut, theme }) => {
  // Wrap component with background video or image if specified
  const maybeWrapWithBg = (element: React.ReactElement) => {
    if (cut.backgroundVideo) {
      return (
        <BackgroundVideoLayer
          src={cut.backgroundVideo}
          startFrom={cut.backgroundVideoStart ?? 0}
          overlayOpacity={cut.backgroundOverlay ?? 0.55}
        >
          {element}
        </BackgroundVideoLayer>
      );
    }
    if (cut.backgroundImage) {
      return (
        <BackgroundImageLayer
          src={cut.backgroundImage}
          overlayOpacity={cut.backgroundOverlay ?? 0.55}
        >
          {element}
        </BackgroundImageLayer>
      );
    }
    return element;
  };

  // Resolve the scene element based on cut type, then wrap with backgroundImage if set
  // Use transparent bg so the animated gradient background shows through
  // When no explicit backgroundColor on the cut, inherit from theme
  const rawBg = (cut.backgroundImage || cut.backgroundVideo) ? "transparent" : (cut.backgroundColor || theme.surfaceColor);
  const bgColor = (rawBg === theme.backgroundColor || rawBg === "#0F172A" || rawBg === "#0f172a") ? "transparent" : rawBg;
  const textColor = cut.color || theme.textColor;
  const accent = cut.accentColor || theme.accentColor;

  // Explicit component types — use theme-derived defaults for colors
  if (cut.type === "text_card" && cut.text) {
    return maybeWrapWithBg(
      <TextCard text={cut.text} fontSize={cut.fontSize} color={textColor} backgroundColor={bgColor} />
    );
  }
  if (cut.type === "stat_card" && cut.stat) {
    return maybeWrapWithBg(
      <StatCard stat={cut.stat} subtitle={cut.subtitle} accentColor={accent} backgroundColor={bgColor} />
    );
  }
  if (cut.type === "callout" && cut.text) {
    return maybeWrapWithBg(
      <CalloutBox
        text={cut.text} type={cut.callout_type} title={cut.title}
        borderColor={accent} backgroundColor={cut.backgroundColor || theme.surfaceColor}
        textColor={textColor} containerBackgroundColor={bgColor}
      />
    );
  }
  if (cut.type === "comparison" && cut.leftLabel && cut.rightLabel && cut.leftValue && cut.rightValue) {
    return maybeWrapWithBg(
      <ComparisonCard
        leftLabel={cut.leftLabel} rightLabel={cut.rightLabel}
        leftValue={cut.leftValue} rightValue={cut.rightValue}
        title={cut.title} backgroundColor={bgColor} textColor={textColor}
      />
    );
  }
  if (cut.type === "hero_title" && cut.text) {
    return maybeWrapWithBg(
      <HeroTitle title={cut.text} subtitle={cut.heroSubtitle || cut.subtitle} />
    );
  }
  if (cut.type === "terminal_scene" && cut.steps) {
    return maybeWrapWithBg(
      <TerminalScene
        title={cut.terminalTitle || "Terminal"}
        steps={cut.steps as TerminalStep[]}
        prompt={cut.prompt}
        accentColor={accent}
        backgroundColor={bgColor || theme.backgroundColor}
      />
    );
  }
  if (cut.type === "screenshot_scene" && cut.backgroundImage && cut.screenshotSteps) {
    return (
      <ScreenshotScene
        backgroundImage={cut.backgroundImage}
        backgroundSize={cut.screenshotSize}
        steps={cut.screenshotSteps as ScreenshotStep[]}
        accentColor={accent}
        cursorStartAt={cut.cursorStartAt}
      />
    );
  }

  // --- Yafho SiliSkin components ---
  if (cut.type === "skin_cross_section") {
    return <SkinCrossSection phase={cut.phase} labels={cut.crossLabels} introFade={cut.introFade} />;
  }
  if (cut.type === "skin_cross_section_3d") {
    return (
      <SkinCrossSection3D
        phase={cut.phase}
        labels={cut.crossLabels}
        introFade={cut.introFade}
        focusX={cut.focusX}
        centerY={cut.centerY}
        fitFrac={cut.fitFrac}
        progressFrom={cut.progressFrom}
        progressTo={cut.progressTo}
      />
    );
  }
  if (cut.type === "blank") {
    // nothing — the brand backdrop shows through (used under audience chips)
    return <AbsoluteFill />;
  }
  if (cut.type === "scar_compare") {
    return (
      <ScarCompare
        progressFrom={cut.progressFrom}
        progressTo={cut.progressTo}
        introFade={cut.introFade}
        areaTop={cut.areaTop}
        areaBottom={cut.areaBottom}
      />
    );
  }
  if (cut.type === "skin_demo") {
    return (
      <SkinSwatch
        shape={cut.skinShape}
        step={cut.skinStep}
        state={cut.skinState}
        from={cut.skinFrom}
        progressFrom={cut.progressFrom}
        progressTo={cut.progressTo}
        months={cut.months}
        reveal={cut.reveal}
        land={cut.land}
        soften={cut.soften}
        zoom={cut.zoom}
        introFade={cut.introFade}
        areaTop={cut.areaTop}
        areaBottom={cut.areaBottom}
      />
    );
  }
  if (cut.type === "patch_3d") {
    return <PatchHero3D motion={cut.motion} centerY={cut.centerY} size={cut.size} introFade={cut.introFade} />;
  }
  if (cut.type === "result_curve") {
    return <ResultCurve months={cut.months} milestones={cut.milestones} areaTop={cut.areaTop} areaBottom={cut.areaBottom} />;
  }
  if (cut.type === "myth_fact" && cut.myth && cut.fact) {
    return <MythFact myth={cut.myth} fact={cut.fact} counter={cut.counter} variant={cut.mythVariant} />;
  }
  if (cut.type === "check_list" && cut.checkItems) {
    return <CheckList title={cut.title} items={cut.checkItems} note={cut.checkNote} />;
  }
  if (cut.type === "day_clock") {
    return <DayClock items={cut.clockItems} start={cut.clockStart} summary={cut.clockSummary} summaryNote={cut.clockSummaryNote} />;
  }
  if (cut.type === "size_guide") {
    return <SizeGuide items={cut.sizeItems} />;
  }
  if (cut.type === "end_card") {
    return (
      <EndCard
        logoSrc={cut.logoSrc ? resolveAsset(cut.logoSrc) : undefined}
        brand={cut.brand}
        tagline={cut.tagline}
        handle={cut.handle}
        qr={cut.qr}
        qrCaption={cut.qrCaption}
        cta={cut.cta}
        patch3d={cut.patch3d}
      />
    );
  }

  // --- Chart types — use theme.chartColors as default palette ---
  if (cut.type === "bar_chart" && cut.chartData) {
    return maybeWrapWithBg(
      <BarChart
        data={cut.chartData} title={cut.title} colors={cut.chartColors || theme.chartColors}
        animationStyle={(cut.chartAnimation as any) || "grow-up"}
        showGrid={cut.showGrid} showValues={cut.showValues} backgroundColor={bgColor}
      />
    );
  }
  if (cut.type === "line_chart" && cut.chartSeries) {
    return maybeWrapWithBg(
      <LineChart
        series={cut.chartSeries} title={cut.title} colors={cut.chartColors || theme.chartColors}
        animationStyle={(cut.chartAnimation as any) || "draw"}
        showGrid={cut.showGrid} showMarkers={cut.showMarkers} showLegend={cut.showLegend}
        xLabel={cut.xLabel} yLabel={cut.yLabel} backgroundColor={bgColor}
      />
    );
  }
  if (cut.type === "pie_chart" && cut.chartData) {
    return maybeWrapWithBg(
      <PieChart
        data={cut.chartData} title={cut.title} colors={cut.chartColors || theme.chartColors}
        animationStyle={(cut.chartAnimation as any) || "expand"}
        donut={cut.donut} centerLabel={cut.centerLabel} centerValue={cut.centerValue}
        showLegend={cut.showLegend} backgroundColor={bgColor}
      />
    );
  }
  if (cut.type === "kpi_grid" && cut.chartData) {
    return maybeWrapWithBg(
      <KPIGrid
        metrics={cut.chartData} title={cut.title} columns={cut.columns}
        colors={cut.chartColors || theme.chartColors} animationStyle={(cut.chartAnimation as any) || "count-up"}
        backgroundColor={bgColor}
      />
    );
  }
  if (cut.type === "progress_bar" && cut.progress !== undefined) {
    return maybeWrapWithBg(
      <AbsoluteFill
        style={{
          background: bgColor || theme.surfaceColor,
          display: "flex", alignItems: "center", justifyContent: "center",
          padding: "80px 120px",
        }}
      >
        {cut.title && (
          <div style={{
            position: "absolute", top: 120, fontSize: 48, fontWeight: 700,
            color: textColor, textAlign: "center", width: "100%",
          }}>
            {cut.title}
          </div>
        )}
        <ProgressBar
          progress={cut.progress} label={cut.progressLabel}
          color={cut.progressColor || accent}
          animationStyle={(cut.progressAnimation as any) || "fill"}
          segments={cut.progressSegments} backgroundColor={cut.backgroundColor || theme.surfaceColor}
        />
      </AbsoluteFill>
    );
  }

  // --- Anime scene (multi-image crossfade + particles) ---
  if (cut.type === "anime_scene" && cut.images && cut.images.length > 0) {
    return (
      <AnimeScene
        images={cut.images}
        animation={(cut.animation as CameraMotion) || "ken-burns"}
        particles={cut.particles}
        particleColor={cut.particleColor}
        particleCount={cut.particleCount}
        particleIntensity={cut.particleIntensity}
        backgroundColor={cut.backgroundColor}
        vignette={cut.vignette ?? true}
        lightingFrom={cut.lightingFrom}
        lightingTo={cut.lightingTo}
        sceneDurationSeconds={cut.out_seconds - cut.in_seconds}
      />
    );
  }

  // --- Media types (image / video fallback) ---
  const animation = cut.animation || cut.transform?.animation;

  if (cut.source && isImage(cut.source)) {
    return maybeWrapWithBg(<ImageScene src={cut.source} animation={animation} flat={theme.flat} introFade={cut.introFade !== false} />);
  }

  if (cut.source && isVideo(cut.source)) {
    return maybeWrapWithBg(
      <VideoScene src={cut.source} startFrom={cut.source_in_seconds ?? 0} flat={theme.flat} playbackRate={cut.playbackRate} />,
    );
  }

  // Final fallback — try as image if source exists, otherwise show text_card
  if (cut.source) {
    return maybeWrapWithBg(<ImageScene src={cut.source} animation={animation} flat={theme.flat} introFade={cut.introFade !== false} />);
  }

  // No source, no type — render as text card with cut id as fallback
  return <TextCard text={cut.text || cut.id} color={textColor} backgroundColor={bgColor} />;
};

// "Dive" exit: the shot pushes in, softens and fades to the background so the
// next scene (which fades in from the same background) reads as going inside.
const ExitZoom: React.FC<{ seconds: number; children: React.ReactNode }> = ({ seconds, children }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const start = durationInFrames - seconds * fps;
  const p = interpolate(frame, [start, durationInFrames], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const e = p * p;
  return (
    <AbsoluteFill style={{ transform: `scale(${1 + 0.6 * e})`, filter: `blur(${8 * e}px)`, opacity: 1 - 0.85 * e }}>
      {children}
    </AbsoluteFill>
  );
};

const CutScene: React.FC<{ cut: Cut; theme: ThemeConfig }> = ({ cut, theme }) =>
  cut.exitZoom ? (
    <ExitZoom seconds={cut.exitZoom}>
      <SceneRenderer cut={cut} theme={theme} />
    </ExitZoom>
  ) : (
    <SceneRenderer cut={cut} theme={theme} />
  );

// ---------------------------------------------------------------------------
// Overlay renderer
// ---------------------------------------------------------------------------

const OverlayRenderer: React.FC<{ overlay: Overlay; inPanel?: boolean }> = ({ overlay, inPanel }) => {
  if (overlay.type === "thesis" && overlay.text) {
    return (
      <ThesisTitle
        text={overlay.text}
        variant={overlay.variant}
        placement={inPanel ? "panel" : ((overlay.position as any) || "bottom")}
        fontSize={inPanel ? undefined : overlay.fontSize}
        note={overlay.subtitle}
      />
    );
  }
  if (overlay.type === "margin_overlay") {
    return <MarginOverlay scarBox={overlay.scarBox} marginPx={overlay.marginPx} label={overlay.label} />;
  }
  if (overlay.type === "healing_timeline") {
    return (
      <HealingTimeline
        from={overlay.from}
        to={overlay.to}
        highlightWindow={overlay.highlightWindow}
        ticks={overlay.ticks}
        emphasis={overlay.emphasis}
        inPanel={inPanel}
      />
    );
  }
  if (overlay.type === "audience_chips" && overlay.chips) {
    return <AudienceChips title={overlay.text} chips={overlay.chips} />;
  }
  if (overlay.type === "stat_badge" && overlay.value && overlay.source) {
    return (
      <StatBadge
        value={overlay.value}
        label={overlay.label ?? ""}
        source={overlay.source}
        position={(overlay.position as any) || "upper"}
        inPanel={inPanel}
      />
    );
  }
  if (overlay.type === "animatic_note" && overlay.label) {
    return <AnimaticNote label={overlay.label} text={overlay.text} />;
  }
  if (overlay.type === "time_counter") {
    return <TimeCounter labels={overlay.labels} placement={(overlay.position as any) || "top"} />;
  }
  if (overlay.type === "section_title") {
    return (
      <SectionTitle
        title={overlay.text}
        subtitle={overlay.subtitle}
        accentColor={overlay.accentColor}
        position={(overlay.position as any) || "top-left"}
      />
    );
  }
  if (overlay.type === "stat_reveal") {
    return (
      <StatReveal
        stat={overlay.text}
        label={overlay.subtitle}
        accentColor={overlay.accentColor}
        position={(overlay.position as any) || "bottom-right"}
      />
    );
  }
  if (overlay.type === "hero_title") {
    return <HeroTitle title={overlay.text} subtitle={overlay.subtitle} />;
  }
  if (overlay.type === "provider_chip" && overlay.providers) {
    return (
      <ProviderChip
        providers={overlay.providers as string[]}
        cycleSeconds={overlay.cycleSeconds}
        position={(overlay.position as any) || "bottom-right"}
        accentColor={overlay.accentColor}
        label={overlay.label}
      />
    );
  }
  return null;
};

// ---------------------------------------------------------------------------
// Main composition
// ---------------------------------------------------------------------------

export const Explainer: React.FC<ExplainerProps> = (props) => {
  const { cuts, overlays, captions, audio } = props;
  const { fps, durationInFrames, width, height } = useVideoConfig();

  // Resolve theme from props — playbook name, theme name, or custom themeConfig
  const theme = resolveTheme(props as Record<string, unknown>);
  const layout = props.layout === "split" ? "split" : "full";
  const visibleOverlays = (overlays ?? []).filter((o) => !o.layouts || o.layouts.includes(layout));
  // In split layout thesis titles leave the video panel for the side panel.
  const panelOverlays = layout === "split" && props.splitPanel !== "center" ? visibleOverlays.filter((o) => o.type === "thesis" || o.type === "healing_timeline" || o.type === "stat_badge") : [];
  const canvasOverlays = visibleOverlays.filter((o) => !panelOverlays.includes(o));

  const renderOverlay = (overlay: Overlay, i: number, inPanel = false) => {
    const from = Math.round(overlay.in_seconds * fps);
    const duration = Math.round((overlay.out_seconds - overlay.in_seconds) * fps);
    return (
      <Sequence key={`overlay-${i}`} from={from} durationInFrames={duration}>
        <OverlayRenderer overlay={overlay} inPanel={inPanel} />
      </Sequence>
    );
  };

  // In split layout, 3D scenes use the full 16:9 frame (left of the text panel)
  // instead of the narrow vertical panel.
  const isBleed = (cut: Cut) => layout === "split" && cut.type === "skin_cross_section_3d";
  const renderCut = (cut: Cut) => {
    const from = Math.round(cut.in_seconds * fps);
    const duration = Math.round((cut.out_seconds - cut.in_seconds) * fps);
    return (
      <Sequence key={cut.id} from={from} durationInFrames={duration}>
        <CutScene cut={cut} theme={theme} />
      </Sequence>
    );
  };

  const scenes = (
    <>
      {/* Layer 1: Visual scenes */}
      {cuts.filter((cut) => !isBleed(cut)).map((cut) => {
        const from = Math.round(cut.in_seconds * fps);
        const duration = Math.round((cut.out_seconds - cut.in_seconds) * fps);

        return (
          <Sequence key={cut.id} from={from} durationInFrames={duration}>
            <CutScene cut={cut} theme={theme} />
          </Sequence>
        );
      })}

      {/* Layer 2: Overlays (section titles, stat reveals, hero titles) */}
      {canvasOverlays.map((overlay, i) => renderOverlay(overlay, i))}
    </>
  );

  // 16:9 split: a 1080x1920 design canvas scaled into a vertical panel.
  const panelScale = height / 1920;
  const panelW = 1080 * panelScale;
  const panelLeft = props.splitPanel === "center" ? (width - panelW) / 2 : Math.round(width * 0.08);
  const textLeft = panelLeft + panelW + Math.round(width * 0.06);

  return (
    <AbsoluteFill style={{ background: theme.backgroundColor, fontFamily: theme.headingFont || fontFamily }}>
      {/* Layer 0: Animated gradient background — driven by theme (flat themes skip it) */}
      {!theme.flat && <AnimatedBackground theme={theme} />}
      {props.backdrop?.color && <AbsoluteFill style={{ background: props.backdrop.color }} />}
      {props.backdrop?.image && (
        <AbsoluteFill>
          <Img src={resolveAsset(props.backdrop.image)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
        </AbsoluteFill>
      )}

      {layout === "split" ? (
        <>
          {/* soft fade before the text panel so close-ups never run under the copy */}
          <AbsoluteFill
            style={{
              maskImage: `linear-gradient(to right, #000 ${textLeft - 160}px, transparent ${textLeft - 30}px)`,
              WebkitMaskImage: `linear-gradient(to right, #000 ${textLeft - 160}px, transparent ${textLeft - 30}px)`,
            }}
          >
            {cuts
              .filter(isBleed)
              .map((cut) => renderCut({ ...cut, focusX: (textLeft * 0.5) / width, fitFrac: (textLeft * 0.9) / width, centerY: 0.5 }))}
          </AbsoluteFill>
          <div style={{ position: "absolute", left: panelLeft, top: 0, width: panelW, height, overflow: "hidden" }}>
            <div style={{ position: "relative", width: 1080, height: 1920, transform: `scale(${panelScale})`, transformOrigin: "0 0" }}>
              <CanvasContext.Provider value={{ width: 1080, height: 1920 }}>{scenes}</CanvasContext.Provider>
            </div>
          </div>
          {panelOverlays.length > 0 && (
            <div style={{ position: "absolute", left: textLeft, right: Math.round(width * 0.06), top: 0, bottom: 0 }}>
              {panelOverlays.map((overlay, i) => renderOverlay(overlay, i, true))}
            </div>
          )}
        </>
      ) : (
        scenes
      )}

      {/* Layer 3: Captions (word-by-word highlight) */}
      {captions && captions.length > 0 && (
        <CaptionOverlay
          words={captions}
          wordsPerPage={6}
          fontSize={42}
          highlightColor={theme.captionHighlightColor}
          backgroundColor={theme.captionBackgroundColor}
        />
      )}

      {/* Layer 4: Audio — narration */}
      {audio?.narration?.src && (
        <Audio src={resolveAsset(audio.narration.src)} volume={audio.narration.volume ?? 1} />
      )}

      {/* Layer 4: Audio — music with offset, fade in/out, and optional loop */}
      {audio?.music?.src && (
        <Audio
          src={resolveAsset(audio.music.src)}
          startFrom={Math.round((audio.music.offsetSeconds ?? 0) * fps)}
          loop={audio.music.loop ?? false}
          loopVolumeCurveBehavior="repeat"
          volume={(f) => {
            const baseVol = audio.music!.volume ?? 0.1;
            const fadeInDur = (audio.music!.fadeInSeconds ?? 2) * fps;
            const fadeOutDur = (audio.music!.fadeOutSeconds ?? 3) * fps;
            const totalFrames = durationInFrames;

            // Fade in
            const fadeIn = interpolate(f, [0, fadeInDur], [0, baseVol], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            });
            // Fade out
            const fadeOut = interpolate(
              f,
              [totalFrames - fadeOutDur, totalFrames],
              [baseVol, 0],
              { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
            );
            return Math.min(fadeIn, fadeOut);
          }}
        />
      )}
    </AbsoluteFill>
  );
};
