---
description: "One-time setup for the kidma-media plugin. Detects and (where possible) auto-fixes prerequisites for generating images and videos via the Gemini API: Python 3.9+, google-genai, Pillow, PyYAML, GEMINI_API_KEY, the gemini-api-docs MCP server, a writable output directory, and a quick API ping to confirm the key works. Run this once before using `generate-image`, `edit-image`, `generate-video`, `describe-image`, or `tts`. Triggers: 'set up kidma-media', 'configure gemini', 'install gemini deps', 'why isn't generate-image working', 'check my gemini setup', 'setup nano banana'."
type: setup
runtime_tools:
  - bash
python_packages:
  - google-genai
  - Pillow
  - pyyaml
---

# kidma-media: Setup

Run the setup check once. It detects what's missing and installs / configures what it can. Safe to re-run any time — it's idempotent.

## What it does

1. Verifies Python 3.9+ is the running interpreter.
2. `pip install --user`s any missing Python packages (`google-genai`, `Pillow`, `pyyaml`).
3. Confirms `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) is in the environment. If absent, prints instructions to generate one at https://aistudio.google.com/apikey and add it to your shell rc file. The key is **never echoed**.
4. Registers the `gemini-api-docs` MCP server at user scope if not already present (`claude mcp add --transport http --scope user gemini-api-docs https://gemini-api-docs-mcp.dev`).
5. Resolves and creates the output directory (priority order: `KIDMA_MEDIA_OUTPUT_DIR` env var → `~/.config/kidma-media/config.json` → `/mnt/user-data/outputs/` → `~/kidma-media-outputs/`) and persists the choice to user config.
6. Sets a default TTS voice (`Achernar`) in user config if not already set.
7. Sends a 1-token text request to `gemini-3.5-flash` to confirm the API key actually works.

## Run it

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/setup_check.py"
```

If you want a dry-run that never installs anything:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/setup_check.py" --no-install
```

## Exit codes

- `0` — all checks passed.
- `1` — one or more checks failed; the script printed actionable next steps for each.
- `2` — Python is too old or `_shared.py` is missing (rare).

## After setup

Restart Claude Code so the MCP server's `search_documentation` tool is loaded into your session. Then try:

- "generate an image of a yellow banana in a fancy restaurant"
- "make a 5-second video of a butterfly landing on a flower"
- `/skills` — confirms all seven `kidma-media` skills are listed.
