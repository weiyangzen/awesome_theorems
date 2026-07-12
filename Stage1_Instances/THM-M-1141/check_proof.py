#!/usr/bin/env python3
"""Fail-closed source/evidence checks for S56-M-1141-PROOF."""

from pathlib import Path

HERE = Path(__file__).resolve().parent
proof = (HERE / "Proof.lean").read_text()
validation = (HERE / "proof-validation.md").read_text()

for token in ("sorry", "admit", "axiom ", "sorryAx", "unsafe"):
    assert token not in proof
for declaration in (
    "theorem positive_denominators_on_compact",
    "inductive ComparisonChain",
    "theorem SymmetricComparison.trans",
    "theorem ComparisonChain.endpoint",
    "theorem harnackInequality_of_analytic_package",
    "#print axioms positive_denominators_on_compact",
    "#print axioms ComparisonChain.endpoint",
):
    assert declaration in proof
assert "UniformValueComparison" in proof
assert "does not prove" in validation
assert "M1141-L-LOCAL" in validation
print(
    "PASS THM-M-1141 proof phase: positivity and finite-chain propagation "
    "packages closed; analytic uniform comparison remains open"
)
