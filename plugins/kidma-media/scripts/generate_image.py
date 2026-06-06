#!/usr/bin/env python3
"""Generate an image via the Gemini API.

Supports two model families, routed by --family or auto-selected:
  - nano-banana (default)       Conversational image gen + multi-ref support.
  - imagen                      Photoreal stills, multi-variant per call.

Usage:
    python generate_image.py --prompt "..." [--model ID] [--family nano-banana|imagen]
                             [--preset NAME] [--aspect 16:9] [--size 2K] [--count N]
                             [--ref path1,path2,...] [--out PATH]

Output: prints absolute path(s) of saved file(s) to stdout, one per line.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _shared import (  # noqa: E402
    apply_preset,
    client,
    load_models,
    out_path,
    preflight,
    read_image_bytes,
    resolve_preset,
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate an image with Gemini")
    p.add_argument("--prompt", required=True, help="The image description")
    p.add_argument("--model", help="Explicit model ID (overrides defaults)")
    p.add_argument("--family", choices=["nano-banana", "imagen"],
                   help="Model family to use; defaults to nano-banana unless --count > 1")
    p.add_argument("--preset", help="Brand preset name from models.yaml")
    p.add_argument("--aspect", help="Aspect ratio (e.g., 16:9). Overrides preset.")
    p.add_argument("--size", help="Image size (1K|2K). Overrides preset.")
    p.add_argument("--count", type=int, default=1, help="Number of images (Imagen only)")
    p.add_argument("--ref", help="Comma-separated reference image paths (Nano Banana only)")
    p.add_argument("--out", help="Output path (single image). For Imagen --count>1, used as basename.")
    return p.parse_args()


def pick_family(args: argparse.Namespace) -> str:
    if args.family:
        return args.family
    if args.count > 1:
        return "imagen"
    if args.model and "imagen" in args.model.lower():
        return "imagen"
    return "nano-banana"


def pick_model(args: argparse.Namespace, family: str) -> str:
    if args.model:
        return args.model
    defaults = load_models().get("defaults", {})
    if family == "imagen":
        return defaults.get("imagen", "imagen-4.0-generate-001")
    return defaults.get("image", "gemini-3.1-flash-image")


def run_nano_banana(args: argparse.Namespace, model: str, preset: dict | None) -> list[Path]:
    from google.genai import types

    prompt = apply_preset(args.prompt, preset)
    aspect = args.aspect or (preset.get("aspect_ratio") if preset else None)
    size = args.size or (preset.get("image_size") if preset else None)

    contents: list = [prompt]
    if args.ref:
        for ref_path in [r.strip() for r in args.ref.split(",") if r.strip()]:
            data, mime = read_image_bytes(ref_path)
            contents.append(types.Part.from_bytes(data=data, mime_type=mime))

    image_cfg_kwargs = {}
    if aspect:
        image_cfg_kwargs["aspect_ratio"] = aspect
    if size:
        image_cfg_kwargs["image_size"] = size

    cfg_kwargs = {"response_modalities": ["IMAGE"]}
    if image_cfg_kwargs:
        cfg_kwargs["image_config"] = types.ImageConfig(**image_cfg_kwargs)
    config = types.GenerateContentConfig(**cfg_kwargs)

    response = client().models.generate_content(model=model, contents=contents, config=config)

    saved: list[Path] = []
    target = out_path(args.prompt, "png", override=args.out)
    target.parent.mkdir(parents=True, exist_ok=True)

    for part in response.parts or []:
        if getattr(part, "text", None):
            sys.stderr.write(part.text + "\n")
        if getattr(part, "inline_data", None) is not None:
            part.as_image().save(target)
            saved.append(target)
            break

    if not saved:
        sys.stderr.write("✗ No image returned by the model.\n")
        sys.exit(1)
    return saved


def run_imagen(args: argparse.Namespace, model: str, preset: dict | None) -> list[Path]:
    from google.genai import types

    prompt = apply_preset(args.prompt, preset)
    aspect = args.aspect or (preset.get("aspect_ratio") if preset else None)

    cfg_kwargs = {"number_of_images": max(1, args.count)}
    if aspect:
        cfg_kwargs["aspect_ratio"] = aspect

    response = client().models.generate_images(
        model=model,
        prompt=prompt,
        config=types.GenerateImagesConfig(**cfg_kwargs),
    )

    target = out_path(args.prompt, "png", override=args.out)
    stem = target.with_suffix("")
    saved: list[Path] = []
    images = response.generated_images or []
    for idx, gen in enumerate(images, start=1):
        path = target if len(images) == 1 else Path(f"{stem}-{idx}.png")
        data = gen.image.image_bytes
        if isinstance(data, str):
            import base64
            data = base64.b64decode(data)
        path.write_bytes(data)
        saved.append(path)

    if not saved:
        sys.stderr.write("✗ No images returned by Imagen.\n")
        sys.exit(1)
    return saved


def main() -> int:
    preflight()
    args = parse_args()
    preset = resolve_preset(args.preset)
    family = pick_family(args)
    model = pick_model(args, family)

    sys.stderr.write(f"→ family={family}  model={model}\n")
    if preset:
        sys.stderr.write(f"→ preset={args.preset}\n")

    if family == "imagen":
        saved = run_imagen(args, model, preset)
    else:
        saved = run_nano_banana(args, model, preset)

    for p in saved:
        print(p.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
