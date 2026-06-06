#!/usr/bin/env python3
"""kidma-media setup: detect and (where possible) fix prerequisites.

Checks:
  1. Python 3.9+
  2. google-genai installed
  3. Pillow installed
  4. PyYAML installed
  5. GEMINI_API_KEY (or GOOGLE_API_KEY) in env
  6. gemini-api-docs MCP server registered
  7. Output dir resolvable and writable
  8. API ping (1-token text call)

Usage:
    python setup_check.py                # report status, install missing pip deps
    python setup_check.py --no-install   # report only, never call pip
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

OK = "✓"
FAIL = "✗"
WARN = "•"

# Add parent dir to path so we can import _shared even when called standalone
sys.path.insert(0, str(Path(__file__).resolve().parent))


def _print(symbol: str, msg: str) -> None:
    print(f"  {symbol} {msg}", flush=True)


def check_python() -> bool:
    if sys.version_info >= (3, 9):
        _print(OK, f"Python {sys.version_info.major}.{sys.version_info.minor} OK")
        return True
    _print(FAIL, f"Python 3.9+ required, found {sys.version_info.major}.{sys.version_info.minor}")
    _print(WARN, "Install via Homebrew: `brew install python@3.12`")
    return False


def check_pip_pkg(name: str, import_name: str, *, install: bool) -> bool:
    try:
        importlib.import_module(import_name)
        _print(OK, f"{name} installed")
        return True
    except ImportError:
        if not install:
            _print(FAIL, f"{name} missing")
            return False
        _print(WARN, f"{name} missing — installing via pip…")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--user", "--quiet", name]
            )
        except subprocess.CalledProcessError as e:
            _print(FAIL, f"pip install {name} failed (exit {e.returncode})")
            return False
        try:
            importlib.import_module(import_name)
            _print(OK, f"{name} installed")
            return True
        except ImportError:
            _print(FAIL, f"{name} still not importable after install")
            return False


def check_api_key() -> bool:
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if key:
        _print(OK, f"GEMINI_API_KEY set ({len(key)} chars, not echoed)")
        return True
    _print(FAIL, "GEMINI_API_KEY not set")
    _print(WARN, "  1. Generate a key at https://aistudio.google.com/apikey")
    _print(WARN, "  2. Add `export GEMINI_API_KEY=<your-key>` to ~/.zshrc or ~/.bashrc")
    _print(WARN, "  3. Open a new terminal and run setup again")
    return False


def check_mcp_server() -> bool:
    claude_bin = shutil.which("claude")
    if not claude_bin:
        _print(WARN, "`claude` CLI not on PATH — skipping MCP server check")
        return True
    try:
        out = subprocess.check_output([claude_bin, "mcp", "list"], text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        _print(WARN, f"`claude mcp list` failed: {e.output.strip()}")
        return True
    if "gemini-api-docs" in out:
        _print(OK, "gemini-api-docs MCP server registered")
        return True
    _print(WARN, "gemini-api-docs MCP not registered — adding…")
    try:
        subprocess.check_call(
            [claude_bin, "mcp", "add", "--transport", "http", "--scope", "user",
             "gemini-api-docs", "https://gemini-api-docs-mcp.dev"]
        )
        _print(OK, "gemini-api-docs MCP server added")
        return True
    except subprocess.CalledProcessError as e:
        _print(FAIL, f"Failed to add MCP server (exit {e.returncode})")
        return False


def check_output_dir() -> bool:
    try:
        from _shared import get_output_dir, load_user_config, save_user_config
    except ImportError as e:
        _print(FAIL, f"Cannot import _shared: {e}")
        return False
    path = get_output_dir()
    test = path / ".kidma-media-write-test"
    try:
        test.write_text("ok")
        test.unlink()
    except OSError as e:
        _print(FAIL, f"Output dir {path} not writable: {e}")
        return False
    cfg = load_user_config()
    if "output_dir" not in cfg:
        cfg["output_dir"] = str(path)
        save_user_config(cfg)
    _print(OK, f"Output dir: {path}")
    return True


def check_default_voice() -> bool:
    """Ensure a default TTS voice is set in user config."""
    try:
        from _shared import load_models, load_user_config, save_user_config
    except ImportError:
        return True
    cfg = load_user_config()
    if cfg.get("tts_voice"):
        _print(OK, f"Default TTS voice: {cfg['tts_voice']}")
        return True
    models = load_models()
    default = models.get("defaults", {}).get("tts_voice") or "Achernar"
    cfg["tts_voice"] = default
    save_user_config(cfg)
    _print(OK, f"Default TTS voice set: {default}")
    return True


def api_ping() -> bool:
    try:
        from google import genai
    except ImportError:
        _print(FAIL, "google-genai not importable — skipping API ping")
        return False
    try:
        c = genai.Client()
        resp = c.models.generate_content(
            model="gemini-3.5-flash",
            contents="Reply with exactly: OK",
        )
        text = (resp.text or "").strip()
        if "OK" in text.upper():
            _print(OK, "API ping succeeded")
            return True
        _print(WARN, f"API responded but content unexpected: {text!r}")
        return True  # treat as soft success
    except Exception as e:
        _print(FAIL, f"API ping failed: {e}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="kidma-media setup")
    parser.add_argument("--no-install", action="store_true", help="never call pip")
    args = parser.parse_args()
    install = not args.no_install

    print("kidma-media setup")
    print("─────────────────")

    results: list[bool] = []
    results.append(check_python())
    results.append(check_pip_pkg("google-genai", "google.genai", install=install))
    results.append(check_pip_pkg("Pillow", "PIL", install=install))
    results.append(check_pip_pkg("PyYAML", "yaml", install=install))
    key_ok = check_api_key()
    results.append(key_ok)
    results.append(check_mcp_server())
    results.append(check_output_dir())
    results.append(check_default_voice())
    if key_ok and all(r for r in results[:4]):
        results.append(api_ping())

    print("─────────────────")
    if all(results):
        print(f"{OK} All checks passed. You're ready to use kidma-media.")
        return 0
    print(f"{FAIL} Some checks failed — see notes above.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
