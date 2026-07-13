#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0051 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0051"
ITEM_ID = "S56-M-0051-INTAKE"
RANK = 1520
BASE_REVISION = "d849f42c82f9da2e07c481c7beaeba6d92f86e19"
BASE_TREE = "874c7795eb7b2cc49d6c8479c316b09b039e9786"
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
MATHLIB_SOURCE_HASH_FIELDS = {
    "exterior_algebra_basic_source_sha256": "Mathlib/LinearAlgebra/ExteriorAlgebra/Basic.lean",
    "exterior_algebra_grading_source_sha256": "Mathlib/LinearAlgebra/ExteriorAlgebra/Grading.lean",
    "finite_dimensional_lemmas_source_sha256": "Mathlib/LinearAlgebra/FiniteDimensional/Lemmas.lean",
    "cross_product_source_sha256": "Mathlib/LinearAlgebra/CrossProduct.lean",
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
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["output_summary"] == receipt["output_summary"]
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

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "格拉斯曼恒等式"
    assert target["category"] == instance["category"] == "代数学 / 线性代数"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 78
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    authoritative = [row for row in execution["items"] if row["theorem_id"] == THEOREM_ID]
    assert len(authoritative) == 7
    intake = authoritative[0]
    assert intake["id"] == ITEM_ID and intake["phase"] == "intake"
    assert intake["execution_rank"] == RANK and intake["layer"] == 0
    assert intake["state"] == "[ ]" and intake["depends_on"] == []
    assert intake["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert intake["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert intake["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "without_any_formula" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    for key in (
        "module",
        "declaration_or_expression",
        "candidate_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert git("rev-parse", "HEAD:Docs/Stage0_Blueprint.md") == revisions["current_stage0_blueprint_blob"]
    assert (
        git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md')
        == revisions["repository_source_record_blob"]
    )
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert not git("status", "--short", cwd=mathlib), "pinned mathlib worktree is dirty"
    for field, relative in MATHLIB_SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"

    expected_tasks = []
    dependency = ITEM_ID
    for task, authority, suffix in zip(dag["tasks"], authoritative[1:], TASK_SUFFIXES, strict=True):
        task_id = f"S56-M-0051-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        for field in ("id", "phase", "layer", "owned_paths", "deliverable", "completion_gate"):
            assert task[field] == authority[field]
        assert task["id"] == task_id and task["depends_on"] == authority["depends_on"] == [dependency]
        assert task["state"] == "open" and task["evidence_ids"] == []
        assert authority["state"] == "[ ]"
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**格拉斯曼恒等式**") == 1
    assert "- 提出者: Hermann Grassmann" in catalog
    assert "- 时间: 1844" in catalog
    assert "- 陈述: 关于外代数的恒等式" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0051 格拉斯曼恒等式" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    crosswalk = (HERE / "source-statement-crosswalk.md").read_text(encoding="utf-8")
    for needle in (
        "10.1017/CBO9781139237352",
        "no formula",
        "ExteriorAlgebra.ι_sq_zero",
        "Submodule.finrank_sup_add_finrank_inf_eq",
        "cross_cross_eq_smul_sub_smul",
        "only an `H1` lead",
    ):
        assert needle in crosswalk
    scope = (HERE / "scope-map.md").read_text(encoding="utf-8")
    assert "does not choose a particular formula" in scope
    assert "three-dimensional vector" in scope

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = [".stage1-worker-selftest.json"] + [
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in sorted(OWNED_FILES)
    ]
    assert receipt["changed_paths"] == expected_changed
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change" and receipt["content_addressed"] is False
    assert receipt["selftest_result"] == "pass"
    for key in (
        "accepted_receipt_ids",
        "proof_body_locations",
        "canonical_obligation_ids",
        "statement_fingerprints",
        "typed_graph_changes",
        "composition_certificates",
        "content_addressed_recipe_ids",
        "content_addressed_receipt_ids",
    ):
        assert receipt[key] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["source_inputs"] == {
        relative: f"sha256:{sha256(ROOT / relative)}" for relative in SOURCE_HASH_FIELDS.values()
    }
    hashed = receipt["non_self_referential_owned_artifact_sha256"]
    expected_hashed = {
        f"Stage1_Instances/{THEOREM_ID}/{name}"
        for name in OWNED_FILES - {"intake-receipt.json"}
    }
    assert set(hashed) == expected_hashed
    for relative, expected in hashed.items():
        assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"

    probe_output = subprocess.check_output(
        ["lake", "env", "lean", f"../../Stage1_Instances/{THEOREM_ID}/IntakeProbe.lean"],
        cwd=ROOT / "Formalizations/Lean",
        stderr=subprocess.STDOUT,
    )
    assert hashlib.sha256(probe_output).hexdigest() == receipt["worker_input_hashes"]["lean_probe_output_sha256"]
    assert receipt["worker_input_hashes"]["intake_probe_sha256"] == sha256(HERE / "IntakeProbe.lean")
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert receipt["worker_input_hashes"]["lake_symlink_target_string"] == (
        f"sha256:{hashlib.sha256(lake_target).hexdigest()}"
    )
    for recipe in receipt["structured_validation_recipes"]:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert isinstance(recipe["env_allowlist"], dict)
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["exit_code"] == 0
        assert recipe["covered_obligation_ids"] == [ITEM_ID]

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(r"\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b", probe)
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
    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet.resolve(), receipt)

    print("intake invariant check: ok (THM-M-0051 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
