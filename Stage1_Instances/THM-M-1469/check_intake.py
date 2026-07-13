#!/usr/bin/env python3
"""Validate the fail-closed THM-M-1469 planned intake."""

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
THEOREM_ID = "THM-M-1469"
ITEM_ID = "S56-M-1469-INTAKE"
RANK = 1146
BASE_REVISION = "521bd42e5ab5e30513a3c2b7377ea4a1516c0d16"
BASE_TREE = "6f3d9fcf297fe5251a1dc839c1e67930001a86fc"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
OWNED_FILES = {
    "README.md",
    "instance.json",
    "scope-map.md",
    "source-statement-crosswalk.md",
    "statement-blocker.md",
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


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first - 1:last])).hexdigest()


def canonical_json_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def path_manifest_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        digest.update(relative.encode() + b"\0" + hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def run_recorded_recipe(recipe: dict) -> bytes:
    expected_env = recipe["env_allowlist"]
    assert set(expected_env) == {"HOME", "LANG", "LC_ALL", "PATH"}
    assert expected_env["HOME"] == str(Path.home())
    assert expected_env["LANG"] == expected_env["LC_ALL"] == "C.UTF-8"
    assert expected_env["PATH"] == os.environ["PATH"]
    assert recipe["network_policy"] == "denied"
    result = subprocess.run(
        recipe["argv"],
        cwd=ROOT / recipe["cwd"],
        env=expected_env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=recipe["timeout_seconds"],
        check=False,
    )
    assert result.returncode == recipe["expected_exit"]
    return result.stdout


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state"
    }
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

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "自适应有限元"
    assert target["category"] == instance["category"] == "其他重要领域 / 数值分析"
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
    assert set(instance) == {
        "schema_version", "normative_profile", "theorem_id", "item_id",
        "lifecycle_mode", "lifecycle", "intent", "baseline", "rework_required",
        "execution_rank", "legacy_priority_slot", "legacy_artifacts_accepted",
        "intake_score", "name_zh", "name_en", "canonical_name", "category",
        "target_lane", "target_system", "literal_source_claim_zh",
        "literal_source_claim_en", "source_attribution", "source_status_untrusted",
        "canonical_statement", "canonical_claim_status", "canonical_claim",
        "statement_blocker", "target_decision", "canonical_formal_target",
        "domain_and_universes", "quantifiers", "ordered_binders", "hypotheses",
        "conclusion", "alternate_encodings", "excluded_degenerate_cases",
        "degenerate_case_status", "candidate_scope_not_credited",
        "excluded_substitutions", "neighbor_target_boundaries", "source_status",
        "source_candidates_not_credited", "formal_candidates_not_credited",
        "bounded_search_result", "source_revisions", "obligation_registry_hash",
        "discovery_protocol_hash", "root_vector", "audit_complete",
        "theorem_complete", "accepted_proof_state", "accepted_receipt_ids",
        "foundation_profile", "tcb_profile", "computation_profile", "formal_system",
        "authoritative_blueprint", "open_task_dag", "public_merge_targets",
        "owners_and_reviewers", "review_due", "revocation_and_incident_procedure",
        "archive_and_recovery_boundary", "freshness_and_revocation_policy",
        "owned_artifacts", "status_boundary"
    }
    assert set(dag) == {
        "schema_version", "normative_profile", "theorem_id", "lifecycle_mode",
        "lifecycle", "audit_complete", "theorem_complete", "accepted_states", "tasks"
    }
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["normative_profile"] == "machine-theorem-assurance/1.0"
    assert set(receipt) == {
        "schema_version", "normative_profile", "receipt_id", "receipt_class",
        "content_addressed", "content_addressing_boundary", "attestor", "item_id",
        "theorem_id", "covered_node_ids", "phase", "intent", "verdict",
        "proposed_state", "accepted", "acceptance_status", "acceptance_authority",
        "base_revision", "base_tree", "worker_branch_or_worktree", "worktree_state",
        "platform", "validated_scope", "source_inputs", "source_evidence",
        "worker_input_hashes", "structure_input_paths", "structure_self_input_boundary",
        "structure_nonfile_inputs", "lean_input_paths", "changed_paths",
        "owned_artifact_sha256", "diff_summary",
        "exact_statement_change", "ownership_and_change_impact",
        "structured_validation_recipes", "validation_actions", "commands_and_results",
        "root_vector_before", "root_vector_after", "debt_delta_basis",
        "lifecycle_before", "lifecycle_after", "audit_complete", "theorem_complete",
        "accepted_receipt_ids", "proof_body_locations", "canonical_obligation_ids",
        "statement_fingerprints", "typed_graph_changes", "composition_certificates",
        "first_failed_gate", "retry_condition", "remaining_root_cut_set",
        "known_failures", "owner", "validated_at", "review_due", "support_state",
        "supersession_state", "revocation_state", "invalidation_inputs",
        "incident_path", "dirty_input_evidence", "selftest_result",
        "placeholder_and_trust_result", "output_summary", "status_boundary"
    }
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "does_not_select_a_stable_truth_valued_proposition" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    for key in (
        "module", "declaration_or_expression", "candidate_expression",
        "elaborated_expression_hash", "environment_fingerprint"
    ):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md') == revisions["repository_source_record_blob"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    assert revisions["repository_record_excerpt_sha256"] == excerpt_sha256(
        ROOT / "Docs/researches/math_theorems.md", 10721, 10726
    )
    assert revisions["stage0_projection_excerpt_sha256"] == excerpt_sha256(
        ROOT / "Docs/Stage0_Blueprint.md", 39946, 39971
    )
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    mathlib_hashes = {
        "mathlib_lax_milgram_source_sha256": "Mathlib/Analysis/InnerProductSpace/LaxMilgram.lean",
        "mathlib_projection_basic_source_sha256": "Mathlib/Analysis/InnerProductSpace/Projection/Basic.lean",
        "mathlib_projection_finite_dimensional_source_sha256": "Mathlib/Analysis/InnerProductSpace/Projection/FiniteDimensional.lean",
        "mathlib_projection_submodule_source_sha256": "Mathlib/Analysis/InnerProductSpace/Projection/Submodule.lean",
    }
    for field, relative in mathlib_hashes.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib source: {field}"

    expected_tasks = []
    dependency = ITEM_ID
    for suffix in TASK_SUFFIXES:
        task_id = f"S56-M-1469-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" and task["evidence_ids"] == [] for task in dag["tasks"])
    authoritative_tasks = {
        row["id"]: row for row in execution["items"]
        if row["theorem_id"] == THEOREM_ID and row["phase"] != "intake"
    }
    for task in dag["tasks"]:
        expected_task_keys = {
            "id", "phase", "layer", "depends_on", "state", "owned_paths",
            "deliverable", "completion_gate", "evidence_ids"
        }
        if task["phase"] == "statement":
            expected_task_keys.add("first_blocker")
        assert set(task) == expected_task_keys
        authority = authoritative_tasks[task["id"]]
        for key in (
            "phase", "layer", "depends_on", "owned_paths", "deliverable", "completion_gate"
        ):
            assert task[key] == authority[key]

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    for literal in (
        "**自适应有限元**",
        "- 提出者: Ivo Babuška/Werner Rheinboldt",
        "- 时间: 1978",
        "- 陈述: 基于后验误差估计的自适应",
    ):
        assert literal in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-1469 自适应有限元" in stage0
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {
        "THM-M-1461", "THM-M-1468", "THM-M-1470", "THM-M-1471"
    }

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
        else:
            assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"

    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change" and receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["dirty_input_evidence"]["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]

    for relative, tagged_digest in receipt["source_inputs"].items():
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}", f"stale receipt input: {relative}"

    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    recipes_by_id = {recipe["recipe_id"]: recipe for recipe in recipes}
    actions = receipt["validation_actions"]
    assert len(actions) == 2
    for action in actions:
        recipe = recipes_by_id[action["recipe_id"]]
        assert set(recipe) == {
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit",
            "expected_outputs", "covered_obligation_ids", "covered_declarations"
        }
        assert all(set(output) == {"path_or_stream", "semantic_hash_policy"}
                   for output in recipe["expected_outputs"])
        assert set(action) == {
            "action_id", "recipe_id", "recipe_sha256", "input_manifest_sha256",
            "stdout_sha256", "started_at", "ended_at", "exit_code",
            "covered_obligation_ids", "covered_declarations"
        }
        identity = {key: recipe[key] for key in (
            "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy", "expected_exit"
        )}
        assert action["recipe_sha256"] == canonical_json_sha256(identity)
        assert action["exit_code"] == 0
        assert action["covered_obligation_ids"] == [ITEM_ID]
        for field in ("recipe_sha256", "input_manifest_sha256", "stdout_sha256"):
            assert re.fullmatch(r"[0-9a-f]{64}", action[field])
    lean_recipe = recipes_by_id["S56-M-1469-INTAKE-RECIPE-LEAN-PROBE"]
    lean_stdout = run_recorded_recipe(lean_recipe)
    lean_action = next(action for action in actions if action["recipe_id"] == lean_recipe["recipe_id"])
    assert lean_action["stdout_sha256"] == hashlib.sha256(lean_stdout).hexdigest()

    structure_inputs = []
    for relative in receipt["structure_input_paths"]:
        path = ROOT / relative
        if relative.endswith("/intake-receipt.json"):
            assert receipt["structure_self_input_boundary"] == (
                "self_referential_receipt_excluded_from_action_input_digest"
            )
            continue
        structure_inputs.append(path)
    structure_action = next(action for action in actions if action["recipe_id"].endswith("STRUCTURE"))
    assert structure_action["input_manifest_sha256"] == path_manifest_hash(structure_inputs)
    assert structure_action["stdout_sha256"] == hashlib.sha256(
        b"intake invariant check: ok (THM-M-1469 planned; H5/M4/R4; six open tasks)\n"
    ).hexdigest()
    lean_inputs = [ROOT / relative for relative in receipt["lean_input_paths"]]
    assert lean_action["input_manifest_sha256"] == path_manifest_hash(lean_inputs)
    assert receipt["worker_input_hashes"]["lake_symlink_target_sha256"] == hashlib.sha256(
        (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    ).hexdigest()
    nonfiles = receipt["structure_nonfile_inputs"]
    assert nonfiles["repository_base_revision"] == git("rev-parse", "HEAD")
    assert nonfiles["repository_base_tree"] == git("rev-parse", "HEAD^{tree}")
    assert nonfiles["mathlib_revision"] == git("rev-parse", "HEAD", cwd=mathlib)
    assert nonfiles["mathlib_tree"] == git("rev-parse", "HEAD^{tree}", cwd=mathlib)
    assert nonfiles["lake_symlink_target_sha256"] == receipt["worker_input_hashes"][
        "lake_symlink_target_sha256"
    ]

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in OWNED_FILES - {"IntakeProbe.lean", "check_intake.py", "intake-receipt.json"}:
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-1469 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
