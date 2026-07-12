#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0640."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0640"
ITEM_ID = "S56-M-0640-INTAKE"
RANK = 1057
BASE_REVISION = "c2467750f2cdb3960045c83e819d96687253303d"
BASE_TREE = "0f79eb697267dc28b29d41a1e282f319d758a2ac"
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
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path)
    assert packet["schema_version"] == "stage1-worker-selftest/1.0"
    assert packet["item_id"] == ITEM_ID
    assert packet["theorem_id"] == THEOREM_ID
    assert packet["intent"] == "intake"
    assert packet["verdict"] == receipt["verdict"] == "no_state_change"
    assert packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["receipt_id"] == receipt["receipt_id"]
    assert packet["accepted_receipt_ids"] == []
    assert packet["covered_node_ids"] == receipt["covered_node_ids"] == [ITEM_ID]
    assert packet["covered_declaration_ids"] == receipt["covered_declaration_ids"] == []
    assert packet["audit_complete"] is receipt["audit_complete"] is False
    assert packet["theorem_complete"] is receipt["theorem_complete"] is False
    assert packet["known_failures"]
    assert packet["commands"]
    assert all(command["exit_code"] == 0 or command.get("expected") == "no matches" for command in packet["commands"])
    assert packet["output_summary"]


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
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "布劳威尔不动点定理"
    assert target["category"] == "拓扑学 / 点集拓扑"
    assert instance["category_manifest"] == target["category"]
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 92
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
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

    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["unresolved_boundary_and_mutation_cases"]
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert dag["audit_complete"] is False
    assert receipt["theorem_complete"] is False
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["content_addressed"] is receipt["accepted"] is False
    assert receipt["proposed_state"] == "[_]"
    assert receipt["verdict"] == "no_state_change"

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0640-{suffix}"
        expected_tasks.append((task_id, suffix.lower(), layer, [dependency]))
        dependency = task_id
    assert [
        (task["id"], task["phase"], task["layer"], task["depends_on"])
        for task in dag["tasks"]
    ] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**布劳威尔不动点定理**" in catalog
    assert "- 提出者: Luitzen Brouwer" in catalog
    assert "- 时间: 1910" in catalog
    assert "- 陈述: n维球到自身的连续映射有不动点" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0640 布劳威尔不动点定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]

    recorded_hashes = receipt["owned_artifact_hashes_before_receipt_and_validation"]
    assert set(recorded_hashes) == OWNED_FILES - {"intake-receipt.json", "validation.md"}
    for name, recorded in recorded_hashes.items():
        actual = sha256(HERE / name)
        assert recorded == f"sha256:{actual}", f"stale owned artifact hash: {name}"

    source_paths = {
        "Docs/Stage1_Targets_rev-5.6.json": ROOT / "Docs/Stage1_Targets_rev-5.6.json",
        "Docs/Stage1_Blueprint_rev-5.6.md": ROOT / "Docs/Stage1_Blueprint_rev-5.6.md",
        "Docs/Stage1_Execution_DAG_rev-5.6.json": ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "skills/execute-stage1-rev56/SKILL.md": ROOT / "skills/execute-stage1-rev56/SKILL.md",
        "Docs/Blueprint_Guidelines.md": ROOT / "Docs/Blueprint_Guidelines.md",
        "Docs/researches/math_theorems.md": ROOT / "Docs/researches/math_theorems.md",
        "Docs/Stage0_Blueprint.md": ROOT / "Docs/Stage0_Blueprint.md",
    }
    assert set(receipt["source_inputs"]) == set(source_paths)
    for name, path in source_paths.items():
        assert receipt["source_inputs"][name] == f"sha256:{sha256(path)}"

    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    tree = subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True).strip()
    assert head == receipt["base_revision"] == BASE_REVISION
    assert tree == receipt["base_tree"] == BASE_TREE

    worker_hashes = receipt["worker_input_hashes"]
    assert worker_hashes["lean_toolchain"] == f"sha256:{sha256(ROOT / 'Formalizations/Lean/lean-toolchain')}"
    assert worker_hashes["lake_manifest"] == f"sha256:{sha256(ROOT / 'Formalizations/Lean/lake-manifest.json')}"
    lake_target = os.readlink(ROOT / "Formalizations/Lean/.lake")
    lake_target_hash = hashlib.sha256((lake_target + "\n").encode()).hexdigest()
    assert worker_hashes["lake_symlink_target_string"] == f"sha256:{lake_target_hash}"
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    mathlib_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=mathlib, text=True).strip()
    mathlib_tree = subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib, text=True).strip()
    assert worker_hashes["mathlib_revision"] == mathlib_head
    assert worker_hashes["mathlib_tree"] == mathlib_tree

    recipes = receipt["structured_validation_recipes"]
    assert len(recipes) == 2
    required_recipe_keys = {
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy",
        "expected_exit", "expected_outputs", "covered_obligation_ids", "covered_declarations",
        "covered_task_ids",
    }
    assert all(set(recipe) == required_recipe_keys for recipe in recipes)
    assert all(recipe["covered_task_ids"] == [ITEM_ID] for recipe in recipes)
    assert all(recipe["expected_outputs"] for recipe in recipes)

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

    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    lean_probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in lean_probe for token in prohibited)

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet.resolve(), receipt)

    print("intake invariant check: ok (THM-M-0640 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
