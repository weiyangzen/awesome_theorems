#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0815."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0815"
ITEM_ID = "S56-M-0815-INTAKE"
RANK = 1374
BASE_REVISION = "adc87f8ea24dcc7c5e2668c0a5ede0ca5c5f0f55"
BASE_TREE = "3c83596059f716cde0d50a5f6b390ada6ca7c8e1"
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
    "mathlib_hall_finite_source_sha256": "Mathlib/Combinatorics/Hall/Finite.lean",
    "mathlib_hall_basic_source_sha256": "Mathlib/Combinatorics/Hall/Basic.lean",
    "mathlib_simple_graph_hall_source_sha256": "Mathlib/Combinatorics/SimpleGraph/Hall.lean",
    "mathlib_simple_graph_matching_source_sha256": "Mathlib/Combinatorics/SimpleGraph/Matching.lean",
    "mathlib_references_bib_sha256": "docs/references.bib",
}
SOURCE_INPUT_PATHS = {
    "Docs/Stage1_Targets_rev-5.6.json",
    "Docs/Stage1_Blueprint_rev-5.6.md",
    "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "skills/execute-stage1-rev56/SKILL.md",
    "Docs/Blueprint_Guidelines.md",
    "Docs/researches/math_theorems.md",
    "Docs/Stage0_Blueprint.md",
    "Formalizations/Lean/lean-toolchain",
    "Formalizations/Lean/lake-manifest.json",
}
PROBE_DECLARATIONS = [
    "Finset.all_card_le_biUnion_card_iff_existsInjective'",
    "Finset.all_card_le_biUnion_card_iff_exists_injective",
    "Fintype.all_card_le_rel_image_card_iff_exists_injective",
    "Fintype.all_card_le_filter_rel_iff_exists_injective",
    "SimpleGraph.exists_isMatching_of_forall_ncard_le",
    "SimpleGraph.exists_isPerfectMatching_of_forall_ncard_le",
    "SimpleGraph.IsBipartiteWith",
    "SimpleGraph.Subgraph.isPerfectMatching_iff",
    "Set.Infinite.ncard",
]
EXPECTED_STRUCTURE_STDOUT_SHA256 = (
    "6298d60c4549b7645e837d16cf4abcc7b8768ca97d1c06957ba9c869332a4508"
)
PROHIBITED = re.compile(
    r"\b(sorry|admit|sorryAx)\b|^\s*(axiom|opaque|constant|unsafe)\s+",
    re.MULTILINE,
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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_sha256(value: object) -> str:
    data = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return sha256_bytes(data)


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet_path = path.resolve()
    packet = load(packet_path)
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
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["commands"] == receipt["commands_and_results"]
    assert receipt["worker_packet_sha256"] == sha256(packet_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    targets = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    authoritative = [
        row for row in execution["items"] if row["theorem_id"] == THEOREM_ID
    ]
    assert len(targets) == 1 and len(authoritative) == 7
    target = targets[0]
    intake_item = authoritative[0]

    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "霍尔婚配定理",
        "category": "组合数学 / 图论",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 86,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    assert intake_item["id"] == ITEM_ID and intake_item["phase"] == "intake"
    assert intake_item["layer"] == 0 and intake_item["state"] == "[ ]"
    assert intake_item["depends_on"] == []
    assert intake_item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert intake_item["deliverable"] == (
        "Create the theorem dossier, scope map, and source-statement crosswalk."
    )
    assert intake_item["completion_gate"] == (
        "rev-5.6 node-specific receipt and master acceptance"
    )

    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"]
    assert target["category"] == instance["category"]
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is False

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"]
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert dag["lifecycle_mode"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["literal_source_claim_zh"] == "二部图完美匹配存在的条件"
    assert instance["canonical_statement"] is None
    assert instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[key] is None
    assert instance["ordered_binders"] == instance["quantifiers"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False
    assert receipt["accepted"] is False and receipt["proposed_state"] == "[_]"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["content_addressed"] is False
    assert receipt["phase"] == "intake"
    assert receipt["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["acceptance_authority"] == "integration lane"
    assert receipt["support_state"] == "provisional_unaccepted"
    assert receipt["lifecycle_before"] == "no_instance_at_L0_baseline"
    assert receipt["lifecycle_after"] == "planned"
    assert receipt["content_addressed_recipe_ids"] == []
    assert receipt["content_addressed_receipt_ids"] == []
    assert receipt["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]
    assert receipt["dirty_input_evidence"]["preflight_status"] == [
        "?? Formalizations/Lean/.lake"
    ]
    assert receipt["dirty_input_evidence"]["preflight_status_sha256"] == sha256_bytes(
        b"?? Formalizations/Lean/.lake\n"
    )

    assert set(instance["owned_artifacts"]) == OWNED_FILES
    assert {path.name for path in HERE.iterdir() if path.is_file()} == OWNED_FILES
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == (
        revisions["repository_math_source_current_blob"]
    )
    assert git(
        "rev-parse",
        f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md',
    ) == revisions["repository_source_record_blob"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    assert set(receipt["source_inputs"]) == SOURCE_INPUT_PATHS
    for relative, digest in receipt["source_inputs"].items():
        assert digest == f"sha256:{sha256(ROOT / relative)}"

    assert revisions["manifest_entry_canonical_sha256"] == canonical_sha256(target)
    assert revisions["target_dag_rows_canonical_sha256"] == canonical_sha256(
        authoritative
    )
    source_lines = (ROOT / "Docs/researches/math_theorems.md").read_text(
        encoding="utf-8"
    ).splitlines(True)
    source_excerpt = "".join(source_lines[5990:5996])
    assert sha256_bytes(source_excerpt.encode()) == revisions[
        "repository_record_excerpt_sha256"
    ]
    assert "**霍尔婚配定理**" in source_excerpt
    assert "- 提出者: Philip Hall" in source_excerpt
    assert "- 时间: 1935" in source_excerpt
    assert "- 陈述: 二部图完美匹配存在的条件" in source_excerpt
    stage0_lines = (ROOT / "Docs/Stage0_Blueprint.md").read_text(
        encoding="utf-8"
    ).splitlines(True)
    stage0_excerpt = "".join(stage0_lines[22252:22278])
    assert sha256_bytes(stage0_excerpt.encode()) == revisions[
        "stage0_projection_excerpt_sha256"
    ]
    assert "THM-M-0815 霍尔婚配定理" in stage0_excerpt
    assert "- 精确定义与前提条件: 待补充" in stage0_excerpt

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert not git("status", "--short", cwd=mathlib)
    for field, relative in MATHLIB_SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"
    assert sha256_bytes(os.readlink(ROOT / "Formalizations/Lean/.lake").encode()) == (
        revisions["lake_symlink_target_sha256"]
    )

    expected_ids = [row["id"] for row in authoritative[1:]]
    assert [task["id"] for task in dag["tasks"]] == expected_ids
    for task, source in zip(dag["tasks"], authoritative[1:]):
        for key in (
            "id",
            "theorem_id",
            "execution_rank",
            "phase",
            "layer",
            "depends_on",
            "owned_paths",
            "deliverable",
            "completion_gate",
        ):
            assert task[key] == source[key], f"DAG mismatch for {task['id']} {key}"
        assert task["state"] == "open" and task["evidence_ids"] == []

    expected_changed = {
        ".stage1-worker-selftest.json",
        *(f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES),
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["root_vector_after"] == {
        "H": "H1",
        "M": "M3",
        "R": "R4",
        "boundary": "provisional planned intake projection only; master acceptance pending",
    }
    for key in (
        "accepted_receipt_ids",
        "canonical_obligation_ids",
        "statement_fingerprints",
        "typed_graph_changes",
        "composition_certificates",
        "proof_body_locations",
    ):
        assert receipt[key] == []
    assert receipt["remaining_root_cut_set"] == [
        f"S56-M-0815-{suffix}" for suffix in TASK_SUFFIXES
    ]
    assert receipt["covered_declaration_ids"] == PROBE_DECLARATIONS
    assert receipt["selftest_result"] == "pass"
    assert receipt["validated_at"] is not None
    assert receipt["worker_input_hashes"]["intake_probe_source_sha256"] == sha256(
        HERE / "IntakeProbe.lean"
    )
    assert receipt["worker_input_hashes"]["intake_probe_output_sha256"]
    assert receipt["worker_input_hashes"]["lean_toolchain"] == (
        f'sha256:{sha256(ROOT / "Formalizations/Lean/lean-toolchain")}'
    )
    assert receipt["worker_input_hashes"]["lake_manifest"] == (
        f'sha256:{sha256(ROOT / "Formalizations/Lean/lake-manifest.json")}'
    )
    assert receipt["worker_input_hashes"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["worker_input_hashes"]["mathlib_tree"] == MATHLIB_TREE

    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
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
    }
    for recipe in recipes:
        assert set(recipe) == required_recipe_keys
        assert recipe["env_allowlist"] == {}
        assert isinstance(recipe["timeout_seconds"], int) and recipe["timeout_seconds"] > 0
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == 0
        assert recipe["covered_obligation_ids"] == [ITEM_ID]
        assert recipe["expected_outputs"]
    by_recipe = {recipe["recipe_id"]: recipe for recipe in recipes}
    structure_recipe = by_recipe[f"{ITEM_ID}-RECIPE-STRUCTURE"]
    lean_recipe = by_recipe[f"{ITEM_ID}-RECIPE-LEAN-PROBE"]
    assert structure_recipe["argv"] == [
        "python3",
        "-B",
        f"Stage1_Instances/{THEOREM_ID}/check_intake.py",
        "--worker-packet",
        ".stage1-worker-selftest.json",
    ]
    assert structure_recipe["covered_declarations"] == []
    assert EXPECTED_STRUCTURE_STDOUT_SHA256 in structure_recipe["expected_outputs"][0][
        "semantic_hash_policy"
    ]
    assert lean_recipe["cwd"] == "Formalizations/Lean"
    assert lean_recipe["argv"] == [
        "lake",
        "env",
        "lean",
        f"../../Stage1_Instances/{THEOREM_ID}/IntakeProbe.lean",
    ]
    assert lean_recipe["covered_declarations"] == PROBE_DECLARATIONS
    assert receipt["worker_input_hashes"]["intake_probe_output_sha256"] in (
        lean_recipe["expected_outputs"][0]["semantic_hash_policy"]
    )

    actions = receipt["validation_actions"]
    assert len(actions) == 2
    actions_by_recipe = {action["recipe_id"]: action for action in actions}
    assert set(actions_by_recipe) == set(by_recipe)
    for recipe_id, action in actions_by_recipe.items():
        recipe = by_recipe[recipe_id]
        assert action["started_at"] <= action["ended_at"] <= receipt["validated_at"]
        assert action["exit_code"] == recipe["expected_exit"] == 0
        assert action["covered_obligation_ids"] == recipe["covered_obligation_ids"]
        assert action["covered_declarations"] == recipe["covered_declarations"]
    assert actions_by_recipe[structure_recipe["recipe_id"]]["stdout_sha256"] == (
        EXPECTED_STRUCTURE_STDOUT_SHA256
    )
    assert actions_by_recipe[lean_recipe["recipe_id"]]["stdout_sha256"] == receipt[
        "worker_input_hashes"
    ]["intake_probe_output_sha256"]
    assert receipt["validation_started_at"] == min(
        action["started_at"] for action in actions
    )
    assert receipt["validation_ended_at"] == max(action["ended_at"] for action in actions)
    assert receipt["validation_ended_at"] == receipt["validated_at"]

    expected_hashed_files = OWNED_FILES - {"intake-receipt.json"}
    assert set(receipt["untracked_owned_artifact_sha256"]) == expected_hashed_files
    for name, digest in receipt["untracked_owned_artifact_sha256"].items():
        assert digest == sha256(HERE / name), f"owned artifact hash mismatch: {name}"

    allowed_dirty = {
        "Formalizations/Lean/.lake",
        ".stage1-worker-selftest.json",
        *(f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES),
    }
    status_lines = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=ROOT,
        text=True,
    ).splitlines()
    actual_dirty = {line[3:] for line in status_lines}
    assert actual_dirty == allowed_dirty, (
        f"unexpected or missing dirty paths: {sorted(actual_dirty ^ allowed_dirty)}"
    )
    status_bytes = "".join(f"{line}\n" for line in status_lines).encode()
    assert receipt["dirty_input_evidence"]["final_status_sha256"] == sha256_bytes(
        status_bytes
    )

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not PROHIBITED.search(probe)
    assert "theorem " not in probe and "lemma " not in probe
    assert "does not select a canonical proposition or prove a new target" in probe
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print(
        "THM-M-0815 intake check: PASS "
        "(planned H1/M3/R4; exact statement and all downstream gates open)"
    )


if __name__ == "__main__":
    main()
