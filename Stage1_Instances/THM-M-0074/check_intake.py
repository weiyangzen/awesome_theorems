#!/usr/bin/env python3
"""Validate the provisional THM-M-0074 intake packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0074"
ITEM_ID = "S56-M-0074-INTAKE"
BASE_REVISION = "d3cbfa8941a8bcaafa3b8a690d1333f9643288ad"
BASE_TREE = "e912a107150c6f9c3fc096901412fce0337c7c01"
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
AUTHORITY_HASHES = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "3cad993d1e9cb7edc363033226cbaddcee9ab4461f63bcaaf1b0bd42686cc942",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "a48ed229f0887bb1d57297734930f7bc50c10932690f054a6bd90e4b978151db",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
PHASES = ["statement", "anchor_audit", "obligation_tree", "proof", "validation", "release"]


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")
    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    authority = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    for relative, expected in AUTHORITY_HASHES.items():
        assert sha256(ROOT / relative) == expected, f"stale authority: {relative}"

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target == {
        "execution_rank": 1024,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM_ID,
        "name": "格里思定理",
        "category": "代数学 / 群论",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 96,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }

    assigned = next(row for row in authority["items"] if row["id"] == ITEM_ID)
    assert assigned["theorem_id"] == THEOREM_ID
    assert assigned["phase"] == "intake" and assigned["layer"] == 0
    assert assigned["depends_on"] == [] and assigned["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert assigned["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == THEOREM_ID and instance["item_id"] == ITEM_ID
    assert instance["lifecycle"] == instance["lifecycle_mode"] == "planned"
    assert instance["intent"] == "intake" and instance["baseline"] == "L0"
    assert instance["rework_required"] is True and instance["legacy_artifacts_accepted"] is False
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    assert formal["module"] is None and formal["declaration_or_expression"] is None
    assert formal["elaborated_expression_hash"] is None and formal["environment_fingerprint"] is None
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == [] and instance["accepted_receipt_ids"] == []
    assert instance["obligation_registry_hash"] is None and instance["discovery_protocol_hash"] is None
    assert any("10.1073/pnas.78.2.689" in row["citation"] for row in instance["primary_source_candidates_not_credited"])
    assert any("10.1007/BF01389186" in row["citation"] for row in instance["primary_source_candidates_not_credited"])

    assert dag["schema_version"] == "stage1-open-task-dag/1.0"
    assert dag["theorem_id"] == THEOREM_ID and dag["lifecycle"] == dag["lifecycle_mode"] == "planned"
    assert dag["accepted_states"] == [] and dag["audit_complete"] is False and dag["theorem_complete"] is False
    assert len(dag["tasks"]) == 6
    dependency = ITEM_ID
    for layer, (phase, task) in enumerate(zip(PHASES, dag["tasks"], strict=True), start=1):
        task_id = f"S56-M-0074-{phase.upper()}"
        authoritative_task = next(row for row in authority["items"] if row["id"] == task_id)
        assert task["id"] == task_id and task["phase"] == phase and task["layer"] == layer
        assert task["depends_on"] == [dependency] and task["state"] == "open"
        assert task["evidence_ids"] == []
        for field in ("phase", "layer", "owned_paths", "deliverable", "completion_gate"):
            assert task[field] == authoritative_task[field]
        dependency = task_id

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert actual_files == OWNED_FILES == set(instance["owned_artifacts"])
    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()

    lean = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    prohibited = re.compile(r"\b(?:sorry|admit|sorryAx)\b|^\s*(?:axiom|constant|opaque|unsafe)\b", re.MULTILINE)
    assert prohibited.search(lean) is None
    assert "monsterExistenceEnvelope" in lean and "Candidate statement envelope only" in lean

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["phase"] == "intake" and receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False and receipt["acceptance_authority"] == "integration lane"
    assert receipt["root_vector_after"] == instance["root_vector"]
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == [] and receipt["canonical_obligation_ids"] == []
    assert receipt["platform"]["operating_system"] == platform.system()
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in OWNED_FILES
    }
    assert set(receipt["changed_paths"]) == expected_changed

    if args.worker_packet is not None:
        packet = load(args.worker_packet)
        assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == expected_changed
        assert packet["known_failures"] == receipt["known_failures"]

    print("check_intake: ok (THM-M-0074 planned H1/M4/R4 intake; six downstream tasks open)")


if __name__ == "__main__":
    main()
