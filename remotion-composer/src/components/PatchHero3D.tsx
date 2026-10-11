import React, { useEffect, useMemo, useState } from "react";
import { AbsoluteFill, cancelRender, continueRender, delayRender, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import { useThree } from "@react-three/fiber";
import * as THREE from "three";
import { RoomEnvironment } from "three/examples/jsm/environments/RoomEnvironment.js";
import { ease, useCanvas } from "./yafho/tokens";

export interface PatchHero3DProps {
  /** Vertical centre of the action as a fraction of the canvas (leave room for titles). */
  centerY?: number;
  /** Sheet length as a fraction of the canvas height. */
  size?: number;
  /** "flex": floats over the skin, bends, springs back and lands on the scar (topic 01); "spin": slow turn (end card). */
  motion?: "flex" | "spin";
  /** Kept for API compatibility: soft shadows fall on the skin surface. */
  wallShadow?: boolean;
  introFade?: boolean;
}

// Skin photo from make_skin.py: 1600 px = 26.67 cm. World unit = 1 cm.
const SKIN_CM = 1600 / 60;
const SHEET_W = 4;
const SHEET_L = 13;
const SEG_X = 24;
const SEG_Z = 72;

/** Rounded-rect sheet texture: matte silicone inside, a brighter moulded rim. */
function sheetTextures(): { map: THREE.CanvasTexture; alpha: THREE.CanvasTexture } {
  const px = 256;
  const py = Math.round((px * SHEET_L) / SHEET_W);
  const r = px * 0.12;
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
  ac.fillStyle = "#9a9a9a"; // interior: more see-through than the rim
  rr(ac, 9);
  ac.fill();

  const m = document.createElement("canvas");
  m.width = px;
  m.height = py;
  const mc = m.getContext("2d")!;
  mc.fillStyle = "#f3efe9";
  mc.fillRect(0, 0, px, py);
  mc.strokeStyle = "#ffffff";
  mc.lineWidth = 6;
  rr(mc, 5);
  mc.stroke();
  const map = new THREE.CanvasTexture(m);
  map.colorSpace = THREE.SRGBColorSpace;
  return { map, alpha: new THREE.CanvasTexture(a) };
}

/** Skin photo under the sheet. Lives inside the canvas: during rendering R3F only
 * draws on `advance`, so we advance once the texture is in the scene. */
const SkinPlane: React.FC<{ url: string }> = ({ url }) => {
  const { advance } = useThree();
  const [handle] = useState(() => delayRender(`skin texture ${url}`));
  const [tex, setTex] = useState<THREE.Texture | null>(null);
  useEffect(() => {
    new THREE.TextureLoader().load(
      url,
      (t) => {
        t.colorSpace = THREE.SRGBColorSpace;
        t.anisotropy = 8;
        t.wrapS = THREE.RepeatWrapping;
        t.wrapT = THREE.RepeatWrapping;
        t.repeat.set(2, 2);
        t.offset.set(0.5, 0.5);
        setTex(t);
      },
      undefined,
      // a missing skin texture must fail the render, not silently float the sheet over nothing
      () => cancelRender(new Error(`PatchHero3D: cannot load ${url}`)),
    );
  }, [url, handle]);
  useEffect(() => {
    if (!tex) return;
    advance(performance.now());
    continueRender(handle);
  }, [tex, handle, advance]);
  if (!tex) return null;
  return (
    <mesh rotation-x={-Math.PI / 2} receiveShadow>
      {/* 2×2 tiles at true scale (1 unit = 1 cm), scar tile centred */}
      <planeGeometry args={[SKIN_CM * 2, SKIN_CM * 2]} />
      {/* the photo already carries its light: Lambert at ~unit irradiance, no tone mapping, keeps the soft shadow */}
      <meshLambertMaterial map={tex} toneMapped={false} />
    </mesh>
  );
};

const Env: React.FC = () => {
  const { gl, scene } = useThree();
  useMemo(() => {
    const pmrem = new THREE.PMREMGenerator(gl);
    scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
    scene.environmentIntensity = 1.0;
    gl.toneMapping = THREE.ACESFilmicToneMapping;
    gl.toneMappingExposure = 1.0;
    gl.shadowMap.enabled = true;
    gl.shadowMap.type = THREE.VSMShadowMap;
  }, [gl, scene]);
  return null;
};

const Rig: React.FC<{ target: [number, number, number]; pos: [number, number, number] }> = ({ target, pos }) => {
  const { camera } = useThree();
  camera.position.set(...pos);
  camera.lookAt(...target);
  camera.updateProjectionMatrix();
  return null;
};

const Sheet: React.FC<{ y: number; bend: number; wave: number; rotY: number; tilt: number }> = ({ y, bend, wave, rotY, tilt }) => {
  const { geo, base } = useMemo(() => {
    const g = new THREE.PlaneGeometry(SHEET_W, SHEET_L, SEG_X, SEG_Z);
    g.rotateX(-Math.PI / 2); // lie flat in XZ
    return { geo: g, base: Float32Array.from(g.attributes.position.array as Float32Array) };
  }, []);
  const tex = useMemo(() => sheetTextures(), []);
  const pos = geo.attributes.position as THREE.BufferAttribute;
  for (let i = 0; i < pos.count; i++) {
    const x = base[i * 3];
    const z = base[i * 3 + 2];
    const zn = z / (SHEET_L / 2);
    // bend > 0: ends lift (soft U), bend < 0: middle lifts; wave: travelling ripple
    const h = bend * zn * zn * 1.6 + wave * 0.35 * Math.sin(zn * 3.2 + x * 0.15);
    pos.setXYZ(i, x, h, z);
  }
  pos.needsUpdate = true;
  geo.computeVertexNormals();
  return (
    <group position={[0, y, 0]} rotation={[tilt, rotY, 0]}>
      <mesh geometry={geo} castShadow>
        <meshPhysicalMaterial
          color="#f6f2ec"
          map={tex.map}
          alphaMap={tex.alpha}
          transparent
          opacity={0.9}
          roughness={0.22}
          metalness={0}
          clearcoat={1}
          clearcoatRoughness={0.18}
          side={THREE.DoubleSide}
          depthWrite={false}
        />
      </mesh>
    </group>
  );
};

/**
 * Topic 01 / 09: the Yafho-Silicare sheet as a hero object. "flex": a
 * translucent medical-silicone sheet floats over real-looking skin, bends and
 * springs back (soft, flexible), then settles onto the scar with a soft
 * shadow. "spin": the same sheet turning slowly on its own (behind the end
 * card). Realistic light (3D exception); text and logo stay in code overlays.
 */
export const PatchHero3D: React.FC<PatchHero3DProps> = ({ centerY = 0.36, size = 0.5, motion = "flex", introFade = false }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const { width, height } = useCanvas();
  const w = Math.round(width);
  const h = Math.round(height);
  const t = frame / Math.max(1, durationInFrames - 1);
  const sec = frame / fps;
  const onSkin = motion === "flex";

  // Camera: looking down at the forearm at ~50°, framed so the sheet spans `size` of the height.
  const fov = 30;
  const visH = SHEET_L / size; // world cm across the frame height (at the target)
  const dist = visH / 2 / Math.tan(((fov / 2) * Math.PI) / 180) * 0.62;
  const elev = onSkin ? 0.95 : 1.25; // radians above the surface
  const shiftZ = (0.5 - centerY) * visH * 0.9; // target nearer the camera → action higher on screen
  const target: [number, number, number] = [0, 0, shiftZ];
  const camPos: [number, number, number] = [0, Math.sin(elev) * dist, shiftZ + Math.cos(elev) * dist];

  let y = 0;
  let bend = 0;
  let wave = 0;
  let rotY = 0;
  let tilt = 0;
  if (motion === "flex") {
    const enter = ease(t, 0, 0.18);
    const land = ease(t, 0.62, 0.86);
    y = (1 - enter) * 9 + (1 - land) * 3.2 + 0.05;
    rotY = -0.45 * (1 - enter) + 0.18 * Math.sin(sec * 1.1) * (1 - land) - 0.08 * land;
    tilt = 0.12 * Math.sin(sec * 1.4) * (1 - land);
    // flex: bends (ends up) and springs back twice, then lies flat
    const flex = Math.sin(Math.min(1, Math.max(0, (t - 0.16) / 0.46)) * Math.PI * 2);
    bend = 1.1 * flex * (1 - land) + (t > 0.86 ? 0.08 * Math.exp(-(t - 0.86) * 30) * Math.cos((t - 0.86) * 90) : 0);
    wave = 0.6 * Math.sin(sec * 2.2) * (1 - land);
  } else {
    y = 1.5;
    rotY = -0.4 + sec * 0.35;
    bend = 0.5 + 0.3 * Math.sin(sec * 1.3);
    wave = 0.4 * Math.sin(sec * 1.5);
    tilt = 0.25;
  }
  const intro = introFade ? ease(frame, 0, 0.4 * fps) : 1;

  return (
    <AbsoluteFill style={{ opacity: intro }}>
      <ThreeCanvas
        width={w}
        height={h}
        shadows
        camera={{ fov, position: camPos, near: 0.5, far: 400 }}
        gl={{ antialias: true, alpha: true, preserveDrawingBuffer: true }}
      >
        <Env />
        <Rig target={target} pos={camPos} />
        <ambientLight intensity={2.0} />
        <directionalLight
          position={[-14, 30, 10]}
          intensity={1.25}
          color="#fff1e4"
          castShadow
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
          shadow-camera-left={-20}
          shadow-camera-right={20}
          shadow-camera-top={20}
          shadow-camera-bottom={-20}
          shadow-radius={14}
          shadow-blurSamples={20}
          shadow-bias={-0.0005}
        />
        <directionalLight position={[12, 8, -16]} intensity={0.9} color="#e4eeff" />
        {onSkin && <SkinPlane url={staticFile("yafho-skin/skin_line_fresh.png")} />}
        {!onSkin && (
          <mesh rotation-x={-Math.PI / 2} receiveShadow position={[0, -0.01, 0]}>
            <planeGeometry args={[200, 200]} />
            <shadowMaterial opacity={0.25} />
          </mesh>
        )}
        <Sheet y={y} bend={bend} wave={wave} rotY={rotY} tilt={tilt} />
      </ThreeCanvas>
    </AbsoluteFill>
  );
};
