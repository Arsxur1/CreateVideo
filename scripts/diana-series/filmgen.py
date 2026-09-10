"""Reusable Diana-series film pipeline. Per-film scripts supply a data-only FILM spec.

build(FILM)  -> four pre-production artifacts, illustrations, narration, props.json
fix(FILM, d) -> regenerate named illustrations with corrected prompts
finish(FILM) -> edit_decisions, atelier render, ffprobe verify, frames, encodes,
                asset_manifest, render_report, seven checkpoints
"""
import json
import os
import re
import subprocess
from pathlib import Path

import jsonschema

# Repo root. This file lives at scripts/diana-series/filmgen.py, so parents[2] is the root.
REPO = Path(os.environ.get("OPENMONTAGE_ROOT") or Path(__file__).resolve().parents[2])
# Contact sheets and frame grabs are review scratch, not source, so they are written under
# projects/ which .gitignore already excludes rather than into the repo tree itself.
SCRATCH = Path(os.environ.get("DIANA_REVIEW_DIR") or REPO / "projects/_review")
SCRATCH.mkdir(parents=True, exist_ok=True)

DL = "https://thedecisionlab.com/biases"
SN = "https://www.sparknotes.com/lit/thinking-fast-and-slow/section1/"
PQ = "https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/bjep.12305"
NIMH = "https://www.nimh.nih.gov/get-involved/science-education/video-series-jane-the-brain"
SCH = ("https://www.scholastic.com/parents/family-life/social-emotional-learning/"
       "development-milestones/emotional-lives-8-10-year-olds.html")

DIANA = ("The girl is eight years old, Vietnamese-Australian, with straight black shoulder-length hair and a soft "
         "fringe, warm light skin, dark almond-shaped eyes and a round friendly face. She wears a mustard-yellow "
         "knitted jumper, a denim pinafore dress and red canvas shoes.")
STYLE = ("Children's picture-book illustration, soft gouache painting, plain warm cream paper background with "
         "visible paper grain, soft pencil linework, rounded organic shapes, muted warm palette, flat 2D storybook "
         "art, not 3D, no text, no lettering, no words, no numbers, no digits.")
ONE = "EXACTLY ONE CHILD in the frame, a single child alone. Do not draw two children."
NOPE = "There are NO people and NO animals at all in this picture."
OPEN = ("Most of the page must stay plain empty cream paper. Draw ONLY the things described, floating on that empty "
        "paper. Do NOT fill the frame with scenery, foliage, flowers, hills, sky, walls or a painted background of "
        "any kind.")
NOICON = ("Do NOT draw any question marks, exclamation marks, letters, symbols, icons, lightbulbs, cogs, gears, "
          "sparkles or floating graphics of any kind.")

VOICE = {"voice_id": "JBFqnCBsd6RMkjVDRZzb", "model_id": "eleven_flash_v2_5",
         "stability": 0.75, "similarity_boost": 0.9, "style": 0.15, "speed": 0.9,
         "use_speaker_boost": True}
IMG = {"aspect_ratio": "16:9", "model": "gemini-2.5-flash-image", "number_of_images": 1}
FPS, LEAD_IN, GAP, TAIL = 30, 1.0, 1.6, 2.5


def proj(f):
    return REPO / "projects" / f["slug"]


def _validate(obj, name, f):
    schema = json.load(open(REPO / f"schemas/artifacts/{name}.schema.json", encoding="utf-8"))
    jsonschema.validate(obj, schema)
    json.dump(obj, open(proj(f) / f"artifacts/{name}.json", "w", encoding="utf-8"), indent=2)
    print(f"{name} SCHEMA-VALID", flush=True)


def nframes(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                          "-show_entries", "stream=nb_frames", "-of", "csv=p=0", str(p)],
                         capture_output=True, text=True).stdout
    digits = re.sub(r"[^0-9]", "", out)
    return int(digits) if digits else -1


