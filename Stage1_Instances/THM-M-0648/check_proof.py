#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0648 proof phase."""

from pathlib import Path
import re

root = Path(__file__).resolve().parent
proof = (root / "Proof.lean").read_text()
statement = (root / "Statement.lean").read_text()

for name in ("DownwardTarget", "UpwardTarget", "CanonicalTarget"):
    marker = f"def {name}"
    assert proof.count(marker) == 1, f"missing or duplicate {marker} in Proof.lean"
    assert statement.count(marker) == 1, f"missing or duplicate {marker} in Statement.lean"

for anchor in (
    "L.exists_elementarySubstructure_card_eq",
    "L.exists_elementaryEmbedding_card_eq_of_ge",
    "theorem canonicalTarget",
    "#print axioms canonicalTarget",
):
    assert anchor in proof, f"missing proof anchor: {anchor}"

for pattern in (r"\bsorry\b", r"\badmit\b", r"\bsorryAx\b", r"^\s*axiom\b",
                r"\bunsafe\b", r"implemented_by"):
    assert re.search(pattern, proof, re.MULTILINE) is None, f"forbidden boundary: {pattern}"

print("PASS THM-M-0648 proof: exact paired root uses both pinned mathlib bodies")
