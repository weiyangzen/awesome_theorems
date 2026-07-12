#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-1444."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-1444"
ITEM_ID = "S56-M-1444-INTAKE"
RANK = 1052
BASE_REVISION = "3815f6945257af057dfb5e6b6dfe2be5b6f451d9"
BASE_TREE = "21a4f0ff758e83ab68c05b7741cdc4720f95cb1c"
SOURCE_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
SOURCE_EXCERPT_SHA256 = "4b67565a2268681bc7c9dccacda395197868075dce82ad4e655c1b5268f09d5f"
STAGE0_EXCERPT_SHA256 = "dc29a0bc0ca3bf2764c67b331491a7fdfea10f20700be29d45884356d87ae901"
PRIMARY_SOURCE_SHA256 = "87c9b019a592cb2c16755db15e54b0df2a2a43c4769cc0df8aca4d9514b75445"
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
TASK_SUFFIXES = [
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
]
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
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    return hashlib.sha256("".join(lines[first - 1 : last]).encode("utf-8")).hexdigest()


def check_receipt_inputs(receipt: dict) -> None:
    for relative, tagged_digest in receipt["source_inputs"].items():
        assert tagged_digest.startswith("sha256:")
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}", (
            f"stale receipt input hash: {relative}"
        )


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
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution_dag = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")
    check_receipt_inputs(receipt)

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "Banach不动点定理"
    assert target["category"] == instance["category"] == "其他重要领域 / 数值分析"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["intake_score"] == instance["intake_score"] == 92
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
    assert "exact_source_complete_root_not_selected" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    assert formal["module"] is formal["declaration_or_expression"] is None
    assert formal["elaborated_expression_hash"] is formal["environment_fingerprint"] is None
    assert formal["gate_state"] == "blocked_source_complete_root_and_formal_encoding_not_selected"
    assert instance["quantifiers"] == instance["ordered_binders"] == instance["hypotheses"] == []
    assert instance["alternate_encodings"] == instance["excluded_degenerate_cases"] == []
    assert instance["root_vector"] == receipt["root_vector_after"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert "10.4064/fm-3-1-133-181" in json.dumps(instance)
    assert instance["source_candidates_not_credited_as_H0"][0]["observed_scan_sha256"] == PRIMARY_SOURCE_SHA256
    assert any(row["theorem_id"] == "THM-M-1443" for row in instance["neighbor_target_boundaries"])
    candidate_names = {row["declaration"] for row in instance["formal_candidates_not_credited"]}
    assert {
        "ContractingWith.exists_fixedPoint",
        "ContractingWith.exists_fixedPoint'",
        "ContractingWith.fixedPoint_isFixedPt",
        "ContractingWith.fixedPoint_unique",
        "ContractingWith.tendsto_iterate_fixedPoint",
    } <= candidate_names

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    assert revisions["repository_source_record_commit"] == SOURCE_COMMIT
    assert revisions["repository_source_record_blob"] == SOURCE_BLOB
    assert revisions["repository_record_excerpt_sha256"] == SOURCE_EXCERPT_SHA256
    assert revisions["stage0_projection_excerpt_sha256"] == STAGE0_EXCERPT_SHA256
    assert revisions["primary_source_observed_scan_sha256"] == PRIMARY_SOURCE_SHA256
    assert revisions["mathlib"] == MATHLIB_REVISION and revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert git("rev-parse", f"{SOURCE_COMMIT}:Docs/researches/math_theorems.md") == SOURCE_BLOB
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 10546, 10551) == SOURCE_EXCERPT_SHA256
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 39271, 39296) == STAGE0_EXCERPT_SHA256
    for field, relative in SOURCE_HASHES.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {relative}"
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert revisions["mathlib_contracting_source_sha256"] == sha256(
        mathlib / "Mathlib/Topology/MetricSpace/Contracting.lean"
    )

    assert dag["accepted_states"] == []
    assert len(dag["tasks"]) == len(TASK_SUFFIXES)
    for index, (task, suffix) in enumerate(zip(dag["tasks"], TASK_SUFFIXES), start=1):
        assert task["id"] == f"S56-M-1444-{suffix}"
        expected_dependency = ITEM_ID if index == 1 else dag["tasks"][index - 2]["id"]
        assert task["depends_on"] == [expected_dependency]
        assert task["state"] == "open" and task["layer"] == index
        assert task["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"
        assert task["evidence_ids"] == []

    assert {path.name for path in HERE.iterdir() if path.is_file()} == OWNED_FILES
    assert instance["owned_artifacts"] == [
        "README.md",
        "instance.json",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "task-dag.json",
        "IntakeProbe.lean",
        "check_intake.py",
        "validation.md",
        "intake-receipt.json",
    ]
    for name in OWNED_FILES:
        data = (HERE / name).read_bytes()
        assert data.endswith(b"\n"), f"{name} is missing a final newline"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"trailing whitespace in {name}"
        )
        assert str(ROOT).encode() not in data, f"absolute worker path leaked into {name}"

    expected_changed = {f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES}
    expected_changed.add(".stage1-worker-selftest.json")
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["proof_body_locations"] == []
    assert receipt["covered_node_ids"] == [ITEM_ID]
    assert receipt["known_failures"]
    assert receipt["selftest_result"] == "pass"
    assert receipt["status_boundary"] == instance["status_boundary"]

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet.resolve(), receipt)

    print("intake invariant check: ok (THM-M-1444 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
