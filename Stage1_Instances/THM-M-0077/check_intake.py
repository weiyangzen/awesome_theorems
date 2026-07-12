#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0077."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0077"
ITEM_ID = "S56-M-0077-INTAKE"
RANK = 1025
BASE_REVISION = "35681bf154be61836528486ed7830f619fc03231"
BASE_TREE = "b45fc969fef64ad53ac30dc548894b08e8bef834"
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
    "mathlib_solvable_source_sha256": "Mathlib/GroupTheory/Solvable.lean",
    "mathlib_sylow_source_sha256": "Mathlib/GroupTheory/Sylow.lean",
    "mathlib_schur_zassenhaus_source_sha256": "Mathlib/GroupTheory/SchurZassenhaus.lean",
    "mathlib_zgroup_source_sha256": "Mathlib/GroupTheory/SpecificGroups/ZGroup.lean",
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
    packet_path = path.resolve()
    packet = load(packet_path)
    data = packet_path.read_bytes()
    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert isinstance(packet["commands"], list) and packet["commands"]
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
    assert target["name"] == instance["name_zh"] == "霍尔定理"
    assert target["category"] == instance["category"] == "代数学 / 群论"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 96
    assert target["source_status_untrusted"] == "已验证"
    assert instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False
    assert instance["theorem_complete"] is False

    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == (
        "Create the theorem dossier, scope map, and source-statement crosswalk."
    )
    assert item["completion_gate"] == (
        "rev-5.6 node-specific receipt and master acceptance"
    )

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"]
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert dag["lifecycle_mode"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["literal_source_claim_zh"] == "有限可解群中Hall子群的存在性"
    assert instance["canonical_statement"] is None
    assert instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[key] is None
    assert instance["ordered_binders"] == instance["quantifiers"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False
    assert receipt["accepted"] is False and receipt["proposed_state"] == "[_]"
    assert receipt["verdict"] == "no_state_change"

    assert set(instance["owned_artifacts"]) == OWNED_FILES
    assert {path.name for path in HERE.iterdir() if path.is_file()} == OWNED_FILES
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD:Docs/researches/math_theorems.md") == (
        revisions["repository_math_source_current_blob"]
    )
    assert git(
        "rev-parse",
        f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md',
    ) == revisions["repository_source_record_blob"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"

    catalog_lines = (ROOT / "Docs/researches/math_theorems.md").read_text(
        encoding="utf-8"
    ).splitlines(True)
    catalog_excerpt = "".join(catalog_lines[567:573])
    assert sha256_bytes(catalog_excerpt.encode()) == revisions[
        "repository_record_excerpt_sha256"
    ]
    assert "**霍尔定理**" in catalog_excerpt
    assert "- 提出者: Philip Hall" in catalog_excerpt
    assert "- 时间: 1928" in catalog_excerpt
    assert "- 陈述: 有限可解群中Hall子群的存在性" in catalog_excerpt
    stage0_lines = (ROOT / "Docs/Stage0_Blueprint.md").read_text(
        encoding="utf-8"
    ).splitlines(True)
    stage0_excerpt = "".join(stage0_lines[2216:2242])
    assert sha256_bytes(stage0_excerpt.encode()) == revisions[
        "stage0_projection_excerpt_sha256"
    ]
    assert "THM-M-0077 霍尔定理" in stage0_excerpt
    assert "- 精确定义与前提条件: 待补充" in stage0_excerpt

    marriage = [
        row for row in manifest["targets"] if row["theorem_id"] == "THM-M-0815"
    ]
    assert len(marriage) == 1
    assert marriage[0]["name"] == "霍尔婚配定理"
    assert marriage[0]["category"] == "组合数学 / 图论"
    assert "Hall's marriage theorem" in instance["excluded_substitutions"][0]

    source = instance["primary_source_candidates_not_credited"][0]
    assert "10.1112/jlms/s1-3.2.98" in source["citation"]
    assert source["candidate_locator"].startswith("exact theorem/page")
    assert "no proposition" in source["status"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert not git("status", "--short", cwd=mathlib)
    for field, relative in MATHLIB_SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(mathlib / relative), f"stale mathlib hash: {field}"

    expected_tasks = []
    dependency = ITEM_ID
    authoritative_by_id = {
        row["id"]: row
        for row in execution["items"]
        if row["theorem_id"] == THEOREM_ID and row["id"] != ITEM_ID
    }
    for suffix in TASK_SUFFIXES:
        task_id = f"S56-M-0077-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        source_task = authoritative_by_id[task_id]
        for key in (
            "depends_on",
            "phase",
            "layer",
            "owned_paths",
            "deliverable",
            "completion_gate",
        ):
            assert task[key] == source_task[key]
        assert task["evidence_ids"] == [] and task["state"] == "open"
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert len(authoritative_by_id) == len(dag["tasks"]) == 6

    receipt_paths = set(receipt["changed_paths"])
    expected_changed = {
        ".stage1-worker-selftest.json",
        *(f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES),
    }
    assert receipt_paths == expected_changed
    assert receipt["root_vector_after"] == {
        "H": "H1",
        "M": "M4",
        "R": "R4",
        "boundary": "provisional planned intake projection only; master acceptance pending",
    }
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["canonical_obligation_ids"] == []
    assert receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == []
    assert receipt["composition_certificates"] == []
    assert receipt["proof_body_locations"] == []
    assert receipt["remaining_root_cut_set"] == [
        f"S56-M-0077-{suffix}" for suffix in TASK_SUFFIXES
    ]
    assert receipt["selftest_result"] == "pass"
    assert receipt["validated_at"] is not None
    assert receipt["worker_input_hashes"]["intake_probe_source_sha256"] == sha256(
        HERE / "IntakeProbe.lean"
    )
    assert receipt["worker_input_hashes"]["intake_probe_output_sha256"] is not None
    assert all(recipe["exit_code"] == 0 for recipe in receipt["structured_validation_recipes"])
    assert receipt["commands_and_results"]

    assert "sorry" not in (HERE / "IntakeProbe.lean").read_text(encoding="utf-8").lower()
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print(
        "THM-M-0077 intake check: PASS "
        "(planned H1/M4/R4; exact statement and all downstream gates open)"
    )


if __name__ == "__main__":
    main()
