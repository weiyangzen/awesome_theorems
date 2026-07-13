#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0745 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0745"
ITEM_ID = "S56-M-0745-INTAKE"
RANK = 1332
BASE_REVISION = "0e5ae82e6d507ee607c3f011900571ffd8096800"
BASE_TREE = "400e6edf1f69b971b60a367e3ea29be359b07907"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MANIFEST_ENTRY_SHA256 = "21ef686422f86be957ffc1eeca9c789d197838ba86e3543f8ed5c4349f67aa79"
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
    "target_manifest_sha256": "Docs/Stage1_Targets_rev-5.6.json",
    "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
    "execution_dag_sha256": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
    "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
    "repository_math_source_sha256": "Docs/researches/math_theorems.md",
    "repository_cs_source_sha256": "Docs/researches/cs_theorems.md",
    "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
    "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
    "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
    "mathlib_halting_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability/Halting.lean"
    ),
    "mathlib_reduce_source_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability/Reduce.lean"
    ),
    "mathlib_references_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/docs/references.bib"
    ),
}
TESTED_INPUT_PATHS = {
    "worker_packet": ".stage1-worker-selftest.json",
    "readme": "Stage1_Instances/THM-M-0745/README.md",
    "instance": "Stage1_Instances/THM-M-0745/instance.json",
    "scope_map": "Stage1_Instances/THM-M-0745/scope-map.md",
    "source_statement_crosswalk": (
        "Stage1_Instances/THM-M-0745/source-statement-crosswalk.md"
    ),
    "task_dag": "Stage1_Instances/THM-M-0745/task-dag.json",
    "intake_probe": "Stage1_Instances/THM-M-0745/IntakeProbe.lean",
    "intake_validator": "Stage1_Instances/THM-M-0745/check_intake.py",
    "validation_record": "Stage1_Instances/THM-M-0745/validation.md",
}


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def line_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first - 1 : last])).hexdigest()


