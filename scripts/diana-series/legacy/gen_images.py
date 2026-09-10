"""One-shot: generate the remaining 21 storybook illustrations with a verbatim character lock."""
import json
import sys
import time
from pathlib import Path

from tools.tool_registry import registry

registry.discover()
tool = registry._tools["google_imagen"]

plan = json.load(open("projects/diana-fast-slow-brain/artifacts/scene_plan.json", encoding="utf-8"))
scenes = {s["id"]: s for s in plan["scenes"]}

CHAR = (
    "The girl is eight years old, Vietnamese-Australian, with straight black shoulder-length hair "
    "and a soft fringe, warm light skin, dark almond-shaped eyes and a round friendly face. "
    "She wears a mustard-yellow knitted jumper, a denim pinafore dress and red canvas shoes. "
    "Draw her exactly this way, identical in every picture."
)
STYLE = (
    "Children's picture-book illustration, soft gouache painting, warm cream paper background with "
    "visible paper grain, soft pencil linework, rounded organic shapes, muted warm palette, "
    "generous empty space, no hard vector outlines, no text, no lettering, no words, no captions."
)
GOLD = "A quick bright warm-gold brush-stroke streak represents fast thinking."
BLUE = "A slow steady deep-blue glow represents slow thinking."

WITH_GIRL = {"sc2", "sc3", "sc4", "sc6", "sc7", "sc8", "sc9", "sc10", "sc11",
             "sc12", "sc14", "sc15", "sc17", "sc19", "sc20", "sc21", "sc22"}
NEEDS_GOLD = {"sc2", "sc3", "sc5", "sc6", "sc7", "sc8", "sc9", "sc10", "sc12", "sc14", "sc20"}
NEEDS_BLUE = {"sc4", "sc5", "sc6", "sc15", "sc20", "sc21"}

TODO = [f"sc{i}" for i in range(2, 23)]

out_dir = Path("projects/diana-fast-slow-brain/assets/images")
out_dir.mkdir(parents=True, exist_ok=True)

results = {}
for sid in TODO:
    sc = scenes[sid]
    dest = out_dir / f"{sid}.png"
    if dest.exists() and dest.stat().st_size > 10000:
        print(f"[skip] {sid} already exists", flush=True)
        results[sid] = {"ok": True, "path": str(dest), "skipped": True}
        continue

    parts = [STYLE]
    if sid in WITH_GIRL:
        parts.append(CHAR)
    if sid in NEEDS_GOLD:
        parts.append(GOLD)
    if sid in NEEDS_BLUE:
        parts.append(BLUE)
    parts.append(sc["description"])
    prompt = " ".join(parts)

    ok = False
    err = None
    for attempt in (1, 2):
        try:
            r = tool.execute({
                "prompt": prompt,
                "aspect_ratio": "16:9",
                "model": "gemini-2.5-flash-image",
                "number_of_images": 1,
                "output_path": str(dest),
            })
            ok = bool(r.success)
            err = r.error
            if ok:
                break
        except Exception as exc:  # noqa: BLE001 - report, do not crash the batch
            err = f"{type(exc).__name__}: {exc}"
        if attempt == 1:
            time.sleep(3)

    size = dest.stat().st_size if dest.exists() else 0
    results[sid] = {"ok": ok and size > 10000, "path": str(dest), "bytes": size, "error": err}
    print(f"[{'ok ' if results[sid]['ok'] else 'FAIL'}] {sid} bytes={size} err={err}", flush=True)

good = [k for k, v in results.items() if v["ok"]]
bad = [k for k, v in results.items() if not v["ok"]]
print(f"\nDONE generated_ok={len(good)} failed={len(bad)}")
if bad:
    print("FAILED:", bad)
json.dump(results, open("projects/diana-fast-slow-brain/artifacts/image_results.json", "w", encoding="utf-8"), indent=2)
sys.exit(0 if not bad else 1)
