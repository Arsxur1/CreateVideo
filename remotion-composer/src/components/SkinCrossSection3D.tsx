import { useMemo } from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import { useThree } from "@react-three/fiber";
import * as THREE from "three";
import { RoomEnvironment } from "three/examples/jsm/environments/RoomEnvironment.js";
import { YAFHO, ease, useCanvas } from "./yafho/tokens";
import type { SkinCrossSectionLabels, SkinPhase } from "./SkinCrossSection";

/**
 * Story phases (hero v2, continuous from one to the next):
 *   dive → closing → patch → months → drying → alarm → freeze … seal → healed
 * plus the hero v1 pair scar → sealed.
 */
export type Skin3DPhase =
  | SkinPhase
  | "dive" | "closing" | "patch" | "months" | "drying" | "alarm" | "freeze" | "seal"
  // effect comparison: the same young scar over ~6 months, without care / with a sheet
  | "untreated" | "treated";

export type Skin3DLabels = SkinCrossSectionLabels & { fibroblast?: string; signalUp?: string; moistureOut?: string };

export interface SkinCrossSection3DProps {
  phase?: Skin3DPhase;
  labels?: Skin3DLabels;
  introFade?: boolean;
  /** Where the block's centre sits, as fractions of the canvas (leave room for a thesis). */
  focusX?: number;
  centerY?: number;
  /** Fraction of canvas width the whole block spans in the wide establishing pose. */
  fitFrac?: number;
  /** Film grain + vignette. */
  grade?: boolean;
  /** Map the cut onto a slice of the phase timeline (e.g. 1 → 1 holds the end state). */
  progressFrom?: number;
  progressTo?: number;
}

const DEFAULT_LABELS: Skin3DLabels = {
  epidermis: "эпидермис",
  dermis: "дерма",
  collagen: "коллаген",
  moisture: "влага ↑",
  signal: "сигнал ↓",
  signalUp: "сигнал ↑",
  fibroblast: "фибробласт",
  moistureOut: "влага уходит",
};

// ---------------------------------------------------------------------------
// Geometry constants (world units). Block spans x ±3.5, z ±1.5; skin top at y=0.
// ---------------------------------------------------------------------------
const HALF_W = 3.5;
const DEPTH = 3;
const FRONT_Z = DEPTH / 2;
const EPI = 0.22;
const DERMIS_BOTTOM = -1.9;
const FAT_BOTTOM = -2.7;
const BUMP_HALF = 1.35;
const BUMP_H = 0.34;
const N_FIBRES = 26; // base scar collagen
const N_EXTRA = 14; // extra collagen laid down on the "alarm" signal
const N_ALL = N_FIBRES + N_EXTRA;
const SLIT_BOTTOM = -1.0; // depth of the (bloodless) incision groove
const SHEET_HALF = 1.65;
const SHEET_T = 0.09;

// Light olive skin (TZ hand model), anatomical cut colours.
const COLORS = {
  skinTop: "#C9946F",
  epiCut: "#A8664B",
  dermisCut: "#E3A890",
  fatCut: "#EBD29C",
  scar: "#B04A3A",
  normalFibre: "#CF8C73",
};

const smooth = Easing.bezier(0.45, 0, 0.2, 1); // slow-in, long settle

function bumpShape(x: number): number {
  if (Math.abs(x) >= BUMP_HALF) return 0;
  return 0.5 * (1 + Math.cos((Math.PI * x) / BUMP_HALF));
}

