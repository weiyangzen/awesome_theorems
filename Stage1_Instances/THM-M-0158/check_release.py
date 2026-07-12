#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0158-RELEASE."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text())


def sha256(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
validation = load("validation-receipt.json")
instance = load("instance.json")
graphs = load("typed-graphs.json")

assert decision["item_id"] == "S56-M-0158-RELEASE"
assert decision["theorem_id"] == validation["theorem_id"] == instance["theorem_id"] == "THM-M-0158"
upstream = decision["upstream_validation"]
assert upstream["receipt_id"] == validation["receipt_id"]
assert upstream["receipt_sha256"] == sha256("validation-receipt.json")
assert validation["support_state"] == upstream["support_state"] == "provisional_worker_selftest"
assert validation["release_grade"] is upstream["release_grade"] is False
assert validation["result"]["audit_complete"] is False
assert validation["result"]["theorem_complete"] is False
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False
assert graphs["closure_boundary"]["minimal_open_root_cut"] == ["M0158-T-RECONSTRUCT"]
assert instance["lifecycle"] == "planned"
assert instance["theorem_complete"] is False

result = decision["decision"]
assert result["verdict"] == "blocked"
assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
assert result["root_vector_before"] == result["root_vector_after"] == ["H1", "M4", "R4"]
assert result["audit_complete"] is result["theorem_complete"] is result["release_accepted"] is False
assert result["accepted_receipt_ids"] == []
assert result["first_failed_gate"]
assert len(result["remaining_root_cut_set"]) == 7

gates = decision["evidence_reconciliation"]
assert gates["canonical_statement_kernel_replay"] == "provisional_pass"
assert gates["direct_exact_proof_kernel_replay"] == "provisional_pass"
assert gates["accepted_root_machine_state"] == "open"
for name in (
    "authoritative_graph_reconciled",
    "audit_z_accepted",
    "hermetic_cold_offline_replay",
    "tcb_sbom_license_closure",
    "independent_clean_runner_attestation",
    "independently_implemented_minimal_verifier",
    "pinpoint_h0_review",
    "independent_r0_review",
    "master_acceptance",
):
    assert gates[name] is False, name

print("PASS S56-M-0158-RELEASE reconciliation")
print("verdict=blocked audit_complete=false theorem_complete=false release_accepted=false")
print(f"first_failed_gate={result['first_failed_gate']}")
