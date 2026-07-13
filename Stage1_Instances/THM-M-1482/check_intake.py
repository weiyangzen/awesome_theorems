#!/usr/bin/env python3
"""Fail-closed scoped validator for the THM-M-1482 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-1482"
ITEM_ID = "S56-M-1482-INTAKE"
RANK = 1159
BASE_REVISION = "8a6dba9921138a63027dc802b77a4cc3a01f3f60"
BASE_TREE = "1afb3440a5a33640728678de56e261f9470af1d1"
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
TASK_SUFFIXES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)
SOURCE_HASHES = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "83871cc366fceca7bae1ca9d7eb9e61c51f282b91012ee8cfee983d256a190ff",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "3ff8beaa6f32c0e296c6250ec271d4ec77ef4f152a5b250d6aa7f3a2b067877d",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/researches/physics_theorems.md": "6abf9da63cf075b0c6a05f3a245838ec0d7848fe873c43f529a7e0ee72cf94fa",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_HASHES = {
    "Mathlib/Data/Multiset/Bind.lean": "5109591298080c721ebd6e0bf8901752b8c5fb231aa284971c1e3e35f66056fb",
    "Mathlib/Probability/ProbabilityMassFunction/Constructions.lean": "2044d12cd63eae39de73e656f731fae0ca890b4708ce99077310f12fea47e7a0",
    "Mathlib/Probability/ProbabilityMassFunction/Monad.lean": "221973d0038d1763577f19f6ca110273c2ed245aa0a894ae85c9121e887d3f18",
}
EXCERPT_HASHES = {
    "catalog": "a6ddd5faec8cb339a2b5f88c6a3eafdb3fee8d53d53ef6ba8dea81f7c6c8b8ef",
    "stage0": "c0bc03841936886ff89705e1fc0d5c29502f910cba98fe6131ee581d60685307",
}


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_sha256(path: Path, first_line: int, last_line: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first_line - 1 : last_line])).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def check_authorities(instance: dict) -> list[dict]:
    manifest = load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    assert manifest["schema_version"] == "stage1-target-set/5.6.2"
    matches = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    assert matches == [
        {
            "execution_rank": RANK,
            "legacy_priority_slot": None,
            "theorem_id": THEOREM_ID,
            "name": "遗传算法",
            "category": "其他重要领域 / 数值分析",
            "source_status_untrusted": "已验证",
            "baseline": "L0",
            "rework_required": True,
            "legacy_artifacts_accepted": False,
            "target_lane": "hard_statement_first_partial_verification",
            "intake_score": 86,
            "lifecycle_mode": "planned",
            "theorem_complete": False,
        }
    ]
    target = matches[0]
    for field in (
        "execution_rank",
        "legacy_priority_slot",
        "baseline",
        "rework_required",
        "legacy_artifacts_accepted",
        "target_lane",
        "intake_score",
        "source_status_untrusted",
        "lifecycle_mode",
        "theorem_complete",
    ):
        assert instance[field] == target[field]
    assert instance["name_zh"] == target["name"]
    assert instance["category"] == target["category"]

    items = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]
    intake = next(row for row in items if row["id"] == ITEM_ID)
    assert intake == {
        "id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "execution_rank": RANK,
        "phase": "intake",
        "layer": 0,
        "state": "[ ]",
        "depends_on": [],
        "owned_paths": [f"Stage1_Instances/{THEOREM_ID}"],
        "deliverable": "Create the theorem dossier, scope map, and source-statement crosswalk.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    return items


def check_instance(instance: dict) -> None:
    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == THEOREM_ID and instance["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert instance["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "no_stable_truth_valued" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    for field in (
        "module",
        "declaration_or_expression",
        "candidate_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[field] is None
    assert "not_a_stable_proposition" in formal["gate_state"]
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert "does not refute properly stated genetic-algorithm results" in instance["status_boundary"]
    assert "No canonical mathematical or Lean statement" in instance["status_boundary"]
    assert instance["status_boundary"].endswith("master acceptance is claimed.")

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert (
        git("rev-parse", "HEAD:Docs/researches/math_theorems.md")
        == revisions["current_repository_math_source_blob"]
    )
    assert (
        git(
            "rev-parse",
            f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md',
        )
        == revisions["repository_source_record_blob"]
    )
    revision_fields = {
        "target_manifest_sha256": "Docs/Stage1_Targets_rev-5.6.json",
        "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
        "execution_dag_sha256": "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
        "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
        "repository_math_source_sha256": "Docs/researches/math_theorems.md",
        "repository_physics_source_sha256": "Docs/researches/physics_theorems.md",
        "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
        "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
        "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
    }
    for field, path in revision_fields.items():
        assert revisions[field] == SOURCE_HASHES[path] == sha256(ROOT / path)
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 10833, 10838) == EXCERPT_HASHES["catalog"]
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 40297, 40322) == EXCERPT_HASHES["stage0"]
    assert revisions["repository_record_excerpt_sha256"] == EXCERPT_HASHES["catalog"]
    assert revisions["stage0_projection_excerpt_sha256"] == EXCERPT_HASHES["stage0"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    mathlib_fields = {
        "mathlib_multiset_bind_source_sha256": "Mathlib/Data/Multiset/Bind.lean",
        "mathlib_pmf_constructions_source_sha256": "Mathlib/Probability/ProbabilityMassFunction/Constructions.lean",
        "mathlib_pmf_monad_source_sha256": "Mathlib/Probability/ProbabilityMassFunction/Monad.lean",
    }
    for field, path in mathlib_fields.items():
        assert revisions[field] == MATHLIB_HASHES[path] == sha256(mathlib / path)


def check_catalog_and_boundaries(instance: dict) -> None:
    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**遗传算法**") == 1
    assert catalog.count("- 提出者: John Holland") == 1
    assert catalog.count("- 陈述: 基于进化的优化算法") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-1482 遗传算法" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    boundaries = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert boundaries == {"THM-M-1481", "THM-M-1483", "THM-M-1484", "THM-M-1485"}


def check_task_dag(dag: dict, authoritative: list[dict]) -> None:
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["theorem_id"] == THEOREM_ID
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert dag["accepted_states"] == []
    assert dag["audit_complete"] is False and dag["theorem_complete"] is False
    assert len(dag["tasks"]) == 6
    dependency = ITEM_ID
    for layer, (task, suffix) in enumerate(zip(dag["tasks"], TASK_SUFFIXES), start=1):
        task_id = f"S56-M-1482-{suffix}"
        source = next(row for row in authoritative if row["id"] == task_id)
        assert task["id"] == task_id and task["depends_on"] == [dependency]
        assert task["state"] == "open" and task["layer"] == source["layer"] == layer
        assert task["phase"] == source["phase"]
        assert task["owned_paths"] == source["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == source["deliverable"]
        assert task["completion_gate"] == source["completion_gate"]
        assert task["evidence_ids"] == []
        dependency = task_id


def check_receipt(receipt: dict, dag: dict) -> None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["content_addressed"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["root_vector_after"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    empty_fields = (
        "accepted_receipt_ids",
        "proof_body_locations",
        "canonical_obligation_ids",
        "statement_fingerprints",
        "typed_graph_changes",
        "composition_certificates",
        "content_addressed_recipe_ids",
        "content_addressed_receipt_ids",
        "declaration_ownership",
    )
    for field in empty_fields:
        assert receipt[field] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["change_impact_set"] == receipt["covered_node_ids"] == [ITEM_ID]
    assert receipt["selftest_result"] == "pass"
    assert receipt["known_failures"]
    assert "master acceptance remains pending" in receipt["status_boundary"]
    assert "no exact-statement" in receipt["status_boundary"]
    assert "no_state_change" in receipt["verdict"]
    assert receipt["validated_at"] == receipt["validation_ended_at"]
    assert receipt["validation_started_at"] < receipt["validation_ended_at"]
    assert receipt["review_due"]
    assert receipt["support_state"].startswith("provisional intake only")
    assert receipt["supersession_state"] == "current_unsuperseded_worker_report"
    assert receipt["revocation_state"] == "not_revoked"
    assert receipt["incident_path"]

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
        "covered_ids",
        "exit_code",
    }
    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    assert all(set(recipe) == required_recipe_keys for recipe in recipes)
    assert all(isinstance(recipe["argv"], list) and recipe["argv"] for recipe in recipes)
    assert all(all(isinstance(arg, str) for arg in recipe["argv"]) for recipe in recipes)
    assert all(recipe["network_policy"] == "denied" for recipe in recipes)
    assert all(recipe["expected_exit"] == recipe["exit_code"] == 0 for recipe in recipes)
    assert all(isinstance(recipe["timeout_seconds"], int) and recipe["timeout_seconds"] > 0 for recipe in recipes)
    assert all(recipe["covered_obligation_ids"] == [] for recipe in recipes)
    assert all(recipe["covered_declarations"] == [] for recipe in recipes)
    assert all(recipe["covered_ids"] == [ITEM_ID] for recipe in recipes)
    assert all(recipe["expected_outputs"] for recipe in recipes)
    assert all(
        set(output) == {"path_or_stream", "semantic_hash_policy", "sha256"}
        for recipe in recipes
        for output in recipe["expected_outputs"]
    )
    assert all(
        output["semantic_hash_policy"] == "exact_bytes_sha256"
        and re.fullmatch(r"[0-9a-f]{64}", output["sha256"])
        for recipe in recipes
        for output in recipe["expected_outputs"]
    )

    changed = receipt["changed_paths"]
    assert changed[0] == ".stage1-worker-selftest.json"
    assert set(changed[1:]) == {f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES}
    hashes = receipt["non_self_referential_owned_artifact_sha256"]
    expected_hashed = OWNED_FILES - {"intake-receipt.json"}
    assert set(hashes) == {f"Stage1_Instances/{THEOREM_ID}/{name}" for name in expected_hashed}
    for path, digest in hashes.items():
        assert digest == sha256(ROOT / path)


def check_public_surfaces(instance: dict) -> None:
    assert {path.name for path in HERE.iterdir() if path.is_file()} == OWNED_FILES
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    text = "\n".join(
        (HERE / name).read_text(encoding="utf-8")
        for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md")
    )
    for term in (
        "H5",
        "M4",
        "R4",
        "schema theorem",
        "crossover",
        "mutation",
        "master acceptance",
        "theorem completion",
    ):
        assert term in text
    assert "theorem_complete=false" in text


def check_probe() -> None:
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert "import Mathlib.Data.Multiset.Bind" in probe
    assert "import Mathlib.Probability.ProbabilityMassFunction.Constructions" in probe
    for name in (
        "Multiset.map",
        "Multiset.bind",
        "Multiset.card_bind",
        "PMF.map",
        "PMF.bind",
        "PMF.support_map",
        "PMF.bind_bind",
    ):
        assert f"#check {name}" in probe or f"#print axioms {name}" in probe
    forbidden = re.compile(r"(?m)^\s*(sorry|admit|axiom|constant|opaque|unsafe\b)|sorryAx")
    assert forbidden.search(probe) is None
    assert re.search(r"(?m)^\s*(theorem|lemma|example)\b", probe) is None


def check_worker_packet(receipt: dict, packet_path: Path) -> None:
    packet = load_json(packet_path)
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
    assert packet["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    instance = load_json(HERE / "instance.json")
    dag = load_json(HERE / "task-dag.json")
    receipt = load_json(HERE / "intake-receipt.json")
    authoritative = check_authorities(instance)
    check_instance(instance)
    check_catalog_and_boundaries(instance)
    check_task_dag(dag, authoritative)
    check_receipt(receipt, dag)
    check_public_surfaces(instance)
    check_probe()
    if args.worker_packet is not None:
        packet_path = args.worker_packet
        if not packet_path.is_absolute():
            packet_path = ROOT / packet_path
        check_worker_packet(receipt, packet_path)
    print("intake invariant check: ok (THM-M-1482 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
