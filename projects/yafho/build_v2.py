"""Yafho SiliSkin — hero v2 «Окно перестройки» (story version).

Stage 2 — animatic (this script, default):
    python projects/yafho/build_v2.py --animatic
  * 3D scenes → stills rendered from SkinCrossSection3D (fast, no animation)
  * new 3D scenes → sketch cards with the shot description
  * Kling shots → the clip if present in assets/kling/, else a «нужен H0X» card
  * healing timeline, titles, stat card and a dashed note with shot number + VO line
  * scratch voice (espeak-ng, robotic — only for timing) and a timing report

Scene data: projects/yafho/hero_v2.json (shared with the final build).
Output: output/yafho/v2/animatic_9x16.mp4, contact sheet, timing report.
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
VO_LEAD = 0.3  # voice starts this long after the scene cut


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


def scratch_voice(scenes: list[dict]) -> tuple[Path, list[dict]]:
    """espeak-ng female voice per line, placed at scene start + VO_LEAD."""
    tmp = OUT / "vo"
    tmp.mkdir(parents=True, exist_ok=True)
    report = []
    inputs: list[str] = []
    filters: list[str] = []
    for i, s in enumerate(scenes):
        wav = tmp / f"{s['id']}.wav"
        subprocess.run(["espeak-ng", "-v", "ru+f3", "-s", "150", "-w", str(wav), s["vo"]], check=True)
        dur = float(subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(wav)],
            capture_output=True, text=True, check=True).stdout.strip())
        slot = s["end"] - s["start"] - VO_LEAD
        report.append({"id": s["id"], "vo": s["vo"], "dur": dur, "slot": slot, "fits": dur <= slot})
        inputs += ["-i", str(wav)]
        delay = int((s["start"] + VO_LEAD) * 1000)
        filters.append(f"[{i}:a]adelay={delay}|{delay}[a{i}]")
    mix = "".join(f"[a{i}]" for i in range(len(scenes)))
    dest = PUBLIC / "vo_scratch.wav"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex",
         ";".join(filters) + f";{mix}amix=inputs={len(scenes)}:normalize=0[out]", "-map", "[out]", str(dest)],
        check=True,
    )
    return dest, report


def build_animatic(data: dict, with_voice: bool) -> dict:
    PUBLIC.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    cuts: list[dict] = []
    overlays: list[dict] = []

    for s in data["scenes"]:
        cut: dict = {"id": s["id"], "source": "", "in_seconds": s["start"], "out_seconds": s["end"]}
        kind = s["kind"]
        if kind == "R":
            clip = KLING / f"{s['kling']}.mp4"
            if clip.exists():
                dest = PUBLIC / clip.name
                shutil.copy2(clip, dest)
                cut["source"] = f"{PUBLIC_REL}/{clip.name}"
            else:
                cut.update(type="text_card", text=f"нужен {s['kling']}", fontSize=48,
                           color="#0F2440", backgroundColor="#ECE6DD")
        elif kind == "3D" and "still" in s:
            png = PUBLIC / f"{s['id']}.png"
            print(f"  still {s['id']} ({s['still']['phase']} @ {s['still']['at']})")
            render_still(s, png)
            cut["source"] = f"{PUBLIC_REL}/{png.name}"
        elif kind == "C":
            cut.update(type="end_card", brand="Yafho SiliSkin", handle="@sil.icare")
        else:  # new 3D scene, not built yet → sketch card
            cut.update(type="text_card", text=f"[эскиз] {s['shot']}", fontSize=42,
                       color="#0F2440", backgroundColor="#ECE6DD")
        cuts.append(cut)

        if s.get("title") and kind != "C":
            ov = {"type": "thesis", "text": s["title"], "variant": "dark",
                  "in_seconds": s["start"] + 0.3, "out_seconds": s["end"]}
            if s.get("footnote"):
                ov["subtitle"] = s["footnote"]
            overlays.append(ov)
        if s.get("timeline"):
            overlays.append({"type": "healing_timeline", "in_seconds": s["start"], "out_seconds": s["end"], **s["timeline"]})
        if s.get("stat"):
            st = s["stat"]
            overlays.append({"type": "stat_badge", "value": st["value"], "label": st["label"], "source": st["source"],
                             "in_seconds": s["start"] + 1.5, "out_seconds": s["end"]})
        if s.get("margin"):
            overlays.append({"type": "margin_overlay", "label": "+1 см", "in_seconds": s["start"] + 0.3, "out_seconds": s["end"]})
        overlays.append({"type": "animatic_note", "label": f"{s['id']} · {fmt_t(s['start'])}–{fmt_t(s['end'])} · {kind}",
                         "text": s["vo"], "in_seconds": s["start"], "out_seconds": s["end"]})

    props: dict = {
        "version": "1.0", "renderer_family": "explainer-data", "render_runtime": "remotion",
        "theme": "yafho-clinical", "playbook": "yafho-clinical",
        "durationSeconds": data["duration"], "cuts": cuts, "overlays": overlays, "audio": {},
    }
    report = []
    if with_voice:
        vo, report = scratch_voice(data["scenes"])
        props["audio"]["narration"] = {"src": f"{PUBLIC_REL}/{vo.name}", "volume": 1}
    return {"props": props, "report": report}


def render(props: dict, out: Path, profile: str) -> None:
    from tools.video.video_compose import VideoCompose

    os.environ.setdefault("REMOTION_GL", "angle")
    res = VideoCompose().execute({"operation": "remotion_render", "edit_decisions": props,
                                  "output_path": str(out), "profile": profile})
    if not res.success:
        raise SystemExit(f"render failed: {res.error}")


def contact_sheet(video: Path, scenes: list[dict], dest: Path) -> None:
    frames = []
    for s in scenes:
        png = dest.parent / f"_{s['id']}.png"
        t = s["start"] + (s["end"] - s["start"]) * 0.7
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(video),
                        "-frames:v", "1", "-vf", "scale=-2:480", str(png)], check=True)
        frames.append(png)
    cols = 7
    rows = (len(frames) + cols - 1) // cols
    inputs = sum((["-i", str(p)] for p in frames), [])
    pad = cols * rows - len(frames)
    chain = "".join(f"[{i}:v]" for i in range(len(frames)))
    if pad:
        inputs += ["-f", "lavfi", "-i", f"color=c=0xFBFAF7:s=270x480:d=1"]
        chain += "".join(f"[{len(frames)}:v]" for _ in range(pad))
    layout = "|".join(f"{c * 270}_{r * 480}" for r in range(rows) for c in range(cols))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex",
                    f"{chain}xstack=inputs={cols * rows}:layout={layout}", "-frames:v", "1", str(dest)], check=True)
    for p in frames:
        p.unlink()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--animatic", action="store_true", default=True)
    ap.add_argument("--no-voice", action="store_true", help="skip the espeak-ng scratch voice")
    args = ap.parse_args()

    data = json.loads(DATA.read_text(encoding="utf-8"))
    print("animatic: building scenes")
    built = build_animatic(data, with_voice=not args.no_voice and shutil.which("espeak-ng") is not None)
    (OUT / "animatic_props.json").write_text(json.dumps(built["props"], ensure_ascii=False, indent=2), encoding="utf-8")

    if built["report"]:
        lines = ["| Сцена | Слот, с | Голос (черновой), с | Влезает |", "|---|---|---|---|"]
        for r in built["report"]:
            lines.append(f"| {r['id']} | {r['slot']:.1f} | {r['dur']:.1f} | {'да' if r['fits'] else '**нет**'} |")
        (OUT / "timing_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("\n".join(lines))

    video = OUT / "animatic_9x16.mp4"
    print("animatic: rendering 9:16")
    render(built["props"], video, "instagram_reels")
    contact_sheet(video, data["scenes"], OUT / "animatic_sheet.png")
    print(f"→ {video.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
