#!/usr/bin/env python3
"""Validate the expanded THM-M-0741 planned dossier."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0741"
INTAKE_ITEM_ID = "S56-M-0741-INTAKE"
HANDOFF_ITEM_ID = "S56-M-0741-STATEMENT"
RANK = 1329
BASE_REVISION = "d05520867fab3367a9b61b9544c3e12241204f54"
BASE_TREE = "fb2cfc62077d5b53e9938632cd6361dd60872067"
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
    "Statement.lean",
    "check_statement.py",
    "statement.json",
    "statement-validation.md",
    "statement-receipt.json",
}
TASK_SUFFIXES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)
SOURCE_HASH_FIELDS = {
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
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


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
    assert packet["item_id"] == HANDOFF_ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    intake_receipt = load(HERE / "intake-receipt.json")
    statement = load(HERE / "statement.json")
    receipt = load(HERE / "statement-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "停机问题"
    assert target["category"] == "数理逻辑 / 递归论"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    intake_item = next(row for row in execution["items"] if row["id"] == INTAKE_ITEM_ID)
    assert intake_item["theorem_id"] == THEOREM_ID and intake_item["execution_rank"] == RANK
    assert intake_item["phase"] == "intake" and intake_item["layer"] == 0
    assert intake_item["state"] == "[_]" and intake_item["depends_on"] == []
    assert intake_item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == intake_receipt["item_id"] == INTAKE_ITEM_ID
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["intent"] == "intake" and receipt["intent"] == "statement"
    assert instance["canonical_statement"] == statement["canonical_statement"]
    assert instance["canonical_claim"] == statement["canonical_statement"]
    assert instance["statement_blocker"] is None
    formal = instance["canonical_formal_target"]
    statement_formal = statement["canonical_formal_target"]
    assert formal["module"] == f"Stage1_Instances/{THEOREM_ID}/Statement.lean"
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0741.HaltingProblemUndecidable"
    )
    assert formal["elaborated_expression_hash"] == (
        "sha256:" + statement_formal["elaborated_expression_sha256"]
    )
    assert formal["environment_fingerprint"]
    assert instance["quantifiers"] and instance["ordered_binders"]
    assert instance["hypotheses"] == []
    assert instance["alternate_encodings"] == [
        {
            "target": "Stage1Instances.THM_M_0741.ExpandedHaltingProblemUndecidable",
            "relationship": "iff",
            "checked_witness": "Stage1Instances.THM_M_0741.haltingProblemUndecidable_iff_expanded",
        }
    ]
    assert instance["obligation_registry_hash"] is None
    assert instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False
    assert instance["foundation_profile"].startswith("lean4-foundation-planned/1.0:")
    assert instance["tcb_profile"].startswith("lean4-mathlib-tcb-planned/1.0:")
    assert instance["computation_profile"].startswith("kernel-computability-proposition-planned/1.0:")

    revisions = instance["source_revisions"]
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert (
        git("rev-parse", f'{revisions["repository_source_record_commit"]}:Docs/researches/math_theorems.md')
        == revisions["repository_source_record_blob"]
    )
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert revisions[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == revisions["mathlib"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == revisions["mathlib_tree"] == MATHLIB_TREE
    assert revisions["mathlib_halting_source_sha256"] == sha256(
        mathlib / "Mathlib/Computability/Halting.lean"
    )

    expected_tasks = []
    dependency = INTAKE_ITEM_ID
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0741-{suffix}"
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        expected_tasks.append((task_id, [dependency]))
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["statement_fingerprints"] == [formal["elaborated_expression_hash"]]
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]][1:]
    assert receipt["root_vector_before"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["known_failures"] and receipt["selftest_result"] == "pass"
    assert receipt["covered_node_ids"] == [HANDOFF_ITEM_ID]
    assert receipt["change_impact_set"] == [HANDOFF_ITEM_ID]
    assert set(receipt["changed_paths"]) == {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM_ID}/README.md",
        f"Stage1_Instances/{THEOREM_ID}/Statement.lean",
        f"Stage1_Instances/{THEOREM_ID}/check_intake.py",
        f"Stage1_Instances/{THEOREM_ID}/check_statement.py",
        f"Stage1_Instances/{THEOREM_ID}/instance.json",
        f"Stage1_Instances/{THEOREM_ID}/intake-receipt.json",
        f"Stage1_Instances/{THEOREM_ID}/scope-map.md",
        f"Stage1_Instances/{THEOREM_ID}/source-statement-crosswalk.md",
        f"Stage1_Instances/{THEOREM_ID}/statement-receipt.json",
        f"Stage1_Instances/{THEOREM_ID}/statement-validation.md",
        f"Stage1_Instances/{THEOREM_ID}/statement.json",
        f"Stage1_Instances/{THEOREM_ID}/task-dag.json",
        f"Stage1_Instances/{THEOREM_ID}/validation.md",
    }
    for relative, tagged_digest in receipt["source_inputs"].items():
        assert tagged_digest == f"sha256:{sha256(ROOT / relative)}", f"stale receipt input: {relative}"
    assert intake_receipt["supersession_state"].startswith(
        "superseded_for_current_dossier_replay_by_S56-M-0741-STATEMENT"
    )
    assert intake_receipt["support_state"].startswith("historical_provisional_intake_input")

    for path in HERE.iterdir():
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
        "statement-validation.md",
        "statement-receipt.json",
        "statement.json",
        "task-dag.json",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text
    lean_text = "\n".join(
        path.read_text(encoding="utf-8") for path in HERE.glob("*.lean")
    )
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|constant|opaque)\s+|^\s*unsafe\b",
        re.MULTILINE,
    )
    assert prohibited.search(lean_text) is None

    if args.worker_packet is not None:
        check_worker_packet(args.worker_packet, receipt)
    print("dossier invariant check: ok (THM-M-0741 planned; H1/M3/R4; statement self-tested)")


if __name__ == "__main__":
    main()
