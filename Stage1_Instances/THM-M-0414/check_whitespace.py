#!/usr/bin/env python3
"""Whitespace check that includes the validation node's untracked artifacts."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATHS = [
    ROOT / ".stage1-worker-selftest.json",
    ROOT / "Stage1_Instances/THM-M-0414/Validation.lean",
    ROOT / "Stage1_Instances/THM-M-0414/check_whitespace.py",
    ROOT / "Stage1_Instances/THM-M-0414/check_validation.py",
    ROOT / "Stage1_Instances/THM-M-0414/validation-phase.md",
    ROOT / "Stage1_Instances/THM-M-0414/validation-receipt.json",
    ROOT / "Stage1_Instances/THM-M-0414/validation-spec.json",
]

for path in PATHS:
    data = path.read_bytes()
    if not data.endswith(b"\n"):
        raise SystemExit(f"missing final newline: {path.relative_to(ROOT)}")
    for number, line in enumerate(data.splitlines(), start=1):
        if line != line.rstrip(b" \t"):
            raise SystemExit(
                f"trailing whitespace: {path.relative_to(ROOT)}:{number}"
            )

print("PASS THM-M-0414 changed-artifact whitespace and final-newline checks")
