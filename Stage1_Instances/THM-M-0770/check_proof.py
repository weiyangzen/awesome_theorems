#!/usr/bin/env python3
"""Fail-closed source checks for S56-M-0770-PROOF."""

from pathlib import Path

here = Path(__file__).resolve().parent
proof = (here / "Proof.lean").read_text()

for token in ("sorry", "admit", "axiom ", "sorryAx", "unsafe"):
    assert token not in proof
for required in (
    "import Statement",
    "theorem zornsLemma : ZornsLemmaTarget.{u}",
    "exact zorn_le_nonempty chains_bounded",
    "#print axioms zornsLemma",
):
    assert required in proof

print("PASS THM-M-0770 proof phase: exact frozen target has a placeholder-free proof body")
