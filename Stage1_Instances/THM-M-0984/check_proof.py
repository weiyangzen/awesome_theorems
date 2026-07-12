#!/usr/bin/env python3
"""Fail-closed source checks for the THM-M-0984 proof phase."""

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text()

assert hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest() == \
    "29fd61ee29db46ea9871743ee6f3d2eb3e0b765ae759d908df9dc4a7a5358cfe"
assert hashlib.sha256((HERE / "ObligationTree.lean").read_bytes()).hexdigest() == \
    "2182acb84c0651c5fd14b51ca1dec3cbddb39e55da2c0c8922a33d39cc7e8d64"
assert all(token not in proof for token in
           ("sorry", "admit", "axiom ", "sorryAx", "unsafe"))
assert "theorem terminalStrongLaw : ObligationTree.TerminalStrongLaw.{u, v}" in proof
assert "ProbabilityTheory.strong_law_ae X" in proof
assert "theorem strongLawRoot : ObligationTree.Root.{u, v}" in proof
assert "ObligationTree.root_of_terminal terminalStrongLaw" in proof
assert proof.count("#print axioms") == 2

print("PASS THM-M-0984 proof source: exact terminal and frozen-root composition bodies present")
print(f"proof sha256: {hashlib.sha256(proof_path.read_bytes()).hexdigest()}")
