#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0415-PROOF."""

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
    "theorem idealClassGroupFinite",
    "theorem idealClassGroupFinite_via_frozen_composition",
    "NumberField.RingOfIntegers.instFintypeClassGroup K",
    "#print axioms idealClassGroupFinite",
    "#print axioms ClassGroup.fintypeOfAdmissibleOfAlgebraic",
    "#print axioms ClassGroup.mkMMem_surjective",
):
    assert declaration in proof

assert receipt["item_id"] == "S56-M-0415-PROOF"
assert receipt["theorem_id"] == "THM-M-0415"
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["result"]["root_closed"] is True
assert receipt["result"]["theorem_complete"] is False
assert receipt["proof_body"]["source_sha256"] == hashlib.sha256(
    proof_path.read_bytes()
).hexdigest()
assert receipt["inputs"]["statement_sha256"] == hashlib.sha256(
    (HERE / "Statement.lean").read_bytes()
).hexdigest()
assert receipt["inputs"]["obligation_registry_sha256"] == hashlib.sha256(
    (HERE / "obligation-registry.json").read_bytes()
).hexdigest()

print("PASS THM-M-0415 proof phase: exact root wrapper pinned and checked")
