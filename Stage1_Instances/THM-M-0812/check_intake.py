#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0812."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0812"
ITEM_ID = "S56-M-0812-INTAKE"
RANK = 1371
BASE_REVISION = "997541734bb32f987fb15f163335a82512992120"
BASE_TREE = "2c866b9d840d48c48ac839740c62d3b9440be0e5"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LAKE_SYMLINK_TARGET_SHA256 = (
    "e8714e9ebb75a5da1eeb16fdb6f50831a6cab29f115df43fa8e7535b38f59826"
)
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
    "mathlib_bipartite_source_sha256": "Mathlib/Combinatorics/SimpleGraph/Bipartite.lean",
    "mathlib_matching_source_sha256": "Mathlib/Combinatorics/SimpleGraph/Matching.lean",
    "mathlib_vertex_cover_source_sha256": "Mathlib/Combinatorics/SimpleGraph/VertexCover.lean",
    "mathlib_hall_source_sha256": "Mathlib/Combinatorics/SimpleGraph/Hall.lean",
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
    }
    assert set(packet) == required
    data = path.resolve().read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert packet["commands"] == receipt["worker_packet_commands"]
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

    targets = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    items = [row for row in execution["items"] if row["id"] == ITEM_ID]
    assert len(targets) == len(items) == 1
    target, item = targets[0], items[0]

    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "柯尼希定理"
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

    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["normative_profile"] == receipt["normative_profile"] == instance["normative_profile"]
    required_instance_keys = {
        "schema_version", "normative_profile", "theorem_id", "item_id", "lifecycle_mode",
        "lifecycle", "intent", "baseline", "rework_required", "execution_rank",
        "legacy_priority_slot", "legacy_artifacts_accepted", "intake_score", "name_zh",
        "name_en", "canonical_name", "category", "category_en", "target_lane", "target_system",
        "literal_source_claim_zh", "literal_source_claim_en", "source_attribution",
        "source_status_untrusted", "canonical_statement", "canonical_claim_status",
        "canonical_claim", "statement_blocker", "canonical_formal_target", "domain_and_universes",
        "quantifiers", "ordered_binders", "hypotheses", "conclusion", "alternate_encodings",
        "excluded_degenerate_cases", "degenerate_case_status", "candidate_scope_not_credited",
        "excluded_substitutions", "formal_candidates_not_credited", "bounded_formal_search",
        "source_status", "source_candidates_not_credited", "source_revisions",
        "obligation_registry_hash", "discovery_protocol_hash", "root_vector", "audit_complete",
        "theorem_complete", "accepted_proof_state", "accepted_receipt_ids", "foundation_profile",
        "tcb_profile", "computation_profile", "formal_system", "authoritative_blueprint",
        "public_merge_targets", "owners_and_reviewers", "support_window", "review_due",
        "revocation_and_incident_procedure", "archive_and_recovery_boundary",
        "freshness_and_revocation_policy", "owned_artifacts", "status_boundary",
    }
    assert set(instance) == required_instance_keys
    assert set(dag) == {
        "schema_version", "normative_profile", "theorem_id", "lifecycle_mode", "lifecycle",
        "audit_complete", "theorem_complete", "accepted_states", "tasks",
    }
    required_receipt_keys = {
        "schema_version", "normative_profile", "receipt_id", "receipt_class",
        "content_addressed", "content_addressing_boundary", "item_id", "theorem_id", "phase",
        "intent", "verdict", "proposed_state", "accepted", "acceptance_authority",
        "base_revision", "base_tree", "worker_branch_or_worktree", "worktree_state",
        "preexisting_untracked_paths", "attestor", "platform", "source_inputs", "source_evidence",
        "worker_input_hashes", "dirty_input_evidence", "non_self_referential_owned_artifact_sha256",
        "validated_scope", "changed_paths", "diff_summary", "output_summary",
        "exact_statement_change", "source_revision_and_proof_body_summary",
        "ownership_and_change_impact", "structured_validation_recipes", "commands_and_results",
        "worker_packet_commands", "root_vector_before", "root_vector_after", "debt_delta_basis",
        "axiom_and_placeholder_result", "actual_source_ownership", "declaration_ownership",
        "readable_ownership", "change_impact_set", "covered_node_ids", "covered_declaration_ids",
        "accepted_receipt_ids", "proof_body_locations", "canonical_obligation_ids",
        "statement_fingerprints", "typed_graph_changes", "composition_certificates",
        "audit_complete", "theorem_complete", "first_failed_gate", "first_failed_downstream_gate",
        "first_failed_theorem_gate", "retry_condition", "remaining_root_cut_set", "known_failures",
        "owner", "reviewer_policy", "validation_started_at", "validation_ended_at", "validated_at",
        "review_due", "support_state", "supersession_state", "invalidation_inputs", "incident_path",
        "selftest_result", "status_boundary",
    }
    assert set(receipt) == required_receipt_keys
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"].startswith("For every finite bipartite graph")
    assert instance["canonical_claim"] is not None
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["alternate_encodings"] == instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R2"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["repository_math_source_current_blob"]
    assert git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md') == revisions["repository_source_record_blob"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    catalog_lines = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8").splitlines(True)
    catalog_excerpt = "".join(catalog_lines[5969:5975])
    assert sha256_bytes(catalog_excerpt.encode()) == revisions["repository_record_excerpt_sha256"]
    assert "**柯尼希定理**" in catalog_excerpt
    assert "- 提出者: Dénes Kőnig" in catalog_excerpt
    assert "- 时间: 1931" in catalog_excerpt
    assert "- 陈述: 二部图中最大匹配等于最小顶点覆盖" in catalog_excerpt

    stage0_lines = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8").splitlines(True)
    stage0_excerpt = "".join(stage0_lines[22171:22197])
    assert sha256_bytes(stage0_excerpt.encode()) == revisions["stage0_projection_excerpt_sha256"]
    assert "THM-M-0812 柯尼希定理" in stage0_excerpt
    assert "- 精确定义与前提条件: 待补充" in stage0_excerpt

    source = instance["source_candidates_not_credited"][0]
    assert source["observed_translation_pdf_bytes"] == 94803
    assert source["observed_translation_pdf_sha256"] == "cecbda9a56b360c5f588c2db30d58d22f1cf0af3333ab009521a4c4ac8ff671a"
    assert source["observed_translation_tex_bytes"] == 9171
    assert source["observed_translation_tex_sha256"] == "c64b81e2a348aea280f96a7dd32a09b5a0bd6283f314821733d95a76a9f453d4"
    assert "not H0" in source["status"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert not git("status", "--short", cwd=mathlib)
    for field, relative in MATHLIB_SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"
    lake = ROOT / "Formalizations/Lean/.lake"
    assert lake.is_symlink()
    assert sha256_bytes(str(lake.readlink()).encode()) == LAKE_SYMLINK_TARGET_SHA256

    expected_tasks = []
    dependency = ITEM_ID
    authoritative_by_id = {
        row["id"]: row
        for row in execution["items"]
        if row["theorem_id"] == THEOREM_ID and row["id"] != ITEM_ID
    }
    for suffix in TASK_SUFFIXES:
        task_id = f"S56-M-0812-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        authoritative = authoritative_by_id[task_id]
        for key in ("depends_on", "phase", "layer", "owned_paths", "deliverable", "completion_gate"):
            assert task[key] == authoritative[key]
        assert task["evidence_ids"] == [] and task["state"] == "open"
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert len(authoritative_by_id) == len(dag["tasks"]) == 6

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {path.name}"
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), f"trailing whitespace: {path.name}"

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["phase"] == "intake" and receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["acceptance_authority"] == "integration lane"
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["root_vector_after"] == {"H": "H1", "M": "M3", "R": "R2"}
    assert receipt["selftest_result"] == "pass"
    assert receipt["platform"]["operating_system"] == platform.system()
    assert receipt["platform"]["architecture"] == platform.machine()
    assert receipt["owner"] == "Stage1 integration lane"
    for field in ("validated_at", "review_due", "support_state", "supersession_state", "invalidation_inputs", "incident_path"):
        assert receipt[field]
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["dirty_input_evidence"]["patch_hash"] is None
    assert set(receipt["dirty_input_evidence"]["owned_untracked_paths"]) == expected_changed
    assert receipt["worker_input_hashes"]["lake_symlink_target_string"] == (
        f"sha256:{LAKE_SYMLINK_TARGET_SHA256}"
    )
    for field, relative in MATHLIB_SOURCE_HASH_FIELDS.items():
        assert receipt["worker_input_hashes"][field] == sha256(mathlib / relative)

    expected_hashed = {
        f"Stage1_Instances/{THEOREM_ID}/{name}"
        for name in OWNED_FILES
        if name != "intake-receipt.json"
    }
    hashes = receipt["non_self_referential_owned_artifact_sha256"]
    assert set(hashes) == expected_hashed
    for relative, expected in hashes.items():
        assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"

    recipes = receipt["structured_validation_recipes"]
    assert [recipe["recipe_id"] for recipe in recipes] == [
        "S56-M-0812-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0812-INTAKE-RECIPE-LEAN-PROBE",
    ]
    for recipe in recipes:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["timeout_seconds"] > 0
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == 0
        assert recipe["expected_outputs"]
        assert recipe["covered_ids"] == [ITEM_ID]

    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(r"\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b", probe)

    if args.worker_packet:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0812 planned; H1/M3/R2; six open tasks)")


if __name__ == "__main__":
    main()
