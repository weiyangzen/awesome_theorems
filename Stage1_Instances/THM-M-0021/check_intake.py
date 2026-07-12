#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0021 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0021"
ITEM_ID = "S56-M-0021-INTAKE"
RANK = 1068
ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
TASK_SUFFIXES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)
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


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain an object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_output(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--worker-packet",
        type=Path,
        help="optional provisional worker packet; absent after integration",
    )
    args = parser.parse_args()

    manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution_dag = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")
    selftest = load(args.worker_packet) if args.worker_packet is not None else None

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    item = next(row for row in execution_dag["items"] if row["id"] == ITEM_ID)

    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert instance["legacy_priority_slot"] is None
    assert target["target_lane"] == instance["target_lane"] == "hard_statement_first_partial_verification"
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["name"] == instance["name_zh"] == "布饶尔-西格尔定理"
    assert target["category"] == instance["category"] == "代数学 / 域论"
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is False

    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] in {"[ ]", "[_]"} and item["depends_on"] == []
    if selftest is not None:
        assert item["state"] == "[ ]", "worker base must precede provisional integration"
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert dag["lifecycle_mode"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None

    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == []
    assert instance["alternate_encodings"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    expected_input_hashes = {
        "target_manifest_sha256": ROOT / "Docs" / "Stage1_Targets_rev-5.6.json",
        "authoritative_blueprint_sha256": ROOT / "Docs" / "Stage1_Blueprint_rev-5.6.md",
        "execution_dag_sha256": ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json",
        "execution_skill_sha256": ROOT / "skills" / "execute-stage1-rev56" / "SKILL.md",
        "blueprint_guidelines_sha256": ROOT / "Docs" / "Blueprint_Guidelines.md",
        "repository_math_source_sha256": ROOT / "Docs" / "researches" / "math_theorems.md",
        "stage0_blueprint_sha256": ROOT / "Docs" / "Stage0_Blueprint.md",
        "lean_toolchain_file_sha256": ROOT / "Formalizations" / "Lean" / "lean-toolchain",
        "lake_manifest_sha256": ROOT / "Formalizations" / "Lean" / "lake-manifest.json",
        "class_number_source_sha256": ROOT / "Formalizations" / "Lean" / ".lake" / "packages" / "mathlib" / "Mathlib" / "NumberTheory" / "NumberField" / "ClassNumber.lean",
        "regulator_source_sha256": ROOT / "Formalizations" / "Lean" / ".lake" / "packages" / "mathlib" / "Mathlib" / "NumberTheory" / "NumberField" / "Units" / "Regulator.lean",
        "discriminant_defs_source_sha256": ROOT / "Formalizations" / "Lean" / ".lake" / "packages" / "mathlib" / "Mathlib" / "NumberTheory" / "NumberField" / "Discriminant" / "Defs.lean",
        "ideal_asymptotics_source_sha256": ROOT / "Formalizations" / "Lean" / ".lake" / "packages" / "mathlib" / "Mathlib" / "NumberTheory" / "NumberField" / "Ideal" / "Asymptotics.lean",
    }
    for key, path in expected_input_hashes.items():
        assert sha256(path) == revisions[key], f"source revision hash mismatch: {key}"
    assert git_output("rev-parse", "HEAD") == revisions["repository_base"]
    assert git_output("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"]
    assert subprocess.run(
        ["git", "-C", str(ROOT / "Formalizations" / "Lean" / ".lake" / "packages" / "mathlib"), "rev-parse", "HEAD"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip() == revisions["mathlib"]
    assert subprocess.run(
        ["git", "-C", str(ROOT / "Formalizations" / "Lean" / ".lake" / "packages" / "mathlib"), "rev-parse", "HEAD^{tree}"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip() == revisions["mathlib_tree"]

    authoritative_items = {row["id"]: row for row in execution_dag["items"]}
    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0021-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        authoritative = authoritative_items[task_id]
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    actual_artifacts = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual_artifacts == OWNED_FILES
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    assert not any(path.is_symlink() for path in HERE.iterdir())
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is False and receipt["content_addressed"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["owner"] == "Stage1 integration lane"
    assert receipt["supersession_state"] == "current_unsuperseded_worker_report"
    assert receipt["revocation_state"] == "not_revoked"
    assert receipt["first_failed_gate"] == "S56-M-0021-STATEMENT: exact source-statement identity is unresolved"
    assert receipt["selftest_result"] == "pass"
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    source_input_paths = {
        "Docs/Stage1_Targets_rev-5.6.json": ROOT / "Docs" / "Stage1_Targets_rev-5.6.json",
        "Docs/Stage1_Blueprint_rev-5.6.md": ROOT / "Docs" / "Stage1_Blueprint_rev-5.6.md",
        "Docs/Stage1_Execution_DAG_rev-5.6.json": ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json",
        "skills/execute-stage1-rev56/SKILL.md": ROOT / "skills" / "execute-stage1-rev56" / "SKILL.md",
        "Docs/Blueprint_Guidelines.md": ROOT / "Docs" / "Blueprint_Guidelines.md",
        "Docs/researches/math_theorems.md": ROOT / "Docs" / "researches" / "math_theorems.md",
        "Docs/Stage0_Blueprint.md": ROOT / "Docs" / "Stage0_Blueprint.md",
    }
    for relative, path in source_input_paths.items():
        assert receipt["source_inputs"][relative] == f"sha256:{sha256(path)}"
    assert receipt["worker_input_hashes"]["lean_toolchain"] == (
        f"sha256:{revisions['lean_toolchain_file_sha256']}"
    )
    assert receipt["worker_input_hashes"]["lake_manifest"] == (
        f"sha256:{revisions['lake_manifest_sha256']}"
    )
    assert receipt["worker_input_hashes"]["mathlib_revision"] == revisions["mathlib"]
    assert receipt["worker_input_hashes"]["mathlib_tree"] == revisions["mathlib_tree"]
    assert receipt["source_evidence"]["repository_record_excerpt_sha256"] == revisions["repository_record_excerpt_sha256"]
    assert receipt["source_evidence"]["duplicate_record_excerpt_sha256"] == revisions["duplicate_record_excerpt_sha256"]
    assert receipt["source_evidence"]["stage0_excerpt_sha256"] == revisions["stage0_excerpt_sha256"]
    preexisting = {row["path"]: row for row in receipt["preexisting_unrelated_changes"]}
    assert sha256(ROOT / "Stage1_Instances" / "THM-M-1360" / "statement-blocker.json") == (
        preexisting["Stage1_Instances/THM-M-1360/statement-blocker.json"]["sha256_before_owned_work"]
    )
    assert sha256(ROOT / "Stage1_Instances" / "THM-M-1360" / "statement-blocker.md") == (
        preexisting["Stage1_Instances/THM-M-1360/statement-blocker.md"]["sha256_before_owned_work"]
    )
    lake_link = ROOT / "Formalizations" / "Lean" / ".lake"
    assert lake_link.is_symlink()
    assert hashlib.sha256(lake_link.readlink().as_posix().encode()).hexdigest() == (
        preexisting["Formalizations/Lean/.lake"]["symlink_target_string_sha256"]
    )

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    if selftest is not None:
        assert selftest["item_id"] == ITEM_ID
        assert selftest["theorem_id"] == THEOREM_ID and selftest["intent"] == "intake"
        assert selftest["audit_complete"] is selftest["theorem_complete"] is False
        assert set(selftest["changed_paths"]) == expected_changed
        assert selftest["state"] == "[_]"
        assert receipt["base_revision"] == selftest["base_revision"]
        assert receipt["receipt_id"] == selftest["receipt_id"]
        assert selftest["accepted_receipt_ids"] == []
        assert selftest["proof_body_locations"] == []
        assert selftest["verdict"] == "no_state_change"
        assert selftest["root_vector_after"] == ROOT_VECTOR
        assert selftest["first_failed_gate"] == receipt["first_failed_gate"]
        assert selftest["remaining_root_cut_set"] == receipt["remaining_root_cut_set"]
        assert selftest["validated_at"] == receipt["validated_at"]

    checked_paths = list(HERE.iterdir())
    if args.worker_packet is not None:
        checked_paths.append(args.worker_packet)
    for path in checked_paths:
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"trailing whitespace: {path.name}"
        )

    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("intake invariant check: ok (THM-M-0021 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
