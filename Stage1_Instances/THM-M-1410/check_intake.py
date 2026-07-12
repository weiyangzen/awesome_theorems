#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-1410."""

import hashlib
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
ROOT = Path(__file__).resolve().parent
THEOREM_ID = "THM-M-1410"
ITEM_ID = "S56-M-1410-INTAKE"
BASE_REVISION = "95073b656f2c285c788e4814325a47fdb4dc1879"
BASE_TREE = "54d91dc1ea3d413402cc921ad61f7b5ebaaedd13"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def find_target(value):
    if isinstance(value, dict):
        if value.get("theorem_id") == THEOREM_ID:
            return value
        for child in value.values():
            found = find_target(child)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = find_target(child)
            if found is not None:
                return found
    return None


def find_dag_items(value):
    if isinstance(value, dict):
        items = value.get("items")
        if isinstance(items, list):
            return [item for item in items if item.get("theorem_id") == THEOREM_ID]
        for child in value.values():
            found = find_dag_items(child)
            if found:
                return found
    elif isinstance(value, list):
        for child in value:
            found = find_dag_items(child)
            if found:
                return found
    return []


instance = json.loads((ROOT / "instance.json").read_text(encoding="utf-8"))
dag = json.loads((ROOT / "task-dag.json").read_text(encoding="utf-8"))
receipt = json.loads((ROOT / "intake-receipt.json").read_text(encoding="utf-8"))
selftest = json.loads((REPO / ".stage1-worker-selftest.json").read_text(encoding="utf-8"))
manifest = json.loads((REPO / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))
execution_dag = json.loads(
    (REPO / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text(encoding="utf-8")
)
target = find_target(manifest)
authoritative_tasks = sorted(find_dag_items(execution_dag), key=lambda item: item["layer"])

assert target is not None
assert target["execution_rank"] == 909
assert target["name"] == "Rokhlin\u5854"
assert target["baseline"] == "L0" and target["rework_required"] is True
assert target["legacy_artifacts_accepted"] is False
assert target["target_lane"] == "hard_statement_first_partial_verification"
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

assert instance["theorem_id"] == target["theorem_id"] == THEOREM_ID
assert instance["item_id"] == selftest["item_id"] == receipt["item_id"] == ITEM_ID
assert instance["execution_rank"] == 909
assert instance["lifecycle"] == "planned" and instance["intent"] == "intake"
assert instance["baseline"] == "L0" and instance["rework_required"] is True
assert instance["canonical_claim"] is None

formal = instance["canonical_formal_target"]
assert formal["module"] is None and formal["declaration_or_expression"] is None
assert formal["elaborated_expression_hash"] is None
assert formal["environment_fingerprint"] is None
assert instance["quantifiers"] == [] and instance["hypotheses"] == []
assert instance["alternate_encodings"] == []
assert instance["obligation_registry_hash"] is None
assert instance["discovery_protocol_hash"] is None
assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
assert instance["root_vector_status"] == "proposed_pending_master_acceptance"
assert "literal repository" in instance["human_debt_scope"]
assert "recompute H" in instance["target_decision"]
assert instance["accepted_proof_state"] == []
assert instance["audit_complete"] is False and instance["theorem_complete"] is False

assert dag["theorem_id"] == THEOREM_ID and dag["lifecycle"] == "planned"
assert dag["authority"] == "target_scoped_projection_only"
assert dag["authoritative_dag"] == "Docs/Stage1_Execution_DAG_rev-5.6.json"
assert dag["accepted_states"] == []
expected_tasks = [
    (ITEM_ID, []),
    ("S56-M-1410-STATEMENT", [ITEM_ID]),
    ("S56-M-1410-ANCHOR_AUDIT", ["S56-M-1410-STATEMENT"]),
    ("S56-M-1410-OBLIGATION_TREE", ["S56-M-1410-ANCHOR_AUDIT"]),
    ("S56-M-1410-PROOF", ["S56-M-1410-OBLIGATION_TREE"]),
    ("S56-M-1410-VALIDATION", ["S56-M-1410-PROOF"]),
    ("S56-M-1410-RELEASE", ["S56-M-1410-VALIDATION"]),
]
assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
assert dag["tasks"][0]["state"] == "worker_selftested_pending_master"
assert all(task["state"] == "open" for task in dag["tasks"][1:])
assert all(task["authoritative_state"] == "[ ]" for task in dag["tasks"])

projection_fields = (
    "id",
    "theorem_id",
    "phase",
    "layer",
    "depends_on",
    "owned_paths",
    "deliverable",
    "completion_gate",
)
assert len(authoritative_tasks) == len(dag["tasks"]) == 7
for projected, authoritative in zip(dag["tasks"], authoritative_tasks, strict=True):
    assert {key: projected[key] for key in projection_fields} == {
        key: authoritative[key] for key in projection_fields
    }
    assert projected["authoritative_state"] == authoritative["state"] == "[ ]"

catalog = (REPO / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
assert "**Rokhlin\u5854**" in catalog
assert "- \u9648\u8ff0: \u904d\u5386\u7406\u8bba\u7684\u5de5\u5177" in catalog
stage0 = (REPO / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
assert "THM-M-1410 Rokhlin\u5854" in stage0
assert "- \u7cbe\u786e\u5b9a\u4e49\u4e0e\u524d\u63d0\u6761\u4ef6: \u5f85\u8865\u5145" in stage0

actual_artifacts = sorted(path.name for path in ROOT.iterdir() if path.is_file())
assert actual_artifacts == sorted(instance["owned_artifacts"])
assert sorted(receipt["changed_paths"]) == sorted(
    [f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_artifacts]
    + [".stage1-worker-selftest.json"]
)
declared_target_paths = sorted(
    path for path in selftest["changed_paths"] if path.startswith(f"Stage1_Instances/{THEOREM_ID}/")
)
assert declared_target_paths == sorted(
    f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_artifacts
)

assert selftest["state"] == "[_]" and selftest["base_revision"] == BASE_REVISION
assert receipt["theorem_id"] == THEOREM_ID and receipt["base_revision"] == BASE_REVISION
assert receipt["base_tree"] == BASE_TREE
assert receipt["proposed_state"] == "[_]" and receipt["master_acceptance"] is False
assert receipt["intent"] == "intake" and receipt["verdict"] == "no_state_change"
assert receipt["result"] == "pass" and receipt["theorem_complete"] is False
assert receipt["accepted_proof_state"] == [] and receipt["accepted_receipt_ids"] == []
assert receipt["first_failed_gate"] == "S56-M-1410-INTAKE master acceptance"
assert instance["source_revisions"]["repository_base"] == BASE_REVISION

for relative, expected_hash in receipt["input_bindings"].items():
    if relative == "preexisting_Formalizations/Lean/.lake_symlink_target_text":
        link = REPO / "Formalizations/Lean/.lake"
        actual_hash = hashlib.sha256(link.readlink().as_posix().encode()).hexdigest()
    else:
        actual_hash = sha256(REPO / relative)
    assert actual_hash == expected_hash, relative

pre_receipt_paths = [
    "Stage1_Instances/THM-M-1410/README.md",
    "Stage1_Instances/THM-M-1410/instance.json",
    "Stage1_Instances/THM-M-1410/scope-map.md",
    "Stage1_Instances/THM-M-1410/source-statement-crosswalk.md",
    "Stage1_Instances/THM-M-1410/task-dag.json",
    "Stage1_Instances/THM-M-1410/IntakeProbe.lean",
    "Stage1_Instances/THM-M-1410/check_intake.py",
]
assert list(receipt["artifact_hashes_pre_receipt"]) == pre_receipt_paths
manifest = ""
for relative in pre_receipt_paths:
    actual_hash = sha256(REPO / relative)
    assert actual_hash == receipt["artifact_hashes_pre_receipt"][relative], relative
    manifest += f"{actual_hash}  {relative}\n"
assert hashlib.sha256(manifest.encode()).hexdigest() == receipt["pre_receipt_artifact_manifest_sha256"]
for relative, expected_hash in selftest["artifact_hashes"].items():
    assert sha256(REPO / relative) == expected_hash, relative

print("THM-M-1410 intake invariant check: ok")
