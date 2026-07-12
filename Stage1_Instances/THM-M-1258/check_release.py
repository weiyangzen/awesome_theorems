#!/usr/bin/env python3
"""Check that the THM-M-1258 release decision fails closed from current authority."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1258"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text())


def sha256(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
instance = load("instance.json")
dag = load("task-dag.json")
graphs = load("typed-graphs.json")
receipt = load("validation-receipt.json")

assert decision["item_id"] == "S56-M-1258-RELEASE"
assert decision["theorem_id"] == instance["theorem_id"] == receipt["theorem_id"]
assert decision["input_receipt_id"] == receipt["receipt_id"]
assert decision["input_receipt_sha256"] == sha256("validation-receipt.json")

# A release decision may not promote provisional evidence or contradict structured authority.
assert instance["lifecycle"] == decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert instance["root_vector"] == decision["root_vector_before"] == decision["root_vector_after"]
assert instance["audit_complete"] is decision["audit_complete"] is False
assert instance["theorem_complete"] is decision["theorem_complete"] is False
assert dag["accepted_states"] == decision["accepted_receipt_ids"] == []
tasks = {task["id"]: task for task in dag["tasks"]}
assert tasks["S56-M-1258-VALIDATION"]["state"] == "open"
assert tasks["S56-M-1258-RELEASE"]["state"] == "open"
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False
assert graphs["root_cut_set"] == decision["remaining_root_cut_set"]

assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["release_grade"] is False
assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
assert receipt["result"]["independent_verification_gate"] == "fail_closed"
assert receipt["result"]["audit_complete"] is False
assert receipt["result"]["theorem_complete"] is False

assert decision["verdict"] == "blocked"
assert decision["first_failed_gate"]["gate"] == "dependency_legal_accepted_state"
assert decision["audit_complete"] is False
assert decision["theorem_complete"] is False
assert decision["accepted_receipt_ids"] == []
assert len(decision["failed_release_gates"]) >= 10

print("ok: release decision is bound to the current provisional validation receipt")
print("ok: lifecycle, task DAG, root graph, debts, and terminal booleans were not promoted")
print("blocked: predecessor acceptance is absent; hermetic and independent release gates also fail")
