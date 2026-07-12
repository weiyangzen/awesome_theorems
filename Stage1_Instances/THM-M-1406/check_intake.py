#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-1406"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


target_data = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
targets = target_data if isinstance(target_data, list) else target_data["targets"]
target = next(item for item in targets if item["theorem_id"] == "THM-M-1406")
execution_dag = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
execution_items = execution_dag if isinstance(execution_dag, list) else execution_dag["items"]
intake_item = next(item for item in execution_items if item["id"] == "S56-M-1406-INTAKE")
instance = load(OWNED / "instance.json")
dag = load(OWNED / "task-dag.json")
receipt = load(OWNED / "intake-receipt.json")

assert target["execution_rank"] == instance["execution_rank"] == intake_item["execution_rank"] == 905
assert target["baseline"] == instance["baseline"] == "L0"
assert target["rework_required"] is instance["rework_required"] is True
assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
assert receipt["lifecycle_mode"] == "planned"
assert target["theorem_complete"] is instance["theorem_complete"] is False
assert intake_item["phase"] == instance["intent"] == receipt["intent"] == "intake"
assert intake_item["depends_on"] == []
assert intake_item["owned_paths"] == ["Stage1_Instances/THM-M-1406"]
assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == "THM-M-1406"
assert instance["item_id"] == receipt["item_id"] == "S56-M-1406-INTAKE"
assert instance["canonical_statement"] is None
assert instance["canonical_formal_target"]["module"] is None
assert instance["canonical_formal_target"]["declaration_or_expression"] is None
assert instance["canonical_formal_target"]["elaborated_expression_hash"] is None
assert instance["canonical_formal_target"]["environment_fingerprint"] is None
assert instance["excluded_degenerate_cases"] == []
assert instance["excluded_degenerate_case_policy"].startswith(
    "No boundary case is excluded at intake."
)
assert instance["degenerate_cases_to_resolve"]
assert instance["root_vector"] == {"human": "H5", "machine": "M4", "readability": "R4"}
assert receipt["root_vector_after"] == instance["root_vector"]
assert instance["audit_complete"] is receipt["audit_complete"] is False
assert instance["theorem_complete"] is receipt["theorem_complete"] is False
assert instance["accepted_proof_state"] == dag["accepted_states"] == []

expected_tasks = [
    ("S56-M-1406-STATEMENT", ["S56-M-1406-INTAKE"]),
    ("S56-M-1406-ANCHOR_AUDIT", ["S56-M-1406-STATEMENT"]),
    ("S56-M-1406-OBLIGATION_TREE", ["S56-M-1406-ANCHOR_AUDIT"]),
    ("S56-M-1406-PROOF", ["S56-M-1406-OBLIGATION_TREE"]),
    ("S56-M-1406-VALIDATION", ["S56-M-1406-PROOF"]),
    ("S56-M-1406-RELEASE", ["S56-M-1406-VALIDATION"]),
]
assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
assert all(task["state"] == "open" for task in dag["tasks"])

owned_files = sorted(path.name for path in OWNED.iterdir() if path.is_file())
assert sorted(instance["owned_artifacts"]) == owned_files
hashed_files = [name for name in owned_files if name != "intake-receipt.json"]
assert sorted(receipt["untracked_owned_artifact_sha256"]) == sorted(hashed_files)
for name in hashed_files:
    digest = hashlib.sha256((OWNED / name).read_bytes()).hexdigest()
    assert receipt["untracked_owned_artifact_sha256"][name] == digest, (
        f"owned artifact hash mismatch: {name}"
    )
for path in OWNED.iterdir():
    if not path.is_file():
        continue
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path.name}"
    assert b"\r" not in data, f"non-LF newline: {path.name}"
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
        f"trailing whitespace: {path.name}"
    )

base = "3d1d6d3eb018f17657cae1cfd7d25fc30492a12b"
tree = "3aa3dd324b35549da6cf2c5a54183a63ed1bfff9"
assert receipt["base_revision"] == instance["source_revisions"]["repository_base"] == base
assert receipt["base_tree"] == instance["source_revisions"]["repository_tree"] == tree
assert instance["source_revisions"]["mathlib"] == (
    "8a178386ffc0f5fef0b77738bb5449d50efeea95"
)
assert receipt["selftest_result"] == "pass" and receipt["accepted"] is False
assert receipt["content_addressed"] is False
assert receipt["covered_node_ids"] == ["S56-M-1406-INTAKE"]
assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
assert receipt["validation_started_at"] <= receipt["validation_completed_at"]
assert receipt["validated_at"] == receipt["validation_completed_at"]
assert receipt["commands_and_results"]
for command in receipt["commands_and_results"]:
    assert isinstance(command["argv"], list) and command["argv"]
    assert all(isinstance(arg, str) and arg for arg in command["argv"])
    assert isinstance(command["exit_code"], int)
    assert command["result"]
    assert "command" not in command

selftest_path = ROOT / ".stage1-worker-selftest.json"
if selftest_path.exists():
    selftest = load(selftest_path)
    assert selftest["item_id"] == "S56-M-1406-INTAKE"
    assert selftest["base_revision"] == base
    assert selftest["state"] == "[_]"
    assert selftest["commands"]
    for command in selftest["commands"]:
        assert isinstance(command["argv"], list) and command["argv"]
        assert all(isinstance(arg, str) and arg for arg in command["argv"])
        assert isinstance(command["exit_code"], int)
        assert command["result"]
    changed_paths = set(selftest["changed_paths"])
    expected_paths = {f"Stage1_Instances/THM-M-1406/{name}" for name in owned_files}
    expected_paths.add(".stage1-worker-selftest.json")
    assert changed_paths == expected_paths
    data = selftest_path.read_bytes()
    assert data.endswith(b"\n")
    assert b"\r" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

print("intake invariant check: ok")
