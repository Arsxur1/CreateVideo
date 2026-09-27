"""Regression tests: openai_image must return every image it requests and bills for.

`execute()` requested `n` images from the API and `estimate_cost` scales with
`n`, but result handling was hardcoded to `response.data[0]` — images 1..n-1
were decoded never, written never, and absent from `artifacts`. The user paid
for `n` images and received one. The sibling tools (`grok_image`,
`dashscope_image`) already loop over every returned image.
"""

import base64
import sys
import types
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class _FakeImage:
    def __init__(self, payload: bytes):
        self.b64_json = base64.b64encode(payload).decode()


class _FakeResponse:
    def __init__(self, n: int, usage=None):
        self.data = [_FakeImage(f"IMAGE_{i}".encode()) for i in range(n)]
        self.usage = usage


class _FakeImages:
    def __init__(self, usage=None):
        self._usage = usage

    def generate(self, **kwargs):
        return _FakeResponse(kwargs["n"], usage=self._usage)


class _FakeClient:
    def __init__(self, *a, **k):
        self.images = _FakeImages()


@pytest.fixture
def openai_tool(monkeypatch):
    # Stub the `openai` SDK so execute() runs fully offline.
    fake = types.ModuleType("openai")
    fake.OpenAI = _FakeClient
    monkeypatch.setitem(sys.modules, "openai", fake)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    from tools.graphics.openai_image import OpenAIImage

    return OpenAIImage()


@pytest.fixture
def openai_tool_with_usage(monkeypatch):
    """Same stub, but the SDK response carries a `usage` block like the real
    OpenAI Images API does, so execute() can compute an exact cost."""
    usage = {
        "input_tokens_details": {"text_tokens": 12, "image_tokens": 0, "cached_tokens": 0},
        "output_tokens": 343,
    }

    class _UsageClient:
        def __init__(self, *a, **k):
            self.images = _FakeImages(usage=usage)

    fake = types.ModuleType("openai")
    fake.OpenAI = _UsageClient
    monkeypatch.setitem(sys.modules, "openai", fake)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    from tools.graphics.openai_image import OpenAIImage, compute_cost

    return OpenAIImage(), usage, compute_cost


def test_all_requested_images_are_written(openai_tool, tmp_path):
    out = tmp_path / "gen.png"
    result = openai_tool.execute({"prompt": "p", "n": 4, "output_path": str(out)})

    assert result.success
    assert result.data["images_generated"] == 4
    assert len(result.artifacts) == 4

    files = sorted(tmp_path.glob("*.png"))
    assert len(files) == 4  # every image reached disk, none overwritten
    contents = {f.read_bytes() for f in files}
    assert contents == {b"IMAGE_0", b"IMAGE_1", b"IMAGE_2", b"IMAGE_3"}


def test_artifacts_match_billed_image_count(openai_tool, tmp_path):
    # What the user pays for must equal what they receive.
    inputs = {"prompt": "p", "n": 3, "quality": "high", "output_path": str(tmp_path / "img.png")}
    result = openai_tool.execute(inputs)
    billed = openai_tool.estimate_cost(inputs)

    assert len(result.artifacts) == 3
    assert billed == pytest.approx(0.211 * 3)


def test_single_image_keeps_exact_output_path(openai_tool, tmp_path):
    out = tmp_path / "single.png"
    result = openai_tool.execute({"prompt": "p", "n": 1, "output_path": str(out)})

    assert result.success
    assert result.artifacts == [str(out)]
    assert out.read_bytes() == b"IMAGE_0"


def test_multi_output_paths_are_suffixed_and_unique():
    from tools.graphics.openai_image import OpenAIImage

    paths = OpenAIImage._output_paths("/tmp/art/pic.png", 3, "png")
    assert [p.name for p in paths] == ["pic_1.png", "pic_2.png", "pic_3.png"]
    assert len(set(paths)) == 3


def test_usage_based_cost_for_gpt_image_25(openai_tool_with_usage, tmp_path):
    """The static cost_map is a pre-flight estimate; once the API returns a
    real `usage` block, execute() must bill from it instead."""
    tool, usage, compute_cost = openai_tool_with_usage
    result = tool.execute({
        "prompt": "p", "model": "gpt-image-2.5-flare", "n": 1,
        "output_path": str(tmp_path / "img.png"),
    })
    assert result.success, result.error
    expected_usd, _breakdown = compute_cost("gpt-image-2.5-flare", usage)
    assert result.cost_usd == pytest.approx(expected_usd)
    assert result.data["cost_source"] == "actual"


def test_xhigh_and_max_quality_are_gpt_image_25_only(openai_tool, tmp_path):
    result = openai_tool.execute({
        "prompt": "p", "model": "gpt-image-2", "quality": "xhigh",
        "output_path": str(tmp_path / "img.png"),
    })
    assert result.success is False
    assert "gpt-image-2.5" in result.error
    assert "xhigh" in result.error
