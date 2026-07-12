#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1129 proof phase."""

from pathlib import Path
import re

root = Path(__file__).resolve().parent
source = (root / "Proof.lean").read_text()

required = {
    "poissonDiskTerm_zero_time",
    "poissonDiskTerm_zero_data",
    "deriv_poissonDiskTerm_zero_data",
    "poissonExpression_zero_data",
}
declared = set(re.findall(r"^theorem\s+([A-Za-z0-9_]+)", source, re.MULTILINE))
assert required <= declared, f"missing proof declarations: {sorted(required - declared)}"
assert "import Statement" in source
assert not re.search(r"\b(sorry|admit)\b|^\s*(axiom|unsafe)\b", source, re.MULTILINE)
assert "PoissonFormulaTarget := by" not in source, "proof phase must not claim the open root"

print("PASS THM-M-1129 proof phase: four local boundary bodies; analytic root remains open")
