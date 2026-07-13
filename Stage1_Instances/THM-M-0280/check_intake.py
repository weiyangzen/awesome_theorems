#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0280 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0280"
ITEM_ID = "S56-M-0280-INTAKE"
RANK = 1286
BASE_REVISION = "2eea98305d46266f078a50cf0e85853bf6a5e702"
BASE_TREE = "02279a8caa5f31ed8e37e35c8584a336eed9b974"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROBE_OUTPUT_SHA256 = "06295a3965083752673a8dc0ced2ed75c9919708deb3ff73b3c9f4f2d164d2cb"
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
    "mathlib_triangle_source_sha256": "Mathlib/MeasureTheory/Function/LpSeminorm/TriangleInequality.lean",
    "mathlib_lpnorm_source_sha256": "Mathlib/MeasureTheory/Function/LpSeminorm/LpNorm.lean",
    "mathlib_lpspace_source_sha256": "Mathlib/MeasureTheory/Function/LpSpace/Basic.lean",
    "mathlib_integral_mean_source_sha256": "Mathlib/MeasureTheory/Integral/MeanInequalities.lean",
    "mathlib_finite_mean_source_sha256": "Mathlib/Analysis/MeanInequalities.lean",
}
PROBE_DECLARATIONS = [
    "MeasureTheory.eLpNorm_add_le",
    "MeasureTheory.lpNorm_add_le",
    "ENNReal.lintegral_Lp_add_le",
    "Real.Lp_add_le",
]


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_sha256(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1 : end])).hexdigest()


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
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]


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
    assert target["name"] == instance["name_zh"] == "闵可夫斯基不等式"
    assert target["category"] == instance["category"] == "分析学 / 实分析"
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
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
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
    assert git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md') == revisions["repository_source_record_blob_at_origin"]
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["repository_source_record_blob_at_base"]
    assert git("rev-parse", "HEAD:Docs/Stage0_Blueprint.md") == revisions["stage0_projection_blob_at_base"]
    for field, relative in SOURCE_HASHES.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    assert revisions["repository_record_excerpt_sha256"] == excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 2013, 2018)
    assert revisions["stage0_projection_excerpt_sha256"] == excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 7738, 7763)

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    for field, relative in MATHLIB_SOURCE_HASHES.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib source hash: {field}"

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0280-{suffix}"
        expected_tasks.append((task_id, [dependency], layer))
        authoritative = next(row for row in execution_dag["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["state"] == "open" and task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"], task["layer"]) for task in dag["tasks"]] == expected_tasks

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**闵可夫斯基不等式**" in catalog
    assert "- 提出者: Hermann Minkowski" in catalog
    assert "- 时间: 1896" in catalog
    assert "- 陈述: L^p空间的三角不等式" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0280 闵可夫斯基不等式" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    neighbors = {row["theorem_id"]: row["name"] for row in instance["neighbor_target_boundaries"]}
    assert neighbors == {
        "THM-M-0279": "赫尔德不等式",
        "THM-M-0281": "延森不等式",
        "THM-M-0417": "闵可夫斯基定理",
        "THM-M-0418": "闵可夫斯基界",
    }
    assert {row["theorem_id"]: row["name"] for row in manifest["targets"] if row["theorem_id"] in neighbors} == neighbors

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["known_failures"] and receipt["selftest_result"] == "pass"

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), f"trailing whitespace: {path.name}"
    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    for declaration in PROBE_DECLARATIONS:
        assert f"#check {declaration}" in probe
        assert f"#print axioms {declaration}" in probe
    lean_run = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0280/IntakeProbe.lean"],
        cwd=ROOT / "Formalizations/Lean",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=120,
    )
    assert lean_run.returncode == 0, lean_run.stdout
    assert hashlib.sha256(lean_run.stdout.encode()).hexdigest() == PROBE_OUTPUT_SHA256
    for declaration in PROBE_DECLARATIONS:
        assert declaration in lean_run.stdout
    assert lean_run.stdout.count("[propext, Classical.choice, Quot.sound]") == 4

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet.resolve(), receipt)

    print("intake invariant check: ok (THM-M-0280 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
