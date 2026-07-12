#!/usr/bin/env python3
"""Fail-closed source checks for the THM-M-1550 proof phase."""

import hashlib
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
statement_path = HERE / "Statement.lean"
proof_path = HERE / "Proof.lean"
statement = statement_path.read_text()
proof = proof_path.read_text()

for source in (statement, proof):
    assert not re.search(r"\b(sorry|admit|sorryAx)\b|^\s*(axiom|unsafe)\b",
                         source, re.MULTILINE)

assert "theorem laxPairIsospectrality : LaxPairIsospectrality.{u}" in statement
assert "theorem spectrumUnderConjugation" in statement
assert "spectrum.units_conjugate" in statement
assert "Matrix.GeneralLinearGroup.coe_inv" in statement
assert "theorem laxPairIsospectrality : LaxPairIsospectrality.{u}" in proof
assert proof.count("#print axioms") == 3

print("PASS THM-M-1550 proof source: exact frozen root and spectrum leaf are implemented")
print(f"statement sha256: {hashlib.sha256(statement_path.read_bytes()).hexdigest()}")
print(f"proof sha256: {hashlib.sha256(proof_path.read_bytes()).hexdigest()}")
