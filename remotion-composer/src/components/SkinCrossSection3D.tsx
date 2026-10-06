import { useMemo } from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
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
  /** Fraction of canvas height where the block's centre sits (leaves room for a thesis below). */
  centerY?: number;
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
const N_FIBRES = 24;

const COLORS = {
  skinTop: "#C98468",
  epiCut: "#B9705A",
  dermisCut: "#E6AE98",
  fatCut: "#EED8B0",
  scar: "#B5523F",
  normalFibre: "#D69A82",
};

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
const DROPLETS = Array.from({ length: 34 }, () => ({
  x: (rnd() - 0.5) * 2.8,
  z: (rnd() - 0.5) * 2.0,
  r: 0.025 + rnd() * 0.035,
  t: rnd(),
}));

// ---------------------------------------------------------------------------
// Procedural textures (deterministic canvas → texture)
// ---------------------------------------------------------------------------
function makeSkinBump(): THREE.CanvasTexture {
  const c = document.createElement("canvas");
  c.width = c.height = 512;
  const g = c.getContext("2d")!;
  g.fillStyle = "#808080";
  g.fillRect(0, 0, 512, 512);
  const r = mulberry32(7);
  for (let i = 0; i < 2600; i++) {
    const v = Math.floor(90 + r() * 80);
    g.fillStyle = `rgba(${v},${v},${v},0.55)`;
    g.beginPath();
    g.arc(r() * 512, r() * 512, 0.6 + r() * 1.6, 0, Math.PI * 2);
    g.fill();
  }
  g.strokeStyle = "rgba(60,60,60,0.25)";
  for (let i = 0; i < 70; i++) {
    g.lineWidth = 0.5 + r();
    g.beginPath();
    const x = r() * 512, y = r() * 512;
    g.moveTo(x, y);
    g.lineTo(x + (r() - 0.5) * 90, y + (r() - 0.5) * 30);
    g.stroke();
  }
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  return t;
}

function makeDermisTexture(): THREE.CanvasTexture {
  const c = document.createElement("canvas");
  c.width = c.height = 512;
  const g = c.getContext("2d")!;
  g.fillStyle = COLORS.dermisCut;
  g.fillRect(0, 0, 512, 512);
  const r = mulberry32(11);
  g.strokeStyle = "rgba(170,95,72,0.35)";
  for (let row = 0; row < 40; row++) {
    g.lineWidth = 2 + r() * 2;
    g.beginPath();
    const y = row * 13 + r() * 6;
    g.moveTo(0, y);
    for (let x = 0; x <= 512; x += 32) g.lineTo(x, y + Math.sin(x / 40 + row) * 4);
    g.stroke();
  }
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.repeat.set(0.35, 0.35);
  return t;
}

// ---------------------------------------------------------------------------
// Layer slabs: a 2D profile (x,y) extruded along z. Caps = cut faces.
// ---------------------------------------------------------------------------
function slabGeometry(top: (x: number) => number, bottom: (x: number) => number): THREE.ExtrudeGeometry {
  const s = new THREE.Shape();
  const N = 90;
  for (let i = 0; i <= N; i++) {
    const x = -HALF_W + (2 * HALF_W * i) / N;
    if (i === 0) s.moveTo(x, top(x));
    else s.lineTo(x, top(x));
  }
  for (let i = N; i >= 0; i--) {
    const x = -HALF_W + (2 * HALF_W * i) / N;
    s.lineTo(x, bottom(x));
  }
  s.closePath();
  const geo = new THREE.ExtrudeGeometry(s, { depth: DEPTH, bevelEnabled: false, steps: 1, curveSegments: 1 });
  geo.translate(0, 0, -FRONT_Z);
  geo.computeVertexNormals();
  return geo;
}

const Environment: React.FC = () => {
  const { gl, scene } = useThree();
  useMemo(() => {
    const pmrem = new THREE.PMREMGenerator(gl);
    scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
    scene.environmentIntensity = 0.4;
    gl.toneMapping = THREE.ACESFilmicToneMapping;
    gl.toneMappingExposure = 0.92;
    gl.shadowMap.enabled = true;
    gl.shadowMap.type = THREE.PCFSoftShadowMap;
  }, [gl, scene]);
  return null;
};

interface CameraSpec {
  position: THREE.Vector3;
  target: THREE.Vector3;
  fov: number;
  offsetY: number;
}

