#!/usr/bin/env python3
"""Fail-closed consistency check for S56-M-0771-RELEASE."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0771"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
instance = load("instance.json")
proof = load("proof-receipt.json")
validation = load("validation-receipt.json")
graphs = load("typed-graphs.json")
targets = json.loads(
    (ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8")
)
target = next(
    entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-0771"
)

assert target["execution_rank"] == 780
assert target["lifecycle_mode"] == instance["lifecycle"] == "planned"
assert target["theorem_complete"] is instance["theorem_complete"] is False
assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}

assert decision["item_id"] == "S56-M-0771-RELEASE"
assert decision["theorem_id"] == "THM-M-0771"
dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0771-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == digest("validation-receipt.json")
assert dependency["support_state"] == validation["support_state"] == "provisional_worker_selftest"
assert dependency["release_grade"] is validation["release_grade"] is False
assert dependency["master_accepted"] is False
assert proof["support_state"] == "provisional_worker_selftest"

result = decision["decision"]
assert result["verdict"] == "blocked"
assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
assert result["root_vector_before"] == result["root_vector_after"] == ["H1", "M3", "R4"]
assert result["audit_complete"] is result["theorem_complete"] is result["release_accepted"] is False
assert decision["accepted_receipt_ids"] == []
assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert result["first_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-REPLAY"

validation_result = validation["result"]
assert validation_result["root_kernel_closed"] is True
assert validation_result["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
assert validation_result["audit_complete"] is validation_result["theorem_complete"] is False
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["root_machine_classification"] == "M3"
assert graphs["closure_boundary"]["theorem_complete"] is False

for gate in (
    "authoritative_graph_reconciled",
    "audit_z_accepted",
    "primary_source_h0_review",
    "independent_r0_review",
    "complete_transitive_provenance_and_tcb",
    "immutable_clean_release_input",
    "hermetic_cold_offline_replay",
    "sbom_and_license_closure",
    "independent_clean_runner_attestation",
    "independently_implemented_minimal_verifier",
    "mutation_and_metamorphic_ci",
    "deterministic_release_bundle",
    "master_acceptance",
):
    assert decision["evidence_reconciliation"][gate] is False, gate

cut_set = "\n".join(result["remaining_root_cut_set"])
for fragment in (
    "master acceptance",
    "stale frozen graph",
    "H0 primary-source",
    "R0 unique anchored",
    "transitive proof-body provenance",
    "empty-cache network-denied cold build",
    "SBOM and license",
    "two signed attestations",
    "minimal release verifier",
    "deterministic content-addressed release bundle",
):
    assert fragment in cut_set, fragment

print("PASS S56-M-0771-RELEASE reconciliation")
print("verdict=blocked lifecycle=planned root_vector=H1/M3/R4")
print("audit_complete=false theorem_complete=false accepted_receipts=0")
print("first_failed_gate=S56-10.2-DEPENDENCY-ACCEPTANCE")
print("first_failed_release_gate=S56-10.6-HERMETIC-COLD-REPLAY")
