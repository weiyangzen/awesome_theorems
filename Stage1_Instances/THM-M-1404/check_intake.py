#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-1404"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


target_data = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
targets = target_data if isinstance(target_data, list) else target_data["targets"]
target = next(item for item in targets if item["theorem_id"] == "THM-M-1404")
instance = load(OWNED / "instance.json")
dag = load(OWNED / "task-dag.json")
receipt = load(OWNED / "intake-receipt.json")

assert target["execution_rank"] == instance["execution_rank"] == 903
assert target["baseline"] == instance["baseline"] == "L0"
assert target["rework_required"] is instance["rework_required"] is True
assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == "THM-M-1404"
assert instance["item_id"] == receipt["item_id"] == "S56-M-1404-INTAKE"
assert instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
assert instance["intent"] == receipt["intent"] == "intake"
assert instance["canonical_statement"] is None
assert instance["canonical_formal_target"]["declaration_or_expression"] is None
assert instance["canonical_formal_target"]["elaborated_expression_hash"] is None
assert instance["root_vector"] == {"human": "H5", "machine": "M4", "readability": "R4"}
assert receipt["root_vector_after"] == {
    "human": instance["root_vector"]["human"],
    "machine": instance["root_vector"]["machine"],
    "readability": instance["root_vector"]["readability"],
}
assert instance["audit_complete"] is False and instance["theorem_complete"] is False
assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
assert instance["accepted_proof_state"] == [] and dag["accepted_states"] == []

expected_tasks = [
    ("S56-M-1404-STATEMENT", ["S56-M-1404-INTAKE"]),
    ("S56-M-1404-ANCHOR_AUDIT", ["S56-M-1404-STATEMENT"]),
    ("S56-M-1404-OBLIGATION_TREE", ["S56-M-1404-ANCHOR_AUDIT"]),
    ("S56-M-1404-PROOF", ["S56-M-1404-OBLIGATION_TREE"]),
    ("S56-M-1404-VALIDATION", ["S56-M-1404-PROOF"]),
    ("S56-M-1404-RELEASE", ["S56-M-1404-VALIDATION"]),
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

base = "028e2535b68678b8296e63e2cacb05ed9775a2d8"
assert receipt["base_revision"] == base
assert instance["source_revisions"]["repository_base"] == base
assert instance["source_revisions"]["repository_tree"] == (
    "2845b046547e71984e5d93f4f04045663bd3bcbb"
)
assert instance["source_revisions"]["mathlib"] == (
    "8a178386ffc0f5fef0b77738bb5449d50efeea95"
)
assert receipt["selftest_result"] == "pass" and receipt["accepted"] is False
assert receipt["content_addressed"] is False
assert receipt["covered_node_ids"] == ["S56-M-1404-INTAKE"]
assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []

selftest_path = ROOT / ".stage1-worker-selftest.json"
if selftest_path.exists():
    selftest = load(selftest_path)
    assert selftest["item_id"] == "S56-M-1404-INTAKE"
    assert selftest["base_revision"] == base
    assert selftest["state"] == "[_]"
    changed_paths = set(selftest["changed_paths"])
    expected_paths = {f"Stage1_Instances/THM-M-1404/{name}" for name in owned_files}
    expected_paths.add(".stage1-worker-selftest.json")
    assert changed_paths == expected_paths

print("intake invariant check: ok")
