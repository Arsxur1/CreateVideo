# Channel themes

A theme is a saved channel look: palette, fonts, caption style, motion, audio levels and voice.
Theme files here are personal and not committed (see `.gitignore`).

```bash
python -m lib.themes list
python -m lib.themes new my-channel --description "..."
python -m lib.themes update my-channel --set palette.accent=#FFB547 --set captions.size=60
python -m lib.themes save my-look --from-project <slug>
python -m lib.themes delete my-channel --yes
python -m lib.themes apply my-channel --project <slug>
```

Applying a theme copies a snapshot into `projects/<slug>/artifacts/theme.json`, so editing or deleting
the theme later never changes a video that is already made. Fields are defined in
`schemas/styles/theme.schema.json`. Workflow: `skills/creative/review-kit.md`.
