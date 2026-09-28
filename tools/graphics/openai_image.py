"""OpenAI GPT Image generation (gpt-image-2, gpt-image-2.5-flare/sunburst)."""

from __future__ import annotations

import base64
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

# USD per 1M tokens, ported from ComfyUI-GPT-Image-Direct's PRICE_PER_1M
# (developers.openai.com/api/docs/pricing, 2026-09-19). gpt-image-2 and
# gpt-image-2.5 share the same rates today.
PRICE_PER_1M = {
    "gpt-image-2": {"text_in": 5.00, "cached_in": 1.25, "image_in": 8.00, "image_out": 30.00},
    "gpt-image-2.5-flare": {"text_in": 5.00, "cached_in": 1.25, "image_in": 8.00, "image_out": 30.00},
    "gpt-image-2.5-sunburst": {"text_in": 5.00, "cached_in": 1.25, "image_in": 8.00, "image_out": 30.00},
}

# quality tiers only gpt-image-2.5 exposes.
GPT_25_ONLY_QUALITIES = {"xhigh", "max"}
GPT_25_MODELS = {"gpt-image-2.5-flare", "gpt-image-2.5-sunburst"}


def compute_cost(model: str, usage: dict[str, Any] | None) -> tuple[float, dict[str, int]]:
    """Exact USD cost from the API's `usage` block. Returns (usd, breakdown dict).

    Ported from ComfyUI-GPT-Image-Direct's compute_cost().
    """
    rates = PRICE_PER_1M.get(model, PRICE_PER_1M["gpt-image-2"])
    usage = usage or {}
    details = usage.get("input_tokens_details") or {}
    text_in = int(details.get("text_tokens", 0) or 0)
    image_in = int(details.get("image_tokens", 0) or 0)
    cached_in = int(details.get("cached_tokens", 0) or 0)
    if not details:
        text_in = int(usage.get("input_tokens", 0) or 0)
    out = int(usage.get("output_tokens", 0) or 0)

    # Cached tokens are billed at the cached rate; OpenAI reports them as part
    # of the input totals, so subtract them from the uncached buckets.
    cached_remaining = cached_in
    image_uncached = max(0, image_in - cached_remaining)
    cached_remaining = max(0, cached_remaining - image_in)
    text_uncached = max(0, text_in - cached_remaining)

    usd = (
        text_uncached * rates["text_in"]
        + image_uncached * rates["image_in"]
        + cached_in * rates["cached_in"]
        + out * rates["image_out"]
    ) / 1_000_000.0
    return usd, {"text_in": text_in, "image_in": image_in, "cached_in": cached_in, "out": out}


def _usage_to_dict(usage: Any) -> dict[str, Any] | None:
    """Normalize the SDK's `response.usage` (a pydantic model) to a plain dict."""
    if usage is None:
        return None
    if isinstance(usage, dict):
        return usage
    if hasattr(usage, "model_dump"):
        return usage.model_dump()
    return dict(usage)


