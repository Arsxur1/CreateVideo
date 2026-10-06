import { useMemo } from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import { useThree } from "@react-three/fiber";
import * as THREE from "three";
import { RoomEnvironment } from "three/examples/jsm/environments/RoomEnvironment.js";
import { YAFHO, ease, useCanvas } from "./yafho/tokens";
import type { SkinCrossSectionLabels, SkinPhase } from "./SkinCrossSection";

export interface SkinCrossSection3DProps {
  /** Same story beats as the 2D SkinCrossSection: scar → sealed (animated) → healed. */
  phase?: SkinPhase;
  labels?: SkinCrossSectionLabels;
  introFade?: boolean;
  /** Where the block's centre sits, as fractions of the canvas (leave room for a thesis). */
  focusX?: number;
  centerY?: number;
  /** Fraction of canvas width the whole block spans in the wide establishing pose. */
  fitFrac?: number;
  /** Film grain + vignette. */
  grade?: boolean;
}

const DEFAULT_LABELS: SkinCrossSectionLabels = {
  epidermis: "эпидермис",
  dermis: "дерма",
  collagen: "коллаген",
  moisture: "влага ↑",
  signal: "сигнал ↓",
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
const N_FIBRES = 26;
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
const CHAOTIC: V3[][] = Array.from({ length: N_FIBRES }, () => {
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
const ALIGNED: V3[][] = Array.from({ length: N_FIBRES }, (_, i) => {
  const y = -0.42 - (i / (N_FIBRES - 1)) * 1.3 + (rndA() - 0.5) * 0.05;
  const len = 1.3 + rndA() * 1.0;
  const x0 = -1.35 + rndA() * (2.7 - len);
  const amp = 0.02 + rndA() * 0.03;
  return [0, 1, 2, 3].map((k) => [x0 + (k * len) / 3, y + (k === 1 ? amp : k === 2 ? -amp : 0), FRONT_Z - 0.005] as V3);
});
const FIBRE_R = Array.from({ length: N_FIBRES }, () => 0.032 + rnd() * 0.014);
const CELLS: V3[] = [
  [-0.75, -0.75, FRONT_Z],
  [0.55, -0.6, FRONT_Z],
  [0.05, -1.15, FRONT_Z],
  [0.85, -1.45, FRONT_Z],
  [-0.6, -1.5, FRONT_Z],
];
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

const SHOTS: Record<SkinPhase, { at: number; pose: Pose }[]> = {
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
};

function poseAt(phase: SkinPhase, p: number): Pose {
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
// Scene
// ---------------------------------------------------------------------------
interface SceneState {
  plate: number;
  film: number;
  align: number;
  cycles: number;
  evaporation: number;
  timeSec: number;
}

const SkinScene: React.FC<{ s: SceneState }> = ({ s }) => {
  const h = BUMP_H * (1 - s.align);
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
    () => profileGeometry(-HALF_W, HALF_W, (x) => hq * bumpShape(x), (x) => hq * bumpShape(x) - EPI, DEPTH, FRONT_Z),
    [hq],
  );
  const dermisGeo = useMemo(
    () =>
      profileGeometry(-HALF_W, HALF_W, (x) => hq * bumpShape(x) - EPI, (x) => DERMIS_BOTTOM + hq * 0.3 * bumpShape(x), DEPTH, FRONT_Z),
    [hq],
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
    const g = new THREE.PlaneGeometry(1.6, DEPTH * 0.998, 64, 1);
    g.rotateX(-Math.PI / 2);
    const pos = g.attributes.position;
    for (let i = 0; i < pos.count; i++) pos.setY(i, hq * bumpShape(pos.getX(i)) + 0.004);
    g.computeVertexNormals();
    return g;
  }, [hq]);

  const fibreCurves = CHAOTIC.map((c, i) => {
    const pts = c.map((p, k) => {
      const a = ALIGNED[i][k];
      const drift = Math.sin(s.timeSec * 0.7 + i * 1.7 + k) * 0.02 * (1 - s.align);
      return new THREE.Vector3(
        THREE.MathUtils.lerp(p[0], a[0], s.align) + drift,
        THREE.MathUtils.lerp(p[1], a[1], s.align) + drift + h * 0.3 * (1 - s.align),
        THREE.MathUtils.lerp(p[2], a[2], s.align),
      );
    });
    return new THREE.CatmullRomCurve3(pts);
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
        <meshBasicMaterial color="#D58B76" transparent opacity={0.3 * (1 - s.align)} depthWrite={false} />
      </mesh>
      <mesh geometry={scarGeo}>
        <meshPhysicalMaterial
          color={COLORS.scar}
          roughness={0.28}
          clearcoat={0.8}
          clearcoatRoughness={0.25}
          alphaMap={scarAlpha}
          transparent
          opacity={0.9 * (1 - s.align * 0.7)}
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
      {fibreCurves.map((c, i) => (
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
      ))}

      {/* fibroblasts and their signalling pulses */}
      {CELLS.map((c, i) => {
        const ph = (s.cycles + i * 0.37) % 1;
        return (
          <group key={i} position={c}>
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
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const { width, height } = useCanvas();
  const L = { ...DEFAULT_LABELS, ...labels };
  const D = durationInFrames;
  const p = frame / Math.max(1, D - 1);

  let plate = 0, film = 0, slow = 0, align = 0;
  if (phase === "sealed") {
    plate = interpolate(frame, [D * 0.04, D * 0.32], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.bezier(0.3, 0, 0.25, 1) });
    film = ease(frame, D * 0.28, D * 0.5);
    slow = ease(frame, D * 0.4, D * 0.7);
    align = interpolate(frame, [D * 0.5, D * 0.98], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: smooth });
  } else if (phase === "healed") {
    slow = 1;
    align = 1;
  }
  const freqAt = (f: number) => {
    const sl = phase === "sealed" ? ease(f, D * 0.4, D * 0.7) : slow;
    return interpolate(sl, [0, 1], [1.4, 0.28]);
  };
  let cycles = 0;
  for (let f = 0; f < frame; f++) cycles += freqAt(f) / fps;

  const state: SceneState = {
    plate,
    film,
    align,
    cycles,
    evaporation: phase === "scar" ? 1 : phase === "sealed" ? 1 - Math.min(1, plate * 1.3) : 0,
    timeSec: frame / fps,
  };

  const cam = cameraFor(poseAt(phase, p), width, height, focusX, centerY, fitFrac);
  const intro = introFade ? ease(frame, 0, Math.round(0.6 * fps)) : 1;
  const h = BUMP_H * (1 - align);

  // Labels appear only once the camera shows what they point at.
  const reveal = (from: number) => ease(frame, D * from, D * from + 0.4 * fps);
  const anchors: { key: keyof SkinCrossSectionLabels; at: V3; side: "left" | "right"; swatch: string; show: number }[] =
    phase === "scar"
      ? [
          { key: "epidermis", at: [-2.4, -0.11, FRONT_Z], side: "left", swatch: COLORS.epiCut, show: reveal(0.7) },
          { key: "dermis", at: [-2.4, -1.15, FRONT_Z], side: "left", swatch: COLORS.dermisCut, show: reveal(0.74) },
          { key: "collagen", at: CHAOTIC[5][2], side: "right", swatch: YAFHO.orange, show: reveal(0.78) },
        ]
      : [
          { key: "moisture", at: [1.0, h * bumpShape(1.0) + 0.06, 0.95], side: "right", swatch: YAFHO.teal, show: phase === "sealed" ? reveal(0.36) : 1 },
          { key: "signal", at: CELLS[3], side: "right", swatch: YAFHO.navy, show: phase === "sealed" ? reveal(0.5) : 1 },
          {
            key: "collagen",
            at: [
              THREE.MathUtils.lerp(CHAOTIC[5][2][0], ALIGNED[5][2][0], align),
              THREE.MathUtils.lerp(CHAOTIC[5][2][1], ALIGNED[5][2][1], align),
              FRONT_Z,
            ],
            side: "left",
            swatch: YAFHO.orange,
            show: phase === "sealed" ? reveal(0.62) : 1,
          },
        ];

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
      {grade && <Grade width={width} height={height} frame={frame} />}
      <svg width={width} height={height} style={{ position: "absolute", inset: 0, overflow: "visible" }}>
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
              <circle cx={ax} cy={ay} r={fs * 0.22} fill={YAFHO.white} stroke={YAFHO.navy} strokeWidth={Math.max(2, fs * 0.07)} />
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
