#!/usr/bin/env python3
"""Describe an image (or OCR it) via Gemini multimodal understanding.

Usage:
    python describe_image.py --input PATH [--prompt "..."] [--model ID]

Output: text printed to stdout. No file written.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _shared import client, load_models, preflight, read_image_bytes  # noqa: E402

DEFAULT_PROMPT = (
    "Describe this image in detail. If it contains text, transcribe it verbatim, "
    "preserving the original language. Hebrew should remain right-to-left in the transcript."
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Describe / OCR an image with Gemini")
    p.add_argument("--input", required=True, help="Image to describe")
    p.add_argument("--prompt", default=DEFAULT_PROMPT, help="Custom instruction")
    p.add_argument("--model", help="Override the default multimodal model")
    return p.parse_args()


def main() -> int:
    preflight()
    args = parse_args()

    from google.genai import types

    model = args.model or load_models().get("defaults", {}).get("describe", "gemini-3.5-flash")
    data, mime = read_image_bytes(args.input)

    sys.stderr.write(f"→ model={model}  input={Path(args.input).name}\n")
    response = client().models.generate_content(
        model=model,
        contents=[args.prompt, types.Part.from_bytes(data=data, mime_type=mime)],
    )

    text = (response.text or "").strip()
    if not text:
        sys.stderr.write("✗ Model returned no text.\n")
        return 1
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
