#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0258."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0258"
ITEM_ID = "S56-M-0258-INTAKE"
RANK = 1266
BASE_REVISION = "c6fd6dad8fcfe5fd464416cd452f50286b546978"
BASE_TREE = "5a80b61d8fa09336779f8d1453dcfe4299c9472f"
SOURCE_RECORD_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_RECORD_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
SOURCE_RECORD_BLOCK_SHA256 = "d92afb26a267e59298d9f077adcdbb155a811a6999438cd7c51a88f479a3a653"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LAKE_SYMLINK_TARGET_SHA256 = "e8714e9ebb75a5da1eeb16fdb6f50831a6cab29f115df43fa8e7535b38f59826"
LEAN_OUTPUT_SHA256 = "5ec5d2e656509f2115e3991d380ccc17d8743575569c2c442f2a913af9c2d7e4"
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
    "mathlib_unit_disc_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Complex/UnitDisc/Basic.lean"
    ),
    "mathlib_schwarz_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Complex/Schwarz.lean"
    ),
    "mathlib_complex_manifold_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Geometry/Manifold/Complex.lean"
    ),
    "mathlib_one_point_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Topology/Compactification/OnePoint/Basic.lean"
    ),
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def canonical_json_sha256(value: object) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def path_manifest_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix().encode()
        data = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


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
    assert packet["item_id"] == ITEM_ID
    assert packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"].strip()
    assert packet["known_failures"] == receipt["known_failures"]


def check_source_hashes(instance: dict, receipt: dict) -> None:
    revisions = instance["source_revisions"]
    for field, relative in SOURCE_HASHES.items():
        actual = sha256(ROOT / relative)
        assert revisions[field] == actual, f"stale instance hash: {field}"
        assert receipt["source_inputs"][relative] == f"sha256:{actual}"


