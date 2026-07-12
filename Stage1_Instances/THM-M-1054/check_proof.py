#!/usr/bin/env python3
"""Fail-closed source checks for the THM-M-1054 proof phase."""

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text()

assert hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest() == \
    "553a0ea00cbad0c7168787901522ad316734450e72886371621dab26a5a4888a"
assert hashlib.sha256((HERE / "ObligationTree.lean").read_bytes()).hexdigest() == \
    "d9a61d256b1c574189b64e2b7a125b2eb78a55d1647b3da2d2b4849460010f02"

required = (
    "theorem nontrivialMeanErgodicPackage_proof :",
    "NontrivialMeanErgodicPackage.{u}",
    "ContinuousLinearMap.tendsto_birkhoffAverage_orthogonalProjection",
    "(Koopman T hT) contraction f",
    "theorem vonNeumannL2MeanErgodic :",
    "VonNeumannL2MeanErgodicTarget.{u}",
    "root_of_nontrivialMeanErgodicPackage nontrivialMeanErgodicPackage_proof",
)
assert all(fragment in proof for fragment in required), "missing exact proof integration fragment"
for forbidden in ("sorry", "admit", "axiom ", "sorryAx", "unsafe", "native_decide", "external "):
    assert forbidden not in proof, f"forbidden proof mechanism: {forbidden.strip()}"
assert proof.count("#print axioms") == 2

print("PASS THM-M-1054 proof: pinned mean-ergodic body and exact root integrated")
print(f"proof sha256: {hashlib.sha256(proof_path.read_bytes()).hexdigest()}")
print("machine root cut set after proof integration: empty; downstream gates remain")
