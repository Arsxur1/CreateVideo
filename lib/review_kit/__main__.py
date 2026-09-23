"""CLI for the review kit. Every command works on projects/<slug>/.

    python -m lib.review_kit providers
    python -m lib.review_kit new <slug> --title "..." --source "<folder>" (--theme <name> | --fresh)
    python -m lib.review_kit prep <slug> [--force]
    python -m lib.review_kit voice <slug> [--only hook,verdict]
    python -m lib.review_kit captions <slug>
    python -m lib.review_kit sfx <slug>
    python -m lib.review_kit music <slug> --query "dreamy lofi" --name dreamy
    python -m lib.review_kit props <slug>
    python -m lib.review_kit validate <slug>
    python -m lib.review_kit stills <slug> [--cover]
    python -m lib.review_kit render <slug> [--draft]
    python -m lib.review_kit review <slug>

Inputs the agent writes into artifacts/ (see skills/creative/review-kit.md):
    prep.json   clips, photos and 4K crops to prepare (created by `new`, then edited)
    lines.json  [{"id", "text" (spoken), "captions": [one chunk per spoken sentence]}]
    shots.json  {"music", "shots": [...], "sfx": [...], "cover": {...}}
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from lib.env_loader import load_env  # noqa: E402

load_env()

PROJECTS = REPO_ROOT / "projects"
TEMPLATE = REPO_ROOT / "templates" / "review-reel"
COMPOSER = REPO_ROOT / "remotion-composer"
TEMPLATE_FILES = ("index.tsx", "Root.tsx", "Composition.tsx", "fonts.ts")
COMPOSITION_ID = "ReviewReel"
COVER_ID = "ReviewCover"


class KitError(Exception):
    pass


def _paths(slug: str) -> dict[str, Path]:
    p = PROJECTS / slug
    if not p.exists():
        raise KitError(f"projects/{slug} not found. Start with `new`.")
    return {"project": p, "art": p / "artifacts", "public": p / "public", "assets": p / "assets", "delivery": p / "delivery"}


def _read(path: Path, what: str) -> Any:
    if not path.exists():
        raise KitError(f"{path.relative_to(REPO_ROOT)} is missing ({what}).")
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _theme(paths: dict[str, Path]) -> dict[str, Any]:
    return _read(paths["art"] / "theme.json", "apply a theme with `python -m lib.themes apply <name> --project <slug>`")


# ---------------------------------------------------------------- commands

def cmd_providers(_: argparse.Namespace) -> None:
    from lib.review_kit.providers import check_all

    for name, res in check_all().items():
        print(f"{'OK ' if res['ok'] else 'NO '} {name:<11} {res['detail']}")


def cmd_new(args: argparse.Namespace) -> None:
    from lib.checkpoint import init_project
    from lib.review_kit.media import inventory

    if bool(args.theme) == bool(args.fresh):
        raise KitError("Pick one: --theme <name> for a saved channel look, or --fresh for a one-off atelier look.")
    source = Path(args.source).resolve()
    if not source.is_dir():
        raise KitError(f"--source {source} is not a folder.")
    project = init_project(args.slug, title=args.title, pipeline_type=args.pipeline)
    art = project / "artifacts"
    art.mkdir(exist_ok=True)
    _write(art / "prep.json", inventory(source))
    if args.theme:
        from lib.themes import apply_theme

        apply_theme(args.theme, args.slug)
        for name in TEMPLATE_FILES:
            shutil.copy2(TEMPLATE / name, project / name)
        theme = _theme({"art": art})
        (project / "art-direction.md").write_text(
            f"# Art direction: channel theme `{theme['name']}`\n\n{theme.get('description', '')}\n\n"
            "Look is fixed by the theme snapshot in artifacts/theme.json. Per-video creative work is the "
            "shot list (artifacts/shots.json): pick shots, crops and overlays that fit this product.\n",
            encoding="utf-8")
        mode = f"theme '{args.theme}' (template: templates/review-reel)"
    else:
        subprocess.run([sys.executable, str(REPO_ROOT / "scripts" / "scaffold_atelier_project.py"), args.slug], check=True)
        mode = "fresh atelier scaffold (author Composition.tsx by hand)"
    print(f"created projects/{args.slug} with {mode}")
    print(f"edit artifacts/prep.json to add 4K crops, then run `prep {args.slug}`")


def cmd_prep(args: argparse.Namespace) -> None:
    from lib.review_kit.media import run_prep

    paths = _paths(args.slug)
    plan = _read(paths["art"] / "prep.json", "created by `new`")
    done = run_prep(plan, paths["public"], paths["project"] / "build", force=args.force)
    _write(paths["art"] / "prep.json", plan)  # records resolved crop times
    print(f"prepared {len(done)} files in public/")
    for crop, info in plan.get("crops", {}).items():
        r = info.get("resolved", {})
        warn = "  (soft: over 1.6x upscale, widen the crop)" if r.get("upscale", 0) > 1.6 else ""
        print(f"  crop {crop}: frame {r.get('time')}s, {r.get('upscale')}x upscale{warn}")


def cmd_voice(args: argparse.Namespace) -> None:
    from lib.review_kit.narration import process_line, stitch, synthesize_lines

    paths = _paths(args.slug)
    lines = _read(paths["art"] / "lines.json", "narration lines from the approved script")
    voice = _theme(paths)["voice"] if (paths["art"] / "theme.json").exists() else _read(paths["art"] / "voice.json", "voice settings")
    raw_dir = paths["assets"] / "audio" / "narration"
    only = set(args.only.split(",")) if args.only else None
    raw = synthesize_lines(lines, voice, raw_dir, only=only)
    processed = []
    for src in raw:
        out = raw_dir / "proc" / (src.stem + ".wav")
        process_line(src, out, float(voice.get("tempo", 1.0)))
        processed.append(out)
    result = stitch(lines, processed, paths["public"] / "audio" / "narration.wav",
                    lead=float(voice.get("lead_seconds", 0.4)), gap=float(voice.get("gap_seconds", 0.35)))
    _write(paths["art"] / "timeline.json", result)
    print(f"narration {result['voice_seconds']}s over {len(lines)} lines -> public/audio/narration.wav")


def cmd_captions(args: argparse.Namespace) -> None:
    from lib.review_kit.captions import time_captions, to_srt

    paths = _paths(args.slug)
    lines = _read(paths["art"] / "lines.json", "narration lines")
    timeline = _read(paths["art"] / "timeline.json", "run `voice` first")["timeline"]
    theme = _read(paths["art"] / "theme.json", "theme") if (paths["art"] / "theme.json").exists() else {}
    max_chars = theme.get("captions", {}).get("max_chars", 52)
    captions = time_captions(lines, timeline, max_chars=max_chars)
    _write(paths["art"] / "captions.json", captions)
    offset = theme.get("intro", {}).get("cover_seconds", 0.0)
    srt = paths["delivery"] / f"{args.slug}-captions.srt"
    srt.parent.mkdir(parents=True, exist_ok=True)
    srt.write_text(to_srt(captions, offset), encoding="utf-8")
    print(f"{len(captions)} captions -> artifacts/captions.json and {srt.relative_to(REPO_ROOT)}")


def cmd_sfx(args: argparse.Namespace) -> None:
    from lib.review_kit.sfx import write_all

    paths = _paths(args.slug)
    print("sfx:", ", ".join(write_all(paths["public"] / "audio" / "sfx")))


def cmd_music(args: argparse.Namespace) -> None:
    from tools.audio.pixabay_music import PixabayMusic

    paths = _paths(args.slug)
    out = paths["public"] / "audio" / "music" / f"{args.name}.mp3"
    out.parent.mkdir(parents=True, exist_ok=True)
    res = PixabayMusic().execute({"query": args.query, "min_duration": args.min_duration, "max_duration": 300, "output_path": str(out)})
    if not res.success:
        raise KitError(f"music search failed: {res.error}")
    preview = paths["assets"] / "music" / "previews" / f"{args.name}-20s.mp3"
    preview.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "15", "-t", "20", "-i", str(out), "-af",
                    "afade=t=in:d=0.5,afade=t=out:st=19:d=1", "-b:a", "160k", str(preview)], check=True)
    d = res.data or {}
    print(f"{d.get('track_title')} by {d.get('artist')} -> public/audio/music/{args.name}.mp3 (preview: {preview.relative_to(REPO_ROOT)})")
    print(f"licence: {d.get('license')}")


def _check_shots(shots_doc: dict[str, Any], public: Path, duration: float) -> list[str]:
    problems = []
    shots = shots_doc.get("shots", [])
    if not shots:
        return ["shots.json has no shots"]
    prev_end = 0.0
    for s in shots:
        if s["to"] <= s["from"]:
            problems.append(f"{s['id']}: 'to' must be after 'from'")
        if abs(s["from"] - prev_end) > 0.05:
            problems.append(f"{s['id']}: starts at {s['from']}s but previous shot ends at {prev_end}s (gap or overlap)")
        prev_end = s["to"]
        if not (public / s["media"]["src"]).exists():
            problems.append(f"{s['id']}: media {s['media']['src']} not found in public/")
        if s.get("enter") == "aperture" and not s.get("aperture"):
            problems.append(f"{s['id']}: enter=aperture needs aperture {{cx, cy}}")
    if prev_end + 0.05 < duration:
        problems.append(f"shots end at {prev_end}s but the reel runs {duration}s (black tail)")
    music = shots_doc.get("music")
    if music and not (public / music).exists():
        problems.append(f"music {music} not found in public/")
    return problems


def cmd_props(args: argparse.Namespace) -> None:
    paths = _paths(args.slug)
    theme = _theme(paths)
    tl = _read(paths["art"] / "timeline.json", "run `voice` first")
    captions = _read(paths["art"] / "captions.json", "run `captions` first")
    shots_doc = _read(paths["art"] / "shots.json", "the shot list")
    problems = _check_shots(shots_doc, paths["public"], tl["duration_seconds"])
    if problems:
        raise KitError("shots.json problems:\n  - " + "\n  - ".join(problems))
    audio = theme["audio"]
    props = {
        "durationSeconds": tl["duration_seconds"],
        "theme": {k: theme[k] for k in ("palette", "fonts", "captions", "tags", "motion", "signature", "intro")},
        "narration": "audio/narration.wav",
        "music": shots_doc.get("music"),
        "musicVolume": audio["music_volume"],
        "musicDuckedVolume": audio["music_ducked_volume"],
        "timeline": [{k: s[k] for k in ("id", "start", "end")} for s in tl["timeline"]],
        "captions": [{k: c[k] for k in ("text", "start", "end")} for c in captions],
        "shots": shots_doc["shots"],
        "sfx": shots_doc.get("sfx", []) if audio.get("sfx", True) else [],
        "cover": shots_doc.get("cover", {"kicker": "", "title": "", "subtitle": "", "image": ""}),
    }
    _write(paths["art"] / "props.json", props)
    print(f"props.json: {len(props['shots'])} shots, {len(props['captions'])} captions, {props['durationSeconds']}s")


def cmd_validate(args: argparse.Namespace) -> None:
    from lib.themes import ThemeError, validate_theme
    from schemas.artifacts import ARTIFACT_NAMES, validate_artifact

    paths = _paths(args.slug)
    failures = 0
    for f in sorted(paths["art"].glob("*.json")):
        if f.stem in ARTIFACT_NAMES:
            try:
                validate_artifact(f.stem, json.loads(f.read_text(encoding="utf-8")))
                print(f"ok    {f.name}")
            except Exception as exc:  # noqa: BLE001
                failures += 1
                print(f"FAIL  {f.name}: {str(exc).splitlines()[0]}")
    theme_file = paths["art"] / "theme.json"
    if theme_file.exists():
        theme = json.loads(theme_file.read_text(encoding="utf-8"))
        try:
            validate_theme(theme)
            print("ok    theme.json")
        except ThemeError as exc:
            failures += 1
            print(f"FAIL  theme.json: {exc}")
    if failures:
        raise KitError(f"{failures} artifact(s) failed validation")


def _stage(paths: dict[str, Path]) -> Path:
    """Copy the project's .tsx/.ts into remotion-composer so a raw still/render sees current code."""
    from tools.video.video_compose import VideoCompose

    return VideoCompose()._stage_atelier_project(paths["project"] / "index.tsx", COMPOSER)


