#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0417-PROOF."""

import hashlib
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROOF_PATH = HERE / "Proof.lean"
RECEIPT_PATH = HERE / "proof-receipt.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


proof = PROOF_PATH.read_text(encoding="utf-8")
receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
registry = json.loads((HERE / "obligation-registry.json").read_text(encoding="utf-8"))

required_fragments = (
    "theorem halfBodyVolume : HalfBodyVolume",
    "theorem blichfeldtBridge : BlichfeldtBridge",
    "theorem differenceExtraction : DifferenceExtraction",
    "theorem minkowskiConvexBody :",
    "theorem closesFrozenStatement :",
    "theorem closesViaFrozenComposition : Root",
    "theorem closesFrozenStatementViaComposition :",
    "theorem frozenRootExactType :",
    "MeasureTheory.exists_pair_mem_lattice_not_disjoint_vadd",
    "MeasureTheory.exists_ne_zero_mem_lattice_of_measure_mul_two_pow_lt_measure",
    "root_compose halfBodyVolume blichfeldtBridge differenceExtraction",
    "#print axioms closesFrozenStatementViaComposition",
    "#print axioms frozenRootExactType",
)
assert all(fragment in proof for fragment in required_fragments)

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide)\b|"
    r"^[ \t]*(?:axiom|unsafe|external)[ \t]",
    re.MULTILINE,
)
assert prohibited.search(proof) is None, "placeholder, oracle, or unsafe declaration found"

expected_closed = {
    "M0417-ROOT",
    "M0417-S-CONTEXT",
    "M0417-N-HALF-VOLUME",
    "M0417-L-BLICHFELDT",
    "M0417-C-COLLISION",
    "M0417-T-DIFFERENCE",
    "M0417-T-COMPOSE",
}
registry_ids = {row["obligation_id"] for row in registry["obligations"]}
assert receipt["schema_version"] == "stage1-proof-receipt/1.0"
assert receipt["item_id"] == "S56-M-0417-PROOF"
assert receipt["theorem_id"] == "THM-M-0417"
assert receipt["support_state"] == "provisional_worker_selftest"
assert set(receipt["closed_obligation_ids"]) == expected_closed
assert expected_closed <= registry_ids
assert not {"M0417-X-SOURCE", "M0417-X-TRUST"} & expected_closed
assert receipt["proof_body"]["wrapper_sha256"] == digest(PROOF_PATH)
assert receipt["inputs"]["statement_sha256"] == digest(HERE / "Statement.lean")
assert receipt["inputs"]["obligation_tree_sha256"] == digest(HERE / "ObligationTree.lean")
assert receipt["inputs"]["obligation_registry_sha256"] == digest(
    HERE / "obligation-registry.json"
)
assert receipt["result"]["exit_code"] == 0
assert receipt["result"]["machine_root_closed"] is True
assert receipt["result"]["audit_complete"] is False
assert receipt["result"]["theorem_complete"] is False
assert receipt["result"]["placeholder_scan"] == "pass"

print("PASS THM-M-0417 proof: exact pinned wrapper and frozen composition checked")
print("machine proof cut set: empty; source/trust and downstream release gates remain")
