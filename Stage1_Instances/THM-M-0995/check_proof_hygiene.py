#!/usr/bin/env python3
"""Reject placeholders, declarations that extend trust, and stale generated oleans."""

import re
from pathlib import Path

here = Path(__file__).resolve().parent
patterns = {
    "proof placeholder": re.compile(r"\b(sorry|admit)\b"),
    "axiom declaration": re.compile(r"(?m)^\s*axiom\b"),
    "unsafe declaration": re.compile(r"(?m)^\s*unsafe\b"),
}

for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
    text = (here / name).read_text()
    for label, pattern in patterns.items():
        assert not pattern.search(text), f"{label} in {name}"

assert not list(here.glob("*.olean")), "generated olean left in the owned path"
assert not list(here.glob("tmp*.lean")), "temporary Lean source left in the owned path"
print("PASS THM-M-0995 proof hygiene: no placeholders, trust extensions, or generated files")
