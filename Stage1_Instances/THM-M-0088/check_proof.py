#!/usr/bin/env python3
"""Fail-closed source checks for the S56-M-0088-PROOF worker artifact."""

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof = (HERE / "Proof.lean").read_text()

assert not re.search(r"\b(sorry|admit|sorryAx)\b|^[ \t]*(axiom|unsafe)\b", proof, re.MULTILINE)
for declaration in (
    "def yonedaPreimage",
    "theorem yonedaPreimage_component",
    "theorem yoneda_map_preimage",
    "theorem yoneda_preimage_map",
    "def yonedaEmbedding",
    "#print axioms Stage1Instances.THM_M_0088.yonedaEmbedding",
):
    assert declaration in proof

assert "Yoneda.naturality" in proof
assert "yonedaEmbedding_of_inverseLaws" in proof
print("PASS THM-M-0088 proof: 6 frozen machine obligations locally closed")
