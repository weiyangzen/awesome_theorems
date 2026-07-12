#!/usr/bin/env python3
"""Narrow proof-phase hygiene and source-boundary check for THM-M-1028."""

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof = (HERE / "Proof.lean").read_text()

forbidden = re.compile(r"\b(sorry|admit|sorryAx)\b|(^|\W)axiom\s", re.MULTILINE)
assert not forbidden.search(proof), "forbidden placeholder or declared axiom in Proof.lean"

required = (
    "isModification_refl",
    "isModification_symm",
    "isModification_trans",
    "merge_path_events",
    "statement_of_path_packages",
    "(continuous : ContinuousModificationPackage.{u})",
    "(nowhereDiff : NowhereDifferentiabilityPackage.{u})",
)
for token in required:
    assert token in proof, f"missing exact proof boundary: {token}"

assert "theorem statement_of_path_packages" in proof
assert "Statement.{u}" in proof
assert proof.count("#print axioms") == 5

print("PASS THM-M-1028 proof source: 5 checked bodies; exact root remains conditional on 2 open packages")