def _npx() -> str:
    return shutil.which("npx") or "npx"


def _still(entry: Path, comp_id: str, frame: int, out: Path, props: Path, public: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run([_npx(), "remotion", "still", str(entry), comp_id, str(out), f"--frame={frame}",
                           f"--props={props}", f"--public-dir={public}"], cwd=COMPOSER, capture_output=True, text=True)
    if proc.returncode != 0 or not out.exists():
        raise KitError(f"still {out.name} failed: {(proc.stderr or proc.stdout)[-400:]}")


def _contact_sheet(files: list[Path], out: Path, cols: int = 10, size: tuple[int, int] = (270, 480)) -> Path:
    from PIL import Image

    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (size[0] + 4), rows * (size[1] + 4)), "black")
    for i, f in enumerate(files):
        thumb = Image.open(f).convert("RGB").resize(size)
        sheet.paste(thumb, ((i % cols) * (size[0] + 4), (i // cols) * (size[1] + 4)))
    sheet.save(out, quality=88)
    return out


def cmd_stills(args: argparse.Namespace) -> None:
    paths = _paths(args.slug)
    props_path = paths["art"] / "props.json"
    props = _read(props_path, "run `props` first")
    entry = _stage(paths)
    offset = props["theme"].get("intro", {}).get("cover_seconds", 0.0)
    snaps = paths["project"] / "snapshots"
    for shot in props["shots"]:
        mid = offset + (shot["from"] + shot["to"]) / 2
        _still(entry, COMPOSITION_ID, round(mid * 30), snaps / f"{shot['id']}.png", props_path, paths["public"])
        print(f"  {shot['id']} @ {mid:.2f}s")
    sheet = _contact_sheet(sorted(snaps.glob("s*.png")), snaps / "contact-sheet.jpg")
    print(f"stills + contact sheet -> {snaps.relative_to(REPO_ROOT)}")
    if args.cover:
        cover = paths["delivery"] / "instagram" / f"{args.slug}-cover.png"
        _still(entry, COVER_ID, 0, cover, props_path, paths["public"])
        print(f"cover -> {cover.relative_to(REPO_ROOT)}")


def cmd_render(args: argparse.Namespace) -> None:
    from schemas.artifacts import validate_artifact
    from tools.video.video_compose import VideoCompose

    paths = _paths(args.slug)
    theme = _theme(paths)
    art = paths["art"]
    ed_path = art / "edit_decisions.json"
    edit = json.loads(ed_path.read_text(encoding="utf-8")) if ed_path.exists() else {
        "version": "1.0", "render_runtime": "remotion", "composition_mode": "atelier", "renderer_family": "product-reveal",
        "cuts": [], "subtitles": {"enabled": True, "style": "sentence", "source": "artifacts/props.json#captions", "position": "bottom-center"},
    }
    if not edit.get("cuts"):
        shots = _read(art / "props.json", "run `props` first")["shots"]
        edit["cuts"] = [{"id": s["id"], "source": s["media"]["src"], "in_seconds": s["from"], "out_seconds": s["to"], "layer": "primary"} for s in shots]
    edit["bespoke"] = {
        "entry": str(paths["project"] / "index.tsx"), "composition_id": COMPOSITION_ID,
        "props_path": str(art / "props.json"), "public_dir": str(paths["public"]),
        "art_direction": str(paths["project"] / "art-direction.md"),
        "crf": 17, "concurrency": 6, "loudnorm_target": float(theme["audio"]["loudness_lufs"]),
    }
    if args.draft:
        edit["bespoke"]["scale"] = 0.5
    validate_artifact("edit_decisions", edit)  # fail here, before a multi-minute render
    # Checkpoints stay with the agent at each pipeline gate; the kit only writes the artifact.
    _write(ed_path, edit)
    out = paths["project"] / "renders" / (f"{args.slug}-draft.mp4" if args.draft else f"{args.slug}.mp4")
    brief_path = art / "brief.json"
    proposal = None
    if brief_path.exists():
        plan = json.loads(brief_path.read_text(encoding="utf-8")).get("metadata", {}).get("production_plan")
        proposal = {"production_plan": plan} if plan else None
    _stage(paths)
    res = VideoCompose().execute({"operation": "render", "output_path": str(out), "edit_decisions": edit, "proposal_packet": proposal})
    if not res.success:
        raise KitError(f"render failed: {res.error}")
    _write(art / "last_render.json", res.data)
    loud = (res.data or {}).get("loudness") or {}
    after = loud.get("after", {})
    print(f"rendered {out.relative_to(REPO_ROOT)}  loudness {after.get('input_i')} LUFS, peak {after.get('input_tp')} dBTP")


def cmd_review(args: argparse.Namespace) -> None:
    from lib.review_kit.review import review_video

    target = Path(args.slug)
    if not target.suffix:
        paths = _paths(args.slug)
        target = paths["project"] / "renders" / f"{args.slug}.mp4"
        sheet = paths["project"] / "snapshots" / "render-sheet.jpg"
    else:
        sheet = target.with_suffix(".sheet.jpg")
    report = review_video(target, sheet)
    print(json.dumps(report, indent=2))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m lib.review_kit", description="Review-reel mechanics.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("providers")
    p = sub.add_parser("new"); p.add_argument("slug"); p.add_argument("--title", required=True); p.add_argument("--source", required=True)
    p.add_argument("--theme"); p.add_argument("--fresh", action="store_true"); p.add_argument("--pipeline", default="hybrid")
    p = sub.add_parser("prep"); p.add_argument("slug"); p.add_argument("--force", action="store_true")
    p = sub.add_parser("voice"); p.add_argument("slug"); p.add_argument("--only")
    for name in ("captions", "sfx", "props", "validate"):
        sub.add_parser(name).add_argument("slug")
    p = sub.add_parser("music"); p.add_argument("slug"); p.add_argument("--query", required=True); p.add_argument("--name", required=True)
    p.add_argument("--min-duration", type=float, default=60)
    p = sub.add_parser("stills"); p.add_argument("slug"); p.add_argument("--cover", action="store_true")
    p = sub.add_parser("render"); p.add_argument("slug"); p.add_argument("--draft", action="store_true")
    p = sub.add_parser("review"); p.add_argument("slug", help="project slug, or a path to an .mp4")
    args = ap.parse_args(argv)
    handler = globals()[f"cmd_{args.cmd}"]
    try:
        handler(args)
    except KitError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
