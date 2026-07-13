#!/usr/bin/env python3
"""Validate the expanded THM-M-0958 planned dossier."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0958"
INTAKE_ITEM = "S56-M-0958-INTAKE"
STATEMENT_ITEM = "S56-M-0958-STATEMENT"
RANK = 1492
BASE_REVISION = "c79ae75db8880483f10bba17c9bc9dd91a9febcf"
STATEMENT_FILES = {
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


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def check_packet(path: Path, receipt: dict) -> None:
    packet = load(path.resolve())
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == STATEMENT_ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["commands"] and packet["output_summary"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    intake = load(HERE / "intake-receipt.json")
    statement = load(HERE / "statement.json")
    receipt = load(HERE / "statement-receipt.json")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == statement["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "Elkin构造"
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["theorem_complete"] is instance["theorem_complete"] is False

    intake_item = next(row for row in execution["items"] if row["id"] == INTAKE_ITEM)
    statement_item = next(row for row in execution["items"] if row["id"] == STATEMENT_ITEM)
    assert intake_item["state"] == "[_]" and intake_item["attempts"] == 1
    assert statement_item["state"] == "[ ]" and statement_item["attempts"] == 0
    assert statement_item["depends_on"] == [INTAKE_ITEM]
    assert statement_item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["item_id"] == intake["item_id"] == INTAKE_ITEM
    assert instance["canonical_statement"] == statement["canonical_statement"]
    formal = instance["canonical_formal_target"]
    statement_formal = statement["canonical_formal_target"]
    assert formal["module"] == statement_formal["module"]
    assert formal["declaration_or_expression"] == statement_formal["declaration_or_expression"]
    assert formal["elaborated_expression_hash"] == (
        f"sha256:{statement_formal['elaborated_expression_sha256']}"
    )
    assert instance["root_vector"] == statement["root_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R4",
    }
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    local_statement = next(row for row in dag["tasks"] if row["id"] == STATEMENT_ITEM)
    assert local_statement["state"] == "open"
    assert receipt["receipt_id"] in local_statement["evidence_ids"]
    assert dag["accepted_states"] == [] and dag["theorem_complete"] is False
    assert set(instance["owned_artifacts"]) == STATEMENT_FILES
    assert set(instance["public_merge_targets"]) == {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in STATEMENT_FILES
    }
    assert STATEMENT_FILES <= {path.name for path in HERE.iterdir() if path.is_file()}

    assert statement["item_id"] == receipt["item_id"] == STATEMENT_ITEM
    assert statement["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert statement["statement_elaborated"] is True
    assert statement["theorem_proved"] is False
    assert statement["audit_complete"] is statement["theorem_complete"] is False
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["selftest_result"] == "pass"
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []

    # Preserve the historical intake boundary rather than rewriting its receipt.
    assert intake["receipt_class"] == "provisional_worker_selftest"
    assert intake["accepted"] is False and intake["content_addressed"] is False
    assert intake["theorem_complete"] is False

    for name in STATEMENT_FILES:
        data = (HERE / name).read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {name}"
        assert b"\r" not in data and b"\x00" not in data, f"invalid bytes: {name}"
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), (
            f"trailing whitespace: {name}"
        )
    for name in (
        "README.md", "scope-map.md", "source-statement-crosswalk.md",
        "validation.md", "statement-validation.md",
    ):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    if args.worker_packet is not None:
        check_packet(args.worker_packet, receipt)

    print("dossier invariant check: ok (THM-M-0958 planned; exact statement H1/M3/R4; proof open)")


if __name__ == "__main__":
    main()
