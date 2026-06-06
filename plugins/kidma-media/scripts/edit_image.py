#!/usr/bin/env python3
"""Edit an image via Nano Banana.

Takes an input image and a natural-language modification instruction, returns
a new image. The script is stateless — for multi-turn iterative editing, the
calling skill feeds the previous output back as the new --input.

Usage:
    python edit_image.py --input PATH --prompt "..." [--model ID]
                         [--aspect 16:9] [--size 2K] [--out PATH]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _shared import (  # noqa: E402
    client,
    load_models,
    out_path,
    preflight,
    read_image_bytes,
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Edit an image with Nano Banana")
    p.add_argument("--input", required=True, help="Path to the image to edit")
    p.add_argument("--prompt", required=True, help="The modification instruction")
    p.add_argument("--model", help="Override the default Nano Banana model ID")
    p.add_argument("--aspect", help="Aspect ratio (e.g., 16:9)")
    p.add_argument("--size", help="Image size (1K|2K)")
    p.add_argument("--out", help="Output path. Default: auto-named under output dir.")
    return p.parse_args()


def main() -> int:
    preflight()
    args = parse_args()

    from google.genai import types

    model = args.model or load_models().get("defaults", {}).get("image", "gemini-3.1-flash-image")
    data, mime = read_image_bytes(args.input)

    contents = [args.prompt, types.Part.from_bytes(data=data, mime_type=mime)]

    image_cfg_kwargs = {}
    if args.aspect:
        image_cfg_kwargs["aspect_ratio"] = args.aspect
    if args.size:
        image_cfg_kwargs["image_size"] = args.size

    cfg_kwargs = {"response_modalities": ["IMAGE"]}
    if image_cfg_kwargs:
        cfg_kwargs["image_config"] = types.ImageConfig(**image_cfg_kwargs)
    config = types.GenerateContentConfig(**cfg_kwargs)

    sys.stderr.write(f"→ editing {Path(args.input).name} with {model}\n")
    response = client().models.generate_content(model=model, contents=contents, config=config)

    target = out_path(args.prompt or "edit", "png", override=args.out)
    target.parent.mkdir(parents=True, exist_ok=True)

    saved = False
    for part in response.parts or []:
        if getattr(part, "text", None):
            sys.stderr.write(part.text + "\n")
        if getattr(part, "inline_data", None) is not None:
            part.as_image().save(target)
            saved = True
            break

    if not saved:
        sys.stderr.write("✗ No edited image returned by the model.\n")
        return 1

    print(target.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
