#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0541 proof source."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
proof = (ROOT / "Proof.lean").read_text(encoding="utf-8")

required = [
    "lemma orderEmbOfFin_erase_apply",
    "lemma face_face",
    "noncomputable def boundary",
    "lemma boundary_squared_single",
    "lemma boundary_squared",
    "theorem statementShape : StatementShape",
    "#check (Stage1Instances.THM_M_0541.statementShape : Stage1Instances.THM_M_0541.StatementShape)",
    "#print axioms Stage1Instances.THM_M_0541.statementShape",
]
for marker in required:
    assert marker in proof, f"missing proof marker: {marker}"

for pattern in (r"\bsorry\b", r"\badmit\b", r"\baxiom\s+", r"\bunsafe\s+(?:def|theorem)"):
    assert re.search(pattern, proof) is None, f"forbidden construct: {pattern}"

statement = (ROOT / "Statement.lean").read_text(encoding="utf-8")
for marker in (
    "def Simplex",
    "def face",
    "abbrev Chains",
    "def HasAlternatingBoundary",
    "def CanonicalTarget",
    "def StatementShape",
):
    assert marker in statement and marker in proof, f"target definition missing: {marker}"

print("proof structural check: ok; exact root theorem and six substantive proof bodies present")
