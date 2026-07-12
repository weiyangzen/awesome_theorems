#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0227 planned intake."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0227"
ITEM_ID = "S56-M-0227-INTAKE"
RANK = 939
BASE_REVISION = "dd8846dbc83818f6ba7124151d5d4b7b29bb5b0d"
BASE_TREE = "1bf3680085cf7338ac4d405cf4ef2188fa14ccec"
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
    assert isinstance(value, dict), f"{path.name} must contain a JSON object"
    return value


def main() -> None:
    manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution_dag = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")
    selftest = load(ROOT / ".stage1-worker-selftest.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    item = next(row for row in execution_dag["items"] if row["id"] == ITEM_ID)

    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "黎曼映射定理"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 110
    assert (
        target["lifecycle_mode"]
        == instance["lifecycle_mode"]
        == dag["lifecycle_mode"]
        == "planned"
    )
    assert (
        target["theorem_complete"]
        is instance["theorem_complete"]
        is dag["theorem_complete"]
        is False
    )
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"

    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert (
        instance["theorem_id"]
        == dag["theorem_id"]
        == receipt["theorem_id"]
        == selftest["theorem_id"]
        == THEOREM_ID
    )
    assert instance["item_id"] == receipt["item_id"] == selftest["item_id"] == ITEM_ID
    assert instance["intent"] == receipt["intent"] == selftest["intent"] == "intake"
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None

    formal = instance["canonical_formal_target"]
    for key in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == []
    assert all(form["checked_witness"] is None for form in instance["alternate_encodings"])
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R3"}
    assert (
        instance["accepted_proof_state"]
        == instance["accepted_receipt_ids"]
        == dag["accepted_states"]
        == []
    )
    assert (
        instance["audit_complete"]
        is receipt["audit_complete"]
        is selftest["audit_complete"]
        is False
    )
    assert (
        instance["theorem_complete"]
        is receipt["theorem_complete"]
        is selftest["theorem_complete"]
        is False
    )

    expected_tasks = []
    dependency = ITEM_ID
    for suffix in TASK_SUFFIXES:
        task_id = f"S56-M-0227-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    actual_artifacts = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual_artifacts == OWNED_FILES
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == set(selftest["changed_paths"]) == expected_changed
    assert receipt["proposed_state"] == selftest["state"] == "[_]"
    assert receipt["accepted"] is False and receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == selftest["accepted_receipt_ids"] == []
    assert receipt["proof_body_locations"] == selftest["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["base_revision"] == selftest["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == selftest["base_tree"] == BASE_TREE
    assert receipt["receipt_id"] == selftest["receipt_id"]

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data, f"non-LF newline: {path.name}"
        assert b"\x00" not in data, f"NUL byte: {path.name}"
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"trailing whitespace: {path.name}"
        )

    for name in (
        "README.md",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "validation.md",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    lean_probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "opaque ", "unsafe ")
    assert all(token not in lean_probe for token in prohibited)

    selftest_data = (ROOT / ".stage1-worker-selftest.json").read_bytes()
    assert (
        selftest_data.endswith(b"\n")
        and b"\r" not in selftest_data
        and b"\x00" not in selftest_data
    )

    print("intake invariant check: ok (THM-M-0227 planned; H1/M4/R3; six open tasks)")


if __name__ == "__main__":
    main()
