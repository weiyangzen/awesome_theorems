#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0281 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0281"
ITEM_ID = "S56-M-0281-INTAKE"
RANK = 1287
BASE_REVISION = "2eea98305d46266f078a50cf0e85853bf6a5e702"
BASE_TREE = "02279a8caa5f31ed8e37e35c8584a336eed9b974"
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
    "mathlib_integral_source_sha256": "Mathlib/Analysis/Convex/Integral.lean",
    "mathlib_finite_jensen_source_sha256": "Mathlib/Analysis/Convex/Jensen.lean",
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
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    return hashlib.sha256("".join(lines[first - 1:last]).encode()).hexdigest()


def canonical_json_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def path_manifest_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        digest.update(relative.encode() + b"\0" + hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def run_recorded_action(recipe: dict) -> bytes:
    assert recipe["env_allowlist"] == {}
    assert recipe["network_policy"] == "denied"
    result = subprocess.run(
        recipe["argv"],
        cwd=ROOT / recipe["cwd"],
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
    assert packet["schema_version"] == "stage1-worker-selftest/1.0"
    assert packet["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["phase"] == packet["intent"] == receipt["phase"] == "intake"
    assert packet["verdict"] == receipt["verdict"] == "no_state_change"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert [row["command"] for row in packet["command_results"]] == packet["commands"]
    assert all(row["exit_code"] == 0 for row in packet["command_results"])
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["diff_summary"] == receipt["diff_summary"]
    assert packet["proof_body_locations"] == receipt["proof_body_locations"] == []
    assert packet["exact_statement_changes"].startswith("No exact mathematical or Lean statement")
    assert packet["source_revisions"]["repository_base"] == BASE_REVISION
    assert packet["source_revisions"]["mathlib_revision"] == MATHLIB_REVISION
    assert "No theorem or proof body was added" in packet["axiom_and_placeholder_result"]
    assert packet["root_vector_before"] == receipt["root_vector_before"]
    assert packet["root_vector_after"] == receipt["root_vector_after"]
    assert packet["debt_delta_basis"] == receipt["debt_delta_basis"]
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
        "owner", "validated_at", "review_due", "invalidation_inputs", "support_state",
        "supersession_state", "revocation_state", "incident_path",
    ):
        assert packet[field] == receipt[field]
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

    matches = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    assert matches == [{
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "延森不等式",
        "category": "分析学 / 实分析",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 86,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }]
    target = matches[0]
    assert instance["execution_rank"] == RANK
    assert instance["name_zh"] == target["name"]
    assert instance["category"] == target["category"]
    for field in (
        "legacy_priority_slot", "baseline", "rework_required",
        "legacy_artifacts_accepted", "target_lane", "intake_score",
        "source_status_untrusted", "lifecycle_mode", "theorem_complete",
    ):
        assert instance[field] == target[field]

    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item == {
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

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == receipt["phase"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "primary_source_selected_root" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert "ConvexOn.map_integral_le" in formal["declaration_candidates"]
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert (
        git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md')
        == revisions["repository_source_record_blob"]
    )
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 2020, 2025) == revisions["repository_record_excerpt_sha256"]
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 7765, 7790) == revisions["stage0_record_excerpt_sha256"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    for field, relative in MATHLIB_SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib source hash: {field}"

    dependency = ITEM_ID
    authoritative = execution["items"]
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0281-{suffix}"
        task = dag["tasks"][layer - 1]
        source = next(row for row in authoritative if row["id"] == task_id)
        assert task["id"] == task_id and task["depends_on"] == [dependency]
        assert task["state"] == "open" and task["layer"] == source["layer"] == layer
        assert task["phase"] == source["phase"]
        assert task["owned_paths"] == source["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == source["deliverable"]
        assert task["completion_gate"] == source["completion_gate"]
        assert task["evidence_ids"] == []
        dependency = task_id

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**延森不等式**" in catalog
    assert "- 提出者: Johan Jensen" in catalog
    assert "- 时间: 1906" in catalog
    assert "- 陈述: 凸函数的积分不等式" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0281 延森不等式" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = [".stage1-worker-selftest.json"] + [
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in sorted(OWNED_FILES)
    ]
    assert receipt["changed_paths"] == expected_changed
    hashes = receipt["owned_artifact_sha256"]
    expected_hashed = set(expected_changed) - {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json",
    }
    assert set(hashes) == expected_hashed
    for relative, expected in hashes.items():
        assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"
    nonreceipt_files = [path for path in HERE.iterdir() if path.is_file() and path.name != "intake-receipt.json"]
    assert (
        receipt["nonrelease_input_manifest"]["owned_nonreceipt_manifest_sha256"]
        == path_manifest_hash(nonreceipt_files)
    )
    assert receipt["nonrelease_input_manifest"]["release_eligible"] is False

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is receipt["signed"] is False
    assert receipt["lifecycle_before"] == receipt["lifecycle_after"] == "planned"
    assert receipt["assurance_baseline_before"] == "L0 / rework_required"
    assert receipt["attestor"]["signature"] is None
    assert receipt["platform"]["architecture"] == "x86_64"
    assert receipt["worker_packet_reference"]["sha256"] == sha256(ROOT / ".stage1-worker-selftest.json")
    for key in (
        "accepted_receipt_ids", "proof_body_locations", "canonical_obligation_ids",
        "statement_fingerprints", "typed_graph_changes", "composition_certificates",
        "content_addressed_recipe_ids", "content_addressed_receipt_ids",
    ):
        assert receipt[key] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["root_vector_after"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert receipt["selftest_result"] == "pass"
    dirty = receipt["dirty_input_evidence"]
    assert dirty["classification"] == "nonrelease_dirty_worker_input"
    assert dirty["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]

    recipes = receipt["structured_validation_recipes"]
    required_recipe_keys = {
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations",
    }
    assert len(recipes) == 2
    assert all(set(recipe) == required_recipe_keys for recipe in recipes)
    assert all(recipe["network_policy"] == "denied" for recipe in recipes)
    assert all(recipe["expected_exit"] == 0 for recipe in recipes)
    assert all(recipe["covered_obligation_ids"] == [ITEM_ID] for recipe in recipes)
    recipes_by_id = {recipe["recipe_id"]: recipe for recipe in recipes}
    actions = receipt["validation_actions"]
    assert len(actions) == 2
    for action in actions:
        recipe = recipes_by_id[action["recipe_id"]]
        identity = {
            "cwd": recipe["cwd"],
            "argv": recipe["argv"],
            "env_allowlist": recipe["env_allowlist"],
            "timeout_seconds": recipe["timeout_seconds"],
            "network_policy": recipe["network_policy"],
            "expected_exit": recipe["expected_exit"],
        }
        assert action["recipe_sha256"] == canonical_json_sha256(identity)
        assert action["started_at"] <= action["ended_at"] <= receipt["validated_at"]
        assert action["exit_code"] == 0 and action["covered_obligation_ids"] == [ITEM_ID]
        for field in ("recipe_sha256", "input_manifest_sha256", "stdout_sha256", "log_sha256"):
            assert re.fullmatch(r"[0-9a-f]{64}", action[field])
    action_by_id = {action["action_id"]: action for action in actions}
    structure = action_by_id["S56-M-0281-INTAKE-ACTION-STRUCTURE"]
    lean = action_by_id["S56-M-0281-INTAKE-ACTION-LEAN-PROBE"]
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
    assert structure["input_manifest_sha256"] == path_manifest_hash(structure_inputs)
    assert lean["input_manifest_sha256"] == path_manifest_hash(lean_inputs)
    structure_stdout = b"intake invariant check: ok (THM-M-0281 planned; H1/M3/R4; six open tasks)\n"
    assert structure["stdout_sha256"] == structure["log_sha256"] == hashlib.sha256(structure_stdout).hexdigest()
    lean_stdout = run_recorded_action(recipes_by_id[lean["recipe_id"]])
    lean_hash = hashlib.sha256(lean_stdout).hexdigest()
    assert lean["stdout_sha256"] == lean["log_sha256"] == lean_hash

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()

    if args.worker_packet:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0281 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
