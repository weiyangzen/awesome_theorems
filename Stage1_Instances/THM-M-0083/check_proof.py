#!/usr/bin/env python3
"""Fail-closed source checks for S56-M-0083-PROOF."""

from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
proof = (HERE / "Proof.lean").read_text()

required = (
    "import Statement",
    "theorem representedBy_of_universalElement",
    "theorem universalElement_of_representedBy",
    "theorem forward",
    "theorem reverse",
    "theorem representableFunctorTarget",
    "RepresentableFunctorTarget F",
    "IsRepresentable.iff_exists_isRepresentedBy",
    "isRepresentedBy_iff",
    "hx.map_bijective",
    "exact ⟨forward F, reverse F⟩",
    "#print axioms representableFunctorTarget",
)
for marker in required:
    assert marker in proof, marker

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE
)
assert prohibited.search(proof) is None

print("PASS THM-M-0083 proof source: two exact directions and root composition present")
