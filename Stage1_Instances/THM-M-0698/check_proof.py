#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0698-PROOF."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text()
receipt = json.loads((HERE / "proof-receipt.json").read_text())

for token in ("sorry", "admit", "axiom ", "sorryAx", "unsafe"):
    assert token not in proof
for declaration in (
    "theorem finiteToSatisfiable_pinned",
    "theorem firstOrderCompactness_via_frozen_composition",
    "theorem firstOrderCompactness_pinned",
    "FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable",
    "#print axioms finiteToSatisfiable_pinned",
    "#print axioms firstOrderCompactness_pinned",
):
    assert declaration in proof

assert receipt["item_id"] == "S56-M-0698-PROOF"
assert receipt["theorem_id"] == "THM-M-0698"
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["result"]["root_closed"] is True
assert receipt["result"]["theorem_complete"] is False
assert receipt["result"]["remaining_machine_cut_set"] == []
assert receipt["proof_body"]["source_sha256"] == hashlib.sha256(
    proof_path.read_bytes()
).hexdigest()
assert receipt["inputs"]["statement_sha256"] == hashlib.sha256(
    (HERE / "Statement.lean").read_bytes()
).hexdigest()
assert receipt["inputs"]["obligation_registry_sha256"] == hashlib.sha256(
    (HERE / "obligation-registry.json").read_bytes()
).hexdigest()

print("PASS THM-M-0698 proof phase: exact pinned compactness root closed")
