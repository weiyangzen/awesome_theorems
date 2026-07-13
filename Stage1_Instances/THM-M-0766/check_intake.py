#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0766 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0766"
ITEM_ID = "S56-M-0766-INTAKE"
RANK = 1352
BASE_REVISION = "fd0fab2ab7f4f514a5cc625bbce92879e718ba13"
BASE_TREE = "4116d53bcf2573069e4b67205353fe3469dbe7bd"
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
SOURCE_INPUTS = [
    "Docs/Stage1_Targets_rev-5.6.json",
    "Docs/Stage1_Blueprint_rev-5.6.md",
    "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "skills/execute-stage1-rev56/SKILL.md",
    "Docs/Blueprint_Guidelines.md",
    "Docs/researches/math_theorems.md",
    "Docs/researches/cs_theorems.md",
    "Docs/Stage0_Blueprint.md",
    "Formalizations/Lean/lean-toolchain",
    "Formalizations/Lean/lake-manifest.json",
]


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    value: dict[str, object] = {}
    for key, item in pairs:
        assert key not in value, f"duplicate JSON key: {key}"
        value[key] = item
    return value


def load(path: Path) -> dict:
    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys
    )
    assert isinstance(value, dict), f"{path.name} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_text_file(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path.name}"
    assert b"\r" not in data, f"carriage return: {path.name}"
    assert b"\x00" not in data, f"NUL byte: {path.name}"
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
        f"trailing whitespace: {path.name}"
    )


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path)
    check_text_file(path)
    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["item_id"] == ITEM_ID
    assert packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution_dag = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert receipt["schema_version"] == "stage1-worker-intake-receipt/1.0"

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    item = next(row for row in execution_dag["items"] if row["id"] == ITEM_ID)

    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "线性有界自动机"
    assert target["category"] == instance["category"] == "数理逻辑 / 递归论"
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."

    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert dag["normative_profile"] == instance["normative_profile"]
    assert dag["audit_complete"] is False
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None

    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == [] and instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    expected_tasks = []
    dependency = ITEM_ID
    for suffix in TASK_SUFFIXES:
        task_id = f"S56-M-0766-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])
    assert all(task["evidence_ids"] == [] for task in dag["tasks"])
    assert [task["layer"] for task in dag["tasks"]] == list(range(1, 7))
    source_items = {row["id"]: row for row in execution_dag["items"]}
    for task in dag["tasks"]:
        source = source_items[task["id"]]
        for key in ("phase", "layer", "owned_paths", "deliverable", "completion_gate"):
            assert task[key] == source[key], f"task field mismatch: {task['id']} {key}"

    actual_entries = {path.name for path in HERE.iterdir()}
    assert actual_entries == OWNED_FILES, f"unexpected owned entry: {sorted(actual_entries ^ OWNED_FILES)}"
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is False and receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["selftest_result"] == "pass"
    assert receipt["covered_node_ids"] == [ITEM_ID]
    assert receipt["change_impact_set"] == [ITEM_ID]
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["root_vector_before"] == {
        "H": "unclassified",
        "M": "unclassified",
        "R": "unclassified",
    }
    assert receipt["known_failures"] and receipt["first_failed_gate"]

    for name, digest in receipt["untracked_owned_artifact_sha256"].items():
        assert name != "intake-receipt.json"
        assert digest == sha256(HERE / name), f"stale owned-artifact hash: {name}"
    assert set(receipt["untracked_owned_artifact_sha256"]) == OWNED_FILES - {"intake-receipt.json"}

    assert set(receipt["source_inputs"]) == set(SOURCE_INPUTS)
    for relative, tagged_digest in receipt["source_inputs"].items():
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}", f"stale source input: {relative}"

    assert instance["source_revisions"]["repository_base"] == BASE_REVISION
    assert instance["source_revisions"]["repository_base_tree"] == BASE_TREE
    assert instance["source_revisions"]["mathlib"] == receipt["worker_input_hashes"]["mathlib_revision"]
    assert instance["source_revisions"]["mathlib_tree"] == receipt["worker_input_hashes"]["mathlib_tree"]

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    for path in HERE.iterdir():
        if path.is_file():
            check_text_file(path)

    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)
        assert receipt["worker_packet_sha256"] == sha256(args.worker_packet)

    print("intake invariant check: ok (THM-M-0766 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
