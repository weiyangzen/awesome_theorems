#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0300 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0300"
ITEM_ID = "S56-M-0300-INTAKE"
RANK = 1304
BASE_REVISION = "940588d30669014430d5a1beb187f2bca118e816"
BASE_TREE = "42d80725ccbabcdd826ed2bc8b3622ac31ac7695"
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
    "mathlib_lp_basic_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/"
        "MeasureTheory/Function/LpSpace/Basic.lean"
    ),
    "mathlib_bochner_basic_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/"
        "MeasureTheory/Integral/Bochner/Basic.lean"
    ),
    "mathlib_haar_unique_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/"
        "MeasureTheory/Measure/Haar/Unique.lean"
    ),
}
TASK_SUFFIXES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)
RECIPE_FIELDS = {
    "recipe_id",
    "cwd",
    "argv",
    "env_allowlist",
    "timeout_seconds",
    "network_policy",
    "expected_exit",
    "expected_outputs",
    "covered_workflow_item_ids",
    "covered_obligation_ids",
    "covered_declarations",
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


def excerpt_sha256(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1 : end])).hexdigest()


def check_worker_packet(path: Path, receipt: dict, expected_changed: set[str]) -> None:
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
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == expected_changed
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]


def check_recorded_commands(receipt: dict) -> None:
    """Keep machine command evidence concrete rather than prose-shaped."""
    commands = receipt["commands_and_results"]
    assert isinstance(commands, list) and commands
    for command in commands:
        assert "command" not in command
        assert isinstance(command.get("argv"), list) and all(
            isinstance(part, str) and part for part in command["argv"]
        )
        assert isinstance(command.get("exit_code"), int)
        assert isinstance(command.get("result"), str) and command["result"]


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
    assert target["name"] == instance["name_zh"] == "哈代空间原子分解"
    assert target["category"] == instance["category_zh"] == "分析学 / 实分析"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is False

    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["attempts"] == 0 and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_id"] == "S56-M-0300-INTAKE-WORKER-20260713"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert receipt["phase"] == "intake"
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "not_one_stable_proposition" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert receipt["root_vector_before"] == {
        "H": "unclassified",
        "M": "unclassified",
        "R": "unclassified",
    }
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["repository_source_record_blob_at_base"]
    assert (
        git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md')
        == revisions["repository_source_record_blob_at_origin"]
    )
    assert git("rev-parse", "HEAD:Docs/Stage0_Blueprint.md") == revisions["stage0_projection_blob_at_base"]
    assert git("log", "-1", "--format=%H", "--", "Docs/Stage1_Targets_rev-5.6.json") == revisions["target_manifest_origin_commit"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    catalog_path = ROOT / "Docs/researches/math_theorems.md"
    stage0_path = ROOT / "Docs/Stage0_Blueprint.md"
    target_path = ROOT / "Docs/Stage1_Targets_rev-5.6.json"
    assert revisions["repository_record_excerpt_sha256"] == excerpt_sha256(catalog_path, 2153, 2158)
    assert revisions["duplicate_repository_record_excerpt_sha256"] == excerpt_sha256(catalog_path, 2633, 2638)
    assert revisions["stage0_projection_excerpt_sha256"] == excerpt_sha256(stage0_path, 8278, 8303)
    assert revisions["duplicate_stage0_projection_excerpt_sha256"] == excerpt_sha256(stage0_path, 9962, 9987)
    assert revisions["target_manifest_excerpt_sha256"] == excerpt_sha256(target_path, 19570, 19583)
    assert revisions["duplicate_target_manifest_excerpt_sha256"] == excerpt_sha256(target_path, 12835, 12848)

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE

    dependency = ITEM_ID
    expected_tasks = []
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0300-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == []
        expected_tasks.append((task_id, [dependency], "open"))
        dependency = task_id
    assert [(row["id"], row["depends_on"], row["state"]) for row in dag["tasks"]] == expected_tasks

    catalog = catalog_path.read_text(encoding="utf-8")
    assert catalog.count("- 陈述: H^1空间的原子分解") == 2
    assert "**哈代空间原子分解**" in catalog and "**原子分解定理**" in catalog
    stage0 = stage0_path.read_text(encoding="utf-8")
    assert "THM-M-0300 哈代空间原子分解" in stage0
    assert "THM-M-0362 原子分解定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    neighbors = {row["theorem_id"]: row["name"] for row in instance["neighbor_target_boundaries"]}
    assert neighbors == {
        "THM-M-0362": "原子分解定理",
        "THM-M-0301": "BMO空间对偶定理",
        "THM-M-0302": "约翰-尼伦伯格不等式",
    }
    manifest_neighbors = {
        row["theorem_id"]: row["name"]
        for row in manifest["targets"]
        if row["theorem_id"] in neighbors
    }
    assert manifest_neighbors == neighbors

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    receipt_path = f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert set(receipt["changed_paths"]) == expected_changed
    dirty = receipt["dirty_input_evidence"]
    assert set(dirty) == {
        "preflight_untracked_paths",
        "owned_untracked_paths",
        "untracked_input_hashes",
    }
    assert dirty["preflight_untracked_paths"] == ["Formalizations/Lean/.lake"]
    assert set(dirty["owned_untracked_paths"]) == expected_changed
    expected_dirty_hashes = expected_changed - {receipt_path}
    assert set(dirty["untracked_input_hashes"]) == expected_dirty_hashes
    for relative, tagged in dirty["untracked_input_hashes"].items():
        assert tagged == f"sha256:{sha256(ROOT / relative)}", (
            f"stale dirty-input hash: {relative}"
        )
    actual_untracked = set(git("ls-files", "--others", "--exclude-standard").splitlines())
    assert actual_untracked == expected_changed | {"Formalizations/Lean/.lake"}
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False and receipt["verdict"] == "no_state_change"
    assert receipt["selftest_result"] == "pass"
    assert receipt["accepted_receipt_ids"] == receipt["content_addressed_receipt_ids"] == []
    assert receipt["content_addressed_recipe_ids"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["proof_body_locations"] == receipt["typed_graph_changes"] == []
    assert receipt["composition_certificates"] == []
    check_recorded_commands(receipt)
    assert receipt["remaining_root_cut_set"] == [row["id"] for row in dag["tasks"]]
    expected_hashed = OWNED_FILES - {"intake-receipt.json"}
    assert set(receipt["owned_artifact_hashes"]) == expected_hashed
    assert "intake-receipt.json" in receipt["self_reference_boundary"]
    for name, tagged in receipt["owned_artifact_hashes"].items():
        assert tagged == f"sha256:{sha256(HERE / name)}", f"stale owned hash: {name}"
    assert receipt["acceptance_authority"] == "rev-5.6 integration lane"
    assert all(receipt[key] for key in (
        "worker_branch_or_worktree",
        "diff_summary",
        "exact_statement_change",
        "source_revision_and_proof_body_summary",
        "ownership_and_change_impact",
        "output_summary",
        "owner",
        "validated_at",
        "review_due",
        "support_state",
        "revocation_policy",
        "incident_path",
    ))
    assert receipt["validation_started_at"] <= receipt["validation_ended_at"] == receipt["validated_at"]
    assert receipt["attestor"] == {
        "kind": "stage1_rev56_worker_selftest",
        "identity": "isolated worker for S56-M-0300-INTAKE",
        "signature": None,
        "signature_status": "unsigned_provisional_worker_evidence",
    }
    assert receipt["invalidation_inputs"] and receipt["known_failures"]
    for relative, tagged in receipt["source_inputs"].items():
        assert tagged == f"sha256:{sha256(ROOT / relative)}", f"stale receipt input: {relative}"
    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["repository_base_revision"] == BASE_REVISION
    assert worker_inputs["repository_base_tree"] == BASE_TREE
    assert worker_inputs["mathlib_revision"] == MATHLIB_REVISION
    assert worker_inputs["mathlib_tree"] == MATHLIB_TREE
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert worker_inputs["lake_symlink_target_string_sha256"] == hashlib.sha256(lake_target).hexdigest()

    recipes = receipt["structured_validation_recipes"]
    assert [row["recipe_id"] for row in recipes] == [
        "S56-M-0300-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0300-INTAKE-RECIPE-LEAN-PROBE",
    ]
    for recipe in recipes:
        assert set(recipe) == RECIPE_FIELDS
        assert recipe["argv"] and recipe["expected_outputs"]
        assert recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        assert recipe["covered_workflow_item_ids"] == [ITEM_ID]
        assert recipe["covered_obligation_ids"] == []
        assert isinstance(recipe["covered_declarations"], list)
    assert recipes[0]["covered_declarations"] == []
    assert set(recipes[1]["covered_declarations"]) == {
        "MeasureTheory.Lp",
        "MeasureTheory.MemLp",
        "MeasureTheory.Integrable",
        "MeasureTheory.integral",
        "MeasureTheory.volume",
        "Filter.Tendsto",
        "Summable",
    }

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in (
        "README.md",
        "instance.json",
        "intake-receipt.json",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "task-dag.json",
        "validation.md",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    forbidden = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert not any(token in probe for token in forbidden)

    if args.worker_packet:
        check_worker_packet(args.worker_packet.resolve(), receipt, expected_changed)

    print("THM-M-0300 intake invariant check: ok (planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
