# Changelog — kidma-media

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
