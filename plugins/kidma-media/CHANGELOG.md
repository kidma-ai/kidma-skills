# Changelog — kidma-media

## 1.1.1 — 2026-06-06

- `assets/models.yaml`: refreshed Veo entries — `veo-3.1-fast-generate-preview` and `veo-3.1-generate-preview` (the `-001` IDs returned 404). Added `veo-3.1-lite-generate-preview`. Replaced single `duration_seconds: 8` with `durations_seconds: [4, 6, 8]` per current API.
- `scripts/generate_video.py`: `--duration` now `choices=[4, 6, 8]` (default `8`); old default of `5` was rejected by the live preview models. Removed silent clamping that masked invalid values.
- `scripts/generate_video.py`: replaced removed `c.files.download(file=…, download_path=…)` call with the current pattern — `c.files.download(file=video)` then `video.save(path)` — to work with google-genai ≥ 2.8.0.
- `skills/generate-video/SKILL.md`: updated model IDs, duration table, and examples to match.

## 1.1.0 — 2026-06-06

- `generate-image`, `generate-video`, `tts`: prompt the user with `AskUserQuestion` to resolve unpinned axes (preset/model/aspect, resolution/duration, voice) before calling the script. Cheapest/fastest option marked Recommended.
- `setup`: ask which output directory to use when no env var / config / `/mnt/user-data/outputs` applies, instead of silently falling back.
- `refresh-models`: structured commit-or-not prompt; default is "Don't commit".

## 1.0.0 — 2026-06-06

- Initial release.
- Skills: `setup`, `generate-image`, `edit-image`, `generate-video`, `describe-image`, `tts`, `refresh-models`.
- Models wired by default (see `assets/models.yaml`):
  - Image: `gemini-3.1-flash-image` (Nano Banana 2) / `imagen-4.0-generate-001`
  - Video: `veo-3.1-fast-generate-001`
  - Multimodal understanding: `gemini-3.5-flash`
  - TTS: `gemini-3.1-flash-tts-preview`
- Brand presets: `kidma-warm-documentary`, `kidma-blue-conceptual`, `kidma-green-conceptual`, `kidma-pink-conceptual`.
