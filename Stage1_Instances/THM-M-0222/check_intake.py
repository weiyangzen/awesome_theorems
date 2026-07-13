#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0222 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0222"
ITEM_ID = "S56-M-0222-INTAKE"
RANK = 1235
BASE_REVISION = "62fad55ced807fdc06921c45d6fcd1f9ad86a1c2"
BASE_TREE = "9d7c8fe49a4c859d90f3069dc47973ffc5ced768"
SOURCE_RECORD_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_RECORD_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
SOURCE_RECORD_EXCERPT_SHA256 = "1c31231598289cf3e34fbcd4fedda3e41f778c4e34c318713ebd2fc2a0f2cf92"
STAGE0_EXCERPT_SHA256 = "e814dbdf0c5d55ae1af334461fa4b9bf26ec08d5883855d70192586f5ced8cf0"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LAKE_SYMLINK_TARGET_WITH_NEWLINE_SHA256 = (
    "e7d8a6bce8b934a5b0dc162324c830c4f26e1146c65bb31e8063491a3f47bfcc"
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
TASK_SUFFIXES = [
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
]
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
    "mathlib_cauchy_integral_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Complex/CauchyIntegral.lean"
    ),
    "mathlib_circle_integral_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/CircleIntegral.lean"
    ),
    "foreign_legacy_wrapper_sha256": (
        "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_178.lean"
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


def owned_input_hashes() -> tuple[str, str]:
    paths = sorted(
        path
        for path in HERE.iterdir()
        if path.is_file() and path.name != "intake-receipt.json"
    )
    manifest = b"".join(
        str(path.relative_to(ROOT)).encode()
        + b"\0"
        + sha256(path).encode()
        + b"\n"
        for path in paths
    )
    patch = b"".join(
        str(path.relative_to(ROOT)).encode()
        + b"\0"
        + str(len(path.read_bytes())).encode()
        + b"\0"
        + path.read_bytes()
        for path in paths
    )
    return hashlib.sha256(patch).hexdigest(), hashlib.sha256(manifest).hexdigest()


def input_manifest_hash(paths: list[Path]) -> str:
    manifest = b"".join(
        str(path.relative_to(ROOT)).encode()
        + b"\0"
        + sha256(path).encode()
        + b"\n"
        for path in paths
    )
    return hashlib.sha256(manifest).hexdigest()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path)
    data = path.read_bytes()
    assert data.endswith(b"\n"), "worker packet is missing a final newline"
    assert b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
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
    assert packet["commands"] == receipt["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]


def check_source_inputs(instance: dict, receipt: dict) -> None:
    revisions = instance["source_revisions"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        actual = sha256(ROOT / relative)
        assert revisions[field] == actual, f"stale instance source hash: {field}"
        assert receipt["source_inputs"][relative] == f"sha256:{actual}", (
            f"stale receipt source hash: {relative}"
        )


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
    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "柯西积分公式",
        "category": "分析学 / 复分析",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 86,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }

    item = next(row for row in execution_dag["items"] if row["id"] == ITEM_ID)
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
    assert instance["execution_rank"] == target["execution_rank"]
    assert instance["baseline"] == target["baseline"] == "L0"
    assert instance["rework_required"] is target["rework_required"] is True
    assert instance["legacy_artifacts_accepted"] is target["legacy_artifacts_accepted"] is False
    assert instance["legacy_priority_slot"] is target["legacy_priority_slot"] is None
    assert instance["target_lane"] == target["target_lane"]
    assert instance["intake_score"] == target["intake_score"]
    assert instance["source_status_untrusted"] == target["source_status_untrusted"]
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == receipt["phase"] == "intake"

    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == instance["hypotheses"] == []
    assert instance["alternate_encodings"] == instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert (
        git("rev-parse", f"{SOURCE_RECORD_COMMIT}:Docs/researches/math_theorems.md")
        == revisions["repository_source_record_blob"]
        == SOURCE_RECORD_BLOB
    )
    catalog_lines = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8").splitlines(True)
    stage0_lines = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8").splitlines(True)
    assert hashlib.sha256("".join(catalog_lines[1604:1610]).encode()).hexdigest() == (
        revisions["repository_record_excerpt_sha256"]
    ) == SOURCE_RECORD_EXCERPT_SHA256
    assert hashlib.sha256("".join(stage0_lines[6166:6192]).encode()).hexdigest() == (
        revisions["stage0_projection_excerpt_sha256"]
    ) == STAGE0_EXCERPT_SHA256
    assert revisions["mathlib"] == MATHLIB_REVISION
    assert revisions["mathlib_tree"] == MATHLIB_TREE
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    check_source_inputs(instance, receipt)

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0222-{suffix}"
        authoritative = next(row for row in execution_dag["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        expected_tasks.append((task_id, [dependency]))
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [
            f"Stage1_Instances/{THEOREM_ID}"
        ]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    catalog = "".join(catalog_lines)
    assert "**柯西积分公式**" in catalog
    assert "- 提出者: Augustin Cauchy" in catalog
    assert "- 时间: 1831" in catalog
    assert "- 陈述: 全纯函数由边界值表示" in catalog
    stage0 = "".join(stage0_lines)
    assert "THM-M-0222 柯西积分公式" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    neighbor_ids = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert neighbor_ids == {"THM-M-0221", "THM-M-0223", "THM-M-0224", "THM-M-1145", "THM-M-1559"}
    manifest_names = {
        row["theorem_id"]: row["name"]
        for row in manifest["targets"]
        if row["theorem_id"] in neighbor_ids
    }
    assert manifest_names == {
        "THM-M-0221": "柯西积分定理",
        "THM-M-0223": "留数定理",
        "THM-M-0224": "刘维尔定理",
        "THM-M-1145": "Cauchy估计",
        "THM-M-1559": "Riemann-Hilbert问题",
    }

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert set(receipt["artifact_sha256"]) == OWNED_FILES - {"intake-receipt.json"}
    for name, expected in receipt["artifact_sha256"].items():
        assert sha256(HERE / name) == expected, f"owned artifact hash mismatch: {name}"

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["acceptance_authority"] == "integration lane"
    assert receipt["attestor"]["signature"] is None
    assert receipt["attestor"]["signature_status"] == "unsigned_provisional_worker_report"
    assert receipt["platform"]["operating_system"] == platform.system()
    assert receipt["platform"]["architecture"] == platform.machine()
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"

    lake_link = ROOT / "Formalizations/Lean/.lake"
    assert lake_link.is_symlink()
    lake_target_with_newline = (os.readlink(lake_link) + "\n").encode()
    assert hashlib.sha256(lake_target_with_newline).hexdigest() == (
        LAKE_SYMLINK_TARGET_WITH_NEWLINE_SHA256
    )
    dirty = receipt["dirty_input_evidence"]
    assert dirty["preexisting_lake_symlink_target_sha256"] == hashlib.sha256(
        os.readlink(lake_link).encode()
    ).hexdigest()
    patch_hash, manifest_hash = owned_input_hashes()
    assert dirty["owned_untracked_patch_sha256"] == patch_hash
    assert dirty["owned_untracked_manifest_sha256"] == manifest_hash
    actions = {action["action_id"]: action for action in receipt["validation_actions"]}
    assert actions[f"{ITEM_ID}-ACTION-STRUCTURE"]["input_manifest_sha256"] == input_manifest_hash(
        [
            ROOT / "Docs/Stage1_Targets_rev-5.6.json",
            ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json",
            HERE / "instance.json",
            HERE / "task-dag.json",
            HERE / "check_intake.py",
        ]
    )
    assert actions[f"{ITEM_ID}-ACTION-LEAN-PROBE"]["input_manifest_sha256"] == input_manifest_hash(
        [
            ROOT / "Formalizations/Lean/lean-toolchain",
            ROOT / "Formalizations/Lean/lake-manifest.json",
            ROOT
            / "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Complex/CauchyIntegral.lean",
            HERE / "IntakeProbe.lean",
        ]
    )
    for recipe in receipt["structured_validation_recipes"]:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert isinstance(recipe["env_allowlist"], dict)
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == 0
        assert recipe["covered_task_ids"] == [ITEM_ID]
        assert recipe["covered_obligation_ids"] == []

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

    public_files = {
        "README.md",
        "instance.json",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "task-dag.json",
        "validation.md",
        "intake-receipt.json",
    }
    forbidden_fragments = ("/" + "home" + "/", "." + "cron" + "/")
    forbidden_completion_claim = "theorem_complete" + "=true"
    for name in public_files:
        text = (HERE / name).read_text(encoding="utf-8")
        assert all(fragment not in text for fragment in forbidden_fragments)
        assert forbidden_completion_claim not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(
        r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|constant|opaque|unsafe)[ \t]",
        probe,
        flags=re.MULTILINE,
    )

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet.resolve(), receipt)

    print("intake invariant check: ok (THM-M-0222 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
