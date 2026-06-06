---
description: "Generate a short video (up to 8 seconds) with the Gemini Veo API and save it to disk. Defaults to `veo-3.1-fast-generate-preview` (per Google's recommendation — quality is usually sufficient, latency much lower than the standard variant). Supports text-to-video and image-to-video. Async: submits → polls every 15s → downloads the MP4 (typical wall time 45–90s). Use when the user asks to generate, create, or make a video, clip, animation, or short film. Triggers: 'generate a video', 'make a video of', 'create a 5 second clip', 'animate this', 'video of X', 'short film', 'צור סרטון', 'סרטון של', 'אנימציה'. Tell the user upfront that this takes ~1 minute so they don't think it's hung."
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

# kidma-media: Generate Video

Submits a Veo request, polls every 15 seconds, downloads the MP4. **Tell the user before running**: "Veo typically takes 45–90 seconds — I'll poll until it's ready."

## Disambiguation before calling

Veo is slow and costly per call — wrong aspect or model means a full re-run. Before invoking, check the request against four axes and resolve unpinned ones in a **single** grouped `AskUserQuestion`. Skip the prompt if all are pinned.

| Axis        | Pinned when…                                  | Ask if ambiguous                                                                  |
|-------------|-----------------------------------------------|-----------------------------------------------------------------------------------|
| Model       | User said "best quality" / "standard Veo"     | `veo-3.1-fast (Recommended — ~45s, cheaper)` / `veo-3.1 (slower, sharper)`        |
| Resolution  | User named a target                           | `720p (Recommended)` / `1080p (higher fidelity, slower)`                          |
| Aspect      | User named a surface (homepage, reel, square) | `16:9 horizontal (Recommended)` / `9:16 vertical / story` / `1:1 square`          |
| Duration    | User gave a number, or said "short" / "long"  | `8s (Recommended — Veo cap, required for 1080p/4k)` / `4s` / `6s`                 |

Defaults marked **Recommended** are the cheapest/fastest. Only ask for axes that are genuinely unresolved.

## Calling the script

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/generate_video.py" \
  --prompt "A butterfly lands on an orange origami flower in a sunny garden" \
  --resolution 720p --duration 8
```

Flags:

| Flag           | Default                         | Notes                                              |
|----------------|---------------------------------|----------------------------------------------------|
| `--prompt`     | (required)                      | Be visual and specific. Mention motion explicitly. |
| `--model`      | `veo-3.1-fast-generate-preview` | Use `veo-3.1-generate-preview` for higher quality. |
| `--resolution` | `720p`                          | `720p` or `1080p` (1080p requires `--duration 8`). |
| `--aspect`     | `16:9`                          | `16:9`, `9:16`, `1:1`.                             |
| `--duration`   | `4`                             | One of `4`, `6`, `8` (Veo 3.1).                    |
| `--image`      | (none)                          | Path to a starting image for image-to-video.       |
| `--out`        | auto                            | Otherwise auto-named under output dir.             |

The script writes progress lines (`⏳ Polling Veo… 30s elapsed`) to stderr. Surface those to the user every couple of ticks so they see life. Print the final saved path to stdout.

## Examples

**Text-to-video, 720p, 8 seconds:**
```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/generate_video.py" \
  --prompt "Slow drone shot of a waterfall in a Galilee forest, golden hour"
```

**Image-to-video animation from a still:**
```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/generate_video.py" \
  --prompt "Slow zoom out, the dog raises its head and looks at the camera" \
  --image /Users/adarf/Desktop/dog.png --duration 6
```

**Vertical 9:16 for social, higher quality:**
```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/generate_video.py" \
  --prompt "Students cheering and high-fiving in a Tel Aviv classroom" \
  --model veo-3.1-generate-preview --aspect 9:16 --resolution 1080p --duration 8
```

## When to switch from fast to standard

Default `veo-3.1-fast-generate-preview` is the upstream recommendation — start there. Switch to `veo-3.1-generate-preview` only if:

- The user explicitly asks for "highest quality" / "best version".
- The fast model produced a clearly subpar result and the user wants to retry.
- The brief has fine detail (text on signs, fine textures) that the fast model struggled with.

## Failure modes

- "operation finished without a response body" — usually a content-safety block. Reword the prompt (avoid people doing dangerous activities, copyrighted characters, etc.).
- A network drop during poll: re-run the call; Veo doesn't expose direct resume in this skill (v1.1 could persist the operation handle).
- Preflight failures send you back to `/setup`.
