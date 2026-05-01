"""Command line interface."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import PROJECT, SAMPLE_PACKET, analyze


def _load_packet(packet_path: str | None) -> dict:
    if packet_path and packet_path != "sample":
        return json.loads(Path(packet_path).read_text(encoding="utf-8"))
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw:
            return json.loads(raw)
    return SAMPLE_PACKET


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=PROJECT["tagline"])
    parser.add_argument("packet", nargs="?", default="sample", help="Path to a JSON packet, or 'sample'.")
    args = parser.parse_args(argv)
    print(json.dumps(analyze(_load_packet(args.packet)), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
