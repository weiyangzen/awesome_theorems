#!/usr/bin/env python3
"""Fail-closed source checks for the THM-M-0644 proof-phase artifact."""

from pathlib import Path
import re

root = Path(__file__).resolve().parent
source = (root / "Proof.lean").read_text()

required = [
    "theorem restrictionDirection",
    "theorem ultraproductDirection",
    "theorem compactnessTarget",
    "FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable.mpr h",
]
for needle in required:
    assert needle in source, f"missing required proof surface: {needle}"

prohibited = re.compile(r"\b(sorry|admit)\b|^[ \t]*(axiom|unsafe)\b", re.MULTILINE)
assert prohibited.search(source) is None, "prohibited proof device found"
assert "forall {L : Language.{u, v}} {T : L.Theory}" in source
assert "T.IsSatisfiable <-> T.IsFinitelySatisfiable" in source

print("PASS THM-M-0644 proof: exact root and both directions present; no prohibited device")
