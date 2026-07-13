#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0283 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0283"
ITEM_ID = "S56-M-0283-INTAKE"
RANK = 1289
BASE_REVISION = "2eea98305d46266f078a50cf0e85853bf6a5e702"
BASE_TREE = "02279a8caa5f31ed8e37e35c8584a336eed9b974"
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
    assert target["name"] == instance["name_zh"] == "马尔可夫不等式"
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

    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] in {"[ ]", "[_]"} and item["depends_on"] == []
    if packet is not None:
        assert item["state"] == "[ ]", "worker base must precede provisional integration"
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["literal_source_claim_zh"] == "非负随机变量的概率上界"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None

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
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
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
    assert hashlib.sha256(b"".join(source_lines[2033:2039])).hexdigest() == source["repository_record_excerpt_sha256"]
    assert hashlib.sha256(b"".join(source_lines[7251:7257])).hexdigest() == source["repository_duplicate_excerpt_sha256"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert source[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == source["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == source["mathlib_tree"] == MATHLIB_TREE
    assert source["mathlib_lintegral_candidate_source_sha256"] == sha256(
        mathlib / "Mathlib/MeasureTheory/Integral/Lebesgue/Markov.lean"
    )
    assert source["mathlib_real_candidate_source_sha256"] == sha256(
        mathlib / "Mathlib/MeasureTheory/Integral/Bochner/Basic.lean"
    )

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**马尔可夫不等式**") == 2
    assert catalog.count("- 陈述: 非负随机变量的概率上界") == 2
    assert (
        "**马尔可夫不等式**\n- 提出者: Andrey Markov\n- 时间: 1889\n"
        "- 陈述: 非负随机变量的概率上界"
    ) in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0283 马尔可夫不等式" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert {candidate["declaration"] for candidate in instance["formal_candidates_not_credited"]} == {
        "MeasureTheory.mul_meas_ge_le_lintegral₀",
        "MeasureTheory.mul_meas_ge_le_lintegral",
        "MeasureTheory.meas_ge_le_lintegral_div",
        "MeasureTheory.mul_meas_ge_le_integral_of_nonneg",
    }

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0283-{suffix}"
        expected_tasks.append((task_id, [dependency], layer))
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
    assert receipt["accepted"] is False and receipt["content_addressed"] is False
    assert receipt["selftest_result"] == "pass"
    assert len(receipt["structured_validation_recipes"]) == 2
    assert all(recipe["network_policy"] == "denied" for recipe in receipt["structured_validation_recipes"])
    assert receipt["worker_input_hashes"]["intake_probe_sha256"] == sha256(HERE / "IntakeProbe.lean")
    assert receipt["worker_input_hashes"]["lean_probe_output_sha256"] == "0820c158f5436f5e120a2561389c150994d5933e5ca1ba5c3159ea9811dd428d"
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    if packet is not None:
        assert set(packet) == PACKET_KEYS
        assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
        assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == expected_changed
        assert isinstance(packet["commands"], list) and packet["commands"]
        assert isinstance(packet["output_summary"], str) and packet["output_summary"]
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

    print("intake invariant check: ok (THM-M-0283 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
