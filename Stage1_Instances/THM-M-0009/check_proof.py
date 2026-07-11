#!/usr/bin/env python3
"""Fail-closed source checks for S56-M-0009-PROOF."""

from pathlib import Path

here = Path(__file__).resolve().parent
proof = (here / "Proof.lean").read_text()

for token in ("sorry", "admit", "axiom ", "sorryAx", "unsafe"):
    assert token not in proof
for required in (
    "import Statement",
    "theorem longExactExtSequence",
    "LongExactExtSequenceTarget.{w, v, u}",
    "Abelian.Ext.covariantSequence_exact X hS n₀ n₁ h",
    "Abelian.Ext.contravariantSequence_exact hS Y n₀ n₁ h",
    "#print axioms longExactExtSequence",
):
    assert required in proof

print("PASS THM-M-0009 proof phase: exact frozen target has a placeholder-free wrapper")