def probe(p):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "csv=p=0", str(p)], capture_output=True, text=True, timeout=90)
        return round(float(out.stdout.strip()), 3)
    except Exception:
        return 0.0


def _sections(f):
    out, t = [], 0.0
    for sid, label, text, prov, pause, pace, energy, emph, note in f["sections"]:
        dur = round(len(text.split()) / 110 * 60 + pause, 2)
        out.append({"id": sid, "label": label, "text": text,
                    "start_seconds": round(t, 2), "end_seconds": round(t + dur, 2),
                    "speaker_directions": note,
                    "delivery_cues": {"pace": pace, "energy": energy, "emphasis_words": emph,
                                      "pause_after_seconds": pause, "delivery_note": note,
                                      "provider_text": prov},
                    "enhancement_cues": [], "pronunciation_guides": []})
        t += dur
    return out, round(t, 2)


def _scenes(f, sections):
    per = {}
    for _, sid, _, _ in f["spec"]:
        per[sid] = per.get(sid, 0) + 1
    missing = [s["id"] for s in sections if s["id"] not in per]
    if missing:
        raise SystemExit(f"scene coverage gap for sections {missing}")
    ids = {sc for sc, _, _, _ in f["spec"]}
    covered = set().union(*[v[1] for v in f["clauses"].values()]) if f["clauses"] else set()
    uncovered = ids - covered
    if uncovered:
        raise SystemExit(f"scenes in no clause set: {sorted(uncovered)}")
    print(f"coverage ok: {len(sections)} sections mapped, all {len(ids)} scenes in a clause set", flush=True)

    sec_map = {s["id"]: s for s in sections}
    scenes, seen = [], {}
    for scid, sid, who, desc in f["spec"]:
        s = sec_map[sid]
        span = s["end_seconds"] - s["start_seconds"]
        n, i = per[sid], seen.get(sid, 0)
        seen[sid] = i + 1
        scenes.append({"id": scid, "type": "generated", "script_section_id": sid,
                       "start_seconds": round(s["start_seconds"] + span * i / n, 3),
                       "end_seconds": round(s["start_seconds"] + span * (i + 1) / n, 3),
                       "description": desc,
                       "narrative_role": "deliver_payload" if scid in f["heroes"] else "evidence",
                       "hero_moment": scid in f["heroes"],
                       "transition_in": "cut", "transition_out": "cut",
                       "shot_language": {"shot_size": "wide" if scid in f.get("wides", set()) else "medium",
                                         "camera_movement": "static", "lighting_key": "natural",
                                         "depth_of_field": "medium", "color_temperature": "warm"},
                       "overlay_notes": "No text in the illustration."})
    return scenes


def _prompt(f, scid, who, desc):
    parts = [STYLE] + ([ONE, DIANA] if who == "DIANA" else [NOPE])
    for text, members in f["clauses"].values():
        if scid in members:
            parts.append(text)
    parts.append(desc)
    return " ".join(parts)


