import React, { useMemo } from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import { useThree } from "@react-three/fiber";
import * as THREE from "three";
import { RoomEnvironment } from "three/examples/jsm/environments/RoomEnvironment.js";
import { ease, useCanvas } from "./yafho/tokens";

export interface PatchHero3DProps {
  /** Vertical centre of the sheet as a fraction of the canvas (leave room for titles). */
  centerY?: number;
  /** Sheet height as a fraction of the canvas height. */
  size?: number;
  /** "flex": turns and bends, springs back (topic 01); "spin": slow turn (end card). */
  motion?: "flex" | "spin";
  /** Cast a soft shadow on the wall behind (off on dark cards). */
  wallShadow?: boolean;
  introFade?: boolean;
}

const W = 2.0;
const H = 3.0;
const SEG_X = 40;
const SEG_Y = 60;

/** Rounded-rect sheet texture: matte silicone inside, a brighter moulded rim. */
function sheetTextures(): { map: THREE.CanvasTexture; alpha: THREE.CanvasTexture } {
  const px = 512;
  const py = Math.round((px * H) / W);
  const r = px * 0.09;
  const rr = (ctx: CanvasRenderingContext2D, inset: number) => {
    const x = inset;
    const y = inset;
    const w = px - inset * 2;
    const h = py - inset * 2;
    const k = Math.max(2, r - inset);
    ctx.beginPath();
    ctx.moveTo(x + k, y);
    ctx.arcTo(x + w, y, x + w, y + h, k);
    ctx.arcTo(x + w, y + h, x, y + h, k);
    ctx.arcTo(x, y + h, x, y, k);
    ctx.arcTo(x, y, x + w, y, k);
    ctx.closePath();
  };
  const a = document.createElement("canvas");
  a.width = px;
  a.height = py;
  const ac = a.getContext("2d")!;
  ac.fillStyle = "#000";
  ac.fillRect(0, 0, px, py);
  ac.fillStyle = "#fff";
  rr(ac, 2);
  ac.fill();
  ac.fillStyle = "#b4b4b4"; // interior: more see-through than the rim
  rr(ac, 14);
  ac.fill();

  const m = document.createElement("canvas");
  m.width = px;
  m.height = py;
  const mc = m.getContext("2d")!;
  mc.fillStyle = "#ece6dc";
  mc.fillRect(0, 0, px, py);
  // fine matte grain of medical silicone
  const img = mc.getImageData(0, 0, px, py);
  for (let i = 0; i < img.data.length; i += 4) {
    const n = (Math.sin(i * 12.9898) * 43758.5453) % 1;
    const d = (n - 0.5) * 10;
    img.data[i] += d;
    img.data[i + 1] += d;
    img.data[i + 2] += d;
  }
  mc.putImageData(img, 0, 0);
  // moulded rim: a bright lip with a darker inner edge so the outline reads on light backgrounds
  mc.strokeStyle = "#b9ad9c";
  mc.lineWidth = 6;
  rr(mc, 15);
  mc.stroke();
  mc.strokeStyle = "#ffffff";
  mc.lineWidth = 9;
  rr(mc, 7);
  mc.stroke();
  const map = new THREE.CanvasTexture(m);
  map.colorSpace = THREE.SRGBColorSpace;
  const alpha = new THREE.CanvasTexture(a);
  return { map, alpha };
}

const Env: React.FC = () => {
  const { gl, scene } = useThree();
  useMemo(() => {
    const pmrem = new THREE.PMREMGenerator(gl);
    scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
    scene.environmentIntensity = 0.6;
    gl.toneMapping = THREE.ACESFilmicToneMapping;
    gl.toneMappingExposure = 1.0;
    gl.shadowMap.enabled = true;
    gl.shadowMap.type = THREE.PCFSoftShadowMap;
  }, [gl, scene]);
  return null;
};

