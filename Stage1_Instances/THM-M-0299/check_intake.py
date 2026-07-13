#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0299 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0299"
ITEM_ID = "S56-M-0299-INTAKE"
RANK = 1303
BASE_REVISION = "940588d30669014430d5a1beb187f2bca118e816"
BASE_TREE = "42d80725ccbabcdd826ed2bc8b3622ac31ac7695"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
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


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path.name} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", default=".stage1-worker-selftest.json")
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution_dag = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")
    selftest = load(ROOT / args.worker_packet)

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    item = next(row for row in execution_dag["items"] if row["id"] == ITEM_ID)

    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "奇异积分有界性定理"
    assert target["category"] == instance["category"] == "分析学 / 实分析"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"

    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["phase"] == "intake" and receipt["verdict"] == "no_state_change"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == selftest["item_id"] == ITEM_ID
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None

    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == []
    assert all(form["checked_witness"] is None for form in instance["alternate_encodings"])
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0299-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        authoritative = next(row for row in execution_dag["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        assert authoritative["theorem_id"] == THEOREM_ID
        assert authoritative["layer"] == layer
        assert task["id"] == authoritative["id"]
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])
    assert all(task["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"] for task in dag["tasks"])
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]

    actual_artifacts = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual_artifacts == OWNED_FILES
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == set(selftest["changed_paths"]) == expected_changed
    assert receipt["proposed_state"] == selftest["state"] == "[_]"
    assert receipt["accepted"] is False and receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["base_revision"] == selftest["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    recipes = {recipe["recipe_id"]: recipe for recipe in receipt["structured_validation_recipes"]}
    actions = {action["recipe_id"]: action for action in receipt["validation_actions"]}
    expected_recipe_ids = {
        "S56-M-0299-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0299-INTAKE-RECIPE-LEAN-PROBE",
    }
    assert set(recipes) == set(actions) == expected_recipe_ids
    assert all(recipe["expected_exit"] == 0 for recipe in recipes.values())
    assert all(action["exit_code"] == 0 for action in actions.values())
    assert recipes["S56-M-0299-INTAKE-RECIPE-STRUCTURE"]["argv"] == [
        "python3", "-B", "Stage1_Instances/THM-M-0299/check_intake.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert recipes["S56-M-0299-INTAKE-RECIPE-LEAN-PROBE"]["argv"] == [
        "lake", "env", "lean", "../../Stage1_Instances/THM-M-0299/IntakeProbe.lean",
    ]
    assert actions["S56-M-0299-INTAKE-RECIPE-STRUCTURE"]["stdout_sha256"] == (
        "520dea67d7e2a3ed023ec0ecc34e5c206237a07fb5064f86c726633c090b8ab7"
    )
    assert actions["S56-M-0299-INTAKE-RECIPE-LEAN-PROBE"]["stdout_sha256"] == (
        "fdae47ffb51a513d2f0a32159ed2f6f18cd98048c3b75258fc3af6dad352a8ab"
    )
    assert receipt["selftest_result"] == "pass"

    receipt_hashes = receipt["owned_artifact_sha256"]
    for relative, digest in receipt_hashes.items():
        if relative.endswith("/intake-receipt.json"):
            assert digest == "self_referential_excluded_from_provisional_digest"
        else:
            assert digest == sha256(ROOT / relative), f"stale owned artifact hash: {relative}"

    recorded = instance["source_revisions"]
    expected_hashes = {
        "target_manifest_sha256": "Docs/Stage1_Targets_rev-5.6.json",
        "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
        "execution_dag_sha256": "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
        "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
        "repository_math_source_sha256": "Docs/researches/math_theorems.md",
        "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
        "applicable_projection_sha256": "Docs/Stage1_Blueprint_Applicable_Theorems.md",
        "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
        "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
        "lp_basic_source_sha256": "Formalizations/Lean/.lake/packages/mathlib/Mathlib/MeasureTheory/Function/LpSpace/Basic.lean",
        "bochner_basic_source_sha256": "Formalizations/Lean/.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/Basic.lean",
        "continuous_linear_map_source_sha256": "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Normed/Operator/ContinuousLinearMap.lean",
    }
    for key, relative in expected_hashes.items():
        assert recorded[key] == sha256(ROOT / relative), f"stale input hash: {key}"
    assert recorded["repository_base"] == BASE_REVISION
    assert recorded["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert recorded["repository_source_record_commit"] == "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
    assert git("rev-parse", "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f:Docs/researches/math_theorems.md") == recorded["repository_source_record_blob"]
    assert git("hash-object", "Docs/researches/math_theorems.md") == recorded["current_repository_math_source_blob"]
    assert recorded["mathlib"] == MATHLIB_REVISION
    assert recorded["mathlib_tree"] == "bdc39a3123201dae413a9d9be56ec242c19e5c2b"

    source_lines = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8").splitlines(True)
    assert hashlib.sha256("".join(source_lines[2145:2151]).encode()).hexdigest() == recorded["repository_record_excerpt_sha256"]
    catalog = "".join(source_lines)
    assert "**奇异积分有界性定理**" in catalog
    assert "- 提出者: Alberto Calderón/Antoni Zygmund" in catalog
    assert "- 时间: 1952" in catalog
    assert "- 陈述: 奇异积分的L^p有界性" in catalog
    stage0_lines = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8").splitlines(True)
    assert hashlib.sha256("".join(stage0_lines[8250:8276]).encode()).hexdigest() == recorded["stage0_excerpt_sha256"]
    stage0 = "".join(stage0_lines)
    assert "THM-M-0299 奇异积分有界性定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    neighbor_ids = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert neighbor_ids == {"THM-M-0298", "THM-M-0350", "THM-M-0352", "THM-M-0364", "THM-M-0366", "THM-M-1171"}
    manifest_ids = {row["theorem_id"] for row in manifest["targets"]}
    assert neighbor_ids <= manifest_ids
    manifest_names = {row["theorem_id"]: row["name"] for row in manifest["targets"]}
    assert all(manifest_names[row["theorem_id"]] == row["name"] for row in instance["neighbor_target_boundaries"])

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

    for name in ("README.md", "instance.json", "scope-map.md", "source-statement-crosswalk.md", "validation.md", "intake-receipt.json"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    lean_probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b", lean_probe)
    lake_link = ROOT / "Formalizations/Lean/.lake"
    assert lake_link.is_symlink()
    assert not git("status", "--short", "--", "Docs/Stage1_Execution_DAG_rev-5.6.json", "Docs/Stage1_Blueprint_rev-5.6.md")

    required_packet_keys = {
        "item_id", "changed_paths", "commands", "output_summary", "base_revision", "known_failures", "state"
    }
    assert set(selftest) == required_packet_keys
    assert selftest["known_failures"] == receipt["known_failures"]
    print("intake invariant check: ok (THM-M-0299 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
