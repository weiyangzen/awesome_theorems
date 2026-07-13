#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0270 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0270"
ITEM_ID = "S56-M-0270-INTAKE"
RANK = 1277
BASE_REVISION = "bd81d4853a030765585ef6fed4310484ceb1e458"
BASE_TREE = "fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4"
SOURCE_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
SOURCE_EXCERPT_SHA256 = "a69a6eaa86079195b1c0cae9eed7592f75a1599c6ec349751ed83e612cb4ffe1"
STAGE0_EXCERPT_SHA256 = "67366d78e8d08dbec614b9346bbf74536b43eed39b2ee6b6bca53497d195d698"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROBE_OUTPUT_SHA256 = "383e38620a29d7f4812de9da059233c9125365472b6c9ec1e769cf9b47d01008"
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
PROBE_DECLARATIONS = (
    "MeasureTheory.lintegral_liminf_le'",
    "MeasureTheory.lintegral_liminf_le",
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


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first - 1 : last])).hexdigest()


def run_probe() -> bytes:
    result = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0270/IntakeProbe.lean"],
        cwd=ROOT / "Formalizations/Lean",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stdout.decode(errors="replace")
    return result.stdout


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    assert packet["schema_version"] == "stage1-worker-selftest/1.0"
    assert packet["item_id"] == ITEM_ID and packet["theorem_id"] == THEOREM_ID
    assert packet["intent"] == "intake" and packet["state"] == "[_]"
    assert packet["verdict"] == "no_state_change"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["receipt_id"] == receipt["receipt_id"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["accepted_receipt_ids"] == []
    assert packet["audit_complete"] is packet["theorem_complete"] is False
    assert packet["first_failed_gate"] == receipt["first_failed_gate"]
    assert packet["remaining_root_cut_set"] == receipt["remaining_root_cut_set"]
    assert isinstance(packet["commands"], list) and packet["commands"]
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
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "法图引理"
    assert target["category"] == instance["category"] == "分析学 / 实分析"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert set(formal["declaration_candidates"]) == set(PROBE_DECLARATIONS)
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", f"{SOURCE_COMMIT}:Docs/researches/math_theorems.md") == SOURCE_BLOB
    assert revisions["repository_source_record_commit"] == SOURCE_COMMIT
    assert revisions["repository_source_record_blob"] == SOURCE_BLOB
    assert git("hash-object", "Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 1943, 1948) == SOURCE_EXCERPT_SHA256
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 7468, 7493) == STAGE0_EXCERPT_SHA256
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert revisions["mathlib_fatou_source_sha256"] == sha256(
        mathlib / "Mathlib/MeasureTheory/Integral/Lebesgue/Add.lean"
    )

    expected_tasks = []
    dependency = ITEM_ID
    for suffix in TASK_SUFFIXES:
        task_id = f"S56-M-0270-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**法图引理**" in catalog
    assert "- 提出者: Pierre Fatou" in catalog
    assert "- 时间: 1906" in catalog
    assert "- 陈述: 积分下极限的不等式" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0270 法图引理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert {row["declaration"] for row in instance["formal_candidates_not_credited"]} == set(PROBE_DECLARATIONS)

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert set(receipt["owned_artifact_sha256"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    for relative, expected in receipt["owned_artifact_sha256"].items():
        if relative.endswith("/intake-receipt.json"):
            assert expected == "self_referential_excluded_from_provisional_digest"
        else:
            assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"

    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"
    assert receipt["owner"] == "Stage1 integration lane"
    assert receipt["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]

    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    assert all(recipe["network_policy"] == "denied" for recipe in recipes)
    assert all(recipe["expected_exit"] == 0 for recipe in recipes)
    assert all(recipe["covered_ids"] == [ITEM_ID] for recipe in recipes)

    probe_output = run_probe()
    assert hashlib.sha256(probe_output).hexdigest() == PROBE_OUTPUT_SHA256
    assert receipt["probe_output_sha256"] == PROBE_OUTPUT_SHA256

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in ("README.md", "instance.json", "intake-receipt.json", "scope-map.md", "source-statement-crosswalk.md", "task-dag.json", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0270 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
