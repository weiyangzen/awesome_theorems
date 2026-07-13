#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0278 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0278"
ITEM_ID = "S56-M-0278-INTAKE"
RANK = 1284
BASE_REVISION = "bd81d4853a030765585ef6fed4310484ceb1e458"
BASE_TREE = "fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
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
TASKS = (
    ("STATEMENT", "statement", 1),
    ("ANCHOR_AUDIT", "anchor_audit", 2),
    ("OBLIGATION_TREE", "obligation_tree", 3),
    ("PROOF", "proof", 4),
    ("VALIDATION", "validation", 5),
    ("RELEASE", "release", 6),
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def path_manifest_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        digest.update(relative.encode() + b"\0" + hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def check_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    assert packet["schema_version"] == "stage1-worker-selftest/1.0"
    assert packet["item_id"] == ITEM_ID and packet["theorem_id"] == THEOREM_ID
    assert packet["intent"] == "intake" and packet["state"] == "[_]"
    assert packet["verdict"] == "no_state_change"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert packet["receipt_id"] == receipt["receipt_id"]
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["commands"] == receipt["commands"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["accepted_receipt_ids"] == []
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
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "里斯表示定理"
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
    assert instance["intent"] == receipt["intent"] == receipt["phase"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == instance["hypotheses"] == []
    assert instance["alternate_encodings"] == instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []

    dependency = ITEM_ID
    expected_tasks = []
    for suffix, phase, layer in TASKS:
        task_id = f"S56-M-0278-{suffix}"
        expected_tasks.append((task_id, phase, layer, [dependency]))
        dependency = task_id
    assert [
        (task["id"], task["phase"], task["layer"], task["depends_on"])
        for task in dag["tasks"]
    ] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])
    assert all(task["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"] for task in dag["tasks"])
    assert all(task["evidence_ids"] == [] and task["deliverable"] for task in dag["tasks"])

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert (
        git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md')
        == revisions["repository_source_record_blob"]
    )
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert revisions["inner_product_dual_source_sha256"] == sha256(
        mathlib / "Mathlib/Analysis/InnerProductSpace/Dual.lean"
    )
    assert revisions["mathlib_references_sha256"] == sha256(mathlib / "docs/references.bib")

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**里斯表示定理**") == 2
    assert catalog.count("- 提出者: Frigyes Riesz") >= 4
    assert catalog.count("- 陈述: Hilbert空间上线性泛函的表示") == 2
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0278 里斯表示定理" in stage0
    assert "- 定理内容: Hilbert空间上线性泛函的表示" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {
        "THM-M-0279",
        "THM-M-0329",
        "THM-M-1288",
    }

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual_files == set(instance["owned_artifacts"]) == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    hashed = OWNED_FILES - {"intake-receipt.json"}
    assert set(receipt["untracked_owned_artifact_sha256"]) == hashed
    for name in hashed:
        assert receipt["untracked_owned_artifact_sha256"][name] == sha256(HERE / name)
    assert receipt["owned_input_manifest_sha256"] == path_manifest_hash(
        [HERE / name for name in hashed]
    )
    for path in HERE.iterdir():
        if path.is_file():
            data = path.read_bytes()
            assert data.endswith(b"\n") and b"\r" not in data
            assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_id"] == f"{ITEM_ID}-worker-selftest"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["selftest_result"] == "pass"
    assert receipt["owner"] == "Stage1 integration lane"
    for field in ("validation_started_at", "validation_ended_at", "validated_at"):
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}", receipt[field])
    for field in (
        "review_due",
        "support_state",
        "supersession_state",
        "revocation_state",
        "incident_path",
    ):
        assert isinstance(receipt[field], str) and receipt[field]
    assert receipt["known_failures"] and receipt["invalidation_inputs"]
    assert receipt["dirty_input_evidence"]["preflight_untracked_paths"] == ["Formalizations/Lean/.lake"]

    if args.worker_packet:
        check_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0278 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
