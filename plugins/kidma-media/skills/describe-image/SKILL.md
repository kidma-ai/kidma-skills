---
description: "Describe an image (or OCR its text) via Gemini multimodal understanding (`gemini-3.5-flash`). Use when the user provides an image and asks to describe, transcribe, OCR, caption, or analyze it. Handles Hebrew text — preserves RTL in the transcript. Useful for: turning whiteboard / notebook photos into text, captioning existing assets before remixing them with `generate-image`, extracting copy from a slide screenshot. Triggers: 'describe this image', 'what does this image show', 'OCR this', 'transcribe this image', 'extract text from this image', 'caption this', 'מה רואים בתמונה', 'תקריא את התמונה', 'תמלל את הטקסט בתמונה'."
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

# kidma-media: Describe Image

Pure read-only. Outputs text to stdout — no file is written.

## Calling the script

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/describe_image.py" \
  --input /path/to/image.png
```

With a custom instruction (OCR-only, structured tagging, etc.):

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/describe_image.py" \
  --input whiteboard.jpg \
  --prompt "Transcribe ONLY the Hebrew text on this whiteboard. Preserve line breaks. Don't describe anything else."
```

Flags:

| Flag       | Default                        | Notes                                                |
|------------|--------------------------------|------------------------------------------------------|
| `--input`  | (required)                     | Local path. PNG / JPG / WEBP / GIF.                  |
| `--prompt` | "Describe… transcribe verbatim" | Override for OCR-only, structured output, etc.       |
| `--model`  | `gemini-3.5-flash`             | Override to `gemini-3.1-pro-preview` for harder OCR. |

## Use cases

- **Whiteboard / notebook → text**: students often hand you a phone photo. Custom prompt: "Transcribe only — no commentary."
- **Captioning before remixing**: describe an asset, then feed the description into `generate-image` to produce a variant.
- **Structured tagging**: prompt for JSON output ("Return JSON with fields: subject, mood, dominant_colors, has_text, language") to drive downstream automation.

## Failure modes

- "Model returned no text" usually means safety filtering — try a different framing or input.
- Preflight failures → run `/setup` first.
