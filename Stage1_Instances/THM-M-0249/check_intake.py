#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0249 planned intake."""

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
THEOREM_ID = "THM-M-0249"
ITEM_ID = "S56-M-0249-INTAKE"
RANK = 1259
BASE_REVISION = "c6fd6dad8fcfe5fd464416cd452f50286b546978"
BASE_TREE = "5a80b61d8fa09336779f8d1453dcfe4299c9472f"
SOURCE_RECORD_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_RECORD_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
SOURCE_RECORD_BLOCK_SHA256 = "a8d668ef213f9a0973388c042b122b39e7208b47bf86cc1b07380cd98c89b105"
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
    "Mathlib/Analysis/Analytic/Basic.lean": "2ff8b93f0a0d8978f813534dfc2a8ba94cc4dc59b3b12180921cebfccc712f30",
    "Mathlib/Topology/ContinuousMap/Polynomial.lean": "c2f4234626602eb7100968f2b534a01a125679f6604ce69fdbdbd05ba344af17",
    "Mathlib/Topology/ContinuousMap/StoneWeierstrass.lean": "a38987686de10fd538e8b029e2341b4177bd836e236f43bcf4c0c7ff0f2e6088",
    "Mathlib/Topology/ContinuousMap/Weierstrass.lean": "671efc224525ad0e72e357f84fda45e9b703dde1be473898d5fc3e99bde74bda",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path)
    for field in (
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    ):
        assert field in packet, f"worker packet lacks required field: {field}"
    assert packet["item_id"] == ITEM_ID
    assert packet["theorem_id"] == THEOREM_ID
    assert packet["intent"] == "intake" and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert all(
        isinstance(command, dict)
        and isinstance(command.get("argv"), list)
        and command["argv"]
        and isinstance(command.get("exit_code"), int)
        for command in packet["commands"]
    )
    assert isinstance(packet["output_summary"], str) and packet["output_summary"].strip()
    assert isinstance(packet["known_failures"], list) and packet["known_failures"]
    assert packet["accepted_receipt_ids"] == []
    assert packet["root_vector_after"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert packet["receipt_path"] == f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json"
    assert packet["owner"] == "Stage1 integration lane"
    assert packet["support_state"] == "provisional_worker_only"
    assert packet["revocation_state"] == "not_revoked_but_unaccepted"
    assert packet["audit_complete"] is False
    assert packet["theorem_complete"] is False


def check_source_hashes(instance: dict, receipt: dict) -> None:
    revisions = instance["source_revisions"]
    for relative, expected in SOURCE_HASHES.items():
        actual = sha256(ROOT / relative)
        assert actual == expected, f"unexpected pinned input hash: {relative}"
        assert receipt["source_inputs"][relative] == f"sha256:{actual}"

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
    for field, relative in field_map.items():
        assert revisions[field] == SOURCE_HASHES[relative], f"stale instance hash: {field}"

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    for relative, expected in MATHLIB_SOURCE_HASHES.items():
        assert sha256(mathlib / relative) == expected, f"stale mathlib source: {relative}"


def check_receipt(receipt: dict, instance: dict, dag: dict) -> None:
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == receipt["intent"] == "intake"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["selftest_result"] == "pass"
    assert receipt["covered_task_ids"] == [ITEM_ID]
    assert receipt["covered_declaration_ids"] == []
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["worker_input_hashes"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["worker_input_hashes"]["mathlib_tree"] == MATHLIB_TREE
    assert receipt["worker_input_hashes"]["lake_symlink_target_string"] == (
        f"sha256:{LAKE_SYMLINK_TARGET_SHA256}"
    )

    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert set(receipt["artifact_sha256"]) == OWNED_FILES - {"intake-receipt.json"}
    for name, expected in receipt["artifact_sha256"].items():
        assert sha256(HERE / name) == expected, f"owned artifact hash mismatch: {name}"

    recipes = receipt["structured_validation_recipes"]
    assert isinstance(recipes, list) and len(recipes) == 2
    required_recipe_fields = {
        "recipe_id",
        "cwd",
        "argv",
        "env_allowlist",
        "timeout_seconds",
        "network_policy",
        "expected_exit",
        "expected_outputs",
        "covered_task_ids",
        "covered_obligation_ids",
        "covered_declarations",
        "observed_exit",
        "input_hashes",
        "stdout_sha256",
        "stderr_sha256",
        "started_at",
        "ended_at",
    }
    for recipe in recipes:
        assert required_recipe_fields <= recipe.keys()
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["observed_exit"] == 0
        assert recipe["covered_task_ids"] == [ITEM_ID]
        assert recipe["covered_obligation_ids"] == []
        assert recipe["covered_declarations"] == []
        assert isinstance(recipe["input_hashes"], dict) and recipe["input_hashes"]
        assert re.fullmatch(r"sha256:[0-9a-f]{64}", recipe["stdout_sha256"])
        assert re.fullmatch(r"sha256:[0-9a-f]{64}", recipe["stderr_sha256"])
    structure, lean_probe = recipes
    assert structure["recipe_id"] == f"{ITEM_ID}-RECIPE-STRUCTURE"
    assert structure["cwd"] == "."
    assert structure["argv"] == [
        "python3",
        f"Stage1_Instances/{THEOREM_ID}/check_intake.py",
        "--worker-packet",
        ".stage1-worker-selftest.json",
    ]
    assert structure["stdout_sha256"] == (
        "sha256:5c8ecadc34b80652477285a1e88fe743db4a36daea099efea11b95c9337446be"
    )
    assert lean_probe["recipe_id"] == f"{ITEM_ID}-RECIPE-LEAN-PROBE"
    assert lean_probe["cwd"] == "Formalizations/Lean"
    assert lean_probe["argv"] == [
        "lake",
        "env",
        "lean",
        f"../../Stage1_Instances/{THEOREM_ID}/IntakeProbe.lean",
    ]
    assert lean_probe["stdout_sha256"] == (
        "sha256:297e6dd65a55cb54bfc752cb25b0834af367be9130b08f851010b3d5acb3b7e4"
    )
    assert isinstance(receipt["commands_and_results"], list) and receipt["commands_and_results"]
    assert instance["accepted_receipt_ids"] == []


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
    assert target["name"] == instance["name_zh"] == "梅尔格良定理"
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

    item = next(row for row in execution_dag["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."

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
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    assert len(instance["source_leads"]) == 2
    assert all(lead["credit"] == "H1_lead_only" for lead in instance["source_leads"])
    assert next(lead for lead in instance["source_leads"] if lead["source_id"].startswith("ARXIV"))["sha256"] == (
        "19270fa85fa42a7042b41e946ec8171cfc7f4c2a73c5db61550b691298f2bdc1"
    )

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", f"{SOURCE_RECORD_COMMIT}:Docs/researches/math_theorems.md") == (
        revisions["repository_source_record_blob"]
    ) == SOURCE_RECORD_BLOB
    source_lines = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8").splitlines(True)
    block_hash = hashlib.sha256("".join(source_lines[1793:1799]).encode()).hexdigest()
    assert block_hash == revisions["repository_record_block_sha256"] == SOURCE_RECORD_BLOCK_SHA256
    assert revisions["mathlib"] == MATHLIB_REVISION and revisions["mathlib_tree"] == MATHLIB_TREE
    check_source_hashes(instance, receipt)

    expected_tasks = []
    dependency = ITEM_ID
    for suffix in TASK_SUFFIXES:
        task_id = f"S56-M-0249-{suffix}"
        expected_tasks.append((task_id, [dependency]))
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])
    assert all(task["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"] for task in dag["tasks"])

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**梅尔格良定理**" in catalog
    assert "- 提出者: Sergei Mergelyan" in catalog
    assert "- 时间: 1951" in catalog
    assert "- 陈述: 紧集上连续函数的多项式逼近" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0249 梅尔格良定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    neighbor_ids = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert neighbor_ids == {"THM-M-0248", "THM-M-0265"}
    manifest_names = {
        row["theorem_id"]: row["name"]
        for row in manifest["targets"]
        if row["theorem_id"] in neighbor_ids
    }
    assert manifest_names == {"THM-M-0248": "毕晓普定理", "THM-M-0265": "魏尔斯特拉斯逼近定理"}

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"

    check_receipt(receipt, instance, dag)
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path.name}"
        assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {path.name}"
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
    lean = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    assert not re.search(r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b", lean)

    lake_link = ROOT / "Formalizations/Lean/.lake"
    assert lake_link.is_symlink()
    assert hashlib.sha256(os.readlink(lake_link).encode()).hexdigest() == LAKE_SYMLINK_TARGET_SHA256
    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet.resolve(), receipt)

    print("intake invariant check: ok (THM-M-0249 planned; H1/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
