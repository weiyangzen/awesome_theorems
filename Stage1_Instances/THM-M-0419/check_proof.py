#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0419 partial proof phase."""

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PROOF_PATH = HERE / "Proof.lean"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


proof = PROOF_PATH.read_text(encoding="utf-8")
phase = json.loads((HERE / "proof-phase.json").read_text(encoding="utf-8"))
receipt = json.loads((HERE / "proof-receipt.json").read_text(encoding="utf-8"))
blocker = json.loads(
    (HERE / "proof-recheck-2026-07-15-head-b1a5b03c-slot14.json").read_text(
        encoding="utf-8"
    )
)
worker = json.loads((ROOT / ".stage1-worker-selftest.json").read_text(encoding="utf-8"))
registry = json.loads((HERE / "obligation-registry.json").read_text(encoding="utf-8"))
graphs = json.loads((HERE / "typed-graphs.json").read_text(encoding="utf-8"))

assert phase["item_id"] == receipt["item_id"] == blocker["item_id"] == worker["item_id"] == "S56-M-0419-PROOF"
assert phase["theorem_id"] == receipt["theorem_id"] == blocker["theorem_id"] == worker["theorem_id"] == "THM-M-0419"
assert phase["base_revision"] == receipt["base_revision"] == blocker["base_revision"] == worker["base_revision"]
assert phase["base_tree"] == receipt["base_tree"] == blocker["base_tree"]
assert phase["base_revision"] == subprocess.check_output(
    ["git", "rev-parse", "HEAD"], text=True, cwd=ROOT
).strip()
assert phase["base_tree"] == subprocess.check_output(
    ["git", "rev-parse", "HEAD^{tree}"], text=True, cwd=ROOT
).strip()

for key, name in (
    ("proof_source_sha256", "Proof.lean"),
    ("statement_source_sha256", "Statement.lean"),
    ("obligation_tree_source_sha256", "ObligationTree.lean"),
    ("obligation_registry_sha256", "obligation-registry.json"),
    ("typed_graphs_sha256", "typed-graphs.json"),
    ("validation_specs_sha256", "validation-specs.json"),
    ("anchor_audit_sha256", "anchor-audit.json"),
):
    assert phase["inputs"][key] == receipt["inputs"][key] == digest(HERE / name)

assert phase["inputs"] == receipt["inputs"]
assert phase["inputs"]["registry_denominator_sha256"] == registry["denominator_sha256"]
assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"]
fingerprints = {
    row["obligation_id"]: row["statement_fingerprint"]
    for row in registry["obligations"]
}
implemented = phase["implemented_declarations"]
assert len(implemented) == 1
assert implemented[0]["declaration"] == "Stage1.THM_M_0419.Proof.cyclotomicIdentify"
assert implemented[0]["obligation_id"] == "M0419-C-CYCLOTOMIC-IDENTIFY"
assert implemented[0]["obligation_statement_fingerprint"] == fingerprints[
    "M0419-C-CYCLOTOMIC-IDENTIFY"
]
assert implemented[0]["terminal_declaration"] == "IsCyclotomicExtension.algEquiv"

candidate = ["M0419-C-CYCLOTOMIC-IDENTIFY"]
cut = [
    "M0419-B-INDUCTION",
    "M0419-L-TAME",
    "M0419-L-WILD-ODD",
    "M0419-L-WILD-TWO",
    "M0419-T-GLOBAL",
]
assert phase["proposed_closed_obligation_ids"] == candidate
assert receipt["proposed_closed_obligation_ids"] == candidate
assert phase["accepted_closed_obligation_ids"] == receipt["accepted_closed_obligation_ids"] == []
assert phase["remaining_root_cut_set"] == receipt["remaining_root_cut_set"] == cut
assert phase["first_failed_gate"] == receipt["first_failed_gate"] == "M0419-B-INDUCTION"
assert phase["root_vector_before"] == phase["root_vector_after"] == {
    "H": "H1", "M": "M3", "R": "R3"
}
assert phase["phase_self_tested"] is True
assert phase["root_closed"] is phase["audit_complete"] is phase["theorem_complete"] is False
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["proposed_state"] == worker["state"] == "[_]"
assert receipt["accepted"] is False and receipt["verdict"] == "blocked"
assert receipt["root_closed"] is receipt["audit_complete"] is receipt["theorem_complete"] is False
assert receipt["proof_body"]["source_sha256"] == digest(PROOF_PATH)
assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
assert worker["changed_paths"] == receipt["changed_paths"]
assert worker["known_failures"] == receipt["known_failures"]
assert blocker["changed_paths"] == receipt["changed_paths"]
assert blocker["proposed_closed_obligation_ids"] == candidate
assert blocker["accepted_closed_obligation_ids"] == []
assert blocker["positive_proof_body_added"] is blocker["proof_phase_self_tested"] is True
assert blocker["root_closed"] is blocker["audit_complete"] is blocker["theorem_complete"] is False
assert blocker["remaining_root_cut_set"] == cut
assert blocker["selftest_manifest_written"] is True

for needle in (
    "def AbstractPositiveContainmentTarget",
    "theorem cyclotomicIdentify :",
    "ObligationTree.PositiveContainmentTarget",
    "IsCyclotomicExtension.algEquiv",
    "#print axioms cyclotomicIdentify",
    "#print axioms IsCyclotomicExtension.algEquiv",
):
    assert needle in proof, f"missing proof surface: {needle}"

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern)\b|"
    r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
    re.MULTILINE,
)
assert prohibited.search(proof) is None, "prohibited proof device found"

print("PASS THM-M-0419 proof phase: cyclotomic-identification transport checked")
print("root closure: open (M3); local branches and globalization remain")
