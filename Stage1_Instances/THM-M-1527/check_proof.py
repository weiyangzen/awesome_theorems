#!/usr/bin/env python3
"""Fail-closed source checks for the THM-M-1527 proof phase."""

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text()

assert hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest() == \
    "9520e44fd993eca1ad6c47d9b9eace32f037c2a20994126e683e159d30c02658"
assert hashlib.sha256((HERE / "ObligationTree.lean").read_bytes()).hexdigest() == \
    "73ea36ecb5ae2f9ff96a58479826053aeafd0c5456a3facabe6506635cc98b36"
assert all(token not in proof for token in
           ("sorry", "admit", "axiom ", "sorryAx", "unsafe"))
assert "theorem maxwell_coordinate_equivalence : MaxwellCoordinateEquivalence.{u}" in proof
assert "assemble_from_component_equivalences" in proof
assert "decomposition.homogeneous_iff" in proof
assert "decomposition.inhomogeneous_iff" in proof
assert proof.count("#print axioms") == 3

print("PASS THM-M-1527 proof source: both premise projections and exact root body present")
print(f"proof sha256: {hashlib.sha256(proof_path.read_bytes()).hexdigest()}")
