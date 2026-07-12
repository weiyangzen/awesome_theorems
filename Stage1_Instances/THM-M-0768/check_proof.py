#!/usr/bin/env python3
"""Fail-closed source checks for S56-M-0768-PROOF."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text()
registry = json.loads((HERE / "obligation-registry.json").read_text())
receipt = json.loads((HERE / "proof-receipt.json").read_text())

assert registry["theorem_id"] == "THM-M-0768"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256(
    (HERE / "Statement.lean").read_bytes()
).hexdigest()
for token in ("sorry", "admit", "axiom ", "sorryAx", "unsafe "):
    assert token not in proof
for required in (
    "import ObligationTree",
    "theorem relationalPackage_proof : RelationalPackage.{u, v}",
    "Function.Embedding.schroeder_bernstein_of_rel",
    "theorem cantorBernsteinSchroeder_proof : CantorBernsteinSchroederTarget.{u, v}",
    "root_of_relational_package relationalPackage_proof",
    "#print axioms cantorBernsteinSchroeder_proof",
):
    assert required in proof
assert receipt["item_id"] == "S56-M-0768-PROOF"
assert receipt["proof_body"]["source_sha256"] == hashlib.sha256(proof_path.read_bytes()).hexdigest()
assert receipt["inputs"]["obligation_registry_sha256"] == hashlib.sha256(
    (HERE / "obligation-registry.json").read_bytes()
).hexdigest()
assert receipt["inputs"]["registry_denominator_sha256"] == registry["denominator_sha256"]
assert receipt["result"]["root_closed"] is True
assert receipt["result"]["theorem_complete"] is False

print("PASS THM-M-0768 proof: pinned relational body closes the exact frozen root")
