#!/usr/bin/env python3
"""Fail-closed source checks for S56-M-0002-PROOF."""

import hashlib
import json
from pathlib import Path

here = Path(__file__).resolve().parent
proof_path = here / "Proof.lean"
proof = proof_path.read_text()
receipt = json.loads((here / "proof-receipt.json").read_text())

for token in ("sorry", "admit", "axiom ", "sorryAx", "unsafe"):
    assert token not in proof
for required in (
    "import Statement",
    "theorem fiveLemma : FiveLemmaTarget (C := C)",
    "CategoryTheory.Abelian.mono_of_epi_of_mono_of_mono",
    "δlastFunctor.map phi",
    "exact_iff_δlast",
    "CategoryTheory.Abelian.epi_of_epi_of_epi_of_mono",
    "δ₀Functor.map phi",
    "exact_iff_δ₀",
    "CategoryTheory.isIso_of_mono_of_epi",
    "#print axioms fiveLemma",
):
    assert required in proof

assert receipt["item_id"] == "S56-M-0002-PROOF"
assert receipt["theorem_id"] == "THM-M-0002"
assert receipt["proof_body"]["source_sha256"] == hashlib.sha256(proof_path.read_bytes()).hexdigest()
assert receipt["result"]["root_closed"] is True
assert receipt["result"]["theorem_complete"] is False

print("PASS THM-M-0002 proof phase: exact frozen target has a placeholder-free proof body")
