#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0133-RELEASE."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0133"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text())


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
validation = load("validation-receipt.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")

assert decision["item_id"] == "S56-M-0133-RELEASE"
assert decision["theorem_id"] == "THM-M-0133"
assert decision["dependency"]["item_id"] == "S56-M-0133-VALIDATION"
assert decision["dependency"]["receipt_id"] == validation["receipt_id"]
assert decision["dependency"]["receipt_sha256"] == digest("validation-receipt.json")
assert validation["support_state"] == "provisional_worker_selftest"
assert validation["release_grade"] is False

root = decision["reconciled_root"]
assert registry["root_obligation_id"] == "M0133-ROOT"
assert root["machine_debt"] == validation["root_decision"]["machine_debt"] == "M2"
assert root["kernel_closed"] is validation["root_decision"]["kernel_closed"] is False
assert root["theorem_complete"] is validation["root_decision"]["theorem_complete"] is False
assert root["remaining_root_cut_set"] == graphs["closure_boundary"]["remaining_root_cut_set"]
assert root["remaining_root_cut_set"] == ["M0133-L-MOD", "M0133-L-LOWER"]
assert root["audit_complete"] is validation["result"]["audit_complete"] is False

terminal = decision["terminal_decisions"]
assert terminal == {
    "audit_z": "not_accepted",
    "theorem_z": "not_accepted",
    "release": "blocked",
    "worker_item_selftest": "pass",
}
assert decision["accepted_receipt_ids"] == []
assert decision["first_failed_gate"] == "proof.root_kernel_closure"
assert decision["failed_gates"][0] == decision["first_failed_gate"]
assert "workflow.master_acceptance" in decision["failed_gates"]

print("release reconciliation ok: validation receipt hash and frozen root state agree")
print("release blocked: exact FLT root remains M2 with two open cut obligations")
print("AUDIT-Z=false; THEOREM-Z=false; accepted receipt ids=[]")
