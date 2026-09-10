"""One-shot: build the Remotion props from measured narration durations."""
import json
import re
from pathlib import Path

FPS = 30
LEAD_IN = 1.0      # seconds of quiet before the first line
GAP = 1.6          # seconds of breathing room between sections
TAIL = 2.5         # seconds of quiet after the last line

proj = Path("projects/diana-fast-slow-brain")
script = json.load(open(proj / "artifacts/script.json", encoding="utf-8"))
plan = json.load(open(proj / "artifacts/scene_plan.json", encoding="utf-8"))
narr = json.load(open(proj / "artifacts/narration_results.json", encoding="utf-8"))

sections = script["sections"]
dur = {sid: v["seconds"] for sid, v in narr["sections"].items()}

by_section = {}
for sc in plan["scenes"]:
    by_section.setdefault(sc["script_section_id"], []).append(sc)

# 1. Lay the audio out on a real timeline.
audio, spans = [], {}
t = LEAD_IN
for i, sec in enumerate(sections):
    sid = sec["id"]
    d = dur[sid]
    audio.append({"id": sid, "src": f"audio/{sid}.mp3", "startSec": round(t, 3), "durSec": d})
    span_end = t + d + (GAP if i < len(sections) - 1 else TAIL)
    spans[sid] = (t, span_end)
    t = span_end
TOTAL = round(t, 3)

# 2. Visuals run continuously: a section's scenes split its whole span, including the gap.
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
            "id": sc["id"],
            "src": f"images/{sc['id']}.png",
            "startSec": round(s, 3),
            "durSec": round(e - s, 3),
            "heroMoment": bool(sc.get("hero_moment")),
            "movement": sc.get("shot_language", {}).get("camera_movement", "static"),
        })

# 3. Phrase-level captions, timed proportionally to characters within each section.
captions = []
for sec in sections:
    sid = sec["id"]
    start, _ = spans[sid]
    d = dur[sid]
    phrases = [p.strip() for p in re.split(r"(?<=[.?!])\s+", sec["text"]) if p.strip()]
    total_chars = sum(len(p) for p in phrases) or 1
    acc = start
    for p in phrases:
        share = d * (len(p) / total_chars)
        captions.append({"text": p, "startSec": round(acc, 3), "durSec": round(share, 3)})
        acc += share

# 4. The three deliberate on-screen text moments named in the scene plan.
def scene_by_id(sid):
    return next(s for s in scenes if s["id"] == sid)

sc3, sc18, sc22 = scene_by_id("sc3"), scene_by_id("sc18"), scene_by_id("sc22")
titles = [
    {"kind": "sum", "text": "17 x 24",
     "startSec": sc3["startSec"] + 1.0, "durSec": max(2.0, sc3["durSec"] - 1.5)},
    {"kind": "scales", "text": "won  |  lost",
     "startSec": sc18["startSec"] + 1.5, "durSec": max(2.0, sc18["durSec"] - 2.0)},
    {"kind": "title", "text": "Diana and the Two Speeds",
     "startSec": sc22["startSec"] + 1.0, "durSec": max(2.0, sc22["durSec"] - 1.0)},
]

props = {
    "fps": FPS,
    "width": 1920,
    "height": 1080,
    "durationInFrames": int(round(TOTAL * FPS)),
    "totalSeconds": TOTAL,
    "music": {"src": "music/bed.wav", "volume": 0.16, "fadeOutStartSec": round(TOTAL - 26, 3)},
    "scenes": scenes,
    "audio": audio,
    "captions": captions,
    "titles": titles,
}

out = proj / "composition"
out.mkdir(parents=True, exist_ok=True)
json.dump(props, open(out / "props.json", "w", encoding="utf-8"), indent=2)

print(f"total: {TOTAL}s  ({int(TOTAL // 60)}m {TOTAL % 60:.1f}s)  frames={props['durationInFrames']}")
print(f"scenes={len(scenes)} audio={len(audio)} captions={len(captions)} titles={len(titles)}")
gaps = [round(scenes[i + 1]["startSec"] - (scenes[i]["startSec"] + scenes[i]["durSec"]), 3)
        for i in range(len(scenes) - 1)]
print("max visual gap between scenes:", max(abs(g) for g in gaps), "(0 means continuous)")
print("last scene ends:", round(scenes[-1]["startSec"] + scenes[-1]["durSec"], 3), "vs total", TOTAL)
