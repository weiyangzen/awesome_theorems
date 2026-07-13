#!/usr/bin/env python3
"""Check the fail-closed THM-M-0758 planned-intake invariants."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0758"
ITEM_ID = "S56-M-0758-INTAKE"
RANK = 1344
BASE_REVISION = "d05520867fab3367a9b61b9544c3e12241204f54"
BASE_TREE = "fb2cfc62077d5b53e9938632cd6361dd60872067"
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
TASK_SUFFIXES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path.name} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
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

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)

    assert manifest["schema_version"] == "stage1-target-set/5.6.2"
    assert target["execution_rank"] == instance["execution_rank"] == item["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "可计算枚举度"
    assert target["category"] == instance["category_zh"] == "数理逻辑 / 递归论"
    assert target["target_lane"] == instance["target_lane"] == "hard_statement_first_partial_verification"
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    assert item["theorem_id"] == THEOREM_ID and item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] in {"[ ]", "[_]"} and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    assert formal["backend"] == "lean4"
    assert all(
        formal[key] is None
        for key in (
            "module",
            "declaration_or_expression",
            "elaborated_expression_hash",
            "environment_fingerprint",
        )
    )
    assert instance["quantifiers"] == instance["ordered_binders"] == instance["hypotheses"] == []
    assert instance["alternate_encodings"] == instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert receipt["theorem_complete"] is False

    neighbors = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert neighbors == {"THM-M-0745", "THM-M-0748", "THM-M-0749", "THM-M-0750", "THM-M-0751", "THM-M-0752"}
    formal_modules = {row["module"] for row in instance["formal_candidates_not_credited"]}
    assert formal_modules == {
        "Mathlib.Computability.Halting",
        "Mathlib.Computability.TuringDegree",
        "Mathlib.Computability.Reduce",
    }

    expected_tasks = []
    dependency = ITEM_ID
    for suffix in TASK_SUFFIXES:
        task_id = f"S56-M-0758-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["change_impact_set"] == [ITEM_ID]
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["selftest_result"] == "pass"
    assert receipt["known_failures"] and receipt["first_failed_theorem_gate"]

    for relative, tagged in receipt["source_inputs"].items():
        assert tagged == f"sha256:{sha256(ROOT / relative)}", f"stale source input: {relative}"
    assert instance["source_revisions"]["repository_base"] == BASE_REVISION
    assert instance["source_revisions"]["repository_base_tree"] == BASE_TREE
    assert instance["source_revisions"]["mathlib"] == receipt["worker_input_hashes"]["mathlib_revision"]
    assert instance["source_revisions"]["mathlib_tree"] == receipt["worker_input_hashes"]["mathlib_tree"]

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx)\b|^[ \t]*(axiom|constant|opaque|unsafe)[ \t]",
        re.MULTILINE,
    )
    assert prohibited.search((HERE / "IntakeProbe.lean").read_text(encoding="utf-8")) is None

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), f"trailing whitespace: {path.name}"
        if path.suffix in {".md", ".json"}:
            text = data.decode("utf-8")
            assert "/home/" not in text and "/.cron/" not in text
            assert "theorem_complete=true" not in text

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0758 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