const Sheet: React.FC<{ bend: number; wave: number; rotY: number; rotX: number; y: number; scale: number; wallShadow: boolean }> = ({
  bend,
  wave,
  rotY,
  rotX,
  y,
  scale,
  wallShadow,
}) => {
  const { geo, base } = useMemo(() => {
    const g = new THREE.PlaneGeometry(W, H, SEG_X, SEG_Y);
    return { geo: g, base: Float32Array.from(g.attributes.position.array as Float32Array) };
  }, []);
  const tex = useMemo(() => sheetTextures(), []);
  // bend: curl around the vertical axis; wave: soft ripple along the length
  const pos = geo.attributes.position as THREE.BufferAttribute;
  for (let i = 0; i < pos.count; i++) {
    const x = base[i * 3];
    const yy = base[i * 3 + 1];
    const z = -bend * x * x + wave * 0.06 * Math.sin(yy * 2.4 + x * 0.8);
    pos.setXYZ(i, x, yy, z);
  }
  pos.needsUpdate = true;
  geo.computeVertexNormals();

  return (
    <>
      <group position={[0, y, 0]} rotation={[rotX, rotY, 0]} scale={scale}>
        <mesh geometry={geo} castShadow>
          <meshPhysicalMaterial
            color="#f4f0ea"
            map={tex.map}
            alphaMap={tex.alpha}
            transparent
            opacity={0.92}
            roughness={0.3}
            metalness={0}
            clearcoat={0.7}
            clearcoatRoughness={0.3}
            sheen={0.4}
            sheenColor={new THREE.Color("#ffffff")}
            side={THREE.DoubleSide}
            depthWrite={false}
          />
        </mesh>
      </group>
      {wallShadow && (
        <mesh position={[0, y, -0.7]} receiveShadow>
          <planeGeometry args={[30, 30]} />
          <shadowMaterial opacity={0.09} />
        </mesh>
      )}
    </>
  );
};

/**
 * Topic 01 / 09: the Yafho-Silicare sheet as a hero object — translucent medical
 * silicone, a slow turn, then it bends and springs back (soft, flexible).
 * Realistic light (3D exception); text and logo stay in code overlays.
 */
export const PatchHero3D: React.FC<PatchHero3DProps> = ({
  centerY = 0.36,
  size = 0.5,
  motion = "flex",
  wallShadow = true,
  introFade = false,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const { width, height } = useCanvas();
  const w = Math.round(width);
  const h = Math.round(height);
  const t = frame / Math.max(1, durationInFrames - 1);
  const sec = frame / fps;

  const fov = 30;
  const dist = 9;
  const visH = 2 * dist * Math.tan(((fov / 2) * Math.PI) / 180);
  const scale = (size * visH) / H;
  const y = (0.5 - centerY) * visH;

  let bend = 0;
  let rotY = 0;
  let rotX = -0.18;
  let wave = 0;
  if (motion === "flex") {
    // turn in, flex (press), release with a damped spring
    rotY = -0.55 + 0.75 * ease(t, 0, 0.45) - 0.12 * Math.sin(sec * 0.9);
    const press = ease(t, 0.3, 0.5);
    const release = t > 0.5 ? Math.exp(-(t - 0.5) * 9) * Math.cos((t - 0.5) * 38) : 1;
    bend = 0.32 * press * release;
    wave = 0.6 * Math.sin(sec * 1.7);
    rotX = -0.18 + 0.08 * Math.sin(sec * 1.1);
  } else {
    rotY = -0.4 + sec * 0.35;
    bend = 0.06 + 0.04 * Math.sin(sec * 1.3);
    wave = 0.5 * Math.sin(sec * 1.5);
  }
  const intro = introFade ? ease(frame, 0, 0.4 * fps) : 1;

  return (
    <AbsoluteFill style={{ opacity: intro }}>
      <ThreeCanvas
        width={w}
        height={h}
        shadows
        camera={{ fov, position: [0, 0, dist], near: 0.1, far: 100 }}
        gl={{ antialias: true, alpha: true, preserveDrawingBuffer: true }}
      >
        <Env />
        <ambientLight intensity={0.35} />
        <directionalLight
          position={[-2.5, 4, 9]}
          intensity={2.0}
          color="#fff1e4"
          castShadow
          shadow-mapSize-width={1024}
          shadow-mapSize-height={1024}
          shadow-camera-left={-6}
          shadow-camera-right={6}
          shadow-camera-top={6}
          shadow-camera-bottom={-6}
          shadow-radius={16}
        />
        <directionalLight position={[5, 3, -6]} intensity={1.4} color="#e4eeff" />
        <Sheet bend={bend} wave={wave} rotY={rotY} rotX={rotX} y={y} scale={scale} wallShadow={wallShadow} />
      </ThreeCanvas>
    </AbsoluteFill>
  );
};
