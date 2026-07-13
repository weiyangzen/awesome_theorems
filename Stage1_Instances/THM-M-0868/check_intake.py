#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0868 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0868"
ITEM_ID = "S56-M-0868-INTAKE"
RANK = 1422
BASE_REVISION = "748243faadc15828fb087059337fd05b7be9fdeb"
BASE_TREE = "e46d642646f80980838b6f016f5d69b817bd464d"
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
    "mathlib_delete_edges_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/"
        "Combinatorics/SimpleGraph/DeleteEdges.lean"
    ),
    "mathlib_subgraph_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/"
        "Combinatorics/SimpleGraph/Subgraph.lean"
    ),
    "mathlib_well_quasi_order_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Order/WellQuasiOrder.lean"
    ),
}
TASK_SUFFIXES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)
RECIPE_FIELDS = {
    "recipe_id",
    "cwd",
    "argv",
    "env_allowlist",
    "timeout_seconds",
    "network_policy",
    "expected_exit",
    "expected_outputs",
    "covered_workflow_item_ids",
    "covered_obligation_ids",
    "covered_declarations",
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


def excerpt_sha256(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1 : end])).hexdigest()


def check_worker_packet(path: Path, receipt: dict, expected_changed: set[str]) -> None:
    packet = load(path)
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
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
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == expected_changed
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

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "图子式定理"
    assert target["category"] == instance["category"] == "组合数学 / 图论"
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
    assert item["state"] == "[ ]" and item["attempts"] == 0 and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert receipt["phase"] == "intake"
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "duplicate_THM_M_0867_ownership_not_frozen" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert receipt["root_vector_before"] == {
        "H": "unclassified",
        "M": "unclassified",
        "R": "unclassified",
    }
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["repository_source_record_blob_at_base"]
    assert (
        git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md')
        == revisions["repository_source_record_blob_at_origin"]
    )
    assert git("rev-parse", "HEAD:Docs/Stage0_Blueprint.md") == revisions["stage0_projection_blob_at_base"]
    assert git("log", "-1", "--format=%H", "--", "Docs/Stage1_Targets_rev-5.6.json") == revisions["target_manifest_origin_commit"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    catalog_path = ROOT / "Docs/researches/math_theorems.md"
    stage0_path = ROOT / "Docs/Stage0_Blueprint.md"
    target_path = ROOT / "Docs/Stage1_Targets_rev-5.6.json"
    assert revisions["repository_record_excerpt_sha256"] == excerpt_sha256(catalog_path, 6362, 6367)
    assert revisions["probable_duplicate_repository_record_excerpt_sha256"] == excerpt_sha256(catalog_path, 6355, 6360)
    assert revisions["stage0_projection_excerpt_sha256"] == excerpt_sha256(stage0_path, 23684, 23709)
    assert revisions["probable_duplicate_stage0_projection_excerpt_sha256"] == excerpt_sha256(stage0_path, 23657, 23682)
    assert revisions["target_manifest_pair_excerpt_sha256"] == excerpt_sha256(target_path, 21325, 21354)

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE

    dependency = ITEM_ID
    expected_tasks = []
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0868-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        for field in ("phase", "layer", "owned_paths", "deliverable", "completion_gate"):
            assert task[field] == authoritative[field]
        assert task["layer"] == layer and task["evidence_ids"] == []
        expected_tasks.append((task_id, [dependency], "open"))
        dependency = task_id
    assert [(row["id"], row["depends_on"], row["state"]) for row in dag["tasks"]] == expected_tasks

    catalog = catalog_path.read_text(encoding="utf-8")
    assert catalog.count("**图子式定理**") == 1
    assert "**Robertson-Seymour图子式定理**" in catalog
    assert "- 陈述:  Wagner猜想的证明" in catalog
    assert "- 陈述: 图子式良拟序定理" in catalog
    stage0 = stage0_path.read_text(encoding="utf-8")
    assert "THM-M-0868 图子式定理" in stage0
    assert "THM-M-0867 Robertson-Seymour图子式定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    neighbors = {row["theorem_id"]: row["name"] for row in instance["neighbor_target_boundaries"]}
    assert neighbors == {
        "THM-M-0867": "Robertson-Seymour图子式定理",
        "THM-M-0866": "Wagner定理",
        "THM-M-0869": "禁用子图问题",
    }
    manifest_neighbors = {
        row["theorem_id"]: row["name"]
        for row in manifest["targets"]
        if row["theorem_id"] in neighbors
    }
    assert manifest_neighbors == neighbors
    source = instance["source_candidates_not_credited"][0]
    assert source["doi"] == "10.1016/j.jctb.2004.08.001"
    assert source["pii"] == "S0095-8956(04)00078-4"

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False and receipt["verdict"] == "no_state_change"
    assert receipt["selftest_result"] == "pass"
    assert receipt["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]
    assert receipt["accepted_receipt_ids"] == receipt["content_addressed_receipt_ids"] == []
    assert receipt["content_addressed_recipe_ids"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["proof_body_locations"] == receipt["typed_graph_changes"] == []
    assert receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [row["id"] for row in dag["tasks"]]
    expected_hashed = OWNED_FILES - {"intake-receipt.json"}
    assert set(receipt["owned_artifact_hashes"]) == expected_hashed
    for name, tagged in receipt["owned_artifact_hashes"].items():
        assert tagged == f"sha256:{sha256(HERE / name)}", f"stale owned hash: {name}"
    assert "intake-receipt.json" in receipt["self_reference_boundary"]
    for relative, tagged in receipt["source_inputs"].items():
        assert tagged == f"sha256:{sha256(ROOT / relative)}", f"stale receipt input: {relative}"
    assert receipt["worker_input_hashes"]["repository_base_revision"] == BASE_REVISION
    assert receipt["worker_input_hashes"]["repository_base_tree"] == BASE_TREE
    assert receipt["worker_input_hashes"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["worker_input_hashes"]["mathlib_tree"] == MATHLIB_TREE
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert receipt["worker_input_hashes"]["lake_symlink_target_string_sha256"] == hashlib.sha256(lake_target).hexdigest()

    recipes = receipt["structured_validation_recipes"]
    assert [row["recipe_id"] for row in recipes] == [
        "S56-M-0868-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0868-INTAKE-RECIPE-LEAN-PROBE",
    ]
    for recipe in recipes:
        assert set(recipe) == RECIPE_FIELDS
        assert recipe["argv"] and recipe["expected_outputs"]
        assert recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
        assert recipe["covered_workflow_item_ids"] == [ITEM_ID]
        assert recipe["covered_obligation_ids"] == []
        assert isinstance(recipe["covered_declarations"], list)
    assert recipes[0]["covered_declarations"] == []
    assert set(recipes[1]["covered_declarations"]) == {
        "SimpleGraph",
        "SimpleGraph.deleteEdges",
        "SimpleGraph.Subgraph.deleteVerts",
        "SimpleGraph.Iso",
        "SimpleGraph.induce",
        "WellQuasiOrdered",
    }

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in (
        "README.md",
        "instance.json",
        "intake-receipt.json",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "task-dag.json",
        "validation.md",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    forbidden = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert not any(token in probe for token in forbidden)

    if args.worker_packet:
        check_worker_packet(args.worker_packet.resolve(), receipt, expected_changed)

    print("THM-M-0868 intake invariant check: ok (planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
