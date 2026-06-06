# kidma-media

Generate and edit media via the Gemini API from Claude Code.

| Skill              | What it does                                                                |
|--------------------|-----------------------------------------------------------------------------|
| `setup`            | One-time prerequisite check + fix (deps, API key, MCP, output dir).         |
| `generate-image`   | Nano Banana 2 + Imagen 4 + Kidma brand presets.                             |
| `edit-image`       | Modify an existing image with a natural-language instruction (Nano Banana). |
| `generate-video`   | Veo 3.1 fast — text-to-video and image-to-video.                            |
| `describe-image`   | Gemini multimodal understanding / OCR (Hebrew RTL-aware).                   |
| `tts`              | Gemini TTS — synthesize Hebrew speech to WAV.                               |
| `refresh-models`   | Keep `assets/models.yaml` current via the Gemini docs MCP.                  |

## Architecture

```
kidma-media/
├── assets/models.yaml         # single source of truth for model IDs + presets + voices
├── scripts/                   # Python helpers; each script ≤ 200 lines
│   ├── _shared.py             # preflight, output dir, slug, preset apply, etc.
│   ├── setup_check.py
│   ├── generate_image.py
│   ├── edit_image.py
│   ├── generate_video.py
│   ├── describe_image.py
│   ├── tts.py
│   └── refresh_models.py
└── skills/                    # one SKILL.md per capability
```

No skill hardcodes a model ID. They read `assets/models.yaml` via `_shared.load_models()`. To pin a non-default model per call, pass `--model <id>`.

## Models in use (as of 2026-06-06)

- **Images** — `gemini-3.1-flash-image` (Nano Banana 2, default), `gemini-3-pro-image` (Nano Banana Pro), `imagen-4.0-generate-001` (Imagen 4).
- **Video** — `veo-3.1-fast-generate-001` (default), `veo-3.1-generate-001` (higher quality).
- **Understanding / OCR** — `gemini-3.5-flash`.
- **TTS** — `gemini-3.1-flash-tts-preview` with voices `Achernar`, `Algieba`, `Aoede`.

Run `/refresh-models` to keep these current.

## Brand presets

`generate-image --preset <name>` wraps the user's prompt with brand-specific framing. Names mirror what `kidma-marketing:article-image-prompt` recommends:

- `kidma-warm-documentary` — photorealistic Israeli school scene.
- `kidma-blue-conceptual` — flat illustration, Kidma blue (#2669F6), Understand stage.
- `kidma-green-conceptual` — light green (#93DC88), Try stage.
- `kidma-pink-conceptual` — pink (#FF70A3), Create stage.

To add a preset, append an entry to `presets:` in `assets/models.yaml`. No code change required.

## Configuration

`/setup` writes to `~/.config/kidma-media/config.json`:

```json
{
  "output_dir": "/Users/you/kidma-media-outputs",
  "tts_voice": "Achernar"
}
```

Override per-session with the `KIDMA_MEDIA_OUTPUT_DIR` env var.

## Auth

Uses **AI Studio** API key (`GEMINI_API_KEY` / `GOOGLE_API_KEY` env var). Not configured for Vertex / Agent Platform enterprise mode.

## Dependencies (auto-installed by `/setup`)

- Python 3.9+
- `google-genai` (≥ 2.0.0)
- `Pillow`
- `PyYAML`

## Related plugins

- `kidma-marketing:article-image-prompt` — generates the prompt that this plugin's `generate-image` executes.
- `kidma-marketing:write-article` — articles whose body can be fed to `tts`.
- `kidma-pedagogy:lesson-exercise` — student summary PDFs that can be paired with TTS audio.