const CameraRig: React.FC<{ spec: CameraSpec; width: number; height: number }> = ({ spec, width, height }) => {
  const { camera } = useThree();
  const cam = camera as THREE.PerspectiveCamera;
  cam.fov = spec.fov;
  cam.near = 0.1;
  cam.far = 200;
  cam.position.copy(spec.position);
  cam.lookAt(spec.target);
  cam.setViewOffset(width, height, 0, spec.offsetY, width, height);
  cam.updateProjectionMatrix();
  return null;
};

function cameraFor(frame: number, D: number, width: number, height: number, centerY: number): CameraSpec {
  const fov = 26;
  const aspect = width / height;
  const p = frame / Math.max(1, D - 1);
  // Fit ~7.6 units of width (block + margin) whatever the aspect.
  const tanH = Math.tan(THREE.MathUtils.degToRad(fov / 2)) * aspect;
  const tanV = Math.tan(THREE.MathUtils.degToRad(fov / 2));
  const fitW = 4.1 / tanH;
  const fitH = 2.6 / tanV / 0.55;
  const dist = Math.max(fitW, fitH) * interpolate(p, [0, 1], [1.04, 0.95]);
  const az = THREE.MathUtils.degToRad(interpolate(p, [0, 1], [-30, -16]));
  const el = THREE.MathUtils.degToRad(interpolate(p, [0, 1], [24, 18]));
  const target = new THREE.Vector3(0, -1.1, 0.2);
  const position = new THREE.Vector3(
    target.x + dist * Math.cos(el) * Math.sin(az),
    target.y + dist * Math.sin(el),
    target.z + dist * Math.cos(el) * Math.cos(az),
  );
  return { position, target, fov, offsetY: (0.5 - centerY) * height };
}

