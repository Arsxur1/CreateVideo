"""One-shot: narrate each script section with ElevenLabs and measure the real durations."""
import json
import subprocess
import sys
from pathlib import Path

from tools.tool_registry import registry

registry.discover()
tool = registry._tools["elevenlabs_tts"]

script = json.load(open("projects/diana-fast-slow-brain/artifacts/script.json", encoding="utf-8"))

# George - Warm, Captivating Storyteller. Premade, so the free plan allows it.
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"
# flash_v2_5 is the model that honours <break> tags; multilingual_v2 silently ignores them
# and the pauses are load-bearing in this script.
MODEL_ID = "eleven_flash_v2_5"

out_dir = Path("projects/diana-fast-slow-brain/assets/audio")
out_dir.mkdir(parents=True, exist_ok=True)


def probe_seconds(path: Path) -> float:
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(path)],
            capture_output=True, text=True, timeout=60,
        )
        return round(float(out.stdout.strip()), 3)
    except Exception:
        return 0.0


results = {}
for sec in script["sections"]:
    sid = sec["id"]
    dest = out_dir / f"{sid}.mp3"
    text = (sec.get("delivery_cues") or {}).get("provider_text") or sec["text"]

    ok, err = False, None
    for attempt in (1, 2):
        try:
            r = tool.execute({
                "text": text,
                "voice_id": VOICE_ID,
                "model_id": MODEL_ID,
                "stability": 0.75,
                "similarity_boost": 0.9,
                "style": 0.15,
                "speed": 0.9,
                "use_speaker_boost": True,
                "output_path": str(dest),
            })
            ok, err = bool(r.success), r.error
            if ok:
                break
        except Exception as exc:  # noqa: BLE001
            err = f"{type(exc).__name__}: {exc}"

    size = dest.stat().st_size if dest.exists() else 0
    secs = probe_seconds(dest) if size > 1000 else 0.0
    results[sid] = {"ok": ok and secs > 0, "path": str(dest), "bytes": size,
                    "seconds": secs, "error": err}
    print(f"[{'ok ' if results[sid]['ok'] else 'FAIL'}] {sid} {secs}s bytes={size} err={err}", flush=True)

total = round(sum(v["seconds"] for v in results.values()), 2)
bad = [k for k, v in results.items() if not v["ok"]]
print(f"\nDONE sections_ok={len(results) - len(bad)} failed={len(bad)} total_narration={total}s")
if bad:
    print("FAILED:", bad)
json.dump({"voice_id": VOICE_ID, "model_id": MODEL_ID, "total_seconds": total, "sections": results},
          open("projects/diana-fast-slow-brain/artifacts/narration_results.json", "w", encoding="utf-8"), indent=2)
sys.exit(0 if not bad else 1)
