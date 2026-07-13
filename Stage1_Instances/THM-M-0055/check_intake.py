#!/usr/bin/env python3
"""Fail-closed scoped validator for the THM-M-0055 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0055"
ITEM_ID = "S56-M-0055-INTAKE"
RANK = 1522
BASE_REVISION = "f3910e9d9c9dde383801913343b9244462e6173a"
BASE_TREE = "28f0e995eac01d75999b013a02e02eb792c07754"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
ROOT_VECTOR = {"H": "H1", "M": "M3", "R": "R4"}
SPIELMAN_PDF_SHA256 = "6b70ebd45e3369754ae597a42fda8531a8cb35407d16afef65dfff509369861c"
OWNED_FILES = {
    "IntakeProbe.lean",
    "README.md",
    "check_intake.py",
    "instance.json",
    "intake-receipt.json",
    "scope-map.md",
    "source-statement-crosswalk.md",
    "statement-blocker.json",
    "statement-blocker.md",
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
    "applicable_targets_sha256": "Docs/Stage1_Blueprint_Applicable_Theorems.md",
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
    "rayleigh_source_sha256": "Mathlib/Analysis/InnerProductSpace/Rayleigh.lean",
    "inner_product_spectrum_source_sha256":
        "Mathlib/Analysis/InnerProductSpace/Spectrum.lean",
    "matrix_hermitian_source_sha256": "Mathlib/Analysis/Matrix/Hermitian.lean",
    "matrix_spectrum_source_sha256": "Mathlib/Analysis/Matrix/Spectrum.lean",
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


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first - 1:last])).hexdigest()


def run_lean_probe() -> bytes:
    env = os.environ.copy()
    env.update({"LC_ALL": "C", "TZ": "UTC"})
    result = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0055/IntakeProbe.lean"],
        cwd=ROOT / "Formalizations/Lean",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        env=env,
        timeout=120,
    )
    assert result.returncode == 0, result.stdout.decode(errors="replace")
    return result.stdout


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
    assert packet["commands"] == receipt["worker_packet_commands"]
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
    blocker = load(HERE / "statement-blocker.json")
    receipt = load(HERE / "intake-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "瑞利商定理",
        "category": "代数学 / 线性代数",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 78,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    for field in (
        "execution_rank", "legacy_priority_slot", "baseline", "rework_required",
        "legacy_artifacts_accepted", "target_lane", "intake_score",
        "source_status_untrusted", "lifecycle_mode", "theorem_complete",
    ):
        assert instance[field] == target[field]
    assert instance["name_zh"] == target["name"]
    assert instance["category"] == target["category"]

    intake = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert intake == {
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
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is instance["canonical_claim"] is None
    assert "recognizable_finite_matrix_rayleigh" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    for key in (
        "module", "declaration_or_expression", "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[key] is None
    assert formal["gate_state"] == blocker["status"]
    assert blocker["canonical_statement"] is blocker["canonical_formal_target"] is None
    assert blocker["elaborated_expression_hash"] is blocker["environment_fingerprint"] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False
    assert blocker["audit_complete"] is blocker["theorem_complete"] is False
    assert "No canonical statement, H0, M0, R0" in instance["status_boundary"]

    modern = instance["source_candidates_not_credited"][1]
    assert modern["observed_source_sha256"] == SPIELMAN_PDF_SHA256
    assert modern["observed_source_bytes"] == 2902506
    assert "Theorem 2.0.1" in modern["candidate_locator"]
    historical = instance["source_candidates_not_credited"][0]
    assert historical["doi"] == "10.1112/plms/s1-4.1.357"

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions[
        "current_repository_math_source_blob"
    ]
    assert git("rev-parse", "HEAD:Docs/Stage0_Blueprint.md") == revisions[
        "current_stage0_blueprint_blob"
    ]
    assert git(
        "rev-parse",
        f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md',
    ) == revisions["repository_source_record_blob"]
    assert revisions["repository_record_excerpt_sha256"] == excerpt_sha256(
        ROOT / "Docs/researches/math_theorems.md", 412, 417
    )
    assert revisions["stage0_projection_excerpt_sha256"] == excerpt_sha256(
        ROOT / "Docs/Stage0_Blueprint.md", 1618, 1643
    )
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert not git("status", "--short", "--untracked-files=all", cwd=mathlib)
    for field, relative in MATHLIB_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert revisions["lake_symlink_target_string_sha256"] == hashlib.sha256(lake_target).hexdigest()

    dependency = ITEM_ID
    assert len(dag["tasks"]) == 6
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0055-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = dag["tasks"][layer - 1]
        assert task["id"] == task_id and task["depends_on"] == [dependency]
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [
            f"Stage1_Instances/{THEOREM_ID}"
        ]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["state"] == "open" and task["evidence_ids"] == []
        dependency = task_id

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    catalog_record = "\n".join(catalog.splitlines()[411:417])
    for literal in (
        "**瑞利商定理**",
        "- 提出者: John William Strutt (Rayleigh)",
        "- 时间: 1870",
        "- 陈述: Hermite矩阵特征值的变分刻画",
        "- 形式化状态: 已验证",
    ):
        assert literal in catalog_record
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    stage0_record = "\n".join(stage0.splitlines()[1617:1643])
    assert "THM-M-0055 瑞利商定理" in stage0_record
    assert "- 精确定义与前提条件: 待补充" in stage0_record
    assert "- 现有 machine-checked 状态: 待补充" in stage0_record
    neighbor_ids = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert neighbor_ids == {
        "THM-M-0043", "THM-M-0053", "THM-M-0054", "THM-M-0056",
        "THM-M-1390", "THM-M-1450",
    }

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual_files == OWNED_FILES
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    digests = receipt["owned_artifact_sha256"]
    assert set(digests) == {f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES}
    for relative, expected in digests.items():
        if relative.endswith("/intake-receipt.json"):
            assert expected == "self_referential_excluded_from_provisional_digest"
        else:
            assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["root_vector_before"] == {
        "H": "unclassified", "M": "unclassified", "R": "unclassified"
    }
    assert receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["first_failed_gate"] == "master_acceptance"
    assert receipt["lifecycle_after"] == "planned"
    assert receipt["owner"] == "Stage1 integration lane"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]
    assert isinstance(receipt["known_failures"], list) and receipt["known_failures"]
    assert receipt["probe_stdout_sha256"] == hashlib.sha256(run_lean_probe()).hexdigest()
    assert blocker["formal_probe"]["probe_stdout_sha256"] == receipt["probe_stdout_sha256"]

    for name in OWNED_FILES:
        data = (HERE / name).read_bytes()
        assert data and data.endswith(b"\n"), f"missing final newline: {name}"
        for line_number, line in enumerate(data.splitlines(), start=1):
            assert line.rstrip(b" \t") == line, f"trailing whitespace: {name}:{line_number}"
    prose = "\n".join(
        (HERE / name).read_text(encoding="utf-8")
        for name in OWNED_FILES
        if name.endswith((".md", ".json"))
    )
    assert "/home/" not in prose and ".cron/stage1-rev56/workers" not in prose

    if args.worker_packet:
        check_worker_packet(args.worker_packet, receipt)
    print("check_intake: ok")


if __name__ == "__main__":
    main()
