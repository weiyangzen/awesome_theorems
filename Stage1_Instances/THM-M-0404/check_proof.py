#!/usr/bin/env python3
"""Fail-closed source/evidence checks for S56-M-0404-PROOF."""

from pathlib import Path

HERE = Path(__file__).resolve().parent
proof = (HERE / "Proof.lean").read_text()
validation = (HERE / "proof-validation.md").read_text()

for token in ("sorry", "admit", "axiom ", "sorryAx", "unsafe"):
    assert token not in proof
for declaration in (
    "theorem eventualPeriodic_to_finiteUnion",
    "theorem eventualPeriodicToFiniteUnion_proof",
    "theorem root_of_eventuallyPeriodicZeroSets",
    "#print axioms eventualPeriodic_to_finiteUnion",
    "#print axioms root_of_eventuallyPeriodicZeroSets",
):
    assert declaration in proof
assert "EventuallyPeriodicZeroSets.{u}" in proof
assert "It does not assert" in validation
assert "M0404-T-EVENTUAL" in validation
print(
    "PASS THM-M-0404 proof phase: local combinatorial package closed; "
    "root remains conditional"
)
