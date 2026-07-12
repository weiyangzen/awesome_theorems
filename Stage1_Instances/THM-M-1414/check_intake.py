#!/usr/bin/env python3
"""Validate the scoped THM-M-1414 planned-intake invariants."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


TARGET_ID = "THM-M-1414"
ITEM_ID = "S56-M-1414-INTAKE"
RANK = 913
TARGET_DIR = Path(__file__).resolve().parent
ROOT = TARGET_DIR.parents[1]
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
    instance = load(TARGET_DIR / "instance.json")
    task_dag = load(TARGET_DIR / "task-dag.json")
    receipt = load(TARGET_DIR / "intake-receipt.json")
    selftest = load(ROOT / ".stage1-worker-selftest.json")
    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution_dag = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert isinstance(instance, dict)
    assert instance["theorem_id"] == TARGET_ID
    assert instance["item_id"] == ITEM_ID
    assert instance["execution_rank"] == RANK
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert instance["intent"] == "intake"
    assert instance["baseline"] == "L0"
    assert instance["rework_required"] is True
    assert instance["legacy_artifacts_accepted"] is False
    assert instance["canonical_statement"] is None
    formal = instance["canonical_formal_target"]
    assert formal["module"] is None
    assert formal["declaration_or_expression"] is None
    assert formal["elaborated_expression_hash"] is None
    assert formal["environment_fingerprint"] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R3"}
    assert instance["audit_complete"] is False
    assert instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == []
    assert instance["accepted_receipt_ids"] == []
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    assert {path.name for path in TARGET_DIR.iterdir() if path.is_file()} == OWNED_FILES

    assert isinstance(task_dag, dict)
    assert task_dag["theorem_id"] == TARGET_ID
    assert task_dag["lifecycle_mode"] == task_dag["lifecycle"] == "planned"
    assert task_dag["theorem_complete"] is False
    assert task_dag["accepted_states"] == []
    tasks = task_dag["tasks"]
    assert [task["id"] for task in tasks] == [
        f"S56-M-1414-{suffix}" for suffix in TASK_SUFFIXES
    ]
    expected_dependency = ITEM_ID
    for task in tasks:
        assert task["state"] == "open"
        assert task["depends_on"] == [expected_dependency]
        expected_dependency = task["id"]

    assert isinstance(manifest, dict)
    target = next(row for row in manifest["targets"] if row["theorem_id"] == TARGET_ID)
    assert target["execution_rank"] == RANK
    assert target["lifecycle_mode"] == "planned"
    assert target["baseline"] == "L0"
    assert target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert target["theorem_complete"] is False

    assert isinstance(execution_dag, dict)
    node = next(row for row in execution_dag["items"] if row["id"] == ITEM_ID)
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
    assert receipt["content_addressed"] is False
    assert receipt["audit_complete"] is False
    assert receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == []
    assert receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == []
    assert receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in tasks]

    assert isinstance(selftest, dict)
    assert selftest["item_id"] == ITEM_ID
    assert selftest["theorem_id"] == TARGET_ID
    assert selftest["state"] == "[_]"
    assert selftest["base_revision"] == receipt["base_revision"]
    assert selftest["receipt_id"] == receipt["receipt_id"]
    assert set(selftest["changed_paths"]) == set(receipt["changed_paths"])

    hashed_files = OWNED_FILES - {"intake-receipt.json"}
    assert set(receipt["untracked_owned_artifact_sha256"]) == hashed_files
    for name in hashed_files:
        digest = hashlib.sha256((TARGET_DIR / name).read_bytes()).hexdigest()
        assert receipt["untracked_owned_artifact_sha256"][name] == digest, name

    for path in TARGET_DIR.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data, f"non-LF newline: {path.name}"
        for line in data.splitlines():
            assert not line.endswith((b" ", b"\t")), f"trailing whitespace: {path.name}"

    print("intake invariant check: ok")


if __name__ == "__main__":
    main()
