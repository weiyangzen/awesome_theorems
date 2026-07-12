#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-1269 release decision."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1269"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


decision = load(HERE / "release-decision.json")
intake = load(HERE / "intake.json")
graphs = load(HERE / "typed-graphs.json")
proof = load(HERE / "proof-receipt.json")
validation = load(HERE / "validation-receipt.json")
targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
dag = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

target = next(entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-1269")
assert target["execution_rank"] == 445
assert target["lifecycle_mode"] == "planned"
assert target["theorem_complete"] is False

assert decision["item_id"] == "S56-M-1269-RELEASE"
assert decision["theorem_id"] == intake["theorem_id"] == validation["theorem_id"]
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []
assert decision["terminal_decisions"]["audit_complete"] is False
assert decision["terminal_decisions"]["theorem_complete"] is False

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-1269-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
assert dependency["master_accepted"] is False
assert validation["support_state"] == proof["support_state"] == "provisional_worker_selftest"
assert validation["release_grade"] is False

tasks = {task["id"]: task for task in dag["items"]}
assert tasks["S56-M-1269-VALIDATION"]["state"] == "[_]"
assert tasks["S56-M-1269-RELEASE"]["state"] == "[ ]"

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["audit_complete"] is False
assert closure["theorem_complete"] is False
assert closure["remaining_root_cut_set"] == ["M1269-L-SINF"]
assert validation["result"]["authoritative_root_closed"] is False
assert validation["result"]["authoritative_root_cut_set"] == ["M1269-L-SINF"]
assert validation["result"]["theorem_complete"] is False

assert proof["result"]["root_machine_proof_body_present"] is True
assert proof["proof_body"]["classification"] == "local_wrapper_upstream_mathlib"
assert decision["root_vector"]["accepted_before"] == ["H2", "M3", "R3"]
assert decision["root_vector"]["accepted_after"] == ["H2", "M3", "R3"]
assert decision["root_vector"]["best_provisional_evidence"] == ["H2", "M0-W", "R3"]

assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert len(decision["remaining_root_cut_set"]) >= 10
for key in (
    "hermetic_release_reproduction",
    "independent_release_verification",
    "human_source_acceptance",
    "readability_acceptance",
    "deterministic_release_bundle",
):
    assert decision["evidence_reconciliation"][key] == "missing"

print("ok: release decision is bound to the current provisional validation receipt")
print("ok: exact-root evidence is recorded without promoting structured authority")
print("blocked: dependency acceptance, audit, hermetic, independent, and bundle gates remain open")
