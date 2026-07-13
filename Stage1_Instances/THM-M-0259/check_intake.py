#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0259 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0259"
ITEM_ID = "S56-M-0259-INTAKE"
RANK = 1267
BASE_REVISION = "c6fd6dad8fcfe5fd464416cd452f50286b546978"
BASE_TREE = "5a80b61d8fa09336779f8d1453dcfe4299c9472f"
SOURCE_RECORD_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_RECORD_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
SOURCE_RECORD_EXCERPT_SHA256 = "36bc5c121bf3001673009403df38784fb57efce7031f7439fe13a46f3602b2d8"
DUPLICATE_RECORD_EXCERPT_SHA256 = "589d866392f6fd515e0f428dbb6741fa70b5dba112668c15cd8eb6c66cf372ee"
STAGE0_EXCERPT_SHA256 = "a57b061620d0d01d0eaca973ccf7076cb48c8247795d237b465ade0946434359"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LAKE_SYMLINK_TARGET_SHA256 = "e8714e9ebb75a5da1eeb16fdb6f50831a6cab29f115df43fa8e7535b38f59826"
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
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "9601541c3966336c2ea27797f4ff93e3dd3d7adc4de88410cc8a6b60a7782190",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "1e2eb8e8c86ccef96bb4dcd85b33f1a06fcf76a7c54c0b51772ddc0b6cebe2c5",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_SOURCE_HASHES = {
    "Mathlib/Analysis/Meromorphic/Basic.lean": "0138f148fe0b14522d32623a40f51693797f770379bea9506d2b48389dd87d73",
    "Mathlib/Data/Complex/Basic.lean": "b26f6e653e122ea18e2dc1f790e46f6e3218b23bacd5d6b441324f11277c978b",
    "Mathlib/Dynamics/PeriodicPts/Defs.lean": "4964d3b8a9b3845e87d6be77efd6b886e6290112a8c59a29efcd70df15ac16e6",
    "Mathlib/Topology/Closure.lean": "19911cf0e1231c924d154956e7b4454532eada84369fc1ca9722e38c78444b17",
    "Mathlib/Topology/Compactification/OnePoint/Basic.lean": "4cafeabe9d0c45884b7648c9417bf854f3e154127c975e0c8bade0eb96722376",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    return hashlib.sha256("".join(lines[first - 1:last]).encode()).hexdigest()


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
    assert required <= set(packet)
    assert packet["schema_version"] == "stage1-worker-selftest/1.0"
    assert packet["item_id"] == ITEM_ID and packet["theorem_id"] == THEOREM_ID
    assert packet["intent"] == "intake" and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["receipt_path"] == f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json"
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert all(
        isinstance(command, dict)
        and isinstance(command.get("argv"), list)
        and command["argv"]
        and isinstance(command.get("exit_code"), int)
        for command in packet["commands"]
    )
    assert isinstance(packet["output_summary"], str) and packet["output_summary"].strip()
    assert packet["root_vector_after"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert packet["accepted_receipt_ids"] == []
    assert packet["owner"] == "Stage1 integration lane"
    assert packet["audit_complete"] is packet["theorem_complete"] is False


def check_source_hashes(instance: dict, receipt: dict) -> None:
    revisions = instance["source_revisions"]
    field_map = {
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
    for relative, expected in SOURCE_HASHES.items():
        assert sha256(ROOT / relative) == expected, f"unexpected pinned input hash: {relative}"
        assert receipt["source_inputs"][relative] == f"sha256:{expected}"
    for field, relative in field_map.items():
        assert revisions[field] == SOURCE_HASHES[relative], f"stale instance hash: {field}"


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
    assert target["name"] == instance["name_zh"] == "麦克马伦定理"
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

    duplicate = next(row for row in manifest["targets"] if row["theorem_id"] == "THM-M-1435")
    assert duplicate["execution_rank"] == 933 and duplicate["name"] == "McMullen定理"
    assert duplicate["category"] == "其他重要领域 / 动力系统"
    assert instance["duplicate_target_record"]["theorem_id"] == "THM-M-1435"

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
    assert instance["literal_source_claim_zh"] == "有理函数的Julia集"
    assert instance["canonical_statement"] is instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert revisions["repository_source_record_commit"] == SOURCE_RECORD_COMMIT
    assert revisions["repository_source_record_blob"] == SOURCE_RECORD_BLOB
    assert git("rev-parse", f"{SOURCE_RECORD_COMMIT}:Docs/researches/math_theorems.md") == SOURCE_RECORD_BLOB
    check_source_hashes(instance, receipt)

    catalog = ROOT / "Docs/researches/math_theorems.md"
    stage0 = ROOT / "Docs/Stage0_Blueprint.md"
    assert excerpt_sha256(catalog, 1864, 1869) == SOURCE_RECORD_EXCERPT_SHA256
    assert excerpt_sha256(catalog, 10481, 10486) == DUPLICATE_RECORD_EXCERPT_SHA256
    assert excerpt_sha256(stage0, 7166, 7191) == STAGE0_EXCERPT_SHA256
    catalog_text = catalog.read_text(encoding="utf-8")
    assert "**麦克马伦定理**" in catalog_text and "**McMullen定理**" in catalog_text
    assert "- 提出者: Curtis McMullen" in catalog_text
    assert "- 时间: 1994" in catalog_text and "- 陈述: 有理函数的Julia集" in catalog_text
    stage0_text = stage0.read_text(encoding="utf-8")
    assert "THM-M-0259 麦克马伦定理" in stage0_text
    assert "THM-M-1435 McMullen定理" in stage0_text
    assert "- 精确定义与前提条件: 待补充" in stage0_text

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    revision_fields = {
        "meromorphic_source_sha256": "Mathlib/Analysis/Meromorphic/Basic.lean",
        "complex_source_sha256": "Mathlib/Data/Complex/Basic.lean",
        "periodic_points_source_sha256": "Mathlib/Dynamics/PeriodicPts/Defs.lean",
        "closure_source_sha256": "Mathlib/Topology/Closure.lean",
        "one_point_source_sha256": "Mathlib/Topology/Compactification/OnePoint/Basic.lean",
    }
    for field, relative in revision_fields.items():
        assert sha256(mathlib / relative) == MATHLIB_SOURCE_HASHES[relative] == revisions[field]
    lake_link = ROOT / "Formalizations/Lean/.lake"
    assert lake_link.is_symlink()
    link_hash = hashlib.sha256(str(lake_link.readlink()).encode()).hexdigest()
    assert link_hash == LAKE_SYMLINK_TARGET_SHA256

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0259-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        expected_tasks.append((task_id, [dependency]))
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == [] and task["state"] == "open"
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks

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
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["covered_task_ids"] == [ITEM_ID]
    assert receipt["covered_declaration_ids"] == []
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["selftest_result"] == "pass"
    for field in ("validation_started_at", "validation_ended_at", "validated_at"):
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}", receipt[field])

    recipes = receipt["structured_validation_recipes"]
    assert {recipe["recipe_id"] for recipe in recipes} == {
        "S56-M-0259-INTAKE-RECIPE-STRUCTURE",
        "S56-M-0259-INTAKE-RECIPE-LEAN-PROBE",
    }
    assert all(recipe["network_policy"] == "denied" for recipe in recipes)
    assert all(recipe["expected_exit"] == recipe["observed_exit"] == 0 for recipe in recipes)
    assert all(recipe["covered_task_ids"] == [ITEM_ID] for recipe in recipes)
    assert all(recipe["covered_obligation_ids"] == [] for recipe in recipes)
    assert all(recipe["covered_declarations"] == [] for recipe in recipes)

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {path.name}"
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"trailing whitespace: {path.name}"
        )
    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0259 planned; H5/M4/R4; duplicate frozen; six open tasks)")


if __name__ == "__main__":
    main()
