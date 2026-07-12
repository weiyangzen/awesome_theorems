#!/usr/bin/env python3
"""Fail-closed consistency check for S56-M-0696-RELEASE."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0696"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def sha256(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
validation = load("validation-receipt.json")
intake = load("intake.json")
graphs = load("typed-graphs.json")
targets = json.loads(
    (ROOT / "Docs" / "Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8")
)

target = next(entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-0696")
assert target["execution_rank"] == 737
assert target["lifecycle_mode"] == "planned"
assert target["theorem_complete"] is False

assert decision["item_id"] == "S56-M-0696-RELEASE"
assert decision["theorem_id"] == "THM-M-0696"
dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0696-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == sha256("validation-receipt.json")
assert dependency["support_state"] == validation["support_state"] == "provisional_worker_selftest"
assert dependency["release_grade"] is validation["release_grade"] is False
assert dependency["master_accepted"] is False

result = decision["decision"]
assert result["verdict"] == "blocked"
assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
accepted_vector = [
    intake["root_vector"]["human"],
    intake["root_vector"]["machine"],
    intake["root_vector"]["readability"],
]
assert result["accepted_root_vector_before"] == accepted_vector == ["H1", "M4", "R3"]
assert result["accepted_root_vector_after"] == accepted_vector
assert result["audit_complete"] is result["theorem_complete"] is False
assert result["release_accepted"] is False
assert decision["accepted_receipt_ids"] == []
assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert result["next_failed_theorem_gate"]["gate_id"] == "evidence.structured_state_freshness"

validation_result = validation["result"]
assert validation_result["kernel_replay"].startswith("pass_for_exact_frozen_root")
assert validation_result["frozen_graph_state"].startswith("stale_pre_proof")
assert validation_result["hermetic_release_gate"] == "fail_closed"
assert validation_result["independent_distinct_runner_gate"] == "fail_closed"
assert validation_result["audit_complete"] is validation_result["theorem_complete"] is False
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False
assert graphs["closure_boundary"]["root_vector"] == ["H1", "M3", "R3"]

reconciliation = decision["evidence_reconciliation"]
assert reconciliation["frozen_graph_root_closed"] is False
assert reconciliation["frozen_graph_root_vector"] == graphs["closure_boundary"]["root_vector"]
for gate in (
    "authoritative_graph_reconciled",
    "audit_z_accepted",
    "theorem_z_accepted",
    "pinpoint_h0_review",
    "independent_r0_review",
    "hermetic_cold_offline_replay",
    "tcb_sbom_license_closure",
    "independent_clean_runner_attestation",
    "independently_implemented_minimal_verifier",
    "deterministic_release_bundle",
    "master_acceptance",
):
    assert reconciliation[gate] is False

cut_set = "\n".join(result["remaining_root_cut_set"])
for required in (
    "master acceptance",
    "frozen obligation graph",
    "H0 pinpoint primary-source",
    "R0 structured reconstruction",
    "transitive TCB closure",
    "empty-cache network-denied cold build",
    "SBOM and license",
    "two signed attestations",
    "minimal release verifier",
    "deterministic content-addressed current release bundle",
):
    assert required in cut_set

print(
    "release-decision: ok (blocked; validation unaccepted and nonrelease; "
    "structured graph stale; audit_complete=false; theorem_complete=false)"
)
