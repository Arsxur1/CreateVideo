import json
from pathlib import Path
from tools.video.remotion_caption_burn import RemotionCaptionBurn


def test_page_break_flag_is_forwarded():
    tool = RemotionCaptionBurn()
    segs = [{"start": 0, "end": 1, "words": [{"word": "Tu", "start": 0.0, "end": 0.1},
                                             {"word": "entends", "start": 0.1, "end": 0.3, "page_break_after": True},
                                             {"word": "parler", "start": 0.3, "end": 0.5}]}]
    caps = tool._segments_to_word_captions(segs)
    assert caps[1]["pageBreakAfter"] is True and "pageBreakAfter" not in caps[0] and "pageBreakAfter" not in caps[2]


def test_composition_props_reach_the_props_file(tmp_path: Path, monkeypatch):
    tool = RemotionCaptionBurn()
    root = tmp_path / "remotion-composer"; (root / "node_modules").mkdir(parents=True); (root / "package.json").write_text("{}")
    monkeypatch.setattr(tool, "_find_remotion_root", lambda: root)
    class R: stdout = "2.0\n"
    class D: stdout = "1080x1920\n"
    calls = []
    def fake_run(cmd, cwd=None, **kw):
        calls.append(cmd)
        if cmd[0] == "ffprobe" and "format=duration" in cmd: return R()
        if cmd[0] == "ffprobe": return D()
        Path(cmd[-1].split("=", 1)[1]).write_bytes(b"x")  # --output=<path>
        return R()
    monkeypatch.setattr(tool, "run_command", fake_run)
    src = tmp_path / "take.mp4"; src.write_bytes(b"v")
    out = tmp_path / "out.mp4"
    img = tmp_path / "x.png"; img.write_bytes(b"i")
    r = tool._render_remotion(str(src), str(out), [{"word": "a", "startMs": 0, "endMs": 100}], 8, 68, "#FFD166",
                              overlays=[{"type": "image", "src": str(img), "in_seconds": 1, "out_seconds": 2}],
                              composition_props={"captionPaddingBottom": 480, "captionFontFamily": "Inter"})
    assert r.success, r.error
    props = json.loads((root / "public" / "demo-props" / "caption-burn-take.json").read_text(encoding="utf-8"))
    assert props["captionPaddingBottom"] == 480 and props["captionFontFamily"] == "Inter"
    assert props["overlays"][0]["type"] == "image" and props["highlightColor"] == "#FFD166"
    assert props["videoSrc"] == "talking-head/take.mp4"


def test_missing_overlay_src_fails_fast_before_rendering(tmp_path: Path, monkeypatch):
    tool = RemotionCaptionBurn()
    root = tmp_path / "remotion-composer"; (root / "node_modules").mkdir(parents=True); (root / "package.json").write_text("{}")
    monkeypatch.setattr(tool, "_find_remotion_root", lambda: root)
    calls = []
    def fake_run(cmd, cwd=None, **kw):
        calls.append(cmd)
        raise AssertionError("render must not run when an overlay src cannot be resolved")
    monkeypatch.setattr(tool, "run_command", fake_run)
    src = tmp_path / "take.mp4"; src.write_bytes(b"v")
    r = tool._render_remotion(str(src), str(tmp_path / "out.mp4"), [{"word": "a", "startMs": 0, "endMs": 100}], 8, 68, "#FFD166",
                              overlays=[{"type": "image", "src": "missing-popin.png", "in_seconds": 1, "out_seconds": 2}])
    assert r.success is False
    assert "overlay src not found" in r.error
    assert calls == []


def test_composition_props_cannot_override_derived_keys(tmp_path: Path, monkeypatch):
    tool = RemotionCaptionBurn()
    root = tmp_path / "remotion-composer"; (root / "node_modules").mkdir(parents=True); (root / "package.json").write_text("{}")
    monkeypatch.setattr(tool, "_find_remotion_root", lambda: root)
    class R: stdout = "2.0\n"
    class D: stdout = "1080x1920\n"
    def fake_run(cmd, cwd=None, **kw):
        if cmd[0] == "ffprobe" and "format=duration" in cmd: return R()
        if cmd[0] == "ffprobe": return D()
        Path(cmd[-1].split("=", 1)[1]).write_bytes(b"x"); return R()
    monkeypatch.setattr(tool, "run_command", fake_run)
    src = tmp_path / "take.mp4"; src.write_bytes(b"v")
    real_captions = [{"word": "a", "startMs": 0, "endMs": 100}]
    r = tool._render_remotion(
        str(src), str(tmp_path / "out.mp4"), real_captions, 8, 68, "#FFD166",
        overlays=None,
        composition_props={"captions": [], "videoSrc": "evil", "overlays": [{"type": "sneaky"}], "captionFontFamily": "Inter"},
    )
    assert r.success, r.error
    props = json.loads((root / "public" / "demo-props" / "caption-burn-take.json").read_text(encoding="utf-8"))
    assert props["captions"] == real_captions
    assert props["videoSrc"] == "talking-head/take.mp4"
    assert props["overlays"] == []
    assert props["captionFontFamily"] == "Inter"


def test_overlay_image_files_are_copied_beside_the_video(tmp_path: Path, monkeypatch):
    tool = RemotionCaptionBurn()
    root = tmp_path / "remotion-composer"; (root / "node_modules").mkdir(parents=True); (root / "package.json").write_text("{}")
    monkeypatch.setattr(tool, "_find_remotion_root", lambda: root)
    class R: stdout = "2.0\n"
    class D: stdout = "1080x1920\n"
    def fake_run(cmd, cwd=None, **kw):
        if cmd[0] == "ffprobe" and "format=duration" in cmd: return R()
        if cmd[0] == "ffprobe": return D()
        Path(cmd[-1].split("=", 1)[1]).write_bytes(b"x"); return R()
    monkeypatch.setattr(tool, "run_command", fake_run)
    src = tmp_path / "take.mp4"; src.write_bytes(b"v")
    img = tmp_path / "popin-1.png"; img.write_bytes(b"p")
    r = tool._render_remotion(str(src), str(tmp_path / "out.mp4"), [{"word": "a", "startMs": 0, "endMs": 100}], 8, 68, "#FFD166",
                              overlays=[{"type": "image", "src": str(img), "in_seconds": 1, "out_seconds": 2}])
    assert r.success, r.error
    props = json.loads((root / "public" / "demo-props" / "caption-burn-take.json").read_text(encoding="utf-8"))
    assert props["overlays"][0]["src"] == "talking-head/popin-1.png"
    assert (root / "public" / "talking-head" / "popin-1.png").read_bytes() == b"p"
