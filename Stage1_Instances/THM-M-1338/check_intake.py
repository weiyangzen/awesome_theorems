#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-1338"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


target_data = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
targets = target_data if isinstance(target_data, list) else target_data["targets"]
target = next(item for item in targets if item["theorem_id"] == "THM-M-1338")
instance = load(OWNED / "instance.json")
dag = load(OWNED / "task-dag.json")
receipt = load(OWNED / "intake-receipt.json")

assert target["execution_rank"] == instance["execution_rank"] == 949
assert target["baseline"] == instance["baseline"] == "L0"
assert target["rework_required"] is instance["rework_required"] is True
assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == "THM-M-1338"
assert instance["item_id"] == receipt["item_id"] == "S56-M-1338-INTAKE"
assert instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
assert instance["intent"] == receipt["intent"] == "intake"
assert instance["canonical_statement"] is None
assert instance["canonical_formal_target"]["declaration_or_expression"] is None
assert instance["canonical_formal_target"]["elaborated_expression_hash"] is None
assert instance["obligation_registry_hash"] is None
assert instance["discovery_protocol_hash"] is None
assert instance["root_vector"] == {"human": "H1", "machine": "M4", "readability": "R4"}
assert receipt["root_vector_after"] == instance["root_vector"]
assert instance["audit_complete"] is receipt["audit_complete"] is False
assert instance["theorem_complete"] is receipt["theorem_complete"] is False
assert instance["accepted_proof_state"] == [] and dag["accepted_states"] == []

expected_tasks = [
    ("S56-M-1338-STATEMENT", ["S56-M-1338-INTAKE"]),
    ("S56-M-1338-ANCHOR_AUDIT", ["S56-M-1338-STATEMENT"]),
    ("S56-M-1338-OBLIGATION_TREE", ["S56-M-1338-ANCHOR_AUDIT"]),
    ("S56-M-1338-PROOF", ["S56-M-1338-OBLIGATION_TREE"]),
    ("S56-M-1338-VALIDATION", ["S56-M-1338-PROOF"]),
    ("S56-M-1338-RELEASE", ["S56-M-1338-VALIDATION"]),
]
assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
assert all(task["state"] == "open" for task in dag["tasks"])
assert receipt["remaining_root_cut_set"] == [task_id for task_id, _ in expected_tasks]

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

base = "85da7777da7cc5104d4bc4eaa1d947b8137ca5f5"
assert receipt["base_revision"] == instance["source_revisions"]["repository_base"] == base
assert receipt["base_tree"] == instance["source_revisions"]["repository_tree"] == (
    "ae4ad4de219b61476e1ed10c008e8139247b9d77"
)
assert instance["source_revisions"]["mathlib"] == (
    "8a178386ffc0f5fef0b77738bb5449d50efeea95"
)
assert receipt["selftest_result"] == "pass" and receipt["accepted"] is False
assert receipt["content_addressed"] is False
assert receipt["covered_node_ids"] == ["S56-M-1338-INTAKE"]
assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
assert receipt["content_addressed_recipe_ids"] == receipt["content_addressed_receipt_ids"] == []

selftest_path = ROOT / ".stage1-worker-selftest.json"
if selftest_path.exists():
    selftest = load(selftest_path)
    assert selftest["item_id"] == "S56-M-1338-INTAKE"
    assert selftest["base_revision"] == base
    assert selftest["state"] == "[_]"
    changed_paths = set(selftest["changed_paths"])
    expected_paths = {f"Stage1_Instances/THM-M-1338/{name}" for name in owned_files}
    expected_paths.add(".stage1-worker-selftest.json")
    assert changed_paths == expected_paths

print("intake invariant check: ok")
