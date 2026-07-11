#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0107-RELEASE."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0107"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text())


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
validation = load("validation-receipt.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
intake = load("intake.json")

assert decision["item_id"] == "S56-M-0107-RELEASE"
assert decision["theorem_id"] == "THM-M-0107"
assert decision["intent"] == "release"
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0107-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == digest("validation-receipt.json")
assert dependency["support_state"] == validation["support_state"] == "provisional_worker_selftest"
assert dependency["release_grade"] is validation["release_grade"] is False
assert dependency["master_accepted"] is False

root = decision["reconciled_root"]
assert registry["root_obligation_id"] == "M0107-ROOT"
assert intake["lifecycle_mode"] == "planned"
assert intake["root_vector"] == {"human": "H2", "machine": "M4", "readability": "R3"}
assert root["root_vector_before"] == root["root_vector_after"] == ["H2", "M3", "R3"]
assert root["kernel_closed"] is validation["root_decision"]["kernel_closed"] is False
assert root["audit_complete"] is validation["result"]["audit_complete"] is False
assert root["theorem_complete"] is validation["result"]["theorem_complete"] is False
assert root["remaining_root_cut_set"] == graphs["closure_boundary"]["remaining_root_cut_set"]
assert root["remaining_root_cut_set"] == ["M0107-L-FINITE", "M0107-L-INTEGRAL-TO-FINITE"]
assert graphs["closure_boundary"]["root_machine_debt"] == "M3"

assert decision["terminal_decisions"] == {
    "audit_z": "not_accepted",
    "theorem_z": "not_accepted",
    "release": "blocked",
    "worker_item_selftest": "pass",
}
assert decision["accepted_receipt_ids"] == []
assert decision["first_failed_gate"]["gate_id"] == "workflow.validation_master_acceptance"
assert decision["first_failed_theorem_gate"]["gate_id"] == "proof.root_kernel_closure"
assert decision["failed_gates"][0] == decision["first_failed_gate"]["gate_id"]
assert "workflow.release_master_acceptance" in decision["failed_gates"]

print("release reconciliation ok: provisional validation receipt and frozen root agree")
print("release blocked: validation is unaccepted and exact root remains M3")
print("AUDIT-Z=false; THEOREM-Z=false; accepted receipt ids=[]")
