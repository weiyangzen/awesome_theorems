#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0884."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0884"
ITEM_ID = "S56-M-0884-INTAKE"
RANK = 1436
BASE_REVISION = "0c019b7194c9c43fa5f683fa82d637a0b275410d"
BASE_TREE = "43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e"
ROOT_VECTOR = {"H": "H5", "M": "M4", "R": "R4"}
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
SOURCE_PATHS = {
    "target_manifest_sha256": "Docs/Stage1_Targets_rev-5.6.json",
    "applicable_theorems_sha256": "Docs/Stage1_Blueprint_Applicable_Theorems.md",
    "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
    "execution_dag_sha256": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
    "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
    "repository_math_source_sha256": "Docs/researches/math_theorems.md",
    "repository_classification_source_sha256": "Docs/researches/classified_theorems.md",
    "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
    "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
    "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
}
MATHLIB_SOURCE_PATHS = {
    "mathlib_simple_graph_finite_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph/Finite.lean"
    ),
    "mathlib_adj_matrix_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph/AdjMatrix.lean"
    ),
    "mathlib_lap_matrix_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph/LapMatrix.lean"
    ),
    "mathlib_matrix_spectrum_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Matrix/Spectrum.lean"
    ),
    "mathlib_real_sqrt_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Data/Real/Sqrt.lean"
    ),
}


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), f"{path} must contain an object"
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_digest(path: Path, first_line: int, last_line: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first_line - 1 : last_line])).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path)
    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]
    check_text_file(path)


def check_text_file(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path}"
    assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {path}"
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
        f"trailing whitespace: {path}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    authority = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "Ramanujan图",
        "category": "组合数学 / 图论",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 86,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    for field in (
        "execution_rank",
        "legacy_priority_slot",
        "category",
        "source_status_untrusted",
        "baseline",
        "rework_required",
        "legacy_artifacts_accepted",
        "target_lane",
        "intake_score",
        "lifecycle_mode",
        "theorem_complete",
    ):
        assert instance[field] == target[field]
    assert instance["name_zh"] == target["name"]

    intake = next(row for row in authority["items"] if row["id"] == ITEM_ID)
    assert intake == {
        "id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "execution_rank": RANK,
        "phase": "intake",
        "layer": 0,
        "state": "[ ]",
        "depends_on": [],
        "owned_paths": [f"Stage1_Instances/{THEOREM_ID}"],
        "deliverable": "Create the theorem dossier, scope map, and source-statement crosswalk.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "graph_class_and_optimality_slogan" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    for field in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[field] is None
    assert instance["ordered_binders"] == instance["quantifiers"] == instance["hypotheses"] == []
    assert instance["alternate_encodings"] == instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert dag["audit_complete"] is dag["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md') == revisions["repository_source_record_blob"]
    assert excerpt_digest(ROOT / "Docs/researches/math_theorems.md", 6474, 6479) == revisions["repository_record_excerpt_sha256"]
    assert excerpt_digest(ROOT / "Docs/Stage0_Blueprint.md", 24116, 24141) == revisions["stage0_projection_excerpt_sha256"]
    for field, relative in SOURCE_PATHS.items():
        assert revisions[field] == digest(ROOT / relative), f"stale source hash: {field}"

    expected_tasks: list[tuple[str, list[str]]] = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0884-{suffix}"
        task = dag["tasks"][layer - 1]
        source_task = next(row for row in authority["items"] if row["id"] == task_id)
        expected_tasks.append((task_id, [dependency]))
        assert task["id"] == task_id and task["depends_on"] == [dependency]
        assert task["state"] == "open" and task["evidence_ids"] == []
        for field in ("phase", "layer", "owned_paths", "deliverable", "completion_gate"):
            assert task[field] == source_task[field]
        assert task["layer"] == layer
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**Ramanujan图**") == 1
    assert catalog.count("- 陈述: 最优谱扩展图") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert stage0.count("THM-M-0884 Ramanujan图") == 1
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {
        "THM-M-0881", "THM-M-0883", "THM-M-0885", "THM-M-0886", "THM-M-0887", "THM-M-0888"
    }
    source = instance["human_source_discovery_not_credited"][0]
    assert source["stable_identifier"] == "arXiv:1711.06558v1"
    assert source["pdf_sha256"] == "cfcdc1d023eb9ab8bb7397fefa98b216cce74770fcbb9177b84ee2534f65a32e"

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual_files == set(instance["owned_artifacts"]) == OWNED_FILES
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["content_addressed"] is receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change" and receipt["proposed_state"] == "[_]"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["canonical_obligation_ids"] == receipt["typed_graph_changes"] == []
    assert receipt["composition_certificates"] == receipt["proof_body_locations"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"
    assert receipt["first_failed_gate"] == "master_acceptance_of_node_specific_intake_receipt"
    started = datetime.fromisoformat(receipt["validation_started_at"])
    ended = datetime.fromisoformat(receipt["validation_ended_at"])
    assert started <= ended <= datetime.now(timezone.utc).astimezone()
    assert receipt["platform"]["operating_system"] == platform.system()
    assert receipt["platform"]["architecture"] == platform.machine()

    for relative, tagged in receipt["source_inputs"].items():
        assert tagged == f"sha256:{digest(ROOT / relative)}", f"stale receipt input: {relative}"
    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["mathlib_revision"] == revisions["mathlib"]
    assert worker_inputs["mathlib_tree"] == revisions["mathlib_tree"]
    for field, relative in MATHLIB_SOURCE_PATHS.items():
        assert worker_inputs[field] == digest(ROOT / relative), f"stale mathlib source: {field}"
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"]
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"]
    assert git("status", "--short", cwd=mathlib) == ""

    hashed_files = actual_files - {"intake-receipt.json"}
    assert set(receipt["untracked_owned_artifact_sha256"]) == hashed_files
    for name in hashed_files:
        assert receipt["untracked_owned_artifact_sha256"][name] == digest(HERE / name), name
    for recipe in receipt["structured_validation_recipes"]:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert isinstance(recipe["env_allowlist"], dict)
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["exit_code"] == 0
    for path in HERE.iterdir():
        if path.is_file():
            check_text_file(path)
    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    for token in ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe "):
        assert token not in probe

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet.resolve(), receipt)

    print("intake invariant check: ok (THM-M-0884 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
