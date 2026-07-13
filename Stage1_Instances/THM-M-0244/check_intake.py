#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0244."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0244"
ITEM_ID = "S56-M-0244-INTAKE"
RANK = 1254
BASE_REVISION = "c6fd6dad8fcfe5fd464416cd452f50286b546978"
BASE_TREE = "5a80b61d8fa09336779f8d1453dcfe4299c9472f"
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
    "applicable_projection_sha256": "Docs/Stage1_Blueprint_Applicable_Theorems.md",
    "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
    "execution_dag_sha256": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
    "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
    "repository_math_source_sha256": "Docs/researches/math_theorems.md",
    "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
    "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
    "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
    "mathlib_phragmen_lindelof_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Complex/PhragmenLindelof.lean"
    ),
    "mathlib_abs_max_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Complex/AbsMax.lean"
    ),
    "mathlib_superpolynomial_decay_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Asymptotics/SuperpolynomialDecay.lean"
    ),
    "mathlib_1000_docs_sha256": "Formalizations/Lean/.lake/packages/mathlib/docs/1000.yaml",
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


def canonical_json_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def path_bytes_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        digest.update(relative.encode() + b"\0" + path.read_bytes())
    return digest.hexdigest()


def path_manifest_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        digest.update(relative.encode() + b"\0" + hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def run_recipe(recipe: dict) -> tuple[int, bytes, bytes]:
    assert recipe["env_allowlist"] == {}
    assert recipe["network_policy"] == "denied"
    result = subprocess.run(
        recipe["argv"],
        cwd=ROOT / recipe["cwd"],
        text=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=recipe["timeout_seconds"],
        check=False,
    )
    return result.returncode, result.stdout, result.stderr


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    assert packet["schema_version"] == "stage1-worker-selftest/1.0"
    assert packet["item_id"] == ITEM_ID and packet["theorem_id"] == THEOREM_ID
    assert packet["intent"] == "intake" and packet["verdict"] == "no_state_change"
    assert packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert packet["receipt_id"] == receipt["receipt_id"]
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert packet["accepted_receipt_ids"] == packet["proof_body_locations"] == []
    assert packet["audit_complete"] is packet["theorem_complete"] is False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    parser.add_argument(
        "--replay-recipes",
        action="store_true",
        help="execute the recorded non-network recipes and verify their output hashes",
    )
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert manifest["scope"]["canonical_sorted_target_id_set_sha256"] == (
        "e07deabaab3463cc1f92cdf5c0cf50ad9f8270d35554529c375d20a8512d8f1a"
    )
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "林德勒夫定理"
    assert target["category"] == instance["category"] == "分析学 / 复分析"
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
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert len(formal["candidate_declarations"]) == 8
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    assert git(
        "rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md'
    ) == revisions["repository_source_record_blob"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0244-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        expected_tasks.append((task_id, [dependency]))
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
    assert catalog.count("**林德勒夫定理**") == 1
    assert "- 提出者: Ernst Lindelöf" in catalog
    assert "- 时间: 1908" in catalog
    assert catalog.count("- 陈述: 角区域内的Phragmén-Lindelöf原理") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0244 林德勒夫定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    neighbor_names = {
        row["theorem_id"]: row["name"] for row in instance["neighbor_target_boundaries"]
    }
    assert neighbor_names == {
        "THM-M-0225": "最大模原理",
        "THM-M-0503": "林德勒夫假设",
        "THM-M-1332": "皮卡-林德勒夫定理",
    }
    covered_neighbor_names = {
        row["theorem_id"]: row["name"]
        for row in manifest["targets"]
        if row["theorem_id"] in {"THM-M-0225", "THM-M-1332"}
    }
    assert covered_neighbor_names == {
        "THM-M-0225": "最大模原理",
        "THM-M-1332": "皮卡-林德勒夫定理",
    }
    assert all(row["theorem_id"] != "THM-M-0503" for row in manifest["targets"])
    assert "- [ ] THM-M-0503 林德勒夫假设" in stage0

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

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["phase"] == "intake" and receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["content_addressed_recipe_ids"] == receipt["content_addressed_receipt_ids"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"
    assert receipt["owner"] == "Stage1 integration lane"
    for field in (
        "reviewer_policy", "validation_started_at", "validation_ended_at", "validated_at",
        "review_due", "support_window", "support_state", "supersession_state",
        "revocation_state", "incident_path", "archive_and_recovery_boundary",
    ):
        assert isinstance(receipt[field], str) and receipt[field]
    for field in ("validation_started_at", "validation_ended_at", "validated_at"):
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}", receipt[field])
    started_at = datetime.fromisoformat(receipt["validation_started_at"])
    ended_at = datetime.fromisoformat(receipt["validation_ended_at"])
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    assert started_at <= ended_at == validated_at <= datetime.now(timezone.utc).astimezone()

    dirty = receipt["dirty_input_evidence"]
    assert dirty["classification"] == "nonrelease_dirty_worker_input"
    assert dirty["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]
    nonrecursive_owned = [HERE / name for name in OWNED_FILES if name != "intake-receipt.json"]
    assert dirty["owned_untracked_patch_sha256"] == path_bytes_hash(nonrecursive_owned)
    assert dirty["owned_untracked_manifest_sha256"] == path_manifest_hash(nonrecursive_owned)

    recipe_fields = {
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy",
        "expected_exit", "expected_outputs", "covered_obligation_ids", "covered_declarations",
    }
    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2 and all(set(recipe) == recipe_fields for recipe in recipes)
    recipes_by_id = {recipe["recipe_id"]: recipe for recipe in recipes}
    assert set(recipes_by_id) == {
        "S56-M-0244-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0244-INTAKE-RECIPE-LEAN-PROBE",
    }
    for recipe in recipes:
        assert not Path(recipe["cwd"]).is_absolute() and ".." not in Path(recipe["cwd"]).parts
        assert recipe["env_allowlist"] == {} and recipe["network_policy"] == "denied"
        assert 0 < recipe["timeout_seconds"] <= 120 and recipe["expected_exit"] == 0
        assert recipe["covered_obligation_ids"] == [ITEM_ID]
        assert recipe["expected_outputs"] == [
            {"path_or_stream": "stdout", "semantic_hash_policy": "exact_bytes_sha256"},
            {"path_or_stream": "stderr", "semantic_hash_policy": "exact_bytes_sha256"},
        ]

    actions = receipt["validation_actions"]
    assert {action["action_id"] for action in actions} == {
        "S56-M-0244-INTAKE-ACTION-STRUCTURE",
        "S56-M-0244-INTAKE-ACTION-LEAN-PROBE",
    }
    actions_by_recipe = {action["recipe_id"]: action for action in actions}
    structure_inputs = [
        ROOT / "Docs/Stage1_Targets_rev-5.6.json",
        ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json",
        HERE / "instance.json", HERE / "task-dag.json", HERE / "check_intake.py",
    ]
    lean_inputs = [
        ROOT / "Formalizations/Lean/lean-toolchain",
        ROOT / "Formalizations/Lean/lake-manifest.json",
        HERE / "IntakeProbe.lean",
    ]
    assert actions_by_recipe["S56-M-0244-INTAKE-RECIPE-STRUCTURE"]["input_manifest_sha256"] == path_manifest_hash(structure_inputs)
    assert actions_by_recipe["S56-M-0244-INTAKE-RECIPE-LEAN-PROBE"]["input_manifest_sha256"] == path_manifest_hash(lean_inputs)
    for recipe_id, action in actions_by_recipe.items():
        recipe = recipes_by_id[recipe_id]
        assert action["recipe_sha256"] == canonical_json_sha256(recipe)
        assert action["exit_code"] == 0
        assert action["covered_obligation_ids"] == [ITEM_ID]
        assert action["covered_declarations"] == recipe["covered_declarations"]
        for field in ("recipe_sha256", "input_manifest_sha256", "stdout_sha256", "stderr_sha256", "log_sha256"):
            assert re.fullmatch(r"[0-9a-f]{64}", action[field])
        assert action["log_sha256"] == hashlib.sha256(
            bytes.fromhex(action["stdout_sha256"]) + bytes.fromhex(action["stderr_sha256"])
        ).hexdigest()
        if args.replay_recipes:
            code, stdout, stderr = run_recipe(recipe)
            assert code == recipe["expected_exit"] == action["exit_code"]
            assert hashlib.sha256(stdout).hexdigest() == action["stdout_sha256"]
            assert hashlib.sha256(stderr).hexdigest() == action["stderr_sha256"]

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"trailing whitespace: {path.name}"
        )
    for name in ("README.md", "instance.json", "scope-map.md", "source-statement-crosswalk.md", "task-dag.json", "validation.md", "intake-receipt.json"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0244 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
