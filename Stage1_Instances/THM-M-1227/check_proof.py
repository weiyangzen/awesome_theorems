#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1227 partial proof packet."""

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


receipt = load("proof-receipt.json")
blocker = load("proof-blocker.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text(encoding="utf-8")

assert receipt["schema_version"] == "stage1-node-receipt/1.0"
assert blocker["schema_version"] == "stage1-proof-blocker/1.0"
assert {receipt["item_id"], blocker["item_id"]} == {"S56-M-1227-PROOF"}
assert {receipt["theorem_id"], blocker["theorem_id"]} == {"THM-M-1227"}
assert receipt["base_revision"] == blocker["base_revision"]

inputs = receipt["inputs"]
for key, name in (
    ("statement_source_sha256", "Statement.lean"),
    ("proof_source_sha256", "Proof.lean"),
    ("obligation_registry_sha256", "obligation-registry.json"),
    ("typed_graphs_sha256", "typed-graphs.json"),
    ("anchor_audit_sha256", "anchor-audit.json"),
):
    assert inputs[key] == hashlib.sha256((HERE / name).read_bytes()).hexdigest()
assert inputs["check_proof_py_sha256"] == hashlib.sha256((HERE / "check_proof.py").read_bytes()).hexdigest()
assert inputs["check_proof_sh_sha256"] == hashlib.sha256((HERE / "check_proof.sh").read_bytes()).hexdigest()

assert inputs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert inputs["registry_denominator_sha256"] == graphs["registry_denominator_sha256"]

fingerprints = {
    row["obligation_id"]: row["statement_fingerprint"]
    for row in registry["obligations"]
}
implemented = ["M1227-B-ZERO"]
cut = [
    "M1227-N-DATA",
    "M1227-N-GLOBAL",
    "M1227-C-GALERKIN",
    "M1227-C-BOUNDS",
    "M1227-C-COMPACT",
]
assert receipt["accepted_closed_obligation_ids"] == []
assert receipt["provisionally_implemented_obligation_ids"] == implemented
assert blocker["provisionally_implemented_obligation_ids"] == implemented
assert receipt["obligation_statement_fingerprints"] == {
    "M1227-B-ZERO": fingerprints["M1227-B-ZERO"]
}
assert blocker["obligation_statement_fingerprints"] == receipt["obligation_statement_fingerprints"]
assert receipt["remaining_root_cut_set"] == blocker["remaining_root_cut_set"] == cut
assert graphs["closure_boundary"]["remaining_root_cut_set"] == cut

assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
assert blocker["outcome"] == "partial_proof_self_tested_root_blocked"
assert blocker["phase_self_tested"] is True
assert receipt["result"]["root_closed"] is False
assert receipt["result"]["audit_complete"] is False
assert receipt["result"]["theorem_complete"] is False
assert blocker["root_closed"] is False
assert blocker["audit_complete"] is False
assert blocker["theorem_complete"] is False
assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
assert receipt["result"]["accepted_root_vector_after"]["M"] == "M4"
assert receipt["result"]["root_vector_after_proposed"]["M"] == "M2"
assert blocker["accepted_root_vector_after"]["M"] == "M4"
assert blocker["root_vector_after_proposed"]["M"] == "M2"

required = (
    "theorem zero_isLerayHopfSolution",
    "theorem lerayHopfExistence_of_eq_zero",
    "#print axioms zero_isLerayHopfSolution",
    "#print axioms lerayHopfExistence_of_eq_zero",
    "#print sorries zero_isLerayHopfSolution",
    "#print sorries lerayHopfExistence_of_eq_zero",
)
for needle in required:
    assert needle in proof, f"missing proof surface: {needle}"

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern)\b|"
    r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
    re.MULTILINE,
)
assert prohibited.search(proof) is None, "prohibited proof device found"

print("PASS THM-M-1227 proof packet: B-ZERO implementation candidate and hashes checked")
print("root remains open; five-node Galerkin/compactness cut preserved")
