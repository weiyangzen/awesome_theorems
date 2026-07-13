#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0977."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0977"
ITEM_ID = "S56-M-0977-INTAKE"
RANK = 1511
BASE_REVISION = "9c75282d42a7ef447d885d1d56997a79418bcd8a"
BASE_TREE = "cc5285432a02107fadffb68c698690d1b98ac5f2"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
ROOT_VECTOR = {"H": "H1", "M": "M3", "R": "R4"}
OWNED_FILES = {
    "IntakeProbe.lean",
    "README.md",
    "check_intake.py",
    "instance.json",
    "intake-receipt.json",
    "scope-map.md",
    "source-statement-crosswalk.md",
    "task-dag.json",
    "validation.md",
}
TASK_SUFFIXES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)
SOURCE_HASH_FIELDS = {
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
    "mathlib_basic_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Probability/Moments/Basic.lean"
    ),
    "legacy_s1_m_273_source_sha256": (
        "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_273.lean"
    ),
}
PROBE_DECLARATIONS = {
    "ProbabilityTheory.measure_ge_le_exp_mul_mgf",
    "ProbabilityTheory.measure_le_le_exp_mul_mgf",
    "ProbabilityTheory.measure_ge_le_exp_cgf",
    "ProbabilityTheory.measure_le_le_exp_cgf",
    "ProbabilityTheory.iIndepFun.integrable_exp_mul_sum",
    "ProbabilityTheory.iIndepFun.mgf_sum",
    "ProbabilityTheory.iIndepFun.cgf_sum",
}


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_sha256(path: Path, first_line: int, last_line: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first_line - 1 : last_line])).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def canonical_manifest_hash(target: dict) -> str:
    encoded = (json.dumps(target, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    return hashlib.sha256(encoded).hexdigest()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    assert manifest["schema_version"] == "stage1-target-set/5.6.2"
    assert manifest["scope"]["covered_targets"] == 1546
    matches = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    assert matches == [
        {
            "execution_rank": RANK,
            "legacy_priority_slot": None,
            "theorem_id": THEOREM_ID,
            "name": "Chernoff界",
            "category": "组合数学 / 计数组合",
            "source_status_untrusted": "已验证",
            "baseline": "L0",
            "rework_required": True,
            "legacy_artifacts_accepted": False,
            "target_lane": "hard_statement_first_partial_verification",
            "intake_score": 86,
            "lifecycle_mode": "planned",
            "theorem_complete": False,
        }
    ]
    target = matches[0]
    revisions = instance["source_revisions"]
    assert canonical_manifest_hash(target) == revisions["manifest_entry_sha256"]
    for field in (
        "execution_rank",
        "legacy_priority_slot",
        "category",
        "baseline",
        "rework_required",
        "legacy_artifacts_accepted",
        "target_lane",
        "intake_score",
        "source_status_untrusted",
        "lifecycle_mode",
        "theorem_complete",
    ):
        assert instance[field] == target[field], f"manifest mismatch: {field}"
    assert instance["name_zh"] == target["name"]

    intake = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert intake["theorem_id"] == THEOREM_ID and intake["execution_rank"] == RANK
    assert intake["phase"] == "intake" and intake["layer"] == 0
    assert intake["state"] == "[ ]" and intake["depends_on"] == []
    assert intake["attempts"] == 0 and intake["children"] == []
    assert intake["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert intake["deliverable"] == (
        "Create the theorem dossier, scope map, and source-statement crosswalk."
    )
    assert intake["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert dag["lifecycle_mode"] == instance["lifecycle_mode"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for field in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[field] is None
    assert set(formal["declaration_candidates_not_credited"]) == PROBE_DECLARATIONS
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    assert revisions["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
    assert subprocess.run(
        ["git", "merge-base", "--is-ancestor", BASE_REVISION, "HEAD"],
        cwd=ROOT,
        check=False,
    ).returncode == 0
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == (
        revisions["current_repository_math_source_blob"]
    )
    assert git(
        "rev-parse",
        f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md',
    ) == revisions["repository_source_record_blob"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
        assert receipt["source_inputs"][relative] == f"sha256:{revisions[field]}"
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 7134, 7139) == (
        revisions["repository_record_excerpt_sha256"]
    )
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 7259, 7264) == (
        revisions["duplicate_record_excerpt_sha256"]
    )
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 26632, 26657) == (
        revisions["stage0_excerpt_sha256"]
    )
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 27069, 27094) == (
        revisions["duplicate_stage0_excerpt_sha256"]
    )
    assert sha256(HERE / "IntakeProbe.lean") == revisions["intake_probe_sha256"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    assert git(
        "log",
        "-1",
        "--format=%H",
        "--",
        "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_273.lean",
    ) == (
        revisions["legacy_s1_m_273_introduction_commit"]
    )

    dependency = ITEM_ID
    expected_tasks: list[tuple[str, list[str]]] = []
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0977-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        expected_tasks.append((task_id, [dependency]))
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [
            f"Stage1_Instances/{THEOREM_ID}"
        ]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == [] and task["state"] == "open"
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**Chernoff界**") == 1
    assert catalog.count("**切尔诺夫界**") == 1
    assert catalog.count("- 陈述: 独立随机变量和的尾概率") == 2
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0977 Chernoff界" in stage0 and "THM-M-0993 切尔诺夫界" in stage0
    assert stage0.count("- 精确定义与前提条件: 待补充") >= 2
    assert instance["duplicate_source_record_boundary"]["theorem_id"] == "THM-M-0993"
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {
        "THM-M-0993",
        "THM-M-0975",
        "THM-M-0978",
        "THM-M-0979",
        "THM-M-0980",
    }

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change" and receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["selftest_result"] == "pass"
    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["mathlib_revision"] == MATHLIB_REVISION
    assert worker_inputs["mathlib_tree"] == MATHLIB_TREE
    assert worker_inputs["intake_probe_sha256"] == revisions["intake_probe_sha256"]
    assert worker_inputs["lean_probe_output_sha256"] == revisions["lean_probe_output_sha256"]
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert worker_inputs["lake_symlink_target_string"] == (
        f"sha256:{hashlib.sha256(lake_target).hexdigest()}"
    )
    for recipe in receipt["structured_validation_recipes"]:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["exit_code"] == 0

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"
    for path in list(HERE.iterdir()) + ([args.worker_packet.resolve()] if args.worker_packet else []):
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"{path.name} is missing a final newline"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|constant|opaque|unsafe)[ \t]",
        re.MULTILINE,
    )
    assert prohibited.search(probe) is None
    for declaration in PROBE_DECLARATIONS:
        assert f"#check {declaration}" in probe and f"#print axioms {declaration}" in probe

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0977 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