function project(spec: CameraSpec, width: number, height: number, p: V3): [number, number] {
  const cam = new THREE.PerspectiveCamera(spec.fov, width / height, 0.1, 200);
  cam.position.copy(spec.position);
  cam.lookAt(spec.target);
  cam.setViewOffset(width, height, 0, spec.offsetY, width, height);
  cam.updateProjectionMatrix();
  cam.updateMatrixWorld();
  const v = new THREE.Vector3(...p).project(cam);
  return [((v.x + 1) / 2) * width, ((1 - v.y) / 2) * height];
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
  const crest = h;

  const skinBump = useMemo(() => makeSkinBump(), []);
  const dermisTex = useMemo(() => makeDermisTexture(), []);
  const hq = Math.round(h * 200) / 200; // quantise geometry rebuilds

  const epiGeo = useMemo(() => slabGeometry((x) => hq * bumpShape(x), (x) => hq * bumpShape(x) - EPI), [hq]);
  const dermisGeo = useMemo(
    () => slabGeometry((x) => hq * bumpShape(x) - EPI, (x) => DERMIS_BOTTOM + hq * 0.3 * bumpShape(x)),
    [hq],
  );
  const fatGeo = useMemo(() => slabGeometry((x) => DERMIS_BOTTOM + hq * 0.3 * bumpShape(x), () => FAT_BOTTOM), [hq]);

  const scarAlpha = useMemo(() => {
    const c = document.createElement("canvas");
    c.width = 256;
    c.height = 4;
    const g = c.getContext("2d")!;
    const grad = g.createLinearGradient(0, 0, 256, 0);
    grad.addColorStop(0, "#000");
    grad.addColorStop(0.3, "#888");
    grad.addColorStop(0.5, "#fff");
    grad.addColorStop(0.7, "#888");
    grad.addColorStop(1, "#000");
    g.fillStyle = grad;
    g.fillRect(0, 0, 256, 4);
    return new THREE.CanvasTexture(c);
  }, []);
  const scarGeo = useMemo(() => {
    const w = 1.5;
    const g = new THREE.PlaneGeometry(w, DEPTH * 0.998, 60, 1);
    g.rotateX(-Math.PI / 2);
    const pos = g.attributes.position;
    for (let i = 0; i < pos.count; i++) pos.setY(i, hq * bumpShape(pos.getX(i)) + 0.004);
    g.computeVertexNormals();
    return g;
  }, [hq]);

  const fibreCurves = CHAOTIC.map((c, i) => {
    const pts = c.map((p, k) => {
      const a = ALIGNED[i][k];
      const drift = Math.sin(s.timeSec * 0.9 + i * 1.7 + k) * 0.025 * (1 - s.align);
      return new THREE.Vector3(
        THREE.MathUtils.lerp(p[0], a[0], s.align) + drift,
        THREE.MathUtils.lerp(p[1], a[1], s.align) + drift + h * 0.3 * (1 - s.align),
        THREE.MathUtils.lerp(p[2], a[2], s.align),
      );
    });
    return new THREE.CatmullRomCurve3(pts);
  });

  // Sheet rests on the scar crest and follows it down as the scar flattens.
  const sheetT = 0.07;
  const gap = 0.05 * s.film;
  // Lift while falling; conform to the skin as it lands (a soft sheet, not a slab).
  const lift = interpolate(s.plate, [0, 1], [2.6, 0]);
  const conform = THREE.MathUtils.smoothstep(s.plate, 0.6, 1);
  const pq = Math.round(s.plate * 60) / 60;
  const sheetGeo = useMemo(() => {
    const half = 1.65;
    const N = 60;
    const bottom = (x: number) => {
      const edgeSag = Math.min(1, (half - Math.abs(x)) / 0.12); // rounded long edges
      const draped = hq * bumpShape(x) + gap;
      const flat = crest + gap;
      return THREE.MathUtils.lerp(flat, draped, conform) + lift + (1 - edgeSag) * 0.01;
    };
    const sh = new THREE.Shape();
    for (let i = 0; i <= N; i++) {
      const x = -half + (2 * half * i) / N;
      if (i === 0) sh.moveTo(x, bottom(x));
      else sh.lineTo(x, bottom(x));
    }
    for (let i = N; i >= 0; i--) {
      const x = -half + (2 * half * i) / N;
      const t = Math.min(1, (half - Math.abs(x)) / 0.08);
      sh.lineTo(x, bottom(x) + sheetT * Math.sqrt(Math.max(0, t)));
    }
    sh.closePath();
    const g = new THREE.ExtrudeGeometry(sh, {
      depth: 2.4,
      bevelEnabled: true,
      bevelThickness: 0.03,
      bevelSize: 0.02,
      bevelSegments: 3,
      curveSegments: 1,
    });
    g.translate(0, 0, -1.35);
    g.computeVertexNormals();
    return g;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [hq, pq, gap]);

  return (
    <>
      <Environment />
      <hemisphereLight args={["#ffffff", "#d9c2b0", 0.45]} />
      <directionalLight
        position={[2, 10, 8]}
        intensity={1.8}
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
        shadow-camera-left={-6}
        shadow-camera-right={6}
        shadow-camera-top={6}
        shadow-camera-bottom={-6}
        shadow-bias={-0.0004}
        shadow-radius={6}
      />
      <directionalLight position={[-7, 3, 5]} intensity={0.55} color="#fff3ea" />
      <directionalLight position={[0, 4, -8]} intensity={0.6} color="#ffffff" />

      {/* soft contact shadow on the "table" */}
      <mesh rotation-x={-Math.PI / 2} position={[0, FAT_BOTTOM - 0.001, 0]} receiveShadow>
        <planeGeometry args={[40, 40]} />
        <shadowMaterial opacity={0.06} />
      </mesh>

      {/* skin layers: material[0] = cut faces (caps), material[1] = outer walls */}
      <mesh geometry={epiGeo} castShadow receiveShadow>
        <meshPhysicalMaterial attach="material-0" color={COLORS.epiCut} roughness={0.6} sheen={0.4} sheenColor="#ffd9c8" />
        <meshPhysicalMaterial
          attach="material-1"
          color={COLORS.skinTop}
          roughness={0.52}
          bumpMap={skinBump}
          bumpScale={0.6}
          sheen={0.6}
          sheenRoughness={0.5}
          sheenColor="#ffd6c4"
          clearcoat={0.15}
          clearcoatRoughness={0.6}
        />
      </mesh>
      <mesh geometry={dermisGeo} receiveShadow>
        <meshPhysicalMaterial attach="material-0" map={dermisTex} roughness={0.7} sheen={0.3} sheenColor="#ffe2d6" />
        <meshPhysicalMaterial attach="material-1" color={COLORS.dermisCut} roughness={0.7} />
      </mesh>
      <mesh geometry={fatGeo} receiveShadow>
        <meshPhysicalMaterial attach="material-0" color={COLORS.fatCut} roughness={0.75} />
        <meshPhysicalMaterial attach="material-1" color={COLORS.fatCut} roughness={0.75} />
      </mesh>
      {FAT_LOBULES.map((l, i) => (
        <mesh key={i} position={[l.x, l.y, FRONT_Z - l.r * 0.2]} scale={[1, 0.8, 0.35]}>
          <sphereGeometry args={[l.r, 24, 16]} />
          <meshPhysicalMaterial color="#F3DDA6" roughness={0.35} clearcoat={0.4} />
        </mesh>
      ))}

      {/* scar tissue tint on the cut face and on the skin surface */}
      <mesh position={[0, -0.95 + h * 0.2, FRONT_Z + 0.002]} scale={[1.35, 0.9, 1]}>
        <circleGeometry args={[1, 48]} />
        <meshBasicMaterial color="#E7A994" transparent opacity={0.35 * (1 - s.align)} depthWrite={false} />
      </mesh>
      <mesh geometry={scarGeo}>
        <meshPhysicalMaterial
          color={COLORS.scar}
          roughness={0.32}
          clearcoat={0.6}
          alphaMap={scarAlpha}
          transparent
          opacity={0.85 * (1 - s.align * 0.75)}
          depthWrite={false}
          bumpMap={skinBump}
          bumpScale={0.3}
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
              <meshPhysicalMaterial color={COLORS.normalFibre} roughness={0.5} />
            </mesh>
          );
        }),
      )}

      {/* collagen in the scar: chaotic → aligned */}
      {fibreCurves.map((c, i) => (
        <mesh key={i} castShadow>
          <tubeGeometry args={[c, 48, 0.038, 10, false]} />
          <meshPhysicalMaterial color={YAFHO.orange} roughness={0.38} clearcoat={0.6} clearcoatRoughness={0.3} sheen={0.5} sheenColor="#ffb08a" />
        </mesh>
      ))}

      {/* fibroblasts and their signalling pulses */}
      {CELLS.map((c, i) => {
        const ph = (s.cycles + i * 0.37) % 1;
        return (
          <group key={i} position={c}>
            <mesh scale={[0.11, 0.065, 0.05]}>
              <sphereGeometry args={[1, 24, 16]} />
              <meshPhysicalMaterial color={YAFHO.navy} roughness={0.3} clearcoat={0.8} />
            </mesh>
            <mesh position={[0, 0, 0.02]} scale={0.1 + ph * 0.32}>
              <ringGeometry args={[0.9, 1, 48]} />
              <meshBasicMaterial color={YAFHO.navy} transparent opacity={(1 - ph) * 0.55} depthWrite={false} />
            </mesh>
          </group>
        );
      })}

      {/* moisture: escaping without a sheet, held under it with one */}
      {DROPLETS.map((d, i) => {
        if (Math.abs(d.x) > 1.6 || Math.abs(d.z) > 1.15) return null;
        const y0 = surface(d.x);
        const rise = ((s.timeSec * 0.45 + d.t) % 1);
        const escaping = s.evaporation * (1 - rise);
        const held = s.film;
        return (
          <group key={i}>
            {escaping > 0.01 && (
              <mesh position={[d.x, y0 + 0.05 + rise * 1.4, d.z]} scale={d.r * (1 - rise * 0.5)}>
                <sphereGeometry args={[1, 16, 12]} />
                <meshPhysicalMaterial color="#bfe9e4" transmission={0.6} roughness={0.05} ior={1.33} transparent opacity={escaping * 0.8} />
              </mesh>
            )}
            {held > 0.01 && (
              <mesh position={[d.x, y0 + d.r * 0.35, d.z]} scale={[d.r * 1.2 * held, d.r * 0.55 * held, d.r * 1.2 * held]}>
                <sphereGeometry args={[1, 16, 12]} />
                <meshPhysicalMaterial color="#8fd6cf" roughness={0.03} clearcoat={1} transmission={0.5} ior={1.33} thickness={0.05} />
              </mesh>
            )}
          </group>
        );
      })}
      {/* hydration dots inside the epidermis cut face */}
      {Array.from({ length: 14 }, (_, i) => {
        const x = -1.3 + i * 0.2;
        return (
          <mesh key={i} position={[x, surface(x) - 0.08 - (i % 3) * 0.04, FRONT_Z + 0.005]} scale={0.028 * s.film}>
            <sphereGeometry args={[1, 12, 10]} />
            <meshPhysicalMaterial color={YAFHO.teal} roughness={0.2} clearcoat={1} />
          </mesh>
        );
      })}

      {/* silicone sheet */}
      {s.plate > 0 && (
        <mesh geometry={sheetGeo} castShadow>
          <meshPhysicalMaterial
            color="#f7fcfb"
            transmission={0.96}
            thickness={0.08}
            roughness={0.14}
            ior={1.41}
            clearcoat={1}
            clearcoatRoughness={0.15}
            attenuationColor="#cfe9e6"
            attenuationDistance={2.5}
          />
        </mesh>
      )}
    </>
  );
};