def check_receipt(receipt: dict, instance: dict, dag: dict) -> None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["covered_node_ids"] == [ITEM_ID]
    assert receipt["covered_declaration_ids"] == []
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"

    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    digests = receipt["owned_artifact_sha256"]
    assert set(digests) == {f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES}
    for relative, expected in digests.items():
        if relative.endswith("/intake-receipt.json"):
            assert expected == "self_referential_excluded_from_provisional_digest"
        else:
            assert sha256(ROOT / relative) == expected, f"owned artifact hash mismatch: {relative}"

    recipes = receipt["structured_validation_recipes"]
    assert isinstance(recipes, list) and len(recipes) == 2
    for recipe in recipes:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert isinstance(recipe["env_allowlist"], dict)
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["observed_exit"] == 0
        assert recipe["covered_obligation_ids"] == [ITEM_ID]

    actions = receipt["validation_actions"]
    assert len(actions) == 2
    recipes_by_id = {recipe["recipe_id"]: recipe for recipe in recipes}
    for action in actions:
        recipe = recipes_by_id[action["recipe_id"]]
        recipe_identity = {
            "cwd": recipe["cwd"],
            "argv": recipe["argv"],
            "env_allowlist": recipe["env_allowlist"],
            "timeout_seconds": recipe["timeout_seconds"],
            "network_policy": recipe["network_policy"],
            "expected_exit": recipe["expected_exit"],
        }
        assert action["recipe_sha256"] == canonical_json_sha256(recipe_identity)
        assert action["exit_code"] == 0
        assert action["covered_obligation_ids"] == [ITEM_ID]
        assert action["covered_declarations"] == recipe["covered_declarations"]
        for field in ("recipe_sha256", "input_manifest_sha256", "stdout_sha256", "log_sha256"):
            assert re.fullmatch(r"[0-9a-f]{64}", action[field])

    action_by_id = {action["action_id"]: action for action in actions}
    structure_inputs = [
        ROOT / "Docs/Stage1_Targets_rev-5.6.json",
        ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json",
        ROOT / ".stage1-worker-selftest.json",
        HERE / "instance.json",
        HERE / "task-dag.json",
        HERE / "check_intake.py",
    ]
    assert action_by_id[f"{ITEM_ID}-ACTION-STRUCTURE"]["input_manifest_sha256"] == (
        path_manifest_hash(structure_inputs)
    )
    lean_inputs = [
        ROOT / "Formalizations/Lean/lean-toolchain",
        ROOT / "Formalizations/Lean/lake-manifest.json",
        HERE / "IntakeProbe.lean",
    ]
    assert action_by_id[f"{ITEM_ID}-ACTION-LEAN-PROBE"]["input_manifest_sha256"] == (
        path_manifest_hash(lean_inputs)
    )
    structure_stdout = (
        b"intake invariant check: ok (THM-M-0258 planned; H5/M4/R4; six open tasks)\n"
    )
    structure_hash = hashlib.sha256(structure_stdout).hexdigest()
    structure_action = action_by_id[f"{ITEM_ID}-ACTION-STRUCTURE"]
    assert structure_action["stdout_sha256"] == structure_action["log_sha256"] == structure_hash
    lean_action = action_by_id[f"{ITEM_ID}-ACTION-LEAN-PROBE"]
    assert lean_action["stdout_sha256"] == lean_action["log_sha256"] == LEAN_OUTPUT_SHA256
    assert instance["accepted_receipt_ids"] == []


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution_dag = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "沃尔夫-登乔定理"
    assert target["category"] == instance["category"] == "分析学 / 复分析"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    item = next(row for row in execution_dag["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
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
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "do_not_select_one_stable_truth_valued_proposition" in instance["canonical_claim_status"]
    assert "Denjoy-Wolff-like" in instance["statement_blocker"]
    assert "Teichmuller-space-boundary" in instance["statement_blocker"]

    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False
    formal_declarations = {
        declaration
        for candidate in instance["formal_candidates_not_credited"]
        for declaration in (
            candidate.get("declarations", [])
            + ([candidate["declaration"]] if "declaration" in candidate else [])
        )
    }
    assert formal_declarations == {
        "Complex.UnitDisc",
        "Complex.UnitDisc.norm_lt_one",
        "Complex.dist_le_dist_of_mapsTo_ball",
        "ChartedSpace",
        "IsManifold",
        "OnePoint",
        "OnePoint.isOpenEmbedding_coe",
        "OnePoint.denseRange_coe",
    }

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", f"{SOURCE_RECORD_COMMIT}:Docs/researches/math_theorems.md") == (
        revisions["repository_source_record_blob"]
    ) == SOURCE_RECORD_BLOB
    source_lines = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8").splitlines(True)
    block_hash = hashlib.sha256("".join(source_lines[1856:1862]).encode()).hexdigest()
    assert block_hash == revisions["repository_record_block_sha256"] == SOURCE_RECORD_BLOCK_SHA256
    assert revisions["mathlib"] == MATHLIB_REVISION and revisions["mathlib_tree"] == MATHLIB_TREE
    check_source_hashes(instance, receipt)

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0258-{suffix}"
        authoritative = next(row for row in execution_dag["items"] if row["id"] == task_id)
        expected_tasks.append((task_id, [dependency]))
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**沃尔夫-登乔定理**") == 1
    assert catalog.count("- 提出者: Hartmut Wolf/Ken'ichi Ohshika") == 1
    assert catalog.count("- 时间: 1990") >= 1
    assert catalog.count("- 陈述: 泰希米勒空间的边界") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0258 沃尔夫-登乔定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert "- 现有 machine-checked 状态: 待补充" in stage0

    neighbor_ids = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert neighbor_ids == {"THM-M-0255", "THM-M-0256", "THM-M-0257"}
    manifest_names = {
        row["theorem_id"]: row["name"]
        for row in manifest["targets"]
        if row["theorem_id"] in neighbor_ids
    }
    assert manifest_names == {
        "THM-M-0255": "拟共形映射理论",
        "THM-M-0256": "泰希米勒理论",
        "THM-M-0257": "阿尔福斯-贝尔斯定理",
    }

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    check_receipt(receipt, instance, dag)
    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["mathlib_revision"] == MATHLIB_REVISION
    assert worker_inputs["mathlib_tree"] == MATHLIB_TREE
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("-C", str(mathlib), "rev-parse", "HEAD") == MATHLIB_REVISION
    assert git("-C", str(mathlib), "rev-parse", "HEAD^{tree}") == MATHLIB_TREE
    assert git("-C", str(mathlib), "status", "--short") == ""
    for field, relative in MATHLIB_SOURCE_HASHES.items():
        assert worker_inputs[field] == sha256(ROOT / relative)
    lake_link = ROOT / "Formalizations/Lean/.lake"
    assert lake_link.is_symlink()
    assert hashlib.sha256(os.readlink(lake_link).encode()).hexdigest() == LAKE_SYMLINK_TARGET_SHA256

    for path in HERE.iterdir():
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
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b", probe)

    started_at = datetime.fromisoformat(receipt["validation_started_at"])
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    assert started_at <= datetime.fromisoformat(receipt["validation_ended_at"]) == validated_at
    assert validated_at <= datetime.now(timezone.utc).astimezone()
    assert receipt["platform"]["operating_system"] == platform.system()
    assert receipt["platform"]["architecture"] == platform.machine()
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet.resolve(), receipt)

    print("intake invariant check: ok (THM-M-0258 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
