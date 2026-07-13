#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0819."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0819"
ITEM_ID = "S56-M-0819-INTAKE"
RANK = 1377
BASE_REVISION = "902d9ce008e88a35a2307c85355560a230cc33c2"
BASE_TREE = "dfc20d8141f18f6b09a03e818acfff408e836714"
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
PROBE_DECLARATIONS = [
    "IsChain",
    "IsAntichain",
    "subsingleton_of_isChain_of_isAntichain",
    "inter_subsingleton_of_isChain_of_isAntichain",
    "Set.chainHeight",
    "Set.exists_eq_chainHeight_of_finite",
    "Set.encard",
    "ENat.card",
]
RECIPE_KEYS = {
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
PACKET_KEYS = {
    "schema_version",
    "theorem_id",
    "item_id",
    "phase",
    "intent",
    "verdict",
    "changed_paths",
    "commands",
    "command_results",
    "output_summary",
    "base_revision",
    "base_tree",
    "worker_reference",
    "diff_summary",
    "exact_statement_changes",
    "source_revisions",
    "proof_body_locations",
    "axiom_and_placeholder_result",
    "root_vector_before",
    "root_vector_after",
    "debt_delta_basis",
    "task_ids",
    "canonical_obligation_ids",
    "statement_fingerprints",
    "typed_graph_changes",
    "composition_certificates",
    "accepted_receipt_ids",
    "provisional_receipt_ids",
    "evidence_record",
    "first_failed_gate",
    "blocked_gates",
    "remaining_root_cut_set",
    "actual_source_ownership",
    "declaration_ownership",
    "readable_ownership",
    "change_impact_set",
    "owner",
    "validated_at",
    "review_due",
    "invalidation_inputs",
    "support_state",
    "supersession_state",
    "revocation_state",
    "incident_path",
    "known_failures",
    "state",
}
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
    "mathlib_order_chain_sha256":
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Order/Preorder/Chain.lean",
    "mathlib_order_antichain_sha256":
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Order/Antichain.lean",
    "mathlib_order_height_sha256":
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Order/Height.lean",
    "mathlib_1000_yaml_sha256": "Formalizations/Lean/.lake/packages/mathlib/docs/1000.yaml",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def path_manifest_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        digest.update(relative.encode() + b"\0" + hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def parse_timestamp(value: str) -> dt.datetime:
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}", value)
    return dt.datetime.fromisoformat(value)


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path)
    data = path.read_bytes()
    assert data.endswith(b"\n"), "worker packet is missing a final newline"
    assert b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    assert set(packet) == PACKET_KEYS
    assert packet["schema_version"] == "stage1-worker-selftest/1.0"
    assert packet["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert packet["item_id"] == ITEM_ID
    assert packet["state"] == "[_]"
    assert packet["phase"] == packet["intent"] == receipt["phase"] == "intake"
    assert packet["verdict"] == receipt["verdict"] == "no_state_change"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert [row["command"] for row in packet["command_results"]] == packet["commands"]
    assert all(isinstance(row["exit_code"], int) for row in packet["command_results"])
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["diff_summary"] == receipt["diff_summary"]
    assert packet["exact_statement_changes"] == receipt["exact_statement_change"]
    assert packet["source_revisions"]["repository_base"] == BASE_REVISION
    assert packet["source_revisions"]["mathlib_revision"] == receipt["worker_input_hashes"]["mathlib_revision"]
    assert packet["proof_body_locations"] == receipt["proof_body_locations"] == []
    assert packet["axiom_and_placeholder_result"] == receipt["axiom_and_placeholder_result"]
    assert packet["root_vector_before"] == receipt["root_vector_before"]
    assert packet["root_vector_after"] == receipt["root_vector_after"]
    assert packet["debt_delta_basis"] == receipt["debt_delta_basis"]
    assert packet["task_ids"] == [ITEM_ID] + [task["id"] for task in load(HERE / "task-dag.json")["tasks"]]
    assert packet["canonical_obligation_ids"] == receipt["canonical_obligation_ids"] == []
    assert packet["statement_fingerprints"] == receipt["statement_fingerprints"] == []
    assert packet["typed_graph_changes"] == receipt["typed_graph_changes"] == []
    assert packet["composition_certificates"] == receipt["composition_certificates"] == []
    assert packet["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    assert packet["provisional_receipt_ids"] == [receipt["receipt_id"]]
    assert packet["evidence_record"] == f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json"
    assert packet["first_failed_gate"] == receipt["first_failed_gate"]
    assert packet["remaining_root_cut_set"] == receipt["remaining_root_cut_set"]
    assert packet["actual_source_ownership"] == receipt["actual_source_ownership"]
    assert packet["declaration_ownership"] == receipt["declaration_ownership"]
    assert packet["readable_ownership"] == receipt["readable_ownership"]
    assert packet["change_impact_set"] == receipt["change_impact_set"]
    for field in (
        "owner",
        "validated_at",
        "review_due",
        "invalidation_inputs",
        "support_state",
        "supersession_state",
        "revocation_state",
        "incident_path",
    ):
        assert packet[field] == receipt[field]
    packet_ref = receipt["worker_packet_reference"]
    assert packet_ref["path"] == path.resolve().relative_to(ROOT).as_posix()
    assert packet_ref["schema_version"] == packet["schema_version"]
    assert packet_ref["sha256"] == sha256(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution_dag = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "Dilworth定理"
    assert target["category"] == instance["category"] == "组合数学 / 图论"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    item = next(row for row in execution_dag["items"] if row["id"] == ITEM_ID)
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

    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert formal["external_declaration_candidate"] == "minChainPartition_eq_antichainWidth"
    assert "fails" in formal["candidate_status"]
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M5", "R": "R3"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
    assert git(
        "rev-parse",
        f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md',
    ) == revisions["repository_source_record_blob"]
    for field, relative in SOURCE_HASHES.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    assert revisions["primary_source"]["observed_preview_pdf_sha256"] == (
        "6af3f64b82c9788779586fbc43d8fa845b24c3ff8f34414c5518aa3545b78243"
    )
    candidate = revisions["external_lean_candidate"]
    assert candidate["commit"] == "f82f920f05a381bb1ce5e8903bde33e27f4365b6"
    assert candidate["source_sha256"] == (
        "4bc86897588087f472b358830bba157b92994e2b0dd44c66805f57c29211c985"
    )
    assert candidate["current_pin_check_exit"] == 1
    assert "sorryAx" in candidate["current_pin_failure"]
    assert revisions["secondary_formalization_source"]["scope"] == (
        "finite partially ordered sets, represented in Coq by FPO U"
    )

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0819-{suffix}"
        authoritative = next(row for row in execution_dag["items"] if row["id"] == task_id)
        expected_tasks.append((task_id, [dependency]))
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
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
    assert catalog.count("**Dilworth定理**") == 1
    assert "- 提出者: Robert Dilworth" in catalog
    assert "- 时间: 1950" in catalog
    assert catalog.count("- 陈述: 偏序集分解为链的最小数目") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0819 Dilworth定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["content_addressed"] is False
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"
    assert receipt["signed"] is False
    assert receipt["owner"] == "Stage1 integration lane"
    for field in (
        "reviewer_policy",
        "validation_started_at",
        "validation_ended_at",
        "validated_at",
        "review_due",
        "support_window",
        "support_state",
        "supersession_state",
        "revocation_state",
        "incident_path",
        "archive_and_recovery_boundary",
    ):
        assert isinstance(receipt[field], str) and receipt[field]
    assert isinstance(receipt["invalidation_inputs"], list) and receipt["invalidation_inputs"]
    validation_start = parse_timestamp(receipt["validation_started_at"])
    validation_end = parse_timestamp(receipt["validation_ended_at"])
    validated_at = parse_timestamp(receipt["validated_at"])
    assert validation_start <= validation_end == validated_at

    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    recipes_by_id = {recipe["recipe_id"]: recipe for recipe in recipes}
    assert set(recipes_by_id) == {
        "S56-M-0819-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0819-INTAKE-RECIPE-LEAN-PROBE",
    }
    for recipe in recipes:
        assert set(recipe) == RECIPE_KEYS
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["env_allowlist"] == {}
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == 0
        assert recipe["covered_obligation_ids"] == [ITEM_ID]
    assert recipes_by_id["S56-M-0819-INTAKE-RECIPE-STRUCTURE"]["covered_declarations"] == []
    assert recipes_by_id["S56-M-0819-INTAKE-RECIPE-LEAN-PROBE"]["covered_declarations"] == PROBE_DECLARATIONS

    expected_nonreceipt_paths = {
        f"Stage1_Instances/{THEOREM_ID}/{name}"
        for name in OWNED_FILES
        if name != "intake-receipt.json"
    }
    owned_digests = receipt["owned_artifact_sha256"]
    assert set(owned_digests) == expected_nonreceipt_paths
    for relative, expected in owned_digests.items():
        assert expected == sha256(ROOT / relative), f"stale owned artifact hash: {relative}"

    dirty = receipt["dirty_input_evidence"]
    assert dirty["classification"] == "nonrelease_dirty_worker_input"
    assert dirty["release_eligible"] is False
    assert dirty["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]
    assert dirty["tracked_patch_sha256"] == hashlib.sha256(b"").hexdigest()
    assert dirty["preexisting_lake_symlink_target_sha256"] == receipt["worker_input_hashes"]["lake_symlink_target_string"].removeprefix("sha256:")

    packet_path = ROOT / receipt["worker_packet_reference"]["path"]
    manifest_paths = [ROOT / relative for relative in expected_nonreceipt_paths] + [packet_path]
    manifest_hash = path_manifest_hash(manifest_paths)
    assert receipt["nonrelease_input_manifest"]["sha256"] == manifest_hash
    assert dirty["untracked_input_manifest_sha256"] == manifest_hash
    assert dirty["initial_status_sha256"] == hashlib.sha256(
        b"?? Formalizations/Lean/.lake\n"
    ).hexdigest()
    final_status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT
    )
    assert dirty["final_status_sha256"] == hashlib.sha256(final_status).hexdigest()

    actions = receipt["validation_actions"]
    assert {action["action_id"] for action in actions} == {
        "S56-M-0819-INTAKE-ACTION-STRUCTURE",
        "S56-M-0819-INTAKE-ACTION-LEAN-PROBE",
    }
    action_by_recipe = {action["recipe_id"]: action for action in actions}
    assert set(action_by_recipe) == set(recipes_by_id)
    for recipe_id, action in action_by_recipe.items():
        recipe = recipes_by_id[recipe_id]
        assert action["recipe_sha256"] == canonical_json_sha256(recipe)
        assert re.fullmatch(r"[0-9a-f]{64}", action["input_manifest_sha256"])
        for field in ("stdout_sha256", "stderr_sha256", "log_sha256"):
            assert re.fullmatch(r"[0-9a-f]{64}", action[field])
        assert parse_timestamp(action["started_at"]) <= parse_timestamp(action["ended_at"])
        assert validation_start <= parse_timestamp(action["started_at"])
        assert parse_timestamp(action["ended_at"]) <= validation_end
        assert action["exit_code"] == recipe["expected_exit"]
        snapshot = action["repository_snapshot"]
        assert snapshot["commit"] == BASE_REVISION and snapshot["tree"] == BASE_TREE
        assert snapshot["dirty_classification"] == dirty["classification"]
        assert snapshot["tracked_patch_sha256"] == dirty["tracked_patch_sha256"]
        assert snapshot["untracked_input_manifest_sha256"] == manifest_hash
        assert action["covered_obligation_ids"] == [ITEM_ID]
        assert action["covered_declaration_ids"] == recipe["covered_declarations"]
        assert action["statement_fingerprints"] == []
        assert action["attestor_reference"] == "receipt.attestor"
        assert action["freshness_reference"] == "receipt.review_due"
        assert action["invalidation_reference"] == "receipt.invalidation_inputs"

    structure_inputs = [
        ROOT / "Docs/Stage1_Targets_rev-5.6.json",
        ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json",
        HERE / "instance.json",
        HERE / "task-dag.json",
        HERE / "check_intake.py",
    ]
    lean_inputs = [
        ROOT / "Formalizations/Lean/lean-toolchain",
        ROOT / "Formalizations/Lean/lake-manifest.json",
        HERE / "IntakeProbe.lean",
    ]
    assert action_by_recipe["S56-M-0819-INTAKE-RECIPE-STRUCTURE"]["input_manifest_sha256"] == path_manifest_hash(structure_inputs)
    assert action_by_recipe["S56-M-0819-INTAKE-RECIPE-LEAN-PROBE"]["input_manifest_sha256"] == path_manifest_hash(lean_inputs)

    structure_stdout = b"intake invariant check: ok (THM-M-0819 planned; H1/M5/R3; six open tasks)\n"
    structure_action = action_by_recipe["S56-M-0819-INTAKE-RECIPE-STRUCTURE"]
    assert structure_action["stdout_sha256"] == hashlib.sha256(structure_stdout).hexdigest()
    assert structure_action["stderr_sha256"] == hashlib.sha256(b"").hexdigest()
    assert structure_action["log_sha256"] == hashlib.sha256(structure_stdout).hexdigest()

    lean_action = action_by_recipe["S56-M-0819-INTAKE-RECIPE-LEAN-PROBE"]
    lean_recipe = recipes_by_id[lean_action["recipe_id"]]
    lean_result = subprocess.run(
        lean_recipe["argv"],
        cwd=ROOT / lean_recipe["cwd"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=lean_recipe["timeout_seconds"],
        check=False,
    )
    assert lean_result.returncode == 0
    assert lean_action["stdout_sha256"] == hashlib.sha256(lean_result.stdout).hexdigest()
    assert lean_action["stderr_sha256"] == hashlib.sha256(lean_result.stderr).hexdigest()
    assert lean_action["log_sha256"] == hashlib.sha256(lean_result.stdout + lean_result.stderr).hexdigest()

    blocker = receipt["blocker_observation"]
    assert blocker["classification"] == "expected_external_candidate_integration_failure"
    assert blocker["source_sha256"] == candidate["source_sha256"]
    assert blocker["exit_code"] == candidate["current_pin_check_exit"] == 1
    assert blocker["stdout_sha256"] == candidate["current_pin_check_output_sha256"]
    assert blocker["stderr_sha256"] == hashlib.sha256(b"").hexdigest()
    assert blocker["log_sha256"] == blocker["stdout_sha256"]
    assert blocker["proof_credit"] == "none"
    assert blocker["replay_boundary"]

    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["lean_toolchain"] == f"sha256:{revisions['lean_toolchain_file_sha256']}"
    assert worker_inputs["lake_manifest"] == f"sha256:{revisions['lake_manifest_sha256']}"
    assert worker_inputs["mathlib_revision"] == revisions["mathlib"]
    assert worker_inputs["mathlib_tree"] == revisions["mathlib_tree"]
    assert worker_inputs["external_candidate_source_sha256"] == candidate["source_sha256"]
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert worker_inputs["lake_symlink_target_string"] == f"sha256:{hashlib.sha256(lake_target).hexdigest()}"

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"{path.name} is missing a final newline"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"{path.name} has trailing whitespace"
        )

    if args.worker_packet:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0819 planned; H1/M5/R3; six open tasks)")


if __name__ == "__main__":
    main()
