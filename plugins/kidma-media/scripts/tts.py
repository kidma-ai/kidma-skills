#!/usr/bin/env python3
"""Generate Hebrew (or any-language) speech via Gemini TTS.

Output is a 24 kHz mono 16-bit PCM WAV file.

Usage:
    python tts.py [--text "..." | --text-file PATH | --stdin]
                  [--model ID] [--voice NAME] [--out PATH]
"""

from __future__ import annotations

import argparse
import base64
import sys
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _shared import (  # noqa: E402
    client,
    load_models,
    load_user_config,
    out_path,
    preflight,
)

PCM_SAMPLE_RATE_HZ = 24_000
PCM_SAMPLE_WIDTH_BYTES = 2  # 16-bit
PCM_CHANNELS = 1


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate speech with Gemini TTS")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--text", help="Text to synthesize")
    g.add_argument("--text-file", help="File whose contents to synthesize")
    g.add_argument("--stdin", action="store_true", help="Read text from stdin")
    p.add_argument("--model", help="Override default TTS model")
    p.add_argument("--voice", help="Prebuilt voice name (e.g., Achernar, Algieba, Aoede)")
    p.add_argument("--out", help="Output WAV path. Default: auto-named under output dir.")
    return p.parse_args()


def read_text(args: argparse.Namespace) -> str:
    if args.text:
        return args.text
    if args.text_file:
        return Path(args.text_file).expanduser().read_text(encoding="utf-8")
    return sys.stdin.read()


def write_wav(path: Path, pcm_bytes: bytes) -> None:
    with wave.open(str(path), "wb") as w:
        w.setnchannels(PCM_CHANNELS)
        w.setsampwidth(PCM_SAMPLE_WIDTH_BYTES)
        w.setframerate(PCM_SAMPLE_RATE_HZ)
        w.writeframes(pcm_bytes)


def main() -> int:
    preflight()
    args = parse_args()

    from google.genai import types

    text = read_text(args).strip()
    if not text:
        sys.stderr.write("✗ Empty text — nothing to synthesize.\n")
        return 1

    models = load_models()
    user_cfg = load_user_config()
    model = args.model or models.get("defaults", {}).get("tts", "gemini-3.1-flash-tts-preview")
    voice = (
        args.voice
        or user_cfg.get("tts_voice")
        or models.get("defaults", {}).get("tts_voice")
        or "Achernar"
    )

    speech_cfg = types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice)
        )
    )
    config = types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=speech_cfg,
    )

    sys.stderr.write(f"→ model={model}  voice={voice}  chars={len(text)}\n")
    response = client().models.generate_content(model=model, contents=text, config=config)

    audio_bytes: bytes | None = None
    for cand in response.candidates or []:
        for part in cand.content.parts or []:
            inline = getattr(part, "inline_data", None)
            if inline is not None and inline.data:
                data = inline.data
                if isinstance(data, str):
                    data = base64.b64decode(data)
                audio_bytes = data
                break
        if audio_bytes:
            break

    if not audio_bytes:
        sys.stderr.write("✗ No audio data returned by the model.\n")
        return 1

    target = out_path(text[:40] or "tts", "wav", override=args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    write_wav(target, audio_bytes)

    sys.stderr.write(f"✓ Saved {len(audio_bytes)} bytes of PCM to {target}\n")
    print(target.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
