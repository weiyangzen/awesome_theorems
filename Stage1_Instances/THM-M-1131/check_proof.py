#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1131 proof phase."""

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
source = (HERE / "Proof.lean").read_text()

for declaration in (
    "theorem fderiv_const_mul_apply",
    "theorem divergence_const_mul",
    "theorem fluxDivergencePackage",
    "theorem fourierHeatConductionLaw",
):
    assert declaration in source, f"missing declaration: {declaration}"

assert "fourierHeatConductionLaw : Statement" in source
assert "statement_of_fluxDivergencePackage fluxDivergencePackage" in source
assert not re.search(r"\b(sorry|admit)\b|\baxiom\s+", source), "forbidden proof gap"

print("check_proof: ok (4 proof declarations, exact Statement root, no proof gaps)")