/**
 * Photoreal-leaning 3D skin cutaway (Three.js): same beats as SkinCrossSection —
 * chaotic orange collagen, a translucent silicone sheet settling on the scar,
 * water held underneath, fibroblast pulses slowing, collagen straightening.
 */
export const SkinCrossSection3D: React.FC<SkinCrossSection3DProps> = ({
  phase = "scar",
  labels,
  introFade = true,
  centerY = 0.36,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const { width, height } = useCanvas();
  const L = { ...DEFAULT_LABELS, ...labels };
  const D = durationInFrames;

  let plate = 0, film = 0, slow = 0, align = 0;
  if (phase === "sealed") {
    plate = ease(frame, D * 0.03, D * 0.24);
    film = ease(frame, D * 0.2, D * 0.42);
    slow = ease(frame, D * 0.32, D * 0.6);
    align = ease(frame, D * 0.45, D * 0.95);
  } else if (phase === "healed") {
    slow = 1;
    align = 1;
  }
  const freqAt = (f: number) => {
    const sl = phase === "sealed" ? ease(f, D * 0.32, D * 0.6) : slow;
    return interpolate(sl, [0, 1], [1.5, 0.3]);
  };
  let cycles = 0;
  for (let f = 0; f < frame; f++) cycles += freqAt(f) / fps;

  const state: SceneState = {
    plate,
    film,
    align,
    cycles,
    evaporation: phase === "scar" ? 1 : phase === "sealed" ? 1 - plate : 0,
    timeSec: frame / fps,
  };

  const cam = cameraFor(frame, D, width, height, centerY);
  const intro = introFade ? ease(frame, 0, Math.round(0.4 * fps)) : 1;
  const h = BUMP_H * (1 - align);

  // Labels: projected anchors, pills pinned to the left/right margins.
  const anchors: { key: keyof SkinCrossSectionLabels; at: V3; side: "left" | "right"; swatch: string; show: number }[] = [
    { key: "epidermis", at: [-2.4, -0.11, FRONT_Z], side: "left", swatch: COLORS.epiCut, show: 1 },
    { key: "dermis", at: [-2.4, -1.15, FRONT_Z], side: "left", swatch: COLORS.dermisCut, show: 1 },
    { key: "collagen", at: [CHAOTIC[5][2][0] * (1 - align) + ALIGNED[5][2][0] * align, CHAOTIC[5][2][1] * (1 - align) + ALIGNED[5][2][1] * align, FRONT_Z], side: "right", swatch: YAFHO.orange, show: 1 },
    { key: "moisture", at: [1.2, h * bumpShape(1.2) + 0.08, 0.9], side: "right", swatch: YAFHO.teal, show: phase === "scar" ? 0 : film },
    { key: "signal", at: CELLS[3], side: "right", swatch: YAFHO.navy, show: phase === "scar" ? 0 : slow },
  ];
  const fs = Math.round(width * 0.03);
  const ph = fs * 1.75;
  const placed = anchors
    .filter((a) => L[a.key] && a.show > 0.01)
    .map((a) => {
      const [ax, ay] = project(cam, width, height, a.at);
      return { ...a, ax, ay, py: a.key === "moisture" ? ay - fs * 3.2 : ay };
    });
  for (const side of ["left", "right"] as const) {
    const col = placed.filter((p) => p.side === side).sort((a, b) => a.py - b.py);
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
      <svg width={width} height={height} style={{ position: "absolute", inset: 0, overflow: "visible" }}>
        {placed.map((a) => {
          const text = L[a.key]!;
          const { ax, ay, py } = a;
          const w = text.length * fs * 0.64 + fs * 2.2;
          const px = a.side === "left" ? width * 0.03 : width * 0.97 - w;
          const edgeX = a.side === "left" ? px + w : px;
          return (
            <g key={a.key} opacity={a.show}>
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
