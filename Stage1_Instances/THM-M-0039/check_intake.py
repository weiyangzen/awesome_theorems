#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0039 planned intake."""

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
THEOREM_ID = "THM-M-0039"
ITEM_ID = "S56-M-0039-INTAKE"
RANK = 1517
BASE_REVISION = "d66b6e80968b53d5b99774584721ae8976f303a5"
BASE_TREE = "aaa82721074fccea81033a9a18d21652af89f8e4"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
INTAKE_FILES = {
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
MATHLIB_HASH_FIELDS = {
    "mathlib_free_algebra_source_sha256": "Mathlib/Algebra/FreeAlgebra.lean",
    "mathlib_simple_ring_basic_source_sha256": "Mathlib/RingTheory/SimpleRing/Basic.lean",
    "mathlib_simple_ring_field_source_sha256": "Mathlib/RingTheory/SimpleRing/Field.lean",
    "mathlib_simple_module_source_sha256": "Mathlib/RingTheory/SimpleModule/Basic.lean",
    "mathlib_wedderburn_artin_source_sha256":
        "Mathlib/RingTheory/SimpleModule/WedderburnArtin.lean",
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


def run_recorded_action(recipe: dict) -> bytes:
    assert recipe["network_policy"] == "denied"
    env = os.environ.copy()
    env.update(recipe["env_allowlist"])
    result = subprocess.run(
        recipe["argv"],
        cwd=ROOT / recipe["cwd"],
        env=env,
        text=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=recipe["timeout_seconds"],
        check=False,
    )
    assert result.returncode == recipe["expected_exit"]
    return result.stdout


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    assert packet["schema_version"] == "stage1-worker-selftest/1.0"
    assert packet["item_id"] == ITEM_ID and packet["theorem_id"] == THEOREM_ID
    assert packet["intent"] == "intake" and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["receipt_id"] == receipt["receipt_id"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["accepted_receipt_ids"] == []
    assert packet["audit_complete"] is packet["theorem_complete"] is False
    assert packet["owner"] == receipt["owner"] == "Stage1 integration lane"
    assert packet["validated_at"] == receipt["validated_at"]
    assert isinstance(packet["commands"], list) and packet["commands"]
    for field in (
        "validated_at",
        "review_due",
        "support_state",
        "supersession_state",
        "revocation_state",
        "incident_path",
    ):
        assert isinstance(packet[field], str) and packet[field]
    assert isinstance(packet["invalidation_inputs"], list) and packet["invalidation_inputs"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()
    strict_worker = args.worker_packet is not None

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "卡普兰斯基定理"
    assert target["category"] == instance["category"] == "代数学 / 环论"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 78
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is False

    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] in {"[ ]", "[_]", "[x]"}
    if strict_worker:
        assert item["state"] == "[ ]"
    assert item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == (
        "Create the theorem dossier, scope map, and source-statement crosswalk."
    )
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["literal_source_claim_zh"] == "关于PI环的结构"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    assert git(
        "rev-parse",
        f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md',
    ) == revisions["repository_source_record_blob"]
    assert sha256(ROOT / "Docs/researches/math_theorems.md") == revisions[
        "repository_math_source_sha256"
    ]
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions[
        "mathlib_tree"
    ] == MATHLIB_TREE
    for field, relative in MATHLIB_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"

    if strict_worker:
        assert git("rev-parse", "HEAD") == BASE_REVISION
        assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
        for field, relative in SOURCE_HASH_FIELDS.items():
            assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
        lake = ROOT / "Formalizations/Lean/.lake"
        assert lake.is_symlink()
        assert hashlib.sha256(str(lake.readlink()).encode()).hexdigest() == revisions[
            "lake_symlink_target_sha256"
        ]

    expected_tasks = []
    dependency = ITEM_ID
    for suffix in TASK_SUFFIXES:
        task_id = f"S56-M-0039-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])
    for task in dag["tasks"]:
        authority = next(row for row in execution["items"] if row["id"] == task["id"])
        assert task["phase"] == authority["phase"]
        assert task["deliverable"] == authority["deliverable"]
        assert task["owned_paths"] == authority["owned_paths"]
        assert task["completion_gate"] == authority["completion_gate"]
        assert task["gate_id"] == f'{task["id"]}-GATE'
        assert task["owned_sources"] == authority["owned_paths"]
        assert task["covered_obligation_ids"] == task["validation_spec_ids"] == []

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**卡普兰斯基定理**" in catalog
    assert "- 提出者: Irving Kaplansky" in catalog
    assert "- 时间: 1958" in catalog
    assert "- 陈述: 关于PI环的结构" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0039 卡普兰斯基定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    assert instance["primary_source_candidate_not_credited"]["candidate_statement"] == (
        "A primitive algebra satisfying a polynomial identity is finite-dimensional over its center."
    )

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == INTAKE_FILES
    assert INTAKE_FILES <= actual_files
    if strict_worker:
        assert actual_files == INTAKE_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in INTAKE_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    digests = receipt["owned_artifact_sha256"]
    assert set(digests) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in INTAKE_FILES
    }
    for relative, expected in digests.items():
        if relative.endswith("/intake-receipt.json"):
            assert expected == "self_referential_excluded_from_provisional_digest"
            continue
        assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"

    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["root_vector_before"] == {
        "H": "unclassified",
        "M": "unclassified",
        "R": "unclassified",
    }
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["owner"] == "Stage1 integration lane"
    assert isinstance(receipt["output_summary"], str) and receipt["output_summary"]
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
    for field in ("validation_started_at", "validation_ended_at", "validated_at"):
        assert re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}", receipt[field]
        )
    dirty = receipt["dirty_input_evidence"]
    assert dirty["classification"] == "nonrelease_dirty_worker_input"
    assert dirty["preexisting_untracked_paths"] == ["Formalizations/Lean/.lake"]
    nonrecursive_owned = [HERE / name for name in INTAKE_FILES if name != "intake-receipt.json"]
    assert dirty["owned_untracked_patch_sha256"] == path_bytes_hash(nonrecursive_owned)
    assert dirty["owned_untracked_manifest_sha256"] == path_manifest_hash(nonrecursive_owned)

    actions = receipt["validation_actions"]
    action_by_id = {action["action_id"]: action for action in actions}
    assert set(action_by_id) == {
        "S56-M-0039-INTAKE-ACTION-STRUCTURE",
        "S56-M-0039-INTAKE-ACTION-LEAN-PROBE",
        "S56-M-0039-INTAKE-ACTION-EXACT-SEARCH",
    }
    recipes = receipt["structured_validation_recipes"]
    recipes_by_id = {recipe["recipe_id"]: recipe for recipe in recipes}
    assert len(recipes_by_id) == 3
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
    assert all(set(recipe) == required_recipe_keys for recipe in recipes)
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
        assert action["exit_code"] == recipe["expected_exit"]
        assert action["covered_obligation_ids"] == [ITEM_ID]

    structure_inputs = [
        ROOT / "Docs/Stage1_Targets_rev-5.6.json",
        ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json",
        HERE / "instance.json",
        HERE / "task-dag.json",
        HERE / "check_intake.py",
    ]
    assert action_by_id["S56-M-0039-INTAKE-ACTION-STRUCTURE"][
        "input_manifest_sha256"
    ] == path_manifest_hash(structure_inputs)
    lean_inputs = [
        ROOT / "Formalizations/Lean/lean-toolchain",
        ROOT / "Formalizations/Lean/lake-manifest.json",
        *[mathlib / relative for relative in MATHLIB_HASH_FIELDS.values()],
        HERE / "IntakeProbe.lean",
    ]
    assert action_by_id["S56-M-0039-INTAKE-ACTION-LEAN-PROBE"][
        "input_manifest_sha256"
    ] == path_manifest_hash(lean_inputs)
    structure_stdout = (
        b"intake invariant check: ok "
        b"(THM-M-0039 planned; H1/M3/R4; six open tasks)\n"
    )
    structure_hash = hashlib.sha256(structure_stdout).hexdigest()
    structure_action = action_by_id["S56-M-0039-INTAKE-ACTION-STRUCTURE"]
    assert structure_action["stdout_sha256"] == structure_hash
    assert structure_action["log_sha256"] == structure_hash

    for action_id in (
        "S56-M-0039-INTAKE-ACTION-LEAN-PROBE",
        "S56-M-0039-INTAKE-ACTION-EXACT-SEARCH",
    ):
        action = action_by_id[action_id]
        output = run_recorded_action(recipes_by_id[action["recipe_id"]])
        output_hash = hashlib.sha256(output).hexdigest()
        assert action["stdout_sha256"] == action["log_sha256"] == output_hash

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    for name in INTAKE_FILES:
        path = HERE / name
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {name}"
        assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {name}"
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"trailing whitespace: {name}"
        )
    for name in (
        "README.md",
        "instance.json",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "task-dag.json",
        "validation.md",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    lean_probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in lean_probe for token in prohibited)

    if strict_worker:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0039 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
