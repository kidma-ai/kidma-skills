#!/usr/bin/env python3
"""Generate a video via Veo 3.1.

Async pattern: submit → poll `operation.done` → download MP4.

Usage:
    python generate_video.py --prompt "..." [--model ID]
                             [--resolution 720p|1080p] [--aspect 16:9]
                             [--duration 4|6|8] [--image PATH] [--out PATH]
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _shared import (  # noqa: E402
    client,
    load_models,
    out_path,
    preflight,
    read_image_bytes,
)

POLL_INTERVAL_SECONDS = 15


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate a video with Veo")
    p.add_argument("--prompt", required=True, help="The video description")
    p.add_argument("--model", help="Override the default Veo model ID")
    p.add_argument("--resolution", choices=["720p", "1080p"], default="720p")
    p.add_argument("--aspect", default="16:9", help="Aspect ratio (16:9, 9:16, 1:1)")
    p.add_argument("--duration", type=int, choices=[4, 6, 8], default=4,
                   help="Duration in seconds (Veo 3.1 accepts 4, 6, or 8 only)")
    p.add_argument("--image", help="Optional starting image (path) for image-to-video")
    p.add_argument("--out", help="Output path. Default: auto-named .mp4 under output dir.")
    return p.parse_args()


def main() -> int:
    preflight()
    args = parse_args()

    from google.genai import types
    from PIL import Image

    model = args.model or load_models().get("defaults", {}).get("video", "veo-3.1-fast-generate-preview")

    cfg_kwargs = {
        "aspect_ratio": args.aspect,
        "number_of_videos": 1,
        "duration_seconds": args.duration,
        "resolution": args.resolution,
    }

    call_kwargs = {"model": model, "prompt": args.prompt}
    if args.image:
        # Reuse byte reader for validation; load via PIL for SDK
        read_image_bytes(args.image)
        call_kwargs["image"] = Image.open(args.image)

    sys.stderr.write(f"→ model={model}  resolution={args.resolution}  duration={cfg_kwargs['duration_seconds']}s\n")
    sys.stderr.write("→ submitting Veo request (this typically takes 45–90s)…\n")

    c = client()
    operation = c.models.generate_videos(
        config=types.GenerateVideosConfig(**cfg_kwargs),
        **call_kwargs,
    )

    elapsed = 0
    while not operation.done:
        time.sleep(POLL_INTERVAL_SECONDS)
        elapsed += POLL_INTERVAL_SECONDS
        sys.stderr.write(f"⏳ Polling Veo… {elapsed}s elapsed\n")
        operation = c.operations.get(operation)

    if getattr(operation, "error", None):
        sys.stderr.write(f"✗ Veo operation failed: {operation.error}\n")
        return 1

    response = getattr(operation, "response", None) or getattr(operation, "result", None)
    if response is None:
        sys.stderr.write("✗ Veo operation finished without a response body.\n")
        return 1

    videos = getattr(response, "generated_videos", None) or []
    if not videos:
        sys.stderr.write("✗ Veo response contained no videos.\n")
        return 1

    target = out_path(args.prompt, "mp4", override=args.out)
    target.parent.mkdir(parents=True, exist_ok=True)

    video_obj = videos[0].video
    try:
        c.files.download(file=video_obj)
        video_obj.save(str(target))
    except Exception as e:  # noqa: BLE001
        data = getattr(video_obj, "video_bytes", None)
        if data:
            if isinstance(data, str):
                import base64
                data = base64.b64decode(data)
            target.write_bytes(data)
        else:
            sys.stderr.write(f"✗ Failed to download Veo video: {e}\n")
            return 1

    sys.stderr.write(f"✓ Saved to {target}\n")
    print(target.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
