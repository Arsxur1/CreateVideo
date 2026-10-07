"""Yafho-Silicare — hero v2 «Окно перестройки» (story version, no voice).

Stage 2 — animatic (3D stills, sketch cards, dashed shot notes):
    python projects/yafho/build_v2.py --animatic
Stage 3 — draft with the animated 3D story:
    python projects/yafho/build_v2.py --draft
Stage 5 — final: music, transitions, all formats + previews:
    python projects/yafho/build_v2.py --final                 # 9x16, 16x9, 4x5
    python projects/yafho/build_v2.py --final --formats 9x16

The story is carried by title sequences (≤ 6 words, held ≥ 2.5 s) and
arrows in the 3D scenes; no voice-over (client decision). Kling shots come
from assets/kling/H0X.mp4, else a «нужен H0X» card.

Scene data: projects/yafho/hero_v2.json (shared with the final build).
Output: output/yafho/v2/<mode>_9x16.mp4 (+ hero_v2_<fmt>.mp4 for --final) + contact sheets.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
ROOT = PROJECT.parent.parent
COMPOSER = ROOT / "remotion-composer"
sys.path.insert(0, str(ROOT))

DATA = PROJECT / "hero_v2.json"
KLING = PROJECT / "assets" / "kling"
OUT = ROOT / "output" / "yafho" / "v2"
PUBLIC_REL = "yafho-v2"  # remotion-composer/public/<PUBLIC_REL> (git-ignored)
PUBLIC = COMPOSER / "public" / PUBLIC_REL
STILL_SECONDS = 9.0  # nominal scene length the still poses are sampled from


def fmt_t(t: float) -> str:
    return f"{int(t // 60)}:{t % 60:04.1f}".replace(".0", "")


def remotion_env() -> dict:
    env = dict(os.environ)
    env.setdefault("REMOTION_GL", "angle")
    return env


def render_still(scene: dict, dest: Path) -> None:
    """Render one 3D pose as a still (1080x1920)."""
    still = scene["still"]
    props = {
        "theme": "yafho-clinical",
        "durationSeconds": STILL_SECONDS,
        "cuts": [{
            "id": scene["id"], "source": "", "in_seconds": 0, "out_seconds": STILL_SECONDS,
            "type": "skin_cross_section_3d", "phase": still["phase"], "introFade": False,
        }],
    }
    props_path = OUT / f".still_{scene['id']}.json"
    props_path.write_text(json.dumps(props, ensure_ascii=False), encoding="utf-8")
    frame = int(still["at"] * (STILL_SECONDS * 30 - 1))
    subprocess.run(
        ["npx", "remotion", "still", "src/index.tsx", "Explainer", str(dest),
         f"--props={props_path}", f"--frame={frame}", "--width=1080", "--height=1920"],
        cwd=COMPOSER, env=remotion_env(), check=True, capture_output=True,
    )
    props_path.unlink()


def clip_seconds(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def build_animatic(data: dict, mode: str = "animatic", fmt: dict | None = None) -> dict:
    PUBLIC.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    cuts: list[dict] = []
    overlays: list[dict] = []

    prev_3d = False
    for s in data["scenes"]:
        cut: dict = {"id": s["id"], "source": "", "in_seconds": s["start"], "out_seconds": s["end"]}
        kind = s["kind"]
        is_3d = kind.startswith("3D") and "phase3d" in s
        if kind == "R":
            clip = KLING / f"{s['kling']}.mp4"
            if clip.exists():
                dest = PUBLIC / clip.name
                shutil.copy2(clip, dest)
                cut["source"] = f"{PUBLIC_REL}/{clip.name}"
                slot = s["end"] - s["start"]
                have = clip_seconds(clip)
                if have < slot - 0.05:  # e.g. a 5 s H08 over a 7.5 s slot → slow it down
                    cut["playbackRate"] = round(have / slot, 3)
            else:
                cut.update(type="text_card", text=f"нужен {s['kling']}", fontSize=48,
                           color="#0F2440", backgroundColor="#ECE6DD")
        elif is_3d and mode in ("draft", "final"):
            # continuous 3D story: no fade between consecutive 3D phases
            cut.update(type="skin_cross_section_3d", phase=s["phase3d"], introFade=not prev_3d)
            cut.update((fmt or {}).get("cut3d", {}))
        elif kind == "3D" and "still" in s:
            png = PUBLIC / f"{s['id']}.png"
            print(f"  still {s['id']} ({s['still']['phase']} @ {s['still']['at']})")
            render_still(s, png)
            cut["source"] = f"{PUBLIC_REL}/{png.name}"
        elif kind == "C":
            cut.update(type="end_card", brand=data.get("brand", "Yafho-Silicare"), handle="@sil.icare",
                       qr=qr_matrix("https://instagram.com/sil.icare"), qrCaption="instagram.com/sil.icare")
        else:  # new 3D scene, not built yet → sketch card
            cut.update(type="text_card", text=f"[эскиз] {s['shot']}", fontSize=42,
                       color="#0F2440", backgroundColor="#ECE6DD")
        if s.get("exit") == "dive" and mode != "animatic":
            cut["exitZoom"] = 1.2
        cuts.append(cut)
        prev_3d = is_3d

        # title sequence: each title holds until the next one (or the cut end)
        titles = s.get("titles", [])
        dur = s["end"] - s["start"]
        for i, t in enumerate(titles):
            t_in = s["start"] + t["at"] * dur + (0.3 if t["at"] == 0 else 0)
            t_out = s["start"] + titles[i + 1]["at"] * dur if i + 1 < len(titles) else s["end"]
            ov = {"type": "thesis", "text": t["text"], "variant": "dark", "in_seconds": round(t_in, 2), "out_seconds": round(t_out, 2)}
            if t.get("footnote") and s.get("footnote"):
                ov["subtitle"] = s["footnote"]
            overlays.append(ov)
        if s.get("timeline"):
            overlays.append({"type": "healing_timeline", "in_seconds": s["start"], "out_seconds": s["end"], **s["timeline"]})
        if s.get("stat"):
            st = s["stat"]
            overlays.append({"type": "stat_badge", "value": st["value"], "label": st["label"], "source": st["source"],
                             "position": (fmt or {}).get("stat_position", st.get("position", "upper")),
                             "in_seconds": s["start"] + 1.5, "out_seconds": s["end"]})
        if s.get("margin"):
            m = s["margin"] if isinstance(s["margin"], dict) else {}
            overlays.append({"type": "margin_overlay", "label": "+1 см", "in_seconds": s["start"] + 0.3, "out_seconds": s["end"], **m})
        if mode == "animatic":
            overlays.append({"type": "animatic_note", "label": f"{s['id']} · {fmt_t(s['start'])}–{fmt_t(s['end'])} · {kind}",
                             "text": s.get("notes"), "in_seconds": s["start"], "out_seconds": s["end"]})

    props: dict = {
        "version": "1.0", "renderer_family": "explainer-data", "render_runtime": "remotion",
        "theme": "yafho-clinical", "playbook": "yafho-clinical",
        "durationSeconds": data["duration"], "cuts": cuts, "overlays": overlays, "audio": {},
    }
    music = data.get("music")
    track = PROJECT / "assets" / "music" / music["file"] if music else None
    if mode == "final" and track and track.exists():
        shutil.copy2(track, PUBLIC / track.name)
        props["audio"]["music"] = {"src": f"{PUBLIC_REL}/{track.name}", "volume": music.get("volume", 1.0),
                                   "fadeInSeconds": music.get("fadeInSeconds", 0.5),
                                   "fadeOutSeconds": music.get("fadeOutSeconds", 2.0)}
    if fmt:
        props["layout"] = fmt.get("layout", "full")
    return {"props": props}


def qr_matrix(url: str) -> list[list[int]]:
    import qrcode

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
    qr.add_data(url)
    qr.make(fit=True)
    return [[int(v) for v in row] for row in qr.get_matrix()]


def render(props: dict, out: Path, profile: str) -> None:
    from tools.video.video_compose import VideoCompose

    os.environ.setdefault("REMOTION_GL", "angle")
    res = VideoCompose().execute({"operation": "remotion_render", "edit_decisions": props,
                                  "output_path": str(out), "profile": profile})
    if not res.success:
        raise SystemExit(f"render failed: {res.error}")


def contact_sheet(video: Path, scenes: list[dict], dest: Path) -> None:
    w, h = (int(v) for v in subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0",
         str(video)], capture_output=True, text=True, check=True).stdout.strip().split(","))
    th = 480
    tw = int(round(th * w / h / 2) * 2)
    frames = []
    for s in scenes:
        png = dest.parent / f"_{s['id']}.png"
        t = s["start"] + (s["end"] - s["start"]) * 0.7
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(video),
                        "-frames:v", "1", "-vf", f"scale={tw}:{th}", str(png)], check=True)
        frames.append(png)
    cols = 7 if w < h else 4
    rows = (len(frames) + cols - 1) // cols
    inputs = sum((["-i", str(p)] for p in frames), [])
    pad = cols * rows - len(frames)
    chain = "".join(f"[{i}:v]" for i in range(len(frames)))
    if pad:
        inputs += ["-f", "lavfi", "-i", f"color=c=0xFBFAF7:s={tw}x{th}:d=1"]
        chain = "".join(f"[{i}:v]" for i in range(len(frames)))
        chain = f"[{len(frames)}:v]split={pad}" + "".join(f"[p{k}]" for k in range(pad)) + ";" + chain + "".join(f"[p{k}]" for k in range(pad))
    layout = "|".join(f"{c * tw}_{r * th}" for r in range(rows) for c in range(cols))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex",
                    f"{chain}xstack=inputs={cols * rows}:layout={layout}", "-frames:v", "1", str(dest)], check=True)
    for p in frames:
        p.unlink()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--animatic", action="store_true", help="stills + notes (stage 2, default)")
    ap.add_argument("--draft", action="store_true", help="animated 3D story, no notes (stage 3)")
    ap.add_argument("--final", action="store_true", help="music + transitions, all formats (stage 5)")
    ap.add_argument("--formats", default="9x16,16x9,4x5", help="comma list for --final")
    args = ap.parse_args()

    data = json.loads(DATA.read_text(encoding="utf-8"))
    if args.final:
        for key in [f.strip() for f in args.formats.split(",") if f.strip()]:
            fmt = data["formats"][key]
            print(f"final {key}: building scenes")
            built = build_animatic(data, mode="final", fmt=fmt)
            (OUT / f"final_props_{key}.json").write_text(json.dumps(built["props"], ensure_ascii=False, indent=2), encoding="utf-8")
            video = OUT / f"hero_v2_{key}.mp4"
            print(f"final {key}: rendering ({fmt['profile']})")
            render(built["props"], video, fmt["profile"])
            contact_sheet(video, data["scenes"], OUT / f"hero_v2_{key}_sheet.png")
            print(f"→ {video.relative_to(ROOT)}")
        return

    mode = "draft" if args.draft else "animatic"
    print(f"{mode}: building scenes")
    built = build_animatic(data, mode=mode)
    (OUT / f"{mode}_props.json").write_text(json.dumps(built["props"], ensure_ascii=False, indent=2), encoding="utf-8")

    video = OUT / f"{mode}_9x16.mp4"
    print(f"{mode}: rendering 9:16")
    render(built["props"], video, "instagram_reels")
    contact_sheet(video, data["scenes"], OUT / f"{mode}_sheet.png")
    print(f"→ {video.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
