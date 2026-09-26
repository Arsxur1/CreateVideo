"""Generate sound effects with ElevenLabs Sound Effects v2 through fal.ai.

Uses the shared ``FAL_KEY`` credential and the fal.ai queue API, then downloads
the generated MP3 to a project-local path.
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    RetryPolicy,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)


class FalElevenLabsSfx(BaseTool):
    """Generate a short sound effect from a text description through fal.ai."""

    name = "fal_elevenlabs_sfx"
    version = "0.1.0"
    tier = ToolTier.GENERATE
    capability = "sound_effects"
    provider = "fal.ai"
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.ASYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.API

    dependencies = ["env:FAL_KEY"]
    install_instructions = (
        "Set FAL_KEY to a fal.ai API key. "
        "Get one at https://fal.ai/dashboard/keys"
    )
    fallback_tools = ["freesound_music"]
    agent_skills = ["sound-effects", "elevenlabs"]

    capabilities = ["generate_sound_effect"]
    supports = {"duration_control": True, "loop": True}
    best_for = [
        "cartoon and UI sound effects from a text description",
        "short impacts, whooshes, squeaks and foley through a shared fal.ai account",
    ]
    not_good_for = ["music", "speech", "offline generation"]

    input_schema = {
        "type": "object",
        "required": ["prompt"],
        "properties": {
            "prompt": {"type": "string", "description": "Description of the sound"},
            "duration_seconds": {
                "type": "number",
                "minimum": 0.5,
                "maximum": 22,
                "description": "Target length; omit to let the model decide",
            },
            "prompt_influence": {
                "type": "number",
                "minimum": 0,
                "maximum": 1,
                "default": 0.3,
            },
            "loop": {"type": "boolean", "default": False},
            "output_path": {"type": "string", "default": "fal_sfx_output.mp3"},
        },
    }

    resource_profile = ResourceProfile(
        cpu_cores=1, ram_mb=256, vram_mb=0, disk_mb=10, network_required=True
    )
    retry_policy = RetryPolicy(max_retries=0, retryable_errors=["rate_limit", "timeout"])
    idempotency_key_fields = ["prompt", "duration_seconds", "prompt_influence", "loop"]
    side_effects = [
        "writes an MP3 file to output_path",
        "submits one paid fal.ai generation request",
    ]
    user_visible_verification = ["Listen to the effect for timing and character"]

    _MODEL = "fal-ai/elevenlabs/sound-effects/v2"
    _QUEUE_URL = f"https://queue.fal.run/{_MODEL}"
    _POLL_INTERVAL_SECONDS = 2
    _MAX_WAIT_SECONDS = 180

    def _get_api_key(self) -> str | None:
        return os.environ.get("FAL_KEY") or os.environ.get("FAL_AI_API_KEY")

    def get_status(self) -> ToolStatus:
        return ToolStatus.AVAILABLE if self._get_api_key() else ToolStatus.UNAVAILABLE

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        """Rough estimate: ~$0.002 per output second, $0.01 floor per request."""
        return round(max(0.01, 0.002 * float(inputs.get("duration_seconds") or 5)), 3)

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        api_key = self._get_api_key()
        if not api_key:
            return ToolResult(
                success=False,
                error="No fal.ai API key found. " + self.install_instructions,
            )

        import requests

        started = time.time()
        headers = {
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json",
        }
        payload: dict[str, Any] = {
            "text": inputs["prompt"],
            "prompt_influence": float(inputs.get("prompt_influence", 0.3)),
            "loop": bool(inputs.get("loop", False)),
        }
        if inputs.get("duration_seconds") is not None:
            payload["duration_seconds"] = float(inputs["duration_seconds"])

        try:
            submit_response = requests.post(
                self._QUEUE_URL, headers=headers, json=payload, timeout=30
            )
            submit_response.raise_for_status()
            queue_data = submit_response.json()
            status_url = queue_data["status_url"]
            response_url = queue_data["response_url"]

            deadline = time.monotonic() + self._MAX_WAIT_SECONDS
            while True:
                if time.monotonic() >= deadline:
                    return ToolResult(
                        success=False,
                        error="fal.ai sound effect generation timed out while waiting in the queue",
                        duration_seconds=round(time.time() - started, 2),
                    )
                time.sleep(self._POLL_INTERVAL_SECONDS)
                status_response = requests.get(status_url, headers=headers, timeout=20)
                status_response.raise_for_status()
                status = status_response.json().get("status", "UNKNOWN")
                if status == "COMPLETED":
                    break
                if status in {"FAILED", "CANCELLED"}:
                    return ToolResult(
                        success=False,
                        error=f"fal.ai sound effect generation {status.lower()}",
                        duration_seconds=round(time.time() - started, 2),
                    )

            result_response = requests.get(response_url, headers=headers, timeout=30)
            result_response.raise_for_status()
            audio_url = result_response.json()["audio"]["url"]

            audio_response = requests.get(audio_url, timeout=60)
            audio_response.raise_for_status()
            output_path = Path(inputs.get("output_path", "fal_sfx_output.mp3"))
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(audio_response.content)
        except Exception as exc:
            safe_error = str(exc).replace(api_key, "[REDACTED]")
            return ToolResult(
                success=False,
                error=f"fal.ai ElevenLabs sound effect generation failed: {safe_error}",
                duration_seconds=round(time.time() - started, 2),
            )

        return ToolResult(
            success=True,
            data={
                "provider": "fal.ai",
                "model": self._MODEL,
                "prompt": inputs["prompt"],
                "output": str(output_path),
                "format": "mp3",
            },
            artifacts=[str(output_path)],
            cost_usd=self.estimate_cost(inputs),
            duration_seconds=round(time.time() - started, 2),
            model=self._MODEL,
        )
