"""Audio mixer tool wrapping FFmpeg and pydub.

Mixes speech, music, and SFX tracks with support for ducking, fades,
and volume normalization. Falls back to FFmpeg-only mode if pydub is
not installed.
"""

from __future__ import annotations

import functools
import json
import math
import subprocess
import time
from pathlib import Path
from typing import Any

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    ToolResult,
    ToolStability,
    ToolStatus,
    ToolTier,
)


@functools.lru_cache(maxsize=None)
def _alimiter_supports_latency() -> bool:
    """True when this ffmpeg's alimiter has the ``latency`` option (FFmpeg 5.0+)."""
    try:
        proc = subprocess.run(
            ["ffmpeg", "-hide_banner", "-h", "filter=alimiter"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=15,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return "latency" in f"{proc.stdout}{proc.stderr}"


class AudioMixer(BaseTool):
    name = "audio_mixer"
    version = "0.1.0"
    tier = ToolTier.CORE
    capability = "audio_processing"
    provider = "ffmpeg"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.DETERMINISTIC

    dependencies = ["cmd:ffmpeg"]
    install_instructions = (
        "FFmpeg is required. pydub is optional for advanced mixing:\n"
        "pip install pydub"
    )
    agent_skills = ["ffmpeg", "video-toolkit"]

    capabilities = ["mix", "duck", "fade", "normalize", "extract_audio", "segmented_music"]

    input_schema = {
        "type": "object",
        "required": ["operation"],
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["mix", "duck", "extract", "full_mix", "segmented_music"],
                "description": (
                    "mix: layer multiple tracks with volume/delay/fades. "
                    "duck: lower music volume when speech is present. "
                    "extract: extract audio from video file. "
                    "full_mix: combine narration tracks + music with ducking + normalize "
                    "in a single call (preferred for compose-director). "
                    "segmented_music: mix music into a video only during specified "
                    "time segments (e.g. music during talking head, silence during "
                    "showcase clips)."
                ),
            },
            "tracks": {
                "type": "array",
                "description": (
                    "Audio tracks for mix/duck operations (advanced format). "
                    "For duck, each track needs a 'role' of 'speech' or 'music'. "
                    "For the simple duck API, use primary_audio/secondary_audio instead."
                ),
                "items": {
                    "type": "object",
                    "required": ["path", "role"],
                    "properties": {
                        "path": {"type": "string"},
                        "role": {
                            "type": "string",
                            "enum": ["speech", "music", "sfx", "primary", "secondary"],
                        },
                        "volume": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 1.0,
                            "default": 1.0,
                        },
                        "start_seconds": {"type": "number", "minimum": 0},
                        "fade_in_seconds": {"type": "number", "minimum": 0},
                        "fade_out_seconds": {"type": "number", "minimum": 0},
                    },
                },
            },
            "primary_audio": {
                "type": "string",
                "description": (
                    "Path to primary/speech audio track (duck operation, simple format). "
                    "This is the track that stays at full volume (e.g. narration/dialogue). "
                    "Use with secondary_audio as an alternative to the tracks array."
                ),
            },
            "secondary_audio": {
                "type": "string",
                "description": (
                    "Path to secondary/music audio track (duck operation, simple format). "
                    "This track gets ducked (volume lowered) when primary audio is present. "
                    "Use with primary_audio as an alternative to the tracks array."
                ),
            },
            "duck_level": {
                "type": "number",
                "description": (
                    "Ducking attenuation in dB for the secondary track (duck operation, "
                    "simple format). Negative values reduce volume, e.g. -12 means duck "
                    "by 12dB. Converted to a linear ratio internally. Default: -12."
                ),
                "default": -12,
            },
            "input_path": {"type": "string", "description": "Input for extract operation"},
            "output_path": {"type": "string"},
            "ducking": {
                "type": "object",
                "description": (
                    "Advanced ducking parameters. Works with both the simple "
                    "(primary_audio/secondary_audio) and advanced (tracks) formats."
                ),
                "properties": {
                    "enabled": {"type": "boolean", "default": True},
                    "music_volume_during_speech": {
                        "type": "number", "minimum": 0, "maximum": 1.0, "default": 0.15,
                    },
                    "attack_ms": {"type": "number", "default": 200},
                    "release_ms": {"type": "number", "default": 500},
                },
            },
            "normalize": {"type": "boolean", "default": True},
            "loudnorm_target": {
                "type": "number",
                "default": -16,
                "minimum": -40,
                "maximum": 0,
                "description": (
                    "Integrated loudness target (LUFS) for the loudnorm filter when "
                    "normalize=true. Default -16 (Apple Podcasts). Pass -14 for "
                    "YouTube/TikTok/IG per sound-design.md. Matches the "
                    "edit_decisions.metadata.loudnorm_target convention — directors "
                    "should forward that field here so the executed loudness matches "
                    "the platform the asset targets."
                ),
            },
            "video_path": {
                "type": "string",
                "description": (
                    "Path to the assembled video (segmented_music operation). "
                    "Music is mixed into this video's audio at specified segments."
                ),
            },
            "music_path": {
                "type": "string",
                "description": "Path to background music file (segmented_music operation).",
            },
            "music_volume": {
                "type": "number",
                "minimum": 0,
                "maximum": 1.0,
                "default": 0.20,
                "description": "Volume level for music during active segments.",
            },
            "segments": {
                "type": "array",
                "description": (
                    "Time segments where music should play (segmented_music operation). "
                    "Each segment: {start: seconds, end: seconds}. Music fades in/out "
                    "at segment boundaries. Outside these segments, music is silent."
                ),
                "items": {
                    "type": "object",
                    "required": ["start", "end"],
                    "properties": {
                        "start": {"type": "number", "minimum": 0},
                        "end": {"type": "number", "minimum": 0},
                    },
                },
            },
            "fade_duration": {
                "type": "number",
                "default": 0.5,
                "description": "Duration of fade in/out at segment boundaries (seconds).",
            },
            "target_duration": {
                "type": "number",
                "exclusiveMinimum": 0,
                "description": (
                    "full_mix only. Exact output length in seconds. Pads a short "
                    "mix and trims a long mix so audio matches the composition."
                ),
            },
        },
    }

    resource_profile = ResourceProfile(cpu_cores=2, ram_mb=1024, vram_mb=0, disk_mb=500)
    idempotency_key_fields = ["operation", "tracks", "ducking"]
    side_effects = ["writes mixed audio file to output_path"]
    user_visible_verification = [
        "Listen to mixed output and verify speech clarity and music ducking",
    ]

    # full_mix renders at one fixed rate. Otherwise the filtergraph negotiates
    # the first input's rate — usually 22.05/24 kHz TTS — and band-limits the
    # music bed before it is mixed. 48 kHz also lets the true-peak limiter
    # oversample by exactly 4x.
    _FULL_MIX_SAMPLE_RATE = 48000
    _TRUE_PEAK_CEILING_DBTP = -1.5
    # alimiter holds its limit exactly at the oversampled rate, but resampling
    # back down overshoots by up to ~0.5 dB on broadband material it limited
    # hard. Limiting this far below the ceiling keeps the delivered true peak
    # at or under it.
    _LIMITER_MARGIN_DB = 0.5
    # Limiting lowers loudness by an amount the pre-limiter measurement can't
    # predict, so full_mix measures what it rendered and re-renders with a
    # corrected gain until it lands within this tolerance (EBU R128 allows
    # +/-0.5 LU), up to a fixed number of renders.
    _LOUDNESS_TOLERANCE_LU = 0.5
    _MAX_LOUDNESS_RENDERS = 3

    @staticmethod
    def _loudnorm_target(inputs: dict[str, Any]) -> float:
        """Resolve the per-call integrated loudness target in LUFS.

        The target was historically hard-coded to -16 (podcast/Apple).
        sound-design.md targets -14 for YouTube/TikTok/IG, and
        edit_decisions.metadata.loudnorm_target is the declarative form.
        Forward that value (or pass loudnorm_target directly) so the executed
        loudness matches the target platform instead of silently defaulting.
        """
        target = inputs.get("loudnorm_target", -16)
        try:
            target = float(target)
        except (TypeError, ValueError):
            target = -16.0
        # Clamp to a sane loudness range to avoid malformed ffmpeg args.
        return max(-40.0, min(0.0, target))

    @staticmethod
    def _loudnorm_filter(inputs: dict[str, Any], in_label: str, out_label: str) -> str:
        """Build a single-pass loudnorm filter graph edge honoring the LUFS target."""
        target = AudioMixer._loudnorm_target(inputs)
        return f"[{in_label}]loudnorm=I={target}:LRA=11:TP=-1.5[{out_label}]"

    def _measure_loudness(
        self, input_args: list[str], filter_parts: list[str], label: str
    ) -> tuple[float, float]:
        """Return the integrated loudness (LUFS) and true peak (dBTP) of ``[label]``.

        Renders the graph to a null sink through loudnorm in analysis mode
        and reads its JSON report. Silence measures as ``-inf``.
        """
        graph = ";".join([*filter_parts, f"[{label}]loudnorm=print_format=json[measured]"])
        proc = self.run_command([
            "ffmpeg", "-hide_banner", "-nostats",
            *input_args,
            "-filter_complex", graph,
            "-map", "[measured]",
            "-f", "null", "-",
        ])
        report = proc.stderr or ""
        start, end = report.rfind("{"), report.rfind("}")
        try:
            stats = json.loads(report[start:end + 1]) if 0 <= start < end else {}
            return float(stats["input_i"]), float(stats["input_tp"])
        except (ValueError, KeyError, TypeError) as exc:
            raise RuntimeError(
                f"Could not read the loudness measurement from ffmpeg: {exc}"
            ) from exc

    def _true_peak_limit_filter(
        self, in_label: str, gain_db: float, limit_dbfs: float, out_label: str
    ) -> str:
        """Apply a static gain, then hold peaks at ``limit_dbfs``.

        alimiter only sees sample peaks, so it runs at 4x the mix rate where
        sample peaks track true (inter-sample) peaks. ``level=0`` disables its
        auto-level stage, which would otherwise push the output back up to
        0 dBFS. ``latency=1`` removes the 5 ms lookahead delay; FFmpeg 4.x
        lacks the option, and the shift it leaves is harmless to A/V sync.
        """
        rate = self._FULL_MIX_SAMPLE_RATE
        limit = 10 ** (limit_dbfs / 20)
        latency = ":latency=1" if _alimiter_supports_latency() else ""
        chain = [f"volume={gain_db:.2f}dB"] if gain_db else []
        chain += [
            f"aresample={rate * 4}",
            f"alimiter=limit={limit:.6f}:attack=5:release=50:level=0{latency}",
            f"aresample={rate}",
        ]
        return f"[{in_label}]{','.join(chain)}[{out_label}]"

    def _track_filters(self, track: dict[str, Any]) -> list[str]:
        """Build per-track filters on the source timeline before scheduling it.

        ``afade=t=out`` defaults to ``st=0``. Applying it after ``adelay``
        therefore fades the delay silence instead of the source audio, leaving
        a delayed track silent by the time it starts. Fade source samples first
        and add the timeline delay last so both fades follow the track itself.
        """
        filters = []
        volume = track.get("volume", 1.0)
        delay_ms = int(track.get("start_seconds", 0) * 1000)
        fade_in = track.get("fade_in_seconds", 0)
        fade_out = track.get("fade_out_seconds", 0)

        if volume != 1.0:
            filters.append(f"volume={volume}")
        if fade_in > 0:
            filters.append(f"afade=t=in:d={fade_in}")
        if fade_out > 0:
            duration_cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "csv=p=0",
                track["path"],
            ]
            duration = float(self.run_command(duration_cmd).stdout.strip().split("\n")[0])
            fade_start = max(0.0, duration - float(fade_out))
            filters.append(f"afade=t=out:st={fade_start}:d={fade_out}")
        if delay_ms > 0:
            filters.append(f"adelay={delay_ms}|{delay_ms}")

        return filters

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        operation = inputs["operation"]
        start = time.time()

        try:
            if operation == "mix":
                result = self._mix(inputs)
            elif operation == "duck":
                result = self._duck(inputs)
            elif operation == "extract":
                result = self._extract(inputs)
            elif operation == "full_mix":
                result = self._full_mix(inputs)
            elif operation == "segmented_music":
                result = self._segmented_music(inputs)
            else:
                return ToolResult(success=False, error=f"Unknown operation: {operation}")
        except Exception as e:
            return ToolResult(success=False, error=str(e))

        result.duration_seconds = round(time.time() - start, 2)
        return result

    def _mix(self, inputs: dict[str, Any]) -> ToolResult:
        """Mix multiple audio tracks into one output."""
        tracks = inputs.get("tracks", [])
        if not tracks:
            return ToolResult(success=False, error="No tracks provided")

        output_path = Path(inputs.get("output_path", "mixed_audio.wav"))
        normalize = inputs.get("normalize", True)

        # Validate all inputs exist
        for t in tracks:
            if not Path(t["path"]).exists():
                return ToolResult(success=False, error=f"Track not found: {t['path']}")

        # Build FFmpeg complex filter for mixing
        filter_parts = []
        input_args = []

        for i, track in enumerate(tracks):
            input_args.extend(["-i", track["path"]])
            filters = self._track_filters(track)

            if filters:
                filter_chain = ",".join(filters)
                filter_parts.append(f"[{i}:a]{filter_chain}[a{i}]")
            else:
                filter_parts.append(f"[{i}:a]acopy[a{i}]")

        # Amix all processed streams
        mix_inputs = "".join(f"[a{i}]" for i in range(len(tracks)))
        filter_parts.append(
            f"{mix_inputs}amix=inputs={len(tracks)}:duration=longest:dropout_transition=2[mixed]"
        )

        if normalize:
            filter_parts.append(self._loudnorm_filter(inputs, "mixed", "out"))
            out_label = "[out]"
        else:
            out_label = "[mixed]"

        filter_complex = ";".join(filter_parts)

        cmd = ["ffmpeg", "-y"]
        cmd.extend(input_args)
        cmd.extend(["-filter_complex", filter_complex])
        cmd.extend(["-map", out_label, str(output_path)])

        self.run_command(cmd)

        return ToolResult(
            success=True,
            data={
                "operation": "mix",
                "track_count": len(tracks),
                "output": str(output_path),
                "normalized": normalize,
            },
            artifacts=[str(output_path)],
        )

    def _duck(self, inputs: dict[str, Any]) -> ToolResult:
        """Apply ducking: lower music volume when speech is present.

        Accepts two input formats:

        Simple format (preferred for agents):
            {
                "operation": "duck",
                "primary_audio": "speech.mp3",
                "secondary_audio": "music.mp3",
                "duck_level": -12,
                "output_path": "out.wav"
            }

        Advanced format (tracks array):
            {
                "operation": "duck",
                "tracks": [
                    {"path": "speech.mp3", "role": "primary"},  # or "speech"
                    {"path": "music.mp3", "role": "secondary"}  # or "music"
                ],
                "output_path": "out.wav"
            }
        """
        ducking = inputs.get("ducking", {})
        output_path = Path(inputs.get("output_path", "ducked_audio.wav"))

        # --- Resolve speech/music paths from either input format ---
        speech_path = None
        music_path = None

        # Simple format: primary_audio / secondary_audio
        if "primary_audio" in inputs or "secondary_audio" in inputs:
            speech_path = inputs.get("primary_audio")
            music_path = inputs.get("secondary_audio")
            # If duck_level (dB) is provided, convert to linear ratio for
            # music_volume_during_speech.  e.g. -12 dB -> 10^(-12/20) ~ 0.25
            if "duck_level" in inputs and "ducking" not in inputs:
                import math
                db = inputs["duck_level"]
                ducking = dict(ducking)  # copy so we don't mutate caller
                ducking.setdefault(
                    "music_volume_during_speech",
                    round(math.pow(10, db / 20), 4),
                )

        # Advanced format: tracks array with role field
        tracks = inputs.get("tracks", [])
        if tracks and speech_path is None and music_path is None:
            # Support both naming conventions: speech/music and primary/secondary
            speech_tracks = [
                t for t in tracks if t.get("role") in ("speech", "primary")
            ]
            music_tracks = [
                t for t in tracks if t.get("role") in ("music", "secondary")
            ]
            if speech_tracks:
                speech_path = speech_tracks[0]["path"]
            if music_tracks:
                music_path = music_tracks[0]["path"]

        if not speech_path or not music_path:
            return ToolResult(
                success=False,
                error=(
                    "Ducking requires a primary (speech) and secondary (music) track. "
                    "Provide either primary_audio/secondary_audio params, or a tracks "
                    "array with role='speech'/'primary' and role='music'/'secondary'."
                ),
            )

        # Use FFmpeg sidechaincompress for ducking
        music_vol = ducking.get("music_volume_during_speech", 0.15)
        attack = ducking.get("attack_ms", 200) / 1000
        release = ducking.get("release_ms", 500) / 1000

        # Sidechain compress: use speech as the key signal to duck music
        filter_complex = (
            f"[1:a]sidechaincompress="
            f"threshold=0.02:ratio=9:attack={attack}:release={release}:"
            f"level_sc=1:mix=0.9[ducked];"
            f"[ducked]volume={music_vol * 3}[music_out];"  # compensate sidechain level
            f"[0:a][music_out]amix=inputs=2:duration=longest[out]"
        )

        cmd = [
            "ffmpeg", "-y",
            "-i", speech_path,
            "-i", music_path,
            "-filter_complex", filter_complex,
            "-map", "[out]",
            str(output_path),
        ]

        self.run_command(cmd)

        return ToolResult(
            success=True,
            data={
                "operation": "duck",
                "speech_track": speech_path,
                "music_track": music_path,
                "output": str(output_path),
            },
            artifacts=[str(output_path)],
        )

    def _extract(self, inputs: dict[str, Any]) -> ToolResult:
        """Extract audio from a video file."""
        input_path = Path(inputs["input_path"])
        if not input_path.exists():
            return ToolResult(success=False, error=f"Input not found: {input_path}")

        output_path = Path(
            inputs.get("output_path", str(input_path.with_suffix(".wav")))
        )

        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_path),
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            str(output_path),
        ]

        self.run_command(cmd)

        return ToolResult(
            success=True,
            data={
                "operation": "extract",
                "input": str(input_path),
                "output": str(output_path),
            },
            artifacts=[str(output_path)],
        )

    def _full_mix(self, inputs: dict[str, Any]) -> ToolResult:
        """One-call mix: layer narration tracks, add music with ducking, normalize.

        This is the preferred operation for the compose-director skill.
        It combines mix + duck + normalize in one FFmpeg filter graph. Tracks
        are summed at unity gain and the output is 48 kHz. To normalize, it
        measures the premix, renders with one static gain and a true-peak
        limiter (<= -1.5 dBTP), then measures the render and re-renders with a
        corrected gain if limiting cost more than 0.5 LU (at most 3 renders).
        The measurements are returned in ``data["loudness"]``.

        Input format:
            {
                "operation": "full_mix",
                "tracks": [
                    {"path": "narration_s1.mp3", "role": "speech", "start_seconds": 0},
                    {"path": "narration_s2.mp3", "role": "speech", "start_seconds": 10.5},
                    {"path": "music.mp3", "role": "music", "volume": 0.3}
                ],
                "ducking": {
                    "enabled": true,
                    "music_volume_during_speech": 0.15,
                    "attack_ms": 200,
                    "release_ms": 500
                },
                "normalize": true,
                "output_path": "mixed_audio.wav"
            }
        """
        tracks = inputs.get("tracks", [])
        if not tracks:
            return ToolResult(success=False, error="No tracks provided for full_mix")

        output_path = Path(inputs.get("output_path", "full_mix_output.wav"))
        output_path.parent.mkdir(parents=True, exist_ok=True)
        normalize = inputs.get("normalize", True)
        ducking = inputs.get("ducking", {"enabled": True})
        target_duration = inputs.get("target_duration")
        target: float | None = None
        if target_duration is not None:
            try:
                target = float(target_duration)
            except (TypeError, ValueError):
                return ToolResult(success=False, error="target_duration must be a positive number")
            if target <= 0:
                return ToolResult(success=False, error="target_duration must be greater than zero")

        speech_tracks = [t for t in tracks if t.get("role") in ("speech", "primary")]
        music_tracks = [t for t in tracks if t.get("role") in ("music", "secondary")]
        sfx_tracks = [t for t in tracks if t.get("role") == "sfx"]
        all_tracks = speech_tracks + music_tracks + sfx_tracks

        if not all_tracks:
            return ToolResult(success=False, error="No valid tracks (need speech/music/sfx roles)")

        # Validate all files exist
        for t in all_tracks:
            if not Path(t["path"]).exists():
                return ToolResult(success=False, error=f"Track not found: {t['path']}")

        # Build FFmpeg inputs and filter graph
        input_args = []
        filter_parts = []

        for i, track in enumerate(all_tracks):
            input_args.extend(["-i", track["path"]])
            filters = [f"aresample={self._FULL_MIX_SAMPLE_RATE}", *self._track_filters(track)]
            filter_parts.append(f"[{i}:a]{','.join(filters)}[a{i}]")

        # Every amix below uses normalize=0. amix's default normalize=1 scales
        # each input by 1/(inputs still running), and a track placed with
        # adelay counts as running from t=0: with 15 narration lines the
        # first line came out ~23.5 dB down and the last at full level, and
        # the attenuated copy fed to the sidechain key stopped the early lines
        # ducking at all. Tracks are already gain-staged by their volume
        # fields, so they sum at unity and the loudness stage sets the level.

        # If ducking is enabled and we have both speech and music, apply sidechain
        duck_enabled = ducking.get("enabled", True) if isinstance(ducking, dict) else bool(ducking)

        if duck_enabled and speech_tracks and music_tracks:
            # Build ONE speech stream, then split it into two independent
            # branches: one feeds the sidechain compressor as the ducking key,
            # the other is mixed into the final output. A filtergraph label may
            # only be consumed once, so reusing the same speech label for both
            # the sidechain key and the output mix is invalid on stricter ffmpeg
            # builds (e.g. the Linux ffmpeg on CI). asplit makes the fork explicit.
            speech_indices = list(range(len(speech_tracks)))
            speech_labels = "".join(f"[a{i}]" for i in speech_indices)

            if len(speech_tracks) > 1:
                filter_parts.append(
                    f"{speech_labels}amix=inputs={len(speech_tracks)}:duration=longest:"
                    "normalize=0[speech_all]"
                )
            else:
                filter_parts.append(f"[a{speech_indices[0]}]acopy[speech_all]")
            if target is not None:
                filter_parts.append("[speech_all]asplit=2[speech_key_raw][speech_out]")
                filter_parts.append(
                    f"[speech_key_raw]apad=whole_dur={target},"
                    f"atrim=duration={target},asetpts=PTS-STARTPTS[speech_key]"
                )
            else:
                filter_parts.append("[speech_all]asplit=2[speech_key][speech_out]")

            # Mix music tracks together
            music_start = len(speech_tracks)
            music_indices = list(range(music_start, music_start + len(music_tracks)))
            music_labels = "".join(f"[a{i}]" for i in music_indices)

            if len(music_tracks) > 1:
                filter_parts.append(
                    f"{music_labels}amix=inputs={len(music_tracks)}:duration=longest:"
                    "normalize=0[music_mix]"
                )
                music_in = "[music_mix]"
            else:
                music_in = f"[a{music_indices[0]}]"

            # Apply sidechain ducking — music is compressed, [speech_key] is the key
            duck_params = ducking if isinstance(ducking, dict) else {}
            attack = duck_params.get("attack_ms", 200) / 1000
            release = duck_params.get("release_ms", 500) / 1000
            music_vol = duck_params.get("music_volume_during_speech", 0.15)

            filter_parts.append(
                f"{music_in}[speech_key]sidechaincompress="
                f"threshold=0.02:ratio=9:attack={attack}:release={release}:"
                f"level_sc=1:mix=0.9[ducked_music];"
                f"[ducked_music]volume={music_vol * 3}[music_out]"
            )

            # Final mix: the other speech branch + ducked music
            mix_label = (
                "[speech_out][music_out]amix=inputs=2:duration=longest:normalize=0[premix]"
            )

            # Add SFX if present
            sfx_start = len(speech_tracks) + len(music_tracks)
            if sfx_tracks:
                sfx_labels = "".join(f"[a{i}]" for i in range(sfx_start, sfx_start + len(sfx_tracks)))
                filter_parts.append(mix_label.replace("[premix]", "[pressfx]"))
                filter_parts.append(
                    f"[pressfx]{sfx_labels}amix=inputs={1 + len(sfx_tracks)}:duration=longest:"
                    "normalize=0[premix]"
                )
            else:
                filter_parts.append(mix_label)

        else:
            # No ducking: simple amix of all tracks
            all_labels = "".join(f"[a{i}]" for i in range(len(all_tracks)))
            filter_parts.append(
                f"{all_labels}amix=inputs={len(all_tracks)}:duration=longest:normalize=0[premix]"
            )

        # A ducked music stream is gated by the speech sidechain, so its tail
        # can disappear when narration ends. If the caller knows the video
        # duration, make that the authoritative mix length before loudness
        # normalization: apad extends short audio and atrim caps long audio.
        premix_label = "premix"
        if target is not None:
            filter_parts.append(
                f"[premix]apad=whole_dur={target},atrim=duration={target},"
                "asetpts=PTS-STARTPTS[premix_duration]"
            )
            premix_label = "premix_duration"

        # Loudness: measure, then apply ONE static gain. Single-pass loudnorm
        # runs in dynamic mode and rides its gain up in every music-only gap,
        # undoing the sidechain ducking; its two-pass linear=true mode silently
        # reverts to dynamic whenever the gain would push peaks over TP or the
        # measured LRA exceeds the target, both routine for ducked narration.
        # A constant gain keeps the mixed speech/music balance and the limiter
        # catches the peaks it pushes past the ceiling. The limiter also runs
        # with normalize=false: unity-gain amix can sum past full scale.
        #
        # Limiting costs loudness the premix measurement can't foresee, so each
        # normalized render is measured and re-rendered with the shortfall
        # added to the gain. The true peak isn't chased that way: the limiter
        # holds it on PCM, and a lossy encoder's overshoot moves unpredictably
        # with the limit, so an over-ceiling encoded peak is reported instead.
        def finite_or_none(value: float) -> float | None:
            return value if math.isfinite(value) else None

        ceiling = self._TRUE_PEAK_CEILING_DBTP
        limit_dbfs = ceiling - self._LIMITER_MARGIN_DB
        gain_db = 0.0
        target_lufs: float | None = None
        loudness: dict[str, Any] = {"true_peak_ceiling_dbtp": ceiling}
        if normalize:
            measured_lufs, measured_tp = self._measure_loudness(
                input_args, filter_parts, premix_label
            )
            loudness.update({
                "target_lufs": self._loudnorm_target(inputs),
                "measured_lufs": finite_or_none(measured_lufs),
                "measured_true_peak_dbtp": finite_or_none(measured_tp),
            })
            # Below the BS.1770 absolute gate (-70 LUFS) the mix is effectively
            # silent; boosting it would only raise the noise floor.
            if math.isfinite(measured_lufs) and measured_lufs > -70:
                target_lufs = loudness["target_lufs"]
                gain_db = target_lufs - measured_lufs

        renders = 0
        while True:
            renders += 1
            graph = ";".join(p for p in [
                *filter_parts,
                self._true_peak_limit_filter(premix_label, gain_db, limit_dbfs, "out"),
            ] if p)
            cmd = ["ffmpeg", "-y", *input_args, "-filter_complex", graph, "-map", "[out]"]
            if target is not None:
                cmd.extend(["-t", str(target)])
            cmd.append(str(output_path))
            self.run_command(cmd)
            if not normalize:
                break

            output_lufs, output_tp = self._measure_loudness(
                ["-i", str(output_path)], [], "0:a"
            )
            loudness.update({
                "output_lufs": finite_or_none(output_lufs),
                "output_true_peak_dbtp": finite_or_none(output_tp),
            })
            miss_lu = (
                target_lufs - output_lufs
                if target_lufs is not None and math.isfinite(output_lufs)
                else 0.0
            )
            if (
                abs(miss_lu) <= self._LOUDNESS_TOLERANCE_LU
                or renders >= self._MAX_LOUDNESS_RENDERS
            ):
                break
            gain_db += miss_lu

        loudness["gain_db"] = round(gain_db, 2)
        if normalize:
            loudness["renders"] = renders
            warnings = []
            if abs(miss_lu) > self._LOUDNESS_TOLERANCE_LU:
                warnings.append(
                    f"Output measures {output_lufs:.1f} LUFS against the "
                    f"{target_lufs} LUFS target after {renders} renders; closing "
                    "the gap needs heavier peak limiting. Lower loudnorm_target or "
                    "the volume of the loudest tracks."
                )
            if math.isfinite(output_tp) and output_tp > ceiling:
                warnings.append(
                    f"True peak {output_tp:.2f} dBTP is over the {ceiling} dBTP "
                    "ceiling: lossy encoders overshoot the limited PCM. Write a "
                    ".wav to deliver within the ceiling."
                )
            if warnings:
                loudness["warning"] = " ".join(warnings)

        return ToolResult(
            success=True,
            data={
                "operation": "full_mix",
                "speech_tracks": len(speech_tracks),
                "music_tracks": len(music_tracks),
                "sfx_tracks": len(sfx_tracks),
                "ducking_enabled": duck_enabled,
                "normalized": normalize,
                "target_duration": target_duration,
                "sample_rate": self._FULL_MIX_SAMPLE_RATE,
                "loudness": loudness,
                "output": str(output_path),
            },
            artifacts=[str(output_path)],
        )

    def _segmented_music(self, inputs: dict[str, Any]) -> ToolResult:
        """Mix background music into a video only during specified time segments.

        Uses FFmpeg volume expressions with smooth fades at segment boundaries.
        Music is silent outside the specified segments.

        Input format:
            {
                "operation": "segmented_music",
                "video_path": "assembled.mp4",
                "music_path": "bg_music.mp3",
                "music_volume": 0.20,
                "segments": [
                    {"start": 0, "end": 17.0},
                    {"start": 167.0, "end": 175.0}
                ],
                "fade_duration": 0.5,
                "output_path": "final_with_music.mp4"
            }
        """
        video_path = inputs.get("video_path")
        music_path = inputs.get("music_path")
        output_path = Path(inputs.get("output_path", "segmented_music_output.mp4"))
        segments = inputs.get("segments", [])
        music_volume = inputs.get("music_volume", 0.20)
        fade_dur = inputs.get("fade_duration", 0.5)

        if not video_path or not Path(video_path).exists():
            return ToolResult(success=False, error=f"Video not found: {video_path}")
        if not music_path or not Path(music_path).exists():
            return ToolResult(success=False, error=f"Music not found: {music_path}")
        if not segments:
            return ToolResult(success=False, error="No segments specified")

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Get video duration
        dur_cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "csv=p=0",
            video_path,
        ]
        total_dur = float(self.run_command(dur_cmd).stdout.strip().split("\n")[0])

        # Build volume expression for each segment with smooth fades
        parts = []
        for seg in sorted(segments, key=lambda s: s["start"]):
            s = seg["start"]
            e = seg["end"]
            fade_in_end = s + fade_dur
            fade_out_start = e - fade_dur
            parts.append(
                f"if(lt(t,{s}),0,"
                f"if(lt(t,{fade_in_end}),{music_volume}*(t-{s})/{fade_dur},"
                f"if(lt(t,{fade_out_start}),{music_volume},"
                f"if(lt(t,{e}),{music_volume}*({e}-t)/{fade_dur},"
                f"0))))"
            )

        vol_expr = "+".join(f"({p})" for p in parts) if len(parts) > 1 else parts[0]

        filter_complex = (
            f"[1:a]atrim=0:{total_dur},asetpts=PTS-STARTPTS,"
            f"volume='{vol_expr}':eval=frame[music_shaped];"
            f"[0:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[speech];"
            f"[music_shaped]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[music_fmt];"
            # normalize=0: amix's default normalize=1 divides every input by the
            # input count (here x0.5 / -6 dB), which would permanently attenuate
            # the narration across the whole timeline — including stretches where
            # the music volume expression is 0. The music is already scaled by the
            # `volume` expression, so speech must pass at unity. Unlike _mix/
            # _full_mix, this path has no loudnorm stage to mask the halving.
            f"[speech][music_fmt]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[aout]"
        )

        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-stream_loop", "-1",
            "-i", music_path,
            "-filter_complex", filter_complex,
            "-map", "0:v",
            "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            str(output_path),
        ]

        self.run_command(cmd)

        if not output_path.exists():
            return ToolResult(success=False, error="No output produced")

        return ToolResult(
            success=True,
            data={
                "operation": "segmented_music",
                "video": video_path,
                "music": music_path,
                "segments": segments,
                "music_volume": music_volume,
                "fade_duration": fade_dur,
                "output": str(output_path),
            },
            artifacts=[str(output_path)],
        )
