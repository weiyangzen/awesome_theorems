#!/usr/bin/env python3
"""Fail-closed evidence reconciliation for S56-M-0342-RELEASE."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0342"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text())


def sha256(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
instance = load("instance.json")
tasks = load("task-dag.json")
graphs = load("typed-graphs.json")
proof = load("proof-receipt.json")
validation = load("validation-receipt.json")

assert decision["item_id"] == "S56-M-0342-RELEASE"
assert decision["theorem_id"] == instance["theorem_id"] == "THM-M-0342"
assert decision["dependency_item"] == validation["item_id"] == "S56-M-0342-VALIDATION"
assert validation["support_state"] == "provisional_worker_selftest"
assert validation["release_grade"] is False
assert validation["result"]["root_closed_by_checked_proof"] is True
assert validation["result"]["hermetic_release_gate"] == "fail_closed"
assert validation["result"]["independent_distinct_runner_gate"] == "fail_closed"
assert validation["result"]["audit_complete"] is False
assert validation["result"]["theorem_complete"] is False
assert proof["result"]["root_closed_by_proof"] is True
assert proof["result"]["theorem_complete"] is False
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False
assert instance["root_vector"] == decision["root_vector_before"] == decision["root_vector_after"]
assert instance["audit_complete"] is decision["audit_complete"] is False
assert instance["theorem_complete"] is decision["theorem_complete"] is False
assert instance["accepted_proof_state"] == decision["accepted_receipt_ids"] == []
assert tasks["lifecycle"] == decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
release_task = next(task for task in tasks["tasks"] if task["id"] == decision["item_id"])
assert release_task["state"] == "open"
assert decision["decision"] == "no_theorem_completion"
assert decision["verdict"] == "no_state_change"
assert decision["first_failed_gate"] == "release.dependency_master_acceptance"
assert decision["evidence_reconciliation"]["master_acceptance"] == "fail_pending"
assert all(value.startswith("fail_") for key, value in decision["evidence_reconciliation"].items()
           if key not in {"exact_statement_elaboration", "exact_root_kernel_closure", "placeholder_and_unsafe_scan"})

receipt = load("release-receipt.json")
assert receipt["inputs"]["release_decision_sha256"] == sha256("release-decision.json")
assert receipt["inputs"]["validation_receipt_sha256"] == sha256("validation-receipt.json")
assert receipt["inputs"]["proof_receipt_sha256"] == sha256("proof-receipt.json")
assert receipt["inputs"]["instance_sha256"] == sha256("instance.json")
assert receipt["inputs"]["task_dag_sha256"] == sha256("task-dag.json")
assert receipt["inputs"]["typed_graphs_sha256"] == sha256("typed-graphs.json")
assert receipt["result"]["theorem_complete"] is False
assert receipt["result"]["state_transition"] == "none"

print("PASS release reconciliation: provisional kernel evidence and authoritative open state agree")
print("PASS fail-closed decision: audit_complete=false and theorem_complete=false")
print("NO STATE CHANGE: lifecycle remains planned; no receipt is accepted")
print("FIRST FAILED GATE: release.dependency_master_acceptance")
print("BLOCKED THEOREM-Z: H0/R0, state freshness, TCB, hermetic, bundle, independent verifier, and master gates remain open")
