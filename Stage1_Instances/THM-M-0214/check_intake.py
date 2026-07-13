#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0214 planned intake."""

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
THEOREM_ID = "THM-M-0214"
ITEM_ID = "S56-M-0214-INTAKE"
RANK = 1229
BASE_REVISION = "62fad55ced807fdc06921c45d6fcd1f9ad86a1c2"
BASE_TREE = "9d7c8fe49a4c859d90f3069dc47973ffc5ced768"
SOURCE_RECORD_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_RECORD_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
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


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path.name} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution_dag = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")
    selftest = load(args.worker_packet.resolve()) if args.worker_packet else None

    targets = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    items = [row for row in execution_dag["items"] if row["id"] == ITEM_ID]
    assert len(targets) == len(items) == 1
    target, item = targets[0], items[0]

    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "球面几何余弦定理"
    assert target["category"] == instance["category"] == "几何学 / 非欧几何"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] in {"[ ]", "[_]"} and item["depends_on"] == []
    if selftest is not None:
        assert item["state"] == "[ ]", "worker base must precede provisional integration"
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == []
    assert all(form["checked_witness"] is None for form in instance["alternate_encodings"])
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["open_task_dag"] == f"Stage1_Instances/{THEOREM_ID}/task-dag.json"
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    expected_tasks = []
    dependency = ITEM_ID
    for suffix in TASK_SUFFIXES:
        task_id = f"S56-M-0214-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])
    assert all(task["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"] for task in dag["tasks"])
    authoritative_rows = {
        row["id"]: row
        for row in execution_dag["items"]
        if row["theorem_id"] == THEOREM_ID and row["phase"] != "intake"
    }
    assert set(authoritative_rows) == {task["id"] for task in dag["tasks"]}
    for task in dag["tasks"]:
        authoritative = authoritative_rows[task["id"]]
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == []
    assert dag["audit_complete"] is False
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]

    actual_artifacts = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual_artifacts == OWNED_FILES
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is False and receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["reviewer_policy"]["self_acceptance_allowed"] is False
    assert "no accepted long-term support" in receipt["support_window"]
    assert receipt["revocation_state"].startswith("not_applicable_never_accepted")
    assert "blocks master acceptance" in receipt["archive_and_recovery_boundary"]
    assert all(word in receipt["incident_path"] for word in ("rejection", "supersession", "revocation"))
    artifact_hashes = receipt["owned_artifact_sha256"]
    assert set(artifact_hashes) == expected_changed
    for relative, digest in artifact_hashes.items():
        if relative == f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json":
            assert digest == "self_referential_excluded_from_provisional_digest"
        elif relative == ".stage1-worker-selftest.json":
            assert digest == "self_referential_handoff_excluded_from_provisional_receipt_digest"
        else:
            assert sha256(ROOT / relative) == digest, f"stale owned artifact hash: {relative}"
    assert "integration lane" in receipt["untracked_input_hash_boundary"]

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
        "euclidean_angle_sphere_source_sha256": "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Geometry/Euclidean/Angle/Sphere.lean",
        "euclidean_triangle_source_sha256": "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Geometry/Euclidean/Triangle.lean",
        "unoriented_angle_source_sha256": "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Geometry/Euclidean/Angle/Unoriented/Basic.lean",
    }
    for key, relative in expected_hashes.items():
        assert recorded[key] == sha256(ROOT / relative), f"stale input hash: {key}"
    assert recorded["repository_base"] == BASE_REVISION
    assert recorded["repository_base_tree"] == BASE_TREE
    if selftest is not None:
        assert git("rev-parse", "HEAD") == BASE_REVISION
    else:
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", BASE_REVISION, "HEAD"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
    assert recorded["repository_source_record_commit"] == SOURCE_RECORD_COMMIT
    assert recorded["repository_source_record_blob"] == SOURCE_RECORD_BLOB
    assert git("rev-parse", f"{SOURCE_RECORD_COMMIT}:Docs/researches/math_theorems.md") == SOURCE_RECORD_BLOB
    assert recorded["current_repository_math_source_blob"] == git("hash-object", "Docs/researches/math_theorems.md")
    assert recorded["mathlib"] == MATHLIB_REVISION and recorded["mathlib_tree"] == MATHLIB_TREE
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE

    source_lines = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8").splitlines(True)
    source_excerpt = "".join(source_lines[1542:1548])
    assert hashlib.sha256(source_excerpt.encode()).hexdigest() == recorded["repository_record_excerpt_sha256"]
    assert "**球面几何余弦定理**" in source_excerpt
    assert "- 提出者: 众多数学家" in source_excerpt
    assert "- 时间: 古代" in source_excerpt
    assert "- 陈述: 球面三角形边与角的关系" in source_excerpt
    discovery = {row["publisher_or_site"]: row for row in instance["human_source_discovery_not_credited"]}
    assert discovery["Encyclopedia of Mathematics"]["response_sha256"] == (
        "4d2e24b24bed1b949306af5b4cc88c7a6d58e3d84ba66c07821f48c8a7c6ecff"
    )
    assert discovery["Encyclopedia of Mathematics"]["response_bytes"] == 19064
    assert discovery["MathWorld"]["response_sha256"] == (
        "adb9e1af40ddc3c7bdcda48e08a77cb4949c159a1cfe688f01819cbd18dd00d0"
    )
    assert discovery["MathWorld"]["response_bytes"] == 103608
    assert all("not a repository artifact" in row["snapshot_boundary"] for row in discovery.values())
    stage0_lines = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8").splitlines(True)
    stage0_excerpt = "".join(stage0_lines[5945:5971])
    assert hashlib.sha256(stage0_excerpt.encode()).hexdigest() == recorded["stage0_record_excerpt_sha256"]
    assert "THM-M-0214 球面几何余弦定理" in stage0_excerpt
    assert "- 精确定义与前提条件: 待补充" in stage0_excerpt

    neighbor_ids = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert neighbor_ids == {"THM-M-0193", "THM-M-0215", "THM-M-0216"}
    neighbor_names = {
        row["theorem_id"]: row["name"]
        for row in manifest["targets"]
        if row["theorem_id"] in neighbor_ids
    }
    assert neighbor_names == {
        "THM-M-0193": "勾股定理",
        "THM-M-0215": "双曲余弦定理",
        "THM-M-0216": "高斯-博内定理",
    }

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"
    checked_paths = list(HERE.iterdir())
    if selftest is not None:
        checked_paths.append(args.worker_packet.resolve())
    for path in checked_paths:
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
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

    if selftest is not None:
        assert selftest["schema_version"] == "stage1-worker-selftest/1.0"
        assert selftest["item_id"] == ITEM_ID and selftest["theorem_id"] == THEOREM_ID
        assert selftest["intent"] == "intake" and selftest["state"] == "[_]"
        assert selftest["verdict"] == receipt["verdict"] == "no_state_change"
        assert selftest["base_revision"] == BASE_REVISION and selftest["base_tree"] == BASE_TREE
        assert set(selftest["changed_paths"]) == expected_changed
        assert selftest["receipt_id"] == receipt["receipt_id"]
        assert selftest["receipt_sha256"] == sha256(HERE / "intake-receipt.json")
        assert selftest["accepted_receipt_ids"] == []
        assert selftest["audit_complete"] is selftest["theorem_complete"] is False
        assert selftest["known_failures"] == receipt["known_failures"]
        assert selftest["root_vector_before"] == receipt["root_vector_before"]
        assert selftest["root_vector_after"] == receipt["root_vector_after"]
        assert selftest["first_failed_gate"] == receipt["first_failed_gate"]
        assert selftest["retry_condition"] == receipt["retry_condition"]
        assert selftest["remaining_root_cut_set"] == receipt["remaining_root_cut_set"]
        assert isinstance(selftest["commands"], list) and selftest["commands"]
        assert isinstance(selftest["output_summary"], str) and selftest["output_summary"]

    print("intake invariant check: ok (THM-M-0214 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
