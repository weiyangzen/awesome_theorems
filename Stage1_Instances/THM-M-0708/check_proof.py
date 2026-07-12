#!/usr/bin/env python3
"""Check the source-level contract of the THM-M-0708 proof receipt."""

from pathlib import Path
import re

root = Path(__file__).resolve().parent
proof = (root / "Proof.lean").read_text(encoding="utf-8")

required = [
    "theorem riceBridge : RiceBridge",
    "ComputablePred.rice C hdec hf hg hfC",
    "theorem riceTheorem : RiceTheoremTarget",
    "root_of_riceBridge riceBridge",
    "theorem riceTheorem_direct : RiceTheoremTarget",
]
for fragment in required:
    assert fragment in proof, f"missing required proof fragment: {fragment}"

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE
)
assert prohibited.search(proof) is None, "prohibited proof token found"

print("PASS THM-M-0708 proof source contract and placeholder scan")
