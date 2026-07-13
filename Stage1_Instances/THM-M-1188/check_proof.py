#!/usr/bin/env python3
"""Validate THM-M-1188 provisional proof artifacts and worker handoff."""

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RECEIPT = HERE / "proof-receipt.json"
PACKET = ROOT / ".stage1-worker-selftest.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


receipt = json.loads(RECEIPT.read_text())
packet = json.loads(PACKET.read_text())

assert receipt["schema_version"] == "stage1-node-receipt/1.0"
assert receipt["item_id"] == packet["item_id"] == "S56-M-1188-PROOF"
assert receipt["theorem_id"] == "THM-M-1188"
assert receipt["phase"] == "proof" and receipt["intent"] == "prove"
assert receipt["accepted"] is False and receipt["accepted_receipt_ids"] == []
assert receipt["proposed_state"] == packet["state"] == "[_]"
assert receipt["base_revision"] == packet["base_revision"]
assert receipt["changed_paths"] == packet["changed_paths"]
assert receipt["known_failures"] == packet["known_failures"]
assert set(packet) == {
    "item_id", "changed_paths", "commands", "output_summary",
    "base_revision", "known_failures", "state",
}

inputs = receipt["inputs"]
for key, name in {
    "statement_sha256": "Statement.lean",
    "obligation_tree_sha256": "ObligationTree.lean",
    "obligation_registry_sha256": "obligation-registry.json",
    "typed_graphs_sha256": "typed-graphs.json",
    "validation_specs_sha256": "validation-specs.json",
    "anchor_audit_sha256": "anchor-audit.json",
    "check_proof_sh_sha256": "check_proof.sh",
}.items():
    assert inputs[key] == sha256(HERE / name), f"stale hash for {name}"
assert receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
assert inputs["check_proof_py_sha256"] == sha256(HERE / "check_proof.py")
registry = json.loads((HERE / "obligation-registry.json").read_text())
assert inputs["registry_denominator_sha256"] == registry["denominator_sha256"]

closed = set(receipt["provisionally_closed_obligation_ids"])
assert set(receipt["recipe"]["covered_ids"]) == closed
assert closed == {
    "M1188-ROOT", "M1188-S-DOMAIN", "M1188-S-BOUNDARY",
    "M1188-S-REGULARITY", "M1188-C-COMPACT", "M1188-L-ATTAIN",
    "M1188-C-PERTURB", "M1188-L-SPATIAL", "M1188-L-TEMPORAL",
    "M1188-B-INTERIOR", "M1188-N-BOUNDARY", "M1188-L-EPSILON",
    "M1188-T-ENGINE", "M1188-T-ASSEMBLE",
}
assert set(receipt["open_proof_or_release_boundaries"]) == {
    "M1188-S-FOUNDATION", "M1188-X-SOURCE", "M1188-X-PROVENANCE",
}
result = receipt["result"]
assert result["exit_code"] == 0 and result["root_kernel_closed"] is True
assert result["accepted_root_closed"] is False
assert result["theorem_complete"] is False
assert result["machine_debt_proposal"] == "M0-L after master acceptance"
assert set(result["axioms"]) == {"propext", "Classical.choice", "Quot.sound"}

proof = (HERE / "Proof.lean").read_text()
for forbidden in ("sorry", "admit", "axiom ", "sorryAx", "unsafe "):
    assert forbidden not in proof, f"prohibited token in Proof.lean: {forbidden}"
for declaration in receipt["exact_declarations"] + receipt["audited_declarations"]:
    assert declaration.split(".")[-1] in proof or declaration.endswith("root_compose")

head = subprocess.run(
    ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True,
    stdout=subprocess.PIPE, check=True,
).stdout.strip()
assert head == receipt["base_revision"]

print("PASS THM-M-1188 proof receipt, hashes, closure boundary, and worker packet")
