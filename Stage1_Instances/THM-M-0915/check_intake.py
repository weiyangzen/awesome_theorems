#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0915 planned intake."""

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
THEOREM_ID = "THM-M-0915"
ITEM_ID = "S56-M-0915-INTAKE"
RANK = 1457
BASE_REVISION = "db4b8793e70ce8af74c9c9490acfa50aa3684d5e"
BASE_TREE = "6434a20532ae7c523ad293e67a6228ab384bfb8a"
SOURCE_RECORD_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_RECORD_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
SOURCE_RECORD_EXCERPT_SHA256 = "8a858a14ec40c742793406044666d4ab8e087930f26a8667e64ac67b13577dbf"
STAGE0_EXCERPT_SHA256 = "3dc80cbe82e20abf943f62261eacbfc492af55d20aba800643ef93696db26c13"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
ROOT_VECTOR = {"H": "H5", "M": "M4", "R": "R4"}
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
SOURCE_HASHES = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_Applicable_Theorems.md": "779e4bd66e6a1c7615ca2884d899f02a871096125a30b8e229536fa5937cc85c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "5d0eb6d57ec108d3083f15d6e3773447c9e9287fa6d2f811ff6197055aa251f5",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "7005d2c291a900e175666f0826ee69b15bb77d208b4fb167174d0982f20055a3",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
INTEGRATION_MUTABLE_HASHES = {
    "Docs/Stage1_Blueprint_rev-5.6.md",
    "Docs/Stage1_Execution_DAG_rev-5.6.json",
}
MATHLIB_HASHES = {
    "Mathlib/RingTheory/PowerSeries/Basic.lean": "292d4961f3963c223b47b4ba71fcc026b1349976165773931e77795318a36fa4",
    "Mathlib/Combinatorics/Enumerative/Partition/GenFun.lean": "6c100971d90ae521c717e8b2ab58b34362e365704f5e525a4c22522f3bbbc34c",
    "Mathlib/RingTheory/PowerSeries/Catalan.lean": "e1c48fd18aa40d91213a66caeb8dfddfc63dcb3fda7d6f34e00df50147016c60",
}


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), f"{path} must contain an object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def lines_sha256(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1 : end])).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def git_blob_sha256(revision: str, relative: str) -> str:
    data = subprocess.check_output(
        ["git", "show", f"{revision}:{relative}"], cwd=ROOT, stderr=subprocess.DEVNULL
    )
    return hashlib.sha256(data).hexdigest()


