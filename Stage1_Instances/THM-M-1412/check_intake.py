#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1412 planned intake."""

from __future__ import annotations

import json
import shutil
from pathlib import Path


TARGET_ID = "THM-M-1412"
ITEM_ID = "S56-M-1412-INTAKE"
RANK = 911
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


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path.name} must contain an object"
    return value


def main() -> None:
    here = Path(__file__).resolve().parent
    root = here.parents[1]
    instance = load(here / "instance.json")
    dag = load(here / "task-dag.json")
    receipt = load(here / "intake-receipt.json")
    manifest = load(root / "Docs/Stage1_Targets_rev-5.6.json")
    execution_dag = load(root / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    targets = manifest["targets"]
    target = next(row for row in targets if row["theorem_id"] == TARGET_ID)
    assert target["execution_rank"] == RANK
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned"
    assert target["legacy_artifacts_accepted"] is False
    assert target["theorem_complete"] is False

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == TARGET_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["execution_rank"] == RANK
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == "intake"
    assert instance["baseline"] == "L0" and instance["rework_required"] is True
    assert instance["legacy_artifacts_accepted"] is False
    assert instance["canonical_statement"] is None
    assert instance["canonical_claim"] is None
    formal_target = instance["canonical_formal_target"]
    assert formal_target["module"] is None
    assert formal_target["declaration_or_expression"] is None
    assert formal_target["elaborated_expression_hash"] is None
    assert formal_target["environment_fingerprint"] is None
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is False
    assert instance["theorem_complete"] is False

    expected_tasks = [f"S56-M-1412-{suffix}" for suffix in TASK_SUFFIXES]
    assert dag["accepted_states"] == []
    assert dag["theorem_complete"] is False
    assert [task["id"] for task in dag["tasks"]] == expected_tasks
    expected_dependency = ITEM_ID
    for task in dag["tasks"]:
        assert task["state"] == "open"
        assert task["depends_on"] == [expected_dependency]
        expected_dependency = task["id"]

    dag_items = execution_dag["items"]
    node = next(row for row in dag_items if row["id"] == ITEM_ID)
    assert node["theorem_id"] == TARGET_ID
    assert node["execution_rank"] == RANK
    assert node["phase"] == "intake" and node["layer"] == 0
    assert node["depends_on"] == []
    assert node["owned_paths"] == [f"Stage1_Instances/{TARGET_ID}"]

    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is False
    assert receipt["audit_complete"] is False
    assert receipt["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == expected_tasks
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == []
    assert receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == []
    assert receipt["composition_certificates"] == []
    assert receipt["covered_node_ids"] == [ITEM_ID]
    assert receipt["selftest_result"] == "pass"

    assert set(instance["owned_artifacts"]) == OWNED_FILES
    assert {path.name for path in here.iterdir() if path.is_file()} == OWNED_FILES
    selftest = load(root / ".stage1-worker-selftest.json")
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{TARGET_ID}/{name}" for name in OWNED_FILES
    }
    assert selftest["item_id"] == ITEM_ID
    assert selftest["theorem_id"] == TARGET_ID
    assert selftest["state"] == "[_]"
    assert set(selftest["changed_paths"]) == set(receipt["changed_paths"]) == expected_changed
    pycache = here / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{TARGET_ID}/")
        assert (root / relative).is_file(), f"missing public merge target: {relative}"

    for path in here.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data, f"non-LF newline: {path.name}"
        for number, line in enumerate(data.splitlines(), start=1):
            assert not line.endswith((b" ", b"\t")), f"trailing whitespace: {path.name}:{number}"
        if path.suffix in {".md", ".json"}:
            text = data.decode("utf-8")
            assert "/home/" not in text and ".cron/" not in text
            assert "theorem_complete=true" not in text

    print("check_intake: ok (THM-M-1412 planned; H5/M4/R4; six open tasks; no completion claim)")


if __name__ == "__main__":
    main()
