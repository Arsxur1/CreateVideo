"""One-shot: generate all illustrations and narration for film 2, The Story Machine."""
import json
import subprocess
import sys
from pathlib import Path

from tools.tool_registry import registry

registry.discover()
img = registry._tools["google_imagen"]
tts = registry._tools["elevenlabs_tts"]

PROJ = Path("projects/diana-story-machine")
plan = json.load(open(PROJ / "artifacts/scene_plan.json", encoding="utf-8"))
script = json.load(open(PROJ / "artifacts/script.json", encoding="utf-8"))
scenes = {s["id"]: s for s in plan["scenes"]}

DIANA = (
    "The girl is eight years old, Vietnamese-Australian, with straight black shoulder-length hair "
    "and a soft fringe, warm light skin, dark almond-shaped eyes and a round friendly face. "
    "She wears a mustard-yellow knitted jumper, a denim pinafore dress and red canvas shoes."
)
FRIEND = (
    "The friend is a clearly different child: curly shoulder-length brown hair, a sage-green cardigan, "
    "a cream skirt and round glasses. She looks nothing like the girl in the mustard jumper."
)
STYLE = (
    "Children's picture-book illustration, soft gouache painting, warm cream paper background with "
    "visible paper grain, soft pencil linework, rounded organic shapes, muted warm palette, flat 2D "
    "storybook art, not 3D, no text, no lettering, no words, no numbers, no digits, no captions."
)
ONE = "EXACTLY ONE CHILD in the frame, a single child alone. Do not draw two children."
NONE = "There are NO people at all in this picture."

WITH_DIANA = {"sc1", "sc4", "sc5", "sc8", "sc9", "sc10", "sc13", "sc16"}
WITH_FRIEND = {"sc2", "sc11", "sc12"}
NO_PEOPLE = {"sc3", "sc6", "sc7", "sc14", "sc15", "sc17"}
BOTH = {"sc18"}

img_dir = PROJ / "assets/images"
img_dir.mkdir(parents=True, exist_ok=True)
aud_dir = PROJ / "assets/audio"
aud_dir.mkdir(parents=True, exist_ok=True)

print("=== illustrations ===", flush=True)
img_fail = []
for sid in [f"sc{i}" for i in range(1, 19)]:
    dest = img_dir / f"{sid}.png"
    if dest.exists() and dest.stat().st_size > 10000:
        print(f"[skip] {sid}", flush=True)
        continue
    parts = [STYLE]
    if sid in WITH_DIANA:
        parts += [ONE, DIANA]
    elif sid in WITH_FRIEND:
        parts += [ONE, FRIEND]
    elif sid in BOTH:
        parts += ["Exactly two children, clearly different from each other.", DIANA, FRIEND]
    else:
        parts += [NONE]
    parts.append(scenes[sid]["description"])
    prompt = " ".join(parts)

    ok, err = False, None
    for _ in (1, 2):
        try:
            r = img.execute({"prompt": prompt, "aspect_ratio": "16:9",
                             "model": "gemini-2.5-flash-image", "number_of_images": 1,
                             "output_path": str(dest)})
            ok, err = bool(r.success), r.error
            if ok:
                break
        except Exception as exc:  # noqa: BLE001
            err = f"{type(exc).__name__}: {exc}"
    size = dest.stat().st_size if dest.exists() else 0
    good = ok and size > 10000
    if not good:
        img_fail.append(sid)
    print(f"[{'ok ' if good else 'FAIL'}] {sid} bytes={size} {err or ''}", flush=True)

print("\n=== narration ===", flush=True)


def probe(p: Path) -> float:
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "csv=p=0", str(p)], capture_output=True, text=True, timeout=60)
        return round(float(out.stdout.strip()), 3)
    except Exception:
        return 0.0


results = {}
for s in script["sections"]:
    sid = s["id"]
    dest = aud_dir / f"{sid}.mp3"
    text = (s.get("delivery_cues") or {}).get("provider_text") or s["text"]
    ok, err = False, None
    for _ in (1, 2):
        try:
            r = tts.execute({"text": text, "voice_id": "JBFqnCBsd6RMkjVDRZzb",
                             "model_id": "eleven_flash_v2_5", "stability": 0.75,
                             "similarity_boost": 0.9, "style": 0.15, "speed": 0.9,
                             "use_speaker_boost": True, "output_path": str(dest)})
            ok, err = bool(r.success), r.error
            if ok:
                break
        except Exception as exc:  # noqa: BLE001
            err = f"{type(exc).__name__}: {exc}"
    secs = probe(dest) if dest.exists() and dest.stat().st_size > 1000 else 0.0
    results[sid] = {"ok": ok and secs > 0, "path": str(dest), "seconds": secs, "error": err}
    print(f"[{'ok ' if results[sid]['ok'] else 'FAIL'}] {sid} {secs}s {err or ''}", flush=True)

total = round(sum(v["seconds"] for v in results.values()), 2)
aud_fail = [k for k, v in results.items() if not v["ok"]]
json.dump({"voice_id": "JBFqnCBsd6RMkjVDRZzb", "model_id": "eleven_flash_v2_5",
           "total_seconds": total, "sections": results},
          open(PROJ / "artifacts/narration_results.json", "w", encoding="utf-8"), indent=2)

print(f"\nDONE images_failed={img_fail} narration_failed={aud_fail} total_narration={total}s")
sys.exit(0 if not img_fail and not aud_fail else 1)
