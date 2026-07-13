#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0079."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0079"
ITEM_ID = "S56-M-0079-INTAKE"
RANK = 1105
BASE_REVISION = "0d2c3bdcd192266bc255ac3d5186da604517145a"
BASE_TREE = "eafbcb48efd51d9cda34f0fc1afe780434abad64"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
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
SOURCE_HASH_FIELDS = {
    "target_manifest_sha256": "Docs/Stage1_Targets_rev-5.6.json",
    "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
    "execution_dag_sha256": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
    "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
    "repository_math_source_sha256": "Docs/researches/math_theorems.md",
    "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
    "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
    "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
}
MATHLIB_SOURCE_HASH_FIELDS = {
    "mathlib_nielsen_schreier_source_sha256": (
        "Mathlib/GroupTheory/FreeGroup/NielsenSchreier.lean"
    ),
    "mathlib_is_free_group_source_sha256": (
        "Mathlib/GroupTheory/FreeGroup/IsFreeGroup.lean"
    ),
    "mathlib_1000_docs_sha256": "docs/1000.yaml",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet_path = path.resolve()
    packet = load(packet_path)
    data = packet_path.read_bytes()
    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
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

    targets = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    items = [row for row in execution["items"] if row["id"] == ITEM_ID]
    assert len(targets) == len(items) == 1
    target, item = targets[0], items[0]

    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "尼尔森-施莱尔定理"
    assert target["category"] == instance["category"] == "代数学 / 群论"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == "已验证"
    assert instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False
    assert instance["theorem_complete"] is False

    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == (
        "Create the theorem dossier, scope map, and source-statement crosswalk."
    )
    assert item["completion_gate"] == (
        "rev-5.6 node-specific receipt and master acceptance"
    )

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"]
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert dag["lifecycle_mode"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["literal_source_claim_zh"] == "自由群的子群仍是自由群"
    assert instance["canonical_statement"] == "Every subgroup of a free group is free."
    assert instance["canonical_claim"] == instance["canonical_statement"]
    formal = instance["canonical_formal_target"]
    for key in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[key] is None
    assert formal["candidate_declaration"] == "subgroupIsFreeOfIsFree"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["audit_complete"] is dag["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is False
    assert instance["accepted_proof_state"] == []
    assert instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["proposed_state"] == "[_]"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["canonical_obligation_ids"] == []
    assert receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == []
    assert receipt["composition_certificates"] == []
    assert receipt["proof_body_locations"] == []
    assert receipt["attestor"]["identity"] == "Stage1 rev-5.6 worker slot9"
    assert receipt["support_state"] == "provisional_unaccepted"
    assert receipt["validated_at"] is not None
    assert receipt["selftest_result"] == "pass"

    assert dag["schema_version"] == "stage1-task-dag/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["root_task_id"] == f"S56-M-0079-{TASK_SUFFIXES[0]}"
    assert len(dag["tasks"]) == len(TASK_SUFFIXES)
    previous = ITEM_ID
    execution_rows = {
        row["id"]: row
        for row in execution["items"]
        if row["theorem_id"] == THEOREM_ID
    }
    for layer, (task, suffix) in enumerate(zip(dag["tasks"], TASK_SUFFIXES), 1):
        expected_id = f"S56-M-0079-{suffix}"
        expected = execution_rows[expected_id]
        assert task["id"] == expected_id
        assert task["state"] == "open" and task["evidence_ids"] == []
        assert task["depends_on"] == [previous]
        assert task["phase"] == expected["phase"]
        assert task["layer"] == expected["layer"] == layer
        assert task["owned_paths"] == expected["owned_paths"] == [
            f"Stage1_Instances/{THEOREM_ID}"
        ]
        assert task["deliverable"] == expected["deliverable"]
        assert task["completion_gate"] == expected["completion_gate"]
        previous = expected_id

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    source_revisions = instance["source_revisions"]
    assert source_revisions["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert source_revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert source_revisions[field] == sha256(ROOT / relative), field

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert mathlib.exists(), "the canonical pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert source_revisions["mathlib"] == MATHLIB_REVISION
    assert source_revisions["mathlib_tree"] == MATHLIB_TREE
    for field, relative in MATHLIB_SOURCE_HASH_FIELDS.items():
        assert source_revisions[field] == sha256(mathlib / relative), field
    worker_hashes = receipt["worker_input_hashes"]
    assert worker_hashes["intake_probe_source_sha256"] == sha256(
        HERE / "IntakeProbe.lean"
    )
    assert worker_hashes["intake_validator_source_sha256"] == sha256(
        HERE / "check_intake.py"
    )

    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 4
    assert all(recipe["expected_exit"] == recipe["exit_code"] == 0 for recipe in recipes)
    assert all(recipe["covered_ids"] == [ITEM_ID] for recipe in recipes)
    assert all(recipe["expected_outputs"] for recipe in recipes)

    files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert files == OWNED_FILES
    assert instance["owned_artifacts"] == [
        "README.md",
        "instance.json",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "task-dag.json",
        "IntakeProbe.lean",
        "check_intake.py",
        "validation.md",
        "intake-receipt.json",
    ]
    assert {Path(path).name for path in instance["public_merge_targets"]} == OWNED_FILES

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"{path} needs a trailing newline"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert "subgroupIsFreeOfIsFree" in probe
    for forbidden in ("sorry", "admit", "sorryAx", "axiom "):
        assert forbidden not in probe

    expected_changed = {f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES}
    expected_changed.add(".stage1-worker-selftest.json")
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["known_failures"]
    assert receipt["remaining_root_cut_set"] == [
        f"S56-M-0079-{suffix}" for suffix in TASK_SUFFIXES
    ]
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print(
        "intake check: ok (manifest/DAG identity, planned lifecycle, source and "
        "formal-candidate boundary, pinned hashes, empty accepted state, nine owned "
        "artifacts, and six open downstream tasks)"
    )


if __name__ == "__main__":
    main()