def check_text_file(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path}"
    assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {path}"
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
        f"trailing whitespace: {path}"
    )


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
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
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"].strip()
    assert packet["known_failures"] == receipt["known_failures"]
    check_text_file(path.resolve())


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
    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "生成函数",
        "category": "组合数学 / 计数组合",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 86,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    assert instance["execution_rank"] == RANK
    assert instance["name_zh"] == target["name"]
    assert instance["category"] == target["category"]
    assert instance["baseline"] == target["baseline"] == "L0"
    assert instance["rework_required"] is target["rework_required"] is True
    assert instance["legacy_artifacts_accepted"] is target["legacy_artifacts_accepted"] is False
    assert instance["target_lane"] == target["target_lane"]
    assert instance["source_status_untrusted"] == target["source_status_untrusted"]

    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] in {"[ ]", "[_]"} and item["depends_on"] == []
    if args.worker_packet is not None:
        assert item["state"] == "[ ]", "worker base must precede provisional integration"
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["literal_source_claim_zh"] == "组合序列的生成函数方法"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "candidate_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == receipt["root_vector_after"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert dag["accepted_states"] == receipt["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    if args.worker_packet is not None:
        assert git("rev-parse", "HEAD") == BASE_REVISION
    else:
        subprocess.check_call(["git", "merge-base", "--is-ancestor", BASE_REVISION, "HEAD"], cwd=ROOT)
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
    assert git("rev-parse", f"{SOURCE_RECORD_COMMIT}:Docs/researches/math_theorems.md") == SOURCE_RECORD_BLOB
    assert revisions["repository_source_record_blob"] == SOURCE_RECORD_BLOB
    assert lines_sha256(ROOT / "Docs/researches/math_theorems.md", 6693, 6698) == SOURCE_RECORD_EXCERPT_SHA256
    assert lines_sha256(ROOT / "Docs/Stage0_Blueprint.md", 24958, 24983) == STAGE0_EXCERPT_SHA256

    field_map = {
        "target_manifest_sha256": "Docs/Stage1_Targets_rev-5.6.json",
        "applicable_theorems_sha256": "Docs/Stage1_Blueprint_Applicable_Theorems.md",
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
        assert git_blob_sha256(BASE_REVISION, relative) == expected, f"unexpected base input: {relative}"
        if relative not in INTEGRATION_MUTABLE_HASHES:
            assert sha256(ROOT / relative) == expected, f"changed pinned input: {relative}"
        assert receipt["source_inputs"][relative] == f"sha256:{expected}"
    for field, relative in field_map.items():
        assert revisions[field] == SOURCE_HASHES[relative], f"stale instance hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    for relative, expected in MATHLIB_HASHES.items():
        assert sha256(mathlib / relative) == expected, f"changed mathlib source: {relative}"

    expected_tasks = []
    dependency = ITEM_ID
    authoritative_tasks = {
        row["id"]: row for row in execution["items"] if row["theorem_id"] == THEOREM_ID
    }
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0915-{suffix}"
        expected_tasks.append((task_id, [dependency], layer))
        dependency = task_id
    assert [(task["id"], task["depends_on"], task["layer"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" and task["evidence_ids"] == [] for task in dag["tasks"])
    for task in dag["tasks"]:
        authoritative = authoritative_tasks[task["id"]]
        for field in ("phase", "layer", "depends_on", "owned_paths", "deliverable", "completion_gate"):
            assert task[field] == authoritative[field], f"task authority drift: {task['id']} {field}"

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**生成函数**") == 1
    assert "- 提出者: 众多数学家" in catalog
    assert "- 时间: 18世纪" in catalog
    assert catalog.count("- 陈述: 组合序列的生成函数方法") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0915 生成函数" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    neighbor_ids = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert neighbor_ids == {"THM-M-0916", "THM-M-0917", "THM-M-0921", "THM-M-0922", "THM-M-0923", "THM-M-0925"}
    manifest_names = {
        row["theorem_id"]: row["name"]
        for row in manifest["targets"]
        if row["theorem_id"] in neighbor_ids
    }
    assert manifest_names == {row["theorem_id"]: row["name"] for row in instance["neighbor_target_boundaries"]}

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = [".stage1-worker-selftest.json"] + [
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in sorted(OWNED_FILES)
    ]
    assert receipt["changed_paths"] == expected_changed
    assert set(receipt["artifact_sha256"]) == OWNED_FILES - {"intake-receipt.json"}
    for name, expected in receipt["artifact_sha256"].items():
        assert sha256(HERE / name) == expected, f"stale artifact hash: {name}"
    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["content_addressed"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["covered_node_ids"] == [ITEM_ID]
    assert receipt["selftest_result"] == "pass"
    assert receipt["worker_input_hashes"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["worker_input_hashes"]["mathlib_tree"] == MATHLIB_TREE
    lake_root = ROOT / "Formalizations/Lean/.lake"
    if args.worker_packet is not None:
        assert lake_root.is_symlink()
        target_string_hash = hashlib.sha256(os.readlink(lake_root).encode()).hexdigest()
        assert receipt["worker_input_hashes"]["lake_symlink_target_string"] == f"sha256:{target_string_hash}"
    assert (lake_root / "packages/mathlib/Mathlib").is_dir()
    for recipe in receipt["structured_validation_recipes"]:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["observed_exit"] == 0
        assert recipe["covered_ids"] == [ITEM_ID]
        assert isinstance(recipe["input_hashes"], dict) and recipe["input_hashes"]

    for path in HERE.iterdir():
        if path.is_file():
            check_text_file(path)
    for name in ("README.md", "instance.json", "scope-map.md", "source-statement-crosswalk.md", "validation.md", "intake-receipt.json"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|constant|opaque|unsafe)[ \t]", probe, re.MULTILINE)

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0915 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
