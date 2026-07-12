#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-0772 release decision."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0772"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def sha256(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
instance = load("instance.json")
dag = load("task-dag.json")
graphs = load("typed-graphs.json")
proof = load("proof-receipt.json")
validation = load("validation-receipt.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))

target = next(entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-0772")
assert target["execution_rank"] == 580
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

assert decision["item_id"] == "S56-M-0772-RELEASE"
assert decision["theorem_id"] == instance["theorem_id"] == validation["theorem_id"]
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == instance["lifecycle"] == "planned"
assert decision["root_vector_before"] == decision["root_vector_after"] == instance["root_vector"]
assert decision["accepted_receipt_ids"] == dag["accepted_states"] == []

tasks = {task["id"]: task for task in dag["tasks"]}
assert tasks["S56-M-0772-VALIDATION"]["state"] == "open"
assert tasks["S56-M-0772-RELEASE"]["state"] == "open"
dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0772-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == sha256("validation-receipt.json")
assert dependency["master_accepted"] is False
assert validation["support_state"] == "provisional_worker_selftest"
assert validation["release_grade"] is False
assert proof["state"] == "provisional_worker_selftest"

terminal = decision["terminal_decisions"]
assert terminal["audit_complete"] is instance["audit_complete"] is False
assert terminal["theorem_complete"] is instance["theorem_complete"] is False
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False
assert validation["result"]["audit_complete"] is False
assert validation["result"]["theorem_complete"] is False
assert validation["result"]["hermetic_release_gate"] == "fail_closed"
assert validation["result"]["independent_distinct_runner_gate"] == "fail_closed"

assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
required = (
    "structured reconciliation",
    "H0 primary-source",
    "R0 anchored",
    "transitive declaration, axiom, provenance, trust, and TCB",
    "empty-cache network-denied cold build",
    "SBOM, license",
    "two signed attestations",
    "minimal release verifier",
    "deterministic content-addressed evidence bundle",
)
cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in required:
    assert fragment in cut_set, fragment

for key in (
    "authoritative_dependency_acceptance",
    "authoritative_graph_reconciliation",
    "human_source_acceptance",
    "readability_acceptance",
    "hermetic_release_reproduction",
    "supply_chain_archive",
    "independent_release_verification",
    "deterministic_release_bundle",
    "master_acceptance",
):
    assert decision["evidence_reconciliation"][key] == "missing"

print("release-decision: ok (blocked; validation unaccepted and non-release)")
print("release-decision: ok (lifecycle/root vector/terminal decisions not promoted)")
print("release-decision: blocked at dependency acceptance; hermetic and independent gates remain open")
