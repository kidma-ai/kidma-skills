"""Shared helpers for kidma-media scripts.

Keep this module free of API calls — it's loaded by every script and must
stay fast and dependency-light. The only third-party imports are PyYAML
(for models.yaml) and a lazy google.genai import inside `client()` so that
preflight() can run even when the SDK isn't installed yet.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
MODELS_YAML = PLUGIN_ROOT / "assets" / "models.yaml"
USER_CONFIG_DIR = Path.home() / ".config" / "kidma-media"
USER_CONFIG_PATH = USER_CONFIG_DIR / "config.json"


def load_models() -> dict[str, Any]:
    """Parse assets/models.yaml. Raises a friendly error if PyYAML missing."""
    try:
        import yaml
    except ImportError:
        sys.stderr.write(
            "✗ PyYAML not installed. Run the `setup` skill (or "
            "`pip install --user pyyaml`) and try again.\n"
        )
        sys.exit(2)
    with open(MODELS_YAML, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_user_config() -> dict[str, Any]:
    """Load user-level config (output dir, voice preference, etc.). Empty dict if absent."""
    if not USER_CONFIG_PATH.exists():
        return {}
    try:
        return json.loads(USER_CONFIG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_user_config(cfg: dict[str, Any]) -> None:
    USER_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    USER_CONFIG_PATH.write_text(json.dumps(cfg, indent=2), encoding="utf-8")


def get_output_dir() -> Path:
    """Resolve the output dir.

    Order: KIDMA_MEDIA_OUTPUT_DIR > user config > /mnt/user-data/outputs (Claude
    sandbox) > ~/kidma-media-outputs.
    """
    env = os.environ.get("KIDMA_MEDIA_OUTPUT_DIR")
    if env:
        path = Path(env).expanduser()
    else:
        cfg = load_user_config()
        if cfg.get("output_dir"):
            path = Path(cfg["output_dir"]).expanduser()
        elif Path("/mnt/user-data/outputs").is_dir():
            path = Path("/mnt/user-data/outputs")
        else:
            path = Path.home() / "kidma-media-outputs"
    path.mkdir(parents=True, exist_ok=True)
    return path


_SLUG_BAD = re.compile(r"[^a-z0-9-]+")


def slugify_prompt(prompt: str, max_len: int = 40) -> str:
    """Deterministic filesystem-safe slug from a prompt. ASCII-only — Hebrew
    prompts produce a short hash-like tail instead of transliteration."""
    ascii_part = prompt.encode("ascii", "ignore").decode("ascii")
    slug = _SLUG_BAD.sub("-", ascii_part.lower()).strip("-")
    if not slug:
        slug = f"prompt-{abs(hash(prompt)) % 10_000:04d}"
    return slug[:max_len].strip("-") or "prompt"


def out_path(prompt: str, ext: str, *, override: str | None = None) -> Path:
    """Build a default output path; if `override` is set use that verbatim."""
    if override:
        return Path(override).expanduser().resolve()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    return get_output_dir() / f"{slugify_prompt(prompt)}-{stamp}.{ext}"


def resolve_preset(name: str | None) -> dict[str, Any] | None:
    if not name:
        return None
    presets = load_models().get("presets", {}) or {}
    preset = presets.get(name)
    if not preset:
        available = ", ".join(presets.keys()) or "(none)"
        sys.stderr.write(f"✗ Unknown preset '{name}'. Available: {available}\n")
        sys.exit(2)
    return preset


def apply_preset(prompt: str, preset: dict[str, Any] | None) -> str:
    if not preset:
        return prompt
    prefix = (preset.get("prompt_prefix") or "").strip()
    suffix = (preset.get("prompt_suffix") or "").strip()
    return f"{prefix} {prompt.strip()} {suffix}".strip()


def read_image_bytes(path: str) -> tuple[bytes, str]:
    """Read a local image; return (raw_bytes, mime_type)."""
    p = Path(path).expanduser().resolve()
    if not p.is_file():
        sys.stderr.write(f"✗ Image not found: {p}\n")
        sys.exit(2)
    ext = p.suffix.lower().lstrip(".")
    mime_map = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "webp": "image/webp",
        "gif": "image/gif",
    }
    mime = mime_map.get(ext, "image/png")
    return p.read_bytes(), mime


def preflight() -> None:
    """Minimal pre-call check. Exits 2 with a hint to run `/setup` on failure."""
    problems: list[str] = []
    if not os.environ.get("GEMINI_API_KEY") and not os.environ.get("GOOGLE_API_KEY"):
        problems.append("GEMINI_API_KEY is not set")
    try:
        import google.genai  # noqa: F401
    except ImportError:
        problems.append("google-genai package not installed")
    if not MODELS_YAML.is_file():
        problems.append(f"models catalog missing at {MODELS_YAML}")
    if problems:
        sys.stderr.write("✗ kidma-media preflight failed:\n")
        for p in problems:
            sys.stderr.write(f"  • {p}\n")
        sys.stderr.write("Run the `setup` skill to fix.\n")
        sys.exit(2)


_CLIENT = None


def client():
    """Return a configured google.genai Client. Honors GEMINI_API_KEY automatically.

    Cached at module scope so the Client outlives any single call expression.
    Without this, a chained `client().models.generate_content(...)` can release
    the temporary Client mid-request; its __del__ closes the underlying httpx
    pool, and the in-flight tenacity retry then raises "Cannot send a request,
    as the client has been closed."
    """
    global _CLIENT
    if _CLIENT is None:
        from google import genai
        _CLIENT = genai.Client()
    return _CLIENT
