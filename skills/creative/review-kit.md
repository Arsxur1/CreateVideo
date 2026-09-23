# Review Kit - Footage-Led Vertical Reels with Channel Themes

## When to use

Product and gadget reviews, unboxings, and any short vertical reel built from the user's own
footage plus narration and captions. It runs inside the `hybrid` pipeline. Every stage, gate
and director skill still applies; the kit only replaces hand-written mechanics.

The kit does **not** make creative decisions. The script, the shot list, crops, overlays, music
and theme choice go through the normal gates with the user.

## Look: saved theme or fresh

Ask at the idea stage, and log it as `playbook_selection` in `decision_log`:

- **Saved theme**: the channel look (palette, fonts, caption style, motion, audio levels,
  voice) comes from `themes/<name>.yaml`. Use it for a series, so every video looks like the
  same channel. The per-video creative work is the shot list.
- **Fresh**: one-off atelier composition per `skills/meta/bespoke-composition.md`. Use it when
  the user wants a different look for this video.

List themes with `python -m lib.themes list`. The user can save, update and delete themes; see
`themes/README.md`. A good fresh look can be kept: `python -m lib.themes save <name> --from-project <slug>`
(needs `artifacts/theme.json` in that project).

## Workflow (theme mode)

```bash
python -m lib.review_kit providers          # which keys really work (free checks only)
python -m lib.review_kit new <slug> --title "..." --source "<footage folder>" --theme <name>
```

1. **Idea / script gates**: as normal. When the script is approved, write
   `artifacts/lines.json`: one entry per narration line,
   `{"id", "text": <spoken text>, "captions": [one caption chunk per spoken sentence]}`.
   The spoken language and caption language can differ (Tamil voice, English captions).
   Write narration in plain spoken style, never ad copy.
2. **Scene plan**: inspect the footage (frame sheets), then edit `artifacts/prep.json`:
   rename clips to short names, set `grade` for dark clips (ffmpeg filter, e.g.
   `eq=gamma=1.18`), add 4K crops `{"clip", "t", "x", "y", "w"}` in 1080-wide coordinates.
   Run `prep`. It reports the upscale per crop; over 1.6x will look soft, so widen it.
3. **Assets**:
   ```bash
   python -m lib.review_kit prep <slug>
   python -m lib.review_kit voice <slug>              # TTS per line, trimmed, tempo, stitched
   python -m lib.review_kit captions <slug>           # timed to real pauses, + SRT
   python -m lib.review_kit sfx <slug>
   python -m lib.review_kit music <slug> --query "..." --name <name>   # repeat for candidates
   ```
   Always sample the voice with the user before the full `voice` run. Use `--only <id>` to
   regenerate single lines. Music previews land in `assets/music/previews/`.
4. Write `artifacts/shots.json` (format below), then:
   ```bash
   python -m lib.review_kit props <slug>       # checks gaps, overlaps, missing media
   python -m lib.review_kit validate <slug>    # schema check before any render
   python -m lib.review_kit stills <slug> --cover
   ```
   The assets gate shows `snapshots/contact-sheet.jpg` and the cover.
5. **Edit / compose**: `python -m lib.review_kit render <slug>` (add `--draft` for half scale).
   Loudness is normalised to the theme target inside `video_compose`. Then
   `python -m lib.review_kit review <slug>` for probe, loudness, black frames, gaps and a frame
   sheet. Fix what it flags before presenting.

The kit never writes checkpoints. The agent writes them at each gate, as the pipeline requires.

## shots.json

```json
{
  "music": "audio/music/<name>.mp3",
  "cover": {
    "kicker": "₹1,000",
    "title": "USB Moon Projector",
    "subtitle": "Honest review",
    "image": "stills/photo-moon.jpg"
  },
  "sfx": [{ "name": "pop", "at": 4.62, "volume": 0.6 }],
  "shots": [
    {
      "id": "s01",
      "from": 0,
      "to": 1.4,
      "media": {
        "type": "video",
        "src": "video/moon.mp4",
        "at": 0.1,
        "zoom": [1.0, 1.08],
        "origin": "45% 35%"
      }
    },
    {
      "id": "s02",
      "from": 1.4,
      "to": 3.75,
      "enter": "aperture",
      "aperture": { "cx": 486, "cy": 676 },
      "media": {
        "type": "video",
        "src": "video/moon.mp4",
        "at": 4.2,
        "zoom": [1.14, 1.0]
      }
    },
    {
      "id": "s03",
      "from": 3.75,
      "to": 6.5,
      "media": {
        "type": "still",
        "src": "stills/tray.jpg",
        "zoom": [1.0, 1.1]
      },
      "overlays": [{ "type": "tag", "text": "3 discs", "top": 300 }]
    }
  ]
}
```

- Times are seconds on the narration timeline (`artifacts/timeline.json`). Shots must be
  contiguous and cover the whole reel; `props` rejects gaps.
- `media`: `video` (`at` = source seconds, `rate`, `filter`) or `still` (`drift` = x pan px).
  `zoom` is start/end scale; `origin` is the CSS transform origin.
- `enter`: `cut` (default), `whip` (fast vertical blur, for rapid lists), `aperture` (light
  circle opens from `aperture.cx/cy`, the reveal). `exit`: `cut`, `fade`, `aperture` (closes to
  black, use on the last shot).
- Overlays (`at` = seconds from shot start): `tag`, `bigword`, `price`, `coverage` (corner
  brackets, `box` = [x, y, w, h]), `controls` (rows with `moon|lamp|dim|dot` icons),
  `ring` (ellipse around a real part; `dark: true` for labels on white products), `verdict`,
  `checklist`, `scrim`.
- Max two overlay layers at once (captions plus one). Captions sit at the theme's `captions.top`,
  so keep overlays out of that band.

## Engine notes

- Always render stills through the kit (`stills`). A raw `npx remotion still` uses the
  staged copy under `remotion-composer/projects/<slug>/`, which may be stale; the kit re-stages first.
- Fonts a theme can use are listed in `lib/themes.py` (`TEMPLATE_FONTS`). Adding one needs a
  static import in `templates/review-reel/fonts.ts` too.
- The first 0.3s decides the swipe. Open on motion or the product, not a title card. If first-frame
  previews matter (WhatsApp, Shorts), set the theme's `intro.cover_seconds` (0.3-0.5).
- Filming advice for the user: `docs/review-filming-checklist.md`.
