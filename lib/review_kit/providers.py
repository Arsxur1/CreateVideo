"""Check which API keys actually work, not just which are set.

The registry marks a tool "available" when its key exists. That says nothing
about quota: a free Google key lists Veo and Imagen but cannot generate, and a
Fish key with no credit gets 402 on paid models. Every check here is a free
call (list, search, balance). Nothing is generated or billed.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable


# Pexels and Pixabay sit behind a CDN that answers 403 to Python's default User-Agent.
USER_AGENT = "OpenMontage/1.0 (+https://github.com/calesthio/OpenMontage)"


def _get(url: str, headers: dict[str, str] | None = None, timeout: int = 20) -> tuple[int, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.load(resp)
    except urllib.error.HTTPError as exc:
        return exc.code, None
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return 0, str(exc)


def _fish(key: str) -> dict[str, Any]:
    status, data = _get("https://api.fish.audio/wallet/self/api-credit", {"Authorization": f"Bearer {key}"})
    if status != 200:
        return {"ok": False, "detail": f"HTTP {status}: key rejected"}
    credit = float(data.get("credit", 0) or 0)
    if credit <= 0:
        return {"ok": True, "detail": f"key works, API credit ${credit:.4f}: paid models (s2.1-pro, s2-pro, s1) will fail with 402; free promo model only"}
    return {"ok": True, "detail": f"key works, API credit ${credit:.2f}"}


def _google(key: str) -> dict[str, Any]:
    status, data = _get(f"https://generativelanguage.googleapis.com/v1beta/models?pageSize=200&key={key}")
    if status != 200:
        return {"ok": False, "detail": f"Gemini API HTTP {status}"}
    names = {m["name"].split("/")[-1] for m in data.get("models", [])}
    groups = {
        "tts": sorted(n for n in names if "tts" in n),
        "veo": sorted(n for n in names if n.startswith("veo")),
        "imagen": sorted(n for n in names if n.startswith("imagen")),
        "lyria": sorted(n for n in names if n.startswith("lyria")),
    }
    tts_status, _ = _get(f"https://texttospeech.googleapis.com/v1/voices?languageCode=en-IN&key={key}")
    listed = ", ".join(f"{k}: {len(v)}" for k, v in groups.items())
    return {"ok": True, "detail": f"Gemini API works ({listed} models listed; listing does not prove generation quota). "
                                  f"Cloud TTS {'works' if tts_status == 200 else f'HTTP {tts_status}'}."}


def _pexels(key: str) -> dict[str, Any]:
    status, _ = _get("https://api.pexels.com/v1/search?query=moon&per_page=1", {"Authorization": key})
    return {"ok": status == 200, "detail": "search works" if status == 200 else f"HTTP {status}"}


def _pixabay(key: str) -> dict[str, Any]:
    status, _ = _get(f"https://pixabay.com/api/?key={urllib.parse.quote(key)}&q=moon&per_page=3")
    return {"ok": status == 200, "detail": "search works" if status == 200 else f"HTTP {status}"}


def _unsplash(key: str) -> dict[str, Any]:
    status, _ = _get("https://api.unsplash.com/search/photos?query=moon&per_page=1", {"Authorization": f"Client-ID {key}"})
    return {"ok": status == 200, "detail": "search works" if status == 200 else f"HTTP {status}"}


CHECKS: dict[str, tuple[tuple[str, ...], Callable[[str], dict[str, Any]]]] = {
    "fish_audio": (("FISH_AUDIO_API_KEY",), _fish),
    "google": (("GOOGLE_API_KEY", "GEMINI_API_KEY"), _google),
    "pexels": (("PEXELS_API_KEY",), _pexels),
    "pixabay": (("PIXABAY_API_KEY",), _pixabay),
    "unsplash": (("UNSPLASH_ACCESS_KEY",), _unsplash),
}


def check_all() -> dict[str, dict[str, Any]]:
    results = {}
    for name, (env_names, fn) in CHECKS.items():
        key = next((os.environ.get(e) for e in env_names if os.environ.get(e)), None)
        results[name] = fn(key) if key else {"ok": False, "detail": f"not set ({' or '.join(env_names)})"}
    return results
