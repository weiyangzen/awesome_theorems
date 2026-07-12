#!/usr/bin/env python3
"""Validate the scoped THM-M-1407 planned-intake invariants."""

from __future__ import annotations

import json
from pathlib import Path


TARGET_ID = "THM-M-1407"
ITEM_ID = "S56-M-1407-INTAKE"
RANK = 906
OWNED_FILES = {
    "README.md",
    "instance.json",
    "scope-map.md",
    "source-statement-crosswalk.md",
    "task-dag.json",
    "IntakeProbe.lean",
    "check_intake.py",
    "validation.md",
    "intake-receipt.json",
}
TASK_SUFFIXES = [
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
]


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    target_dir = Path(__file__).resolve().parent
    root = target_dir.parents[1]
    instance = load(target_dir / "instance.json")
    task_dag = load(target_dir / "task-dag.json")
    receipt = load(target_dir / "intake-receipt.json")
    manifest = load(root / "Docs/Stage1_Targets_rev-5.6.json")
    execution_dag = load(root / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert isinstance(instance, dict)
    assert instance["theorem_id"] == TARGET_ID
    assert instance["item_id"] == ITEM_ID
    assert instance["execution_rank"] == RANK
    assert instance["lifecycle"] == "planned"
    assert instance["intent"] == "intake"
    assert instance["baseline"] == "L0"
    assert instance["rework_required"] is True
    assert instance["legacy_artifacts_accepted"] is False
    assert instance["canonical_claim"] is None
    assert instance["canonical_formal_target"]["declaration_or_expression"] is None
    assert instance["canonical_formal_target"]["elaborated_expression_hash"] is None
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H4", "M": "M4", "R": "R4"}
    assert instance["audit_complete"] is False
    assert instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == []
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    assert {path.name for path in target_dir.iterdir() if path.is_file()} == OWNED_FILES

    assert isinstance(task_dag, dict)
    assert task_dag["theorem_id"] == TARGET_ID
    assert task_dag["lifecycle"] == "planned"
    assert task_dag["accepted_states"] == []
    tasks = task_dag["tasks"]
    assert [task["id"] for task in tasks] == [
        f"S56-M-1407-{suffix}" for suffix in TASK_SUFFIXES
    ]
    expected_dependency = ITEM_ID
    for task in tasks:
        assert task["state"] == "open"
        assert task["depends_on"] == [expected_dependency]
        expected_dependency = task["id"]

    assert isinstance(manifest, dict)
    manifest_targets = manifest.get("targets", manifest)
    if isinstance(manifest_targets, dict):
        manifest_targets = list(manifest_targets.values())
    target = next(row for row in manifest_targets if row["theorem_id"] == TARGET_ID)
    assert target["execution_rank"] == RANK
    assert target["lifecycle_mode"] == "planned"
    assert target["baseline"] == "L0"
    assert target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert target["theorem_complete"] is False

    assert isinstance(execution_dag, dict)
    dag_nodes = execution_dag.get("items", execution_dag.get("nodes", execution_dag))
    if isinstance(dag_nodes, dict):
        dag_nodes = list(dag_nodes.values())
    node = next(row for row in dag_nodes if row["id"] == ITEM_ID)
    assert node["theorem_id"] == TARGET_ID
    assert node["execution_rank"] == RANK
    assert node["phase"] == "intake"
    assert node["layer"] == 0
    assert node["state"] == "[ ]"
    assert node["depends_on"] == []
    assert node["owned_paths"] == [f"Stage1_Instances/{TARGET_ID}"]

    assert isinstance(receipt, dict)
    assert receipt["item_id"] == ITEM_ID
    assert receipt["theorem_id"] == TARGET_ID
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is False
    assert receipt["audit_complete"] is False
    assert receipt["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in tasks]

    for path in target_dir.iterdir():
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        assert content.endswith("\n"), f"missing final newline: {path.name}"
        for number, line in enumerate(content.splitlines(), start=1):
            assert line.rstrip(" \t") == line, f"trailing whitespace: {path.name}:{number}"

    print("intake invariant check: ok")


if __name__ == "__main__":
    main()
