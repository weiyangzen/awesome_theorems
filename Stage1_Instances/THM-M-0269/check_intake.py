#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0269 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0269"
ITEM_ID = "S56-M-0269-INTAKE"
RANK = 1276
BASE_REVISION = "c2e294becadae6ce784f27ee69f2e8dbf57e0b30"
BASE_TREE = "3f567e7f76b189432b73444354070c0ff75925b9"
ALLOW_INTEGRATED_HEAD = False
SOURCE_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
SOURCE_EXCERPT_SHA256 = "12407aa63bafb9f7e504e2dc025e21d414d38f3fa1d98fa346fb00290be63de8"
STAGE0_EXCERPT_SHA256 = "e9111868cedab32323fd8a0a7adbaa047473c25800479664b5a3cb07c14196d3"
MANIFEST_ENTRY_SHA256 = "157ed1259a9c86e9ffa6f8147b0b21e67b242c429d16e9e091e65fe055176bf0"
DAG_ENTRY_SHA256 = "0eeaa8cc58a6648c40b864ae81c024d397236ba846eb706a3c1fdd378c4c0944"
PROBE_OUTPUT_SHA256 = "089904c4a149ad5b7ec27898946bd18d5f18b081e781e711e0773a0e7231fb9a"
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
TASK_PHASES = (
    "statement",
    "anchor_audit",
    "obligation_tree",
    "proof",
    "validation",
    "release",
)
TASK_DELIVERABLES = (
    "Elaborate the exact Lean 4 target with the minimal pinned imports.",
    "Audit mathlib and external Lean 4 candidates at immutable revisions.",
    "Freeze the obligation registry and typed proof/provenance/workflow graphs.",
    "Implement or pin/import the required proof bodies without placeholders.",
    "Run hermetic kernel, trust, provenance, and independent validation gates.",
    "Reconcile evidence and decide the exact theorem-completion verdict.",
)
PROBE_DECLARATIONS = (
    "MeasureTheory.lintegral_iSup",
    "MeasureTheory.lintegral_iSup'",
    "MeasureTheory.lintegral_tendsto_of_tendsto_of_monotone",
    "MeasureTheory.lintegral_iSup_ae",
    "MeasureTheory.lintegral_iSup_directed_of_measurable",
    "MeasureTheory.lintegral_iSup_directed",
    "MeasureTheory.integral_tendsto_of_tendsto_of_monotone",
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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    return sha256_bytes("".join(lines[first - 1 : last]).encode("utf-8"))


def canonical_row_sha256(row: dict) -> str:
    data = json.dumps(row, ensure_ascii=False, separators=(",", ":")).encode("utf-8") + b"\n"
    return sha256_bytes(data)


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    required = {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
        "worker_branch_or_worktree",
        "diff_summary",
        "exact_statement_change",
        "source_revision_and_proof_body_summary",
        "commands_and_results",
        "axiom_and_placeholder_result",
        "debt_delta_basis",
        "covered_node_ids",
        "canonical_obligation_ids",
        "statement_fingerprints",
        "typed_graph_changes",
        "composition_certificates",
        "content_addressed_recipe_ids",
        "content_addressed_receipt_ids",
        "proof_body_locations",
        "actual_source_ownership",
        "declaration_ownership",
        "readable_ownership",
        "change_impact_set",
    }
    assert required <= set(packet), "worker packet omits a scheduler-required field"
    assert packet["schema_version"] == "stage1-worker-selftest/1.0"
    assert packet["item_id"] == ITEM_ID and packet["theorem_id"] == THEOREM_ID
    assert packet["intent"] == "intake" and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["receipt_id"] == receipt["receipt_id"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["accepted_receipt_ids"] == []
    assert packet["covered_node_ids"] == [ITEM_ID]
    for field in (
        "canonical_obligation_ids",
        "statement_fingerprints",
        "typed_graph_changes",
        "composition_certificates",
        "content_addressed_recipe_ids",
        "content_addressed_receipt_ids",
        "proof_body_locations",
        "declaration_ownership",
    ):
        assert packet[field] == []
    assert packet["actual_source_ownership"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert packet["change_impact_set"] == [ITEM_ID]
    assert packet["worker_branch_or_worktree"] == receipt["worker_branch_or_worktree"]
    assert packet["diff_summary"] == receipt["diff_summary"]
    assert packet["exact_statement_change"] == receipt["exact_statement_change"]
    assert packet["source_revision_and_proof_body_summary"] == receipt["source_revision_and_proof_body_summary"]
    assert packet["axiom_and_placeholder_result"] == receipt["axiom_and_placeholder_result"]
    assert packet["debt_delta_basis"] == receipt["debt_delta_basis"]
    assert isinstance(packet["commands_and_results"], list) and packet["commands_and_results"]
    assert all(row.get("exit_code") in (0, 1) and row.get("result") for row in packet["commands_and_results"])
    commands = packet["commands"]
    for required_command in (
        "python3 Docs/tools/check_stage1_standard.py",
        "python3 scripts/stage1_target.py check",
        "python3 scripts/stage1_target.py show THM-M-0269",
        "curl -L --fail --silent --show-error https://measure.axler.net/MIRA.pdf -o /tmp/thm-m-0269-mira-final.pdf",
        "curl -L --fail --silent --show-error https://zenodo.org/api/records/2313710/files/article.pdf/content -o /tmp/thm-m-0269-lebesgue-final.pdf",
        "cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0269/IntakeProbe.lean",
    ):
        assert required_command in commands
    assert any(command.startswith("rg -n --glob '*.lean' '^\\s*(sorry|admit|") for command in commands)
    assert packet["audit_complete"] is packet["theorem_complete"] is False
    assert packet["first_failed_gate"] == receipt["first_failed_gate"]
    assert packet["remaining_root_cut_set"] == receipt["remaining_root_cut_set"]
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
    assert target["name"] == instance["name_zh"] == "勒贝格单调收敛定理"
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
    assert canonical_row_sha256(target) == instance["source_revisions"]["manifest_entry_sha256"] == MANIFEST_ENTRY_SHA256

    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] in ("[ ]", "[_]") and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"
    assert canonical_row_sha256(item) == instance["source_revisions"]["execution_dag_intake_entry_sha256"] == DAG_ENTRY_SHA256

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["normative_profile"] == receipt["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"].startswith("Repository catalog wording")
    assert instance["canonical_claim"].startswith("The repository owns the monotone-convergence theorem family")
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["foundation_profile"].startswith("stage1-foundation-profile/1.0-planned:")
    assert instance["tcb_profile"].startswith("stage1-tcb-profile/1.0-planned:")
    assert instance["computation_profile"].startswith("stage1-computation-profile/1.0-planned:")
    assert instance["formal_system"].startswith("lean4-mathlib-adapter/1.0-planned")
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == BASE_REVISION
    assert revisions["repository_base_tree"] == BASE_TREE
    if not ALLOW_INTEGRATED_HEAD:
        assert git("rev-parse", "HEAD") == BASE_REVISION
        assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert git("rev-parse", f"{SOURCE_COMMIT}:Docs/researches/math_theorems.md") == SOURCE_BLOB
    assert revisions["repository_source_record_commit"] == SOURCE_COMMIT
    assert revisions["repository_source_record_blob"] == SOURCE_BLOB
    assert git("hash-object", "Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert git("hash-object", "Docs/Stage0_Blueprint.md") == revisions["current_stage0_blueprint_blob"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 1936, 1941) == SOURCE_EXCERPT_SHA256
    assert revisions["repository_record_excerpt_sha256"] == SOURCE_EXCERPT_SHA256
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 7441, 7466) == STAGE0_EXCERPT_SHA256
    assert revisions["stage0_projection_excerpt_sha256"] == STAGE0_EXCERPT_SHA256

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert revisions["mathlib_lebesgue_add_source_sha256"] == sha256(
        mathlib / "Mathlib/MeasureTheory/Integral/Lebesgue/Add.lean"
    )
    assert revisions["mathlib_bochner_basic_source_sha256"] == sha256(
        mathlib / "Mathlib/MeasureTheory/Integral/Bochner/Basic.lean"
    )
    assert revisions["mathlib_1000_yaml_sha256"] == sha256(mathlib / "docs/1000.yaml")

    intake_task = dag["tasks"][0]
    assert intake_task["id"] == ITEM_ID and intake_task["phase"] == "intake"
    assert intake_task["layer"] == 0 and intake_task["depends_on"] == []
    assert intake_task["state"] == "self_tested_pending_master_acceptance"
    assert intake_task["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert intake_task["deliverable"] == item["deliverable"]
    assert intake_task["completion_gate"] == item["completion_gate"]
    assert intake_task["evidence_ids"] == [receipt["receipt_id"]]
    dependency = ITEM_ID
    expected_tasks = []
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0269-{suffix}"
        expected_tasks.append((task_id, [dependency], layer))
        dependency = task_id
    downstream = dag["tasks"][1:]
    assert [(task["id"], task["depends_on"], task["layer"]) for task in downstream] == expected_tasks
    assert all(task["state"] == "open" and task["evidence_ids"] == [] for task in downstream)
    for task, phase, deliverable in zip(downstream, TASK_PHASES, TASK_DELIVERABLES, strict=True):
        assert task["phase"] == phase
        assert task["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == deliverable
        assert task["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**勒贝格单调收敛定理**" in catalog
    assert "- 提出者: Henri Lebesgue" in catalog
    assert "- 陈述: 单调函数列的积分极限" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0269 勒贝格单调收敛定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert {candidate["declaration"] for candidate in instance["formal_candidates_not_credited"]} == {
        "MeasureTheory.lintegral_iSup",
        "MeasureTheory.lintegral_iSup'",
        "MeasureTheory.lintegral_tendsto_of_tendsto_of_monotone",
        "MeasureTheory.lintegral_iSup_ae",
        "MeasureTheory.lintegral_iSup_directed_of_measurable",
        "MeasureTheory.lintegral_iSup_directed",
        "MeasureTheory.integral_tendsto_of_tendsto_of_monotone",
    }

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    expected_hashed = expected_changed - {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json",
    }
    assert set(receipt["non_self_referential_owned_artifact_sha256"]) == expected_hashed
    for relative, expected in receipt["non_self_referential_owned_artifact_sha256"].items():
        assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"

    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["receipt_id"] == "S56-M-0269-INTAKE-WORKER-20260713"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["verdict"] == "no_state_change"
    started = datetime.fromisoformat(receipt["validation_started_at"])
    ended = datetime.fromisoformat(receipt["validation_ended_at"])
    validated = datetime.fromisoformat(receipt["validated_at"])
    assert started <= ended == validated
    assert receipt["review_due"] and receipt["invalidation_inputs"]
    assert receipt["support_state"] == "provisional_worker_only"
    assert isinstance(receipt["structured_validation_recipes"], list)
    assert {recipe["recipe_id"] for recipe in receipt["structured_validation_recipes"]} == {
        "S56-M-0269-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0269-INTAKE-RECIPE-LEAN-PROBE",
    }
    assert all(recipe["expected_exit"] == 0 for recipe in receipt["structured_validation_recipes"])
    assert isinstance(receipt["commands_and_results"], list) and receipt["commands_and_results"]
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in downstream]
    assert receipt["selftest_result"] == "pass"

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    for declaration in PROBE_DECLARATIONS:
        assert f"#check {declaration}" in probe
    lean_run = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0269/IntakeProbe.lean"],
        cwd=ROOT / "Formalizations/Lean",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=120,
    )
    assert lean_run.returncode == 0, lean_run.stdout.decode("utf-8", errors="replace")
    assert sha256_bytes(lean_run.stdout) == PROBE_OUTPUT_SHA256

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0269 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
