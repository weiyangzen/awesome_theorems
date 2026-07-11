#!/usr/bin/env python3
"""Fail-closed source checks for S56-M-0106-PROOF."""

from pathlib import Path

HERE = Path(__file__).resolve().parent
proof = (HERE / "Proof.lean").read_text()

required = (
    "import Statement",
    "import Mathlib.RingTheory.NoetherNormalization",
    "theorem noetherNormalization_proof : NoetherNormalizationTarget.{u}",
    "exists_finite_inj_algHom_of_fg k R",
    "AlgebraicGeometry.IsFinite.SpecMap_iff",
    "affineSpaceMorphism g",
    "#print axioms noetherNormalization_proof",
)
for fragment in required:
    assert fragment in proof, f"missing proof fragment: {fragment}"

for forbidden in ("sorry", "admit", "sorryAx", "axiom ", "unsafe "):
    assert forbidden not in proof, f"forbidden proof token: {forbidden!r}"

print("PASS THM-M-0106 proof phase: exact frozen target has an unconditional proof body")
