#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1333-RELEASE."""

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1333"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def sha256(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


spec = load("release-spec.json")
decision = load("release-decision.json")
validation = load("validation-receipt.json")
statement = load("statement.json")
proof = load("proof-receipt.json")
graphs = load("typed-graphs.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))

target = next(entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-1333")
assert target["execution_rank"] == 874
assert target["lifecycle_mode"] == "planned"
assert target["theorem_complete"] is False
assert spec["item_id"] == decision["item_id"] == "S56-M-1333-RELEASE"
assert spec["theorem_id"] == decision["theorem_id"] == "THM-M-1333"

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-1333-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == sha256("validation-receipt.json")
assert dependency["support_state"] == validation["support_state"] == "provisional_worker_selftest"
assert dependency["release_grade"] is validation["release_grade"] is False
assert dependency["master_accepted"] is False

result = subprocess.run(
    ["python3", str(HERE / "check_validation.py")],
    cwd=ROOT,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    timeout=150,
    check=False,
)
assert result.returncode == 0, result.stdout
assert "OPEN exact root" in result.stdout
assert "BLOCKED release gates" in result.stdout

assert statement["statement_elaborated"] is True
assert statement["theorem_complete"] is False
assert proof["result"]["root_closed"] is False
assert validation["result"]["unconditional_root_proof_body_present"] is False
assert validation["result"]["audit_complete"] is False
assert validation["result"]["theorem_complete"] is False
assert validation["result"]["hermetic_release_gate"] == "fail_closed"
assert validation["result"]["independent_distinct_runner_gate"] == "fail_closed"
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["root_machine_debt"] == "M4"

verdict = decision["decision"]
assert verdict["verdict"] == "blocked"
assert verdict["lifecycle_before"] == verdict["lifecycle_after"] == "planned"
assert verdict["root_vector_before"] == verdict["root_vector_after"] == ["H2", "M4", "R3"]
assert verdict["audit_complete"] is verdict["theorem_complete"] is verdict["release_accepted"] is False
assert verdict["accepted_receipt_ids"] == []
assert verdict["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert verdict["next_failed_theorem_gate"]["gate_id"] == "proof.root_kernel_closure"
assert verdict["remaining_root_cut_set"][:5] == [
    "M1333-C-EULER", "M1333-C-INVARIANTS", "M1333-L-COMPACT",
    "M1333-L-INTEGRAL", "M1333-L-DERIV",
]
assert decision["release_grade"] is False
assert decision["master_acceptance"] == "pending_and_not_claimed"

for gate in (
    "exact_root_kernel_closed", "authoritative_graph_reconciled", "audit_z_accepted",
    "pinpoint_h0_review", "independent_r0_review", "hermetic_cold_offline_replay",
    "tcb_sbom_license_closure", "independent_clean_runner_attestation",
    "independently_implemented_minimal_verifier", "deterministic_release_bundle",
    "master_acceptance",
):
    assert decision["evidence_reconciliation"][gate] is False, gate

print("PASS S56-M-1333-RELEASE reconciliation and upstream narrow Lean replay")
print("verdict=blocked lifecycle=planned root_vector=H2/M4/R3")
print("audit_complete=false theorem_complete=false accepted_receipts=0")
print("first_failed_gate=S56-10.2-DEPENDENCY-ACCEPTANCE")
print("next_failed_theorem_gate=proof.root_kernel_closure:M1333-C-EULER")
