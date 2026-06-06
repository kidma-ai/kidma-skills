#!/usr/bin/env python3
"""Helper for the `refresh-models` skill.

The actual "what are the current Gemini model IDs?" lookup happens in the
agent (calling the `mcp__gemini-api-docs__search_docs` tool) — that's the
only place the MCP is reachable. This script handles the surrounding
mechanics:

  - `--show`    Print the current models.yaml as JSON (for the agent to diff against).
  - `--validate` Confirm models.yaml parses and has the required keys.
  - `--path`     Print the absolute models.yaml path so the agent can Edit it directly.

Usage:
    python refresh_models.py --show
    python refresh_models.py --validate
    python refresh_models.py --path
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _shared import MODELS_YAML, load_models  # noqa: E402


REQUIRED_TOP_LEVEL = {"defaults", "image_models", "video_models"}
REQUIRED_DEFAULT_KEYS = {"image", "imagen", "video", "describe", "tts"}


def show() -> int:
    print(json.dumps(load_models(), indent=2, ensure_ascii=False))
    return 0


def validate() -> int:
    try:
        models = load_models()
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"✗ Failed to parse {MODELS_YAML}: {e}\n")
        return 1

    missing_top = REQUIRED_TOP_LEVEL - models.keys()
    if missing_top:
        sys.stderr.write(f"✗ Missing top-level keys: {sorted(missing_top)}\n")
        return 1

    defaults = models.get("defaults") or {}
    missing_defaults = REQUIRED_DEFAULT_KEYS - defaults.keys()
    if missing_defaults:
        sys.stderr.write(f"✗ defaults missing keys: {sorted(missing_defaults)}\n")
        return 1

    if not models.get("image_models"):
        sys.stderr.write("✗ image_models is empty\n")
        return 1
    if not models.get("video_models"):
        sys.stderr.write("✗ video_models is empty\n")
        return 1

    print("✓ models.yaml is valid")
    return 0


def path() -> int:
    print(str(MODELS_YAML))
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--show", action="store_true", help="Print current models.yaml as JSON")
    g.add_argument("--validate", action="store_true", help="Validate models.yaml structure")
    g.add_argument("--path", action="store_true", help="Print absolute path to models.yaml")
    args = p.parse_args()

    if args.show:
        return show()
    if args.validate:
        return validate()
    if args.path:
        return path()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
