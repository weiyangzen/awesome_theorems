#!/usr/bin/env python3
"""Fail-closed source/evidence checks for S56-M-0981-PROOF."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof = (HERE / "Proof.lean").read_text()
receipt = json.loads((HERE / "proof-receipt.json").read_text())
validation = (HERE / "proof-validation.md").read_text()

for token in ("sorry", "admit", "axiom ", "sorryAx", "unsafe"):
    assert token not in proof
for declaration in (
    "theorem emptyEventPackage",
    "theorem unitMassPackage",
    "theorem countableAdditivityPackage",
    "theorem canonicalRoot_via_frozen_composition",
    "theorem kolmogorovAxioms",
    "#print axioms kolmogorovAxioms",
):
    assert declaration in proof

assert receipt["item_id"] == "S56-M-0981-PROOF"
assert receipt["theorem_id"] == "THM-M-0981"
assert receipt["result"]["root_closed"] is True
assert receipt["result"]["theorem_complete"] is False
assert "M0981-ROOT" in receipt["closed_obligation_ids"]
assert "Master acceptance" in validation
print("PASS THM-M-0981 proof phase: exact root and frozen composition closed")
