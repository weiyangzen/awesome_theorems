#!/usr/bin/env python3
"""Fail-closed scoped validator for the THM-M-1475 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-1475"
ITEM_ID = "S56-M-1475-INTAKE"
RANK = 1152
BASE_REVISION = "f4efdfc7c685252a98f3508a5974ba81c0377a95"
BASE_TREE = "94a9cfc613f86042a21fdfa174ba887334b93893"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
OWNED_FILES = {
    "IntakeProbe.lean",
    "README.md",
    "check_intake.py",
    "instance.json",
    "intake-receipt.json",
    "scope-map.md",
    "source-statement-crosswalk.md",
    "task-dag.json",
    "validation.md",
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
    "Docs/Stage1_Blueprint_rev-5.6.md": "2e0d25fbfb60989e9c661f0c8be09ce1dcb4f1b6688f20a51d4528fea15d76cd",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "fd43e64009594dbffc9a38d4a1e28f09c75cf84151edbbe6368a80df4bb914d3",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Docs/Stage0_Blueprint.md": "ab92a43f9ca23ba446bf8cb881a787d30b99bc7181857fea049f5a8208b2b65f",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_HASHES = {
    "Mathlib/Analysis/ODE/Basic.lean": "ae12311010b33270373065089e7abbad74fc3df21b8067276301846890ac477d",
    "Mathlib/Data/Complex/Basic.lean": "b26f6e653e122ea18e2dc1f790e46f6e3218b23bacd5d6b441324f11277c978b",
    "Mathlib/FieldTheory/RatFunc/AsPolynomial.lean": "36136d6741ad08e83f45fcb821074a9b16dc7f71ab2e245654dc3f67342d3356",
    "Mathlib/LinearAlgebra/Matrix/ToLin.lean": "a58c81046f02ed406daaf24bd50ab7a68c5e5b43f906b6c8180aea740c49ac2a",
}
EXCERPT_HASHES = {
    "catalog": "c3e292af7c0858266314a055e5acd58a8db88dccbcd5bc868ff31dad5a189881",
    "stage0": "92c07524f10554dcc8e616ab8db80392e51353a0c56545342565ad26517af9ba",
    "general_rk": "8c5ff1593d79712179602045dd82f3f7839b8ac7a320ff8806a77b4879a1e201",
    "neighbors": "4ebfacbf576a213f3be167912a49e41a6cbaba7b28828adb3915c06211c443e6",
}


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_sha256(path: Path, first_line: int, last_line: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first_line - 1 : last_line])).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def check_authorities(instance: dict) -> list[dict]:
    manifest = load_json(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    matches = [row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID]
    assert matches == [
        {
            "execution_rank": RANK,
            "legacy_priority_slot": None,
            "theorem_id": THEOREM_ID,
            "name": "龙格-库塔法的稳定性",
            "category": "其他重要领域 / 数值分析",
            "source_status_untrusted": "已验证",
            "baseline": "L0",
            "rework_required": True,
            "legacy_artifacts_accepted": False,
            "target_lane": "hard_statement_first_partial_verification",
            "intake_score": 86,
            "lifecycle_mode": "planned",
            "theorem_complete": False,
        }
    ]
    target = matches[0]
    for field in (
        "execution_rank",
        "legacy_priority_slot",
        "baseline",
        "rework_required",
        "legacy_artifacts_accepted",
        "target_lane",
        "intake_score",
        "source_status_untrusted",
        "lifecycle_mode",
        "theorem_complete",
    ):
        assert instance[field] == target[field]
    assert instance["name_zh"] == target["name"]
    assert instance["category"] == target["category"]

    items = load_json(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]
    intake = next(row for row in items if row["id"] == ITEM_ID)
    assert intake == {
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
    return items


def check_instance(instance: dict) -> None:
    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == THEOREM_ID and instance["item_id"] == ITEM_ID
    assert instance["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert instance["intent"] == "intake"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "no_stable_truth_valued_proposition" in instance["canonical_claim_status"]
    formal = instance["canonical_formal_target"]
    for field in (
        "module",
        "declaration_or_expression",
        "candidate_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        assert formal[field] is None
    assert "not_a_stable_proposition" in formal["gate_state"]
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert "does not refute" in instance["status_boundary"]
    assert "No canonical mathematical or Lean statement" in instance["status_boundary"]
    assert "or master acceptance is claimed" in instance["status_boundary"]

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert (
        git("rev-parse", "HEAD:Docs/researches/math_theorems.md")
        == revisions["current_repository_math_source_blob"]
    )
    assert (
        git(
            "rev-parse",
            f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md',
        )
        == revisions["repository_source_record_blob"]
    )
    for path, expected in SOURCE_HASHES.items():
        assert sha256(ROOT / path) == expected, f"changed authoritative input: {path}"
    assert revisions["target_manifest_sha256"] == SOURCE_HASHES["Docs/Stage1_Targets_rev-5.6.json"]
    assert revisions["authoritative_blueprint_sha256"] == SOURCE_HASHES["Docs/Stage1_Blueprint_rev-5.6.md"]
    assert revisions["execution_dag_sha256"] == SOURCE_HASHES["Docs/Stage1_Execution_DAG_rev-5.6.json"]
    assert revisions["execution_skill_sha256"] == SOURCE_HASHES["skills/execute-stage1-rev56/SKILL.md"]
    assert revisions["blueprint_guidelines_sha256"] == SOURCE_HASHES["Docs/Blueprint_Guidelines.md"]
    assert revisions["repository_math_source_sha256"] == SOURCE_HASHES["Docs/researches/math_theorems.md"]
    assert revisions["stage0_blueprint_sha256"] == SOURCE_HASHES["Docs/Stage0_Blueprint.md"]
    assert revisions["lean_toolchain_file_sha256"] == SOURCE_HASHES["Formalizations/Lean/lean-toolchain"]
    assert revisions["lake_manifest_sha256"] == SOURCE_HASHES["Formalizations/Lean/lake-manifest.json"]

    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 10763, 10768) == EXCERPT_HASHES["catalog"]
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 40108, 40133) == EXCERPT_HASHES["stage0"]
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 10167, 10172) == EXCERPT_HASHES["general_rk"]
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 10770, 10789) == EXCERPT_HASHES["neighbors"]
    assert revisions["repository_record_excerpt_sha256"] == EXCERPT_HASHES["catalog"]
    assert revisions["stage0_projection_excerpt_sha256"] == EXCERPT_HASHES["stage0"]
    assert revisions["general_rk_record_excerpt_sha256"] == EXCERPT_HASHES["general_rk"]
    assert revisions["neighbor_stability_record_excerpt_sha256"] == EXCERPT_HASHES["neighbors"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    for path, expected in MATHLIB_HASHES.items():
        assert sha256(mathlib / path) == expected, f"changed mathlib input: {path}"


def check_lake_symlink(receipt: dict) -> None:
    lake = ROOT / "Formalizations/Lean/.lake"
    assert lake.is_symlink(), "the automation-provided .lake path must remain a symlink"
    target_hash = hashlib.sha256(str(lake.readlink()).encode("utf-8")).hexdigest()
    assert target_hash == receipt["worker_input_hashes"]["lake_symlink_target_string_sha256"]


def check_catalog_and_boundaries(instance: dict) -> None:
    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**龙格-库塔法的稳定性**") == 1
    assert catalog.count("- 陈述: RK方法的稳定性区域") == 1
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-1475 龙格-库塔法的稳定性" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0
    boundaries = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert {"THM-M-1396", "THM-M-1474", "THM-M-1476", "THM-M-1477", "THM-M-1478"} <= boundaries


def check_task_dag(dag: dict, authoritative: list[dict]) -> None:
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["normative_profile"] == "machine-theorem-assurance/1.0"
    assert dag["theorem_id"] == THEOREM_ID
    assert dag["lifecycle_mode"] == dag["lifecycle"] == "planned"
    assert dag["accepted_states"] == []
    assert dag["audit_complete"] is False and dag["theorem_complete"] is False
    assert len(dag["tasks"]) == 6
    dependency = ITEM_ID
    for layer, (task, suffix) in enumerate(zip(dag["tasks"], TASK_SUFFIXES), start=1):
        task_id = f"S56-M-1475-{suffix}"
        source = next(row for row in authoritative if row["id"] == task_id)
        assert task["id"] == task_id and task["depends_on"] == [dependency]
        assert task["state"] == "open" and task["layer"] == source["layer"] == layer
        assert task["phase"] == source["phase"]
        assert task["owned_paths"] == source["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == source["deliverable"]
        assert task["completion_gate"] == source["completion_gate"]
        assert task["evidence_ids"] == []
        dependency = task_id


def check_receipt(receipt: dict, dag: dict) -> None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["content_addressed"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    for key in (
        "accepted_receipt_ids",
        "proof_body_locations",
        "canonical_obligation_ids",
        "statement_fingerprints",
        "typed_graph_changes",
        "composition_certificates",
        "content_addressed_recipe_ids",
        "content_addressed_receipt_ids",
    ):
        assert receipt[key] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["root_vector_after"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["selftest_result"] == "pass"
    assert receipt["source_inputs"] == {path: f"sha256:{digest}" for path, digest in SOURCE_HASHES.items()}
    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    assert all(recipe["network_policy"] == "denied" for recipe in recipes)
    assert all(recipe["expected_exit"] == 0 for recipe in recipes)
    assert all(recipe["covered_obligation_ids"] == [ITEM_ID] for recipe in recipes)


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load_json(path.resolve())
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
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]


def check_files(instance: dict, receipt: dict) -> None:
    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual == OWNED_FILES, f"unexpected owned artifact inventory: {sorted(actual)}"
    expected_changed = [".stage1-worker-selftest.json"] + [
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in sorted(OWNED_FILES)
    ]
    assert receipt["changed_paths"] == expected_changed
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    hashes = receipt["non_self_referential_owned_artifact_sha256"]
    expected_hashed = set(expected_changed) - {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json",
    }
    assert set(hashes) == expected_hashed
    for relative, expected in hashes.items():
        assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for name in (
        "README.md",
        "instance.json",
        "scope-map.md",
        "source-statement-crosswalk.md",
        "task-dag.json",
        "validation.md",
        "intake-receipt.json",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(r"\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b", probe)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()
    instance = load_json(HERE / "instance.json")
    dag = load_json(HERE / "task-dag.json")
    receipt = load_json(HERE / "intake-receipt.json")
    authoritative = check_authorities(instance)
    check_instance(instance)
    check_lake_symlink(receipt)
    check_catalog_and_boundaries(instance)
    check_task_dag(dag, authoritative)
    check_receipt(receipt, dag)
    check_files(instance, receipt)
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)
    print("intake invariant check: ok (THM-M-1475 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