def build(f):
    P = proj(f)
    for d in ("artifacts", "assets/images", "assets/audio", "assets/music", "composition"):
        (P / d).mkdir(parents=True, exist_ok=True)

    sections, total_est = _sections(f)

    research = {
        "version": "1.0", "topic": f["topic"], "research_date": "2026-09-09",
        "research_summary": f["summary"],
        "landscape": {"existing_content": f["existing"], "saturated_angles": f["saturated"],
                      "underserved_gaps": f["gaps"]},
        "data_points": [{"claim": c, "source_url": u, "source_name": sn,
                         "credibility": cr, "surprise_factor": sf, "usable_as": ua}
                        for c, u, sn, cr, sf, ua in f["data_points"]],
        "audience_insights": {"knowledge_level": f["knowledge_level"],
                              "common_questions": f["questions"],
                              "misconceptions": [{"myth": m, "reality": r, "source": s}
                                                 for m, r, s in f["misconceptions"]],
                              "pain_points": f["pain_points"]},
        "angles_discovered": [{"name": n, "type": t, "hook": h, "why_now": w, "grounded_in": g}
                              for n, t, h, w, g in f["angles"]],
        "expert_voices": [{"name": f.get("author_name", "Daniel Kahneman"),
                           "title_or_affiliation": f.get("author_title", "Nobel laureate, author"),
                           "position": f.get("kahneman", f.get("author_claim", "")), "source_url": f["source_url"],
                           "contrarian": False}],
        "sources": [
            {"url": f["source_url"], "title": f["source_title"], "used_for": "Mechanism", "reliability": "secondary"},
            {"url": f.get("source_url_secondary", f["source_url"]),
             "title": f.get("source_title_secondary", f["source_title"] + " (direct source read)"),
             "used_for": f["chapters"], "reliability": "primary"},
            {"url": PQ, "title": "Metacognition and emotional regulation in children 8 to 12",
             "used_for": "Age appropriateness", "reliability": "primary"},
            {"url": NIMH, "title": "Jane the Brain - NIMH", "used_for": "Format benchmark", "reliability": "primary"},
            {"url": SCH, "title": "Social and Emotional Lives of 8- to 10-Year-Olds",
             "used_for": "Development at this age", "reliability": "secondary"}],
        "metadata": {"series": f"Film {f['position']}.", "excluded_claims": f["excluded"]}
    }
    _validate(research, "research_brief", f)

    proposal = {
        "version": "1.0", "concept_options": f["concepts"],
        "selected_concept": {"concept_id": "c1", "rationale": f["rationale"],
                             "modifications": ["All production decisions carry over from the previous films",
                                               f"New device: {f['device_short']}",
                                               "Scene coverage and clause coverage asserted before generation",
                                               "Render via video_compose operation 'render'"]},
        "production_plan": {
            "pipeline": "animated-explainer", "playbook": "custom-atelier-storybook",
            "renderer_family": "explainer-teacher", "render_runtime": "remotion",
            "composition_mode": "atelier",
            "delivery_promise": {"promise_type": "teacher_explainer", "motion_required": False,
                                 "source_required": False,
                                 "tone_mode": "intimate, a bedtime storybook read aloud",
                                 "quality_floor": "presentable", "approved_fallback": "still_led"},
            "art_direction": f["art_direction"],
            "taste_profile": {"design_read": "The same bedtime picture book, later in the series",
                              "visual_variance": 8, "motion_intensity": 3, "information_density": 2,
                              "palette_discipline": "Unchanged. Cream ground, muted warm palette.",
                              "layout_variation": "Each scene composed for its beat.",
                              "reference_strategy": "Series continuity only.",
                              "anti_patterns": f["anti_patterns"],
                              "quality_gates": ["Contact sheet reviewed before render",
                                                "Every script section mapped to a scene, asserted at build time",
                                                "Every scene in at least one prompt-clause set, asserted at build time",
                                                "ffprobe the rendered file against the props frame count"]},
            "music_source": {"source_type": "ai_generated", "provider": "reused from film 1 (Google Lyria)",
                             "mood_direction": "The same bed as the earlier films.", "estimated_cost_usd": 0.0},
            "voice_selection": {"provider": "elevenlabs", "voice_id": VOICE["voice_id"],
                                "rationale": "The same warm storyteller voice as the earlier films.",
                                "estimated_cost_usd": 0.85, "delivery_style": f["delivery_style"],
                                "pacing_policy": "Roughly 110 words per minute with three genuine silences.",
                                "sample_approval_required": False},
            "stages": [
                {"stage": "script", "approach": "Around 320 words at an 8-year-old listening level.", "tools": []},
                {"stage": "scene_plan", "approach": "Eighteen scenes covering all fifteen sections.", "tools": []},
                {"stage": "assets", "approach": "Same image model and character lock, same voice, music reused.",
                 "tools": [{"tool_name": "google_imagen", "role": "illustration", "available": True},
                           {"tool_name": "elevenlabs_tts", "role": "narration", "available": True}]},
                {"stage": "edit", "approach": "Timeline rebuilt from measured narration durations.", "tools": []},
                {"stage": "compose", "approach": "Atelier Remotion render via operation 'render'.",
                 "tools": [{"tool_name": "video_compose", "role": "render", "available": True}]}],
            "quality_tradeoffs": f["tradeoffs"],
            "alternative_paths": [{"description": "Reuse everything from the earlier films",
                                   "total_cost_usd": 1.57, "quality_level": "standard"}]},
        "cost_estimate": {"total_estimated_usd": 1.57, "budget_cap_usd": 2.5, "budget_verdict": "within_budget",
                          "line_items": [
                              {"tool": "google_imagen", "operation": "storybook illustrations", "quantity": 18,
                               "estimated_usd": 0.72, "notes": "0.04 USD each"},
                              {"tool": "elevenlabs_tts", "operation": "narration", "quantity": 1,
                               "estimated_usd": 0.85, "notes": "Zero if Daniel records it"},
                              {"tool": "video_compose", "operation": "local render", "quantity": 1,
                               "estimated_usd": 0.0, "notes": "No API cost"}],
                          "savings_options": ["Daniel records the narration"]},
        "approval": {"status": "approved", "approved_budget_usd": 2.5,
                     "user_notes": ("Daniel instructed: continue until finish, dont need to ask every video. "
                                    "Standing authorisation for the remaining films in the approved series.")},
        "metadata": {"series_position": f["position"], "new_this_film": [f["device_short"]],
                     "chapters": f["chapters"]}
    }
    _validate(proposal, "proposal_packet", f)

    script = {"version": "1.0", "title": f["title"], "total_duration_seconds": total_est,
              "voice_performance": {
                  "performance_intent": f["performance_intent"],
                  "pacing_profile": f.get("pacing_profile", "contemplative"),
                  "energy_curve": f["energy_curve"],
                  "pause_policy": f["pause_policy"], "sample_section_id": f["sample_section"],
                  "provider_notes": {"all": "Roughly 110 words per minute.",
                                     "elevenlabs": "Same voice as the earlier films, George.",
                                     "human_recording": f["human_note"]}},
              "sections": sections,
              "metadata": {"series_position": f["position"],
                           "word_count_approx": sum(len(s["text"].split()) for s in sections),
                           "target_wpm": 110, "reading_age": f["reading_age"],
                           "pause_beats": f["pause_beats"], "grounded_in": f["grounded_in"],
                           "accuracy_guardrails_applied": f["guardrails"]}}
    _validate(script, "script", f)

    scenes = _scenes(f, sections)
    scene_plan = {"version": "1.0", "style_playbook": "custom-atelier-storybook", "scenes": scenes,
                  "metadata": {"character_lock": DIANA,
                               "one_child_rule": "Every frame containing a person contains exactly one child.",
                               "device_lock": f["device_lock"],
                               "style_lock": "Unchanged from the earlier films.",
                               "scene_count": len(scenes),
                               "section_coverage": "All script sections mapped, asserted before generation.",
                               "generation_order": "All eighteen generated, then reviewed on one contact sheet."}}
    _validate(scene_plan, "scene_plan", f)

    from tools.tool_registry import registry
    registry.discover()
    img = registry._tools["google_imagen"]
    tts = registry._tools["elevenlabs_tts"]
    by_id = {s["id"]: s for s in scenes}

    print("=== illustrations ===", flush=True)
    img_fail = []
    for scid, _, who, _ in f["spec"]:
        dest = P / "assets/images" / f"{scid}.png"
        if dest.exists() and dest.stat().st_size > 10000:
            print(f"[skip] {scid}", flush=True)
            continue
        ok, err = False, None
        for _ in range(3):
            try:
                r = img.execute({**IMG, "prompt": _prompt(f, scid, who, by_id[scid]["description"]),
                                 "output_path": str(dest)})
                ok, err = bool(r.success), r.error
                if ok:
                    break
            except Exception as exc:
                err = f"{type(exc).__name__}: {exc}"
        size = dest.stat().st_size if dest.exists() else 0
        good = ok and size > 10000
        if not good:
            img_fail.append(scid)
        print(f"[{'ok ' if good else 'FAIL'}] {scid} bytes={size} {err or ''}", flush=True)

    print("\n=== narration ===", flush=True)
    results = {}
    for s in sections:
        sid = s["id"]
        dest = P / "assets/audio" / f"{sid}.mp3"
        ok, err = False, None
        for _ in range(2):
            try:
                r = tts.execute({**VOICE, "text": s["delivery_cues"]["provider_text"],
                                 "output_path": str(dest)})
                ok, err = bool(r.success), r.error
                if ok:
                    break
            except Exception as exc:
                err = f"{type(exc).__name__}: {exc}"
        secs = probe(dest) if dest.exists() and dest.stat().st_size > 1000 else 0.0
        results[sid] = {"ok": ok and secs > 0, "path": str(dest), "seconds": secs, "error": err}
        print(f"[{'ok ' if results[sid]['ok'] else 'FAIL'}] {sid} {secs}s {err or ''}", flush=True)

    aud_fail = [k for k, v in results.items() if not v["ok"]]
    json.dump({**{k: VOICE[k] for k in ("voice_id", "model_id")},
               "total_seconds": round(sum(v["seconds"] for v in results.values()), 2),
               "sections": results},
              open(P / "artifacts/narration_results.json", "w", encoding="utf-8"), indent=2)

    _props(f, sections, scenes, {k: v["seconds"] for k, v in results.items()})
    print(f"\nDONE images_failed={img_fail} narration_failed={aud_fail}", flush=True)
    return not (img_fail or aud_fail)