class OpenAIImage(BaseTool):
    name = "openai_image"
    version = "0.1.0"
    tier = ToolTier.GENERATE
    capability = "image_generation"
    provider = "openai"
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.API

    dependencies = []  # checked dynamically
    install_instructions = (
        "Set OPENAI_API_KEY to your OpenAI API key.\n"
        "  pip install openai"
    )
    agent_skills = ["flux-best-practices"]  # general image gen knowledge

    capabilities = ["generate_image", "generate_illustration", "text_to_image"]
    supports = {
        "complex_instructions": True,
        "text_in_image": True,
        "multiple_outputs": True,
    }
    best_for = [
        "complex multi-element compositions",
        "images with text/labels",
        "following detailed instructions accurately",
    ]
    not_good_for = ["offline generation", "budget-constrained projects at high quality"]

    input_schema = {
        "type": "object",
        "required": ["prompt"],
        "properties": {
            "prompt": {"type": "string"},
            "model": {
                "type": "string",
                "enum": ["gpt-image-2", "gpt-image-2.5-flare", "gpt-image-2.5-sunburst"],
                "default": "gpt-image-2",
            },
            "size": {
                "type": "string",
                "enum": [
                    "1024x1024", "1536x1024", "1024x1536", "auto",
                    # gpt-image-2.5 presets
                    "2048x2048", "1536x2048", "2048x1536", "3840x2160", "2160x3840",
                ],
                "default": "1024x1024",
            },
            "quality": {
                "type": "string",
                "enum": ["low", "medium", "high", "xhigh", "max", "auto"],
                "default": "high",
                "description": "xhigh and max are gpt-image-2.5 only.",
            },
            "output_format": {
                "type": "string",
                "enum": ["png", "jpeg", "webp"],
                "default": "png",
            },
            "n": {"type": "integer", "default": 1, "minimum": 1, "maximum": 4},
            "output_path": {"type": "string"},
        },
    }

    resource_profile = ResourceProfile(
        cpu_cores=1, ram_mb=512, vram_mb=0, disk_mb=100, network_required=True
    )
    retry_policy = RetryPolicy(max_retries=2, retryable_errors=["rate_limit", "timeout"])
    idempotency_key_fields = ["prompt", "size", "quality", "model"]
    side_effects = ["writes image file to output_path", "calls OpenAI API"]
    user_visible_verification = ["Inspect generated image for relevance and quality"]

    @staticmethod
    def _output_paths(output_path: str | None, count: int, extension: str) -> list[Path]:
        """Derive one output path per generated image.

        With a single image, honor the requested path as-is. With several,
        suffix each with `_1`, `_2`, … so no image overwrites another.
        """
        ext = extension if extension.startswith(".") else f".{extension}"
        if not output_path:
            return [Path(f"generated_image_{idx + 1}{ext}") for idx in range(count)]

        path = Path(output_path)
        suffix = path.suffix or ext
        if count == 1:
            return [path if path.suffix else path.with_suffix(suffix)]

        base = path.with_suffix("") if path.suffix else path
        return [base.parent / f"{base.name}_{idx + 1}{suffix}" for idx in range(count)]

    def get_status(self) -> ToolStatus:
        if os.environ.get("OPENAI_API_KEY"):
            return ToolStatus.AVAILABLE
        return ToolStatus.UNAVAILABLE

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        # gpt-image-2 per-image pricing at 1024x1024 (non-square sizes run
        # slightly cheaper): https://developers.openai.com/api/docs/guides/image-generation
        # gpt-image-2.5 shares gpt-image-2's token rates; low/medium/high reuse
        # the same published numbers. xhigh/max have no published flat price
        # yet, so they're extrapolated from high's $/token rate (0.211/1756
        # tokens) against ComfyUI-GPT-Image-Direct's EST_OUTPUT_TOKENS -- a
        # rough pre-flight number, superseded by compute_cost() once the API
        # returns real usage.
        quality = inputs.get("quality", "high")
        n = inputs.get("n", 1)
        cost_map = {"low": 0.006, "medium": 0.053, "high": 0.211, "xhigh": 0.360, "max": 0.844, "auto": 0.053}
        return cost_map.get(quality, 0.053) * n

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        if not os.environ.get("OPENAI_API_KEY"):
            return ToolResult(
                success=False,
                error="OPENAI_API_KEY not set. " + self.install_instructions,
            )

        from openai import OpenAI

        start = time.time()
        model = inputs.get("model", "gpt-image-2")
        prompt = inputs["prompt"]
        size = inputs.get("size", "1024x1024")
        n = inputs.get("n", 1)
        quality = inputs.get("quality", "high")

        if quality in GPT_25_ONLY_QUALITIES and model not in GPT_25_MODELS:
            return ToolResult(
                success=False,
                error=f"quality={quality!r} is only supported by gpt-image-2.5 models "
                      f"({', '.join(sorted(GPT_25_MODELS))}), not {model!r}",
            )

        client = OpenAI()

        try:
            output_format = inputs.get("output_format", "png")
            response = client.images.generate(
                model=model,
                prompt=prompt,
                size=size,
                quality=quality,
                output_format=output_format,
                n=n,
            )

            items = response.data or []
            if not items:
                return ToolResult(success=False, error="OpenAI returned no image outputs")

            ext = output_format
            output_paths = self._output_paths(inputs.get("output_path"), len(items), ext)
            outputs: list[str] = []
            for item, out_path in zip(items, output_paths):
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_bytes(base64.b64decode(item.b64_json))
                outputs.append(str(out_path))

            usage = _usage_to_dict(getattr(response, "usage", None))

        except Exception as e:
            return ToolResult(success=False, error=f"OpenAI image generation failed: {e}")

        if usage:
            cost_usd, _breakdown = compute_cost(model, usage)
            cost_source = "actual"
        else:
            cost_usd = self.estimate_cost(inputs)
            cost_source = "estimated"

        return ToolResult(
            success=True,
            data={
                "provider": "openai",
                "model": model,
                "prompt": prompt,
                "output": outputs[0],
                "outputs": outputs,
                "images_generated": len(outputs),
                "cost_source": cost_source,
            },
            artifacts=outputs,
            cost_usd=cost_usd,
            duration_seconds=round(time.time() - start, 2),
            model=model,
        )
