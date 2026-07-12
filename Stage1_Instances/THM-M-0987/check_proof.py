#!/usr/bin/env python3
"""Fail-closed source checks for S56-M-0987-PROOF."""

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text()

for token in ("sorry", "admit", "axiom ", "sorryAx", "unsafe"):
    assert token not in proof
for declaration in (
    "theorem centralLimitTheorem_proof",
    "theorem pinnedBridge_proof",
    "theorem canonicalRoot_proof",
):
    assert declaration in proof
assert "CentralLimitTheoremTarget.{uOmega, uOmega'}" in proof
assert "PinnedBridge.{uOmega, uOmega'}" in proof
assert proof.count("ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub") == 2
assert "root_of_pinnedBridge pinnedBridge_proof" in proof
assert proof.count("#print axioms") == 3

print("PASS THM-M-0987 proof source: exact root and pinned bridge bodies present")
print(f"proof sha256: {hashlib.sha256(proof_path.read_bytes()).hexdigest()}")
