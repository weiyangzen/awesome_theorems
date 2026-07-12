#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


validation = subprocess.run(
    ["python3", str(HERE / "check_validation.py")],
    cwd=ROOT,
    check=True,
    text=True,
    capture_output=True,
)
assert "ok: exact statement" in validation.stdout
assert "blocked: cold empty-cache hermetic replay" in validation.stdout

decision = load("release-decision.json")
receipt = load("validation-receipt.json")
graphs = load("typed-graphs.json")
intake = load("intake.json")
task_dag = load("task-dag.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))

assert decision["item_id"] == "S56-M-1131-RELEASE"
assert decision["theorem_id"] == "THM-M-1131"
assert decision["decision"]["verdict"] == "blocked"
assert decision["decision"]["lifecycle_before"] == intake["lifecycle_mode"] == "planned"
assert decision["decision"]["lifecycle_after"] == "planned"
assert decision["decision"]["root_vector_before"] == intake["root_vector"]
assert decision["decision"]["root_vector_after"] == intake["root_vector"]
assert decision["decision"]["audit_complete"] is False
assert decision["decision"]["theorem_complete"] is False
assert decision["decision"]["release_accepted"] is False
assert decision["decision"]["accepted_receipt_ids"] == []

assert receipt["receipt_id"] == decision["evaluated_snapshot"]["validation_receipt_id"]
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["release_grade"] is False
assert receipt["result"]["audit_complete"] is False
assert receipt["result"]["theorem_complete"] is False
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False

states = {node["id"]: node["state"] for node in task_dag["nodes"]}
assert states["S56-M-1131-VALIDATION"] != "accepted"
assert states["S56-M-1131-RELEASE"] == "open"
assert decision["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
failed = {gate["gate_id"] for gate in decision["failed_gates"]}
assert {
    "S56-10.2-DEPENDENCY-ACCEPTANCE",
    "S56-H0-SOURCE",
    "S56-R0-RECONSTRUCTION",
    "S56-10.6-HERMETIC-COLD-BUILD",
    "S56-10.7-INDEPENDENT-VERIFICATION",
    "S56-10.4-MASTER-ACCEPTANCE",
}.issubset(failed)

entries = targets["targets"] if isinstance(targets, dict) else targets
target = next(entry for entry in entries if entry["theorem_id"] == "THM-M-1131")
assert target["execution_rank"] == 336
assert target["baseline"] == "L0"
assert target["rework_required"] is True
assert target["theorem_complete"] is False

print("ok: narrow Lean validation replayed against the pinned existing environment")
print("ok: release decision agrees with provisional receipt, open authoritative graph, and target manifest")
print("blocked: theorem completion is false; prerequisite acceptance and all listed release gates remain open")
