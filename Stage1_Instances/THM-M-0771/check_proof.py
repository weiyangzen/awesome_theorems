#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0771-PROOF."""

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text()

required = (
    "import ObligationTree",
    "import Mathlib.SetTheory.Cardinal.Order",
    "theorem wellOrderConstruction_proof",
    "ObligationTree.RelationWitness alpha",
    "exact IsWellOrder.subtype_nonempty",
    "theorem wellOrderingTheorem_proof : WellOrderingTarget.{u}",
    "ObligationTree.root_of_relationWitness wellOrderConstruction_proof",
    "#print axioms wellOrderConstruction_proof",
    "#print axioms wellOrderingTheorem_proof",
)
for fragment in required:
    assert fragment in proof, f"missing proof fragment: {fragment}"

for forbidden in ("sorry", "admit", "sorryAx"):
    assert forbidden not in proof, f"forbidden proof token: {forbidden!r}"
assert not re.search(r"^\s*(axiom|unsafe)\b", proof, re.MULTILINE), (
    "added axiom or unsafe declaration"
)

receipt = json.loads((HERE / "proof-receipt.json").read_text())
assert receipt["item_id"] == "S56-M-0771-PROOF"
assert receipt["theorem_id"] == "THM-M-0771"
assert receipt["proof_body"]["source_sha256"] == hashlib.sha256(proof_path.read_bytes()).hexdigest()
assert receipt["inputs"]["statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert receipt["inputs"]["obligation_tree_sha256"] == hashlib.sha256((HERE / "ObligationTree.lean").read_bytes()).hexdigest()
assert receipt["inputs"]["obligation_registry_sha256"] == hashlib.sha256((HERE / "obligation-registry.json").read_bytes()).hexdigest()
assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
assert receipt["result"]["root_machine_proof_body_present"] is True
assert receipt["result"]["theorem_complete"] is False

print(
    "PASS THM-M-0771 proof phase: exact WellOrderingTarget closed by the "
    "pinned IsWellOrder.subtype_nonempty construction"
)