function mulberry32(seed: number) {
  return () => {
    seed |= 0;
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

type V3 = [number, number, number];

const rnd = mulberry32(20261006);
const CHAOTIC: V3[][] = Array.from({ length: N_ALL }, () => {
  const cx = (rnd() - 0.5) * 2.2;
  const cy = -0.45 - rnd() * 1.2;
  const a = rnd() * Math.PI;
  const len = 0.8 + rnd() * 0.7;
  const dx = Math.cos(a), dy = Math.sin(a);
  return [0, 1, 2, 3].map((k) => {
    const t = k / 3 - 0.5;
    const wob = k === 1 || k === 2 ? (rnd() - 0.5) * 0.6 : 0;
    return [cx + dx * len * t - dy * wob, cy + dy * len * t + dx * wob, FRONT_Z - 0.02 + rnd() * 0.03] as V3;
  });
});
// Healed: long, staggered, gently wavy fibres running parallel to the surface.
const rndA = mulberry32(424242);
const ALIGNED: V3[][] = Array.from({ length: N_ALL }, (_, i) => {
  const y = -0.42 - (i / (N_ALL - 1)) * 1.3 + (rndA() - 0.5) * 0.05;
  const len = 1.3 + rndA() * 1.0;
  const x0 = -1.35 + rndA() * (2.7 - len);
  const amp = 0.02 + rndA() * 0.03;
  return [0, 1, 2, 3].map((k) => [x0 + (k * len) / 3, y + (k === 1 ? amp : k === 2 ? -amp : 0), FRONT_Z - 0.005] as V3);
});
const FIBRE_R = Array.from({ length: N_ALL }, () => 0.032 + rnd() * 0.014);
const CELLS: V3[] = [
  [-0.75, -0.75, FRONT_Z],
  [0.55, -0.6, FRONT_Z],
  [0.05, -1.15, FRONT_Z],
  [0.85, -1.45, FRONT_Z],
  [-0.6, -1.5, FRONT_Z],
];
// Fibroblasts wait in the healthy dermis and migrate into the wound ("patch").
const CELL_HOME: V3[] = CELLS.map(([x, y, z], i) => [(i % 2 ? 1 : -1) * (2.1 + (i % 3) * 0.35), y, z]);
// Pale first-responder cells drawn to the closing incision (no blood).
const rndG = mulberry32(777);
const GATHER = Array.from({ length: 22 }, () => ({
  from: [(rndG() - 0.5) * 4.6, -0.2 - rndG() * 1.3, FRONT_Z - 0.01] as V3,
  to: [(rndG() - 0.5) * 0.16, -0.08 - rndG() * 0.85, FRONT_Z + 0.005] as V3,
  r: 0.035 + rndG() * 0.025,
  delay: rndG() * 0.35,
}));
const FAT_LOBULES = Array.from({ length: 18 }, (_, i) => ({
  x: -HALF_W + 0.25 + i * 0.39,
  y: -2.1 - (i % 3) * 0.2,
  r: 0.15 + (i % 4) * 0.03,
}));
const DROPLETS = Array.from({ length: 60 }, () => ({
  x: (rnd() - 0.5) * 2.8,
  z: (rnd() - 0.5) * 2.0,
  r: 0.018 + rnd() * 0.03,
  t: rnd(),
}));

// ---------------------------------------------------------------------------
// Procedural textures (deterministic canvas → texture)
// ---------------------------------------------------------------------------
function canvasTexture(size: number, draw: (g: CanvasRenderingContext2D, r: () => number) => void, seed: number) {
  const c = document.createElement("canvas");
  c.width = c.height = size;
  draw(c.getContext("2d")!, mulberry32(seed));
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  return t;
}

const makeSkinBump = () =>
  canvasTexture(
    512,
    (g, r) => {
      g.fillStyle = "#808080";
      g.fillRect(0, 0, 512, 512);
      for (let i = 0; i < 3200; i++) {
        const v = Math.floor(80 + r() * 90);
        g.fillStyle = `rgba(${v},${v},${v},0.55)`;
        g.beginPath();
        g.arc(r() * 512, r() * 512, 0.6 + r() * 1.5, 0, Math.PI * 2);
        g.fill();
      }
      g.strokeStyle = "rgba(55,55,55,0.28)";
      for (let i = 0; i < 90; i++) {
        g.lineWidth = 0.5 + r();
        g.beginPath();
        const x = r() * 512, y = r() * 512;
        g.moveTo(x, y);
        g.lineTo(x + (r() - 0.5) * 100, y + (r() - 0.5) * 30);
        g.stroke();
      }
    },
    7,
  );

const makeSkinColor = () => {
  const t = canvasTexture(
    512,
    (g, r) => {
      g.fillStyle = COLORS.skinTop;
      g.fillRect(0, 0, 512, 512);
      for (let i = 0; i < 260; i++) {
        const warm = r() > 0.5;
        g.fillStyle = warm ? `rgba(180,95,70,${0.04 + r() * 0.05})` : `rgba(235,200,170,${0.04 + r() * 0.05})`;
        g.beginPath();
        g.arc(r() * 512, r() * 512, 10 + r() * 40, 0, Math.PI * 2);
        g.fill();
      }
    },
    13,
  );
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
};

const makeDermisTexture = () => {
  const t = canvasTexture(
    512,
    (g, r) => {
      g.fillStyle = COLORS.dermisCut;
      g.fillRect(0, 0, 512, 512);
      g.strokeStyle = "rgba(160,85,65,0.3)";
      for (let row = 0; row < 40; row++) {
        g.lineWidth = 2 + r() * 2;
        g.beginPath();
        const y = row * 13 + r() * 6;
        g.moveTo(0, y);
        for (let x = 0; x <= 512; x += 32) g.lineTo(x, y + Math.sin(x / 40 + row) * 4);
        g.stroke();
      }
    },
    11,
  );
  t.colorSpace = THREE.SRGBColorSpace;
  t.repeat.set(0.35, 0.35);
  return t;
};

// Fine striations along each collagen tube (u runs along the tube).
const makeFibreBump = () => {
  const t = canvasTexture(
    256,
    (g, r) => {
      g.fillStyle = "#808080";
      g.fillRect(0, 0, 256, 256);
      for (let i = 0; i < 40; i++) {
        const v = Math.floor(60 + r() * 120);
        g.fillStyle = `rgb(${v},${v},${v})`;
        g.fillRect(0, r() * 256, 256, 1 + r() * 3);
      }
    },
    21,
  );
  t.repeat.set(6, 1);
  return t;
};

const makeGelBump = () => {
  const t = canvasTexture(
    256,
    (g, r) => {
      g.fillStyle = "#808080";
      g.fillRect(0, 0, 256, 256);
      for (let i = 0; i < 1400; i++) {
        const v = Math.floor(100 + r() * 60);
        g.fillStyle = `rgba(${v},${v},${v},0.5)`;
        g.fillRect(r() * 256, r() * 256, 1.5, 1.5);
      }
    },
    31,
  );
  t.repeat.set(3, 3);
  return t;
};

// ---------------------------------------------------------------------------
// Profile (x,y) extruded along z. Caps (material 0) = cut faces; walls (1) = outside.
// ---------------------------------------------------------------------------
function profileGeometry(
  x0: number,
  x1: number,
  top: (x: number) => number,
  bottom: (x: number) => number,
  depth: number,
  zFront: number,
  bevel?: THREE.ExtrudeGeometryOptions,
): THREE.ExtrudeGeometry {
  const s = new THREE.Shape();
  const N = 90;
  for (let i = 0; i <= N; i++) {
    const x = x0 + ((x1 - x0) * i) / N;
    if (i === 0) s.moveTo(x, top(x));
    else s.lineTo(x, top(x));
  }
  for (let i = N; i >= 0; i--) {
    const x = x0 + ((x1 - x0) * i) / N;
    s.lineTo(x, bottom(x));
  }
  s.closePath();
  const geo = new THREE.ExtrudeGeometry(s, { depth, bevelEnabled: false, steps: 1, curveSegments: 1, ...bevel });
  geo.translate(0, 0, zFront - depth);
  geo.computeVertexNormals();
  return geo;
}

/** Layer slab with a V-groove (healing incision) of half-width `g` at the surface. */
function slitGeometry(yTop: number, yBot: number, g: number): THREE.ExtrudeGeometry {
  const half = (y: number) => (y >= SLIT_BOTTOM ? (g * (y - SLIT_BOTTOM)) / -SLIT_BOTTOM : 0);
  const shapes: THREE.Shape[] = [];
  if (yBot >= SLIT_BOTTOM) {
    // groove cuts through the whole layer → two pieces
    for (const side of [-1, 1]) {
      const sh = new THREE.Shape();
      sh.moveTo(side * HALF_W, yTop);
      sh.lineTo(side * half(yTop), yTop);
      sh.lineTo(side * half(yBot), yBot);
      sh.lineTo(side * HALF_W, yBot);
      sh.closePath();
      shapes.push(sh);
    }
  } else {
    const sh = new THREE.Shape();
    sh.moveTo(-HALF_W, yTop);
    sh.lineTo(-half(yTop), yTop);
    sh.lineTo(0, SLIT_BOTTOM);
    sh.lineTo(half(yTop), yTop);
    sh.lineTo(HALF_W, yTop);
    sh.lineTo(HALF_W, yBot);
    sh.lineTo(-HALF_W, yBot);
    sh.closePath();
    shapes.push(sh);
  }
  const geo = new THREE.ExtrudeGeometry(shapes, { depth: DEPTH, bevelEnabled: false, steps: 1, curveSegments: 1 });
  geo.translate(0, 0, FRONT_Z - DEPTH);
  geo.computeVertexNormals();
  return geo;
}

const Environment: React.FC = () => {
  const { gl, scene } = useThree();
  useMemo(() => {
    const pmrem = new THREE.PMREMGenerator(gl);
    scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
    scene.environmentIntensity = 0.35;
    scene.background = new THREE.Color(YAFHO.offWhite);
    scene.backgroundIntensity = 1;
    gl.toneMapping = THREE.ACESFilmicToneMapping;
    gl.toneMappingExposure = 0.95;
    gl.shadowMap.enabled = true;
    gl.shadowMap.type = THREE.PCFSoftShadowMap;
  }, [gl, scene]);
  return null;
};

// ---------------------------------------------------------------------------
// Camera: directed keyframed shots, eased, continuous from H02 into H03.
// ---------------------------------------------------------------------------
interface Pose {
  az: number; // degrees, 0 = straight at the cut face
  el: number; // degrees above horizon
  zoom: number; // distance multiplier vs. the wide fit
  target: V3;
}

const WIDE: Pose = { az: -26, el: 20, zoom: 1, target: [0, -1.05, 0.2] };

const P_TOP: Pose = { az: -20, el: 76, zoom: 0.4, target: [0, 0, 0.4] };
const P_REVEAL: Pose = { az: -30, el: 26, zoom: 0.84, target: [0, -0.6, 0.3] };
const P_SLIT: Pose = { az: -18, el: 20, zoom: 0.62, target: [0, -0.45, 0.7] };
const P_PATCH: Pose = { az: -8, el: 18, zoom: 0.72, target: [0, -0.85, 0.7] };
const P_DRY: Pose = { az: -38, el: 30, zoom: 0.62, target: [0, 0.05, 0.1] };
const P_ALARM: Pose = { az: -12, el: 14, zoom: 0.68, target: [0, -0.9, 0.7] };
const P_FREEZE: Pose = { az: -22, el: 22, zoom: 1.2, target: [0, -1.05, 0.2] };

const SHOTS: Record<Skin3DPhase, { at: number; pose: Pose }[]> = {
  dive: [
    { at: 0, pose: P_TOP },
    { at: 1, pose: P_REVEAL },
  ],
  closing: [
    { at: 0, pose: P_REVEAL },
    { at: 1, pose: P_SLIT },
  ],
  patch: [
    { at: 0, pose: P_SLIT },
    { at: 1, pose: P_PATCH },
  ],
  months: [
    { at: 0, pose: P_PATCH },
    { at: 1, pose: WIDE },
  ],
  drying: [
    { at: 0, pose: WIDE },
    { at: 1, pose: P_DRY },
  ],
  alarm: [
    { at: 0, pose: P_DRY },
    { at: 1, pose: P_ALARM },
  ],
  freeze: [
    { at: 0, pose: P_ALARM },
    { at: 1, pose: P_FREEZE },
  ],
  // Macro glide over the skin to the raised scar, then crane down to reveal the cut.
  scar: [
    { at: 0, pose: { az: -58, el: 38, zoom: 0.52, target: [-0.3, 0.05, -0.1] } },
    { at: 0.38, pose: { az: -46, el: 32, zoom: 0.6, target: [0, 0.0, 0.2] } },
    { at: 0.82, pose: WIDE },
    { at: 1, pose: { ...WIDE, az: -23, zoom: 0.96 } },
  ],
  // Rise to watch the sheet land, then arc in on the collagen as it settles.
  sealed: [
    { at: 0, pose: { ...WIDE, az: -23, zoom: 0.96 } },
    { at: 0.3, pose: { az: -20, el: 30, zoom: 0.9, target: [0, -0.6, 0.2] } },
    { at: 0.55, pose: { az: -13, el: 20, zoom: 0.8, target: [0, -0.85, 0.55] } },
    { at: 1, pose: { az: -7, el: 17, zoom: 0.72, target: [0, -0.85, 0.75] } },
  ],
  healed: [
    { at: 0, pose: { az: -14, el: 16, zoom: 0.8, target: [0, -0.9, 0.4] } },
    { at: 1, pose: { az: -24, el: 22, zoom: 0.92, target: [0, -0.9, 0.2] } },
  ],
  seal: [],
  untreated: [
    { at: 0, pose: { az: -20, el: 26, zoom: 0.74, target: [0, -0.65, 0.4] } },
    { at: 1, pose: { az: -15, el: 23, zoom: 0.68, target: [0, -0.65, 0.4] } },
  ],
  treated: [],
};
SHOTS.seal = SHOTS.sealed;
SHOTS.treated = SHOTS.untreated;

function poseAt(phase: Skin3DPhase, p: number): Pose {
  const keys = SHOTS[phase];
  let i = 0;
  while (i < keys.length - 2 && p > keys[i + 1].at) i++;
  const a = keys[i], b = keys[i + 1];
  const t = smooth(Math.min(1, Math.max(0, (p - a.at) / (b.at - a.at || 1))));
  const l = (u: number, v: number) => u + (v - u) * t;
  return {
    az: l(a.pose.az, b.pose.az),
    el: l(a.pose.el, b.pose.el),
    zoom: l(a.pose.zoom, b.pose.zoom),
    target: [0, 1, 2].map((k) => l(a.pose.target[k], b.pose.target[k])) as V3,
  };
}

interface CameraSpec {
  position: THREE.Vector3;
  target: THREE.Vector3;
  fov: number;
  offsetX: number;
  offsetY: number;
}

function cameraFor(pose: Pose, width: number, height: number, focusX: number, centerY: number, fitFrac: number): CameraSpec {
  const fov = 24;
  const tanV = Math.tan(THREE.MathUtils.degToRad(fov / 2));
  const tanH = tanV * (width / height);
  const fitW = 4.2 / (tanH * fitFrac);
  const fitH = 2.6 / (tanV * 0.6);
  const dist = Math.max(fitW, fitH) * pose.zoom;
  const az = THREE.MathUtils.degToRad(pose.az);
  const el = THREE.MathUtils.degToRad(pose.el);
  const target = new THREE.Vector3(...pose.target);
  const position = new THREE.Vector3(
    target.x + dist * Math.cos(el) * Math.sin(az),
    target.y + dist * Math.sin(el),
    target.z + dist * Math.cos(el) * Math.cos(az),
  );
  return { position, target, fov, offsetX: (0.5 - focusX) * width, offsetY: (0.5 - centerY) * height };
}

function applyCamera(cam: THREE.PerspectiveCamera, spec: CameraSpec, width: number, height: number) {
  cam.fov = spec.fov;
  cam.aspect = width / height;
  cam.near = 0.05;
  cam.far = 300;
  cam.position.copy(spec.position);
  cam.lookAt(spec.target);
  cam.setViewOffset(width, height, spec.offsetX, spec.offsetY, width, height);
  cam.updateProjectionMatrix();
  cam.updateMatrixWorld();
}

const CameraRig: React.FC<{ spec: CameraSpec; width: number; height: number }> = ({ spec, width, height }) => {
  const { camera } = useThree();
  applyCamera(camera as THREE.PerspectiveCamera, spec, width, height);
  return null;
};

function project(spec: CameraSpec, width: number, height: number, p: V3): [number, number, boolean] {
  const cam = new THREE.PerspectiveCamera();
  applyCamera(cam, spec, width, height);
  const v = new THREE.Vector3(...p).project(cam);
  return [((v.x + 1) / 2) * width, ((1 - v.y) / 2) * height, v.z < 1];
}

// ---------------------------------------------------------------------------
// Story state: each phase eases a few values from → to, so consecutive
// phases join seamlessly (end of one = start of the next).
// ---------------------------------------------------------------------------
interface StoryValues {
  slit: number; // incision half-width at the surface (0 = closed)
  gather: number; // first-responder cells travelling to the incision
  migrate: number; // fibroblasts: home (0) → wound (1)
  grow: number; // collagen laid down (0..1)
  extra: number; // extra collagen on the alarm signal
  bump: number; // scar ridge height (× BUMP_H)
  scarTint: number; // redness of the scar line
  evaporation: number;
  freq: number; // fibroblast signalling, pulses per second
  plate: number;
  film: number;
  align: number;
  timeScale: number; // 1 = real time, →0 = frozen
  veil: number; // white wash for the "freeze" beat
}
type Key = keyof StoryValues;

const BASE: StoryValues = {
  slit: 0, gather: 0, migrate: 1, grow: 1, extra: 0, bump: 1, scarTint: 1, evaporation: 0,
  freq: 1.4, plate: 0, film: 0, align: 0, timeScale: 1, veil: 0,
};

interface PhaseSpec {
  from: Partial<StoryValues>;
  to?: Partial<StoryValues>;
  win?: Partial<Record<Key, [number, number]>>;
}

const SEAL_WIN: PhaseSpec["win"] = {
  plate: [0.04, 0.32], film: [0.28, 0.5], freq: [0.4, 0.7], align: [0.5, 0.98], evaporation: [0.04, 0.28],
};

const STORY: Record<Skin3DPhase, PhaseSpec> = {
  dive: { from: { slit: 0.3, migrate: 0, grow: 0, bump: 0, scarTint: 0, freq: 0.5 } },
  closing: {
    from: { slit: 0.3, migrate: 0, grow: 0, bump: 0, scarTint: 0, freq: 0.5 },
    to: { slit: 0, gather: 1, scarTint: 0.35 },
    win: { slit: [0.08, 0.8], gather: [0, 0.95], scarTint: [0.6, 1] },
  },
  patch: {
    from: { migrate: 0, grow: 0, bump: 0, scarTint: 0.35, freq: 0.9 },
    to: { migrate: 1, grow: 1, bump: 0.4, scarTint: 0.7, freq: 1.2 },
    win: { migrate: [0, 0.45], grow: [0.2, 1], bump: [0.3, 1], scarTint: [0.3, 1] },
  },
  months: { from: { bump: 0.4, scarTint: 0.7, freq: 1.2 }, to: { bump: 0.6, scarTint: 0.85 } },
  drying: {
    from: { bump: 0.6, scarTint: 0.85, freq: 1.2 },
    to: { evaporation: 1, freq: 1.5 },
    win: { evaporation: [0, 0.35] },
  },
  alarm: {
    from: { bump: 0.6, scarTint: 0.85, evaporation: 1, freq: 1.5 },
    to: { freq: 2.8, extra: 1, bump: 1, scarTint: 1 },
    win: { freq: [0, 0.5], extra: [0.1, 0.9], bump: [0.2, 1] },
  },
  freeze: {
    from: { extra: 1, evaporation: 1, freq: 2.8 },
    to: { timeScale: 0.04, veil: 0.5 },
    win: { timeScale: [0, 0.5], veil: [0.3, 0.8] },
  },
  scar: { from: { evaporation: 1 } },
  sealed: { from: { evaporation: 1 }, to: { plate: 1, film: 1, align: 1, freq: 0.28, evaporation: 0 }, win: SEAL_WIN },
  seal: { from: { extra: 1, evaporation: 1, freq: 2.4 }, to: { plate: 1, film: 1, align: 1, freq: 0.28, evaporation: 0 }, win: SEAL_WIN },
  healed: { from: { align: 1, freq: 0.28 } },
  untreated: {
    from: { bump: 0.25, scarTint: 0.45, grow: 0.55, extra: 0, freq: 1.0, evaporation: 0.6 },
    to: { bump: 1, scarTint: 1, grow: 1, extra: 1, freq: 2.6, evaporation: 1 },
    win: { grow: [0, 0.5], extra: [0.3, 1], freq: [0, 0.6] },
  },
  treated: {
    from: { bump: 0.25, scarTint: 0.45, grow: 0.55, freq: 1.0, plate: 1, film: 1 },
    to: { grow: 0.9, align: 0.9, freq: 0.35 },
    win: { grow: [0, 0.5], align: [0.15, 1], freq: [0, 0.6] },
  },
};

const EASED: Partial<Record<Key, (t: number) => number>> = {
  plate: Easing.bezier(0.3, 0, 0.25, 1),
  align: smooth,
};

function storyAt(phase: Skin3DPhase, p: number): StoryValues {
  const spec = STORY[phase];
  const out = { ...BASE, ...spec.from };
  if (spec.to) {
    for (const k of Object.keys(spec.to) as Key[]) {
      const [a, b] = spec.win?.[k] ?? [0, 1];
      const t = Math.min(1, Math.max(0, (p - a) / (b - a || 1)));
      const e = (EASED[k] ?? smooth)(t);
      out[k] = out[k] + ((spec.to[k] as number) - out[k]) * e;
    }
  }
  return out;
}

// ---------------------------------------------------------------------------
// Scene
// ---------------------------------------------------------------------------
interface SceneState extends StoryValues {
  cycles: number;
  timeSec: number; // simulated time (slows down with timeScale)
}

const SkinScene: React.FC<{ s: SceneState }> = ({ s }) => {
  const h = BUMP_H * s.bump * (1 - s.align);
  const slitQ = Math.round(s.slit * 100) / 100;
  const surface = (x: number) => h * bumpShape(x);
  const hq = Math.round(h * 200) / 200; // quantise geometry rebuilds

  const tex = useMemo(
    () => ({
      skinBump: makeSkinBump(),
      skinColor: makeSkinColor(),
      dermis: makeDermisTexture(),
      fibre: makeFibreBump(),
      gel: makeGelBump(),
    }),
    [],
  );

  const epiGeo = useMemo(
    () =>
      slitQ > 0
        ? slitGeometry(0, -EPI, slitQ)
        : profileGeometry(-HALF_W, HALF_W, (x) => hq * bumpShape(x), (x) => hq * bumpShape(x) - EPI, DEPTH, FRONT_Z),
    [hq, slitQ],
  );
  const dermisGeo = useMemo(
    () =>
      slitQ > 0
        ? slitGeometry(-EPI, DERMIS_BOTTOM, slitQ)
        : profileGeometry(-HALF_W, HALF_W, (x) => hq * bumpShape(x) - EPI, (x) => DERMIS_BOTTOM + hq * 0.3 * bumpShape(x), DEPTH, FRONT_Z),
    [hq, slitQ],
  );
  const fatGeo = useMemo(
    () => profileGeometry(-HALF_W, HALF_W, (x) => DERMIS_BOTTOM + hq * 0.3 * bumpShape(x), () => FAT_BOTTOM, DEPTH, FRONT_Z),
    [hq],
  );

  // Raised, glossier, redder scar strip following the ridge with soft edges.
  const scarAlpha = useMemo(() => {
    const c = document.createElement("canvas");
    c.width = 256;
    c.height = 64;
    const g = c.getContext("2d")!;
    const grad = g.createLinearGradient(0, 0, 256, 0);
    grad.addColorStop(0, "#000");
    grad.addColorStop(0.28, "#777");
    grad.addColorStop(0.5, "#fff");
    grad.addColorStop(0.72, "#777");
    grad.addColorStop(1, "#000");
    g.fillStyle = grad;
    g.fillRect(0, 0, 256, 64);
    // irregular edges
    const r = mulberry32(5);
    for (let i = 0; i < 40; i++) {
      g.fillStyle = `rgba(0,0,0,${0.2 + r() * 0.3})`;
      g.fillRect(r() < 0.5 ? r() * 70 : 186 + r() * 70, r() * 64, 20, 4);
    }
    return new THREE.CanvasTexture(c);
  }, []);
  const scarGeo = useMemo(() => {
    const g = new THREE.PlaneGeometry(0.3 + 1.3 * Math.max(s.bump, 0.05), DEPTH * 0.998, 64, 1);
    g.rotateX(-Math.PI / 2);
    const pos = g.attributes.position;
    for (let i = 0; i < pos.count; i++) pos.setY(i, hq * bumpShape(pos.getX(i)) + 0.004);
    g.computeVertexNormals();
    return g;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [hq, Math.round(s.bump * 40)]);

  // Collagen: each fibre is spun out along its path (grow), extras join on "alarm".
  const fibreCurves = CHAOTIC.map((c, i) => {
    const visible = i < N_FIBRES ? s.grow : s.extra;
    const order = i < N_FIBRES ? i / N_FIBRES : (i - N_FIBRES) / N_EXTRA;
    const g = Math.min(1, Math.max(0, visible * 1.6 - order * 0.6));
    if (g <= 0.02) return null;
    const pts = c.map((p, k) => {
      const a = ALIGNED[i][k];
      const drift = Math.sin(s.timeSec * 0.7 + i * 1.7 + k) * 0.02 * (1 - s.align);
      return new THREE.Vector3(
        THREE.MathUtils.lerp(p[0], a[0], s.align) + drift,
        THREE.MathUtils.lerp(p[1], a[1], s.align) + drift + h * 0.3 * (1 - s.align),
        THREE.MathUtils.lerp(p[2], a[2], s.align),
      );
    });
    const full = new THREE.CatmullRomCurve3(pts);
    if (g >= 0.999) return full;
    const sampled = full.getPoints(40).slice(0, Math.max(2, Math.round(40 * g) + 1));
    return new THREE.CatmullRomCurve3(sampled);
  });

  // Sheet: falls bending like fabric (edges trail), then drapes over the ridge.
  const gap = 0.045 * s.film;
  const fall = 1 - s.plate;
  const lift = 3.2 * fall * fall;
  const trail = 0.45 * Math.sin(Math.PI * Math.min(1, s.plate * 1.15));
  const conform = THREE.MathUtils.smoothstep(s.plate, 0.7, 1);
  const pq = Math.round(s.plate * 90) / 90;
  const sheetBottom = (x: number) => {
    const draped = hq * bumpShape(x) + gap;
    const flat = h + gap;
    const u = x / SHEET_HALF;
    return THREE.MathUtils.lerp(flat, draped, conform) + lift + trail * u * u;
  };
  const sheetGeo = useMemo(
    () =>
      profileGeometry(
        -SHEET_HALF,
        SHEET_HALF,
        (x) => sheetBottom(x) + SHEET_T,
        sheetBottom,
        2.4,
        1.25,
        { bevelEnabled: true, bevelThickness: 0.035, bevelSize: 0.03, bevelSegments: 4 },
      ),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [hq, pq, gap],
  );
  const filmGeo = useMemo(
    () =>
      s.film > 0.01
        ? profileGeometry(-SHEET_HALF + 0.05, SHEET_HALF - 0.05, (x) => hq * bumpShape(x) + gap + 0.002, (x) => hq * bumpShape(x) + 0.003, 2.3, 1.2)
        : null,
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [hq, gap, s.film > 0.01],
  );

  return (
    <>
      <Environment />
      <hemisphereLight args={["#fff6ee", "#c9ab98", 0.3]} />
      {/* warm key */}
      <directionalLight
        position={[-4, 10, 8]}
        intensity={2.2}
        color="#ffe9d8"
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
        shadow-camera-left={-6}
        shadow-camera-right={6}
        shadow-camera-top={6}
        shadow-camera-bottom={-6}
        shadow-bias={-0.0004}
        shadow-radius={8}
      />
      {/* cool rim from behind — edge light on skin, sheet and droplets */}
      <directionalLight position={[5, 5, -9]} intensity={1.7} color="#dfeaff" />
      {/* soft fill */}
      <directionalLight position={[-8, 2, 5]} intensity={0.35} color="#fff1e6" />

      <mesh rotation-x={-Math.PI / 2} position={[0, FAT_BOTTOM - 0.001, 0]} receiveShadow>
        <planeGeometry args={[60, 60]} />
        <shadowMaterial opacity={0.1} />
      </mesh>

      <mesh geometry={epiGeo} castShadow receiveShadow>
        <meshPhysicalMaterial attach="material-0" color={COLORS.epiCut} roughness={0.55} sheen={0.5} sheenColor="#ffcbb5" />
        <meshPhysicalMaterial
          attach="material-1"
          map={tex.skinColor}
          roughness={0.5}
          bumpMap={tex.skinBump}
          bumpScale={0.8}
          sheen={0.7}
          sheenRoughness={0.45}
          sheenColor="#ffcfb8"
          clearcoat={0.2}
          clearcoatRoughness={0.55}
        />
      </mesh>
      <mesh geometry={dermisGeo} receiveShadow>
        <meshPhysicalMaterial attach="material-0" map={tex.dermis} roughness={0.62} sheen={0.4} sheenColor="#ffd8c8" />
        <meshPhysicalMaterial attach="material-1" color={COLORS.dermisCut} roughness={0.7} />
      </mesh>
      <mesh geometry={fatGeo} receiveShadow>
        <meshPhysicalMaterial attach="material-0" color={COLORS.fatCut} roughness={0.6} />
        <meshPhysicalMaterial attach="material-1" color={COLORS.fatCut} roughness={0.7} />
      </mesh>
      {FAT_LOBULES.map((l, i) => (
        <mesh key={i} position={[l.x, l.y, FRONT_Z - l.r * 0.2]} scale={[1, 0.8, 0.35]}>
          <sphereGeometry args={[l.r, 24, 16]} />
          <meshPhysicalMaterial color="#F0D695" roughness={0.25} clearcoat={0.6} clearcoatRoughness={0.2} />
        </mesh>
      ))}

      {/* scar tissue: denser, darker zone on the cut face; glossy red ridge on top */}
      <mesh position={[0, -0.95 + h * 0.2, FRONT_Z + 0.002]} scale={[1.35, 0.9, 1]}>
        <circleGeometry args={[1, 64]} />
        <meshBasicMaterial color="#D58B76" transparent opacity={0.3 * s.bump * (1 - s.align)} depthWrite={false} />
      </mesh>
      <mesh geometry={scarGeo}>
        <meshPhysicalMaterial
          color={COLORS.scar}
          roughness={0.28}
          clearcoat={0.8}
          clearcoatRoughness={0.25}
          alphaMap={scarAlpha}
          transparent
          opacity={0.9 * s.scarTint * (1 - s.align * 0.7)}
          depthWrite={false}
          bumpMap={tex.skinBump}
          bumpScale={0.4}
        />
      </mesh>

      {/* ordered dermis fibres outside the scar */}
      {Array.from({ length: 12 }, (_, r) =>
        [-1, 1].map((side) => {
          const y = -0.42 - r * 0.115;
          const x0 = side < 0 ? -HALF_W + 0.1 : BUMP_HALF + 0.1;
          const curve = new THREE.CatmullRomCurve3([
            new THREE.Vector3(x0, y, FRONT_Z - 0.01),
            new THREE.Vector3(x0 + 0.7, y + 0.025, FRONT_Z - 0.01),
            new THREE.Vector3(x0 + 1.4, y - 0.025, FRONT_Z - 0.01),
            new THREE.Vector3(x0 + 1.95, y, FRONT_Z - 0.01),
          ]);
          return (
            <mesh key={`${r}${side}`}>
              <tubeGeometry args={[curve, 32, 0.022, 8, false]} />
              <meshPhysicalMaterial color={COLORS.normalFibre} roughness={0.5} bumpMap={tex.fibre} bumpScale={0.5} />
            </mesh>
          );
        }),
      )}

      {/* collagen in the scar: chaotic → aligned */}
      {fibreCurves.map((c, i) =>
        c && (
        <mesh key={i} castShadow>
          <tubeGeometry args={[c, 56, FIBRE_R[i], 12, false]} />
          <meshPhysicalMaterial
            color={i % 3 === 0 ? "#E0692A" : YAFHO.orange}
            roughness={0.36}
            bumpMap={tex.fibre}
            bumpScale={0.6}
            clearcoat={0.7}
            clearcoatRoughness={0.25}
            sheen={0.6}
            sheenColor="#ffb08a"
          />
        </mesh>
        ),
      )}

      {/* fibroblasts and their signalling pulses */}
      {CELLS.map((c, i) => {
        const ph = (s.cycles + i * 0.37) % 1;
        const m = Math.min(1, Math.max(0, s.migrate * 1.3 - i * 0.06));
        const pos: V3 = [0, 1, 2].map((k) => THREE.MathUtils.lerp(CELL_HOME[i][k], c[k], m)) as V3;
        return (
          <group key={i} position={pos}>
            <mesh scale={[0.11, 0.065, 0.05]}>
              <sphereGeometry args={[1, 24, 16]} />
              <meshPhysicalMaterial color={YAFHO.navy} roughness={0.25} clearcoat={1} clearcoatRoughness={0.1} />
            </mesh>
            <mesh position={[0, 0, 0.02]} scale={0.1 + ph * 0.32}>
              <ringGeometry args={[0.9, 1, 64]} />
              <meshBasicMaterial color={YAFHO.navy} transparent opacity={(1 - ph) * 0.5} depthWrite={false} />
            </mesh>
          </group>
        );
      })}

      {/* first-responder cells drawn into the closing incision */}
      {s.gather > 0.001 &&
        s.gather < 0.999 &&
        GATHER.map((g, i) => {
          const t = Math.min(1, Math.max(0, (s.gather - g.delay) / (1 - g.delay)));
          const e = smooth(t);
          const fade = t < 0.85 ? 1 : 1 - (t - 0.85) / 0.15;
          return (
            <mesh key={i} position={[0, 1, 2].map((k) => THREE.MathUtils.lerp(g.from[k], g.to[k], e)) as V3} scale={g.r * fade}>
              <sphereGeometry args={[1, 16, 12]} />
              <meshPhysicalMaterial color="#F6EAD6" roughness={0.3} clearcoat={0.6} sheen={0.5} sheenColor="#ffffff" />
            </mesh>
          );
        })}

      {/* moisture escaping without a sheet (fine mist) */}
      {s.evaporation > 0.01 &&
        DROPLETS.map((d, i) => {
          if (Math.abs(d.x) > 1.6 || Math.abs(d.z) > 1.2) return null;
          const rise = (s.timeSec * 0.35 + d.t) % 1;
          const a = s.evaporation * Math.sin(Math.PI * rise);
          return (
            <mesh key={i} position={[d.x + Math.sin(rise * 5 + i) * 0.05, surface(d.x) + 0.04 + rise * 1.2, d.z]} scale={d.r * 0.8}>
              <sphereGeometry args={[1, 14, 10]} />
              <meshPhysicalMaterial color="#d9f2ef" roughness={0.05} clearcoat={1} transparent opacity={a * 0.7} depthWrite={false} />
            </mesh>
          );
        })}

      {/* moisture held under the sheet: wet film + beads */}
      {filmGeo && (
        <mesh geometry={filmGeo}>
          <meshPhysicalMaterial color="#9ad9d2" roughness={0.02} clearcoat={1} transmission={0.7} ior={1.33} thickness={0.05} transparent opacity={0.55 * s.film} />
        </mesh>
      )}
      {s.film > 0.01 &&
        DROPLETS.slice(0, 36).map((d, i) => {
          if (Math.abs(d.x) > 1.5 || Math.abs(d.z) > 1.05) return null;
          const grow = THREE.MathUtils.clamp(s.film * 1.4 - d.t * 0.4, 0, 1);
          return (
            <mesh key={i} position={[d.x, surface(d.x) + d.r * 0.3, d.z]} scale={[d.r * 1.3 * grow, d.r * 0.6 * grow, d.r * 1.3 * grow]}>
              <sphereGeometry args={[1, 16, 12]} />
              <meshPhysicalMaterial color="#8ed3cb" roughness={0.02} clearcoat={1} transmission={0.6} ior={1.33} thickness={0.04} />
            </mesh>
          );
        })}
      {/* hydration inside the epidermis cut face */}
      {Array.from({ length: 16 }, (_, i) => {
        const x = -1.45 + i * 0.19;
        return (
          <mesh key={i} position={[x, surface(x) - 0.08 - (i % 3) * 0.04, FRONT_Z + 0.005]} scale={0.026 * s.film}>
            <sphereGeometry args={[1, 12, 10]} />
            <meshPhysicalMaterial color={YAFHO.teal} roughness={0.15} clearcoat={1} />
          </mesh>
        );
      })}

      {/* frosted medical-grade silicone gel sheet */}
      {s.plate > 0 && (
        <mesh geometry={sheetGeo} castShadow>
          <meshPhysicalMaterial
            color="#e9f3f1"
            transmission={0.9}
            thickness={0.18}
            roughness={0.3}
            ior={1.41}
            bumpMap={tex.gel}
            bumpScale={0.15}
            clearcoat={1}
            clearcoatRoughness={0.06}
            specularIntensity={1}
            attenuationColor="#d4ece8"
            attenuationDistance={1.6}
            sheen={0.4}
            sheenColor="#ffffff"
          />
        </mesh>
      )}
    </>
  );
};

// Film grain (frame-seeded) + soft vignette.
const Grade: React.FC<{ width: number; height: number; frame: number }> = ({ width, height, frame }) => (
  <svg width={width} height={height} style={{ position: "absolute", inset: 0, pointerEvents: "none" }}>
    <defs>
      <filter id="yafho-grain">
        <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={frame % 97} />
        <feColorMatrix type="saturate" values="0" />
      </filter>
      <radialGradient id="yafho-vignette" cx="50%" cy="45%" r="75%">
        <stop offset="55%" stopColor={YAFHO.navy} stopOpacity={0} />
        <stop offset="100%" stopColor="#3b2a20" stopOpacity={0.1} />
      </radialGradient>
    </defs>
    <rect width={width} height={height} filter="url(#yafho-grain)" opacity={0.05} style={{ mixBlendMode: "overlay" }} />
    <rect width={width} height={height} fill="url(#yafho-vignette)" />
  </svg>
);

/**
 * Cinematic 3D skin cutaway (Three.js): directed camera, light-olive skin with
 * a glossy raised scar, a frosted silicone sheet that falls like fabric and
 * drapes over the ridge, water held underneath, fibroblast pulses slowing and
 * collagen straightening. Same story beats as the 2D SkinCrossSection.
 */
export const SkinCrossSection3D: React.FC<SkinCrossSection3DProps> = ({
  phase = "scar",
  labels,
  introFade = true,
  focusX = 0.5,
  centerY = 0.36,
  fitFrac = 0.96,
  grade = true,
  progressFrom = 0,
  progressTo = 1,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const canvas = useCanvas();
  const width = Math.round(canvas.width);
  const height = Math.round(canvas.height);
  const L = { ...DEFAULT_LABELS, ...labels };
  const D = durationInFrames;
  const toP = (f: number) => progressFrom + (progressTo - progressFrom) * (f / Math.max(1, D - 1));
  const p = toP(frame);

  const v = storyAt(phase, p);
  // Integrate signalling pulses and simulated time so slow-motion never jumps.
  let cycles = 0;
  let simTime = 0;
  for (let f = 0; f < frame; f++) {
    const vf = storyAt(phase, toP(f));
    cycles += (vf.freq * vf.timeScale) / fps;
    simTime += vf.timeScale / fps;
  }
  const { plate, film, align } = v;
  const slow = phase === "sealed" || phase === "seal" ? ease(frame, D * 0.4, D * 0.7) : phase === "healed" ? 1 : 0;

  const state: SceneState = { ...v, cycles, timeSec: simTime };

  const pose = poseAt(phase, p);
  if (phase === "alarm") {
    // nervous micro-shake that grows with the alarm
    const k = 0.012 * ease(frame, 0, D * 0.5);
    pose.target = [pose.target[0] + Math.sin(frame * 0.9) * k, pose.target[1] + Math.sin(frame * 1.3 + 1) * k, pose.target[2]];
  }
  const cam = cameraFor(pose, width, height, focusX, centerY, fitFrac);
  const intro = introFade ? ease(frame, 0, Math.round(0.6 * fps)) : 1;
  const h = BUMP_H * v.bump * (1 - align);
  const isSeal = phase === "sealed" || phase === "seal";

  // Labels appear only once the camera shows what they point at.
  const reveal = (from: number) => ease(frame, D * from, D * from + 0.4 * fps);
  type Anchor = { key: keyof Skin3DLabels; at: V3; side: "left" | "right"; swatch: string; show: number };
  const collagenAt: V3 = [
    THREE.MathUtils.lerp(CHAOTIC[5][2][0], ALIGNED[5][2][0], align),
    THREE.MathUtils.lerp(CHAOTIC[5][2][1], ALIGNED[5][2][1], align),
    FRONT_Z,
  ];
  const anchors: Anchor[] =
    phase === "scar"
      ? [
          { key: "epidermis", at: [-2.4, -0.11, FRONT_Z], side: "left", swatch: COLORS.epiCut, show: reveal(0.7) },
          { key: "dermis", at: [-2.4, -1.15, FRONT_Z], side: "left", swatch: COLORS.dermisCut, show: reveal(0.74) },
          { key: "collagen", at: CHAOTIC[5][2], side: "right", swatch: YAFHO.orange, show: reveal(0.78) },
        ]
      : phase === "patch"
        ? [
            { key: "fibroblast", at: CELLS[1], side: "right", swatch: YAFHO.navy, show: reveal(0.4) },
            { key: "collagen", at: collagenAt, side: "left", swatch: YAFHO.orange, show: reveal(0.7) },
          ]
        : phase === "drying"
          ? [{ key: "moistureOut", at: [0.5, h * bumpShape(0.5) + 0.85, 0.6], side: "right", swatch: YAFHO.teal, show: reveal(0.3) }]
        : phase === "alarm"
          ? [
              { key: "signalUp", at: CELLS[3], side: "right", swatch: YAFHO.navy, show: reveal(0.25) },
              { key: "collagen", at: collagenAt, side: "left", swatch: YAFHO.orange, show: reveal(0.5) },
            ]
          : isSeal || phase === "healed"
            ? [
                { key: "moisture", at: [1.0, h * bumpShape(1.0) + 0.06, 0.95], side: "right", swatch: YAFHO.teal, show: isSeal ? reveal(0.36) : 1 },
                { key: "signal", at: CELLS[3], side: "right", swatch: YAFHO.navy, show: isSeal ? reveal(0.5) : 1 },
                { key: "collagen", at: collagenAt, side: "left", swatch: YAFHO.orange, show: isSeal ? reveal(0.62) : 1 },
              ]
            : [];

  // Motion arrows (world space → screen): explain what moves where.
  type MoveArrow = { from: V3; to: V3; color: string; show: number };
  const crest = h;
  const fadeOut = (a: number, b: number) => 1 - ease(frame, D * a, D * b);
  const moves: MoveArrow[] =
    phase === "closing"
      ? [
          { from: [-1.45, 0.28, FRONT_Z], to: [-0.4, 0.28, FRONT_Z], color: YAFHO.navy, show: reveal(0.04) * fadeOut(0.72, 0.88) },
          { from: [1.45, 0.28, FRONT_Z], to: [0.4, 0.28, FRONT_Z], color: YAFHO.navy, show: reveal(0.04) * fadeOut(0.72, 0.88) },
        ]
      : phase === "drying"
        ? [-0.7, 0, 0.7].map((x, i) => ({
            from: [x, h * bumpShape(x) + 0.12, 0.6] as V3,
            to: [x, h * bumpShape(x) + 0.85, 0.6] as V3,
            color: YAFHO.teal,
            show: reveal(0.15 + i * 0.06),
          }))
        : phase === "alarm"
          ? [{ from: [0, crest + 0.12, 1.25], to: [0, crest + 0.75, 1.25], color: YAFHO.orange, show: reveal(0.35) }]
          : phase === "untreated"
            ? [{ from: [0, crest + 0.15, 1.25] as V3, to: [0, crest + 0.8, 1.25] as V3, color: YAFHO.orange, show: reveal(0.35) }]
          : phase === "treated"
            ? [{ from: [0, 1.0, 1.25] as V3, to: [0, crest + 0.2, 1.25] as V3, color: YAFHO.teal, show: reveal(0.35) }]
          : isSeal
            ? [
                { from: [0, 2.3, 0.6], to: [0, 1.15, 0.6], color: YAFHO.navy, show: reveal(0.01) * fadeOut(0.24, 0.32) },
                { from: [0, 0.95, 1.25], to: [0, crest + 0.12, 1.25], color: YAFHO.orange, show: reveal(0.62) },
              ]
            : [];

  const regionL = Math.max(0, (focusX - fitFrac / 2) * width);
  const regionR = Math.min(width, (focusX + fitFrac / 2) * width);
  const fs = Math.round(Math.max((regionR - regionL) * 0.03, height * 0.022));
  const ph = fs * 1.75;
  const placed = anchors
    .filter((a) => L[a.key] && a.show > 0.01)
    .map((a) => {
      const [ax, ay, visible] = project(cam, width, height, a.at);
      return { ...a, ax, ay, visible, py: a.key === "moisture" ? ay - fs * 3 : ay };
    })
    .filter((a) => a.visible && a.ax > regionL && a.ax < regionR && a.ay > 0 && a.ay < height);
  for (const side of ["left", "right"] as const) {
    const col = placed.filter((q) => q.side === side).sort((a, b) => a.py - b.py);
    for (let i = 1; i < col.length; i++) {
      if (col[i].py - col[i - 1].py < ph * 1.35) col[i].py = col[i - 1].py + ph * 1.35;
    }
  }

  return (
    <AbsoluteFill style={{ background: YAFHO.offWhite, opacity: intro }}>
      <ThreeCanvas width={width} height={height} shadows gl={{ antialias: true, alpha: true, preserveDrawingBuffer: true }}>
        <CameraRig spec={cam} width={width} height={height} />
        <SkinScene s={state} />
      </ThreeCanvas>
      {v.veil > 0 && <AbsoluteFill style={{ background: YAFHO.offWhite, opacity: v.veil }} />}
      {grade && <Grade width={width} height={height} frame={frame} />}
      <svg width={width} height={height} style={{ position: "absolute", inset: 0, overflow: "visible" }}>
        {moves
          .filter((m) => m.show > 0.01)
          .map((m, i) => {
            const [x1, y1] = project(cam, width, height, m.from);
            const [x2f, y2f] = project(cam, width, height, m.to);
            const x2 = x1 + (x2f - x1) * m.show;
            const y2 = y1 + (y2f - y1) * m.show;
            const ang = Math.atan2(y2 - y1, x2 - x1);
            const hl = fs * 0.9;
            const sw = Math.max(5, fs * 0.22);
            const head = (c: string, grow: number) =>
              `${x2 + Math.cos(ang) * grow},${y2 + Math.sin(ang) * grow} ` +
              `${x2 - Math.cos(ang - 0.5) * (hl + grow)},${y2 - Math.sin(ang - 0.5) * (hl + grow)} ` +
              `${x2 - Math.cos(ang + 0.5) * (hl + grow)},${y2 - Math.sin(ang + 0.5) * (hl + grow)}`;
            return (
              <g key={`mv${i}`} opacity={Math.min(1, m.show * 1.5)}>
                <line x1={x1} y1={y1} x2={x2 - Math.cos(ang) * hl * 0.6} y2={y2 - Math.sin(ang) * hl * 0.6} stroke={YAFHO.white} strokeWidth={sw + 6} strokeLinecap="round" />
                <polygon points={head(YAFHO.white, 4)} fill={YAFHO.white} />
                <line x1={x1} y1={y1} x2={x2 - Math.cos(ang) * hl * 0.6} y2={y2 - Math.sin(ang) * hl * 0.6} stroke={m.color} strokeWidth={sw} strokeLinecap="round" />
                <polygon points={head(m.color, 0)} fill={m.color} />
              </g>
            );
          })}
        {placed.map((a) => {
          const text = L[a.key]!;
          const { ax, ay, py } = a;
          const w = text.length * fs * 0.64 + fs * 2.2;
          const px = a.side === "left" ? regionL + width * 0.02 : regionR - width * 0.02 - w;
          const edgeX = a.side === "left" ? px + w : px;
          const slide = (1 - a.show) * fs * (a.side === "left" ? -1 : 1);
          return (
            <g key={a.key} opacity={a.show} transform={`translate(${slide}, 0)`}>
              <line x1={edgeX} y1={py} x2={ax} y2={ay} stroke={YAFHO.navy} strokeWidth={Math.max(2, fs * 0.07)} />
              {(() => {
                // arrowhead on the leader, pointing at the anchor
                const ang = Math.atan2(ay - py, ax - edgeX);
                const hl = fs * 0.5;
                const pts = `${ax},${ay} ${ax - Math.cos(ang - 0.45) * hl},${ay - Math.sin(ang - 0.45) * hl} ${ax - Math.cos(ang + 0.45) * hl},${ay - Math.sin(ang + 0.45) * hl}`;
                return <polygon points={pts} fill={YAFHO.navy} stroke={YAFHO.white} strokeWidth={2} />;
              })()}
              <rect x={px} y={py - ph / 2} width={w} height={ph} rx={ph / 2} fill={YAFHO.white} />
              <circle cx={px + fs * 0.9} cy={py} r={fs * 0.3} fill={a.swatch} />
              <text x={px + fs * 1.5} y={py + fs * 0.36} fontSize={fs} fontFamily={YAFHO.sans} fontWeight={800} fill={YAFHO.navy}>
                {text}
              </text>
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
