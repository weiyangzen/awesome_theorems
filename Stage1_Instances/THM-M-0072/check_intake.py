#!/usr/bin/env python3
"""Scoped structural validator for the THM-M-0072 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0072"
ITEM_ID = "S56-M-0072-INTAKE"
RANK = 1102
BASE_REVISION = "b99cf0ffec59c781f8bd25309bdfa53e77372a0a"
BASE_TREE = "e015394246c3919236f2c6ba1a8184c37130f1e4"
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
    "Statement.lean",
    "check_statement.py",
    "statement.json",
    "statement-receipt.json",
    "statement-validation.md",
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
EXPECTED_CHANGED = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0072/README.md",
    "Stage1_Instances/THM-M-0072/Statement.lean",
    "Stage1_Instances/THM-M-0072/check_intake.py",
    "Stage1_Instances/THM-M-0072/check_statement.py",
    "Stage1_Instances/THM-M-0072/instance.json",
    "Stage1_Instances/THM-M-0072/intake-receipt.json",
    "Stage1_Instances/THM-M-0072/scope-map.md",
    "Stage1_Instances/THM-M-0072/source-statement-crosswalk.md",
    "Stage1_Instances/THM-M-0072/statement-receipt.json",
    "Stage1_Instances/THM-M-0072/statement-validation.md",
    "Stage1_Instances/THM-M-0072/statement.json",
    "Stage1_Instances/THM-M-0072/task-dag.json",
    "Stage1_Instances/THM-M-0072/validation.md",
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")
    statement = load(HERE / "statement.json")
    statement_receipt = load(HERE / "statement-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "汤普森转移引理"
    assert target["category"] == instance["category"] == "代数学 / 群论"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is False

    intake_item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert intake_item["theorem_id"] == THEOREM_ID and intake_item["execution_rank"] == RANK
    assert intake_item["phase"] == "intake" and intake_item["layer"] == 0
    assert intake_item["state"] == "[_]" and intake_item["depends_on"] == []
    assert intake_item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert intake_item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] == statement["canonical_statement"]
    assert instance["canonical_claim"] is not None and instance["statement_blocker"] is None
    formal = instance["canonical_formal_target"]
    assert formal["module"] == "Stage1_Instances/THM-M-0072/Statement.lean"
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_0072.ThompsonTransferLemmaTarget"
    assert formal["elaborated_expression_hash"] == "sha256:" + statement["canonical_formal_target"]["elaborated_expression_sha256"]
    assert formal["environment_fingerprint"] is not None
    assert instance["ordered_binders"] and instance["quantifiers"]
    assert instance["hypotheses"] and instance["alternate_encodings"]
    assert instance["excluded_degenerate_cases"]
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert statement["accepted_receipt_ids"] == statement_receipt["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md') == revisions["repository_source_record_blob"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    for field, relative in {
        "transfer_source_sha256": "Mathlib/GroupTheory/Transfer.lean",
        "focal_source_sha256": "Mathlib/GroupTheory/Focal.lean",
        "is_perfect_source_sha256": "Mathlib/GroupTheory/IsPerfect.lean",
    }.items():
        assert revisions[field] == sha256(mathlib / relative)
    assert revisions["thompson_1968_pdf_sha256"] == "93f494417422c31b1bd5a5bd92f3741b7a41bbd8f1581b224d0a5459bc5da83d"
    assert revisions["lynd_arxiv_1303_5996v2_pdf_sha256"] == "eec187eea45d76cc424f43173e057d13398f72276f6253ce3fb491a3e8a6f9c8"

    suffixes = ("STATEMENT", "ANCHOR_AUDIT", "OBLIGATION_TREE", "PROOF", "VALIDATION", "RELEASE")
    dependency = ITEM_ID
    expected_ids = []
    for layer, suffix in enumerate(suffixes, start=1):
        task_id = f"S56-M-0072-{suffix}"
        expected_ids.append(task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        authority = next(row for row in execution["items"] if row["id"] == task_id)
        assert task["phase"] == authority["phase"]
        assert task["layer"] == authority["layer"] == layer
        assert task["depends_on"] == authority["depends_on"] == [dependency]
        assert task["owned_paths"] == authority["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authority["deliverable"]
        assert task["completion_gate"] == authority["completion_gate"]
        assert task["state"] == "open" and task["evidence_ids"] == []
        dependency = task_id
    assert [row["id"] for row in dag["tasks"]] == expected_ids

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**汤普森转移引理**" in catalog
    assert "- 提出者: John Thompson" in catalog
    assert "- 时间: 1964" in catalog
    assert "- 陈述: 关于群局部性质与整体性质的关系" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0072 汤普森转移引理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    crosswalk = (HERE / "source-statement-crosswalk.md").read_text(encoding="utf-8")
    assert "Lemma 5.38(a)(i)" in crosswalk and "printed\npage 411" in crosswalk
    assert "10.1090/S0002-9904-1968-11953-6" in crosswalk
    assert "10.1016/0021-8693(64)90006-7" in crosswalk
    assert "arXiv `1303.5996v2`" in crosswalk

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    assert set(statement_receipt["changed_paths"]) == EXPECTED_CHANGED
    status_paths = {
        line[3:] if line.startswith("?? ") else line[2:].lstrip()
        for line in git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert status_paths == EXPECTED_CHANGED, f"actual changed paths differ: {sorted(status_paths)}"
    assert statement_receipt["proposed_state"] == "[_]" and statement_receipt["accepted"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert statement_receipt["canonical_obligation_ids"] == []
    assert statement_receipt["statement_fingerprints"] == [formal["elaborated_expression_hash"]]
    assert statement_receipt["remaining_root_cut_set"] == expected_ids

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert "def NoIndexTwoSubgroup" in probe
    assert "def ThompsonSourceEnvelope" in probe
    assert "#check MonoidHom.transfer" in probe
    assert "#check Subgroup.commutator_inf_eq_focalSubgroup" in probe
    forbidden = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert not any(token in probe for token in forbidden)

    if args.worker_packet:
        packet = load(args.worker_packet.resolve())
        assert packet["item_id"] == "S56-M-0072-STATEMENT"
        assert packet["theorem_id"] == THEOREM_ID
        assert packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == EXPECTED_CHANGED
        assert packet["known_failures"] == statement_receipt["known_failures"]

    print("THM-M-0072 intake invariant check: ok")


if __name__ == "__main__":
    main()
