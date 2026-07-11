#!/usr/bin/env python3
"""Fail-closed source checks for S56-M-0001-PROOF."""

from pathlib import Path

here = Path(__file__).resolve().parent
proof = (here / "Proof.lean").read_text()

for token in ("sorry", "admit", "axiom ", "sorryAx", "unsafe"):
    assert token not in proof
for required in (
    "import Statement",
    "theorem longExactHomologySequence",
    "LongExactHomologySequenceTarget.{v, u, w}",
    "hS.homology_exact₂ i",
    "hS.homology_exact₃ i j hij",
    "hS.homology_exact₁ i j hij",
    "#print axioms longExactHomologySequence",
):
    assert required in proof

print("PASS THM-M-0001 proof phase: exact frozen target has a placeholder-free proof body")
