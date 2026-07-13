#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0976 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0976"
ITEM_ID = "S56-M-0976-INTAKE"
RANK = 1510
BASE_REVISION = "9c75282d42a7ef447d885d1d56997a79418bcd8a"
BASE_TREE = "cc5285432a02107fadffb68c698690d1b98ac5f2"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
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
PACKET_KEYS = {
    "item_id",
    "changed_paths",
    "commands",
    "output_summary",
    "base_revision",
    "known_failures",
    "state",
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
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain an object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--worker-packet",
        type=Path,
        help="optional provisional worker packet; absent after integration",
    )
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution_dag = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")
    packet = load(args.worker_packet.resolve()) if args.worker_packet is not None else None

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    item = next(row for row in execution_dag["items"] if row["id"] == ITEM_ID)

    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "McDiarmid不等式"
    assert target["category"] == instance["category"] == "组合数学 / 计数组合"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] in {"[ ]", "[_]"} and item["depends_on"] == []
    if packet is not None:
        assert item["state"] == "[ ]", "worker base must precede provisional integration"
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["normative_profile"] == instance["normative_profile"]
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["literal_source_claim_zh"] == "有界差函数的集中"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None

    formal = instance["canonical_formal_target"]
    for key in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[key] is None
    assert formal["declaration_candidates"] == []
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is dag["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    source = instance["source_revisions"]
    assert source["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert source["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    if packet is not None:
        assert git("rev-parse", "HEAD") == BASE_REVISION
        assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    elif git("rev-parse", "HEAD") == BASE_REVISION:
        assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert git("rev-parse", f'{source["repository_source_record_commit"]}:Docs/researches/math_theorems.md') == source["repository_source_record_blob"]
    assert git("hash-object", "Docs/researches/math_theorems.md") == source["current_repository_math_source_blob"]
    source_lines = (ROOT / "Docs/researches/math_theorems.md").read_bytes().splitlines(keepends=True)
    excerpt_hashes = [
        hashlib.sha256(b"".join(source_lines[start:end])).hexdigest()
        for start, end in ((7126, 7132), (7293, 7299), (7918, 7924))
    ]
    assert excerpt_hashes == [source["repository_record_excerpt_sha256"]] * 3
    assert source["repository_duplicate_probability_excerpt_sha256"] == excerpt_hashes[1]
    assert source["repository_duplicate_process_excerpt_sha256"] == excerpt_hashes[2]
    stage0_lines = (ROOT / "Docs/Stage0_Blueprint.md").read_bytes().splitlines(keepends=True)
    assert hashlib.sha256(b"".join(stage0_lines[26604:26630])).hexdigest() == source["stage0_projection_excerpt_sha256"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert source[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == source["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == source["mathlib_tree"] == MATHLIB_TREE
    assert source["mathlib_independence_source_sha256"] == sha256(
        mathlib / "Mathlib/Probability/Independence/Basic.lean"
    )
    assert source["mathlib_subgaussian_source_sha256"] == sha256(
        mathlib / "Mathlib/Probability/Moments/SubGaussian.lean"
    )
    assert source["mathlib_function_update_source_sha256"] == sha256(
        mathlib / "Mathlib/Logic/Function/Basic.lean"
    )
    assert source["repo_hoeffding_wrapper_sha256"] == sha256(
        ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_274.lean"
    )

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**McDiarmid不等式**") == 3
    assert catalog.count("- 陈述: 有界差函数的集中") == 3
    assert (
        "**McDiarmid不等式**\n- 提出者: Colin McDiarmid\n- 时间: 1989\n"
        "- 陈述: 有界差函数的集中"
    ) in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0976 McDiarmid不等式" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {
        "THM-M-0974", "THM-M-0975", "THM-M-0977", "THM-M-0978", "THM-M-0994", "THM-M-1080"
    }
    assert instance["formal_candidates_not_credited"] == []

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0976-{suffix}"
        expected_tasks.append((task_id, [dependency], layer))
        authoritative = next(row for row in execution_dag["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        assert task["phase"] == authoritative["phase"]
        assert task["owned_paths"] == authoritative["owned_paths"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        dependency = task_id
    assert [(task["id"], task["depends_on"], task["layer"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" and task["evidence_ids"] == [] for task in dag["tasks"])

    actual_artifacts = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual_artifacts == OWNED_FILES
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["proposed_state"] == "[_]"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["accepted"] is False and receipt["content_addressed"] is False
    assert receipt["selftest_result"] == "pass"
    assert len(receipt["structured_validation_recipes"]) == 2
    assert all(recipe["network_policy"] == "denied" for recipe in receipt["structured_validation_recipes"])
    assert receipt["worker_input_hashes"]["intake_probe_sha256"] == sha256(HERE / "IntakeProbe.lean")
    assert receipt["worker_input_hashes"]["lean_probe_output_sha256"] == "bb6bde64a3e5db9190f8d848ba06ea051dc5161cca547de88a9d06e5f3136874"
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["content_addressed_recipe_ids"] == receipt["content_addressed_receipt_ids"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]

    expected_hashed_inputs = expected_changed - {f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json"}
    assert set(receipt["untracked_input_hashes"]) == expected_hashed_inputs
    for relative, expected in receipt["untracked_input_hashes"].items():
        assert expected == f"sha256:{sha256(ROOT / relative)}", f"stale untracked input hash: {relative}"
    for recipe in receipt["structured_validation_recipes"]:
        assert recipe["covered_node_ids"] == [ITEM_ID]
        assert recipe["covered_obligation_ids"] == []
        assert recipe["covered_declarations"] == []
        assert recipe["expected_outputs"]
        assert all(
            set(output) == {"path_or_stream", "semantic_hash_policy"}
            and isinstance(output["path_or_stream"], str)
            and isinstance(output["semantic_hash_policy"], str)
            and output["path_or_stream"]
            and output["semantic_hash_policy"]
            for output in recipe["expected_outputs"]
        )

    prohibited = re.compile(r"(?<![A-Za-z0-9_])(sorry|admit|sorryAx|axiom|constant|opaque|unsafe)(?![A-Za-z0-9_])")
    assert prohibited.search((HERE / "IntakeProbe.lean").read_text(encoding="utf-8")) is None

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    if packet is not None:
        assert set(packet) == PACKET_KEYS
        assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
        assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == expected_changed
        assert packet["commands"] == receipt["worker_packet_commands"]
        assert isinstance(packet["commands"], list) and packet["commands"]
        assert isinstance(packet["output_summary"], str) and packet["output_summary"]
        assert packet["output_summary"] == receipt["output_summary"]
        assert packet["known_failures"] == receipt["known_failures"]

    checked_paths = list(HERE.iterdir())
    if args.worker_packet is not None:
        checked_paths.append(args.worker_packet.resolve())
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

    print("intake invariant check: ok (THM-M-0976 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
