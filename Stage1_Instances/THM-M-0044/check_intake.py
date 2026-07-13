#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0044 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0044"
ITEM_ID = "S56-M-0044-INTAKE"
RANK = 1084
BASE_REVISION = "0ea006c25dcbfe400adbb084c0a3476a9b271741"
BASE_TREE = "ff2e3bde08d7f5d6c83519160a4a6bd2cb7526db"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
ROOT_VECTOR = {"H": "H1", "M": "M3", "R": "R3"}
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
    "statement-validation.md",
    "statement-receipt.json",
    "AnchorAudit.lean",
    "anchor-audit.json",
    "check_anchor_audit.py",
    "anchor-audit-validation.md",
    "anchor-audit-receipt.json",
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
    "singular_values_source_sha256": "Mathlib/Analysis/InnerProductSpace/SingularValues.lean",
    "inner_product_spectrum_source_sha256": "Mathlib/Analysis/InnerProductSpace/Spectrum.lean",
    "matrix_spectrum_source_sha256": "Mathlib/Analysis/Matrix/Spectrum.lean",
    "unitary_group_source_sha256": "Mathlib/LinearAlgebra/UnitaryGroup.lean",
    "mathlib_references_sha256": "docs/references.bib",
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


def canonical_json_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def path_manifest_sha256(paths: list[str]) -> str:
    digest = hashlib.sha256()
    for relative in sorted(paths):
        digest.update(
            relative.encode()
            + b"\0"
            + hashlib.sha256((ROOT / relative).read_bytes()).digest()
        )
    return digest.hexdigest()


def excerpt_sha256(start: int, end: int, relative: str) -> str:
    result = subprocess.run(
        ["sed", "-n", f"{start},{end}p", relative],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    return hashlib.sha256(result).hexdigest()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    assert packet["schema_version"] == "stage1-worker-selftest/1.0"
    assert packet["item_id"] == ITEM_ID and packet["theorem_id"] == THEOREM_ID
    assert packet["intent"] == "intake" and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["receipt_id"] == receipt["receipt_id"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["accepted_receipt_ids"] == []
    assert packet["audit_complete"] is packet["theorem_complete"] is False
    assert packet["owner"] == receipt["owner"] == "Stage1 integration lane"
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
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
    assert target["name"] == instance["name_zh"] == "奇异值分解定理"
    assert target["category"] == instance["category"] == "代数学 / 线性代数"
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
    assert item["state"] in {"[ ]", "[_]"} and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"].startswith("Every finite rectangular")
    assert "A = U * Sigma * V*" in instance["canonical_claim"]
    formal = instance["canonical_formal_target"]
    assert formal["module"] == "Stage1_Instances/THM-M-0044/Statement.lean"
    assert formal["declaration_or_expression"] == \
        "Stage1Instances.THM_M_0044.SingularValueDecompositionTarget"
    assert formal["candidate_expression"] is None
    assert formal["elaborated_expression_hash"] == \
        "f9a0f27af3e6287fc303bfbd9ecf382111bd44ed8d60e27cff6d0acc59b1052b"
    assert isinstance(formal["environment_fingerprint"], str)
    assert "LinearMap.singularValues" in formal["candidate_declarations"]
    assert "Matrix.IsHermitian.spectral_theorem" in formal["candidate_declarations"]
    assert len(instance["alternate_encodings"]) == 2
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == receipt["root_vector_after"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == receipt["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == BASE_REVISION
    assert revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "bcf3f9fa:Docs/researches/math_theorems.md") == revisions["repository_source_record_blob"]
    # These hashes authenticate the historical intake snapshot. Later master
    # checklist projection changes do not invalidate the accepted intake data.
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert len(revisions[field]) == 64 and (ROOT / relative).is_file()
    assert revisions["repository_record_excerpt_sha256"] == excerpt_sha256(335, 340, "Docs/researches/math_theorems.md")
    assert revisions["duplicate_record_excerpt_sha256"] == excerpt_sha256(10581, 10586, "Docs/researches/math_theorems.md")
    assert revisions["stage0_excerpt_sha256"] == excerpt_sha256(1321, 1349, "Docs/Stage0_Blueprint.md")
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    for field, relative in MATHLIB_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"
    assert revisions["inspected_axler_source_sha256"] == instance["source_candidates_not_credited"][0]["observed_source_sha256"]

    expected_tasks = []
    dependency = ITEM_ID
    authoritative_items = {row["id"]: row for row in execution["items"]}
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0044-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        authoritative = authoritative_items[task_id]
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**奇异值分解定理**") == 1
    assert catalog.count("**奇异值分解**") == 1
    assert "- 陈述: 任意矩阵可分解为UΣV*形式" in catalog
    assert "- 陈述: 矩阵的SVD分解" in catalog
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {
        "THM-M-1449",
        "THM-M-0043",
        "THM-M-0046",
    }

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    # The intake receipt remains immutable historical evidence for its original
    # nine-artifact packet; later statement artifacts do not rewrite it.
    intake_files = OWNED_FILES - {
        "Statement.lean", "check_statement.py", "statement.json", "statement-validation.md",
        "statement-receipt.json", "AnchorAudit.lean", "anchor-audit.json",
        "check_anchor_audit.py", "anchor-audit-validation.md", "anchor-audit-receipt.json"
    }
    expected_intake_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in intake_files
    }
    assert set(receipt["changed_paths"]) == expected_intake_changed

    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["content_addressed"] is False
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"
    recipes = {row["recipe_id"]: row for row in receipt["structured_validation_recipes"]}
    actions = {row["recipe_id"]: row for row in receipt["validation_actions"]}
    structure_id = "S56-M-0044-INTAKE-RECIPE-STRUCTURE"
    lean_id = "S56-M-0044-INTAKE-RECIPE-LEAN-PROBE"
    assert set(recipes) == set(actions) == {structure_id, lean_id}
    assert actions[structure_id]["recipe_sha256"] == canonical_json_sha256(recipes[structure_id])
    assert actions[lean_id]["recipe_sha256"] == canonical_json_sha256(recipes[lean_id])
    assert len(actions[structure_id]["input_manifest_sha256"]) == 64
    assert actions[lean_id]["input_manifest_sha256"] == path_manifest_sha256([
        "Formalizations/Lean/lean-toolchain",
        "Formalizations/Lean/lake-manifest.json",
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/SingularValues.lean",
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Spectrum.lean",
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Matrix/Spectrum.lean",
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/LinearAlgebra/UnitaryGroup.lean",
        "Stage1_Instances/THM-M-0044/IntakeProbe.lean",
    ])
    assert all(action["exit_code"] == 0 for action in actions.values())
    assert all(action["covered_obligation_ids"] == [ITEM_ID] for action in actions.values())
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {path.name}"
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), f"trailing whitespace: {path.name}"
    for name in (
        "README.md",
        "instance.json",
        "intake-receipt.json",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "task-dag.json",
        "validation.md",
    ):
        content = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in content and ".cron/" not in content
        assert "theorem_complete=true" not in content
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)

    print("intake invariant check: ok (THM-M-0044 planned; H1/M3/R3; six open tasks)")


if __name__ == "__main__":
    main()
