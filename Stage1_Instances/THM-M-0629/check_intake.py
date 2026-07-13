#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0629 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0629"
ITEM_ID = "S56-M-0629-INTAKE"
RANK = 1322
BASE_REVISION = "d1b510bacab792f84a99231485cf4429fdb78978"
BASE_TREE = "f77c4e4db196fc0ecc271815514a411d06ea6053"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROBE_OUTPUT_SHA256 = "078ac09e10ddbbb1299c74f8037a72b898ad42dd99723e492b19ed6d50632384"
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
    "mathlib_one_point_basic_sha256": (
        "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Topology/Compactification/OnePoint/Basic.lean"
    ),
}
TESTED_INPUT_PATHS = {
    "worker_packet": ".stage1-worker-selftest.json",
    "readme": "Stage1_Instances/THM-M-0629/README.md",
    "instance": "Stage1_Instances/THM-M-0629/instance.json",
    "scope_map": "Stage1_Instances/THM-M-0629/scope-map.md",
    "source_statement_crosswalk": (
        "Stage1_Instances/THM-M-0629/source-statement-crosswalk.md"
    ),
    "task_dag": "Stage1_Instances/THM-M-0629/task-dag.json",
    "intake_probe": "Stage1_Instances/THM-M-0629/IntakeProbe.lean",
    "intake_validator": "Stage1_Instances/THM-M-0629/check_intake.py",
    "validation_record": "Stage1_Instances/THM-M-0629/validation.md",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def line_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[first - 1 : last])).hexdigest()


def compact_json_sha256(value: object) -> str:
    data = (json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    return hashlib.sha256(data).hexdigest()


def check_text_hygiene(path: Path) -> None:
    content = path.read_bytes()
    assert content.endswith(b"\n"), f"missing final newline: {path}"
    assert not content.endswith(b"\n\n"), f"extra blank line at EOF: {path}"
    assert b"\r" not in content and b"\0" not in content
    for number, line in enumerate(content.splitlines(), start=1):
        assert line.rstrip() == line, f"trailing whitespace: {path}:{number}"


def check_worker_packet(path: Path, receipt: dict) -> None:
    check_text_hygiene(path.resolve())
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
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["output_summary"] == receipt["output_summary"]
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

    targets = [r for r in manifest["targets"] if r["theorem_id"] == THEOREM_ID]
    items = [r for r in execution["items"] if r["id"] == ITEM_ID]
    assert len(targets) == len(items) == 1
    target, item = targets[0], items[0]
    assert compact_json_sha256(target) == instance["source_revisions"]["manifest_entry_sha256"]
    assert compact_json_sha256(item) == instance["source_revisions"]["execution_dag_intake_entry_sha256"]

    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "一点紧化定理"
    assert target["category"] == instance["category"] == "拓扑学 / 点集拓扑"
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
    assert instance["literal_source_claim_zh"] == "局部紧Hausdorff空间的一点紧化"
    assert instance["canonical_statement"] is instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is dag["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    revisions = instance["source_revisions"]
    assert revisions["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert revisions["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
    if args.worker_packet is not None:
        assert git("rev-parse", "HEAD") == BASE_REVISION
    else:
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", BASE_REVISION, "HEAD"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    assert git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md') == revisions["repository_source_record_blob"]
    for field, relative in SOURCE_HASHES.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    assert revisions["repository_record_excerpt_sha256"] == line_sha256(
        ROOT / "Docs/researches/math_theorems.md", 4664, 4669
    )
    assert revisions["stage0_projection_excerpt_sha256"] == line_sha256(
        ROOT / "Docs/Stage0_Blueprint.md", 17206, 17231
    )
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**一点紧化定理**" in catalog
    assert "- 提出者: Pavel Alexandrov" in catalog
    assert "- 时间: 1924" in catalog
    assert "- 陈述: 局部紧Hausdorff空间的一点紧化" in catalog
    stage0 = (ROOT / "Docs/Stage0_Blueprint.md").read_text(encoding="utf-8")
    assert "THM-M-0629 一点紧化定理" in stage0
    assert "- 精确定义与前提条件: 待补充" in stage0

    expected_tasks = []
    dependency = ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0629-{suffix}"
        authoritative = next(r for r in execution["items"] if r["id"] == task_id)
        task = next(r for r in dag["tasks"] if r["id"] == task_id)
        expected_tasks.append((task_id, [dependency]))
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["state"] == "open" and task["evidence_ids"] == []
        dependency = task_id
    assert [(t["id"], t["depends_on"]) for t in dag["tasks"]] == expected_tasks
    assert {r["theorem_id"] for r in instance["neighbor_target_boundaries"]} == {"THM-M-0628", "THM-M-0630"}

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    for name in OWNED_FILES:
        check_text_hygiene(HERE / name)
    expected_changes = {
        ".stage1-worker-selftest.json",
        *(f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES),
    }
    assert set(receipt["changed_paths"]) == expected_changes
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False and receipt["verdict"] == "no_state_change"
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["proof_body_locations"] == receipt["accepted_receipt_ids"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]
    assert receipt["worker_input_hashes"]["lean_probe_output_sha256"] == PROBE_OUTPUT_SHA256
    tested_inputs = receipt["tested_input_sha256"]
    assert set(tested_inputs) == set(TESTED_INPUT_PATHS)
    for name, relative in TESTED_INPUT_PATHS.items():
        if name == "worker_packet" and args.worker_packet is None:
            continue
        path = args.worker_packet.resolve() if name == "worker_packet" else ROOT / relative
        assert tested_inputs[name] == sha256(path), f"stale tested input: {name}"
    assert receipt["selftest_result"] == "pass"

    for name in ("README.md", "instance.json", "scope-map.md", "source-statement-crosswalk.md", "task-dag.json", "validation.md", "intake-receipt.json"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    lean_probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in lean_probe for token in prohibited)

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)

    print("intake invariant check: ok (THM-M-0629 planned; H1/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