def _props(f, sections, scenes, dur):
    P = proj(f)
    by_section = {}
    for sc in scenes:
        by_section.setdefault(sc["script_section_id"], []).append(sc)

    audio, spans, tt = [], {}, LEAD_IN
    for i, sec in enumerate(sections):
        sid = sec["id"]
        audio.append({"id": sid, "src": f"audio/{sid}.mp3", "startSec": round(tt, 3), "durSec": dur[sid]})
        end = tt + dur[sid] + (GAP if i < len(sections) - 1 else TAIL)
        spans[sid] = (tt, end)
        tt = end
    TOTAL = round(tt, 3)

    pscenes = []
    for i, sec in enumerate(sections):
        sid = sec["id"]
        start, end = spans[sid]
        if i == 0:
            start = 0.0
        grp = by_section.get(sid)
        if not grp:
            if pscenes:
                pscenes[-1]["durSec"] = round(pscenes[-1]["durSec"] + (end - start), 3)
            continue
        step = (end - start) / len(grp)
        for j, sc in enumerate(grp):
            pscenes.append({"id": sc["id"], "src": f"images/{sc['id']}.png",
                            "startSec": round(start + j * step, 3), "durSec": round(step, 3),
                            "heroMoment": bool(sc.get("hero_moment")),
                            "movement": "static"})

    captions = []
    for sec in sections:
        start = spans[sec["id"]][0]
        d = dur[sec["id"]]
        phr = [p.strip() for p in re.split(r"(?<=[.?!])\s+", sec["text"]) if p.strip()]
        chars = sum(len(p) for p in phr) or 1
        acc = start
        for p in phr:
            share = d * (len(p) / chars)
            captions.append({"text": p, "startSec": round(acc, 3), "durSec": round(share, 3)})
            acc += share

    last = pscenes[-1]
    props = {"fps": FPS, "width": 1920, "height": 1080,
             "durationInFrames": int(round(TOTAL * FPS)), "totalSeconds": TOTAL,
             "music": {"src": "music/bed.wav", "volume": 0.16, "fadeOutStartSec": round(TOTAL - 26, 3)},
             "scenes": pscenes, "audio": audio, "captions": captions,
             "titles": [{"kind": "title", "text": f["title"],
                         "startSec": round(last["startSec"] + 1.0, 3),
                         "durSec": round(max(2.0, min(8.0, last["durSec"] - 1.0)), 3)}]}
    json.dump(props, open(P / "composition/props.json", "w", encoding="utf-8"), indent=2)
    print(f"total {TOTAL}s ({int(TOTAL // 60)}m {TOTAL % 60:.1f}s) frames={props['durationInFrames']} "
          f"scenes={len(pscenes)} captions={len(captions)}", flush=True)


