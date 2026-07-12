#!/usr/bin/env python3
"""Fail-closed consistency check for S56-M-0653-RELEASE."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0653"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def sha256(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
validation = load("validation-receipt.json")
instance = load("instance.json")
graphs = load("typed-graphs.json")
targets = json.loads(
    (ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8")
)

target = next(
    entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-0653"
)
assert target["execution_rank"] == 698
assert target["lifecycle_mode"] == "planned"
assert target["theorem_complete"] is False

assert decision["item_id"] == "S56-M-0653-RELEASE"
assert decision["theorem_id"] == "THM-M-0653"
dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0653-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == sha256("validation-receipt.json")
assert dependency["support_state"] == validation["support_state"] == "provisional_worker_selftest"
assert dependency["release_grade"] is validation["release_grade"] is False
assert dependency["master_accepted"] is False

result = decision["decision"]
assert result["verdict"] == "blocked"
assert result["lifecycle_before"] == result["lifecycle_after"] == instance["lifecycle"] == "planned"
assert result["root_vector_before"] == result["root_vector_after"] == ["H2", "M3", "R4"]
assert instance["root_vector"] == {"H": "H2", "M": "M3", "R": "R4"}
assert result["audit_complete"] is result["theorem_complete"] is result["release_accepted"] is False
assert decision["accepted_receipt_ids"] == []
assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert result["next_failed_theorem_gate"]["gate_id"] == "proof.root_kernel_closure"

assert validation["result"]["unconditional_root_proof_body_present"] is False
assert validation["result"]["minimal_mathematical_open_root_cut_set"] == ["M0653-D-BETH"]
assert validation["result"]["audit_complete"] is False
assert validation["result"]["theorem_complete"] is False
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["root_machine_classification"] == "M3"
assert graphs["closure_boundary"]["theorem_complete"] is False

reconciliation = decision["evidence_reconciliation"]
for gate in (
    "authoritative_graph_reconciled",
    "audit_z_accepted",
    "pinpoint_h0_review",
    "independent_r0_review",
    "hermetic_cold_offline_replay",
    "tcb_sbom_license_closure",
    "independent_clean_runner_attestation",
    "independently_implemented_minimal_verifier",
    "deterministic_release_bundle",
    "master_acceptance",
):
    assert reconciliation[gate] is False, gate

cut = "\n".join(result["remaining_root_cut_set"])
for fragment in (
    "M0653-D-BETH",
    "H0 primary-source",
    "R0 structured",
    "empty-cache network-denied cold build",
    "two signed attestations",
    "minimal release verifier",
    "deterministic content-addressed release bundle",
):
    assert fragment in cut, fragment

print("PASS S56-M-0653-RELEASE reconciliation")
print("verdict=blocked lifecycle=planned root_vector=H2/M3/R4")
print("audit_complete=false theorem_complete=false accepted_receipts=0")
print("first_failed_gate=S56-10.2-DEPENDENCY-ACCEPTANCE")
print("next_failed_theorem_gate=proof.root_kernel_closure:M0653-D-BETH")
