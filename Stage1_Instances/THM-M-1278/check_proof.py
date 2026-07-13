#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1278 partial proof phase."""

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
registry = json.loads((HERE / "obligation-registry.json").read_text(encoding="utf-8"))
graphs = json.loads((HERE / "typed-graphs.json").read_text(encoding="utf-8"))

assert phase["item_id"] == "S56-M-1278-PROOF"
assert phase["theorem_id"] == "THM-M-1278"
assert registry["item_id"] == graphs["item_id"] == "S56-M-1278-OBLIGATION_TREE"
assert registry["theorem_id"] == graphs["theorem_id"] == "THM-M-1278"
assert phase["inputs"]["proof_source_sha256"] == hashlib.sha256(proof_path.read_bytes()).hexdigest()
for key, name in (
    ("statement_source_sha256", "Statement.lean"),
    ("obligation_tree_source_sha256", "ObligationTree.lean"),
    ("obligation_registry_sha256", "obligation-registry.json"),
    ("typed_graphs_sha256", "typed-graphs.json"),
):
    assert phase["inputs"][key] == hashlib.sha256((HERE / name).read_bytes()).hexdigest()
denominator = registry["frozen_denominators"]
denominator_sha256 = hashlib.sha256(
    json.dumps(denominator, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()
assert phase["inputs"]["registry_denominator_sha256"] == denominator_sha256
assert denominator_sha256 == graphs["registry_denominator_sha256"]

fingerprints = {row["obligation_id"]: row["statement_fingerprint"] for row in registry["obligations"]}
implemented = {
    row["obligation_id"]: row["obligation_statement_fingerprint"]
    for row in phase["implemented_declarations"]
}
assert implemented == {
    "M1278-N-SUBTRACT-MEAN": fingerprints["M1278-N-SUBTRACT-MEAN"],
    "M1278-N-ENERGY": fingerprints["M1278-N-ENERGY"],
}
assert phase["closed_obligation_ids"] == ["M1278-N-SUBTRACT-MEAN", "M1278-N-ENERGY"]
assert phase["remaining_root_cut_set"] == [
    "M1278-L-SHARP-ONOFRI", "M1278-S-AREA", "M1278-S-FINITE"
]
assert phase["first_failed_gate"] == "M1278-L-SHARP-ONOFRI"
assert phase["phase_self_tested"] is True
assert phase["root_closed"] is False
assert phase["audit_complete"] is False
assert phase["theorem_complete"] is False

assert receipt["item_id"] == phase["item_id"]
assert receipt["theorem_id"] == phase["theorem_id"]
assert receipt["base_revision"] == phase["base_revision"]
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
assert receipt["proof_body"]["source_sha256"] == phase["inputs"]["proof_source_sha256"]
assert receipt["closed_obligation_ids"] == phase["closed_obligation_ids"]
assert receipt["obligation_statement_fingerprints"] == implemented
assert receipt["inputs"] == phase["inputs"]
assert receipt["first_failed_gate"] == phase["first_failed_gate"]
assert receipt["remaining_root_cut_set"] == phase["remaining_root_cut_set"]
assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
assert receipt["result"]["root_closed"] is False
assert receipt["result"]["audit_complete"] is False
assert receipt["result"]["theorem_complete"] is False

assert blocker["item_id"] == phase["item_id"]
assert blocker["theorem_id"] == phase["theorem_id"]
assert blocker["outcome"] == "partial_proof_self_tested_root_blocked"
assert blocker["closed_obligation_ids"] == phase["closed_obligation_ids"]
assert blocker["first_failed_gate"] == phase["first_failed_gate"]
assert blocker["remaining_root_cut_set"] == phase["remaining_root_cut_set"]
assert blocker["root_closed"] is blocker["audit_complete"] is blocker["theorem_complete"] is False

required = (
    "theorem exists_subtract_mean",
    "theorem gradient_subtractMean_extension",
    "theorem tangentialGradient_subtractMean",
    "theorem dirichletEnergy_subtractMean",
    "#print axioms exists_subtract_mean",
    "#print axioms dirichletEnergy_subtractMean",
)
for needle in required:
    assert needle in proof, f"missing proof surface: {needle}"

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern)\b|"
    r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
    re.MULTILINE,
)
assert prohibited.search(proof) is None, "prohibited proof device found"

print("PASS THM-M-1278 proof phase: mean-shift construction and energy invariance checked")
print("root closure: open (M3); sharp Onofri, area, and finiteness cut remains")
