#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0757."""

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
THEOREM_ID = "THM-M-0757"
ITEM_ID = "S56-M-0757-INTAKE"
RANK = 1343
BASE_REVISION = "d05520867fab3367a9b61b9544c3e12241204f54"
BASE_TREE = "fb2cfc62077d5b53e9938632cd6361dd60872067"
SOURCE_RECORD_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_RECORD_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
SOURCE_RECORD_EXCERPT_SHA256 = "65df298407a658bce224e99524969adbf6697f3822185c5cb4fd9e34382100bc"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LAKE_SYMLINK_TARGET_SHA256 = "e8714e9ebb75a5da1eeb16fdb6f50831a6cab29f115df43fa8e7535b38f59826"
SUCCESS = "intake invariant check: ok (THM-M-0757 planned; H5/M4/R4; six open tasks)\n"
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
}
MATHLIB_HASH_FIELDS = {
    "mathlib_ordinal_basic_sha256": "Mathlib/SetTheory/Ordinal/Basic.lean",
    "mathlib_zfc_ordinal_sha256": "Mathlib/SetTheory/ZFC/Ordinal.lean",
    "mathlib_recursive_in_sha256": "Mathlib/Computability/RecursiveIn.lean",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def excerpt_sha256(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1 : end])).hexdigest()


def check_text_file(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path.name}"
    assert b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
        f"trailing whitespace: {path.name}"
    )


def check_worker_packet(path: Path, receipt: dict) -> None:
    path = path.resolve()
    packet = load(path)
    check_text_file(path)
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
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["known_failures"] == receipt["known_failures"]
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

    targets = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    items = [row for row in execution["items"] if row["theorem_id"] == THEOREM_ID]
    assert len(targets) == 1 and len(items) == 7
    target = targets[0]
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "可容许序数"
    assert target["category"] == instance["category"] == "数理逻辑 / 递归论"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    intake_item = next(row for row in items if row["id"] == ITEM_ID)
    assert intake_item["phase"] == "intake" and intake_item["layer"] == 0
    assert intake_item["state"] in {"[ ]", "[_]"} and intake_item["depends_on"] == []
    if args.worker_packet is not None:
        assert intake_item["state"] == "[ ]", "worker base must precede provisional integration"
        assert git("rev-parse", "HEAD") == BASE_REVISION
    else:
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", BASE_REVISION, "HEAD"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    assert intake_item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert intake_item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert intake_item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "no_stable_truth_valued_proposition" in instance["canonical_claim_status"]
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
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
    assert revisions["repository_source_record_commit"] == SOURCE_RECORD_COMMIT
    assert git("rev-parse", f"{SOURCE_RECORD_COMMIT}:Docs/researches/math_theorems.md") == (
        revisions["repository_source_record_blob"]
    ) == SOURCE_RECORD_BLOB
    assert git("rev-parse", f"{BASE_REVISION}:Docs/researches/math_theorems.md") == revisions["repository_math_source_blob_at_base"]
    assert git("rev-parse", f"{BASE_REVISION}:Docs/Stage0_Blueprint.md") == revisions["stage0_projection_blob_at_base"]
    assert revisions["repository_record_excerpt_sha256"] == excerpt_sha256(
        ROOT / "Docs/researches/math_theorems.md", 5577, 5582
    ) == SOURCE_RECORD_EXCERPT_SHA256
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    for field in (
        "crossref_bulletin_observed_json_sha256",
        "crossref_transactions_observed_json_sha256",
    ):
        assert re.fullmatch(r"[0-9a-f]{64}", revisions[field])

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    for field, relative in MATHLIB_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"
    lake_link = ROOT / "Formalizations/Lean/.lake"
    assert lake_link.is_symlink()
    assert hashlib.sha256(os.readlink(lake_link).encode()).hexdigest() == LAKE_SYMLINK_TARGET_SHA256

    authoritative = {row["id"]: row for row in items}
    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0757-{suffix}"
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        auth = authoritative[task_id]
        expected_tasks.append((task_id, [dependency]))
        assert task["phase"] == auth["phase"] and task["layer"] == auth["layer"] == layer
        assert task["owned_paths"] == auth["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == auth["deliverable"]
        assert task["completion_gate"] == auth["completion_gate"]
        assert task["state"] == "open" and task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    catalog_block = "\n".join(catalog.splitlines()[5576:5582])
    for marker in (
        "**可容许序数**",
        "- 提出者: Gerald Sacks",
        "- 时间: 1966",
        "- 陈述: α-递归论",
    ):
        assert marker in catalog_block
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0757 可容许序数" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    neighbor_ids = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert neighbor_ids == {
        "THM-M-0752",
        "THM-M-0753",
        "THM-M-0754",
        "THM-M-0755",
        "THM-M-0756",
        "THM-M-0758",
    }
    target_by_id = {row["theorem_id"]: row for row in manifest["targets"]}
    for neighbor in instance["neighbor_target_boundaries"]:
        assert target_by_id[neighbor["theorem_id"]]["name"] == neighbor["name"]

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    for path in HERE.iterdir():
        if path.is_file():
            check_text_file(path)
    digests = receipt["owned_artifact_sha256"]
    assert set(digests) == {f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES}
    for relative, expected_hash in digests.items():
        if relative.endswith("/intake-receipt.json"):
            assert expected_hash == "self_referential_excluded_from_provisional_digest"
        else:
            assert sha256(ROOT / relative) == expected_hash, f"stale owned hash: {relative}"

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["known_failures"] and receipt["selftest_result"] == "pass"
    assert receipt["first_failed_gate"].startswith("S56-M-0757-STATEMENT")
    assert {recipe["recipe_id"] for recipe in receipt["structured_validation_recipes"]} == {
        "S56-M-0757-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0757-INTAKE-RECIPE-LEAN-PROBE",
    }
    for recipe in receipt["structured_validation_recipes"]:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert isinstance(recipe["env_allowlist"], dict)
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["observed_exit"] == 0
        assert recipe["covered_task_ids"] == [ITEM_ID]
        assert recipe["covered_obligation_ids"] == []

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"
    for name in (
        "README.md",
        "instance.json",
        "intake-receipt.json",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "task-dag.json",
        "validation.md",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    lean_probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(
        r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        lean_probe,
        re.MULTILINE,
    )

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)
    print(SUCCESS, end="")


if __name__ == "__main__":
    main()
