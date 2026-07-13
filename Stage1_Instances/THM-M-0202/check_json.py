#!/usr/bin/env python3
"""Strictly parse THM-M-0202 JSON artifacts and the optional worker packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", action="store_true")
    args = parser.parse_args()

    paths = sorted(HERE.glob("*.json"))
    if args.worker_packet:
        paths.append(ROOT / ".stage1-worker-selftest.json")
    for path in paths:
        value = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys
        )
        if not isinstance(value, dict):
            raise TypeError(f"{path} must contain a JSON object")
    print(f"strict json: ok ({len(paths)} files)")


if __name__ == "__main__":
    main()
