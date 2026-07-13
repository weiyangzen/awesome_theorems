#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1026 partial proof phase."""

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text(encoding="utf-8")
phase = json.loads((HERE / "proof-phase.json").read_text(encoding="utf-8"))
receipt = json.loads((HERE / "proof-receipt.json").read_text(encoding="utf-8"))
blocker = json.loads((HERE / "proof-blocker.json").read_text(encoding="utf-8"))
worker = json.loads((HERE.parent.parent / ".stage1-worker-selftest.json").read_text(encoding="utf-8"))
registry = json.loads((HERE / "obligation-registry.json").read_text(encoding="utf-8"))
graphs = json.loads((HERE / "typed-graphs.json").read_text(encoding="utf-8"))

assert phase["item_id"] == receipt["item_id"] == blocker["item_id"] == "S56-M-1026-PROOF"
assert phase["theorem_id"] == receipt["theorem_id"] == blocker["theorem_id"] == "THM-M-1026"
assert registry["item_id"] == graphs["item_id"] == "S56-M-1026-OBLIGATION_TREE"
assert registry["theorem_id"] == graphs["theorem_id"] == "THM-M-1026"

for key, name in (
    ("proof_source_sha256", "Proof.lean"),
    ("statement_source_sha256", "Statement.lean"),
    ("obligation_tree_source_sha256", "ObligationTree.lean"),
    ("obligation_registry_sha256", "obligation-registry.json"),
    ("typed_graphs_sha256", "typed-graphs.json"),
    ("validation_specs_sha256", "validation-specs.json"),
    ("anchor_audit_sha256", "anchor-audit.json"),
):
    assert phase["inputs"][key] == hashlib.sha256((HERE / name).read_bytes()).hexdigest()

assert phase["inputs"]["registry_denominator_sha256"] == registry["denominator_sha256"]
assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"]
fingerprints = {row["obligation_id"]: row["statement_fingerprint"] for row in registry["obligations"]}
implemented = {
    row["obligation_id"]: row["obligation_statement_fingerprint"]
    for row in phase["implemented_declarations"]
}
assert implemented == {
    obligation_id: fingerprints[obligation_id]
    for obligation_id in (
        "M1026-B-CONVERSE",
        "M1026-C-STABLE-WITNESS",
        "M1026-L-CONSTANT-WEAK-LIMIT",
        "M1026-T-CONVERSE",
    )
}
assert phase["closed_obligation_ids"] == [
    "M1026-B-CONVERSE",
    "M1026-C-STABLE-WITNESS",
    "M1026-L-CONSTANT-WEAK-LIMIT",
    "M1026-T-CONVERSE",
]
assert phase["remaining_root_cut_set"] == ["M1026-T-NECESSITY"]
assert phase["first_failed_gate"] == "M1026-C-BLOCK-DECOMPOSITION"
assert phase["phase_self_tested"] is True
assert phase["root_closed"] is phase["audit_complete"] is phase["theorem_complete"] is False

assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
assert receipt["verdict"] == "blocked"
assert receipt["inputs"] == phase["inputs"]
assert receipt["closed_obligation_ids"] == phase["closed_obligation_ids"]
assert receipt["obligation_statement_fingerprints"] == implemented
assert receipt["first_failed_gate"] == phase["first_failed_gate"]
assert receipt["remaining_root_cut_set"] == phase["remaining_root_cut_set"]
assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
assert receipt["result"]["root_closed"] is False
assert receipt["result"]["theorem_complete"] is False

assert blocker["outcome"] == "partial_proof_self_tested_root_blocked"
assert blocker["closed_obligation_ids"] == phase["closed_obligation_ids"]
assert blocker["first_failed_gate"] == phase["first_failed_gate"]
assert blocker["remaining_root_cut_set"] == phase["remaining_root_cut_set"]
assert blocker["root_closed"] is blocker["audit_complete"] is blocker["theorem_complete"] is False

assert worker["item_id"] == phase["item_id"]
assert worker["theorem_id"] == phase["theorem_id"]
assert worker["base_revision"] == phase["base_revision"]
assert worker["state"] == "[_]"
assert worker["theorem_complete"] is False
assert worker["changed_paths"] == receipt["changed_paths"]

for needle in (
    "theorem stable_normalizers",
    "theorem weaklyConverges_of_eventually_eq",
    "theorem converseTerminal",
    "#print axioms stable_normalizers",
    "#print axioms weaklyConverges_of_eventually_eq",
    "#print axioms converseTerminal",
):
    assert needle in proof, f"missing proof surface: {needle}"

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern)\b|"
    r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
    re.MULTILINE,
)
assert prohibited.search(proof) is None, "prohibited proof device found"

print("PASS THM-M-1026 proof phase: converse branch checked")
print("root closure: open (M3); necessity terminal remains")
