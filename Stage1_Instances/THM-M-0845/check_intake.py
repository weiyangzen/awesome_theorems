#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0845."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0845"
ITEM_ID = "S56-M-0845-INTAKE"
BASE_REVISION = "444860f481e8bbf64a3357008fd4d01a52006f08"
BASE_TREE = "dee24a14497f877ebd81712a99d2da08de62d7ad"
SOURCE_RECORD_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_RECORD_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
CURRENT_SOURCE_BLOB = "b78ec1f48495aa5747ef252665ab58e418d195e4"
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
SOURCE_HASHES = {
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
MATHLIB_SOURCE_HASHES = {
    "mathlib_simple_graph_maps_source_sha256": (
        "Mathlib/Combinatorics/SimpleGraph/Maps.lean"
    ),
    "mathlib_fintype_pi_source_sha256": "Mathlib/Data/Fintype/Pi.lean",
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


def canonical_json_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def path_manifest_sha256(paths: list[str]) -> str:
    digest = hashlib.sha256()
    for relative in sorted(paths):
        digest.update(
            relative.encode()
            + b"\0"
            + hashlib.sha256((ROOT / relative).read_bytes()).digest()
        )
    return digest.hexdigest()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    assert packet["schema_version"] == "stage1-worker-selftest/1.0"
    assert packet["item_id"] == ITEM_ID and packet["theorem_id"] == THEOREM_ID
    assert packet["intent"] == "intake" and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["receipt_id"] == receipt["receipt_id"]
    assert packet["accepted_receipt_ids"] == []
    assert packet["content_addressed_recipe_ids"] == receipt["content_addressed_recipe_ids"]
    assert packet["content_addressed_receipt_ids"] == receipt["content_addressed_receipt_ids"]
    assert packet["content_addressed_log_ids"] == receipt["content_addressed_log_ids"]
    assert packet["audit_complete"] is packet["theorem_complete"] is False
    assert packet["owner"] == receipt["owner"] == "Stage1 integration lane"
    for field in (
        "validated_at",
        "review_due",
        "support_state",
        "supersession_state",
        "revocation_state",
        "incident_path",
    ):
        assert isinstance(packet[field], str) and packet[field]
    assert isinstance(packet["invalidation_inputs"], list) and packet["invalidation_inputs"]


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
    assert target["execution_rank"] == instance["execution_rank"] == 1400
    assert target["name"] == instance["name_zh"] == "图同态计数"
    assert target["category"] == instance["category"] == "组合数学 / 图论"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == 1400
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is instance["canonical_claim"] is None
    assert "not_one_stable_truth_valued_proposition" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    for key in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["foundation_profile"].startswith("lean4-foundation-planned/1.0:")
    assert instance["tcb_profile"].startswith("lean4-mathlib-tcb-planned/1.0:")
    assert instance["computation_profile"].startswith("kernel-graph-counting-planned/1.0:")
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", f"{SOURCE_RECORD_COMMIT}:Docs/researches/math_theorems.md") == revisions["repository_source_record_blob"] == SOURCE_RECORD_BLOB
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"] == CURRENT_SOURCE_BLOB
    for field, relative in SOURCE_HASHES.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert not git("status", "--short", cwd=mathlib), "pinned mathlib source is dirty"
    for field, relative in MATHLIB_SOURCE_HASHES.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"

    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0845-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = dag["tasks"][layer - 1]
        assert task["id"] == task_id and task["depends_on"] == [dependency]
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["state"] == "open" and task["evidence_ids"] == []
        dependency = task_id

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    catalog_block = "\n".join(
        [
            "**图同态计数**",
            "- 提出者: 众多数学家",
            "- 时间: 20世纪",
            "- 陈述: 子图同态的计数",
            "- 重要性: 高",
            "- 形式化状态: 已验证",
        ]
    )
    assert catalog.count(catalog_block) == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    stage0_start = stage0.index("- [ ] THM-M-0845 图同态计数")
    stage0_end = stage0.index("\n- [ ] THM-M-0846 ", stage0_start)
    stage0_block = stage0[stage0_start:stage0_end]
    assert "- 定理内容: 子图同态的计数" in stage0_block
    assert "- 精确定义与前提条件: 待补充" in stage0_block
    assert "- 现有 machine-checked 状态: 待补充" in stage0_block

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert all((ROOT / path).is_file() for path in instance["public_merge_targets"])
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["owner"] == "Stage1 integration lane"
    assert receipt["validated_at"] == "2026-07-13T19:50:21+08:00"
    assert receipt["review_due"] == "before master acceptance or any dependent statement work"
    assert isinstance(receipt["invalidation_inputs"], list) and receipt["invalidation_inputs"]
    assert receipt["support_state"] == "provisional_worker_only"
    assert receipt["supersession_state"] == "current_unsuperseded_worker_report"
    assert receipt["revocation_state"] == "not_revoked"
    assert isinstance(receipt["incident_path"], str) and receipt["incident_path"]
    assert receipt["first_failed_gate"] == "master_acceptance_of_provisional_intake"
    assert receipt["first_open_downstream_gate"].startswith("S56-M-0845-STATEMENT:")

    recipes = {row["recipe_id"]: row for row in receipt["structured_validation_recipes"]}
    actions = {row["recipe_id"]: row for row in receipt["validation_actions"]}
    structure_id = "S56-M-0845-INTAKE-RECIPE-STRUCTURE"
    lean_id = "S56-M-0845-INTAKE-RECIPE-LEAN-PROBE"
    assert set(recipes) == set(actions) == {structure_id, lean_id}
    assert actions[structure_id]["recipe_sha256"] == canonical_json_sha256(recipes[structure_id])
    assert actions[lean_id]["recipe_sha256"] == canonical_json_sha256(recipes[lean_id])
    assert actions[structure_id]["input_manifest_sha256"] == path_manifest_sha256([
        "Docs/Stage1_Targets_rev-5.6.json",
        "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "Stage1_Instances/THM-M-0845/instance.json",
        "Stage1_Instances/THM-M-0845/task-dag.json",
        "Stage1_Instances/THM-M-0845/check_intake.py",
    ])
    assert actions[lean_id]["input_manifest_sha256"] == path_manifest_sha256([
        "Formalizations/Lean/lean-toolchain",
        "Formalizations/Lean/lake-manifest.json",
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph/Maps.lean",
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Data/Fintype/Pi.lean",
        "Stage1_Instances/THM-M-0845/IntakeProbe.lean",
    ])
    assert all(action["exit_code"] == 0 for action in actions.values())
    assert all(action["covered_ids"] == [ITEM_ID] for action in actions.values())
    assert set(receipt["content_addressed_recipe_ids"]) == {
        f"sha256:{action['recipe_sha256']}" for action in actions.values()
    }
    assert set(receipt["content_addressed_receipt_ids"]) == {
        f"sha256:{canonical_json_sha256(action)}" for action in actions.values()
    }
    assert set(receipt["content_addressed_log_ids"]) == {
        f"sha256:{action['log_sha256']}" for action in actions.values()
    }
    expected_hashed_paths = [".stage1-worker-selftest.json"] + sorted(
        f"Stage1_Instances/{THEOREM_ID}/{name}"
        for name in OWNED_FILES
        if name != "intake-receipt.json"
    )
    assert receipt["dirty_input_evidence"]["non_self_referential_manifest_sha256"] == \
        path_manifest_sha256(expected_hashed_paths)
    artifact_hashes = receipt["owned_artifact_sha256"]
    assert artifact_hashes[f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json"] == \
        "self_referential_excluded_from_provisional_digest"
    for relative in expected_hashed_paths:
        assert artifact_hashes[relative] == sha256(ROOT / relative)

    for path in HERE.iterdir():
        if path.is_file():
            data = path.read_bytes()
            assert data.endswith(b"\n"), f"missing final newline: {path.name}"
            assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {path.name}"
            assert all(
                not line.endswith((b" ", b"\t")) for line in data.splitlines()
            ), f"trailing whitespace: {path.name}"
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
        private_home_prefix = "/" + "home" + "/"
        private_cron_segment = "." + "cron" + "/"
        assert private_home_prefix not in text and private_cron_segment not in text
        forbidden_completion_claim = "theorem_complete" + "=true"
        assert forbidden_completion_claim not in text

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0845 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
