#!/usr/bin/env python3
"""Fail-closed consistency check for S56-M-0707-RELEASE."""

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0707"


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

target = next(entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-0707")
assert target["execution_rank"] == 748
assert target["lifecycle_mode"] == "planned"
assert target["theorem_complete"] is False

assert decision["item_id"] == "S56-M-0707-RELEASE"
assert decision["theorem_id"] == "THM-M-0707"
dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0707-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == sha256("validation-receipt.json")
assert dependency["support_state"] == validation["support_state"] == "provisional_worker_selftest"
assert dependency["release_grade"] is validation["release_grade"] is False
assert dependency["master_accepted"] is False

replay = subprocess.run(
    ["python3", str(HERE / "check_validation.py")],
    cwd=ROOT,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    timeout=60,
    check=False,
)
assert replay.returncode == 0, replay.stdout

result = decision["decision"]
assert result["verdict"] == "blocked"
assert result["lifecycle_before"] == result["lifecycle_after"] == instance["lifecycle"] == "planned"
assert result["root_vector_before"] == result["root_vector_after"] == ["H1", "M4", "R3"]
assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R3"}
assert result["audit_complete"] is result["theorem_complete"] is result["release_accepted"] is False
assert decision["accepted_receipt_ids"] == []
assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert result["next_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"

assert validation["result"]["exact_root_proof_body_present"] is True
assert validation["result"]["hermetic_release_gate"] == "fail_closed"
assert validation["result"]["independent_distinct_runner_gate"] == "fail_closed"
assert validation["result"]["audit_complete"] is False
assert validation["result"]["theorem_complete"] is False
boundary = graphs["closure_boundary"]
assert boundary["root_closed"] is False
assert boundary["provisional_root_machine_classification"] == "M0-W"
assert boundary["remaining_root_cut_set"] == [
    "M0707-X-SOURCE", "M0707-X-FOUNDATION", "M0707-X-PROVENANCE"
]

for gate in (
    "authoritative_state_reconciled",
    "audit_z_accepted",
    "pinpoint_h0_review",
    "independent_r0_review",
    "accepted_foundation_and_provenance_closure",
    "hermetic_cold_offline_replay",
    "tcb_sbom_license_closure",
    "independent_clean_runner_attestation",
    "independently_implemented_minimal_verifier",
    "deterministic_release_bundle",
    "master_acceptance",
):
    assert decision["evidence_reconciliation"][gate] is False, gate

cut = "\n".join(result["remaining_root_cut_set"])
for fragment in (
    "M0707-X-SOURCE",
    "M0707-X-FOUNDATION",
    "M0707-X-PROVENANCE",
    "R0 structured",
    "empty-cache network-denied cold build",
    "two signed attestations",
    "minimal release verifier",
    "deterministic content-addressed release bundle",
):
    assert fragment in cut, fragment

print("PASS S56-M-0707-RELEASE reconciliation")
print("verdict=blocked lifecycle=planned accepted_root_vector=H1/M4/R3")
print("provisional_kernel_root=M0-W audit_complete=false theorem_complete=false")
print("first_failed_gate=S56-10.2-DEPENDENCY-ACCEPTANCE")
print("next_failed_release_gate=S56-10.6-HERMETIC-COLD-BUILD")
