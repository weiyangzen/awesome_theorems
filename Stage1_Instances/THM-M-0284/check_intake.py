#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0284 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0284"
ITEM_ID = "S56-M-0284-INTAKE"
RANK = 1290
BASE_REVISION = "2eea98305d46266f078a50cf0e85853bf6a5e702"
BASE_TREE = "02279a8caa5f31ed8e37e35c8584a336eed9b974"
SOURCE_RECORD_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_RECORD_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
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
TASK_SUFFIXES = [
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
]
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
MATHLIB_HASH_FIELDS = {
    "mathlib_zero_one_source_sha256": (
        "Mathlib/Probability/Independence/ZeroOne.lean"
    ),
    "mathlib_independence_basic_source_sha256": (
        "Mathlib/Probability/Independence/Basic.lean"
    ),
    "mathlib_overview_sha256": "docs/overview.yaml",
    "mathlib_undergrad_sha256": "docs/undergrad.yaml",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def excerpt_sha256(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1 : end])).hexdigest()


def check_text_file(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path.name}"
    assert b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
        f"trailing whitespace: {path.name}"
    )


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    check_text_file(path.resolve())
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
    expected_paths = set(receipt["changed_paths"]) | {".stage1-worker-selftest.json"}
    assert set(packet["changed_paths"]) == expected_paths
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]


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
    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "柯尔莫哥洛夫零一律",
        "category": "分析学 / 实分析",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 86,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }

    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item == {
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
    assert instance["execution_rank"] == RANK
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == receipt["phase"] == "intake"
    assert instance["baseline"] == "L0" and instance["rework_required"] is True
    assert instance["legacy_priority_slot"] is None
    assert instance["legacy_artifacts_accepted"] is False

    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[key] is None
    assert formal["declaration_candidates"] == [
        "ProbabilityTheory.measure_zero_or_one_of_measurableSet_limsup_atTop",
        "ProbabilityTheory.measure_zero_or_one_of_measurableSet_limsup_atBot",
        "ProbabilityTheory.Kernel.measure_zero_or_one_of_measurableSet_limsup_atTop",
    ]
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert git("rev-parse", "HEAD:Docs/Stage0_Blueprint.md") == revisions["stage0_current_blob"]
    assert (
        git("rev-parse", f"{SOURCE_RECORD_COMMIT}:Docs/researches/math_theorems.md")
        == revisions["repository_source_record_blob"]
        == SOURCE_RECORD_BLOB
    )
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 2041, 2046) == revisions["catalog_excerpt_sha256"]
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 7392, 7397) == revisions["duplicate_catalog_excerpt_sha256"]
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 7846, 7871) == revisions["stage0_projection_excerpt_sha256"]
    assert excerpt_sha256(ROOT / "Docs/Stage1_Targets_rev-5.6.json", 19360, 19373) == revisions["target_manifest_excerpt_sha256"]
    assert excerpt_sha256(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json", 159849, 159863) == revisions["execution_item_excerpt_sha256"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    for field, relative in MATHLIB_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"
    legacy = ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_284.lean"
    assert revisions["unrelated_legacy_slot_sha256"] == sha256(legacy)
    assert "THM-M-1004: Optional stopping theorem" in legacy.read_text(encoding="utf-8")

    expected_chain = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0284-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        expected_chain.append((task_id, [dependency]))
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [
            f"Stage1_Instances/{THEOREM_ID}"
        ]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["state"] == "open" and task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_chain

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    for phrase in (
        "**柯尔莫哥洛夫零一律**",
        "- 提出者: Andrey Kolmogorov",
        "- 时间: 1933",
        "- 陈述: 尾事件的零一性质",
    ):
        assert phrase in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0284 柯尔莫哥洛夫零一律" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {
        "THM-M-0283",
        "THM-M-0285",
        "THM-M-1007",
        "THM-M-1008",
    }

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files}
    assert set(receipt["changed_paths"]) == expected_changed
    assert set(receipt["owned_output_sha256"]) == expected_changed
    for relative, digest in receipt["owned_output_sha256"].items():
        if digest is not None:
            assert digest == sha256(ROOT / relative), f"stale output hash: {relative}"

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["acceptance_authority"] == "integration lane"
    assert receipt["attestor"]["signature"] is None
    assert receipt["attestor"]["signature_status"] == "unsigned_provisional_worker_report"
    assert receipt["platform"]["operating_system"] == platform.system()
    assert receipt["platform"]["architecture"] == platform.machine()
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"

    for relative, tagged_digest in receipt["source_inputs"].items():
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}"
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert receipt["worker_input_hashes"]["lake_symlink_target_string"] == (
        f"sha256:{hashlib.sha256(lake_target).hexdigest()}"
    )
    assert receipt["worker_input_hashes"]["mathlib_revision"] == revisions["mathlib"]
    assert receipt["worker_input_hashes"]["mathlib_tree"] == revisions["mathlib_tree"]

    for recipe in receipt["structured_validation_recipes"]:
        assert recipe["recipe_id"].startswith(f"{ITEM_ID}-")
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert isinstance(recipe["env_allowlist"], dict)
        assert isinstance(recipe["timeout_seconds"], int) and recipe["timeout_seconds"] > 0
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["exit_code"] == 0
        assert isinstance(recipe["expected_outputs"], list) and recipe["expected_outputs"]
        assert recipe["covered_task_ids"] == [ITEM_ID]
        assert recipe["covered_obligation_ids"] == []

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()
    for path in HERE.iterdir():
        if path.is_file():
            check_text_file(path)
    for name in (
        "README.md",
        "instance.json",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "task-dag.json",
        "validation.md",
        "intake-receipt.json",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b", probe
    )

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0284 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
