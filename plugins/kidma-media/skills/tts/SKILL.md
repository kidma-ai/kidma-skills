---
description: "Synthesize speech (Hebrew or any language) from text via Gemini TTS (`gemini-3.1-flash-tts-preview`). Outputs a 24 kHz mono WAV file using one of the prebuilt voices (Achernar — warm/neutral default, Algieba — instructional, Aoede — expressive narrative). Use when the user wants to turn an article, lesson summary, paragraph, or arbitrary text into spoken audio. Pairs naturally with `kidma-marketing:write-article` (listenable article version) and `kidma-pedagogy:lesson-exercise` (student audio recap). Triggers: 'make audio of', 'narrate this', 'read this aloud', 'turn this into speech', 'TTS this', 'voice over', 'תקריא את הטקסט', 'צור הקלטה', 'אודיו של', 'קריינות'."
type: action
depends_on:
  - kidma-media:setup
runtime_tools:
  - bash
python_packages:
  - google-genai
  - Pillow
  - pyyaml
---

# kidma-media: Text-to-Speech

Synthesize text to a 24 kHz mono WAV file via Gemini TTS. Voice is read from the user config (set during `/setup`); override per-call with `--voice`.

## Calling the script

**Inline text:**
```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/tts.py" \
  --text "שלום, אני מורה בבית ספר יסודי."
```

**From a file (typical for an article):**
```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/tts.py" \
  --text-file /path/to/article-body.txt
```

**From stdin (chain with another tool):**
```bash
echo "Some text" | python "${CLAUDE_PLUGIN_ROOT}/scripts/tts.py" --stdin
```

Flags:

| Flag           | Default                                                  | Notes                              |
|----------------|----------------------------------------------------------|------------------------------------|
| `--text` / `--text-file` / `--stdin` | (one required)                              | Source of the text.                |
| `--model`      | `gemini-3.1-flash-tts-preview`                           | Override only when explicitly asked. |
| `--voice`      | from `~/.config/kidma-media/config.json` (or `Achernar`) | `Achernar` / `Algieba` / `Aoede`.  |
| `--out`        | auto                                                     | WAV path.                          |

Output: prints the saved WAV path to stdout.

## Voice picking

| Voice     | Feel                                                              | Use for                                |
|-----------|-------------------------------------------------------------------|----------------------------------------|
| `Achernar`| Warm, neutral.                                                    | Default. Most use cases.               |
| `Algieba` | Clear, instructional.                                             | Lesson summaries, explainers.          |
| `Aoede`   | Expressive, narrative.                                            | Articles, stories, longer-form pieces. |

If the user names a specific voice in chat, pass it via `--voice`. To change the persistent default, edit `~/.config/kidma-media/config.json` (`tts_voice` key) or just call with `--voice` every time.

## Long text

Gemini TTS has a per-call character cap (currently a few thousand characters). For long articles:

1. Split the input at paragraph boundaries (blank lines).
2. Call this script per chunk.
3. Concatenate the resulting WAVs with `ffmpeg`:
   ```bash
   ffmpeg -f concat -safe 0 -i <(for f in chunk-*.wav; do echo "file '$f'"; done) -c copy combined.wav
   ```

The skill body should split for the user when input clearly exceeds the cap; otherwise pass the whole text in one call.

## Failure modes

- Empty input → exit 1 immediately.
- "No audio data returned" usually means safety filtering or an empty model response — surface the message to the user and try a shorter excerpt.
- Preflight failures → `/setup` first.
