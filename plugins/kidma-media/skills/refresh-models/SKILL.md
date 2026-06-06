---
description: "Refresh the kidma-media `assets/models.yaml` catalog by querying the live Gemini docs MCP server (`mcp__gemini-api-docs__search_docs`) for current model IDs, comparing against the local catalog, and updating defaults. Use this when (a) a `generate-image` / `generate-video` call complains about a deprecated model, (b) Google announces a new Nano Banana / Imagen / Veo / TTS model, or (c) you just want to confirm the catalog is still accurate. Triggers: 'refresh gemini models', 'update model list', 'check for new gemini models', 'is nano banana up to date', 'refresh models.yaml'."
type: maintenance
runtime_tools:
  - bash
python_packages:
  - pyyaml
---

# kidma-media: Refresh Models Catalog

Two-step refresh: (1) query the MCP for current truth, (2) Edit `assets/models.yaml` to match.

## Prerequisite

The `gemini-api-docs` MCP server must be registered. `/setup` adds it; verify with `claude mcp list`.

## Procedure

### 1. Print the current catalog and capture the file path

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/refresh_models.py" --show
python "${CLAUDE_PLUGIN_ROOT}/scripts/refresh_models.py" --path
```

The first prints the parsed YAML as JSON. The second prints the absolute path you'll edit.

### 2. Query the MCP for current model IDs

Call `mcp__gemini-api-docs__search_docs` with each of:

- `"current Gemini image generation model IDs Nano Banana"`
- `"current Imagen model IDs"`
- `"current Veo video model IDs Veo 3"`
- `"current Gemini TTS model IDs"`
- `"Gemini multimodal understanding model IDs gemini flash"`
- `"Gemini model deprecations 2026"`

Cross-reference the responses. Watch for:

- A new flagship Nano Banana (e.g., `gemini-3.2-flash-image`) — should become `defaults.image`.
- New Veo (e.g., `veo-4.x-...`) — should become `defaults.video`.
- Anything in the response flagged "deprecated" — REMOVE from the catalog.
- New voice names for TTS — add to `tts_voices:` list.

### 3. Diff and propose changes to the user

Print a clear diff. Format:

```
Changes proposed to assets/models.yaml:
  defaults.image:  gemini-3.1-flash-image       →  gemini-3.2-flash-image    (new flagship)
  defaults.video:  veo-3.1-fast-generate-001    →  veo-3.1-fast-generate-002  (point update)
  + video_models:  veo-3.1-fast-generate-002    (new entry)
  - video_models:  veo-3.0-generate-preview     (deprecated)
```

If the catalog is already current, say so and stop — no edit needed.

### 4. Apply the changes via Edit tool

Use the `Edit` tool against the path returned by `--path` to apply each change minimally. Preserve all surrounding YAML structure, indentation, and comments. Do NOT regenerate the whole file from scratch — preserve the human-curated `presets:` block verbatim.

### 5. Validate

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/refresh_models.py" --validate
```

If validation fails, revert the edit (re-Edit back to the original) and surface the error.

### 6. Bump CHANGELOG and offer to commit

- Append a dated entry to `plugins/kidma-media/CHANGELOG.md` summarizing the model changes.
- Use `AskUserQuestion` to confirm next step. Options, in order:
  - `Don't commit (Recommended)` — leave the working tree dirty for the user to review.
  - `Commit only` — local commit, no push.
  - `Commit & push` — commit and push to `main`.

  Do NOT commit without an explicit selection.

## Important

- Never silently drop a model from the catalog without confirming the deprecation explicitly came from the MCP.
- Never invent a model ID from training data. The MCP is authoritative.
- The `presets:` and `tts_voices:` blocks are human-curated — only touch them if the MCP explicitly indicates a change (e.g., a voice was removed).
