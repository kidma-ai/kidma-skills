---
description: "Edit an existing image with a natural-language instruction via Nano Banana 2 (`gemini-3.1-flash-image`). Takes an input image path and a description of the change to make (swap background, change colors, add/remove objects, restyle), returns a new image. Stateless — for iterative editing, feed the previous output back as the new input. Use when the user supplies an existing image and asks to modify it. Triggers: 'edit this image', 'change the X in this image', 'remove the Y', 'add a Z', 'swap the background', 'make it look like', 'restyle this', 'ערוך את התמונה', 'שנה את', 'הוסף ל'. If the user just generated an image and wants modifications, chain this skill with the previous output as `--input`."
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

# kidma-media: Edit Image

Apply a natural-language edit to an existing image. Always uses Nano Banana (Imagen is text-only).

## Calling the script

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/edit_image.py" \
  --input /path/to/source.png \
  --prompt "Swap the background to a sunny Tel Aviv beach"
```

Flags:

| Flag       | Meaning                                                                 |
|------------|-------------------------------------------------------------------------|
| `--input`  | Required. Path to the source image (PNG/JPG/WEBP/GIF).                  |
| `--prompt` | Required. Plain-English instruction. Be specific.                       |
| `--model`  | Override (e.g., `--model gemini-3-pro-image` for the Pro variant).      |
| `--aspect` | Force a target aspect ratio.                                            |
| `--size`   | Force `1K` or `2K`.                                                     |
| `--out`    | Explicit output path. Otherwise auto-named.                             |

The script prints the saved path to stdout.

## Iterative editing

The script is stateless — to chain edits, pass the previous output as the next `--input`:

```bash
out1=$(python "${CLAUDE_PLUGIN_ROOT}/scripts/edit_image.py" \
        --input source.png --prompt "Make the desk wooden")
out2=$(python "${CLAUDE_PLUGIN_ROOT}/scripts/edit_image.py" \
        --input "$out1" --prompt "Add a steaming coffee cup on the desk")
```

The agent should propose each next edit explicitly and confirm with the user rather than silently looping.

## Tips for good edits

- One change per call. "Remove the cat AND change the color AND add a hat" tends to fail — split into three calls.
- Be specific about what *not* to change: "keep the lighting and composition identical, only change the wall color to teal".
- For removing objects, name them explicitly: "remove the red car in the bottom-left corner".

## Failure modes

- "No edited image returned" usually means safety filtering blocked the request — reword the prompt and retry.
- Preflight failures send you back to `/setup`.
