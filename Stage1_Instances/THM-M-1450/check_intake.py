#!/usr/bin/env python3
"""Validate the fail-closed THM-M-1450 planned intake."""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-1450"
ITEM_ID = "S56-M-1450-INTAKE"
RANK = 1127
BASE_REVISION = "03bed3c211cb739ccd2629908210fda0f9adf6ca"
BASE_TREE = "a48670276bfe2105ddbfb4057314b21056dae0cb"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
ROOT_VECTOR = {"H": "H5", "M": "M4", "R": "R4"}
RECEIPT_ID = "S56-M-1450-INTAKE-WORKER-20260713"
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
MATHLIB_HASH_FIELDS = {
    "mathlib_eigenspace_basic_source_sha256": "Mathlib/LinearAlgebra/Eigenspace/Basic.lean",
    "mathlib_matrix_to_lin_source_sha256": "Mathlib/LinearAlgebra/Matrix/ToLin.lean",
    "mathlib_spectrum_source_sha256": "Mathlib/Analysis/InnerProductSpace/Spectrum.lean",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain an object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def line_excerpt_sha256(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1 : end])).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def check_packet(path: Path, receipt: dict) -> None:
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
    assert packet["item_id"] == ITEM_ID
    assert packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION == receipt["base_revision"]
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["known_failures"] == receipt["known_failures"]
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
    assert target["name"] == instance["name_zh"] == "幂迭代"
    assert target["category"] == instance["category"] == "其他重要领域 / 数值分析"
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
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == instance["hypotheses"] == []
    assert instance["alternate_encodings"] == instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == receipt["root_vector_after"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_id"] == RECEIPT_ID
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["phase"] == "intake"
    assert receipt["content_addressed"] is False
    assert receipt["selftest_result"] == "pass"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["root_vector_before"] == {"H": "unclassified", "M": "unclassified", "R": "unclassified"}
    assert receipt["first_failed_gate"].startswith("master acceptance")
    started = datetime.datetime.fromisoformat(receipt["validation_started_at"])
    ended = datetime.datetime.fromisoformat(receipt["validation_ended_at"])
    validated = datetime.datetime.fromisoformat(receipt["validated_at"])
    assert started <= ended == validated <= datetime.datetime.now(tz=validated.tzinfo)

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    source_spec = f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md'
    assert git("rev-parse", source_spec) == revisions["repository_source_record_blob"]
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert git("rev-parse", "HEAD:Docs/Stage0_Blueprint.md") == revisions["current_stage0_blueprint_blob"]
    assert revisions["repository_record_excerpt_sha256"] == line_excerpt_sha256(
        ROOT / "Docs/researches/math_theorems.md", 10588, 10593
    )
    assert revisions["stage0_projection_excerpt_sha256"] == line_excerpt_sha256(
        ROOT / "Docs/Stage0_Blueprint.md", 39433, 39458
    )
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    for field, relative in MATHLIB_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"
    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["lean_toolchain"] == f'sha256:{revisions["lean_toolchain_file_sha256"]}'
    assert worker_inputs["lake_manifest"] == f'sha256:{revisions["lake_manifest_sha256"]}'
    assert worker_inputs["mathlib_revision"] == revisions["mathlib"]
    assert worker_inputs["mathlib_tree"] == revisions["mathlib_tree"]
    for field in MATHLIB_HASH_FIELDS:
        assert worker_inputs[field] == f"sha256:{revisions[field]}"

    phase_data = (
        ("STATEMENT", "statement", "Elaborate the exact Lean 4 target with the minimal pinned imports."),
        ("ANCHOR_AUDIT", "anchor_audit", "Audit mathlib and external Lean 4 candidates at immutable revisions."),
        ("OBLIGATION_TREE", "obligation_tree", "Freeze the obligation registry and typed proof/provenance/workflow graphs."),
        ("PROOF", "proof", "Implement or pin/import the required proof bodies without placeholders."),
        ("VALIDATION", "validation", "Run hermetic kernel, trust, provenance, and independent validation gates."),
        ("RELEASE", "release", "Reconcile evidence and decide the exact theorem-completion verdict."),
    )
    expected_tasks = []
    dependency = ITEM_ID
    for layer, (suffix, phase, deliverable) in enumerate(phase_data, start=1):
        task_id = f"S56-M-1450-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        task = dag["tasks"][layer - 1]
        assert task["phase"] == phase and task["layer"] == layer
        assert task["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == deliverable
        assert task["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"
        assert task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**幂迭代**" in catalog
    assert "- 提出者: 众多数学家" in catalog
    assert "- 时间: 20世纪" in catalog
    assert "- 陈述: 最大特征值的迭代方法" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-1450 幂迭代" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    eigenspace_source = (mathlib / MATHLIB_HASH_FIELDS["mathlib_eigenspace_basic_source_sha256"]).read_text(encoding="utf-8")
    assert "theorem HasEigenvector.pow_apply" in eigenspace_source
    spectrum_source = (mathlib / MATHLIB_HASH_FIELDS["mathlib_spectrum_source_sha256"]).read_text(encoding="utf-8")
    assert "theorem eigenvectorBasis_apply_self_apply" in spectrum_source

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    status_lines = git("status", "--short", "--untracked-files=all").splitlines()
    changed_worktree_paths = {line[3:] for line in status_lines}
    assert changed_worktree_paths == expected_changed | {"Formalizations/Lean/.lake"}
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["content_addressed_recipe_ids"] == receipt["content_addressed_receipt_ids"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    lean_probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in lean_probe for token in prohibited)
    assert "#check Module.End.HasEigenvector.pow_apply" in lean_probe
    assert "#check LinearMap.IsSymmetric.eigenvectorBasis_apply_self_apply" in lean_probe

    if args.worker_packet is not None:
        check_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-1450 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
