#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0218 planned intake."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0218"
ITEM_ID = "S56-M-0218-INTAKE"
RANK = 1011
BASE_REVISION = "d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9"
BASE_TREE = "829a47c47ae831cada4f8acc6c2c00ba5883215e"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
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


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path.name} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main() -> None:
    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution_dag = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")
    selftest = load(ROOT / ".stage1-worker-selftest.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    item = next(row for row in execution_dag["items"] if row["id"] == ITEM_ID)

    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "庞加莱圆盘模型"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 106
    assert (
        target["lifecycle_mode"]
        == instance["lifecycle_mode"]
        == dag["lifecycle_mode"]
        == "planned"
    )
    assert (
        target["theorem_complete"]
        is instance["theorem_complete"]
        is dag["theorem_complete"]
        is False
    )
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"

    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert (
        instance["theorem_id"]
        == dag["theorem_id"]
        == receipt["theorem_id"]
        == selftest["theorem_id"]
        == THEOREM_ID
    )
    assert instance["item_id"] == receipt["item_id"] == selftest["item_id"] == ITEM_ID
    assert instance["intent"] == receipt["intent"] == selftest["intent"] == "intake"
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
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
    assert instance["hypotheses"] == []
    assert all(form["checked_witness"] is None for form in instance["alternate_encodings"])
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert (
        instance["accepted_proof_state"]
        == instance["accepted_receipt_ids"]
        == dag["accepted_states"]
        == []
    )
    assert (
        instance["audit_complete"]
        is receipt["audit_complete"]
        is selftest["audit_complete"]
        is False
    )
    assert (
        instance["theorem_complete"]
        is receipt["theorem_complete"]
        is selftest["theorem_complete"]
        is False
    )

    expected_tasks = []
    dependency = ITEM_ID
    for suffix in TASK_SUFFIXES:
        task_id = f"S56-M-0218-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])
    assert all(task["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"] for task in dag["tasks"])
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]

    actual_artifacts = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual_artifacts == OWNED_FILES
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == set(selftest["changed_paths"]) == expected_changed
    assert receipt["proposed_state"] == selftest["state"] == "[_]"
    assert receipt["accepted"] is False and receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == selftest["accepted_receipt_ids"] == []
    assert receipt["proof_body_locations"] == selftest["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["base_revision"] == selftest["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == selftest["base_tree"] == BASE_TREE
    assert receipt["receipt_id"] == selftest["receipt_id"]

    recorded = instance["source_revisions"]
    expected_hashes = {
        "target_manifest_sha256": "Docs/Stage1_Targets_rev-5.6.json",
        "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
        "execution_dag_sha256": "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
        "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
        "repository_math_source_sha256": "Docs/researches/math_theorems.md",
        "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
        "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
        "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
        "unit_disc_source_sha256": "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Complex/UnitDisc/Basic.lean",
        "conformal_source_sha256": "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Complex/Conformal.lean",
        "upper_half_plane_metric_source_sha256": "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Complex/UpperHalfPlane/Metric.lean",
    }
    for key, relative in expected_hashes.items():
        assert recorded[key] == sha256(ROOT / relative), f"stale input hash: {key}"
    assert recorded["repository_base"] == BASE_REVISION
    assert recorded["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert recorded["repository_source_record_commit"] == "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
    assert recorded["repository_source_record_blob"] == "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
    assert git(
        "rev-parse",
        "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f:Docs/researches/math_theorems.md",
    ) == recorded["repository_source_record_blob"]
    assert recorded["current_repository_math_source_blob"] == "b78ec1f48495aa5747ef252665ab58e418d195e4"
    assert git("hash-object", "Docs/researches/math_theorems.md") == recorded[
        "current_repository_math_source_blob"
    ]
    assert recorded["mathlib"] == MATHLIB_REVISION
    assert recorded["mathlib_tree"] == "bdc39a3123201dae413a9d9be56ec242c19e5c2b"

    source_lines = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8").splitlines(True)
    assert hashlib.sha256("".join(source_lines[1570:1576]).encode()).hexdigest() == recorded[
        "repository_record_excerpt_sha256"
    ]
    catalog_lines = "".join(source_lines)
    assert "**庞加莱圆盘模型**" in catalog_lines
    assert "- 提出者: Henri Poincaré" in catalog_lines
    assert "- 时间: 1882" in catalog_lines
    assert "- 陈述: 双曲几何的共形模型" in catalog_lines
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0218 庞加莱圆盘模型" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    neighbor_ids = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert neighbor_ids == {"THM-M-0217", "THM-M-0219"}
    neighbor_names = {
        row["theorem_id"]: row["name"]
        for row in manifest["targets"]
        if row["theorem_id"] in neighbor_ids
    }
    assert neighbor_names == {"THM-M-0217": "克莱因模型", "THM-M-0219": "庞加莱半平面模型"}

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data, f"non-LF newline: {path.name}"
        assert b"\x00" not in data, f"NUL byte: {path.name}"
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"trailing whitespace: {path.name}"
        )

    for name in (
        "README.md",
        "instance.json",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "validation.md",
        "intake-receipt.json",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    lean_probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b", lean_probe)

    lake_link = ROOT / "Formalizations/Lean/.lake"
    assert lake_link.is_symlink()
    assert hashlib.sha256(os.readlink(lake_link).encode()).hexdigest() == LAKE_SYMLINK_TARGET_SHA256

    selftest_data = (ROOT / ".stage1-worker-selftest.json").read_bytes()
    assert selftest_data.endswith(b"\n") and b"\r" not in selftest_data and b"\x00" not in selftest_data
    assert all(not line.endswith((b" ", b"\t")) for line in selftest_data.splitlines())

    print("intake invariant check: ok (THM-M-0218 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
