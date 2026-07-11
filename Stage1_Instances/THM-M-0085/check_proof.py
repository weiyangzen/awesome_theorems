#!/usr/bin/env python3
"""Fail-closed source checks for S56-M-0085-PROOF."""

from pathlib import Path

HERE = Path(__file__).resolve().parent
proof = (HERE / "Proof.lean").read_text()
validation = (HERE / "proof-validation.md").read_text()

for token in ("sorry", "admit", "axiom ", "sorryAx", "unsafe"):
    assert token not in proof, f"forbidden proof token: {token!r}"

for fragment in (
    "import Statement",
    "theorem beckMonadicity : Statement",
    "letI : CategoryTheory.Monad.CreatesColimitOfIsSplitPair G := creates",
    "CategoryTheory.Monad.monadicOfCreatesGSplitCoequalizers adj",
    ").eqv",
    "#print axioms beckMonadicity",
):
    assert fragment in proof, f"missing proof fragment: {fragment}"

assert "S56-M-0085-PROOF" in validation
assert "theorem completion is not claimed" in validation

print("PASS THM-M-0085 proof phase: exact frozen target has a placeholder-free proof body")
