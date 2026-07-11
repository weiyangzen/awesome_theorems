#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0087-PROOF."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text()
receipt = json.loads((HERE / "proof-receipt.json").read_text())

for token in ("sorry", "admit", "axiom ", "sorryAx", "unsafe"):
    assert token not in proof
for required in (
    "import Statement",
    "import ObligationTree",
    "theorem fullPackage : ObligationTree.FullPackage C",
    "theorem faithfulPackage : ObligationTree.FaithfulPackage C",
    "theorem adjunctionPackage : ObligationTree.AdjunctionPackage C",
    "theorem finiteLimitsPackage : ObligationTree.FiniteLimitsPackage C",
    "theorem gabrielPopescu_via_frozen_composition : Statement C",
    "ObligationTree.root_of_packages C",
    "theorem gabrielPopescu : Statement C",
    "#print axioms IsGrothendieckAbelian.GabrielPopescuAux.kernel_ι_d_comp_d",
    "#print axioms IsGrothendieckAbelian.GabrielPopescu.preservesInjectiveObjects",
):
    assert required in proof

assert receipt["item_id"] == "S56-M-0087-PROOF"
assert receipt["theorem_id"] == "THM-M-0087"
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["result"]["root_closed"] is True
assert receipt["result"]["theorem_complete"] is False
assert receipt["proof_body"]["source_sha256"] == hashlib.sha256(
    proof_path.read_bytes()
).hexdigest()
for key, filename in (
    ("statement_sha256", "Statement.lean"),
    ("obligation_tree_sha256", "ObligationTree.lean"),
    ("obligation_registry_sha256", "obligation-registry.json"),
):
    assert receipt["inputs"][key] == hashlib.sha256((HERE / filename).read_bytes()).hexdigest()

print("PASS THM-M-0087 proof phase: exact Gabriel-Popescu root pinned and checked")
