---
description: "Generate an image with the Gemini API and save it to disk. Routes between Nano Banana 2 (`gemini-3.1-flash-image`, default — fast, conversational, supports reference images) and Imagen 4 (`imagen-4.0-generate-001`, photoreal, multi-variant). Supports Kidma brand presets (`kidma-warm-documentary`, `kidma-blue-conceptual`, `kidma-green-conceptual`, `kidma-pink-conceptual`) that bake the right Kidma color into the prompt for one-shot brand-aligned output. Use when the user asks to generate, create, draw, or make an image, picture, hero image, illustration, or visual. Triggers: 'generate an image', 'create a picture of', 'make a hero image', 'draw a', 'illustration of', 'visualize', 'image of', 'ייצר תמונה', 'צייר', 'תמונה של', 'create variants of'. If the user just produced a prompt via `article-image-prompt`, run this skill to execute it. Pair with `edit-image` for follow-up modifications."
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

# kidma-media: Generate Image

Routes to the right model based on what the user asked for, applies a brand preset if requested, calls the Gemini API, and saves the PNG to the configured output dir (or wherever the user asked).

## Model selection

- **Default** → Nano Banana 2 (`gemini-3.1-flash-image`). Best for everyday work, iterative refinements, and any case where the user provides reference images.
- **Imagen 4** (`imagen-4.0-generate-001`) → use when the user says "photoreal", "high fidelity", asks for **multiple variants** (e.g., "give me 4 versions"), or the prompt is purely text-to-image with no refs.
- **Nano Banana Pro** (`gemini-3-pro-image`) → use when the user explicitly asks for "the pro model" or "highest quality" and is willing to wait.

If the user's intent is ambiguous about model choice, prefer the default. You can always re-run with `--family imagen` if the first pass disappoints.

## Brand presets

Mirrors `kidma-marketing:article-image-prompt`. Use a preset whenever the context is a Kidma article, school proposal, or other branded surface:

| Preset                       | When to use                                                  |
|------------------------------|--------------------------------------------------------------|
| `kidma-warm-documentary`     | Style A — real Israeli school photo, warm and human          |
| `kidma-blue-conceptual`      | Style B, Understand stage (research, analysis, learning)     |
| `kidma-green-conceptual`     | Style B variant, Try stage (experimentation, activities)     |
| `kidma-pink-conceptual`      | Style B variant, Create stage (creativity, making, projects) |

Each preset injects a `prompt_prefix` and `prompt_suffix` and sets sensible aspect + size defaults. The user's prompt becomes the "subject" inside the preset's framing.

## Disambiguation before calling

Before invoking the script, check the user's request against three axes. Resolve any axis they did **not** pin (in chat or via a flag) with a single grouped `AskUserQuestion`. Skip the prompt entirely if all axes are pinned.

| Axis    | Pinned when…                                          | Ask if ambiguous                                                                                          |
|---------|-------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| Preset  | User named a preset, or said "not brand"              | `kidma-warm-documentary` / `kidma-blue-conceptual` / `kidma-green-conceptual` / `kidma-pink-conceptual` / `No preset (Recommended)` |
| Model   | User said "photoreal", "Pro", "Imagen", or "variants" | `Nano Banana 2 (Recommended)` / `Imagen 4 (photoreal)` / `Nano Banana Pro (slow, best quality)`           |
| Aspect  | User named a target (hero, square, vertical, story)   | `1:1 (Recommended)` / `16:9 horizontal` / `9:16 vertical` / `4:3` / `3:4`                                 |

Defaults shown as **Recommended** are the cheapest/fastest options — list them first. Only ask for axes that are genuinely unresolved; one round of questions, not three.

## Calling the script

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/generate_image.py" \
  --prompt "A teacher in her 40s reviewing a student's tablet in a sunlit Israeli classroom" \
  --preset kidma-warm-documentary
```

Common flags:

| Flag         | Meaning                                                              |
|--------------|----------------------------------------------------------------------|
| `--prompt`   | Required. The subject. The preset (if any) wraps this.               |
| `--model`    | Explicit model ID. Overrides the family default.                     |
| `--family`   | `nano-banana` or `imagen`. Skip — auto-detected unless overriding.   |
| `--preset`   | Brand preset name. See table above.                                  |
| `--aspect`   | `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `5:4`, `4:5`. Overrides preset. |
| `--size`     | `1K` or `2K`. Nano Banana only.                                      |
| `--count`    | Imagen-only. Number of variants (1–4). Picks Imagen automatically if > 1. |
| `--ref`      | Comma-separated paths to reference images (Nano Banana only).        |
| `--out`      | Explicit output path. Otherwise auto-named under the configured output dir. |

The script writes `→ family=... model=...` to stderr so you can confirm the route, and prints saved file paths to stdout (one per line).

## Examples

**Plain image:**
```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/generate_image.py" \
  --prompt "A yellow banana in a fancy restaurant, Gemini-themed"
```

**Four Imagen variants:**
```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/generate_image.py" \
  --prompt "A robot holding a red skateboard" \
  --count 4 --aspect 1:1
```

**Brand-aligned conceptual illustration for an article about analyzing data:**
```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/generate_image.py" \
  --prompt "A magnifying glass over a bar chart, hands sketching a conclusion" \
  --preset kidma-blue-conceptual
```

**Multi-reference composite:**
```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/generate_image.py" \
  --prompt "An office group photo of these people, smiling, in a school staff room" \
  --ref /Users/adarf/Desktop/principal.jpg,/Users/adarf/Desktop/teacher.jpg
```

## After running

- Read the stdout path and report it to the user.
- If the result doesn't satisfy the brief, propose either (a) `edit-image` with the produced PNG as input, or (b) re-running with `--preset` or `--family imagen` for a different look. Don't silently re-run.
- For Hebrew prompts the filename auto-slug will be a short numeric tail — that's expected; use `--out` if you want a meaningful name.

## Failure modes

- If `python ... generate_image.py` exits non-zero with a "preflight failed" message, the user hasn't run `/setup` yet. Run `/setup` first, then retry.
- Quota / safety blocks come back as non-zero exits with the Gemini error message on stderr — surface that verbatim to the user.
