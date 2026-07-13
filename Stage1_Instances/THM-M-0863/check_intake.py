#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0863."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0863"
ITEM_ID = "S56-M-0863-INTAKE"
RANK = 1417
BASE_REVISION = "3ef3a6bf4f2f9b86930beb27693f7429fea3e63a"
BASE_TREE = "c9eba4c65f6e228f9cefc8bdf62136b7fb69426a"
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
TASK_SUFFIXES = [
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
]
SOURCE_HASHES = {
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
MATHLIB_SOURCE_HASHES = {
    "mathlib_connected_source_sha256":
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph/Connectivity/Connected.lean",
    "mathlib_connectivity_subgraph_source_sha256":
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph/Connectivity/Subgraph.lean",
    "mathlib_paths_source_sha256":
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph/Paths.lean",
    "mathlib_subgraph_source_sha256":
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph/Subgraph.lean",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dirty_manifest_sha256(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.as_posix()):
        data = path.read_bytes()
        relative = path.relative_to(ROOT).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(len(data)).encode("ascii"))
        digest.update(b"\0")
        digest.update(data)
    return digest.hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def check_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"{path} is missing a final newline"
    assert b"\r" not in data and b"\x00" not in data, f"invalid bytes in {path}"
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), \
        f"trailing whitespace in {path}"


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    check_text_hygiene(path.resolve())
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
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
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
    assert target["name"] == instance["name_zh"] == "Whitney定理"
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
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "recognizable_whitney_ear_theorem_family" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "intake"
    assert receipt["lifecycle_before"] == "no_rev56_instance_at_uniform_L0_baseline"
    assert receipt["lifecycle_after"] == "planned"
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["debt_vector_change_proposed"] is True
    assert "grants no accepted proof state" in receipt["debt_vector_change_boundary"]

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert git(
        "rev-parse",
        f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md',
    ) == revisions["repository_source_record_blob"]
    for field, relative in SOURCE_HASHES.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
        assert receipt["source_inputs"][relative] == f"sha256:{revisions[field]}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    for field, relative in MATHLIB_SOURCE_HASHES.items():
        assert receipt["worker_input_hashes"][field] == sha256(ROOT / relative)

    expected_tasks = []
    dependency = ITEM_ID
    authoritative_tasks = {
        row["id"]: row for row in execution["items"] if row["theorem_id"] == THEOREM_ID
    }
    assert len(authoritative_tasks) == len(TASK_SUFFIXES) + 1
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0863-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        source = authoritative_tasks[task_id]
        for field in ("phase", "layer", "owned_paths", "deliverable", "completion_gate"):
            assert task[field] == source[field]
        assert task["layer"] == layer and task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**Whitney定理**") == 1
    assert "- 提出者: Hassler Whitney" in catalog
    assert "- 时间: 1932" in catalog
    assert catalog.count("- 陈述: 2-连通图的耳分解") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0863 Whitney定理" in stage0
    assert "定理内容: 2-连通图的耳分解" in stage0
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {
        "THM-M-0862", "THM-M-0864"
    }
    source = instance["source_candidates_not_credited"][0]
    assert source["doi"] == "10.1090/S0002-9947-1932-1501641-2"
    assert source["observed_pdf_sha256"] == \
        "dc5b3da59a06b4b6f21bd424add1d28576b059143a470f2593257a0073d14fa5"

    assert {path.name for path in HERE.iterdir() if path.is_file()} == OWNED_FILES
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    assert set(receipt["changed_paths"]) == {
        ".stage1-worker-selftest.json",
        *(f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES),
    }
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["content_addressed"] is receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change" and receipt["proposed_state"] == "[_]"
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["selftest_result"] == "pass"
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["known_failures"]
    assert receipt["covered_node_ids"] == [ITEM_ID]
    assert receipt["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]
    assert receipt["worker_input_hashes"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["worker_input_hashes"]["mathlib_tree"] == MATHLIB_TREE
    required_packet_fields = (
        "owner", "validated_at", "validation_started_at", "validation_finished_at",
        "review_due", "support_state", "supersession_state", "revocation_state",
        "incident_path", "invalidation_inputs",
    )
    assert all(receipt[field] for field in required_packet_fields)

    artifact_hashes = receipt["owned_artifact_sha256"]
    assert set(artifact_hashes) == OWNED_FILES
    assert artifact_hashes["intake-receipt.json"] == "self-reference-excluded"
    for name in OWNED_FILES - {"intake-receipt.json"}:
        assert artifact_hashes[name] == f"sha256:{sha256(HERE / name)}"
    dirty = receipt["dirty_input_evidence"]
    expected_dirty_paths = [
        ROOT / ".stage1-worker-selftest.json",
        *(HERE / name for name in sorted(OWNED_FILES - {"intake-receipt.json"})),
    ]
    expected_dirty_names = {
        path.relative_to(ROOT).as_posix() for path in expected_dirty_paths
    } | {f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json"}
    assert set(dirty["owned_untracked_paths"]) == expected_dirty_names
    assert set(dirty["hash_manifest"]) == expected_dirty_names
    assert dirty["hash_manifest"][f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json"] == \
        "self-reference-excluded"
    for path in expected_dirty_paths:
        relative = path.relative_to(ROOT).as_posix()
        assert dirty["hash_manifest"][relative] == f"sha256:{sha256(path)}"
    assert dirty["deterministic_manifest_sha256"] == dirty_manifest_sha256(expected_dirty_paths)

    expected_declarations = [
        "SimpleGraph.Preconnected",
        "SimpleGraph.Connected",
        "SimpleGraph.Preconnected.exists_isPath",
        "SimpleGraph.Walk.IsPath",
        "SimpleGraph.Walk.IsCycle",
        "SimpleGraph.Walk.toSubgraph",
        "SimpleGraph.Walk.connected_induce_support",
        "SimpleGraph.Subgraph.induce",
        "SimpleGraph.Subgraph.deleteVerts",
    ]
    required_recipe_keys = {
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy",
        "expected_exit", "expected_outputs", "covered_obligation_ids", "covered_declarations",
        "covered_ids", "covered_task_ids",
    }
    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2 and all(set(recipe) == required_recipe_keys for recipe in recipes)
    assert all(recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0 for recipe in recipes)
    assert all(recipe["covered_ids"] == recipe["covered_task_ids"] == [ITEM_ID] for recipe in recipes)
    structure = next(recipe for recipe in recipes if recipe["recipe_id"].endswith("STRUCTURE"))
    assert structure["cwd"] == "." and structure["covered_obligation_ids"] == []
    assert structure["covered_declarations"] == []
    assert structure["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM_ID}/check_intake.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    lean_recipe = next(recipe for recipe in recipes if recipe["recipe_id"].endswith("LEAN-PROBE"))
    assert lean_recipe["cwd"] == "Formalizations/Lean"
    assert lean_recipe["argv"] == [
        "lake", "env", "lean", f"../../Stage1_Instances/{THEOREM_ID}/IntakeProbe.lean"
    ]
    assert lean_recipe["covered_obligation_ids"] == []
    assert lean_recipe["covered_declarations"] == expected_declarations

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()

    for name in OWNED_FILES:
        check_text_hygiene(HERE / name)
    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)
    if args.worker_packet:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0863 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
