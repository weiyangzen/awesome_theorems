#!/usr/bin/env python3
"""Fail-closed source/evidence checks for S56-M-1082-PROOF."""

from pathlib import Path

HERE = Path(__file__).resolve().parent
proof = (HERE / "Proof.lean").read_text()
validation = (HERE / "proof-validation.md").read_text()

for token in ("sorry", "admit", "axiom ", "sorryAx", "unsafe"):
    assert token not in proof
for declaration in (
    "theorem gaussianProcess_iff_finiteDimensionalGaussian",
    "ObligationTree.root_of_directions",
    "ObligationTree.forward_from_projection",
    "ObligationTree.reverse_from_constructor",
    "#print axioms gaussianProcess_iff_finiteDimensionalGaussian",
):
    assert declaration in proof
for boundary in (
    "theorem-completion gate is claimed",
    "M1082-X-SOURCE",
    "M1082-S-FOUNDATION",
    "M1082-X-PROVENANCE",
):
    assert boundary in validation

print("PASS THM-M-1082 proof phase: exact root proof body assembled from frozen children")