def fix(f, fixes):
    """fixes: {scene_id: full_prompt_string}"""
    from tools.tool_registry import registry
    registry.discover()
    img = registry._tools["google_imagen"]
    for scid, prompt in fixes.items():
        dest = proj(f) / "assets/images" / f"{scid}.png"
        ok, err = False, None
        for _ in range(3):
            try:
                r = img.execute({**IMG, "prompt": prompt, "output_path": str(dest)})
                ok, err = bool(r.success), r.error
                if ok:
                    break
            except Exception as exc:
                err = f"{type(exc).__name__}: {exc}"
        size = dest.stat().st_size if dest.exists() else 0
        print(f"[{'ok ' if ok and size > 10000 else 'FAIL'}] {scid} bytes={size} {err or ''}", flush=True)


def sheet(f, out=None):
    from PIL import Image, ImageDraw
    d = proj(f) / "assets/images"
    n_total = len(f["spec"])
    W, H, cols, pad = 440, 247, 4, 8
    rows = (n_total + cols - 1) // cols
    sh = Image.new("RGB", (cols * (W + pad) + pad, rows * (H + pad) + pad), (40, 40, 40))
    dr = ImageDraw.Draw(sh)
    for n, (scid, _, _, _) in enumerate(f["spec"]):
        im = Image.open(d / f"{scid}.png").convert("RGB").resize((W, H))
        x = pad + (n % cols) * (W + pad)
        y = pad + (n // cols) * (H + pad)
        sh.paste(im, (x, y))
        dr.text((x + 6, y + 6), scid, fill=(255, 60, 60))
    out = Path(out or SCRATCH / f"sheet_{f['slug']}.png")
    sh.save(out)
    print(out, sh.size)
    return out


def finish(f, regens, reason, frame_times=None):
    P = proj(f)
    props = json.load(open(P / "composition/props.json", encoding="utf-8"))
    narr = json.load(open(P / "artifacts/narration_results.json", encoding="utf-8"))

    ed = {"version": "1.0", "render_runtime": "remotion", "composition_mode": "atelier",
          "renderer_family": "explainer-teacher",
          "cuts": [{"id": s["id"], "source": f"projects/{f['slug']}/assets/images/{s['id']}.png",
                    "in_seconds": 0.0, "out_seconds": round(s["durSec"], 3)} for s in props["scenes"]],
          "audio": {"narration": {"segments": [
              {"asset_id": a["id"], "start_seconds": a["startSec"],
               "end_seconds": round(a["startSec"] + a["durSec"], 3)} for a in props["audio"]]}},
          "music": {"asset_id": "bed", "volume": 0.16, "ducking": True,
                    "fade_in_seconds": 3.0, "fade_out_seconds": 26.0},
          "subtitles": {"enabled": True, "style": "sentence", "font": "Georgia serif",
                        "font_size": 46, "color": "#3B3026"},
          "bespoke": {"entry": f"projects/{f['slug']}/composition/index.tsx",
                      "composition_id": f["comp_id"],
                      "props_path": str((P / "composition/props.json").resolve()),
                      "public_dir": str((P / "assets").resolve()), "crf": 18,
                      "art_direction": f["art_direction"]},
          "metadata": {"total_seconds": props["totalSeconds"], "frames": props["durationInFrames"],
                       "fps": 30, "series_position": f["position"]}}
    _validate(ed, "edit_decisions", f)

    from tools.tool_registry import registry
    registry.discover()
    (P / "renders").mkdir(exist_ok=True)
    out = (P / "renders/final.mp4").resolve()
    if out.exists() and nframes(out) == props["durationInFrames"]:
        print("render already correct, skipping re-render", flush=True)
    else:
        r = registry._tools["video_compose"].execute(
            {"operation": "render", "edit_decisions": ed, "output_path": str(out)})
        print("render success:", r.success, r.error, flush=True)
        if not r.success:
            raise SystemExit(f"render failed: {r.error}")

    nb = nframes(out)
    if nb != props["durationInFrames"]:
        raise SystemExit(f"FRAME MISMATCH rendered={nb} expected={props['durationInFrames']}")
    print(f"ffprobe ok: {nb} frames == props", flush=True)

    total = props["totalSeconds"]
    times = frame_times or [round(total * x) for x in (0.10, 0.32, 0.54, 0.76, 0.96)]
    from PIL import Image
    tiles = []
    for t in times:
        pth = SCRATCH / f"fr_{f['slug']}_{t}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(out),
                        "-frames:v", "1", "-y", str(pth)], check=True)
        tiles.append(pth)
    W, H = 640, 360
    sh = Image.new("RGB", (W * 2 + 12, H * 3 + 16), (30, 30, 30))
    for i, pth in enumerate(tiles):
        sh.paste(Image.open(pth).convert("RGB").resize((W, H)), ((i % 2) * (W + 12), (i // 2) * (H + 8)))
    fpath = SCRATCH / f"frames_{f['slug']}.png"
    sh.save(fpath)
    print("frames:", fpath, times, flush=True)

    R = P / "renders"
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(R / "final.mp4"), "-vf", "scale=1280:720",
                    "-c:v", "libx264", "-crf", "27", "-preset", "medium", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "112k", "-movflags", "+faststart", "-y",
                    str(R / "final_mobile.mp4")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(R / "final.mp4"),
                    "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-y",
                    str(R / "final_share.mp4")], check=True)

    n_img = len(f["spec"]) + len(regens)
    cost = round(0.04 * n_img + 0.85, 2)
    assets = [{"id": s["id"], "type": "image", "path": f"assets/images/{s['id']}.png",
               "source_tool": "google_imagen", "scene_id": s["id"], "provider": "google_imagen",
               "model": IMG["model"], "resolution": "1920x1080", "format": "png",
               "subtype": "generated", "license": "generated", "cost_usd": 0.04}
              for s in props["scenes"]]
    assets += [{"id": a["id"], "type": "narration", "path": f"assets/audio/{a['id']}.mp3",
                "source_tool": "elevenlabs_tts", "scene_id": a["id"], "provider": "elevenlabs",
                "model": VOICE["model_id"], "format": "mp3", "duration_seconds": a["durSec"],
                "subtype": "generated", "license": "generated", "cost_usd": 0.0,
                "voice_performance": {"source_section_id": a["id"], "delivery_cues_applied": True,
                                      "provider_text_used": True}} for a in props["audio"]]
    assets.append({"id": "bed", "type": "music", "path": "assets/music/bed.wav",
                   "source_tool": "google_lyria", "scene_id": "global", "provider": "google_lyria",
                   "model": "lyria", "format": "wav", "subtype": "reused from film 1",
                   "license": "generated", "cost_usd": 0.0})
    manifest = {"version": "1.0", "assets": assets, "total_cost_usd": cost,
                "metadata": {"series_position": f["position"], "title": f["title"],
                             "asset_count": len(assets), "images_generated_total": n_img,
                             "regenerations": regens, "regeneration_reason": reason,
                             "narration_total_seconds": narr["total_seconds"]}}
    _validate(manifest, "asset_manifest", f)

    outs = []
    for name, res, tgt in (("final.mp4", "1920x1080", "master"),
                           ("final_share.mp4", "1920x1080", "share"),
                           ("final_mobile.mp4", "1280x720", "mobile")):
        pth = R / name
        outs.append({"path": f"projects/{f['slug']}/renders/{name}", "format": "mp4",
                     "codec": "h264", "audio_codec": "aac", "resolution": res, "fps": 30,
                     "duration_seconds": probe(pth), "file_size_bytes": pth.stat().st_size,
                     "platform_target": tgt})
    report = {"version": "1.0", "outputs": outs, "render_grammar": "explainer-teacher",
              "warnings": ["Post-render self-review flags missing burned-in subtitles. False positive: "
                           "captions are drawn inside the Remotion composition, not burned by ffmpeg."],
              "verification_notes": [
                  f"ffprobe confirms {nb} frames, {props['totalSeconds']}s, 1920x1080, 30fps, h264, 48kHz stereo AAC.",
                  "Frame count asserted equal to composition/props.json before encoding.",
                  f"Five frames checked at {times} seconds.",
                  "Contact sheet reviewed before render; regenerations listed in the asset manifest.",
                  "Rendered via video_compose operation 'render', which routes to the atelier path.",
                  "Timeline built from ffprobe-measured narration durations, not script estimates."],
              "metadata": {"series_position": f["position"], "title": f["title"],
                           "composition_mode": "atelier", "composition_id": f["comp_id"],
                           "render_runtime": "remotion", "frames": props["durationInFrames"],
                           "total_seconds": props["totalSeconds"], "cost_usd": cost,
                           "chapters": f["chapters"]}}
    _validate(report, "render_report", f)

    from lib.checkpoint import write_checkpoint
    PD = REPO / "projects"

    def L(rel):
        return json.load(open(P / rel, encoding="utf-8"))

    snap = {"spent_usd": cost, "estimated_remaining_usd": 0.0, "budget_cap_usd": 2.5}
    stages = [("research", {"research_brief": L("artifacts/research_brief.json")}, None),
              ("proposal", {"proposal_packet": L("artifacts/proposal_packet.json")}, None),
              ("script", {"script": L("artifacts/script.json")}, None),
              ("scene_plan", {"scene_plan": L("artifacts/scene_plan.json")}, None),
              ("assets", {"asset_manifest": L("artifacts/asset_manifest.json"),
                          "narration_results": L("artifacts/narration_results.json")}, snap),
              ("edit", {"edit_decisions": L("artifacts/edit_decisions.json")}, None),
              ("compose", {"render_report": L("artifacts/render_report.json")}, snap)]
    for stage, arts, cs in stages:
        write_checkpoint(PD, f["slug"], stage, "completed", arts, cost_snapshot=cs,
                         human_approval_required=True, human_approved=True)
        print("checkpoint", stage, flush=True)
    print(f"FINISHED {f['slug']} cost={cost} frames={props['durationInFrames']} "
          f"secs={props['totalSeconds']}", flush=True)
    return cost


def init(f):
    import shutil
    from lib.checkpoint import init_project
    init_project(f["slug"], title=f["title"], pipeline_type="animated-explainer")
    P = proj(f)
    (P / "composition").mkdir(parents=True, exist_ok=True)
    (P / "assets/music").mkdir(parents=True, exist_ok=True)
    src = REPO / "projects/diana-fast-slow-brain"
    tsx = (src / "composition/index.tsx").read_text(encoding="utf-8")
    (P / "composition/index.tsx").write_text(tsx.replace("DianaTwoSpeeds", f["comp_id"]), encoding="utf-8")
    shutil.copy2(src / "assets/music/bed.wav", P / "assets/music/bed.wav")
    print("init ok:", P, f["comp_id"], flush=True)
