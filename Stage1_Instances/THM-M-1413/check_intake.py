#!/usr/bin/env python3
"""Validate the scoped THM-M-1413 planned-intake invariants."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


TARGET_ID = "THM-M-1413"
ITEM_ID = "S56-M-1413-INTAKE"
RANK = 912
BASE = "cbe531e6fdc68190477a9c7e8f635fe5a68a4bcd"
BASE_TREE = "0b4a5720f51c89484fdc5f6b6f07dc01ee1e95c8"
MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
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


def records(value: object, *keys: str) -> list[dict]:
    if isinstance(value, list):
        return value
    assert isinstance(value, dict)
    for key in keys:
        candidate = value.get(key)
        if isinstance(candidate, list):
            return candidate
        if isinstance(candidate, dict):
            return list(candidate.values())
    raise AssertionError(f"no record list found under {keys}")


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
    assert instance["lifecycle_mode"] == "planned"
    assert instance["intent"] == "intake"
    assert instance["baseline"] == "L0"
    assert instance["rework_required"] is True
    assert instance["legacy_artifacts_accepted"] is False
    assert instance["canonical_statement"] is None
    assert instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["audit_complete"] is False
    assert instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == []
    assert instance["accepted_receipt_ids"] == []
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    assert {path.name for path in target_dir.iterdir() if path.is_file()} == OWNED_FILES

    assert isinstance(task_dag, dict)
    assert task_dag["theorem_id"] == TARGET_ID
    assert task_dag["lifecycle_mode"] == "planned"
    assert task_dag["accepted_states"] == []
    tasks = task_dag["tasks"]
    assert [task["id"] for task in tasks] == [
        f"S56-M-1413-{suffix}" for suffix in TASK_SUFFIXES
    ]
    expected_dependency = ITEM_ID
    for task in tasks:
        assert task["state"] == "open"
        assert task["depends_on"] == [expected_dependency]
        expected_dependency = task["id"]

    target = next(row for row in records(manifest, "targets") if row["theorem_id"] == TARGET_ID)
    assert target["execution_rank"] == RANK
    assert target["lifecycle_mode"] == "planned"
    assert target["baseline"] == "L0"
    assert target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert target["theorem_complete"] is False

    node = next(row for row in records(execution_dag, "items", "nodes") if row["id"] == ITEM_ID)
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
    assert receipt["base_revision"] == BASE
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is False
    assert receipt["audit_complete"] is False
    assert receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == []
    assert receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == []
    assert receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in tasks]
    assert receipt["selftest_result"] == "pass"
    assert instance["source_revisions"]["mathlib"] == MATHLIB

    hashed = sorted(OWNED_FILES - {"intake-receipt.json"})
    assert sorted(receipt["untracked_owned_artifact_sha256"]) == hashed
    for name in hashed:
        actual = hashlib.sha256((target_dir / name).read_bytes()).hexdigest()
        assert receipt["untracked_owned_artifact_sha256"][name] == actual, name

    for path in target_dir.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data, f"non-LF newline: {path.name}"
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"trailing whitespace: {path.name}"
        )
        text = data.decode("utf-8")
        if path.suffix in {".md", ".json"}:
            assert "/home/" not in text and ".cron/" not in text

    print("intake invariant check: ok")


if __name__ == "__main__":
    main()
