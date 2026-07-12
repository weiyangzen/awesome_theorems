#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-1353."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-1353"
ITEM_ID = "S56-M-1353-INTAKE"
RANK = 963
BASE_REVISION = "122f443c54e4e81d1bf325b07e18ba095823da6d"
BASE_TREE = "2629bb0cacebd896715a9abad7c52ad60e7bccd0"
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
INSTANCE_REQUIRED_KEYS = {
    "schema_version", "normative_profile", "theorem_id", "item_id", "execution_rank",
    "lifecycle_mode", "lifecycle", "intent", "baseline", "rework_required",
    "legacy_artifacts_accepted", "legacy_priority_slot", "name_zh", "name_en",
    "canonical_name", "category", "target_lane", "source_status_untrusted", "intake_score",
    "target_system", "literal_source_claim_zh", "literal_source_claim_en",
    "canonical_claim_status", "canonical_statement", "canonical_claim",
    "candidate_family_not_credited_as_statement", "target_disposition", "statement_blocker",
    "canonical_formal_target", "domain_and_universes", "ordered_binders", "quantifiers",
    "hypotheses", "conclusion", "alternate_encodings", "excluded_degenerate_cases",
    "degenerate_case_status", "candidate_scope_not_credited", "degenerate_cases_to_resolve",
    "excluded_substitutions", "neighbor_target_boundaries", "source_status",
    "source_candidates_not_credited", "formal_candidates_not_credited", "source_revisions",
    "obligation_registry_hash", "discovery_protocol_hash", "root_vector", "audit_complete",
    "theorem_complete", "accepted_proof_state", "accepted_receipt_ids", "foundation_profile",
    "tcb_profile", "computation_profile", "formal_system", "authoritative_blueprint",
    "public_merge_targets", "owners_and_reviewers", "freshness_and_revocation_policy",
    "owned_artifacts", "status_boundary",
}
DAG_REQUIRED_KEYS = {
    "schema_version", "theorem_id", "lifecycle_mode", "lifecycle", "audit_complete",
    "theorem_complete", "accepted_states", "tasks",
}
RECEIPT_REQUIRED_KEYS = {
    "schema_version", "receipt_id", "receipt_class", "content_addressed",
    "content_addressing_boundary", "item_id", "theorem_id", "phase", "intent", "verdict",
    "proposed_state", "accepted", "acceptance_authority", "base_revision", "base_tree",
    "worker_branch_or_worktree", "worktree_state", "preexisting_untracked_paths", "attestor",
    "platform", "source_inputs", "external_source_locators", "source_evidence",
    "worker_input_hashes", "validated_scope", "changed_paths", "diff_summary",
    "exact_statement_change", "source_revision_and_proof_body_summary",
    "ownership_and_change_impact", "owned_artifact_sha256", "structured_validation_recipes",
    "commands_and_results", "root_vector_before", "root_vector_after", "debt_delta_basis",
    "axiom_and_placeholder_result", "actual_source_ownership", "declaration_ownership",
    "readable_ownership", "change_impact_set", "covered_node_ids",
    "canonical_obligation_ids", "statement_fingerprints", "typed_graph_changes",
    "composition_certificates", "proof_body_locations", "accepted_receipt_ids",
    "audit_complete", "theorem_complete", "remaining_root_cut_set", "known_failures", "owner",
    "validation_started_at", "validation_ended_at", "validated_at", "review_due",
    "invalidation_inputs", "support_state", "supersession_state", "incident_path",
    "first_failed_gate", "retry_condition", "status_boundary",
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
MATHLIB_SOURCE_HASH_FIELDS = {
    "mathlib_ode_basic_source_sha256": "Mathlib/Analysis/ODE/Basic.lean",
    "mathlib_matrix_exponential_source_sha256": (
        "Mathlib/Analysis/Normed/Algebra/MatrixExponential.lean"
    ),
    "mathlib_periodic_source_sha256": "Mathlib/Algebra/Ring/Periodic.lean",
    "mathlib_matrix_gl_defs_source_sha256": (
        "Mathlib/LinearAlgebra/Matrix/GeneralLinearGroup/Defs.lean"
    ),
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
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    assert set(instance) == INSTANCE_REQUIRED_KEYS
    assert set(dag) == DAG_REQUIRED_KEYS
    assert set(receipt) == RECEIPT_REQUIRED_KEYS
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"

    targets = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    items = [row for row in execution["items"] if row["id"] == ITEM_ID]
    assert len(targets) == len(items) == 1
    target, item = targets[0], items[0]

    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "Floquet定理"
    assert target["category"] == "微分方程 / 常微分方程"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 108
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
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
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == BASE_REVISION
    assert revisions["repository_base_tree"] == BASE_TREE
    assert git("cat-file", "-t", BASE_REVISION) == "commit"
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
    assert (
        git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md')
        == revisions["repository_source_record_blob"]
    )
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    catalog_excerpt = "\n".join(
        (ROOT / "Docs/researches/math_theorems.md")
        .read_text(encoding="utf-8")
        .splitlines()[9865:9871]
    ) + "\n"
    assert sha256_bytes(catalog_excerpt.encode()) == revisions["repository_record_excerpt_sha256"]
    assert "**Floquet定理**" in catalog_excerpt
    assert "- 提出者: Gaston Floquet" in catalog_excerpt
    assert "- 时间: 1883" in catalog_excerpt
    assert "- 陈述: 周期系统的基本解矩阵" in catalog_excerpt
    stage0_excerpt = "\n".join(
        (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8").splitlines()[36803:36829]
    ) + "\n"
    assert sha256_bytes(stage0_excerpt.encode()) == revisions["stage0_projection_excerpt_sha256"]
    assert "THM-M-1353 Floquet定理" in stage0_excerpt
    assert "- 精确定义与前提条件: 待补充" in stage0_excerpt

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    for field, relative in MATHLIB_SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"

    expected_tasks = []
    dependency = ITEM_ID
    for suffix in TASK_SUFFIXES:
        task_id = f"S56-M-1353-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])
    authoritative_downstream = [
        row for row in execution["items"]
        if row["theorem_id"] == THEOREM_ID and row["id"] != ITEM_ID
    ]
    assert len(authoritative_downstream) == len(dag["tasks"]) == 6
    authoritative_by_id = {row["id"]: row for row in authoritative_downstream}
    for task in dag["tasks"]:
        source = authoritative_by_id[task["id"]]
        for key in (
            "depends_on", "phase", "layer", "owned_paths", "deliverable", "completion_gate"
        ):
            assert task[key] == source[key]
        assert task["evidence_ids"] == []
    neighbor_ids = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert neighbor_ids == {"THM-M-1352", "THM-M-1354", "THM-M-1355"}

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    digests = receipt["owned_artifact_sha256"]
    assert set(digests) == {f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES}
    for relative, expected in digests.items():
        if relative.endswith("/intake-receipt.json"):
            assert expected == "self_referential_excluded_from_provisional_digest"
            continue
        assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"

    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]

    required_recipe_keys = {
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy",
        "expected_exit", "expected_outputs", "covered_ids", "covered_obligation_ids",
        "covered_declarations",
    }
    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    assert all(set(recipe) == required_recipe_keys for recipe in recipes)
    assert all(recipe["network_policy"] == "denied" for recipe in recipes)
    assert all(recipe["expected_exit"] == 0 for recipe in recipes)
    assert all(recipe["covered_ids"] == [ITEM_ID] for recipe in recipes)
    assert all(recipe["covered_obligation_ids"] == [] for recipe in recipes)
    assert recipes[0]["argv"] == ["python3", "-B", str(HERE.relative_to(ROOT) / "check_intake.py")]

    for key in (
        "owner", "validation_started_at", "validation_ended_at", "validated_at", "review_due",
        "support_state", "supersession_state", "incident_path",
    ):
        assert isinstance(receipt[key], str) and receipt[key]
    assert isinstance(receipt["invalidation_inputs"], list) and receipt["invalidation_inputs"]

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    checked_paths = list(HERE.iterdir())
    if args.worker_packet is not None:
        checked_paths.append(args.worker_packet.resolve())
    for path in checked_paths:
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {path.name}"
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"trailing whitespace: {path.name}"
        )

    for name in (
        "README.md", "instance.json", "intake-receipt.json", "scope-map.md",
        "source-statement-crosswalk.md", "task-dag.json", "validation.md",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-1353 planned; H1/M4/R4; six open tasks)")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


if __name__ == "__main__":
    main()
