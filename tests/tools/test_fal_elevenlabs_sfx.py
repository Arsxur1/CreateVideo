from __future__ import annotations

from unittest.mock import MagicMock, patch

from tools.audio.fal_elevenlabs_sfx import FalElevenLabsSfx
from tools.base_tool import ToolStatus
from tools.tool_registry import ToolRegistry


def _response(*, json_data=None, content=b""):
    response = MagicMock()
    response.json.return_value = json_data
    response.content = content
    response.raise_for_status.return_value = None
    return response


def test_contract_and_cost(monkeypatch):
    tool = FalElevenLabsSfx()

    monkeypatch.setenv("FAL_KEY", "test-key")
    assert tool.get_status() == ToolStatus.AVAILABLE
    assert tool.estimate_cost({"duration_seconds": 1}) == 0.01
    assert tool.estimate_cost({"duration_seconds": 20}) == 0.04
    assert tool.get_info()["capability"] == "sound_effects"


def test_registry_discovers_provider(monkeypatch):
    monkeypatch.setenv("FAL_KEY", "test-key")
    registry = ToolRegistry()
    registry.discover()
    assert registry.get("fal_elevenlabs_sfx") is not None


def test_execute_submits_once_and_downloads_audio(tmp_path, monkeypatch):
    monkeypatch.setenv("FAL_KEY", "test-key")
    output_path = tmp_path / "squeak.mp3"
    tool = FalElevenLabsSfx()
    tool._POLL_INTERVAL_SECONDS = 0

    post_response = _response(
        json_data={
            "status_url": "https://queue.example/status",
            "response_url": "https://queue.example/result",
        }
    )
    status_response = _response(json_data={"status": "COMPLETED"})
    result_response = _response(json_data={"audio": {"url": "https://media.example/sfx.mp3"}})
    audio_response = _response(content=b"fake-mp3")

    with (
        patch("requests.post", return_value=post_response) as mock_post,
        patch("requests.get", side_effect=[status_response, result_response, audio_response]),
    ):
        result = tool.execute(
            {"prompt": "tiny mouse squeak", "duration_seconds": 0.6, "output_path": str(output_path)}
        )

    assert result.success is True
    assert result.model == "fal-ai/elevenlabs/sound-effects/v2"
    assert output_path.read_bytes() == b"fake-mp3"
    payload = mock_post.call_args.kwargs["json"]
    assert payload["text"] == "tiny mouse squeak"
    assert payload["duration_seconds"] == 0.6


def test_execute_without_key_fails(monkeypatch):
    monkeypatch.delenv("FAL_KEY", raising=False)
    monkeypatch.delenv("FAL_AI_API_KEY", raising=False)
    result = FalElevenLabsSfx().execute({"prompt": "pop"})
    assert result.success is False
