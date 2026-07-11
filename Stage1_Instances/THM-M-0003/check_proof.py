#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0003-PROOF."""

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
    "theorem kernelSegment",
    "S.L₀_exact",
    "theorem leftBridgeSegment",
    "S.L₁'_exact",
    "theorem rightBridgeSegment",
    "S.L₂'_exact",
    "theorem cokernelSegment",
    "S.L₃_exact",
    "theorem snakeLemma : SnakeLemmaTarget.{v, u}",
    "exact S.snake_lemma",
    "theorem snakeLemma_via_frozen_composition",
    "ObligationTree.root_compose",
    "#print axioms snakeLemma_via_frozen_composition",
):
    assert required in proof

assert receipt["item_id"] == "S56-M-0003-PROOF"
assert receipt["theorem_id"] == "THM-M-0003"
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["result"]["root_closed"] is True
assert receipt["result"]["theorem_complete"] is False
assert receipt["proof_body"]["source_sha256"] == hashlib.sha256(
    proof_path.read_bytes()
).hexdigest()
for key, name in (
    ("statement_sha256", "Statement.lean"),
    ("obligation_tree_sha256", "ObligationTree.lean"),
    ("obligation_registry_sha256", "obligation-registry.json"),
):
    assert receipt["inputs"][key] == hashlib.sha256((HERE / name).read_bytes()).hexdigest()

print("PASS THM-M-0003 proof phase: exact root and frozen composition are closed")
