#!/usr/bin/env python3
"""Fail-closed source checks for the THM-M-1515 proof phase."""

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof = (HERE / "Proof.lean").read_text()

assert hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest() == \
    "60b548f2032771a84c7da069e9343a74544294380dec21d041f492c880989add"
assert hashlib.sha256((HERE / "ObligationTree.lean").read_bytes()).hexdigest() == \
    "46fe18ed3c9a8f7f490ac2898fa891dd2344991ad22996c721facc61893c4f27"
assert all(token not in proof for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "boundary_along_curve_derivative" in proof
assert "momentum_pairing_derivative" in proof
assert "theorem noether_first_theorem : NoetherFirstTheoremTarget.{u}" in proof
assert "root_of_derivative_packages" in proof
assert proof.count("#print axioms") == 3

print("PASS THM-M-1515 proof source: two analytic packages and exact root body present")
print(f"proof sha256: {hashlib.sha256((HERE / 'Proof.lean').read_bytes()).hexdigest()}")
