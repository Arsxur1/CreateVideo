"""Burned-in captions must not be reported missing when their source is traceable."""
import json

from tools.video.video_compose import VideoCompose

check = VideoCompose._burned_in_subtitle_source_exists


def _project(tmp_path, captions):
    art = tmp_path / "proj" / "artifacts"
    art.mkdir(parents=True)
    props = art / "props.json"
    props.write_text(json.dumps({"captions": captions}), encoding="utf-8")
    return props


def test_fragment_reference_resolves_relative_to_project(tmp_path) -> None:
    props = _project(tmp_path, [{"text": "hi", "start": 0, "end": 1}])
    ed = {"bespoke": {"props_path": str(props)}}
    assert check({"source": "artifacts/props.json#captions"}, ed)


def test_atelier_props_with_captions_count_as_burned_in(tmp_path) -> None:
    props = _project(tmp_path, [{"text": "hi", "start": 0, "end": 1}])
    ed = {"composition_mode": "atelier", "bespoke": {"props_path": str(props)}}
    assert check({}, ed)


def test_empty_captions_are_still_missing(tmp_path) -> None:
    props = _project(tmp_path, [])
    ed = {"composition_mode": "atelier", "bespoke": {"props_path": str(props)}}
    assert not check({"source": "artifacts/props.json#captions"}, ed)


def test_plain_subtitle_file_path(tmp_path) -> None:
    srt = tmp_path / "subs.srt"
    srt.write_text("1\n00:00:00,000 --> 00:00:01,000\nhi\n", encoding="utf-8")
    assert check({"source": str(srt)}, {})
    assert not check({"source": str(tmp_path / "missing.srt")}, {})
