#!/usr/bin/env python3
"""Validate the fail-closed planned intake for THM-M-0869."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0869"
ITEM_ID = "S56-M-0869-INTAKE"
RANK = 1423
BASE_REVISION = "748243faadc15828fb087059337fd05b7be9fdeb"
BASE_TREE = "e46d642646f80980838b6f016f5d69b817bd464d"
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
    "statement-blocker.md",
    "statement-blocker.json",
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
    "applicable_targets_sha256": "Docs/Stage1_Blueprint_Applicable_Theorems.md",
    "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
    "execution_dag_sha256": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
    "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
    "repository_math_source_sha256": "Docs/researches/math_theorems.md",
    "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
    "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
    "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
    "mathlib_simplegraph_copy_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph/Copy.lean"
    ),
    "mathlib_simplegraph_subgraph_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph/Subgraph.lean"
    ),
    "mathlib_simplegraph_basic_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph/Basic.lean"
    ),
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_row_sha256(row: dict) -> str:
    data = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256((data + "\n").encode()).hexdigest()


def check_receipt_inputs(receipt: dict) -> None:
    for relative, tagged_digest in receipt["source_inputs"].items():
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}", (
            f"stale receipt input hash: {relative}"
        )

    artifact_inputs = receipt["nonrelease_artifact_inputs"]
    assert artifact_inputs["hash_algorithm"] == "sha256"
    assert artifact_inputs["receipt_hash_boundary"].startswith(
        "intake-receipt.json is self-referential"
    )
    expected_artifacts = OWNED_FILES - {"intake-receipt.json"}
    assert set(artifact_inputs["artifact_sha256"]) == expected_artifacts
    for name, digest in artifact_inputs["artifact_sha256"].items():
        assert digest == sha256(HERE / name), f"stale nonrelease artifact hash: {name}"


def check_worker_packet(path: Path, receipt: dict) -> None:
    packet = load(path)
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
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

    manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution_dag = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    blocker = load(HERE / "statement-blocker.json")
    receipt = load(HERE / "intake-receipt.json")
    check_receipt_inputs(receipt)

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "禁用子图问题"
    assert target["category"] == instance["category"] == "组合数学 / 图论"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"] == "hard_statement_first_partial_verification"
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is False

    item = next(row for row in execution_dag["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert blocker["schema_version"] == "stage1-statement-blocker/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert instance["normative_profile"] == dag["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == blocker["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert receipt["receipt_id"] == "S56-M-0869-INTAKE-WORKER-20260713"
    assert receipt["phase"] == instance["intent"] == receipt["intent"] == "intake"
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    assert "do_not_identify_one_stable" in instance["canonical_claim_status"]

    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is dag["theorem_complete"] is receipt["theorem_complete"] is False

    assert blocker["blocked_item_id"] == "S56-M-0869-STATEMENT"
    assert blocker["state"] == "open"
    assert blocker["canonical_statement"] is blocker["canonical_formal_target"] is None
    assert len(blocker["required_decisions"]) >= 7

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == revisions["repository_base"] == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == revisions["repository_base_tree"] == BASE_TREE
    assert git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md') == revisions["repository_source_record_blob"]
    assert git("hash-object", "Docs/researches/math_theorems.md") == revisions["current_repository_math_source_blob"]
    for field, relative in SOURCE_HASHES.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    assert revisions["mathlib"] == MATHLIB_REVISION
    assert revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("-C", "Formalizations/Lean/.lake/packages/mathlib", "rev-parse", "HEAD") == MATHLIB_REVISION
    assert git("-C", "Formalizations/Lean/.lake/packages/mathlib", "rev-parse", "HEAD^{tree}") == MATHLIB_TREE

    source_lines = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8").splitlines(keepends=True)
    assert hashlib.sha256("".join(source_lines[6368:6374]).encode()).hexdigest() == revisions["repository_record_excerpt_sha256"]
    stage0_lines = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8").splitlines(keepends=True)
    assert hashlib.sha256("".join(stage0_lines[23710:23736]).encode()).hexdigest() == revisions["stage0_projection_excerpt_sha256"]
    assert canonical_row_sha256(target) == revisions["target_manifest_entry_sha256"]
    assert canonical_row_sha256(item) == revisions["execution_dag_intake_entry_sha256"]

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0869-{suffix}"
        authoritative = next(row for row in execution_dag["items"] if row["id"] == task_id)
        expected_tasks.append((task_id, [dependency]))
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("**禁用子图问题**") == 1
    assert "- 陈述: 禁用子图类的刻画" in catalog
    assert "- 形式化状态: 已验证" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0869 禁用子图问题" in stage0
    assert "- 命题类型: 问题 / 判定命题" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    neighbor_ids = {row["theorem_id"] for row in instance["neighbor_target_boundaries"]}
    assert neighbor_ids == {"THM-M-0840", "THM-M-0865", "THM-M-0866", "THM-M-0867", "THM-M-0868"}
    manifest_names = {
        row["theorem_id"]: row["name"]
        for row in manifest["targets"]
        if row["theorem_id"] in neighbor_ids
    }
    assert manifest_names == {
        "THM-M-0840": "强完美图定理",
        "THM-M-0865": "Kuratowski定理",
        "THM-M-0866": "Wagner定理",
        "THM-M-0867": "Robertson-Seymour图子式定理",
        "THM-M-0868": "图子式定理",
    }

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["content_addressed"] is False
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["acceptance_authority"] == "Stage1 integration lane"
    assert receipt["attestor"]["signature"] is None
    assert receipt["attestor"]["signature_status"] == "unsigned_provisional_worker_report"
    assert receipt["platform"]["operating_system"] == platform.system()
    assert receipt["platform"]["architecture"] == platform.machine()
    started_at = datetime.fromisoformat(receipt["validation_started_at"])
    ended_at = datetime.fromisoformat(receipt["validation_ended_at"])
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    assert started_at <= ended_at == validated_at <= datetime.now(timezone.utc).astimezone()
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"
    assert receipt["covered_node_ids"] == receipt["change_impact_set"] == [ITEM_ID]
    assert receipt["first_failed_gate"] == "master acceptance of the node-specific intake receipt remains pending"
    assert receipt["first_failed_theorem_gate"].startswith("S56-M-0869-STATEMENT")
    command_argv = [row["argv"] for row in receipt["commands_and_results"] if "argv" in row]
    for required in (
        ["python3", "Docs/tools/check_stage1_standard.py"],
        ["python3", "scripts/stage1_target.py", "check"],
        ["python3", "scripts/stage1_target.py", "show", THEOREM_ID],
        ["python3", "-B", f"Stage1_Instances/{THEOREM_ID}/check_intake.py", "--worker-packet", ".stage1-worker-selftest.json"],
    ):
        assert required in command_argv

    worker_inputs = receipt["worker_input_hashes"]
    assert worker_inputs["lean_toolchain"] == f"sha256:{revisions['lean_toolchain_file_sha256']}"
    assert worker_inputs["lake_manifest"] == f"sha256:{revisions['lake_manifest_sha256']}"
    assert worker_inputs["mathlib_revision"] == revisions["mathlib"]
    assert worker_inputs["mathlib_tree"] == revisions["mathlib_tree"]
    assert worker_inputs["intake_probe_sha256"] == sha256(HERE / "IntakeProbe.lean")
    lake_target = (ROOT / "Formalizations/Lean/.lake").readlink().as_posix().encode()
    assert worker_inputs["lake_symlink_target_string"] == f"sha256:{hashlib.sha256(lake_target).hexdigest()}"
    for recipe in receipt["structured_validation_recipes"]:
        assert isinstance(recipe["argv"], list) and recipe["argv"]
        assert isinstance(recipe["env_allowlist"], dict)
        assert recipe["network_policy"] == "denied"
        assert recipe["expected_exit"] == recipe["exit_code"] == 0
        assert recipe["covered_ids"] == [ITEM_ID]

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

    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md", "statement-blocker.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet.resolve(), receipt)

    print("intake invariant check: ok (THM-M-0869 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
