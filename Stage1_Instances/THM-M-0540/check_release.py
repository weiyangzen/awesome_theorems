#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0540-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0540"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
validation = load("validation-receipt.json")
instance = load("instance.json")

assert decision["item_id"] == "S56-M-0540-RELEASE"
assert decision["theorem_id"] == "THM-M-0540"
assert decision["prerequisite"]["item_id"] == "S56-M-0540-VALIDATION"
assert decision["prerequisite"]["receipt_id"] == validation["receipt_id"]
assert decision["prerequisite"]["receipt_sha256"] == digest("validation-receipt.json")
assert decision["prerequisite"]["release_grade"] is False
assert validation["result"]["hermetic_release_gate"] == "fail_closed"
assert validation["result"]["independent_verification_gate"] == "fail_closed"

for key, name in {
    "proof_receipt_sha256": "proof-receipt.json",
    "instance_sha256": "instance.json",
    "typed_graphs_sha256": "typed-graphs.json",
    "source_crosswalk_sha256": "source-statement-crosswalk.md",
    "readable_tree_sha256": "obligation-tree.md",
}.items():
    assert decision["reconciled_inputs"][key] == digest(name)

result = decision["decision"]
assert result["verdict"] == "blocked"
assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
assert result["root_vector_before"] == result["root_vector_after"] == instance["root_vector"]
assert result["audit_complete"] is instance["audit_complete"] is False
assert result["theorem_complete"] is instance["theorem_complete"] is False
assert result["accepted_receipt_ids"] == []
assert decision["evidence_reconciliation"]["master_acceptance"] == "absent"

required_failures = {
    "immutable_clean_input",
    "cold_empty_cache_build",
    "offline_restoration_and_replay",
    "complete_tcb_sbom_and_license_archive",
    "deterministic_evidence_bundle",
    "independent_clean_runner_attestation",
    "independently_implemented_minimal_verifier",
}
assert all(decision["evidence_reconciliation"][key] == "fail" for key in required_failures)

print("ok: prerequisite validation receipt and all reconciled input hashes match")
print("ok: weaker-state rule preserved planned [H1, M3, R4] with no accepted receipts")
print("ok: AUDIT-Z and every missing release gate fail closed")
print("verdict: blocked; audit_complete=false; theorem_complete=false")
