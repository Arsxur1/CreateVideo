"""One-shot: build the Remotion props for film 2 from measured narration durations."""
import json
import re
from pathlib import Path

FPS = 30
LEAD_IN = 1.0
GAP = 1.6
TAIL = 2.5

proj = Path("projects/diana-story-machine")
script = json.load(open(proj / "artifacts/script.json", encoding="utf-8"))
plan = json.load(open(proj / "artifacts/scene_plan.json", encoding="utf-8"))
narr = json.load(open(proj / "artifacts/narration_results.json", encoding="utf-8"))

sections = script["sections"]
dur = {sid: v["seconds"] for sid, v in narr["sections"].items()}

by_section = {}
for sc in plan["scenes"]:
    by_section.setdefault(sc["script_section_id"], []).append(sc)

audio, spans = [], {}
t = LEAD_IN
for i, sec in enumerate(sections):
    sid = sec["id"]
    d = dur[sid]
    audio.append({"id": sid, "src": f"audio/{sid}.mp3", "startSec": round(t, 3), "durSec": d})
    end = t + d + (GAP if i < len(sections) - 1 else TAIL)
    spans[sid] = (t, end)
    t = end
TOTAL = round(t, 3)

scenes = []
for i, sec in enumerate(sections):
    sid = sec["id"]
    start, end = spans[sid]
    if i == 0:
        start = 0.0
    group = by_section[sid]
    step = (end - start) / len(group)
    for j, sc in enumerate(group):
        s = start + j * step
        e = start + (j + 1) * step
        scenes.append({
            "id": sc["id"], "src": f"images/{sc['id']}.png",
            "startSec": round(s, 3), "durSec": round(e - s, 3),
            "heroMoment": bool(sc.get("hero_moment")),
            "movement": sc.get("shot_language", {}).get("camera_movement", "static"),
        })

captions = []
for sec in sections:
    sid = sec["id"]
    start, _ = spans[sid]
    d = dur[sid]
    phrases = [p.strip() for p in re.split(r"(?<=[.?!])\s+", sec["text"]) if p.strip()]
    chars = sum(len(p) for p in phrases) or 1
    acc = start
    for p in phrases:
        share = d * (len(p) / chars)
        captions.append({"text": p, "startSec": round(acc, 3), "durSec": round(share, 3)})
        acc += share

last = scenes[-1]
titles = [{"kind": "title", "text": "The Story Machine",
           "startSec": round(last["startSec"] + 1.0, 3),
           "durSec": round(max(2.0, last["durSec"] - 1.0), 3)}]

props = {
    "fps": FPS, "width": 1920, "height": 1080,
    "durationInFrames": int(round(TOTAL * FPS)), "totalSeconds": TOTAL,
    "music": {"src": "music/bed.wav", "volume": 0.16, "fadeOutStartSec": round(TOTAL - 26, 3)},
    "scenes": scenes, "audio": audio, "captions": captions, "titles": titles,
}

out = proj / "composition"
out.mkdir(parents=True, exist_ok=True)
json.dump(props, open(out / "props.json", "w", encoding="utf-8"), indent=2)

print(f"total {TOTAL}s ({int(TOTAL//60)}m {TOTAL%60:.1f}s) frames={props['durationInFrames']}")
print(f"scenes={len(scenes)} audio={len(audio)} captions={len(captions)} titles={len(titles)}")
print("last scene ends:", round(scenes[-1]["startSec"] + scenes[-1]["durSec"], 3), "vs total", TOTAL)
