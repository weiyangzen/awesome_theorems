#!/usr/bin/env python3
"""Scoped structural validator for the THM-M-0094 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0094"
ITEM_ID = "S56-M-0094-INTAKE"
RANK = 1111
BASE_REVISION = "d266c6f5ce5732e1fccd687e2f9ce9aa2a0ed1fe"
BASE_TREE = "e77c8d6d5b41cb13d9d8acab2753ac37c4ebd6b4"
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
    "global_sections_source_sha256": "Mathlib/CategoryTheory/Sites/GlobalSections.lean",
    "sheaf_cohomology_source_sha256": "Mathlib/CategoryTheory/Sites/SheafCohomology/Basic.lean",
    "scheme_modules_sheaf_source_sha256": "Mathlib/AlgebraicGeometry/Modules/Sheaf.lean",
    "lie_weights_root_system_source_sha256": "Mathlib/Algebra/Lie/Weights/RootSystem.lean",
    "representation_irreducible_source_sha256": "Mathlib/RepresentationTheory/Irreducible.lean",
    "lie_group_source_sha256": "Mathlib/Geometry/Manifold/Algebra/LieGroup.lean",
}
TASK_SUFFIXES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)


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

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "博雷尔-韦伊-博特定理"
    assert target["category"] == instance["category"] == "代数学 / 表示论"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is False

    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_id"] == "S56-M-0094-INTAKE-WORKER-20260713"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert receipt["phase"] == "intake"
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert formal["declaration_candidates"] == []
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert receipt["root_vector_before"] == {
        "H": "unclassified", "M": "unclassified", "R": "unclassified"
    }
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert git(
        "rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md'
    ) == revisions["repository_source_record_blob"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    for field, relative in MATHLIB_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"

    dependency = ITEM_ID
    expected = []
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0094-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["authoritative_state"] == authoritative["state"] == "[ ]"
        assert task["evidence_ids"] == []
        expected.append((task_id, [dependency], "open"))
        dependency = task_id
    assert [(row["id"], row["depends_on"], row["state"]) for row in dag["tasks"]] == expected

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**博雷尔-韦伊-博特定理**") == 1
    assert "- 提出者: Armand Borel/André Weil/Raoul Bott" in catalog
    assert "- 时间: 1954" in catalog
    assert catalog.count("- 陈述: 紧李群表示的几何实现") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0094 博雷尔-韦伊-博特定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["lifecycle_before"] == "L0 / rework_required"
    assert receipt["lifecycle_after"] == "planned"
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["selftest_result"] == "pass"
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["remaining_root_cut_set"] == [row["id"] for row in dag["tasks"]]
    expected_hashed = OWNED_FILES - {"intake-receipt.json"}
    assert set(receipt["owned_artifact_hashes"]) == expected_hashed
    assert "intake-receipt.json" in receipt["self_reference_boundary"]
    for name, tagged in receipt["owned_artifact_hashes"].items():
        assert tagged == f"sha256:{sha256(HERE / name)}", f"stale owned hash: {name}"
    assert receipt["accepted_receipt_ids"] == receipt["content_addressed_receipt_ids"] == []
    assert receipt["content_addressed_recipe_ids"] == []
    assert receipt["proof_body_locations"] == receipt["typed_graph_changes"] == []
    assert receipt["composition_certificates"] == []
    assert receipt["acceptance_authority"] == "rev-5.6 integration lane"
    assert all(receipt[key] for key in (
        "worker_branch_or_worktree", "diff_summary", "exact_statement_change",
        "source_revision_and_proof_body_summary", "ownership_and_change_impact",
        "output_summary", "owner", "validated_at", "review_due",
        "support_state", "revocation_policy", "incident_path",
    ))
    assert receipt["attestor"] == {
        "kind": "stage1_rev56_worker_selftest",
        "identity": "isolated worker for S56-M-0094-INTAKE",
        "signature": None,
        "signature_status": "unsigned_provisional_worker_evidence",
    }
    assert receipt["invalidation_inputs"]
    for relative, tagged in receipt["source_inputs"].items():
        assert tagged == f"sha256:{sha256(ROOT / relative)}", f"stale receipt input: {relative}"
    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["repository_base_revision"] == BASE_REVISION
    assert worker_inputs["repository_base_tree"] == BASE_TREE
    assert worker_inputs["mathlib_revision"] == MATHLIB_REVISION
    assert worker_inputs["mathlib_tree"] == MATHLIB_TREE
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert worker_inputs["lake_symlink_target_string_sha256"] == hashlib.sha256(lake_target).hexdigest()

    recipes = receipt["structured_validation_recipes"]
    assert [recipe["recipe_id"] for recipe in recipes] == [
        "S56-M-0094-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0094-INTAKE-RECIPE-LEAN-PROBE",
    ]
    required_recipe_keys = {
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit", "expected_outputs",
        "covered_workflow_item_ids", "covered_obligation_ids", "covered_declarations",
    }
    for recipe in recipes:
        assert set(recipe) == required_recipe_keys
        assert recipe["argv"] and recipe["expected_outputs"]
        assert recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        assert recipe["covered_workflow_item_ids"] == [ITEM_ID]
        assert recipe["covered_obligation_ids"] == []
    assert recipes[0]["covered_declarations"] == []
    assert set(recipes[1]["covered_declarations"]) == {
        "CategoryTheory.Sheaf.Γ", "CategoryTheory.Sheaf.H",
        "CategoryTheory.Sheaf.cohomologyFunctor", "AlgebraicGeometry.Scheme.Modules",
        "AlgebraicGeometry.Scheme.Modules.pushforward", "LieModule.Weight",
        "LieAlgebra.IsKilling.rootSystem", "RootPairing", "Representation",
        "Representation.IsIrreducible", "LieGroup",
    }

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    for declaration in (
        "CategoryTheory.Sheaf.H", "AlgebraicGeometry.Scheme.Modules",
        "LieAlgebra.IsKilling.rootSystem", "Representation.IsIrreducible", "LieGroup",
    ):
        assert f"#check {declaration}" in probe
    forbidden = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert not any(token in probe for token in forbidden)

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {path.name}"
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in (
        "README.md", "instance.json", "intake-receipt.json", "scope-map.md",
        "source-statement-crosswalk.md", "task-dag.json", "validation.md",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    if args.worker_packet:
        packet = load(args.worker_packet.resolve())
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == expected_changed
        assert packet["known_failures"] == receipt["known_failures"]
        assert packet["commands"] and packet["output_summary"]

    print("THM-M-0094 intake invariant check: ok (planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
