#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1408 planned intake."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{name} must contain an object"
    return value


instance = load("instance.json")
dag = load("task-dag.json")
manifest = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))
targets = manifest["targets"] if isinstance(manifest, dict) else manifest
target = next(row for row in targets if row["theorem_id"] == "THM-M-1408")

assert target["execution_rank"] == 907
assert target["baseline"] == "L0" and target["rework_required"] is True
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
assert target["legacy_artifacts_accepted"] is False

assert instance["schema_version"] == "stage1-instance-intake/1.0"
assert instance["item_id"] == "S56-M-1408-INTAKE"
assert instance["theorem_id"] == dag["theorem_id"] == "THM-M-1408"
assert instance["execution_rank"] == 907
assert instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
assert instance["baseline"] == "L0" and instance["rework_required"] is True
assert instance["canonical_statement"] is None
formal_target = instance["canonical_formal_target"]
assert formal_target["module"] is None
assert formal_target["declaration_or_expression"] is None
assert formal_target["elaborated_expression_hash"] is None
assert formal_target["environment_fingerprint"] is None
assert instance["obligation_registry_hash"] is None
assert instance["discovery_protocol_hash"] is None
assert instance["root_vector"] == {"human": "H1", "machine": "M4", "readability": "R3"}
assert instance["accepted_proof_state"] == []
assert instance["accepted_receipt_ids"] == []
assert instance["audit_complete"] is False
assert instance["theorem_complete"] is False

expected_tasks = [
    "S56-M-1408-STATEMENT",
    "S56-M-1408-ANCHOR_AUDIT",
    "S56-M-1408-OBLIGATION_TREE",
    "S56-M-1408-PROOF",
    "S56-M-1408-VALIDATION",
    "S56-M-1408-RELEASE",
]
assert dag["accepted_states"] == []
assert dag["theorem_complete"] is False
assert [task["id"] for task in dag["tasks"]] == expected_tasks
assert all(task["state"] == "open" for task in dag["tasks"])
expected_dependency = "S56-M-1408-INTAKE"
for task in dag["tasks"]:
    assert task["depends_on"] == [expected_dependency]
    expected_dependency = task["id"]

artifact_names = set(instance["owned_artifacts"])
assert artifact_names == {path.name for path in HERE.iterdir() if path.is_file()}
for relative in instance["public_merge_targets"]:
    assert relative.startswith("Stage1_Instances/THM-M-1408/")
    assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
    text = (HERE / name).read_text(encoding="utf-8")
    assert "/home/" not in text and ".cron/" not in text
    assert "theorem_complete=true" not in text

print("check_intake: ok (THM-M-1408 planned; H1/M4/R3; six open tasks; no completion claim)")