def canonical_manifest_entry(target: dict) -> str:
    data = (json.dumps(target, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    return hashlib.sha256(data).hexdigest()


def check_text_hygiene(path: Path) -> None:
    content = path.read_bytes()
    assert content.endswith(b"\n"), f"missing final newline: {path}"
    assert not content.endswith(b"\n\n"), f"extra blank line at EOF: {path}"
    assert b"\r" not in content, f"carriage return: {path}"
    assert b"\0" not in content, f"NUL byte: {path}"
    for number, line in enumerate(content.splitlines(), start=1):
        assert line.rstrip() == line, f"trailing whitespace: {path}:{number}"


def check_worker_packet(path: Path, receipt: dict) -> None:
    path = path.resolve()
    check_text_hygiene(path)
    packet = load(path)
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
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert manifest["scope"]["covered_targets"] == 1546
    assert canonical_manifest_entry(target) == MANIFEST_ENTRY_SHA256
    assert target == {
        "execution_rank": RANK,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "递归枚举集",
        "category": "数理逻辑 / 递归论",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 86,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"]
    assert target["category"] == instance["category"]
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"]
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == []
    assert item["attempts"] == 0 and item["children"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["literal_source_claim_zh"] == "递归可枚举集的性质"
    assert instance["canonical_statement"] is instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    assert formal["module"] is formal["declaration_or_expression"] is None
    assert formal["elaborated_expression_hash"] is formal["environment_fingerprint"] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == instance["hypotheses"] == []
    assert instance["alternate_encodings"] == []
    assert instance["root_vector"] == {"H": "H5", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert "No accepted stable proposition" in instance["status_boundary"]

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    git("cat-file", "-e", f"{BASE_REVISION}^{{commit}}")
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
    assert git("merge-base", "--is-ancestor", BASE_REVISION, "HEAD") == ""
    assert (
        git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md')
        == revisions["repository_source_record_origin_blob"]
    )
    assert (
        git("rev-parse", "HEAD:Docs/researches/math_theorems.md")
        == revisions["repository_source_record_current_blob"]
    )
    for field, relative in SOURCE_HASHES.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    assert revisions["manifest_entry_sha256"] == MANIFEST_ENTRY_SHA256
    lake_link = ROOT / "Formalizations/Lean/.lake"
    assert lake_link.is_symlink(), "automation-provided .lake path must remain a symlink"
    link_target_hash = hashlib.sha256((str(lake_link.readlink()) + "\n").encode()).hexdigest()
    assert link_target_hash == revisions["lake_symlink_target_sha256"]
    assert revisions["repository_record_excerpt_sha256"] == line_sha256(
        ROOT / "Docs/researches/math_theorems.md", 5493, 5498
    )
    assert revisions["stage0_projection_excerpt_sha256"] == line_sha256(
        ROOT / "Docs/Stage0_Blueprint.md", 20353, 20378
    )
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    assert git("rev-parse", "HEAD:Mathlib/Computability/Halting.lean", cwd=mathlib) == revisions["mathlib_halting_source_blob"]
    assert git("rev-parse", "HEAD:Mathlib/Computability/Reduce.lean", cwd=mathlib) == revisions["mathlib_reduce_source_blob"]
    assert git("rev-parse", "HEAD:docs/references.bib", cwd=mathlib) == revisions["mathlib_references_blob"]
    assert sha256(ROOT / "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability/Halting.lean") == revisions["mathlib_halting_source_sha256"]
    assert sha256(ROOT / "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability/Reduce.lean") == revisions["mathlib_reduce_source_sha256"]
    assert sha256(ROOT / "Formalizations/Lean/.lake/packages/mathlib/docs/references.bib") == revisions["mathlib_references_sha256"]

    expected_tasks: list[tuple[str, list[str], str, int]] = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0745-{suffix}"
        expected_tasks.append((task_id, [dependency], suffix.lower(), layer))
        dependency = task_id
    assert [
        (task["id"], task["depends_on"], task["phase"], task["layer"])
        for task in dag["tasks"]
    ] == expected_tasks
    assert all(task["state"] == "open" and task["evidence_ids"] == [] for task in dag["tasks"])
    assert all(task["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"] for task in dag["tasks"])
    execution_by_id = {row["id"]: row for row in execution["items"]}
    for task in dag["tasks"]:
        authority = execution_by_id[task["id"]]
        for field in ("phase", "layer", "depends_on", "owned_paths", "deliverable", "completion_gate"):
            assert task[field] == authority[field], f"task projection mismatch: {task['id']} {field}"

    actual_artifacts = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual_artifacts == OWNED_FILES
    assert set(instance["owned_artifacts"]) == OWNED_FILES
    expected_changed = {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is False and receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["selftest_result"] == "pass"
    assert receipt["covered_node_ids"] == [ITEM_ID]
    assert receipt["change_impact_set"] == [ITEM_ID]
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["root_vector_before"] == {
        "H": "unclassified",
        "M": "unclassified",
        "R": "unclassified",
    }
    assert receipt["known_failures"] and receipt["first_failed_theorem_gate"]
    for record in receipt["commands_and_results"]:
        assert ("argv" in record) != ("command" in record), "command record needs exactly one invocation form"
        assert isinstance(record["exit_code"], int)
        assert isinstance(record["result"], str) and record["result"]
        if "argv" in record:
            assert isinstance(record["argv"], list) and record["argv"]
            assert all(isinstance(arg, str) and arg for arg in record["argv"])
            assert "=" not in record["argv"][0], "environment assignments belong in the env field"
    assert receipt["worker_input_hashes"]["lake_symlink_target_string"] == (
        f"sha256:{revisions['lake_symlink_target_sha256']}"
    )
    assert receipt["worker_input_hashes"]["intake_probe_sha256"] == sha256(
        HERE / "IntakeProbe.lean"
    )
    assert receipt["worker_input_hashes"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["worker_input_hashes"]["mathlib_tree"] == MATHLIB_TREE
    for field in (
        "mathlib_halting_source_sha256",
        "mathlib_reduce_source_sha256",
        "mathlib_references_sha256",
    ):
        assert receipt["worker_input_hashes"][field] == revisions[field]
    for relative, tagged_digest in receipt["source_inputs"].items():
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}", f"stale receipt input: {relative}"
    for field, relative in TESTED_INPUT_PATHS.items():
        if field == "worker_packet" and args.worker_packet is None:
            continue
        assert receipt["tested_input_sha256"][field] == sha256(ROOT / relative), f"stale tested input: {field}"

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file(), f"missing public merge target: {relative}"
    for path in HERE.iterdir():
        if path.is_file():
            check_text_hygiene(path)
    for name in ("README.md", "scope-map.md", "source-statement-crosswalk.md", "validation.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0745 planned; H5/M4/R4; six open tasks)")


if __name__ == "__main__":
    main()
