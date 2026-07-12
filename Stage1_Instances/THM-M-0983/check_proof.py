#!/usr/bin/env python3
"""Fail-closed source checks for S56-M-0983-PROOF."""

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text()

for token in ("sorry", "admit", "axiom ", "sorryAx", "unsafe"):
    assert token not in proof
for declaration in (
    "theorem pairwiseProjection_proof",
    "theorem strongLaw_proof",
    "theorem expectationTransport_proof",
    "theorem obligationTarget_proof",
    "theorem bernoulliStrongLaw_proof",
):
    assert declaration in proof
assert "BernoulliStrongLawTarget.{u}" in proof
assert "ProbabilityTheory.strong_law_ae_real" in proof
assert "root_of_packages" in proof
assert proof.count("#print axioms") == 5

print("PASS THM-M-0983 proof source: three packages and exact root body present")
print(f"proof sha256: {hashlib.sha256(proof_path.read_bytes()).hexdigest()}")
