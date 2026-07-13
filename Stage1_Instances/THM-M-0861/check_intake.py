#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0861 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0861"
ITEM_ID = "S56-M-0861-INTAKE"
RANK = 1415
BASE_REVISION = "464759128569180ab640c412cd80bc5dd2c3b44a"
BASE_TREE = "8da3c9130640d08d4e179450a0418368d0454745"
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
    "graph_basic_source_sha256": "Mathlib/Combinatorics/Graph/Basic.lean",
    "bipartite_source_sha256": "Mathlib/Combinatorics/SimpleGraph/Bipartite.lean",
    "line_graph_source_sha256": "Mathlib/Combinatorics/SimpleGraph/LineGraph.lean",
    "coloring_source_sha256": "Mathlib/Combinatorics/SimpleGraph/Coloring.lean",
    "finite_source_sha256": "Mathlib/Combinatorics/SimpleGraph/Finite.lean",
    "edge_labeling_source_sha256": "Mathlib/Combinatorics/SimpleGraph/EdgeLabeling.lean",
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

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "König边着色定理"
    assert target["category"] == instance["category"] == "组合数学 / 图论"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is False

    authoritative_items = [row for row in execution["items"] if row["theorem_id"] == THEOREM_ID]
    assert len(authoritative_items) == 7
    intake = authoritative_items[0]
    assert intake["id"] == ITEM_ID and intake["phase"] == "intake"
    assert intake["layer"] == 0 and intake["state"] == "[ ]"
    assert intake["depends_on"] == []
    assert intake["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert intake["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert "finite bipartite multigraph" in instance["canonical_statement"]
    assert "edge chromatic number" in instance["canonical_statement"]
    assert "Source-backed mathematical family only" in instance["canonical_claim"]
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
    for suffix in TASK_SUFFIXES:
        task_id = f"S56-M-0861-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" and task["evidence_ids"] == [] for task in dag["tasks"])
    for task, authority in zip(dag["tasks"], authoritative_items[1:], strict=True):
        for field in ("id", "phase", "layer", "owned_paths", "deliverable", "completion_gate"):
            assert task[field] == authority[field]
        assert task["depends_on"] == authority["depends_on"]
        assert authority["state"] == "[ ]"

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**König边着色定理**" in catalog
    assert "- 提出者: Dénes Kőnig" in catalog
    assert "- 时间: 1916" in catalog
    assert "- 陈述: 二部图的边色数等于最大度" in catalog
    crosswalk = (HERE / "source-statement-crosswalk.md").read_text(encoding="utf-8")
    for needle in (
        "10.1007/BF01456961",
        "Satz C",
        "Printed page 455",
        revisions["inspected_konig_pdf_sha256"],
        "parallel edges",
        "not yet `H0`",
    ):
        assert needle in crosswalk
    scope = (HERE / "scope-map.md").read_text(encoding="utf-8")
    assert "finite bipartite multigraph" in scope
    assert "strict specialization" in scope

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert set(receipt["owned_artifact_sha256"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    for relative, expected in receipt["owned_artifact_sha256"].items():
        if relative.endswith("/intake-receipt.json"):
            assert expected == "self_referential_excluded_from_provisional_digest"
        else:
            assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"

    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change" and receipt["content_addressed"] is False
    assert receipt["selftest_result"] == "pass"
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["content_addressed_recipe_ids"] == receipt["content_addressed_receipt_ids"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    required_recipe_keys = {
        "recipe_id",
        "cwd",
        "argv",
        "env_allowlist",
        "timeout_seconds",
        "network_policy",
        "expected_exit",
        "expected_outputs",
        "covered_obligation_ids",
        "covered_declarations",
        "exit_code",
    }
    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    assert all(set(recipe) == required_recipe_keys for recipe in recipes)
    assert all(recipe["network_policy"] == "denied" for recipe in recipes)
    assert all(recipe["expected_exit"] == recipe["exit_code"] == 0 for recipe in recipes)
    assert all(recipe["covered_obligation_ids"] == [] for recipe in recipes)
    assert all(len(recipe["expected_outputs"]) == 1 for recipe in recipes)
    provisional_hashes = receipt["provisional_recipe_sha256"]
    for recipe in recipes:
        canonical = json.dumps(recipe, sort_keys=True, separators=(",", ":")).encode() + b"\n"
        assert provisional_hashes[recipe["recipe_id"]] == f"sha256:{hashlib.sha256(canonical).hexdigest()}"

    lean_output = subprocess.check_output(
        ["lake", "env", "lean", f"../../Stage1_Instances/{THEOREM_ID}/IntakeProbe.lean"],
        cwd=ROOT / "Formalizations/Lean",
        stderr=subprocess.STDOUT,
    )
    lean_hash = hashlib.sha256(lean_output).hexdigest()
    assert lean_hash == receipt["lean_probe_stdout_sha256"]
    recipe_by_id = {recipe["recipe_id"]: recipe for recipe in recipes}
    assert recipe_by_id["S56-M-0861-INTAKE-RECIPE-STRUCTURE"]["covered_declarations"] == []
    assert set(recipe_by_id["S56-M-0861-INTAKE-RECIPE-LEAN-PROBE"]["covered_declarations"]) == {
        "Graph",
        "Graph.IsLink",
        "Graph.Inc",
        "Graph.incidenceSet",
        "SimpleGraph.IsBipartite",
        "SimpleGraph.IsBipartiteWith",
        "SimpleGraph.lineGraph",
        "SimpleGraph.lineGraph_adj_iff_exists",
        "SimpleGraph.Coloring",
        "SimpleGraph.Colorable",
        "SimpleGraph.chromaticNumber",
        "SimpleGraph.maxDegree",
        "SimpleGraph.degree_le_maxDegree",
        "SimpleGraph.EdgeLabeling",
    }
    assert recipe_by_id["S56-M-0861-INTAKE-RECIPE-LEAN-PROBE"]["expected_outputs"][0]["sha256"] == lean_hash
    expected_structure_output = b"intake invariant check: ok (THM-M-0861 planned; H1/M4/R4; six open tasks)\n"
    assert recipe_by_id["S56-M-0861-INTAKE-RECIPE-STRUCTURE"]["expected_outputs"][0]["sha256"] == hashlib.sha256(expected_structure_output).hexdigest()
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    code_lines = "\n".join(line for line in probe.splitlines() if not line.lstrip().startswith(("/", "*", "#")))
    assert not re.search(r"\b(sorry|admit|axiom|constant|opaque|unsafe)\b", code_lines)

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()
    checked_paths = list(HERE.iterdir())
    if args.worker_packet is not None:
        packet = load(args.worker_packet.resolve())
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
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == receipt["changed_paths"]
        assert packet["known_failures"] == receipt["known_failures"]
        assert packet["output_summary"] == receipt["output_summary"]
        assert packet["commands"]
        checked_paths.append(args.worker_packet.resolve())
    for path in checked_paths:
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path}"
        assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {path}"

    print("intake invariant check: ok (THM-M-0861 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
